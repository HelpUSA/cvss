# Auth-1F Online PostgreSQL Integration

Auth-1F validates the account lifecycle against a real PostgreSQL instance
created exclusively for the GitHub Actions job.

## Execution architecture

- Source and Pull Request: GitHub
- Integration runner: GitHub-hosted Ubuntu
- Database: PostgreSQL 16 Alpine service container
- Application preview: Vercel Preview Deployment
- Production hosting: Railway remains unchanged
- Local Docker: not used
- Local PostgreSQL: not used
- Railway PostgreSQL: not accessed

## Disposable database lifecycle

The `PostgreSQL integration` job declares a PostgreSQL service container.

GitHub Actions:

1. creates the PostgreSQL service;
2. waits for its health check;
3. exposes it only to the hosted runner;
4. applies the current Prisma schema;
5. executes integration and concurrency tests;
6. destroys the service with the hosted runner.

The CI credentials exist only inside the workflow definition and provide no
access to Railway or another persistent database.

## Integration coverage

The Auth-1F suite validates:

- password reset against PostgreSQL;
- Argon2id credential persistence;
- reset-token single use;
- concurrent reset-token consumption;
- revocation of sessions after password reset;
- invitation acceptance;
- invitation email binding;
- invitation single use;
- concurrent invitation consumption;
- duplicate membership prevention;
- individual session revocation;
- other-session revocation;
- all-session revocation;
- session-token non-exposure;
- cross-tenant authorization denial.

## Regression coverage

The workflow also executes:

- Auth-1B contract;
- Auth-1C contract;
- Auth-1D contract;
- Auth-1E contract;
- TypeScript validation;
- Next.js production build;
- real Python pipeline and tests.

## Vercel

Vercel remains responsible for the Pull Request Preview Deployment.

All checks returned for the current Pull Request head are monitored before
Auth-1F is considered complete.

## Railway safety boundary

Auth-1F does not:

- read Railway database credentials;
- use `RAILWAY_API_TOKEN`;
- link to a Railway project;
- create Railway environments;
- create Railway services;
- connect to Railway production;
- copy the Railway production environment;
- deploy to Railway.
