# Antigravity handoff — Threat Exploit Maturity

Repository: HelpUSA/cvss
Branch: chatgpt/advanced-threat-exploit-maturity
Base: scientific-validation

## ChatGPT already implemented

- advanced Exploit Maturity section;
- X default;
- A/P/U explicit values;
- separate threat-intelligence reference and observedAt;
- client-side provenance requirement for non-X E;
- server-side E validation;
- invalid/future observedAt rejection;
- environmental-analysis promotion to candidateMetrics.E only for A/P/U with provenance;
- responsive CSS;
- tests and documentation.

## Required validation

Run:
- npm ci
- npx prisma validate
- npx prisma generate
- npm run typecheck
- npm run test:saas:unit
- npm run build
- pytest tests/
- real pipeline

## Runtime cases

A. E=X:
- no threat provenance required;
- no candidateMetrics.E;
- nomenclature remains without T unless another Threat metric exists.

B. E=A with valid reference and observedAt:
- candidate E:A;
- vector/nomenclature should reflect CVSS-BT or CVSS-BTE depending on Environmental metrics.

C. E=P:
- candidate E:P;
- provenance preserved.

D. E=U:
- candidate E:U;
- provenance preserved.

E. E non-X with missing reference:
- client blocks;
- crafted server request rejected.

F. E non-X with missing/invalid/future observedAt:
- rejected server-side.

G. Invalid E value:
- rejected server-side.

H. ABSTAIN interaction:
- Threat E must not bypass stale/missing environmental evidence.

I. Evidence reuse:
- reused snapshot must not invent E if prior metadata did not contain threatIntelligence.
- if metadata does contain threatIntelligence, document actual behavior; do not silently propagate unless clearly intended and fresh.

## Semantic checks

Confirm:
- X is default;
- E comes from threat intelligence;
- no inference from Base score;
- no causal overstatement;
- source and observedAt persist in evidence metadata.

## Do not change

- scorer;
- FIRST arithmetic;
- CR/IR/AR semantics;
- TTL thresholds;
- ABSTAIN;
- C1/C2.

## Return

Create:
docs/reviews/ANTIGRAVITY_ADVANCED_THREAT_EXECUTION_REPORT.md

Include:
- tested HEAD;
- gates;
- cases A-I;
- nomenclature;
- provenance persistence;
- reuse interaction;
- responsive/accessibility;
- files changed;
- residual issues;
- MERGE or FIX_REQUIRED.
