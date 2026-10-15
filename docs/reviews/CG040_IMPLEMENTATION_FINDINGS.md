# CG-040 implementation findings

Date: 2026-10-15
Branch: chatgpt/cg040-gemini-audit-validation

## Executive result

Gemini identified useful risk areas, but several recommendations described gaps that are already implemented or were stated too strongly. This branch applies only evidence-backed, low-risk improvements and adds safeguards without silently retuning the frozen deterministic baseline.

## Findings by topic

### Canonical FIRST scorer

Current implementation:
- core/cvss40.py delegates to cvss==3.6;
- release gate pins FIRST cvss-resources commit d766d0c8ab4368b67bf27dd0e411eb481f05fdbb;
- the project overrides package rounding to match FIRST JavaScript one-decimal behavior.

Changes in CG-040:
- pyproject.toml now pins cvss==3.6, matching the validated release gate;
- FIRST corpus gate now requires exact one-decimal score equality instead of accepting an absolute delta below 0.05;
- targeted EQ3/EQ6 regression tests cover CR/IR/AR cross-products over partial-impact vectors.

Decision:
- do not migrate to Decimal or Rust without a demonstrated reference-corpus mismatch.

### EQ3/EQ6

Accepted as a high-risk implementation area. The complete FIRST corpus remains the normative oracle. Fast targeted tests were added to expose lookup failures/determinism regressions in this region.

### Sensitivity / over-abstention

The production ABSTAIN policy is not changed.

Added core/cvss_sensitivity.py as an isolated proof utility. It:
- varies only valid Threat/Environmental candidate metrics;
- delegates every score to the existing canonical scorer;
- returns score_min, score_max and invariant;
- caps Cartesian expansion;
- cannot modify Base metrics.

This permits future proof that an unresolved metric domain is score-invariant without guessing its value.

Activation is intentionally deferred until metric-domain derivation is formally specified and validated against FIRST.

### Evidence freshness / TTL

Gemini's proposed TTL concept already exists:
- dynamic telemetry default maximum age: 1 day;
- static telemetry default maximum age: 7 days;
- override: max_telemetry_age_days;
- stale evidence causes fail-closed ABSTAIN;
- near-expiry evidence can produce AUTO_ACCEPT_WITH_WARNING.

No duplicate TTL subsystem was added.

Future schema work may migrate from age-in-days to observed_at/evaluation_time while preserving current semantics, but that is an operational schema evolution rather than a missing safety control.

### Modified impact controls

The executable catalog already supports:
- MVC, MVI, MVA;
- MSC, MSI, MSA;
- policy provenance requirements.

Therefore Gemini's claim that local modified impact coverage is absent is not true for the current repository.

No heuristic control-to-metric mapping was added. Presence of a control remains insufficient to change a metric.

### Metamorphic testing

MR-1 already is monotonicity of criticality, equivalent to the proposed Gemini MR-5 concept.

Existing high-volume campaign covers MR-1 through MR-4 across 10,000 seeded cases.

Added corrected uncertainty property support:
- new envelope must be contained in the previous envelope;
- strict contraction is not universally required;
- tests verify non-expansion when admissible domains narrow.

The historical G9B campaign is not rewritten; the new property is additive post-freeze validation.

### JCS / RFC 8785

Frontend already contains:
- JCS-compatible canonicalizer;
- RFC 8785 published-example regression;
- non-finite number rejection;
- lone surrogate rejection;
- structural/hash invariance checks.

Added an explicit test that canonically hashed Unicode is preserved as-is and is not silently NFC-normalized.

This protects against the incorrect interpretation that NFC normalization is part of JCS.

The existing documentation remains conservative: formal RFC 8785 conformance requires a pinned independent corpus.

### Expert/HITL legacy

Active SaaS authorization uses REVIEWER as an optional tenant role. Current UX architecture explicitly removes mandatory expert/HITL semantics from the operational path.

Legacy artifacts still exist, including tests/test_expert_portal_blinding.py and historical expert portal files. They are research/history artifacts and should not be deleted merely because the operational model changed.

Production/browser verification is still required to ensure stale deployment content is no longer serving old expert/HITL language.

## Files changed/added in CG-040

- pyproject.toml
- scripts/run_first_reference_corpus_round4.py
- core/cvss_sensitivity.py
- tests/test_cvss_sensitivity.py
- tests/test_cvss_eq3_eq6_regression.py
- web/tests/jcs-unicode-policy.test.ts
- docs/architecture/CVSS_SENSITIVITY_ENVELOPE_POLICY.md
- docs/reviews/GEMINI_AUDIT_VALIDATION_2026-10-15.md
- docs/reviews/CG040_IMPLEMENTATION_FINDINGS.md
- docs/tasks/ANTIGRAVITY_CG040_COMPLEMENT.md

## What was deliberately not changed

- frozen deterministic rule catalog behavior;
- production ABSTAIN decision;
- C1/C2 sealed material;
- historical expert-study evidence;
- control-to-metric semantics;
- JCS Unicode normalization;
- scorer numeric type.

## Validation still required in executor environment

- install exact locked dependencies;
- run pytest including new tests;
- run complete FIRST reference corpus gate;
- run the existing 10k metamorphic campaign;
- run web TypeScript tests, typecheck and build;
- run JCS tests;
- verify production deployment source/browser behavior;
- return exact command output and current-head hashes.
