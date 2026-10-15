# Deterministic Synthetic Authentication for E2E

Date: 2026-10-15

## Objective

Promote the synthetic user journeys from manually authenticated Playwright tests toward deterministic CI execution without weakening production authentication.

## Design choice

Use Better Auth's official `testUtils()` plugin in a separate E2E-only auth instance.

The production auth instance remains unchanged:
- Google OAuth remains the interactive production provider.
- email/password remains disabled.
- the public `/api/auth/[...all]` route imports only `@/lib/auth`.
- no synthetic login HTTP endpoint is added.

Better Auth documents `testUtils()` specifically for integration/E2E testing and recommends a separate test-only auth instance rather than adding privileged test helpers to production auth configuration.

## Files

- `e2e/user-journey/synthetic-auth.ts`
  - separate Better Auth instance;
  - same database/secret contract;
  - `testUtils()` only;
  - local HTTP host restriction.

- `e2e/user-journey/global-setup.ts`
  - opt-in with `E2E_SYNTHETIC_AUTH=1`;
  - requires local PostgreSQL;
  - provisions deterministic E2E user;
  - provisions E2E organization + ADMIN membership;
  - provisions ACTIVE test policy;
  - generates Playwright cookies and storageState.

- `playwright.user-journey.config.ts`
  - invokes global setup;
  - consumes generated storageState;
  - starts a local app server in synthetic mode.

## Fail-closed controls

Synthetic mode fails unless:
1. `E2E_SYNTHETIC_AUTH=1`;
2. `E2E_BASE_URL` is HTTP on localhost/127.0.0.1;
3. `DATABASE_URL` points to localhost/127.0.0.1;
4. organization slug starts with `e2e`.

This deliberately prevents use against staging or production.

## Deterministic fixtures

User:
- synthetic-e2e@helpus.invalid
- ACTIVE
- platform role USER

Organization:
- e2e-org by default
- ACTIVE

Membership:
- ADMIN
- ACTIVE

Policy:
- E2E-CVSS-ENV
- version 1
- ACTIVE

This makes the advanced CR/IR/AR journey deterministic.

## CI proving period

The real pipeline gains a separate job:

Synthetic User Journey E2E

It uses:
- disposable PostgreSQL 16 service;
- fixed E2E-only Better Auth secret;
- local Next.js server;
- Playwright Chromium;
- three consecutive complete suite executions.

For the proving period the job uses:

continue-on-error: true

Promotion to blocking requires:
- compatible Better Auth testUtils on the pinned version;
- 3 consecutive full runs green;
- no flakiness;
- acceptable execution time;
- artifact review;
- no production-auth regression.

## Production boundary

No testUtils import exists in production auth.
No test route exists.
No remote synthetic auth is permitted.
No production secret is used in CI.
