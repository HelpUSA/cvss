# Antigravity Execution Instructions - HelpUS CVSS AI

## Objective

Use this package as the reviewed pre-freeze baseline. Merge the reviewed code, scientific documentation and Overleaf sources into the local HelpUS CVSS project; update the production-facing application semantics; synchronize `docs/scientific-validation/`; then return evidence that all release gates have passed. Do **not** invent or pre-fill experimental outcomes.

## Absolute rules

1. Do not start C1/C2 held-out evaluation until the release gates below pass.
2. Do not describe Dataset B as confirmatory validation or evidence of generalization.
3. Do not convert CVSS v3.x to v4.0 silently.
4. Do not call a CNA-provided score an NVD-authored score merely because NVD indexes it.
5. Do not mix CVSS severity (`None/Low/Medium/High/Critical`) with HelpUS operational disposition (`P0-P4`).
6. Do not use `Defer` as a CVSS severity.
7. Do not use a firewall/WAF alone to infer `MAC:H`.
8. Do not infer `MAV:A`/`MAV:L` simply because a service is not Internet-facing.
9. Do not infer `AR:L` from redundancy or high availability. CR/IR/AR must come from an explicit versioned organization policy.
10. Do not claim `100% correct`, `zero hallucination`, `immutable`, `guaranteed`, or compliance certification without evidence that specifically supports the claim.
11. Do not manually type benchmark percentages, p-values, confidence intervals or sample counts into LaTeX. Generate them from machine-readable data.
12. Do not call a HelpUS-derived Environmental vector “official”; call it a CVSS v4.0-compliant/HelpUS-derived Environmental vector.

## Gate 1 - Comprehensive CVSS v4.0 calculator validation

The bundled 10-case test is a smoke/regression suite only. It is not sufficient evidence of calculator conformance.

Required actions:
- Pin the exact calculator implementation/version/commit used by production.
- Pin a specific commit/release of the FIRST `cvss-resources` reference corpus.
- Run the full valid reference corpus and negative tests against the calculator.
- Persist raw input, expected value, observed value, status, calculator version and corpus commit.
- Generate `CVSS_V4_CONFORMANCE_REPORT.md` directly from raw results.
- Explain every discrepancy. C1/C2 must not begin while unexplained calculator discrepancies remain.
- Add backend/frontend parity testing so the UI and backend calculate the same vector/score for the same corpus input.

Do not restore the earlier stale `10/10 comprehensive conformance` claim. The included report intentionally marks full corpus validation as pending.

## Gate 2 - Dataset B source provenance and CVSS nomenclature

Re-audit all 12 real-CVE rows in Dataset B from authoritative/current records available locally or via permitted sources.

For each source assessment store at least:
- `cve_id`
- `cvss_version`
- full source vector
- source nomenclature (`CVSS-B`, `CVSS-BT`, etc.)
- source score and severity
- metric provider / provider role
- CNA and indexing source when applicable
- source URL or record identifier
- published / last-modified / retrieved timestamps
- record version/hash where practical

Important:
- A vector containing an explicit Threat metric such as `E:P`, `E:A`, or `E:U` is not a pure Base-only input. Preserve the correct nomenclature.
- Preserve competing CNA/NVD assessments separately; never overwrite one with the other.
- If a real CVE has no defensible source-backed CVSS v4.0 assessment, replace it for the source-backed v4.0 subset or mark an investigator-authored assessment explicitly. Never invent a conversion.
- `dataset_b_source_assessments_normalized.csv` is a migration/provenance draft until the authoritative re-audit is complete.
- The legacy 3/12 (25%) transition observation must not be promoted as a scientific/product KPI until Dataset B source semantics and the local operational mapping are re-audited. If shown at all, label it as a legacy development-stage observation with numerator/denominator.

Regenerate all Dataset B tables/figures from the canonical machine-readable source after the audit.

## Gate 3 - Merge the reviewed engine invariants

Apply or preserve the semantics in `core/ai_evidence_engine.py` in the real production engine:
- absent/unknown evidence => abstain;
- stale evidence => abstain according to versioned freshness policy;
- conflicting routes/firewall evidence => abstain;
- `PUBLIC_ROUTED` and `INTERNAL_ROUTED` => candidate `MAV:N`;
- `ADJACENT_ONLY` => candidate `MAV:A` only with explicit adjacency evidence;
- `LOCAL_ONLY` => candidate `MAV:L`;
- `PHYSICAL_ONLY` => candidate `MAV:P`;
- firewall/WAF presence alone never sets `MAC:H`;
- exploit-specific preconditions may support a MAC change only when documented;
- CR/IR/AR and modified-impact mappings require an explicit organization policy ID and version;
- redundancy/high availability does not imply `AR:L`;
- insufficient/conflicting evidence must set `HUMAN_REVIEW_REQUIRED` and prevent automatic downgrade;
- until the held-out study is complete, contextual recommendations remain provisional and HITL-gated.

Make the evidence freshness window policy-driven rather than hidden hard-coded behavior. Record policy version/effective date.

## Gate 4 - Tests and reproducibility

Run the entire repository test suite from a clean dependency-locked environment, not only the bundled targeted tests.

At minimum include regression tests for:
- missing evidence;
- stale evidence;
- conflicting evidence;
- same IP/CIDR in different routing domains;
- internal L3 routing => `MAV:N`;
- true adjacent-only condition => `MAV:A`;
- local-only condition => `MAV:L`;
- firewall does not imply `MAC:H`;
- high availability does not imply `AR:L`;
- CR/IR/AR mapping without policy => abstain/review;
- incomplete ACL/NAT/VPN states => review;
- no automatic downgrade on insufficient evidence;
- source/vector parsing;
- vector synthesis;
- backend/frontend CVSS parity;
- provenance receipt generation.

Persist raw test outputs. Regenerate `TEST_REPORT.md` from observed results.

## Gate 5 - Production web application synchronization

Update `cvss.helpusbr.com` and its local source so the UI/logic match the scientific model.

Required UI separation:
1. Source assessment/provenance.
2. HelpUS-derived CVSS v4.0 Environmental vector, score and CVSS severity.
3. Local operational disposition P0-P4.
4. Evidence/provenance chain.
5. HITL decision/status.
6. Abstention status/reason.

Required removals/qualifications:
- Dataset B must be labeled Development Benchmark, never “validated 30-scenario scientific proof”.
- Remove/qualify `100% agreement`, `zero hallucination`, `guaranteed`, `immutable`, and universal compliance claims.
- Historical presets must be labeled historical/illustrative; Allodi et al. 2017 is a historical CVSS v3.0 human-assessment baseline, not a CVSS v4.0 ground truth.
- Remove any public logic/text that implies `internal_only => MAV:A`.
- Do not use P4 as automatic risk acceptance; label it `P4_DEFER_RECOMMENDED` until an authorized human decision.
- Do not reuse SSVC `Act/Attend/Track` as local HelpUS labels.

Audit receipt pipeline:
`JSON Schema validation -> RFC 8785/JCS canonicalization -> SHA-256`.
Digital signatures, Merkle proofs and trusted timestamps are separate layers. A Merkle tree is a tamper-evident structure within its threat model, not absolute immutability.

## Gate 6 - Experimental protocol finalization

Use `EXPERIMENT_PROTOCOL_v1.0_DRAFT.md`, `HELDOUT_CUSTODY_PROTOCOL.md`, and related documents as the starting point.

Before freeze, finalize:
- C1 target population or call it “Independent Diverse Held-Out Set” rather than representative;
- C1/C2 inclusion/exclusion rules;
- metric eligibility independent of HelpUS output;
- reporting of agreement + coverage + abstention together;
- expert selection and COI policy;
- ethics/IRB/REB/exemption determination as actually applicable;
- supplied-material-only blinding;
- scenario randomization seed/procedure;
- pre-adjudication agreement preservation;
- adjudication procedure and `REFERENCE_UNRESOLVED` handling;
- evidence sufficiency labels (`SUFFICIENT`, `INSUFFICIENT`, `CONFLICTING`);
- primary CI method for SFDR (pre-specified); sensitivity interval if desired;
- technical rerun vs model/ruleset retuning policy;
- pilot archival policy;
- failure classification process;
- evidence-quality audit sample/100% audit decision.

Do not call a Git freeze “preregistration” unless the protocol is deposited externally before results.

## Gate 7 - Historical statistics and Dataset A

Treat the 2017 work as historical human-assessment evidence, not a native CVSS v4.0 experiment.

Keep distinct:
- `A1`: historical 2017 human results;
- optional `A2`: new CVSS v4.0 re-annotation, if conducted later.

Historical Fisher statistics must be generated by script. The reviewed reproducibility script reports:
- two-sided Fisher p ~= 4.2235e-6;
- sample cross-product OR ~= 3.388;
- conditional MLE OR ~= 3.377;
- conditional exact 95% CI ~= [1.913, 6.184].

Do not manually mix an asymptotic formula with a conditional exact interval. State the estimator/method explicitly.

Use the correct bibliographic metadata: Allodi et al., FDSE 2017. Do not call the publication ESSoS 2017 in scholarly metadata.

## Gate 8 - Book / Overleaf

Use the accompanying reviewed Overleaf ZIP as the source baseline.

It already:
- separates CVSS severity from P0-P4;
- labels Dataset B as development-stage;
- separates historical 2017 results from prospective v4.0 evaluation;
- removes manual per-metric score deltas;
- tones down unsupported regulatory/economic/accuracy claims;
- moves ExposureAdjustedEPSS to exploratory/future work;
- expands Threats to Validity;
- fixes headers/wide tables/Markdown artifacts;
- generates historical statistics through LaTeX macros.

After local Dataset B source re-audit, regenerate the affected appendix/table through scripts. Do not hand-edit numerical claims.

Do not add C1/C2 results until those experiments actually occur.

Build cleanly with bibliography, render/inspect all pages and record:
- Git SHA / source state;
- build timestamp;
- TeX tool versions;
- PDF page count;
- PDF SHA-256;
- undefined refs/citations;
- visual inspection result.

## Gate 9 - Bibliography audit

Verify every entry in `references.bib` against a real primary source/DOI/official publication. Confirm that each citation supports the sentence where it is used.

Do not reintroduce unverified/fabricated references. Prefer primary standards/specifications and original papers.

## Gate 10 - `docs/` synchronization

Copy/update the scientific-validation package under the project repository, preferably:
`docs/scientific-validation/`

At minimum synchronize:
- `ANTIGRAVITY_EXECUTION_INSTRUCTIONS.md`
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
- `STATISTICAL_REPRODUCIBILITY_REPORT.md`
- `TEST_REPORT.md`
- `WEB_APP_REQUIRED_PATCHES.md`
- `TODO_EXTERNAL_VALIDATION.md`
- `BOOK_CHANGELOG.md`
- final build manifest.

## Freeze decision

Do **not** freeze the confirmatory engine/protocol until all of the following are true:
- comprehensive FIRST corpus validation is complete with no unexplained calculator discrepancies;
- all 12 real Dataset B sources/provenance are re-audited;
- complete clean-repository tests and backend/frontend parity pass;
- production web semantics are synchronized;
- book is rebuilt from the audited data and passes visual checks;
- ethics determination is appropriately documented;
- held-out custody, expert protocol, metric eligibility and statistical plan are finalized.

## Required return package from Antigravity

Return:
1. exact files changed;
2. Git diff summary;
3. commit SHA(s), dependency lockfile and OCI digest if available;
4. all test commands and raw results;
5. FIRST corpus commit and valid/negative test statistics;
6. audited 12-CVE provenance table with source nomenclature;
7. production URL smoke-test screenshots/results for PT/EN/ES;
8. compiled final book PDF and Overleaf ZIP;
9. updated `docs/scientific-validation/` tree;
10. unresolved blockers/TODOs;
11. explicit decision: `SAFE_TO_FREEZE = YES/NO`, with reasons.

## Scope discipline

Do not add feature creep (KEV, SSVC, Terraform, Kubernetes, PKI enhancements) as a prerequisite for the scientific freeze unless it is necessary to support a specific experimental claim. Scientific correctness, source provenance, fail-safe behavior and reproducibility come first.
