# Antigravity handoff — Synthetic User Journey / Playwright E2E

Repository: HelpUSA/cvss
Branch: chatgpt/synthetic-user-journey-e2e
Base: scientific-validation

## Mission

Act as a real first-time operator before we expose the product to human testers.

This is NOT a feature-development round.

Find:
- broken paths;
- confusing paths;
- hidden prerequisites;
- dead ends;
- misleading messages;
- mobile problems;
- permission problems;
- inconsistencies between what the UI says and what actually happens.

Then make only the minimum fixes required to make the journeys reliable and understandable.

## What ChatGPT already added

1. Playwright scripts:
- test:user-journey:e2e
- test:user-journey:e2e:headed

2. Config:
- web/playwright.user-journey.config.ts

Projects:
- desktop 1440x900
- tablet
- mobile

3. Automated journeys:
- web/e2e/user-journey/guided-basic.spec.ts
- web/e2e/user-journey/advanced-bte.spec.ts
- web/e2e/user-journey/helpers.ts

4. Security:
- playwright/.auth/
- playwright-report/
- test-results/
are gitignored.

5. Architecture:
- docs/architecture/SYNTHETIC_USER_JOURNEY_E2E.md

## Important authentication rule

DO NOT commit:
- Google credentials;
- cookies;
- Better Auth session tokens;
- storageState.

Use an E2E-only account and E2E-only organization.

Generate local storage state interactively or via the existing authorized test environment.

Suggested flow:

mkdir -p playwright/.auth

Set:
E2E_BASE_URL=<test/staging URL>

Then:

npx playwright codegen --save-storage=playwright/.auth/user.json "$E2E_BASE_URL/login"

Complete Google authentication manually in the browser.

Close codegen.

Then export:
E2E_ORGANIZATION_SLUG=<disposable test tenant slug>

If testing governed CR/IR/AR:
E2E_ACTIVE_POLICY_LABEL="<exact visible ACTIVE policy option>"

## PHASE 1 — Manual synthetic-human browser audit

Do this BEFORE Playwright.

Act as though you have never seen HELPUS.

Do not inspect database/code while navigating.

Do not call APIs directly.

Use only visible browser controls.

### Persona A — Basic new operator

Goal:
complete first valid run without opening any advanced CVSS panel.

Path:

Login
→ choose organization
→ Comece aqui
→ Project
→ Environment
→ Assessment
→ Step 4 essential evidence
→ Execute
→ Result
→ Evidence Library

At every page record:

1. Where am I?
2. What do I think the next action is?
3. What can I safely ignore?
4. Is any word unclear?
5. Did I need implementation knowledge to continue?

PASS only if the basic operator can finish without opening:
- Threat E;
- CR/IR/AR;
- Supplemental Metrics.

### Persona B — Operator who makes mistakes

Intentionally test:
- malformed project slug;
- invalid CVE;
- invalid CVSS vector;
- UNKNOWN reachability;
- UNKNOWN evidence quality;
- blank telemetry age;
- missing threat provenance after choosing E;
- CR/IR/AR without policy if UI permits reaching it.

Evaluate:
- message clarity;
- error placement;
- recovery without reload when appropriate;
- no technical stack trace.

### Persona C — ABSTAIN recovery

Create an execution that legitimately ABSTAINS.

Then, without reading source code:
- explain why it abstained;
- identify what must be corrected;
- return to Step 4;
- correct evidence;
- produce a valid new result.

If the UI does not make that path clear:
NEEDS_CHANGE.

### Persona D — Returning operator / reuse

After a successful run:

Evidence Library
→ inspect preserved snapshot
→ return to assessment
→ reuse evidence
→ execute again
→ confirm a new run is created
→ confirm original evidence remains historical.

Check whether the operator understands that reuse is a starting point/new run, not mutation of history.

### Persona E — Advanced operator

Use:
- E=P with fresh explicit threat-intelligence provenance;
- governed CR=H, IR=M, AR=L using an ACTIVE test policy;
- selected Supplemental Metrics.

Expected:
CVSS-BTE where appropriate.

Verify Supplemental values remain visibly non-scoring.

### Persona F — Viewer/read-only

If a VIEWER test account is available:
- inspect existing assessment/result;
- attempt to locate creation/execution actions.

Expected:
read-only user should not be invited to perform forbidden actions.

If no VIEWER fixture exists, mark NOT_EXECUTED and recommend a future dedicated permission fixture rather than weakening auth.

## PHASE 2 — Run automated Playwright journeys

Before running, inspect/fix the new test code itself.

ChatGPT created the initial implementation from current UI contracts; treat compilation/runtime selector failures as test defects unless the product behavior is truly broken.

Run:

cd web
npm ci
npx playwright install --with-deps chromium
npx prisma validate
npx prisma generate
npm run typecheck
npm run test:saas:unit
npm run build

Then:

npm run test:user-journey:e2e

For interactive debugging:

npm run test:user-journey:e2e:headed

## Basic automated journey acceptance

For desktop/tablet/mobile:

- Project created through UI;
- Environment created through UI;
- Assessment created through UI;
- advanced E/CR-IR-AR/Supplemental disclosures closed;
- Base vector accepted;
- reachability/evidence quality/freshness entered;
- run created;
- result page reached;
- source/contextual result visible;
- technical details collapsed by default;
- Evidence Library reachable;
- no horizontal overflow.

## Reuse automated acceptance

- prior snapshot appears;
- select preserved evidence;
- execute new run;
- result indicates GUIDED_REUSE provenance/traceability as available;
- no mutation of historical snapshot.

If the visible result no longer exposes GUIDED_REUSE directly after UX consolidation, do not add technical noise merely to satisfy the selector.
Instead change the test to assert the user-visible reuse lineage through the appropriate audit disclosure.

## ABSTAIN automated acceptance

- UNKNOWN/insufficient environment produces ABSTAIN;
- result explains abstention in plain language;
- user can return;
- corrected evidence produces a valid result.

## Advanced automated journey acceptance

Only execute when E2E_ACTIVE_POLICY_LABEL is configured.

Test:
- E=P with source + observedAt;
- CR=H;
- IR=M;
- AR=L;
- Supplemental Safety/Automatable/Provider Urgency;
- final nomenclature includes CVSS-BTE;
- Supplemental summary states it does not alter numerical score.

## Playwright test-quality requirements

Prefer:
- getByRole
- getByLabel
- visible text contracts

Avoid:
- brittle CSS chains;
- database IDs;
- arbitrary sleep/timeouts;
- direct API setup for user actions being tested.

API/DB setup is acceptable only for fixtures that a normal operator cannot reasonably create, such as a pre-existing ACTIVE policy or role fixture.

## Production safety

DO NOT initially run destructive/write journeys against customer production data.

Preferred order:

1. local/staging disposable DB;
2. dedicated E2E tenant on deployed preview/staging;
3. only then a dedicated production E2E tenant if explicitly safe.

Never use customer organization data.

## Cleanup

E2E-created data must be identifiable with prefix:
E2E

Do not invent destructive cleanup scripts against production.

If safe archive/delete endpoints already exist, evaluate them separately.

Otherwise document test-data retention and use disposable DB/tenant.

## Screenshots / evidence

For the manual audit, preserve screenshots at:
- organization selection;
- Comece aqui;
- Step 1;
- Step 2;
- Step 3;
- Step 4 before advanced;
- Step 4 advanced;
- valid result;
- ABSTAIN result;
- Evidence Library;
- reuse;
- mobile Step 4;
- mobile result.

Do not commit secrets in screenshots.

## Allowed fixes

Only fixes revealed by real journey execution, such as:
- selector/accessibility label defects;
- broken CTA/link;
- confusing error copy;
- mobile overflow;
- incorrect collapsed/open default;
- broken reuse path;
- result content ordering;
- missing user-visible recovery guidance;
- test fixture/setup defects.

## Forbidden scope expansion

Do not add:
- new scoring metrics;
- new algorithms;
- new risk score;
- new AI feature;
- new threat feed;
- expert/HITL requirement;
- schema migration unless an actual blocking bug proves unavoidable and is reported first.

Do not modify:
- canonical scorer;
- FIRST arithmetic;
- ABSTAIN semantics;
- CR/IR/AR semantics;
- Threat E semantics;
- Supplemental scoring invariance;
- C1/C2.

## Required permanent-CI assessment

At the end, decide whether this suite is stable enough to become a blocking GitHub CI gate.

Do NOT make it blocking merely because it passes once.

Evaluate:
- execution time;
- deterministic auth fixture;
- deterministic policy fixture;
- test-data lifecycle;
- flakiness over at least 3 consecutive runs.

If those are not solved, recommend:
NON_BLOCKING_E2E
with the exact prerequisites to promote it later.

## Required final report

Create:

docs/reviews/ANTIGRAVITY_SYNTHETIC_USER_JOURNEY_REPORT.md

Return:

==================================================
ANTIGRAVITY SYNTHETIC USER JOURNEY REPORT
==================================================

Repository:
HelpUSA/cvss

PR:
#40

Tested HEAD:

Target environment:
LOCAL / PREVIEW / STAGING / PRODUCTION-E2E

Browser auth fixture:
PASS / FAIL

Secrets excluded from Git:
PASS / FAIL

Manual Persona A basic:
PASS / NEEDS_CHANGE

Manual Persona B errors:
PASS / NEEDS_CHANGE

Manual Persona C ABSTAIN recovery:
PASS / NEEDS_CHANGE

Manual Persona D evidence reuse:
PASS / NEEDS_CHANGE

Manual Persona E advanced BTE:
PASS / NEEDS_CHANGE / NOT_EXECUTED

Manual Persona F viewer:
PASS / NEEDS_CHANGE / NOT_EXECUTED

Desktop E2E:
PASS / FAIL

Tablet E2E:
PASS / FAIL

Mobile E2E:
PASS / FAIL

Basic 1→5:
PASS / FAIL

Advanced controls untouched on basic run:
PASS / FAIL

Evidence Library:
PASS / FAIL

Evidence reuse:
PASS / FAIL

ABSTAIN:
PASS / FAIL

ABSTAIN correction:
PASS / FAIL

Advanced BTE:
PASS / FAIL / SKIPPED

No horizontal overflow:
PASS / FAIL

Accessibility selectors:
PASS / FAIL

Typecheck:
PASS / FAIL

SaaS tests:
x/x

Python:
x/x

Build:
PASS / FAIL

Playwright runs:
Run 1: PASS / FAIL
Run 2: PASS / FAIL
Run 3: PASS / FAIL

Flakiness observed:
YES / NO

Test data cleanup/lifecycle:
SAFE / NEEDS_WORK

CI recommendation:
BLOCKING_E2E / NON_BLOCKING_E2E

Changes made:

Files changed:

Residual issues:

Recommendation:
MERGE / FIX_REQUIRED

==================================================

The final report must distinguish:
- product defects;
- test defects;
- fixture/environment limitations.

FIM.
