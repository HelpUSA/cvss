# ADR 0001: Authentication foundation

- Status: Accepted
- Decision: BETTER_AUTH
- Architecture gate: ADR_READY
- Date: 2026-07-15
- Better Auth: 1.6.23
- Prisma adapter: 1.6.23
- Argon2 implementation: @node-rs/argon2 2.0.2

## Context

The application requires local credentials, PostgreSQL-backed sessions,
explicit session revocation, tenant isolation and a global platform
administrator independent from tenant memberships.

NextAuth v4 was declared but no authentication implementation existed. Its
Credentials Provider does not match the required persistent database-session
architecture.

## Decision

Use Better Auth with the Prisma adapter.

Use custom Argon2id password hashing through `@node-rs/argon2`.

Authentication, Prisma and Argon2id execute only in the Node.js runtime.

Middleware may redirect navigation but is not an authorization boundary.
Protected server pages, routes and actions validate the session, user status,
organization status, membership status and tenant role again on the server.

## Registration

Public registration is disabled.

Users enter through the explicit idempotent PLATFORM_ADMIN bootstrap or a
future valid invitation.

## Authorization

Global capability:

- PLATFORM_ADMIN

Tenant roles:

- ADMIN
- OPERATOR
- REVIEWER
- VIEWER

PLATFORM_ADMIN receives no implicit tenant-content access.

REVIEWER remains reserved without operational access during Auth-1.

## Password policy

- Argon2id
- algorithm value 2
- 64 MiB memory
- 3 iterations
- parallelism 4
- 32-byte output
- length from 12 to 128 characters

Passwords, hashes, session tokens and token hashes are never logged.

## Legacy isolation

The first authentication migration is exclusively additive.

These models remain byte-for-byte unchanged:

- Run
- Assessment
- Comparison
- AuditEvent

Auth-1A adds no column, relation, index, backfill, rename or constraint to
those models.

## Deferred

- production migration application
- login UI
- authenticated routes
- invitation delivery
- password reset delivery
- reviewer workflow
- MFA
- OAuth
- magic links
- RLS
