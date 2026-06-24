# Safety Policy

This scaffold protects local Salesforce development workflows by defaulting to read-only investigation, explicit command allowlists, conservative org policy, and trace logging.

## Policy summary

- Read-only commands may run through `agent/scripts/sf_safe.py` when they match `agent/config/allowed-commands.yml`.
- Deploy, data write, delete, permission-change, destructive, and release commands require same-session approval or are blocked.
- Production is blocked for deploys by default.
- Unknown org type is treated as production until confirmed.
- Every command attempt is logged as JSON Lines in `agent/traces/` with secrets redacted.
- Command output is not logged by default.
- No org aliases, usernames, instance URLs, access tokens, client secrets, or credentials are hardcoded.
- TODO: Confirm the official Salesforce MCP server status before adding any MCP integration. This scaffold contains no MCP code.
- Production MCP, if available outside this scaffold, is informational/read-only only. Do not use it for admin ticket changes, metadata writes, data writes, permission changes, or deployment work.

## Required refusal behavior

When a command is blocked, the agent must print a clear refusal message that includes the policy reason and exit non-zero.

## Approval behavior

When a command requires approval, the agent must show the command, target org alias, target org type, and risk reason. The user must type `yes` in the same session before execution.
