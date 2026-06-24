# Local Salesforce CLI Agent

A local, CLI-first Salesforce agent scaffold for safe ticket-driven sandbox workflows.

This repository gives Codex, Claude Code, GitHub Copilot, and human developers a shared operating model for Salesforce CLI work: investigate first, prefer declarative automation, protect production, require approval for risky commands, and produce release/change-set handoff notes.

## What This Does

This scaffold helps an AI assistant or developer:

- Start from Jira or pasted ticket context.
- Confirm target org alias and org type before running Salesforce commands.
- Prefer Flow, validation rules, formulas, field configuration, approval processes, and other declarative automation before Apex.
- Use read-only `sf` and Git commands before proposing changes.
- Ask clarifying questions when ticket requirements are incomplete.
- Treat unknown orgs as production-risk until confirmed otherwise.
- Require same-session approval for deploys, data writes, deletes, permission changes, and risky metadata operations.
- Run Salesforce CLI commands through a local policy wrapper: `agent/scripts/sf_safe.py`.
- Log command attempts locally while redacting likely secrets.
- Produce a release/change-set component summary after approved sandbox validation or deployment.

## What This Does Not Do

- It does not connect directly to Jira.
- It does not create Salesforce Change Sets in Setup.
- It does not provide hosted backend automation.
- It does not implement Salesforce MCP integration.
- It does not bypass Salesforce permissions.
- It does not replace CI/CD or release governance.

## Repository Layout

```text
AGENTS.md
CLAUDE.md
.github/copilot-instructions.md
agent/
  AGENT.md
  README.md
  safety-policy.md
  config/
    allowed-commands.yml
    org-policy.yml
  skills/
    apex-test-diagnosis.md
    deployment-validation.md
    flow-automation-first.md
    fls-crud-investigation.md
    org-diff.md
    ticket-resolution.md
  scripts/
    sf_safe.py
    collect_org_context.py
    run_apex_tests.py
  templates/
    change-set-summary.md
  traces/
    .gitkeep
  evals/
    test-scenarios.md
```

## Tool Integration

This repo includes lightweight bridge files so different coding assistants find the same Salesforce rules:

- `AGENTS.md`: for Codex and other agent-aware tools.
- `CLAUDE.md`: for Claude Code.
- `.github/copilot-instructions.md`: for GitHub Copilot.

The durable Salesforce source of truth is:

- `agent/AGENT.md`
- `agent/safety-policy.md`
- `agent/config/*.yml`
- `agent/skills/*.md`

## How To Use In An Existing Salesforce Repo

Copy these files into the root of the target Salesforce repo:

```text
agent/
AGENTS.md
CLAUDE.md
.github/copilot-instructions.md
.gitignore
```

If the target repo already has a `.gitignore`, merge these rules into it:

```gitignore
agent/traces/*
!agent/traces/.gitkeep
```

Then update:

- Replace `MY_SANDBOX` with the team sandbox alias, or keep it as an example placeholder.
- Review `agent/config/org-policy.yml` for scratch, sandbox, and production rules.
- Review `agent/config/allowed-commands.yml` whenever the Salesforce CLI version changes.
- Keep secrets, `.env` files, access tokens, and org credentials out of Git.

## How To Prompt An Assistant

For a Jira or ticket-driven request:

```text
Use agent/skills/ticket-resolution.md.
Work in sandbox only.
Prefer Flow/config/validation/formulas before Apex.
Use agent/scripts/sf_safe.py for Salesforce CLI commands where possible.
Produce a change-set summary.
```

For an admin automation request:

```text
Use agent/skills/flow-automation-first.md.
Evaluate declarative options before Apex.
Confirm org alias and org type before commands.
```

For deployment validation:

```text
Use agent/skills/deployment-validation.md.
Run git status and git diff first.
Do not deploy without explicit same-session approval.
```

## Quick Start

Preview a policy decision without executing the command:

```bash
python3 agent/scripts/sf_safe.py --dry-run "sf org display --target-org MY_SANDBOX --json"
```

Run a read-only org display command through the wrapper:

```bash
python3 agent/scripts/sf_safe.py "sf org display --target-org MY_SANDBOX --json"
```

Collect read-only org context:

```bash
python3 agent/scripts/collect_org_context.py --target-org MY_SANDBOX --output agent/traces/org-context.json
```

Run Apex tests through the wrapper:

```bash
python3 agent/scripts/run_apex_tests.py --target-org MY_SANDBOX --test-level RunLocalTests
```

## Safety Model

Command policy lives in `agent/config/allowed-commands.yml`.

Commands are grouped into:

- `allowed`: read-oriented commands such as org display, SOQL query, schema describe, deploy preview, deploy report, Apex test run/report, and Git read commands.
- `requires_approval`: deploys, validation deploys, data writes, permission changes, and deploy-resume operations.
- `blocked`: legacy namespace commands, destructive source deletes, dangerous deploy flags, destructive shell commands, and commands likely to expose secrets.

Org policy lives in `agent/config/org-policy.yml`.

The default stance is:

- scratch: allowed for local/dev work, with approval for risky operations
- sandbox: allowed for ticket work, with approval for risky operations
- production: deploys blocked by default
- unknown org type: treated as production-risk

## Main Capabilities

### Ticket Resolution

`agent/skills/ticket-resolution.md` turns Jira or pasted ticket text into:

- requirement summary
- missing questions
- impacted metadata list
- declarative-first solution proposal
- sandbox validation/deployment plan
- change-set component list

### Flow And Automation First

`agent/skills/flow-automation-first.md` helps the assistant prefer:

- Flow
- validation rules
- formulas
- field configuration
- approval processes
- permission configuration
- layout or Lightning page configuration

Apex should be proposed only when declarative options are insufficient, unsafe, or unmaintainable.

### CLI Safety Wrapper

`agent/scripts/sf_safe.py` provides:

- allowlist enforcement
- approval prompts for risky commands
- blocked-command refusal with policy reason
- org alias and org type display
- dry-run mode
- JSONL trace logging
- secret-pattern redaction

### Investigation Playbooks

The scaffold includes repeatable skills for:

- Apex test diagnosis
- FLS/CRUD investigation
- deployment validation
- org diff
- ticket resolution
- Flow/automation-first solution design

### Release Handoff

`agent/templates/change-set-summary.md` provides a standard output format for:

- ticket ID/title
- business requirement summary
- components changed
- suggested change-set members
- test evidence
- deployment or validation result
- manual setup or release notes

## Verified Salesforce CLI Version

The current command policy was checked against:

```text
@salesforce/cli/2.139.6 darwin-arm64 node-v22.22.3
```

If your team uses a different Salesforce CLI version, rerun `sf --version` and review `agent/config/allowed-commands.yml`.

## Where To Change Things Later

- Main agent behavior: `agent/AGENT.md`
- Human-readable policy: `agent/safety-policy.md`
- Command policy: `agent/config/allowed-commands.yml`
- Org rules: `agent/config/org-policy.yml`
- Ticket workflow: `agent/skills/ticket-resolution.md`
- Flow-first workflow: `agent/skills/flow-automation-first.md`
- Change-set format: `agent/templates/change-set-summary.md`
- Codex entrypoint: `AGENTS.md`
- Claude Code entrypoint: `CLAUDE.md`
- GitHub Copilot entrypoint: `.github/copilot-instructions.md`

## Current MCP Position

Salesforce MCP integration is intentionally not implemented in this scaffold. If a production MCP exists in your environment, treat it as read-only/informational for this workflow. Do not use production MCP for admin changes, metadata writes, data writes, permission changes, or deployments.
