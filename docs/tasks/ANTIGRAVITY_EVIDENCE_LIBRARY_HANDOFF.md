# Antigravity handoff — Evidence Library + provenance

Repository: HelpUSA/cvss
Branch: chatgpt/evidence-library-provenance
Base: scientific-validation

## ChatGPT already implemented

- tenant-scoped read-only Evidence Library using existing EvidenceSnapshot model;
- navigation entry;
- optional source reference and captured_at fields in guided run;
- payload wiring into existing run API contract;
- provenance display on result traceability;
- styles and regression tests;
- no schema migration and no scorer/rule changes.

## Required validation

Inside web/:
1. npm ci
2. npx prisma validate
3. npx prisma generate
4. npm run typecheck
5. npm run test:saas:unit
6. npm run build

## Browser scenarios

1. Execute a run with no source reference and blank captured_at:
   - run succeeds/abstains according to evidence;
   - snapshot sourceReference remains null;
   - capturedAt uses execution time.

2. Execute a run with:
   - source reference = advisory URL or ADV identifier;
   - explicit captured_at.
   Confirm both are persisted and displayed on result traceability.

3. Open Evidence Library:
   - only current tenant snapshots appear;
   - environment/project labels correct;
   - newest captured evidence first;
   - hash readable without layout overflow;
   - expired snapshot is visibly marked Expirada;
   - empty-state works.

4. Verify tenant isolation using two disposable tenants if available.

5. Test 1440px / 768px / 375px and keyboard focus on provenance details/summary.

## Important

Do not create a second evidence model.
Do not make historical EvidenceSnapshot editable.
Do not implement reuse in this PR unless a critical blocker is discovered.
Do not change scorer, rule catalog, ABSTAIN, TTL thresholds or C1/C2.

## Return

Create:
docs/reviews/ANTIGRAVITY_EVIDENCE_LIBRARY_EXECUTION_REPORT.md

Report:
- tested head;
- tests/typecheck/build;
- no-reference scenario;
- explicit provenance scenario;
- Evidence Library tenant isolation;
- ordering;
- expired-state;
- desktop/tablet/mobile;
- accessibility;
- files changed;
- residual issues;
- MERGE or FIX_REQUIRED.
