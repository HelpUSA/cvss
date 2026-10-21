# Synthetic E2E Stability Isolation

Date: 2026-10-15

## Problem

PR #41 proved deterministic authentication but the non-blocking E2E job remained flaky because desktop/tablet/mobile rounds wrote into the same logical E2E organization and therefore shared project/environment/assessment state in one disposable database.

## Fix

The CI proving loop now isolates state by BOTH:

- stability round;
- Playwright project/viewport.

Each invocation receives a unique organization slug:

e2e-<github_run_id>-<round>-<project>

Examples:

- e2e-123456-1-desktop
- e2e-123456-1-tablet
- e2e-123456-1-mobile
- e2e-123456-2-desktop

The deterministic global setup already upserts the E2E organization, membership, ACTIVE policy and session for whichever E2E slug is supplied, so no product code or auth semantics need to change.

## Execution model

For each of 3 stability rounds:

1. desktop runs alone in its own E2E org;
2. tablet runs alone in its own E2E org;
3. mobile runs alone in its own E2E org.

The underlying PostgreSQL service is still disposable and local to the GitHub Actions job.

## Why this is preferable

- no cross-viewport data collisions;
- no cleanup race;
- no destructive teardown;
- no extra database instances;
- same user journey semantics;
- deterministic artifacts per viewport;
- easier failure attribution.

## Blocking promotion

The job remains:

continue-on-error: true

Promotion is NOT part of this change.

A later decision may remove continue-on-error only after:
- all 9 isolated invocations pass;
- no retry-dependent success;
- no flakiness in a fresh CI run;
- runtime remains acceptable.
