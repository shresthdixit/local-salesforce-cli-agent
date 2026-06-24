# Agent Instructions

This repository uses the local Salesforce CLI agent scaffold in `agent/`.

Before doing Salesforce CLI, metadata, ticket-resolution, deployment-validation, FLS/CRUD, org-diff, Flow, or Apex-test work:

1. Read `agent/AGENT.md`.
2. Follow the relevant skill in `agent/skills/`.
3. Prefer the ticket workflow in `agent/skills/ticket-resolution.md` for Jira or pasted ticket context.
4. Prefer declarative automation using `agent/skills/flow-automation-first.md` before proposing Apex.
5. Run Salesforce CLI commands through `agent/scripts/sf_safe.py` when possible.
6. Never deploy, update, delete, change permissions, or run metadata writes without same-session approval.
7. Treat unknown org type as production until confirmed.
8. Use `agent/templates/change-set-summary.md` after approved sandbox validation or deployment.

Trace logs under `agent/traces/` are local audit artifacts and must not be committed except for `agent/traces/.gitkeep`.
