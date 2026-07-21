# Auth-1F Online PostgreSQL Integration

- Execution environment: GitHub Actions
- Database environment: temporary Railway environment
- Application preview: Vercel Preview Deployment
- Local Docker: not used
- Local PostgreSQL: not used
- Persistent database mutation: none
- Production deployment: none

## Flow

For every Pull Request targeting `real-world-cvss`:

1. GitHub Actions creates an isolated Railway environment.
2. A new Railway PostgreSQL service is added to that environment.
3. The public disposable database URL is masked in the runner logs.
4. The current Prisma schema is applied only to that temporary database.
5. Auth-1F integration tests execute against PostgreSQL.
6. Auth-1B through Auth-1E regressions execute.
7. TypeScript, Next.js build and Python validation execute.
8. The workflow waits for the Vercel Preview check.
9. The Railway environment is deleted in an unconditional cleanup step.

A fallback cleanup job removes orphan environments when the Pull Request is
closed or merged.

## Integration coverage

The suite validates:

- password reset against real PostgreSQL;
- Argon2id credential persistence;
- reset token single use;
- concurrent reset-token consumption;
- revocation of all sessions after reset;
- invitation acceptance;
- invitation email binding;
- invitation single use;
- concurrent invitation consumption;
- duplicate membership prevention;
- individual session revocation;
- other-session revocation;
- all-session revocation;
- session token non-exposure;
- cross-tenant authorization denial.

## Required GitHub configuration

Secret:

- `RAILWAY_API_TOKEN`

Variables:

- `RAILWAY_PROJECT_ID`
- `RAILWAY_BASE_ENVIRONMENT`

The preparation script configures these items before writing the Auth-1F
branch.

## Safety boundaries

The workflow does not:

- use a local Docker engine;
- connect to a local PostgreSQL server;
- use production DATABASE_URL;
- use staging DATABASE_URL;
- create migration files;
- merge the Pull Request;
- deploy production;
- send transactional email.
