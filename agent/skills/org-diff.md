# Org Diff

## Goal

Compare metadata evidence from two orgs without writing to either org.

## Pre-conditions

- Confirm both source and comparison org aliases and org types.
- Treat unknown org type as production and stop.
- Use retrieval and Git/file diff evidence only.

## Steps

1. Action: Confirm first org context.
   Exact command if applicable:
   ```bash
   sf org display --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: alias and org type.

2. Action: Confirm second org context.
   Exact command if applicable:
   ```bash
   sf org display --target-org <OTHER_ORG_ALIAS> --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: alias and org type.

3. Action: Review local changed metadata to focus the diff.
   Exact command if applicable:
   ```bash
   git diff
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: relevant components to retrieve or compare.

4. Action: Retrieve metadata from an org using a manifest.
   Exact command if applicable:
   ```bash
   sf project retrieve start --target-org MY_SANDBOX --manifest package.xml --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: retrieved components, warnings, and failures.

5. Action: Compare retrieved metadata with local Git tooling.
   Exact command if applicable:
   ```bash
   git diff
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: meaningful XML or source differences after ignoring generated noise.

## Stop conditions

- Either org alias or org type is unknown.
- Retrieval fails 3 times.
- A write/deploy command would be needed.
- Differences cannot be attributed to stable metadata rather than generated noise.

## Output format

Return:

- Org aliases and types.
- Manifest or component scope used.
- Commands run.
- Meaningful differences grouped by metadata type.
- Ignored noise categories.
- Risks and recommended next step.

## Assumptions

- CONFIRMED: CLI commands in this skill were verified against local sf CLI 2.139.6 help output.
