# Deployment Validation

## Goal

Validate branch metadata safely before deployment, using Git evidence and approval-gated validation commands.

## Pre-conditions

- Confirm target org alias and org type.
- Run `git status` and `git diff` before proposing metadata changes.
- Production deploys are blocked by default.
- Validation-only deploy commands still require explicit same-session approval.

## Steps

1. Action: Confirm org context.
   Exact command if applicable:
   ```bash
   sf org display --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: alias and org type. Treat unknown as production.

2. Action: Check repository status.
   Exact command if applicable:
   ```bash
   git status
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: staged, unstaged, and untracked metadata.

3. Action: Review metadata diff.
   Exact command if applicable:
   ```bash
   git diff
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: Apex, Flow, profile, permission set, object, field, and destructive changes.

4. Action: [REQUIRES APPROVAL] Run validation-only deploy.
   Exact command if applicable:
   ```bash
   sf project deploy start --dry-run --target-org MY_SANDBOX --test-level RunLocalTests --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: component failures, test failures, warnings, and deployment id.

## Stop conditions

- Target org type is production or unknown.
- User has not explicitly approved the validation command in the same session.
- Diff includes destructive changes, permission changes, or high-risk metadata.
- Validation fails or has warnings requiring review.

## Output format

Return:

- Target org alias and type.
- Git status summary.
- Changed metadata summary.
- Validation command approval status.
- Validation result evidence.
- Release risk summary.
- Recommended next step.

## Assumptions

- CONFIRMED: CLI commands in this skill were verified against local sf CLI 2.139.6 help output.
