# Ticket Resolution

## Goal

Resolve a Salesforce ticket from Jira or pasted ticket context by extracting requirements, investigating metadata safely, proposing a declarative-first solution, deploying only to sandbox after approval, and producing a release/change-set component list.

## Pre-conditions

- Ticket context is provided by the user, Claude, Codex, GitHub Copilot, or pasted Jira text. Do not call Jira APIs in this scaffold.
- Confirm target org alias and type before any command.
- If the user does not provide an alias, use the current Salesforce CLI default target org after `sf org display --json` confirms it is a sandbox. This can be the same authenticated sandbox used by the Salesforce extension in VS Code if it is also configured for the local `sf` CLI.
- Target org must be a sandbox for deploy, validation, data write, permission-change, or metadata-change work.
- If the ticket lacks acceptance criteria, target object/field, affected user persona, automation trigger, or deployment expectation, ask clarifying questions before proposing a final solution.
- Use `agent/skills/flow-automation-first.md` for solution design before proposing Apex.

## Steps

1. Action: Extract ticket intent and gaps.
   Exact command if applicable: none.
   What to check in output: ticket ID/title, business problem, acceptance criteria, affected users, target objects/fields, expected timing, and missing questions.

2. Action: Confirm sandbox context.
   Exact command if applicable:
   ```bash
   sf org display --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   Or, when the user provides an explicit alias:
   ```bash
   sf org display --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: alias, username, org id, instance URL, and sandbox indicators. Stop if org type is production or unknown.

3. Action: Inspect local branch changes before proposing metadata changes.
   Exact command if applicable:
   ```bash
   git status
   # CONFIRMED: local Git read-only command.
   ```
   What to check in output: unstaged, staged, and untracked files related to the ticket.

4. Action: Review local metadata diff.
   Exact command if applicable:
   ```bash
   git diff
   # CONFIRMED: local Git read-only command.
   ```
   What to check in output: changed Flow, object, field, validation rule, permission, layout, Apex, and test metadata.

5. Action: Inspect object schema for impacted objects.
   Exact command if applicable:
   ```bash
   sf sobject describe --sobject Account --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: existing fields, field data types, formula/calculated flags, createable/updateable flags, and existing schema that may satisfy the requirement.

6. Action: Query read-only supporting data when needed.
   Exact command if applicable:
   ```bash
   sf data query --query "SELECT Id, Name FROM Account LIMIT 10" --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: record shape, values needed to reproduce the ticket, and whether the ticket has enough data evidence.

7. Action: Retrieve focused metadata if local source is incomplete.
   Exact command if applicable:
   ```bash
   sf project retrieve start --target-org MY_SANDBOX --manifest package.xml --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: retrieved components, warnings, failures, and whether retrieved metadata matches ticket scope.

8. Action: Preview deployable metadata before approval.
   Exact command if applicable:
   ```bash
   sf project deploy preview --target-org MY_SANDBOX --manifest package.xml --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: deployable components, conflicts, deletes, ignored files, and missing components for the change-set list.

9. Action: Present proposed solution and ask for approval.
   Exact command if applicable: none.
   What to check in output: declarative-first design, metadata impact list, test plan, risks, and explicit approval request.

10. Action: [REQUIRES APPROVAL] Validate or deploy to sandbox only after approval.
    Exact command if applicable:
    ```bash
    sf project deploy start --dry-run --target-org MY_SANDBOX --test-level RunLocalTests --json
    # CONFIRMED: verified against local sf CLI 2.139.6 help output.
    ```
    What to check in output: component successes/failures, test results, warnings, and job id. Use a real sandbox deploy command only if the user explicitly approves deploying, not just validating.

11. Action: Read deploy or validation status when a job id is available.
    Exact command if applicable:
    ```bash
    sf project deploy report --target-org MY_SANDBOX --job-id <JOB_ID> --json
    # CONFIRMED: verified against local sf CLI 2.139.6 help output.
    ```
    What to check in output: final status, component results, test results, and warnings.

12. Action: Produce release/change-set summary.
    Exact command if applicable: none.
    What to check in output: use `agent/templates/change-set-summary.md` and include every changed component needed for release handoff.

## Stop conditions

- Ticket requirements or acceptance criteria are too vague to design safely.
- Target org alias/username or type is unknown.
- Target org is production and the requested work is deploy, update, delete, permission-change, or metadata-change work.
- The proposed solution requires Apex before declarative alternatives have been evaluated.
- User has not approved validation or deployment in the same session.
- Deploy preview shows conflicts, deletes, ignored files, or missing components that need human review.
- Any command fails 3 times.

## Output format

Return:

- Ticket ID/title.
- Requirement summary and acceptance criteria.
- Clarifying questions, if any.
- Confirmed target org alias and type.
- Evidence gathered.
- Declarative-first proposed solution.
- Metadata impact list.
- Test plan and test evidence.
- Approval status for validation/deploy.
- Change-set/component summary using `agent/templates/change-set-summary.md`.
- Open release notes or manual setup steps.

## Verified commands

- CONFIRMED: CLI commands in this skill were verified against local sf CLI 2.139.6 help output.
- CONFIRMED: Git commands in this skill are local read-only commands.
