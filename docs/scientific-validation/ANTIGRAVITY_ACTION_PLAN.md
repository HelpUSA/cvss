# ANTIGRAVITY_ACTION_PLAN.md

## Objective

Merge the attached reviewed files into the local HelpUS CVSS repository and bring the production web application, scientific artifacts and `docs/` directory into one consistent state **before** the experimental freeze. Do not invent results.

## Blocking tasks, in order

### Gate 1 - CVSS calculator validation
- Replace the old 10-case "conformance" claim with the corrected smoke-suite wording in this package.
- Pin `FIRSTdotorg/cvss-resources` and run the comprehensive reference set + negative tests.
- Persist raw JSON/CSV results and regenerate `CVSS_V4_CONFORMANCE_REPORT.md` automatically.
- Do not begin C1/C2 until unexplained discrepancies are zero.

### Gate 2 - Dataset B provenance/nomenclature
- Use `data/article/dataset_b_source_assessments_normalized.csv` as the migration target.
- Re-retrieve/verify all 12 real source assessments.
- Record the actual source nomenclature. Explicit `E:P/U/A` means Threat is selected; do not call such a score pure CVSS-B.
- Preserve competing CNA/NVD assessments separately.
- Regenerate book tables from the canonical machine-readable source.

### Gate 3 - Engine semantics and fail-safe
Apply the reviewed `core/ai_evidence_engine.py` invariants to the production engine:
- missing/stale/conflicting/unknown evidence -> abstain;
- internal routed -> MAV:N;
- adjacent only with explicit L2/adjacent semantics -> MAV:A;
- local-only -> MAV:L;
- firewall/WAF alone never -> MAC:H;
- CR/IR/AR only through a versioned organization policy;
- redundancy/high availability never automatically -> AR:L;
- automatic downgrade remains disabled until HITL approval.

### Gate 4 - Full local tests
- Run the complete repository suite in a clean dependency-locked environment.
- Add tests listed in `WEB_APP_REQUIRED_PATCHES.md`.
- Run backend/frontend CVSS parity over the pinned FIRST corpus.
- Save raw outputs and regenerate `TEST_REPORT.md`.

### Gate 5 - Production web synchronization
Implement all items in `WEB_APP_REQUIRED_PATCHES.md`. In particular:
- Dataset B = development benchmark, not validation;
- no `100%`, `zero hallucination`, `immutable`, `guaranteed`, or false-positive/noise-reduction claim without measured denominator;
- the 25% figure, if retained, is only `3/12 legacy development-stage transition observation`;
- no `internal_only -> MAV:A`;
- separate source assessment, HelpUS CVSS-BE output, P0-P4 operational policy, evidence and HITL.

### Gate 6 - Book/Overleaf
- Start from the accompanying reviewed Overleaf ZIP.
- Merge any later local source-audit results through the generation pipeline, not by editing numbers manually.
- Build with bibliography, inspect every page, and archive build manifest + PDF SHA256.
- Do not add C1/C2 results until the held-out experiment actually runs.

### Gate 7 - Experimental freeze
Only after Gates 1-6:
- finalize `EXPERIMENT_PROTOCOL_v1.0.md`;
- record engine Git SHA, ruleset version, policy version, dependency lockfile and OCI digest;
- complete institutional ethics determination;
- freeze C1/C2 custody protocol;
- recruit blinded independent experts;
- execute held-out study without retuning.

## `docs/` synchronization
Copy/update at least the following in the local project's `docs/scientific-validation/` directory:
- `ANTIGRAVITY_ACTION_PLAN.md`
- `CVSS_CALCULATOR_PROVENANCE.md`
- `CVSS_V4_CONFORMANCE_REPORT.md`
- `DATASET_SOURCE_AUDIT.md`
- `EXPERIMENT_PROTOCOL_v1.0_DRAFT.md`
- `HELDOUT_CUSTODY_PROTOCOL.md`
- `BENCHMARK_RERUN_POLICY.md`
- `FAILURE_TAXONOMY.md`
- `EVIDENCE_QUALITY_PROTOCOL.md`
- `ETHICS_REVIEW_CHECKLIST.md`
- `EXPERT_COI_FORM.md`
- `EXPERT_CONSENT_TEMPLATE.md`
- `TEST_REPORT.md`
- `WEB_APP_REQUIRED_PATCHES.md`
- `TODO_EXTERNAL_VALIDATION.md`
- `BOOK_CHANGELOG.md`

## Required final response from Antigravity
Return:
1. exact files changed;
2. Git diff summary;
3. all test commands and raw results;
4. FIRST corpus commit and conformance statistics;
5. audited 12-CVE provenance table;
6. production URL smoke-test results;
7. compiled book PDF + Overleaf ZIP;
8. updated `docs/` tree;
9. unresolved blockers;
10. explicit statement whether engine/protocol are now safe to freeze.
