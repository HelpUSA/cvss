# Antigravity handoff — safe evidence reuse

Repository: HelpUSA/cvss
Branch: chatgpt/evidence-reuse-safety
Base: scientific-validation

## ChatGPT already implemented

- same-environment reusable evidence query;
- tenant-scoped filtering;
- reuse selector in Step 4;
- expired snapshots disabled in UI;
- prefill of reusable evidence fields;
- GUIDED_REUSE lineage;
- backend validation of tenant/environment;
- backend rejection of expired snapshots;
- server-side telemetry age recomputation from original capturedAt;
- immutable-copy behavior creating a new EvidenceSnapshot;
- regression tests.

## Required validation

Inside web/:

1. npm ci
2. npx prisma validate
3. npx prisma generate
4. npm run typecheck
5. npm run test:saas:unit
6. npm run build

Run Python suite if required by CI.

## Runtime scenarios

### A. Same environment, fresh snapshot
- select existing snapshot;
- fields prefill;
- execute;
- expect new run + new EvidenceSnapshot;
- original snapshot unchanged;
- sourceType = GUIDED_REUSE;
- metadata contains reusedEvidenceSnapshotId.

### B. Expired snapshot
- visible but disabled in selector;
- direct crafted request with its ID must be rejected server-side.

### C. Foreign environment same tenant
- crafted request with snapshot from another environment must be rejected.

### D. Foreign tenant
- crafted request with snapshot from another tenant must be rejected/not found.

### E. Age manipulation
- craft client payload with telemetryAgeDays=0 for an old reused snapshot;
- server must overwrite/recompute current age from original capturedAt before analysis.

### F. Freshness outcome
- if recomputed age exceeds maxTelemetryAgeDays, engine should fail closed according to existing rules.

## Immutability proof

Verify no update/delete occurs on original EvidenceSnapshot.
New run must reference a newly created snapshot.

## Accessibility/responsive

Validate reuse disclosure/select at 1440px, 768px, 375px, keyboard navigation and zoom 200%.

## Do not change

- scorer;
- rule catalog;
- ABSTAIN semantics;
- TTL thresholds;
- C1/C2;
- historical snapshots.

## Return

Create:
docs/reviews/ANTIGRAVITY_EVIDENCE_REUSE_EXECUTION_REPORT.md

Include:
- tested HEAD;
- gates;
- scenarios A-F;
- tenant isolation;
- same-environment enforcement;
- expired rejection;
- age recomputation proof;
- immutability proof;
- responsive/accessibility;
- files changed;
- residual issues;
- MERGE or FIX_REQUIRED.
