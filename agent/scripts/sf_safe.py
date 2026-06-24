#!/usr/bin/env python3
"""Local Salesforce CLI safety wrapper."""

import argparse
import datetime as dt
import getpass
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
TRACES_DIR = ROOT / "traces"
ALLOWED_PATH = CONFIG_DIR / "allowed-commands.yml"
ORG_POLICY_PATH = CONFIG_DIR / "org-policy.yml"
SECRET_40_RE = re.compile(r"\b[A-Za-z0-9]{40,}\b")
SECRET_FLAG_RE = re.compile(r"(--(?:access-token|client-secret)(?:\s+|=))([^\s]+)", re.IGNORECASE)


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def load_simple_yaml(path: Path) -> Dict[str, Any]:
    """Parse the intentionally constrained YAML used by this scaffold.

    # CONFIRMED: this constrained parser supports this scaffold's config format.
    """
    data: Dict[str, Any] = {}
    current_list: Optional[str] = None
    current_item: Optional[Dict[str, Any]] = None
    current_map: Optional[str] = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if indent == 0 and line.endswith(":"):
            key = line[:-1]
            if key in {"allowed", "requires_approval", "blocked"}:
                data[key] = []
                current_list = key
                current_map = None
            else:
                data[key] = {}
                current_map = key
                current_list = None
            current_item = None
        elif indent == 0 and ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = parse_scalar(value)
            current_list = None
            current_map = None
            current_item = None
        elif current_list and line.startswith("- "):
            current_item = {}
            data[current_list].append(current_item)
            rest = line[2:]
            if ":" in rest:
                key, value = rest.split(":", 1)
                current_item[key.strip()] = parse_scalar(value)
        elif current_list and current_item is not None and ":" in line:
            key, value = line.split(":", 1)
            current_item[key.strip()] = parse_scalar(value)
        elif current_map and ":" in line:
            key, value = line.split(":", 1)
            data[current_map][key.strip()] = parse_scalar(value)
    return data


def redact(value: str) -> str:
    value = SECRET_FLAG_RE.sub(lambda match: match.group(1) + "[REDACTED]", value)
    return SECRET_40_RE.sub("[REDACTED]", value)


def normalize(command: str) -> str:
    return " ".join(shlex.split(command))


def parse_base_command(command: str) -> str:
    parts = shlex.split(command)
    return " ".join(parts[:4])


def find_policy(command: str, policy: Dict[str, Any]) -> Dict[str, str]:
    normalized = normalize(command)
    for entry in policy.get("blocked", []):
        pattern = entry.get("pattern", "")
        if pattern and (normalized.startswith(pattern) or pattern in normalized):
            return {"decision": "blocked", "reason": entry.get("reason", "Blocked by policy."), "pattern": pattern}
    for entry in policy.get("requires_approval", []):
        pattern = entry.get("pattern", "")
        if pattern and normalized.startswith(pattern):
            return {"decision": "requires_approval", "reason": entry.get("reason", "Requires approval."), "pattern": pattern}
    for entry in policy.get("allowed", []):
        pattern = entry.get("pattern", "")
        if pattern and normalized.startswith(pattern):
            return {"decision": "allowed", "reason": entry.get("reason", "Allowed by policy."), "pattern": pattern}
    return {"decision": "blocked", "reason": "Command is not in the allowlist.", "pattern": parse_base_command(command)}


def target_org_from_command(command: str) -> Optional[str]:
    parts = shlex.split(command)
    for index, part in enumerate(parts):
        if part in {"--target-org", "-o"} and index + 1 < len(parts):
            return parts[index + 1]
        if part.startswith("--target-org="):
            return part.split("=", 1)[1]
    return None


def infer_org_type(payload: Dict[str, Any]) -> str:
    # TODO: Confirm exact production org detection rules for this environment.
    result = payload.get("result", payload)
    org_type = str(result.get("orgType") or result.get("edition") or "").lower()
    username = str(result.get("username") or result.get("alias") or "").lower()
    instance_url = str(result.get("instanceUrl") or "").lower()
    if result.get("isScratchOrg") is True or "scratch" in org_type:
        return "scratch"
    if result.get("isSandbox") is True or "sandbox" in org_type or "sandbox" in username or "test.salesforce.com" in instance_url:
        return "sandbox"
    if result.get("isSandbox") is False or "production" in org_type:
        return "production"
    return "unknown"


def get_org_context(command: str) -> Dict[str, str]:
    if not normalize(command).startswith("sf "):
        return {"org_alias": "N/A", "org_type": "local"}
    org_alias = target_org_from_command(command) or "UNKNOWN"
    if org_alias == "UNKNOWN":
        cmd = ["sf", "org", "display", "--json"]
    else:
        cmd = ["sf", "org", "display", "--target-org", org_alias, "--json"]
    # CONFIRMED: verified against local sf CLI 2.139.6 help output.
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        if completed.returncode != 0:
            return {"org_alias": org_alias, "org_type": "unknown"}
        payload = json.loads(completed.stdout or "{}")
        result = payload.get("result", payload)
        resolved_alias = org_alias
        if resolved_alias == "UNKNOWN":
            resolved_alias = str(result.get("alias") or result.get("username") or "UNKNOWN")
        return {"org_alias": resolved_alias, "org_type": infer_org_type(payload)}
    except Exception:
        return {"org_alias": org_alias, "org_type": "unknown"}


def apply_org_policy(decision: Dict[str, str], org_type: str, org_policy: Dict[str, Any]) -> Dict[str, str]:
    policy_type = org_type if org_type in org_policy else "production"
    rules = org_policy.get(policy_type, {})
    if decision["decision"] == "requires_approval" and rules.get("blocked_entirely"):
        return {
            "decision": "blocked",
            "reason": rules.get("blocked_reason", "Org policy blocks this command."),
            "pattern": decision.get("pattern", ""),
        }
    return decision


def log_attempt(
    command: str,
    org_alias: str,
    org_type: str,
    decision: str,
    exit_code: Optional[int],
    approved_by: Optional[str] = None,
) -> None:
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "command": redact(command),
        "org_alias": redact(org_alias),
        "org_type": org_type,
        "policy_decision": decision,
        "exit_code": exit_code,
    }
    if approved_by:
        record["approved_by"] = redact(approved_by)
    path = TRACES_DIR / f"sf_safe-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d')}.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local Salesforce CLI commands through a safety wrapper.")
    parser.add_argument("--dry-run", action="store_true", help="Show policy decision without executing.")
    parser.add_argument("command", help="Command string to evaluate and optionally execute.")
    args = parser.parse_args()

    command = args.command.strip()
    policy = load_simple_yaml(ALLOWED_PATH)
    org_policy = load_simple_yaml(ORG_POLICY_PATH)
    context = get_org_context(command)
    decision = apply_org_policy(find_policy(command, policy), context["org_type"], org_policy)

    print(f"Target org alias: {context['org_alias']}")
    print(f"Target org type: {context['org_type']}")
    print(f"Policy decision: {decision['decision']} ({decision['reason']})")

    if args.dry_run:
        log_attempt(command, context["org_alias"], context["org_type"], "dry_run:" + decision["decision"], None)
        print("Dry run only. Command was not executed.")
        return 0 if decision["decision"] != "blocked" else 2

    if context["org_alias"] == "UNKNOWN" or context["org_type"] == "unknown":
        log_attempt(command, context["org_alias"], context["org_type"], "blocked:unknown_org", 2)
        print("Refusing to run: target org alias or type is unknown. Confirm it first.", file=sys.stderr)
        return 2

    if decision["decision"] == "blocked":
        log_attempt(command, context["org_alias"], context["org_type"], "blocked", 2)
        print(f"Refusing to run command: {decision['reason']}", file=sys.stderr)
        return 2

    if decision["decision"] == "requires_approval":
        print("This command requires explicit approval in this session.")
        print(f"Command: {redact(command)}")
        approved = input("Type yes to approve: ").strip()
        if approved != "yes":
            log_attempt(command, context["org_alias"], context["org_type"], "approval_denied", 3)
            print("Approval not granted. Command was not executed.")
            return 3
        log_attempt(command, context["org_alias"], context["org_type"], "approval_granted", None, approved_by=getpass.getuser())

    completed = subprocess.run(shlex.split(command), check=False)
    log_attempt(command, context["org_alias"], context["org_type"], decision["decision"], completed.returncode)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
