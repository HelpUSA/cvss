# Antigravity handoff — Supplemental Metrics

Repository: HelpUSA/cvss
Branch: chatgpt/supplemental-metrics
Base: scientific-validation

## ChatGPT already implemented

- all six FIRST Supplemental Metrics;
- X defaults;
- progressive-disclosure UI;
- server-side exact-value validation;
- separate supplementalMetrics path in analysis service;
- vector enrichment including Supplemental Metrics;
- explicit separation from candidateMetrics;
- result-page Supplemental Metrics summary;
- evidence metadata persistence via existing EvidenceSnapshot;
- tests/docs;
- no scorer or rule changes.

## Required validation

Run:
1. npm ci
2. npx prisma validate
3. npx prisma generate
4. npm run typecheck
5. npm run test:saas:unit
6. npm run build
7. pytest tests/
8. real pipeline

## Core invariant to prove

For the same Base/Threat/Environmental metrics:

adding or changing only Supplemental Metrics MUST NOT change the numerical CVSS score.

Test at least:
- no Supplemental vs S:P;
- AU:Y;
- R:I;
- V:C;
- RE:H;
- U:Red;
- all six together.

The vector may change; the score must remain identical.

## Runtime cases

A. All X:
- no supplemental segments should be emitted if X values are omitted by enrichment logic;
- score/nomenclature unchanged.

B. Each valid metric:
- S:N/P
- AU:N/Y
- R:A/U/I
- V:D/C
- RE:L/M/H
- U:Clear/Green/Amber/Red

Confirm vector acceptance and no score change.

C. Invalid values:
- crafted request with S=H, AU=A, R=Z, V=H, RE=Red, U=High, etc.
- server must reject.

D. Result page:
- non-X supplemental values shown in dedicated "Contexto suplementar" section;
- clear statement that they do not alter numerical CVSS score;
- candidateMetrics explanation remains separate.

E. ABSTAIN:
- Supplemental Metrics must not cure missing/stale/conflicting environmental evidence.

F. Threat + Environmental + Supplemental:
- confirm CVSS-BTE numerical score equals same BTE vector without Supplemental Metrics;
- supplemental segments preserved in vector.

G. Evidence reuse:
- verify current reuse behavior does not silently invent new Supplemental Metrics.
- document if prior supplemental metadata is prefilled or not; do not add hidden propagation in this PR.

## FIRST semantics

Check labels against official definitions:
- Safety Present/Negligible;
- Automatable Yes/No;
- Recovery Automatic/User/Irrecoverable;
- Value Density Diffuse/Concentrated;
- Response Effort Low/Moderate/High;
- Provider Urgency Clear/Green/Amber/Red.

## Accessibility/responsive

Test 1440px / 768px / 375px, keyboard details/summary, selects, zoom 200%.

## Do not change

- canonical scorer;
- Threat E semantics;
- CR/IR/AR governance;
- ABSTAIN;
- TTL;
- C1/C2.

## Return

Create:
docs/reviews/ANTIGRAVITY_SUPPLEMENTAL_METRICS_REPORT.md

Include:
- tested HEAD;
- gates;
- per-metric cases;
- score invariance proof;
- vector behavior;
- invalid-value rejection;
- result display;
- ABSTAIN;
- BTE+Supplemental;
- evidence reuse interaction;
- responsive/accessibility;
- files changed;
- residual issues;
- MERGE or FIX_REQUIRED.
