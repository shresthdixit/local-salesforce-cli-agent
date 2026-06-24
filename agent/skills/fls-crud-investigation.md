# FLS CRUD Investigation

## Goal

Investigate field-level security, object CRUD, and user access issues with structured evidence instead of yes/no answers.

## Pre-conditions

- Confirm target org alias and org type.
- Identify user, profile, permission set, object, and field from the prompt or ask for missing inputs.
- Use read-only SOQL and schema describe only.

## Steps

1. Action: Confirm org context.
   Exact command if applicable:
   ```bash
   sf org display --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: alias, username, and org type indicators.

2. Action: Describe the object schema.
   Exact command if applicable:
   ```bash
   sf sobject describe --sobject Account --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: field existence, createable, updateable, nillable, calculated, and permission-related metadata.

3. Action: Query field permissions for the target field.
   Exact command if applicable:
   ```bash
   sf data query --query "SELECT Parent.Profile.Name, Parent.Label, SObjectType, Field, PermissionsRead, PermissionsEdit FROM FieldPermissions WHERE SObjectType = 'Account' AND Field = 'Account.AnnualRevenue'" --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: whether relevant profile or permission set grants read/edit access.

4. Action: Query object permissions for the target object.
   Exact command if applicable:
   ```bash
   sf data query --query "SELECT Parent.Profile.Name, Parent.Label, SObjectType, PermissionsRead, PermissionsCreate, PermissionsEdit, PermissionsDelete FROM ObjectPermissions WHERE SObjectType = 'Account'" --target-org MY_SANDBOX --json
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: object-level read/create/edit/delete permissions.

5. Action: Search local code for user-mode and system-mode behavior.
   Exact command if applicable:
   ```bash
   git diff
   # CONFIRMED: verified against local sf CLI 2.139.6 help output.
   ```
   What to check in output: Apex data access mode, selectors, sharing declarations, flows, LWC usage, and permission assumptions.

## Stop conditions

- User/profile/permission set context is missing and cannot be inferred.
- Org type is unknown.
- Permission change is needed; mark it [REQUIRES APPROVAL] and stop.
- Evidence is incomplete or contradictory.

## Output format

Return:

- Target org alias and type.
- Object and field investigated.
- User/profile/permission set context.
- FieldPermissions evidence.
- ObjectPermissions evidence.
- Schema describe evidence.
- Local code evidence.
- Risk summary and recommended next step.

## Assumptions

- CONFIRMED: CLI commands in this skill were verified against local sf CLI 2.139.6 help output.
