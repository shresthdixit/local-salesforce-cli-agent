# Local Salesforce CLI Agent Scaffold

## Should this be committed?

Yes, commit this scaffold to Git after review. It is meant to be shared with the team as repository guidance and local safety tooling.

Commit:

- `agent/`
- `.gitignore`
- `AGENTS.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`

Do not commit:

- `agent/traces/*.jsonl`
- local auth files, `.env` files, access tokens, org credentials, or personal sandbox notes
- generated `__pycache__` or `.pyc` files

The PDF architecture document is optional. Commit it only if the team wants the original design artifact in source control.

## What this scaffold does

This is a local, CLI-first Salesforce assistant scaffold. It gives Codex, Claude Code, GitHub Copilot, and human developers a shared operating model for safe Salesforce work.

It helps an assistant:

- Start from Jira or pasted ticket context.
- Confirm target org alias and org type before commands.
- Prefer Flow, validation rules, formulas, fields, approval processes, and other declarative automation before Apex.
- Investigate with read-only `sf` and Git commands first.
- Ask clarifying questions when ticket requirements are incomplete.
- Keep production protected by treating unknown orgs as production.
- Require same-session approval for deploys, data writes, permission changes, deletes, and other risky work.
- Run Salesforce CLI commands through `agent/scripts/sf_safe.py` where possible.
- Log command attempts locally while redacting likely secrets.
- Produce a release/change-set component summary after approved sandbox validation or deployment.

It does not:

- Connect directly to Jira.
- Create Salesforce Change Sets in Setup.
- Provide hosted backend automation.
- Implement Salesforce MCP integration.
- Bypass Salesforce permissions or replace CI/CD.

## How to add this to an existing repo

1. Copy these files into the root of the existing Salesforce repo:

   ```text
   agent/
   AGENTS.md
   CLAUDE.md
   .github/copilot-instructions.md
   .github/agents/salesforce-ticket-agent.agent.md
   .gitignore
   ```

2. Merge `.gitignore` carefully if the target repo already has one. Keep these rules:

   ```gitignore
   agent/traces/*
   !agent/traces/.gitkeep
   ```

3. Update placeholders:

   - Replace `MY_SANDBOX` with the team sandbox alias, keep it as an example placeholder, or rely on the current Salesforce CLI default target org after the agent confirms it is a sandbox.
   - Review `agent/config/org-policy.yml` for your scratch, sandbox, and production rules.
   - Review `agent/config/allowed-commands.yml` after Salesforce CLI upgrades.

4. In each assistant, start from the bridge file it naturally reads:

   - Codex: `AGENTS.md`
   - Claude Code: `CLAUDE.md`
   - GitHub Copilot: `.github/copilot-instructions.md`

5. For a Jira ticket, paste the ticket text and ask:

   ```text
   Use agent/skills/ticket-resolution.md. Work in sandbox only. Prefer Flow/config before Apex. Produce a change-set summary.
   ```

   If your Salesforce extension in VS Code is already using the same default org as the local `sf` CLI, you can say:

   ```text
   Use the current Salesforce CLI default target org if it is confirmed as sandbox.
   ```

6. For CLI commands, prefer:

   ```bash
   python3 agent/scripts/sf_safe.py --dry-run "sf org display --target-org MY_SANDBOX --json"
   ```

## Tool integration files

This scaffold includes lightweight bridge files so each assistant finds the same Salesforce rules without duplicating them:

- `AGENTS.md` points Codex and agent-aware tools to `agent/AGENT.md`.
- `CLAUDE.md` imports `AGENTS.md` and adds Claude-specific notes.
- `.github/copilot-instructions.md` points GitHub Copilot to the same scaffold.

The durable source of truth remains `agent/AGENT.md` plus the skill files under `agent/skills/`.

## Capabilities

### Ticket resolution

Use `agent/skills/ticket-resolution.md` to turn Jira or pasted ticket text into:

- requirement summary
- missing questions
- impacted metadata list
- declarative-first solution proposal
- sandbox validation/deployment plan
- change-set component list

### Flow and automation first

Use `agent/skills/flow-automation-first.md` when the ticket involves admin work, Flow, validation, fields, formulas, approval processes, permissions, or automation. Apex should be proposed only when declarative options are insufficient, unsafe, or unmaintainable.

### CLI safety

Use `agent/scripts/sf_safe.py` to enforce:

- allowed read-only command patterns
- approval-required risky command patterns
- blocked dangerous command patterns
- org policy for scratch, sandbox, and production
- trace logging with secret redaction

### Investigation playbooks

Use the skill files for repeatable workflows:

- Apex test diagnosis
- FLS/CRUD investigation
- deployment validation
- org diff
- ticket resolution
- Flow/automation-first solution design

### Release handoff

Use `agent/templates/change-set-summary.md` after approved sandbox validation or deployment to produce a component-level release handoff for Change Sets or release review.

## Where to change things later

- Change agent behavior: edit `agent/AGENT.md`.
- Add or refine a workflow: edit or add files under `agent/skills/`.
- Change command policy: edit `agent/config/allowed-commands.yml`.
- Change org safety rules: edit `agent/config/org-policy.yml`.
- Change release handoff format: edit `agent/templates/change-set-summary.md`.
- Change Codex/Claude/Copilot entry instructions: edit `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`.

## Verified command syntax

These commands were checked against the installed Salesforce CLI on this machine: `@salesforce/cli/2.139.6 darwin-arm64 node-v22.22.3`.

- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf org display --target-org MY_SANDBOX --json`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf org list --json`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf org list users --target-org MY_SANDBOX --json`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf data query --query "..." --target-org MY_SANDBOX --json`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf sobject describe --sobject Account --target-org MY_SANDBOX --json`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf project retrieve start --target-org MY_SANDBOX --manifest package.xml --json`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf project deploy preview --target-org MY_SANDBOX --manifest package.xml --json`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf project deploy report --target-org MY_SANDBOX --job-id <JOB_ID> --json`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf project deploy start --dry-run --target-org MY_SANDBOX --test-level RunLocalTests --json`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf apex run test --target-org MY_SANDBOX --test-level RunLocalTests --result-format json --wait 10`.
- CONFIRMED: verified against local sf CLI 2.139.6 help output. `sf apex get test --test-run-id <TEST_RUN_ID> --target-org MY_SANDBOX --result-format json`.
- CONFIRMED: local Git read-only commands. `git status`, `git diff`, and `git log`.
- CONFIRMED: Python standard-library only. The constrained YAML reader in `agent/scripts/sf_safe.py` needs no extra package install.

## TODO decisions from open questions

- TODO: Confirm the official Salesforce MCP server status before adding any MCP integration. This scaffold intentionally contains no MCP integration code.
- TODO: Decide exact production org detection rules for this environment beyond conservative inference from `sf org display --json`.

## Setup

1. Install and authenticate the Salesforce CLI.
2. Confirm Python 3 is available.
3. Review `agent/config/allowed-commands.yml` and `agent/config/org-policy.yml`.
4. Replace the placeholder sandbox alias `MY_SANDBOX` with your real sandbox alias when ready.
5. Keep `agent/traces/` out of Git content. The included `.gitignore` keeps only `.gitkeep`.

## Quick start

Preview policy decision:

```bash
python3 agent/scripts/sf_safe.py --dry-run "sf org display --target-org MY_SANDBOX --json"
# CONFIRMED: verified against local sf CLI 2.139.6 help output.
```

Use the current default target org:

```bash
python3 agent/scripts/sf_safe.py --dry-run "sf org display --json"
# CONFIRMED: verified against local sf CLI 2.139.6 help output.
```

Run a read-only command:

```bash
python3 agent/scripts/sf_safe.py "sf org display --target-org MY_SANDBOX --json"
# CONFIRMED: verified against local sf CLI 2.139.6 help output.
```

Collect context:

```bash
python3 agent/scripts/collect_org_context.py --target-org MY_SANDBOX --output agent/traces/org-context.json
# CONFIRMED: verified against local sf CLI 2.139.6 help output.
```

Run Apex tests:

```bash
python3 agent/scripts/run_apex_tests.py --target-org MY_SANDBOX --test-level RunLocalTests
# CONFIRMED: verified against local sf CLI 2.139.6 help output.
```

## Usage model

The agent follows `agent/AGENT.md`, starts with read-only evidence, confirms org alias and type before commands, stops after each investigation phase, and requires same-session approval for risky commands.

For Gabriela-style ticket work, paste the Jira ticket context into the assistant and ask it to use `agent/skills/ticket-resolution.md`. The workflow is sandbox-first, declarative-first, and produces a release/change-set component list after approval-based validation or deployment.

## MCP status

TODO: MCP integration is scaffold-only. Do not add MCP server integration code until official release status, auth, command surface, and governance rules are confirmed.
