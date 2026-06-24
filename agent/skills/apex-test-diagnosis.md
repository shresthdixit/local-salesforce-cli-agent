# Apex Test Diagnosis

## Goal

Diagnose Apex test failures using read-only evidence, bounded retries, and structured reporting.

## Pre-conditions

- Confirm target org alias: `MY_SANDBOX` or a user-provided alias.
- Confirm org type before running commands.
- Stop if org type is unknown; treat it as production until confirmed.
- Maximum 3 failed command attempts before reporting.

## Steps

1. Action: Confirm org context.
   Exact command if applicable:
   ```bash
   sf org display --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: alias, username, org id, and sandbox/scratch/production indicators.

2. Action: Review local metadata changes before interpreting failures.
   Exact command if applicable:
   ```bash
   git status
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: changed Apex classes, triggers, flows, and tests.

3. Action: Inspect local diff for likely test-impacting changes.
   Exact command if applicable:
   ```bash
   git diff
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: changed logic, validation assumptions, selectors, triggers, permissions, and test data setup.

4. Action: Run targeted or local Apex tests.
   Exact command if applicable:
   ```bash
   sf apex run test --target-org MY_SANDBOX --test-level RunLocalTests --result-format json --wait 10
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: failing method names, stack traces, assertion messages, exception types, and run id.

5. Action: Fetch a known test run result if a run id exists.
   Exact command if applicable:
   ```bash
   sf apex get test --test-run-id <TEST_RUN_ID> --target-org MY_SANDBOX --result-format json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: detailed failures and code locations.

## Stop conditions

- Org alias or org type is unknown.
- Any command fails 3 times.
- Failure cause is not supported by evidence.
- A fix would require metadata changes; stop, summarize evidence, and ask before proposing changes.

## Output format

Return:

- Target org alias and type.
- Commands run.
- Failing tests and exact failure evidence.
- Likely cause with confidence level.
- Relevant local diff evidence.
- Recommended next step.

## Assumptions

- CONFIRMED: CLI commands in this skill were verified against local sf CLI 2.139.6 help output.
