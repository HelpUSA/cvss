# Antigravity handoff — deterministic synthetic E2E authentication

Repository: HelpUSA/cvss
Branch: chatgpt/deterministic-synthetic-auth
Base: scientific-validation

## Mission

Validate and, if necessary, minimally repair the deterministic test-only authentication path for Playwright.

This round exists to remove Google OAuth as an E2E CI dependency WITHOUT creating a production auth bypass.

## Normative Better Auth design

Better Auth documents the testUtils plugin for integration/E2E and recommends using it in a separate test-only auth instance.

ChatGPT implemented that pattern.

Do NOT move testUtils into web/src/lib/auth.ts.

Do NOT expose a synthetic login endpoint.

## Implemented by ChatGPT

1. web/e2e/user-journey/synthetic-auth.ts
- separate betterAuth instance;
- prisma adapter;
- testUtils();
- same secret/base path contract;
- localhost-only base URL.

2. web/e2e/user-journey/global-setup.ts
- requires E2E_SYNTHETIC_AUTH=1;
- requires local DB host;
- requires localhost app;
- provisions deterministic user;
- provisions e2e organization;
- ADMIN membership;
- ACTIVE E2E-CVSS-ENV v1 policy;
- generates Playwright storageState.

3. Playwright config
- globalSetup wired;
- generated storageState consumed;
- local web server support.

4. real-pipeline.yml
- new Synthetic User Journey E2E job;
- postgres:16 disposable service;
- db push;
- build;
- Chromium install;
- three consecutive E2E executions;
- report artifacts;
- continue-on-error:true during proving period.

5. Guard tests
- production auth has no testUtils;
- public auth route still imports only production auth;
- local-only restrictions;
- deterministic fixtures;
- non-blocking CI classification.

## FIRST task: dependency compatibility

Pinned Better Auth version:
1.6.23

Verify that this exact installed version exports:
testUtils from better-auth/plugins

If yes:
continue.

If not:
DO NOT casually upgrade Better Auth.

Investigate the smallest safe compatible option:
- exact compatible test utility export/subpath already present in 1.6.23;
- only if absolutely necessary, propose a narrowly scoped dependency change and document security/regression impact.

Any dependency upgrade is FIX_REQUIRED and must be called out explicitly before merge recommendation.

## Security invariants

Must prove:

A. web/src/lib/auth.ts contains no testUtils.

B. web/src/app/api/auth/[...all]/route.ts contains no synthetic/test route behavior.

C. Synthetic fixture refuses:
- https remote app URL;
- non-local app hostname;
- remote DATABASE_URL;
- organization slug not starting e2e;
- mode without E2E_SYNTHETIC_AUTH=1.

D. CI uses only disposable Postgres.

E. CI Better Auth secret is E2E-only and not a production secret.

F. generated storageState remains gitignored.

## Functional validation

Run locally with disposable Postgres.

Required env example:

DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/cvss_e2e
BETTER_AUTH_SECRET=synthetic-e2e-only-secret-0123456789abcdef
BETTER_AUTH_URL=http://127.0.0.1:3000
E2E_BASE_URL=http://127.0.0.1:3000
E2E_SYNTHETIC_AUTH=1
E2E_ORGANIZATION_SLUG=e2e-org

Then:

cd web
npm ci
npx prisma validate
npx prisma generate
npx prisma db push
npm run typecheck
npm run test:saas:unit
npm run build
npx playwright install --with-deps chromium
npm run test:user-journey:e2e

## Required E2E behavior

The suite must NOT skip for missing manual storage state in synthetic mode.

It must automatically:
- create/upsert synthetic user;
- create/upsert E2E org;
- create ADMIN membership;
- create ACTIVE E2E policy;
- create session;
- create cookies;
- authenticate browser.

Then execute:
- desktop basic;
- tablet basic;
- mobile basic;
- reuse;
- ABSTAIN/recovery;
- advanced BTE.

## Advanced BTE

Synthetic mode should make this deterministic through:

E2E-CVSS-ENV · v1

Expected:
advanced test RUNS, not SKIPS.

## Three-run stability proof

Execute the full suite 3 times against the same disposable DB.

Use unique E2E_RUN_ID values.

Report:
Run 1
Run 2
Run 3

Any intermittent failure => FLAKY.

Do not promote to blocking if flaky.

## CI validation

Push fixes if required.

Inspect GitHub Actions job:

Synthetic User Journey E2E

Because continue-on-error=true, the main workflow may remain green even if this job fails.

You MUST report the actual synthetic job conclusion separately.

Do not call the E2E proven merely because real-pipeline overall is green.

## Promotion decision

Recommend BLOCKING_E2E only if:
- synthetic job succeeds;
- all 3 runs succeed;
- no manual storage state needed;
- advanced BTE runs;
- no flakiness;
- production auth untouched;
- runtime acceptable.

Otherwise:
NON_BLOCKING_E2E
with exact remaining blockers.

Do NOT change continue-on-error to false in this PR unless all criteria above are proven and the report explicitly justifies promotion.

## Quality gates

- Prisma validate
- Prisma generate
- TypeScript
- SaaS unit
- Python 166/166 expected
- Next build
- synthetic Playwright x3
- real-pipeline

## Report

Create:
docs/reviews/ANTIGRAVITY_DETERMINISTIC_SYNTHETIC_AUTH_REPORT.md

Return:

==================================================
ANTIGRAVITY DETERMINISTIC SYNTHETIC AUTH REPORT
==================================================

Repository:
HelpUSA/cvss

PR:
#41

Tested HEAD:

Better Auth pinned version:
1.6.23

testUtils compatibility:
PASS / FAIL

Dependency upgrade:
NO / YES
If YES:
details:

Production auth unchanged:
PASS / FAIL

No public synthetic route:
PASS / FAIL

Local app guard:
PASS / FAIL

Local DB guard:
PASS / FAIL

E2E slug guard:
PASS / FAIL

StorageState gitignored:
PASS / FAIL

Synthetic user:
PASS / FAIL

Synthetic organization:
PASS / FAIL

ADMIN membership:
PASS / FAIL

ACTIVE policy:
PASS / FAIL

Session/cookies generated:
PASS / FAIL

Manual Google login required:
NO / YES

Desktop E2E:
PASS / FAIL

Tablet E2E:
PASS / FAIL

Mobile E2E:
PASS / FAIL

Evidence reuse:
PASS / FAIL

ABSTAIN recovery:
PASS / FAIL

Advanced BTE:
PASS / FAIL / SKIPPED

Run 1:
PASS / FAIL

Run 2:
PASS / FAIL

Run 3:
PASS / FAIL

Flakiness:
YES / NO

Synthetic CI job:
PASS / FAIL / RUNNING

Overall real-pipeline:
PASS / FAIL / RUNNING

Typecheck:
PASS / FAIL

SaaS tests:
x/x

Python:
x/x

Build:
PASS / FAIL

Runtime:

CI classification:
BLOCKING_E2E / NON_BLOCKING_E2E

continue-on-error:
KEEP / REMOVE

Product auth defects:

E2E fixture defects:

Changes made:

Residual issues:

Recommendation:
MERGE / FIX_REQUIRED

==================================================

Critical:
Do not infer PASS from overall workflow success. Inspect the Synthetic User Journey E2E job directly.
