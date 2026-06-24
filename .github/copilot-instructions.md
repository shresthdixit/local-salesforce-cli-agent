# GitHub Copilot Repository Instructions

This is a Salesforce CLI-oriented repository with a local agent scaffold under `agent/`.

For Salesforce ticket, metadata, Flow, Apex, FLS/CRUD, org-diff, deployment-validation, or CLI work:

- Read and follow `agent/AGENT.md`.
- Use `agent/skills/ticket-resolution.md` for Jira or pasted ticket context.
- Use `agent/skills/flow-automation-first.md` before proposing Apex for admin-style changes.
- Use `agent/scripts/sf_safe.py` for Salesforce CLI commands when possible.
- Confirm target org alias and org type before commands.
- Treat unknown org type as production.
- Do not deploy, update, delete, change permissions, or run metadata-write commands without explicit same-session user approval.
- For sandbox validation or deployment handoff, produce `agent/templates/change-set-summary.md`.

Do not commit trace logs from `agent/traces/`; only `agent/traces/.gitkeep` should be tracked.
