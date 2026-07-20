# Auth-1D tenant administration

- Status: implemented and locally validated
- Date: 2026-07-20
- Schema change: none
- Migration: none
- Bootstrap: not executed

## Scope

Auth-1D adds the first controlled tenant mutations to the authenticated
application.

## Organization creation

Only an ACTIVE PLATFORM_ADMIN can create an organization.

The organization and the creator's first ACTIVE ADMIN membership are
created in one Serializable transaction.

This does not grant the platform administrator access to pre-existing
organizations.

## Membership administration

An ACTIVE ADMIN membership is required.

The API accepts the email of an existing ACTIVE user and resolves the
authoritative user ID on the server.

Roles and organization identifiers supplied by the browser are never
accepted as authorization evidence.

## Last active administrator

Demotion, suspension and revocation compare the current and resulting
membership states.

When the operation removes an ACTIVE ADMIN, the transaction counts
ACTIVE ADMIN memberships in the same organization.

The operation is rejected when the count is one.

The transaction uses Serializable isolation and retries a bounded number
of P2034 conflicts.

## Projects and environments

ADMIN and OPERATOR may create projects and environments.

Projects are created with the organization ID returned by the
authoritative tenant context.

An environment's projectId is accepted only after the server confirms
that the project is ACTIVE and belongs to the same organization.

## Mutation security

Every mutation requires:

- a valid server-side session;
- an active user;
- the required tenant permission;
- same-origin browser context;
- JSON content type;
- bounded request size;
- validated names, slugs, IDs, roles and statuses.

## Audit

Every successful mutation appends SecurityAuditEvent.

Audit metadata never stores passwords, password hashes, session tokens,
token hashes, cookies, authorization headers or secrets.

## Deferred

- invitation delivery and acceptance;
- password reset delivery;
- disposable PostgreSQL integration tests;
- real concurrency tests;
- cross-tenant E2E tests;
- lifecycle archival mutations.
