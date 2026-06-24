#!/usr/bin/env python3
"""Run Apex tests through sf_safe.py and stop after bounded retries."""

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SAFE = ROOT / "scripts" / "sf_safe.py"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Apex tests with local policy enforcement.")
    parser.add_argument("--target-org", default="MY_SANDBOX")
    parser.add_argument("--test-level", default="RunLocalTests")
    parser.add_argument("--class-names", default="", help="Comma-separated Apex test class names.")
    parser.add_argument("--max-attempts", type=int, default=3)
    args = parser.parse_args()

    command = (
        f"sf apex run test --target-org {args.target_org} --test-level {args.test_level} "
        "--result-format json --wait 10"
    )  # CONFIRMED: verified against local sf CLI 2.139.6 help output.
    if args.class_names:
        command += f" --class-names {args.class_names}"  # CONFIRMED: verified against local sf CLI 2.139.6 help output.

    for attempt in range(1, args.max_attempts + 1):
        print(f"Apex test attempt {attempt} of {args.max_attempts}")
        result = subprocess.run([sys.executable, str(SAFE), command], check=False)
        if result.returncode == 0:
            print("Apex test command completed successfully.")
            return 0
    print("Stopped after 3 failed attempts. Report the failures and request manual review.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
