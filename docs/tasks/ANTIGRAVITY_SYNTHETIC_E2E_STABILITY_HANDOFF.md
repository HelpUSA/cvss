# Antigravity handoff — stabilize synthetic E2E state isolation

Repository: HelpUSA/cvss
Branch: chatgpt/stabilize-synthetic-e2e
Base: scientific-validation

## Objective

Eliminate the known synthetic E2E flakiness caused by shared logical state between desktop/tablet/mobile.

Do not change product behavior.

## Implemented change

The CI loop no longer runs all Playwright projects together against one E2E organization.

For each stability round and viewport it now runs a separate Playwright invocation with:

E2E_ORGANIZATION_SLUG=e2e-<github_run_id>-<round>-<project>

and:

--project=<desktop|tablet|mobile>

This yields 9 isolated invocations:
3 rounds × 3 viewports.

## Expected effect

Desktop, tablet and mobile no longer share:
- projects;
- environments;
- assessments;
- evidence snapshots;
- run state;

inside the same logical tenant.

They still share the same disposable PostgreSQL service, which is acceptable because tenant-level uniqueness is now deterministic.

## Validate first

Inspect:
.github/workflows/real-pipeline.yml

Confirm:
- nested loop round × project;
- unique E2E_ORGANIZATION_SLUG;
- one Playwright project per invocation;
- continue-on-error remains true.

## Run locally if useful

Use local PostgreSQL plus:

E2E_SYNTHETIC_AUTH=1
E2E_BASE_URL=http://127.0.0.1:3000
BETTER_AUTH_URL=http://127.0.0.1:3000
BETTER_AUTH_SECRET=synthetic-e2e-only-secret-0123456789abcdef

Then run individual project tests with unique org slugs, for example:

E2E_RUN_ID=local-1-desktop \
E2E_ORGANIZATION_SLUG=e2e-local-1-desktop \
npx playwright test --config=playwright.user-journey.config.ts --project=desktop

Repeat tablet/mobile and three rounds.

## Required validation

Quality gates:
- Prisma validate/generate
- TypeScript
- SaaS unit
- Python
- Next build

E2E:
Round 1 desktop PASS
Round 1 tablet PASS
Round 1 mobile PASS

Round 2 desktop PASS
Round 2 tablet PASS
Round 2 mobile PASS

Round 3 desktop PASS
Round 3 tablet PASS
Round 3 mobile PASS

No invocation may depend on a retry to pass.

## If failures remain

Classify each failure:

A. tenant-state collision
B. browser/device-specific selector
C. timing/navigation
D. app defect
E. infrastructure/runtime

Do not hide flakiness by increasing retries/timeouts arbitrarily.

Do not serialize by adding sleeps.

## Blocking gate decision

Even if all 9 pass in one CI run:

do NOT automatically remove continue-on-error in this PR.

Report whether a second dedicated stability round is advisable before promotion.

## Required report

Create:
docs/reviews/ANTIGRAVITY_SYNTHETIC_E2E_STABILITY_REPORT.md

Return:

==================================================
ANTIGRAVITY SYNTHETIC E2E STABILITY REPORT
==================================================

Repository:
HelpUSA/cvss

PR:
#42

Tested HEAD:

Isolation model:
PASS / FAIL

Unique org per viewport:
PASS / FAIL

Unique org per stability round:
PASS / FAIL

Round 1 desktop:
PASS / FAIL

Round 1 tablet:
PASS / FAIL

Round 1 mobile:
PASS / FAIL

Round 2 desktop:
PASS / FAIL

Round 2 tablet:
PASS / FAIL

Round 2 mobile:
PASS / FAIL

Round 3 desktop:
PASS / FAIL

Round 3 tablet:
PASS / FAIL

Round 3 mobile:
PASS / FAIL

Any retry-dependent pass:
YES / NO

Flakiness:
YES / NO

Synthetic CI job:
PASS / FAIL / RUNNING

Overall real-pipeline:
PASS / FAIL / RUNNING

Runtime:

Typecheck:
PASS / FAIL

SaaS:
x/x

Python:
x/x

Build:
PASS / FAIL

Product defects:

Test defects:

Infrastructure defects:

Changes made:

Residual issues:

continue-on-error:
KEEP / REMOVE-LATER

Recommendation:
MERGE / FIX_REQUIRED

==================================================
