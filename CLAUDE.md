# Claude Code Instructions

@AGENTS.md

## Claude-Specific Notes

- Use `agent/AGENT.md` as the source of truth for Salesforce CLI work.
- For Jira or pasted ticket context, use `agent/skills/ticket-resolution.md`.
- For admin-style requests, prefer `agent/skills/flow-automation-first.md` before Apex.
- `CLAUDE.md` is an instruction file, not an enforcement mechanism; risky Salesforce commands must still go through `agent/scripts/sf_safe.py` where possible.
