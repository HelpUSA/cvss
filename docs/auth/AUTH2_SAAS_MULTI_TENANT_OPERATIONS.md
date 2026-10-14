# Auth-2 / SaaS Operations — Multi-Tenant Production Hardening

**Status:** partial implementation in Git; local/deployment work pending  
**Scope:** operational SaaS only; does not alter the frozen CVSS deterministic baseline.

## Implemented in this branch

### Google identity and canonical SuperAdmin

- Google OAuth remains the login provider through Better Auth.
- `PLATFORM_SUPERADMIN_EMAIL` defines the canonical platform SuperAdmin.
- Production canonical value: `helpus.ecommerce@gmail.com`.
- When Better Auth creates that Google user, the database hook assigns
  `PLATFORM_ADMIN` and ACTIVE status.
- A reconciliation command exists for an already-created Google user:

```bash
npm run auth:reconcile-google-superadmin
```

The reconciliation refuses to promote a user that is not linked to provider
`google`.

### Global user management

Added SuperAdmin-only global user administration:

- `GET /api/platform/users`
- `PATCH /api/platform/users/{userId}`
- `/app/admin/users`

Capabilities:

- list users and linked providers;
- view platform role, memberships and active sessions;
- ACTIVE / SUSPENDED / DISABLED lifecycle;
- revoke every session automatically when a user is suspended/disabled;
- promote/demote platform role only when the actor is the canonical
  SuperAdmin;
- protect the canonical SuperAdmin from suspension, disablement or demotion;
- append `SecurityAuditEvent` for global user mutation.

Platform role still does not grant implicit tenant access.

## Required production environment

Antigravity must configure production/preview secrets through the deployment
platform, never Git:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_URL`
- `AUTH_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `PLATFORM_SUPERADMIN_EMAIL=helpus.ecommerce@gmail.com`

The existing Google OAuth application must include the exact production and
approved preview callback URLs expected by Better Auth.

## Work intentionally not completed remotely

The following requires Antigravity/local infrastructure or a dedicated
implementation round.

### 1. Existing production database reconciliation

After deploying this branch:

1. take a database backup;
2. confirm the Google user exists;
3. confirm its Better Auth `Account.providerId = google`;
4. set `PLATFORM_SUPERADMIN_EMAIL`;
5. run `npm run auth:reconcile-google-superadmin`;
6. verify an audit event was produced;
7. sign out/in and confirm the SuperAdmin console;
8. verify a normal Google user is still `USER`.

Do not create a password credential for the canonical SuperAdmin.

### 2. Assessment persistence schema

Implement additive Prisma models for:

- `Assessment`
- `AssessmentRun`
- `EvidenceSnapshot`
- `AssessmentReview`
- optional `OrganizationPolicyVersion`
- optional `PlatformSetting`

Every model must be tenant-reachable through Environment -> Project ->
Organization and indexed for tenant-scoped access.

Existing legacy `Run` / `Assessment` research models must not be silently
repurposed without a migration plan; names may need `OperationalAssessment`
and `OperationalAssessmentRun` to avoid collision.

### 3. Authenticated operational analysis route

The current `POST /api/analyze-environment` is not tenant-authenticated.

Antigravity should:

1. extract its deterministic calculation into a shared service with no HTTP
   trust assumptions;
2. preserve the public route only as a rate-limited demo/compatibility route;
3. add a tenant-scoped route resolving session + membership server-side;
4. require `analysis:execute`;
5. validate project/environment ownership;
6. snapshot evidence before scoring;
7. persist an immutable run record and receipt digest;
8. never trust organization/project/role IDs supplied as authorization by the
   browser.

### 4. REVIEWER role

The existing REVIEWER role currently has zero operational permissions.

Implement:

- `decision:review`;
- tenant review queue;
- review decision model;
- approve/reject/request-evidence transitions;
- separation between scorer output and organizational approval;
- audit event for every review action.

### 5. SuperAdmin organization lifecycle

Implement platform routes/UI for:

- list/search organizations;
- ACTIVE / SUSPENDED / ARCHIVED state;
- organization usage summary;
- tenant ADMIN recovery/assignment under explicit rules;
- suspend organization -> block tenant operational execution without deleting
  historical evidence;
- archive only through a controlled lifecycle.

### 6. Platform settings

Implement a versioned `PlatformSetting` or equivalent, with audit history,
for:

- feature flags;
- per-tenant run quotas;
- rate limits;
- retention/export policy;
- allowed OAuth domains if later desired;
- maintenance mode;
- integration/service-account enablement;
- report-generation policy.

Secrets must never live in this table.

### 7. Evidence library

Add tenant/environment-scoped evidence snapshots:

- source type;
- source reference;
- capture time;
- freshness/expiry;
- canonical content hash;
- raw artifact storage reference;
- classification;
- uploader/integration identity.

Runs should reference snapshot IDs/hashes instead of depending only on an
ephemeral request body.

### 8. Audit hardening

Current `SecurityAuditEvent` is useful but mutable at the database layer.
Future hardening may add append-only controls, hash chaining and externally
anchored signed checkpoints. This is a product hardening control, not a CVSS
requirement.

### 9. Operational tests required

Before production cutover, add:

- Google login E2E for canonical SuperAdmin;
- Google login E2E for ordinary user;
- cross-tenant denial tests;
- global user suspend -> sessions revoked;
- canonical SuperAdmin cannot be disabled/demoted;
- non-canonical platform admin cannot change platform roles;
- tenant analysis cannot access another tenant's project/environment;
- public demo route cannot persist into a tenant;
- suspended organization cannot execute operational analysis.

## Recommended cutover

Do not redirect the public homepage straight into tenant execution until:

1. Google production OAuth is validated;
2. SuperAdmin reconciliation passes;
3. organization/user administration passes;
4. authenticated assessment persistence exists;
5. tenant-scoped analysis E2E is green.

Then present two explicit entry points:

- Public Demo / Scientific information
- Sign in to Operational Workspace
