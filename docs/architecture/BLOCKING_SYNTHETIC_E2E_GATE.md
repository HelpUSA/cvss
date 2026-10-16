# Promote Synthetic User Journey E2E to Blocking CI

Date: 2026-10-15

## Background

PR #42 proved the synthetic browser suite stable with:
- 3 stability rounds;
- desktop, tablet, mobile;
- isolated E2E organization per viewport and round;
- 9/9 isolated invocations passing;
- zero retry-dependent passes;
- zero remaining flakiness;
- successful Synthetic User Journey E2E job.

## Promotion

The only CI semantic change in this PR is removal of:

continue-on-error: true

from the:

Synthetic User Journey E2E

job.

This means failures in the synthetic browser journey now fail the overall real-pipeline.

## Guard

web/tests/synthetic-e2e-isolation.test.ts now asserts:
- per-round/per-viewport isolation remains present;
- the synthetic E2E job exists;
- no continue-on-error directive exists for this workflow.

## Rollback criterion

Do not weaken product/auth/scoring behavior to make this gate pass.

If a future failure is proven to be infrastructure-only and recurrent:
1. classify and document it;
2. fix the fixture or CI environment;
3. temporarily restore non-blocking only through an explicit PR with evidence.

Do not silently reintroduce continue-on-error.
