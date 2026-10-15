# Antigravity continuation — CG-040

Date: 2026-10-15
Repository: HelpUSA/cvss
Branch: chatgpt/cg040-gemini-audit-validation

## Mandatory first reads

1. docs/reviews/GEMINI_AUDIT_VALIDATION_2026-10-15.md
2. docs/reviews/CG040_IMPLEMENTATION_FINDINGS.md
3. docs/architecture/CVSS_SENSITIVITY_ENVELOPE_POLICY.md

Do not reimplement work already present in this branch.

## ChatGPT already completed

- restored authenticated GitHub read/write access;
- reviewed Gemini recommendations against the current repository;
- confirmed PR #28 and #29 are merged;
- pinned pyproject scorer dependency to cvss==3.6 to match the scientific gate;
- tightened the FIRST corpus gate to exact one-decimal score equality;
- added bounded score-envelope sensitivity utility outside the canonical scorer;
- added corrected non-expansion uncertainty test support;
- added targeted EQ3/EQ6 CR/IR/AR cross-product regression tests;
- confirmed TTL/freshness already exists and did not duplicate it;
- confirmed MVC/MVI/MVA and MSC/MSI/MSA support already exists;
- confirmed MR-1 already covers criticality monotonicity;
- confirmed JCS implementation already exists;
- added Unicode-as-is JCS regression to prevent silent NFC normalization;
- preserved historical expert/HITL artifacts while keeping them out of active operational semantics.

## Your task is validation/completion, not redesign

Run against THIS exact branch/head and return raw results.

### Python

From a clean environment with exact dependencies:

1. verify cvss==3.6;
2. run:
   - pytest tests/test_cvss_sensitivity.py
   - pytest tests/test_cvss_eq3_eq6_regression.py
   - pytest tests/test_environmental_metamorphic_rules.py
   - pytest tests/test_fail_safe_abstention.py
   - pytest tests/test_first_reference_gate_contract.py
3. run the full pytest suite;
4. run scripts/run_first_reference_corpus_round4.py;
5. require ZERO score mismatches;
6. run scripts/run_metamorphic_campaign.py;
7. do not regenerate/tune against sealed C1/C2.

### Web

Inside web/:

1. npm ci
2. npx prisma validate
3. npx prisma generate
4. npm run typecheck
5. npm run test:saas:unit
6. npm run build
7. run the existing JCS scripts, including RFC example/conformance contracts.

Confirm web/tests/jcs-unicode-policy.test.ts passes and that composed/decomposed Unicode remain distinct canonical strings.

### EQ3/EQ6 inspection

Inspect the installed cvss==3.6 implementation and confirm the coupled EQ3/EQ6 logic is preserved. Do not rewrite the scorer if the pinned FIRST corpus remains zero-mismatch.

If any mismatch appears:
- record vector;
- expected score;
- observed score;
- macrovector;
- exact dependency versions;
- do not paper over it with tolerance.

### Sensitivity short-circuit

Do NOT connect score_envelope() to production ABSTAIN yet.

Instead:
1. run experiments on synthetic/reference-safe vectors;
2. identify which unresolved metric domains are legitimately enumerable;
3. produce a machine-readable table of invariant/non-invariant cases;
4. specifically test the Gemini AR/VA/SA assertion rather than assuming it;
5. propose integration only if domain derivation can be deterministic and audit-preserving.

### Freshness

Current TTL is already implemented. Do not add a second competing mechanism.

Assess whether an additive schema migration to observed_at/evaluation_time/max_ttl_seconds is operationally worthwhile. If proposed, preserve backward compatibility with telemetry_age_days and provide migration/tests. Do not change current frozen behavior solely for naming.

### JCS / hashing

Do not add NFC normalization inside the JCS canonical domain.

Check whether Python evidence_hash requires cross-language canonical equivalence with TypeScript audit receipts. If yes, prepare a separate proposal/test corpus first; do not silently change historical hashes.

### Expert/HITL cleanup

Do not delete historical expert-study files/tests.

Verify active production UX and routes do not require experts/HITL. Check the actual cvss.helpusbr.com deployment source and current deployed SHA. Report any stale legacy wording.

### Required return

Commit your evidence/results on top of this branch or open a PR targeting it.

Return:
- exact head SHA tested;
- dependency versions;
- all commands;
- pass/fail counts;
- FIRST corpus evaluated count and mismatch count;
- metamorphic campaign result;
- web unit/typecheck/build result;
- JCS result;
- browser/production deployment SHA;
- residual issues;
- any proposed code change separately justified.

Do not declare completion if tests were not actually executed.
