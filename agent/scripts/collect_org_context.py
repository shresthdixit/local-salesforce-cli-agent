#!/usr/bin/env python3
"""Collect a read-only org context snapshot through sf_safe.py."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SAFE = ROOT / "scripts" / "sf_safe.py"


def run_safe(command: str) -> int:
    return subprocess.run([sys.executable, str(SAFE), command], check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect read-only org context.")
    parser.add_argument("--target-org", default="MY_SANDBOX")
    parser.add_argument("--output", default=str(ROOT / "traces" / "org-context.json"))
    args = parser.parse_args()

    commands = [
        f"sf org display --target-org {args.target_org} --json",  # CONFIRMED: verified against local sf CLI 2.139.6 help output.
        "sf org list --json",  # CONFIRMED: verified against local sf CLI 2.139.6 help output.
    ]
    results = []
    for command in commands:
        code = run_safe(command)
        results.append({"command": command, "exit_code": code})
        if code != 0:
            break

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"target_org": args.target_org, "commands": results}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote read-only context command summary to {output}")
    return 0 if all(item["exit_code"] == 0 for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
