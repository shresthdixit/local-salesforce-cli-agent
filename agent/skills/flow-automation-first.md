# Flow Automation First

## Goal

Guide Salesforce admin-ticket solution design toward declarative automation before Apex, while still recognizing when Apex is the safer or more maintainable option.

## Pre-conditions

- Ticket context or user request describes a Salesforce behavior change, field/config change, validation, automation, or user-facing admin issue.
- Confirm target sandbox alias and org type before running commands.
- Do not deploy, update data, change permissions, or modify metadata without same-session approval.

## Steps

1. Action: Classify the requested change.
   Exact command if applicable: none.
   What to check in output: whether the ticket is best served by Flow, validation rule, formula field, field configuration, page/layout configuration, approval process, permission configuration, Apex, or a combination.

2. Action: Confirm sandbox context.
   Exact command if applicable:
   ```bash
   sf org display --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: sandbox indicators and target alias.

3. Action: Inspect existing schema before adding fields or automation.
   Exact command if applicable:
   ```bash
   sf sobject describe --sobject Account --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: existing fields, data types, requiredness, formula/calculated flags, and updateability.

4. Action: Retrieve relevant declarative metadata if not present locally.
   Exact command if applicable:
   ```bash
   sf project retrieve start --target-org MY_SANDBOX --manifest package.xml --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: Flow, CustomObject, CustomField, ValidationRule, Layout, PermissionSet, Profile, and ApprovalProcess metadata relevant to the ticket.

5. Action: Review branch changes and dependencies.
   Exact command if applicable:
   ```bash
   git diff
   # CONFIRMED: local Git read-only command.
   ```
   What to check in output: whether proposed or existing changes affect flows, validations, formulas, permissions, object metadata, layouts, Apex, or tests.

6. Action: Choose the simplest maintainable implementation path.
   Exact command if applicable: none.
   What to check in output: Flow before trigger, validation rule before Apex validation, formula before calculated Apex field, permission set before profile where appropriate, and configuration before code.

7. Action: Justify Apex only if needed.
   Exact command if applicable: none.
   What to check in output: Apex is justified only for complex transactions, bulk-safe logic that Flow cannot handle cleanly, callouts/integration constraints, reusable domain logic, recursion/performance control, or testability/maintainability reasons.

8. Action: Preview deployable metadata before approval.
   Exact command if applicable:
   ```bash
   sf project deploy preview --target-org MY_SANDBOX --manifest package.xml --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: Flow/version metadata, validation rules, fields, permissions, layouts, and unexpected Apex components.

9. Action: [REQUIRES APPROVAL] Validate declarative changes in sandbox.
   Exact command if applicable:
   ```bash
   sf project deploy start --dry-run --target-org MY_SANDBOX --test-level RunLocalTests --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: metadata validation failures, Flow errors, Apex test failures, and warnings.

## Stop conditions

- The ticket does not include enough business context or acceptance criteria.
- The target org is not confirmed as sandbox.
- The solution requires Apex but no declarative alternatives have been evaluated.
- Deploy preview includes unexpected Apex, destructive changes, or permission changes.
- Validation/deploy approval has not been granted in the same session.

## Output format

Return:

- Recommended implementation type.
- Declarative options considered.
- Apex justification, only if Apex is proposed.
- Metadata components affected.
- Test and validation plan.
- Risks, dependencies, and manual setup notes.
- Change-set members if the solution proceeds to release handoff.

## Verified commands

- CONFIRMED: CLI commands in this skill were verified against local sf CLI 2.139.6 help output.
- CONFIRMED: Git commands in this skill are local read-only commands.
