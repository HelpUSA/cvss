# Auth-1A schema and migration plan

## New enums

- UserStatus: ACTIVE, SUSPENDED, DISABLED
- PlatformRole: USER, PLATFORM_ADMIN
- OrganizationStatus: ACTIVE, SUSPENDED, ARCHIVED
- MembershipRole: ADMIN, OPERATOR, REVIEWER, VIEWER
- MembershipStatus: ACTIVE, SUSPENDED, REVOKED
- ProjectStatus: ACTIVE, ARCHIVED
- EnvironmentStatus: ACTIVE, ARCHIVED

## Better Auth models

- User
- Session
- Account
- Verification

## Application models

- Organization
- Membership
- Project
- Environment
- Invitation
- PasswordResetToken
- SecurityAuditEvent

## Migration boundary

The first migration may create only new enums, tables, indexes and foreign
keys.

It must not alter, rename, reindex, backfill, truncate, update, delete from or
add relations to Run, Assessment, Comparison or AuditEvent.

## Identity rules

Email normalization consists only of trim plus lowercase.

Organization selection uses a server-resolved slug. Client organization IDs
and roles are never trusted.

PLATFORM_ADMIN is global and separate from MembershipRole. It grants no silent
tenant-content access.

## Suspension and sessions

SUSPENDED or DISABLED users cannot authenticate and have global sessions
revoked.

SUSPENDED or REVOKED memberships block only the corresponding organization.

## First platform administrator

The bootstrap requires PLATFORM_ADMIN_EMAIL, PLATFORM_ADMIN_NAME and
PLATFORM_ADMIN_PASSWORD.

It is explicit, idempotent, creates no organization, hashes with Argon2id,
prints no password or hash and appends a SecurityAuditEvent.

## Last active ADMIN

Demotion, suspension or revocation of an ADMIN membership executes in a
serialized database transaction.

The transaction rejects any operation that would leave zero active tenant
ADMIN memberships. PLATFORM_ADMIN cannot silently bypass this invariant.

## SecurityAuditEvent

SecurityAuditEvent is separate from the legacy AuditEvent and append-only by
application contract.

It never stores passwords, password hashes, session tokens, token hashes,
cookies, authorization headers or secrets.

Indexes are required for organizationId, actorUserId, action and createdAt.

## Validation before production

1. Compare legacy model blocks byte-for-byte.
2. Run Prisma format, generate and validate.
3. Generate migration SQL without applying it.
4. Reject destructive or legacy-targeting SQL.
5. Test on disposable PostgreSQL.
6. Test rollback before production authentication data.
7. Test concurrent last-ADMIN mutations.
8. Test cross-tenant IDOR denial.
