# CVSS Submission Package — Academic Artifacts

Updated: 2026-10-20 (Academic Text Synchronization)

## Manuscript Artifacts

- `article/ieee/cvss40_double_blind.tex` (Canonical IEEE LaTeX double-blind manuscript)
- `article/ieee/cvss40_double_blind.pdf` (Compiled double-blind manuscript)
- `article/generated/cvss40_ieee_manuscript_polished.md` (Full Markdown manuscript)
- `article/generated/cvss40_ieee_manuscript_double_blind.md` (Double-blind Markdown manuscript)

## Core Reproducibility Artifacts

- `outputs/first-reference-corpus-round4.json` (FIRST Reference Corpus Round 5 results: 486,472/486,472 conformant)
- `outputs/metamorphic_campaign_10k_manifest.json` (Metamorphic campaign: 10,000 cases, 0 violations)
- `data/article/cvss40_environmental_scenarios.csv` (Empirical dataset: 30 scenarios)
- `validation/article/cvss40_scenario_metrics.json` (Per-scenario validation and metrics)
- `validation/article/trace/*.json` (Per-scenario reproducible trace artifacts)

## Specification-Level Conformance and Metamorphic Validation

- **FIRST Reference Corpus (Round 5)**: 486,472 / 486,472 test cases conform with 0 divergences against pinned FIRST reference commit `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`.
- **Metamorphic Validation**: 10,000 executions evaluated across four metamorphic relations (MR-1: monotonicity of criticality, MR-2: defense removal monotonicity, MR-3: context permutation invariance, MR-4: irrelevant control invariance) with 0 invariant violations (Campaign ID: `HELPUS-METAMORPHIC-10K-G9B`, Verdict: `PASSED`).
- **Separation Boundary**: Specification-level validation establishes engine correctness and metamorphic invariance under mathematical specifications; it is orthogonal to and does not replace controlled workflow evaluation across curated scenarios.

## Controlled Workflow Evaluation (Hybrid Dataset)

- **Total Scenarios**: 30
- **Real NVD CVSS v4.0 Vulnerability Records**: 12
- **Curated Synthetic Scenarios**: 18
- **Evidence Coverage**: 100.00% (30/30)
- **Trace Completeness**: 100.00% (30/30)
- **Explicit Uncertainty Fields**: 100.00% (30/30)
- **Human Authorization Gate**: Official scoring is non-autonomous by design; this is a workflow governance constraint and does not represent 30 completed independent expert reviews.
- **Operational Priority Shifts**: 22 / 30 scenarios (73.33%)

## Scientific Governance and Claim Boundaries

1. **Human Expert Adjudication**: Independent human expert evaluation is planned under a blinded protocol (`article/expert_review/`) and has NOT been concluded. No expert consensus or inter-rater agreement is claimed.
2. **Confirmatory Protocol G10B**: Protocol G10B remains `PROTOCOL DEFINED / EXECUTION NOT AUTHORIZED`.
3. **Confirmatory Datasets C1 / C2**: Held-out confirmatory benchmark datasets C1 and C2 remain `SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE` until formal execution authorization.
4. **Descriptive Empirical Scope**: The controlled workflow evaluation demonstrates artifact completeness, trace reproducibility, and context sensitivity across curated scenarios under construction-controlled conditions. It does not establish autonomous scoring accuracy, predictive superiority, or production effectiveness.
5. **Double-Blind Integrity**: All author and institutional identities remain strictly withheld for double-blind peer review.
