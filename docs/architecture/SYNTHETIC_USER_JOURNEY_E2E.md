# Synthetic User Journey E2E

Date: 2026-10-15

## Goal

Validate HELPUS CVSS as a user-operated product, not only as a collection of passing unit/integration tests.

This layer complements, rather than replaces:
- canonical scorer validation;
- FIRST reference corpus gates;
- SaaS unit tests;
- API authorization tests;
- production build checks.

## Test model

Two complementary passes are required.

### Pass 1 — agent as a first-time human

Antigravity navigates the actual browser without developer shortcuts.

It must:
- read the page before acting;
- use visible labels and CTAs;
- note ambiguous wording;
- intentionally make selected mistakes;
- recover through the UI;
- record screenshots/notes.

This pass is qualitative.

### Pass 2 — Playwright regression journey

Playwright repeats stable workflows using visible UI semantics.

Initial automated coverage:
- Project creation;
- Environment creation;
- Assessment creation;
- basic Step 4 run with advanced controls untouched;
- result comprehension;
- Evidence Library access;
- evidence reuse;
- ABSTAIN and recovery;
- optional governed BTE journey when an ACTIVE test policy is supplied;
- desktop/tablet/mobile projects;
- horizontal-overflow checks.

## Authentication boundary

Google credentials, cookies and session tokens MUST NOT be committed.

The suite consumes a Playwright storage state from:

playwright/.auth/user.json

or the path supplied by:

E2E_STORAGE_STATE

That directory is gitignored.

A local authenticated state can be generated interactively, for example:

npx playwright codegen --save-storage=playwright/.auth/user.json "$E2E_BASE_URL/login"

Complete Google login manually in the opened browser, then close it.

## Required environment

- E2E_BASE_URL
- E2E_ORGANIZATION_SLUG
- E2E_STORAGE_STATE (optional when using the default path)
- E2E_RUN_ID (optional deterministic suffix)
- E2E_ACTIVE_POLICY_LABEL (required only for governed BTE test)

Use only a disposable E2E organization.

Do not run write journeys against a customer tenant.

## Commands

npm run test:user-journey:e2e

Headed:

npm run test:user-journey:e2e:headed

Single browser:

npx playwright test --config=playwright.user-journey.config.ts --project=desktop

## Evidence artifacts

On failure Playwright retains:
- trace;
- screenshot;
- video.

The report is written under:
playwright-report/user-journey

These artifacts are local/CI artifacts and are not committed.

## Safety

Tests create identifiable records prefixed with E2E.

Until a safe cleanup/archival mechanism is explicitly validated, the suite should use a disposable tenant/database and must not attempt ad-hoc destructive cleanup.

## Acceptance principle

A successful browser response is not enough.

The basic journey passes only if:
- advanced controls remain closed;
- the operator reaches a valid result using essential fields;
- the result is understandable before opening technical details;
- no horizontal overflow occurs at target viewports;
- ABSTAIN provides an actionable recovery path.
