# Auth-1E account lifecycle

- Status: implemented and locally validated
- Date: 2026-07-20
- Schema change: none
- Migration: none
- Email provider: Resend API

## Password reset

The request endpoint always returns a generic accepted response.

Eligible accounts receive a 256-bit opaque token. Only its SHA-256 hash
is stored in PasswordResetToken.

The token:

- expires after 30 minutes;
- can be used only once;
- replaces previous unused reset tokens;
- is revoked when email delivery fails.

A successful reset:

- hashes the new password with Argon2id;
- marks the token as used;
- revokes other reset tokens;
- deletes every active session for the user;
- appends a SecurityAuditEvent.

## Invitations

An ADMIN with membership:manage may create and revoke invitations.

The raw token is delivered by email and is never stored.

Acceptance requires:

- a valid, unused and unrevoked token;
- an ACTIVE organization;
- an ACTIVE authenticated user;
- exact normalized email equality.

Acceptance creates or reactivates the membership and records the actor.

## Session management

Users may:

- revoke one of their own sessions;
- revoke every other session;
- revoke every session, including the current one.

Session listings never expose the session token.

## Email configuration

Production requires:

- RESEND_API_KEY;
- AUTH_EMAIL_FROM;
- AUTH_PUBLIC_BASE_URL or BETTER_AUTH_URL.

The public base URL must use HTTPS in production.

## Deferred

- account provisioning for people without an existing CVSS account;
- real PostgreSQL integration tests;
- real concurrency tests;
- provider delivery tests;
- deployment configuration and secret provisioning.
