# Auth-1H — Operational gates

Auth-1H groups the remaining Phase 1 operational controls into one milestone.

## Automatic pull-request gates

The Auth-1H workflow validates:

- the Resend adapter with mocked `fetch`, so no external message is sent;
- missing configuration rejection and HTTPS public URL enforcement;
- authorization and idempotency headers;
- explicit Node.js Runtime on authentication routes;
- `node:crypto` and native Argon2 dependencies;
- `prisma migrate deploy` on PostgreSQL 16 created for the workflow;
- exactly two completed migrations and zero incomplete migrations;
- a second deploy to prove idempotency;
- Prisma status, schema validation and Auth-1F integration.

## Controlled email sandbox

The TypeScript entrypoint includes a sandbox mode that sends one message only
when all protected values are supplied:

- `RESEND_API_KEY`;
- `AUTH_EMAIL_FROM`;
- `AUTH1H_EMAIL_TEST_TO`;
- `AUTH_PUBLIC_BASE_URL` using HTTPS;
- `AUTH1H_SANDBOX_IDEMPOTENCY_KEY`.

The repository default branch is `main`. GitHub manual dispatch requires the
workflow file to exist on the default branch. Auth-1H therefore does not add a
misleading `workflow_dispatch` file only to `real-world-cvss`.

A trusted default-branch runner, or an explicitly authorized controlled
operator run, remains a separate checkpoint. The recipient is never accepted
as a public workflow input.

## Boundaries

The PR gate does not read secret values, send real email, access a persistent
database, deploy the application or authorize production. Merge, trusted
sandbox automation, the real sandbox send and production remain separate
explicit checkpoints.