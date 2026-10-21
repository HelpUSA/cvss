# Antigravity handoff — promote synthetic E2E to blocking gate

Repository: HelpUSA/cvss
Branch: chatgpt/promote-synthetic-e2e-blocking
Base: scientific-validation

## Objective

Validate the final promotion of Synthetic User Journey E2E from non-blocking to blocking CI.

## Change scope

Only:
- remove continue-on-error:true from Synthetic User Journey E2E;
- update guard test;
- documentation.

No product feature change.

## Required validation

Confirm .github/workflows/real-pipeline.yml:
- Synthetic User Journey E2E exists;
- continue-on-error is absent;
- 3 rounds remain;
- desktop/tablet/mobile remain isolated;
- unique E2E_ORGANIZATION_SLUG remains.

Run:
- prisma validate
- prisma generate
- typecheck
- SaaS unit
- Python
- Next build

Then inspect the new real-pipeline on the actual PR HEAD.

The acceptance condition is stricter now:

1. Synthetic User Journey E2E = SUCCESS.
2. validate = SUCCESS.
3. AI Exchange Contract Validation = SUCCESS.
4. overall real-pipeline = SUCCESS.

If Synthetic User Journey E2E fails, the overall workflow should fail. That is the intended behavior.

## Do not hide failure

Do not:
- re-add continue-on-error;
- add arbitrary sleeps;
- raise retries/timeouts without root cause;
- weaken assertions;
- remove mobile/tablet;
- skip advanced BTE.

If a real flaky/infrastructure failure appears, report FIX_REQUIRED.

## Required report

Create:
docs/reviews/ANTIGRAVITY_BLOCKING_E2E_PROMOTION_REPORT.md

Return:

==================================================
ANTIGRAVITY BLOCKING E2E PROMOTION REPORT
==================================================

Repository:
HelpUSA/cvss

PR:
#43

Tested HEAD:

continue-on-error absent:
PASS / FAIL

Isolation retained:
PASS / FAIL

3 rounds retained:
PASS / FAIL

Desktop:
PASS / FAIL

Tablet:
PASS / FAIL

Mobile:
PASS / FAIL

Advanced BTE:
PASS / FAIL

Evidence reuse:
PASS / FAIL

ABSTAIN recovery:
PASS / FAIL

Any retry-dependent pass:
YES / NO

Flakiness:
YES / NO

Synthetic User Journey E2E job:
PASS / FAIL

validate job:
PASS / FAIL

AI Exchange Contract Validation:
PASS / FAIL

Overall real-pipeline:
PASS / FAIL

Typecheck:
PASS / FAIL

SaaS:
x/x

Python:
x/x

Build:
PASS / FAIL

Runtime:

Blocking behavior proven:
YES / NO

Changes made:

Residual issues:

Recommendation:
MERGE / FIX_REQUIRED

==================================================
