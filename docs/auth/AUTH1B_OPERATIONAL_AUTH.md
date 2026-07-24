# Auth-1B operational authentication

- Status: implemented and locally validated
- Date: 2026-07-20
- Better Auth: 1.6.23
- Next.js: 15.5.18
- Prisma: 6.19.0
- Password hashing: Argon2id

## Delivered

- Better Auth server configuration;
- Prisma PostgreSQL adapter;
- custom Argon2id hashing and verification;
- public registration disabled;
- `/api/auth/[...all]`;
- React authentication client;
- `/login`;
- logout;
- database-backed sessions;
- optimistic `/app` middleware redirect;
- authoritative server-side session validation;
- inactive-account denial and session revocation;
- explicit idempotent PLATFORM_ADMIN bootstrap.

## Bootstrap

The bootstrap is never executed during build or validation.

Required environment variables:

- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_URL`
- `PLATFORM_ADMIN_EMAIL`
- `PLATFORM_ADMIN_NAME`
- `PLATFORM_ADMIN_PASSWORD`

Explicit command:

`npm run auth:bootstrap`

The command creates no organization, stores only the Argon2id hash,
does not print the password or hash and appends a security audit event.

## Authorization boundary

Auth-1B proves identity and active account status.

The middleware checks only for the existence of a session cookie and
is not an authorization boundary. Protected server components validate
the session again.

## Deferred to Auth-1C

- organization selection;
- active membership resolution;
- tenant RBAC;
- action-level permissions;
- last-active-ADMIN invariant;
- cross-tenant IDOR tests;
- tenant-scoped domain queries;
- invitation acceptance;
- password-reset delivery.
