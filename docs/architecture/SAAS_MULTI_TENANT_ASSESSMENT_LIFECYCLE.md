# HelpUS CVSS Operational SaaS — Multi-Tenant Assessment Lifecycle

**Status:** implementation blueprint  
**Scientific baseline:** unchanged; frozen deterministic scoring baseline remains `007fe79a6cd0e843fe6a9f837444720e23a4bcad`.

## 1. Product boundary

The public site may remain open for institutional content and a limited
demonstration. Operational analysis must run inside an authenticated workspace.

Target hierarchy:

`User -> Organization -> Project -> Environment -> Assessment -> Run -> Evidence Snapshot -> Result -> Review/Audit`

The deterministic CVSS engine remains unchanged. This phase adds identity,
tenant isolation, persistence, workflow, auditability, and administration
around the engine.

## 2. Authentication

Production sign-in is Google OAuth through Better Auth.

The canonical platform super-administrator account is configured by
`PLATFORM_SUPERADMIN_EMAIL`. Production must set it to the approved HelpUS
Google account. The application must not depend on password bootstrap for
normal operation.

Rules:

- Google identity is the authentication source.
- New users default to platform role `USER`.
- Only the canonical configured account may be automatically reconciled to
  `PLATFORM_ADMIN`.
- Platform role never grants implicit access to an existing tenant.
- Tenant access still requires an ACTIVE Membership.
- Disabled/suspended users lose active sessions.
- Every global administrative mutation is audited.

## 3. Platform SuperAdmin responsibilities

The global SuperAdmin console should manage:

### Users
- list/search users;
- inspect Google-linked identity/provider;
- ACTIVE / SUSPENDED / DISABLED lifecycle;
- revoke all sessions;
- inspect tenant memberships;
- promote/demote platform administrators only under explicit invariant rules;
- prevent disabling or demoting the canonical SuperAdmin account;
- audit every change.

### Organizations
- create organization;
- suspend/reactivate/archive organization;
- inspect tenant administrators and member counts;
- transfer/add tenant ADMIN membership;
- review usage and activity.

### Platform controls
- feature flags;
- plan / quota policy;
- retention policy;
- allowed authentication providers/domains if later enabled;
- rate limits;
- report/export policy;
- integration/service-account policy;
- system maintenance mode;
- audit/event retention settings.

These controls should be stored as versioned platform configuration, never as
untracked UI-only state.

## 4. Tenant roles

Recommended operational roles:

- `ADMIN`: members, projects, environments, policies, evidence, analyses and
  review configuration.
- `OPERATOR`: projects/environments/evidence and analysis execution.
- `REVIEWER`: review/approve governed decisions but cannot administer tenant.
- `VIEWER`: read-only.

The existing reserved REVIEWER role should be activated only when its
permissions and review workflow are implemented server-side.

## 5. Assessment lifecycle

Introduce a persistent logical `Assessment` representing an analytical
procedure, and immutable-ish `AssessmentRun` records for repeated executions.

Example:

- Assessment: “CVE-2026-1234 / ERP Production”.
- Run 1: initial evidence.
- Run 2: after network segmentation.
- Run 3: abstained because telemetry expired.

Recommended workflow:

`DRAFT -> READY -> RUNNING -> COMPLETED | ABSTAINED | FAILED -> REVIEW_REQUIRED -> APPROVED -> ARCHIVED`

A run should never overwrite a prior run.

## 6. Required run provenance

Persist at minimum:

- organization/project/environment IDs;
- assessment and run IDs;
- actor user ID;
- CVE / vulnerability identifier;
- source vector and source metadata;
- evidence snapshot hash;
- deterministic engine build/commit;
- rule catalog version/hash;
- organizational policy ID/version;
- candidate metrics;
- final vector/score when available;
- abstention reasons;
- operational disposition;
- canonical audit receipt hash;
- timestamps;
- optional reviewer/approval record.

## 7. Evidence snapshots

Analyses should reference versioned evidence snapshots rather than receiving
only ephemeral browser payloads.

Evidence classes may include:

- CMDB / asset inventory;
- topology/routing;
- firewall/segmentation;
- IAM/MFA;
- WAF/EDR;
- data classification;
- business criticality;
- HA/RTO/RPO;
- dependency graph;
- vulnerability metadata.

Every snapshot needs source, captured-at time, freshness policy, digest and
tenant/environment ownership.

## 8. API boundary

The current public `POST /api/analyze-environment` is suitable only as a
demonstration compatibility endpoint. It does not resolve a tenant/session and
must not be the production operational path.

Target operational API:

`POST /api/organizations/{org}/projects/{project}/environments/{env}/assessments`

and:

`POST /api/organizations/{org}/projects/{project}/environments/{env}/assessments/{assessmentId}/runs`

The server must resolve the session and authoritative tenant context and verify
`analysis:execute`. Client-supplied organization IDs/roles are never trusted.

The production run endpoint should call a shared deterministic analysis service
used by both the compatibility/demo route and authenticated route so scoring
logic is not duplicated.

## 9. Separation from scientific confirmatory execution

The operational SaaS workspace must not expose or route C1/C2.

G10B scientific execution is a separate governed clean-room workflow.
Production tenant users cannot access confirmatory datasets or controls.

## 10. Delivery phases

### SaaS-1 — Global identity and SuperAdmin
Google-only login, canonical SuperAdmin reconciliation, global user management,
session revocation, organization lifecycle and audit.

### SaaS-2 — Persistent assessments
Add Assessment / AssessmentRun / EvidenceSnapshot schema and tenant-scoped CRUD.

### SaaS-3 — Authenticated analysis
Extract deterministic analysis service and add tenant-scoped execution route.
Persist every run.

### SaaS-4 — Review workflow
Activate REVIEWER permissions, review queue, approval records and policy-based
review requirements.

### SaaS-5 — Operations
Quotas, rate limiting, retention, exports, integrations/service accounts,
observability and billing hooks.

## 11. Non-negotiable security invariants

- deny by default;
- tenant ID is resolved server-side;
- no implicit PLATFORM_ADMIN tenant bypass;
- canonical SuperAdmin account cannot be accidentally disabled/demoted;
- Google OAuth secrets only in environment/secret manager;
- no credentials/tokens in Git;
- all mutations audited;
- session revocation on global user suspension/disable;
- tenant-scoped DB filters on all operational data;
- production analysis data never shares namespace with C1/C2.
