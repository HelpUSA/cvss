# Operationalizing CVSS v4.0 Environmental Metrics with Evidence Normalization, Governance, and Traceability

Generated UTC: `2026-07-13T19:33:32.800768+00:00`

## Abstract

CVSS v4.0 defines Environmental metrics that allow vulnerability severity to be adapted to a consumer organization's deployment context. However, selecting Environmental metric values remains evidence-intensive because local asset criticality, exposure, compensating controls, and operational requirements are often distributed across multiple sources. This paper presents an evidence normalization, governance, and traceability workflow for collecting, structuring, and tracing environmental evidence used to support CVSS v4.0 Environmental metric assessment. The workflow preserves official CVSS v4.0 semantics and treats candidate recommendations as subject to explicit human authorization, not as autonomous official scoring. The evaluation strictly separates specification-level arithmetic conformance validation from controlled workflow evaluation across curated scenarios. At the specification level, the scoring core demonstrated 100.0% conformance across 486,472 official FIRST reference corpus vectors (commit `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`) and zero invariant violations across 10,000 metamorphic executions. Under controlled scenario evaluation with a hybrid dataset of 30 scenarios (12 real NVD records carrying CVSS v4.0 data and 18 curated synthetic cases), the workflow achieved 100.0% evidence coverage, 100.0% trace completeness, and operational priority changes in 22 of 30 scenarios. The evaluation demonstrates workflow schema completeness, context sensitivity, and traceability under construction-controlled conditions; it does not establish autonomous scoring accuracy, predictive superiority, or production effectiveness.

## Keywords

CVSS v4.0; Environmental metrics; vulnerability prioritization; cybersecurity risk; evidence normalization; governance; human-in-the-loop; traceability; reproducibility; uncertainty.

## I. Introduction

The Common Vulnerability Scoring System is widely used to communicate vulnerability severity. In practice, however, vulnerability handling decisions often require more than a Base score. A vulnerability affecting an isolated lab asset, an identity provider, a public API gateway, or an operational technology monitoring component may require different remediation urgency even when the Base severity appears similar.

CVSS v4.0 provides a structured distinction between Base, Threat, Environmental, and Supplemental information [1], [2]. This distinction matters because Base metrics describe vulnerability characteristics, while Environmental metrics allow a consumer organization to represent local deployment context [2], [3]. The challenge addressed in this work is therefore operational rather than definitional: selecting Environmental metric values consistently requires evidence, local context, uncertainty handling, and reviewable decision records.

This paper proposes an evidence normalization, governance, and traceability workflow for Environmental metric assessment. The workflow collects and structures evidence, suggests candidate Environmental metric values through deterministic policy rules with assistive evidence ingestion, flags uncertainty, enforces human authorization constraints, and exports trace artifacts. The contribution provides: (1) a strict scientific separation between specification-level arithmetic conformance (486,472 FIRST reference cases; 10,000 metamorphic executions with zero violations) and controlled workflow evaluation across curated scenarios; (2) an evidence normalization and human-in-the-loop governance workflow for collecting and structuring environmental evidence; (3) a trace model linking evidence, candidate metrics, uncertainty, and review state; (4) a controlled evaluation dataset of 30 curated scenarios exercising schema coverage (12 NVD records, 18 synthetic cases, 22 priority shifts); and (5) a reproducible artifact package. The contribution is a method and prototype workflow, not a new scoring standard.

## II. Background: CVSS v4.0 and Environmental Metrics

CVSS v4.0 separates vulnerability scoring and contextual information into metric groups including Base, Threat, Environmental, and Supplemental metrics [1], [2]. The workflow in this paper preserves that structure. Base CVSS information is stored separately as the severity baseline. Threat context is treated as time-sensitive evidence requiring review. Environmental assessment support is the main focus because it depends directly on consumer-side deployment context.

The workflow strictly adheres to the official CVSS v4.0 nomenclature and scoring mechanics [2], [3]:
- **CVSS-B:** Base metrics only (AV, AC, AT, PR, UI, VC, VI, VA, SC, SI, SA).
- **CVSS-BT:** Base and Threat metrics (incorporating Exploit Maturity $E$).
- **CVSS-BE:** Base and Environmental metrics (incorporating consumer context via Modified Base metrics and Security Requirements).
- **CVSS-BTE:** Base, Threat, and Environmental metrics combined.

Environmental assessment operates across two mechanisms:
1. **Modified Base Metrics:** Override intrinsic Base parameters when local deployment context alters exposure or impact. These include Modified Attack Vector (MAV), Modified Attack Complexity (MAC), Modified Attack Requirements (MAT), Modified Privileges Required (MPR), Modified User Interaction (MUI), Modified Vulnerable System Impacts (MVC, MVI, MVA), and Modified Subsequent System Impacts (MSC, MSI, MSA). Unmodified metrics default to their Base values.
2. **Security Requirements:** Express consumer-side mission criticality for Confidentiality Requirement (CR), Integrity Requirement (IR), and Availability Requirement (AR), taking values in $\{\text{High}, \text{Medium}, \text{Low}, \text{Not Defined}\}$.

Under the FIRST CVSS v4.0 standard, vectors are mapped into a 6-dimensional MacroVector $\vec{M} = (EQ_1, EQ_2, EQ_3, EQ_4, EQ_5, EQ_6)$ representing discrete Equivalence Sets with precomputed boundary scores. The workflow does not reimplement or approximate this algorithm; it normalizes evidence into valid Environmental metrics and delegates calculation directly to the canonical FIRST-compatible scoring core (validated against 486,472 official reference vectors).

## III. Problem Statement

Although CVSS v4.0 defines Environmental metrics, applying them in a real consumer environment remains difficult. Analysts must determine asset importance, exposure, privilege context, compensating controls, confidentiality requirements, integrity requirements, availability requirements, and candidate Modified Base metric values. These inputs may be incomplete, distributed across multiple systems, or inconsistently documented.

This creates three practical problems. First, Environmental decisions may not be reproducible when the evidence trail is missing. Second, analysts may make inconsistent choices across similar assets. Third, remediation prioritization may over-rely on Base severity even when local context should change urgency.

## IV. Proposed AI/Watcher Workflow

The proposed workflow supports the analyst through eight steps: ingest vulnerability and Base CVSS v4.0 information; collect local environmental evidence; structure that evidence into scenario fields; suggest candidate Environmental metric values; attach evidence and rationale to each recommendation; flag uncertainty and missing evidence; require explicit human review status; and export CSV, JSON, report, and table artifacts for reproducibility.

The workflow does not modify the official CVSS v4.0 formula. It evaluates evidence normalization, policy resolution, and trace generation rather than the semantic extraction accuracy of a generative AI model. Assistive processing is strictly limited to ingestion support, and the output is a human-reviewable, evidence-backed candidate recommendation requiring explicit human authorization.

## V. Prototype Architecture

The prototype uses a scenario dataset, validation scripts, trace JSON artifacts, generated Markdown tables, and article-ready result packages. Each scenario contains the Base vector and score, curated Environmental context, candidate Environmental assessment fields, evidence links, uncertainty flags, human review status, and priority comparison fields.

The current implementation produces the following artifacts:

- `data/article/cvss40_environmental_scenarios.csv`
- `validation/article/cvss40_scenario_metrics.json`
- `validation/article/trace/*.json`
- `article/generated/cvss40_dataset_summary_table.md`
- `article/generated/cvss40_priority_shift_table.md`
- `article/generated/cvss40_traceability_table.md`

## VI. Evaluation Design

### Validation Structure and Separation

The evaluation is structured into two strictly separated tiers: specification-level conformance verification and controlled workflow evaluation across curated scenarios. Specification-level verification evaluates whether the scoring engine adheres to the CVSS v4.0 mathematical standard and maintains formal monotonicity properties under metamorphic relations. Empirical workflow evaluation assesses whether the AI/watcher pipeline successfully structures evidence, flags uncertainty, enforces human authorization requirements as a governance constraint, and exports reproducible artifacts across consumer scenarios.

### Specification-Level Verification Design

To establish a mathematically verified baseline prior to evaluating the operational workflow, the deterministic scoring core was evaluated against the official FIRST reference corpus Round 5, comprising 486,472 vectors evaluated against pinned FIRST commit `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`. In addition, a metamorphic testing campaign evaluated 10,000 executions across four metamorphic relations: MR-1 (monotonicity of criticality), MR-2 (defense removal monotonicity), MR-3 (context permutation invariance), and MR-4 (irrelevant control invariance). Specification-level verification establishes arithmetic conformance to published standards; it does not evaluate contextual suitability or operational effectiveness in production.

#### Formal Specification of Metamorphic Relations

Let $\mathcal{V}$ denote the space of valid CVSS v4.0 Base vectors, $\mathcal{E}$ the space of structured environmental evidence contexts, and $f: \mathcal{V} \times \mathcal{E} \to \mathbb{R} \times \mathcal{M}$ the deterministic evaluation pipeline returning an Environmental score $S(v, e) \in [0.0, 10.0]$ and candidate modified metrics $M(v, e) \in \mathcal{M}$. The campaign (Campaign ID: `HELPUS-METAMORPHIC-10K-G9B`) evaluated 10,000 executions (2,500 per relation) across four formal relations:
1. **MR-1 (Monotonicity of Criticality):** Elevating security requirements $R \in \{\text{CR}, \text{IR}, \text{AR}\}$ ordered $\text{L} < \text{M} < \text{H}$ satisfies $S(v, T_{\text{MR1}}(e)) \ge S(v, e)$. Violation: $S(v, T_{\text{MR1}}(e)) < S(v, e)$.
2. **MR-2 (Defense Removal Monotonicity):** Removing reachability restrictions satisfies $S(v, T_{\text{MR2}}(e_{\text{def}})) \ge S(v, e_{\text{def}})$. Violation: $S(v, T_{\text{MR2}}(e_{\text{def}})) < S(v, e_{\text{def}})$.
3. **MR-3 (Context Permutation Invariance):** Permuting evidence key ordering satisfies $S(v, \pi(e)) = S(v, e) \land M(v, \pi(e)) = M(v, e)$. Violation: $S(v, \pi(e)) \ne S(v, e) \lor M(v, \pi(e)) \ne M(v, e)$.
4. **MR-4 (Irrelevant Control Invariance):** Adding disjoint irrelevant context attributes satisfies $S(v, e \cup I) = S(v, e) \land M(v, e \cup I) = M(v, e)$. Violation: $S(v, e \cup I) \ne S(v, e) \lor M(v, e \cup I) \ne M(v, e)$.

### Empirical Workflow Evaluation Design

This evaluation uses a curated hybrid scenario dataset to assess whether an AI/watcher-assisted workflow can support reproducible CVSS v4.0 Environmental metric assessment. The dataset contains 30 scenarios: 12 scenarios are based on real NVD vulnerability records with CVSS v4.0 data, and 18 scenarios are synthetic curated cases used to preserve controlled variation across asset classes and deployment contexts.

For all scenarios, the official or assigned CVSS v4.0 Base vector and CVSS-B score are stored separately from the AI/watcher Environmental assessment fields. The local Environmental context is curated for article evaluation and includes asset class, deployment context, exposure, privilege assumptions, compensating controls, candidate Security Requirements, candidate Modified Base metric rationale, evidence summaries, uncertainty flags, and human review status.

The evaluation measures workflow properties rather than predictive superiority. The reported metrics are scenario count, evidence coverage, trace completeness, uncertainty flag coverage, explicit human review status, priority shifts between Base-only and Environmental-aware views, and the distribution of curated environment profiles. Watcher outputs are treated as evidence-backed candidate recommendations and not as autonomous official CVSS scores.

### Dataset Summary

| Metric | Value |
|---|---:|
| Scenario count | 30 |
| NVD CVSS v4 rows | 12 |
| Synthetic curated rows | 18 |
| Evidence coverage | 100.0% |
| Trace completeness | 100.0% |
| Uncertainty rate | 100.0% |
| Priority shift count | 22 |
| Priority shift percentage | 73.33% |

## VII. Results

### Specification Conformance and Metamorphic Invariance Results

Specification-level evaluation demonstrated 100.00% arithmetic conformance with the official standard: 486,472 of 486,472 vectors in the FIRST reference corpus Round 5 passed with zero arithmetic divergences against pinned commit `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`. In the metamorphic testing campaign, 10,000 executions completed with zero invariant violations across all four relations (MR-1: 2,500/2,500; MR-2: 2,500/2,500; MR-3: 2,500/2,500; MR-4: 2,500/2,500; campaign ID `HELPUS-METAMORPHIC-10K-G9B`, verdict: PASSED). These results confirm that the underlying scoring core behaves as a deterministic, monotonic, and specification-conformant calculator.

#### Specification-Level Verification Summary

| Evaluation Tier | Evaluated | Conformance / Invariance |
|---|---:|---:|
| FIRST Reference Corpus (Round 5) | 486,472 | 486,472 / 486,472 (0 divergences) |
| Metamorphic MR-1 (Criticality) | 2,500 | 2,500 / 2,500 (0 violations) |
| Metamorphic MR-2 (Defense removal) | 2,500 | 2,500 / 2,500 (0 violations) |
| Metamorphic MR-3 (Permutation) | 2,500 | 2,500 / 2,500 (0 violations) |
| Metamorphic MR-4 (Irrelevant control) | 2,500 | 2,500 / 2,500 (0 violations) |
| Total Metamorphic Campaign | 10,000 | 10,000 / 10,000 (0 violations) |

### Empirical Workflow Results

The generated scenario dataset contains 30 scenarios. Of these, 12 use real NVD CVE records with CVSS v4.0 data and curated local Environmental contexts, while 18 are explicitly marked as curated synthetic scenarios. Evidence coverage reached 100.00%, and trace completeness reached 100.00%, indicating that each scenario contains evidence fields and a corresponding trace artifact.

All 30 scenarios retain an explicit human review requirement flag as an architectural governance constraint, ensuring that AI/watcher output is treated as a candidate recommendation rather than an autonomous official score. This workflow constraint does not represent completed independent expert adjudication. Uncertainty flags are present in 100.00% of scenarios, reflecting intentionally conservative handling of curated local context, threat-state uncertainty, and review requirements.

Priority changed in 22 of 30 scenarios (73.33%) when moving from the Base-only view to the Environmental-aware view. Formally, priorities belong to the ordered set $\mathcal{P} = \langle \text{defer}, \text{low}, \text{medium}, \text{high}, \text{critical} \rangle$ under the ordinal mapping $g: \mathcal{P} \to \{0, 1, 2, 3, 4\}$. The Category Delta is defined as $\Delta_{\text{cat}} = g(P_{\text{env}}) - g(P_{\text{base}})$, with mean $\bar{\Delta}_{\text{cat}} = \frac{1}{30} \sum_{i=1}^{30} \Delta_{\text{cat}}^{(i)} = \frac{6.0}{30} = 0.2$, a maximum upward shift of +2.0 and a maximum downward shift of -3.0. These shifts show that the workflow can operationally differentiate vulnerability handling based on consumer-specific context while preserving the official CVSS v4.0 Base information as a separate baseline.

### Priority Shift Table

| Base priority | Environmental priority | Count |
|---|---|---:|
| critical | critical | 3 |
| high | critical | 4 |
| high | defer | 1 |
| high | high | 2 |
| high | medium | 2 |
| low | defer | 2 |
| low | high | 1 |
| low | low | 1 |
| low | medium | 1 |
| medium | critical | 2 |
| medium | defer | 1 |
| medium | high | 6 |
| medium | low | 2 |
| medium | medium | 2 |

### Controlled Workflow Evaluation on 12 Real NVD CVEs

The controlled workflow evaluation incorporates 12 real CVE records from the National Vulnerability Database (NVD) published with official CVSS v4.0 metrics, paired with curated organizational deployment contexts. The table below details the 12 cases, reporting the official input score and nomenclature (CVSS-B or CVSS-BT), contextual score and nomenclature (CVSS-BE or CVSS-BTE), numeric score delta, and operational priority shift ($\Delta_{\\text{cat}}$). This curated benchmark demonstrates operational workflow sensitivity under realistic vulnerability data rather than an independent sample of operational efficacy. Full 30-metric Base and Environmental vectors for all 12 cases are preserved in the reproducibility trace repository (alidation/article/trace/SCN-NVD-001.json through SCN-NVD-012.json) and data/article/cvss40_environmental_scenarios.csv.

| CVE ID | Input Type | Input Score | Context Type | Context Score | Score $\Delta$ | Priority Shift ($\Delta_{\\text{cat}}$) |
|---|---|---:|---|---:|---:|---|
| CVE-2026-4251 | CVSS-BT | 1.1 | CVSS-BTE | 1.1 | 0.0 | low $\to$ low (0) |
| CVE-2026-4252 | CVSS-BT | 8.9 | CVSS-BTE | 8.8 | -0.1 | high $\to$ medium (-1) |
| CVE-2026-4270 | CVSS-B | 6.8 | CVSS-BE | 6.8 | 0.0 | medium $\to$ high (+1) |
| CVE-2026-28490 | CVSS-B | 8.3 | CVSS-BE | 8.3 | 0.0 | high $\to$ critical (+1) |
| CVE-2026-28498 | CVSS-B | 8.2 | CVSS-BE | 8.1 | -0.1 | high $\to$ high (0) |
| CVE-2026-29510 | CVSS-B | 5.1 | CVSS-BE | 5.1 | 0.0 | medium $\to$ low (-1) |
| CVE-2026-29513 | CVSS-B | 5.1 | CVSS-BE | 5.1 | 0.0 | medium $\to$ medium (0) |
| CVE-2026-29520 | CVSS-B | 5.1 | CVSS-BE | 5.1 | 0.0 | medium $\to$ high (+1) |
| CVE-2026-29521 | CVSS-B | 5.1 | CVSS-BE | 5.1 | 0.0 | medium $\to$ high (+1) |
| CVE-2026-3644 | CVSS-B | 6.0 | CVSS-BE | 5.9 | -0.1 | medium $\to$ low (-1) |
| CVE-2026-4224 | CVSS-B | 6.0 | CVSS-BE | 6.0 | 0.0 | medium $\to$ high (+1) |
| CVE-2026-4253 | CVSS-BT | 2.0 | CVSS-BTE | 2.0 | 0.0 | low $\to$ medium (+1) |

### Traceability Table

| Metric | Value |
|---|---:|
| Rows with evidence | 30 |
| Rows with trace JSON | 30 |
| Rows with uncertainty flags | 30 |
| Rows flagged for review (governance constraint) | 30 |

## VIII. Discussion

The results support the feasibility of using an AI/watcher-assisted workflow to structure Environmental metric assessment around evidence, uncertainty, and reviewability. The workflow does not change the CVSS v4.0 formula and does not claim to produce autonomous official scores. Instead, it separates official Base severity from consumer-side Environmental assessment support.

The hybrid dataset improves over a purely synthetic evaluation by incorporating real NVD CVE records with CVSS v4.0 data. However, because the 30 scenarios were designed to exercise schema coverage, field boundaries, and priority transitions, the evaluation is subject to construction bias (endogenous validation). The observed 100.0% coverage and transitions demonstrate that the workflow schema, ingestion pipeline, and governance gates function as designed across diverse asset profiles; they do not constitute independent empirical proof of predictive superiority, operational accuracy, or real-world risk reduction.

The strongest contribution is traceability: each scenario links the candidate Environmental assessment to evidence summaries, uncertainty flags, review status, and trace JSON. This makes the decision path inspectable and supports reproducibility. The main practical implication is that security teams can use the workflow to make Environmental assessment more explicit and auditable, while keeping final metric selection under human review.

The governance model strictly isolates active operational assets from unexecuted confirmatory protocols. The confirmatory protocol G10B remains explicitly in a `PROTOCOL DEFINED / EXECUTION NOT AUTHORIZED` state. Correspondingly, held-out confirmatory benchmark datasets C1 (real-world cases) and C2 (adversarial/metamorphic cases) remain sealed, unopened, and unexecuted confirmatory datasets under a strict no-retuning constraint governed by a fail-closed execution gatekeeper (`scripts/g10b_confirmatory_gate.py`). They will not be unsealed, inspected, or executed without explicit human authorization constraint and formal gatekeeper release.

Furthermore, independent human expert adjudication has not yet been concluded. The research package includes a pre-registered blinded evaluation protocol (`article/expert_review/`), but claims no completed expert agreement or inter-rater reliability. The empirical results presented in this paper reflect solely the descriptive evaluation of the 30 curated scenarios.

## IX. Limitations and Threats to Validity

This work has several limitations. First, the dataset is curated and partially synthetic. Although part of the dataset uses real NVD CVE records with CVSS v4.0 data, the local Environmental contexts are curated for evaluation and do not represent production deployment measurements.

Second, the workflow does not validate predictive superiority, exploit likelihood, or real-world remediation outcomes. The evaluation measures traceability, evidence coverage, uncertainty handling, review status, and priority shifts, not whether the resulting priorities are objectively superior in production.

Third, the AI/watcher recommendations are not final official CVSS scores. The workflow requires explicit human review status, and final Environmental metric decisions remain analyst responsibility.

Fourth, threat context is treated conservatively. Unless a validated threat-intelligence process is integrated, threat-related fields should be interpreted as contextual evidence requiring review.

Finally, independent expert adjudication has not yet been completed. Future work should compare watcher-assisted recommendations with assessments by multiple security analysts and measure inter-rater agreement, review effort, and decision consistency.

## X. Conclusion

This paper presents an AI/watcher-assisted workflow for supporting CVSS v4.0 Environmental metric assessment through evidence collection, traceability, uncertainty flags, and explicit human review status. The method preserves official CVSS v4.0 semantics and separates specification-level validation (achieving 486,472/486,472 FIRST reference corpus conformance and zero violations across 10,000 metamorphic executions) from controlled workflow evaluation. Across 30 curated hybrid scenarios, the workflow achieved 100.0% evidence and trace coverage and produced operational priority changes in 22 cases under controlled conditions subject to construction bias, while retaining a non-autonomous workflow in which official scoring decisions remain subject to explicit human authorization; independent expert adjudication was not part of this evaluation. Confirmatory protocol G10B remains protocol defined and execution unauthorized, with datasets C1 and C2 sealed. Future work will execute independent expert adjudication under the pre-registered blinded protocol, measure inter-rater agreement, and evaluate the workflow in production-like settings.

## References

[1] FIRST, "Common Vulnerability Scoring System version 4.0." [Online]. Available: https://www.first.org/cvss/v4.0/. Accessed: Jul. 13, 2026.
[2] FIRST, "Common Vulnerability Scoring System version 4.0: Specification Document." [Online]. Available: https://www.first.org/cvss/v4.0/specification-document. Accessed: Jul. 13, 2026.
[3] FIRST, "Common Vulnerability Scoring System version 4.0: User Guide." [Online]. Available: https://www.first.org/cvss/v4.0/user-guide. Accessed: Jul. 13, 2026.
[4] FIRST, "Common Vulnerability Scoring System version 4.0: Implementation Guide." [Online]. Available: https://www.first.org/cvss/v4.0/implementation-guide. Accessed: Jul. 13, 2026.
[5] FIRST, "Common Vulnerability Scoring System version 4.0: Examples." [Online]. Available: https://www.first.org/cvss/v4.0/examples. Accessed: Jul. 13, 2026.
[6] FIRST, "Common Vulnerability Scoring System version 4.0: FAQ." [Online]. Available: https://www.first.org/cvss/v4.0/faq. Accessed: Jul. 13, 2026.
[7] FIRST, "CVSS v4.0 Calculator." [Online]. Available: https://www.first.org/cvss/calculator/4.0. Accessed: Jul. 13, 2026.
[8] FIRST, "CVSS Data Representations." [Online]. Available: https://www.first.org/cvss/data-representations. Accessed: Jul. 13, 2026.
[9] National Institute of Standards and Technology, "National Vulnerability Database API." [Online]. Available: https://nvd.nist.gov/developers/vulnerabilities. Accessed: Jul. 13, 2026.
[10] National Vulnerability Database, "CVE-2026-4251 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-4251. Accessed: Jul. 13, 2026.
[11] National Vulnerability Database, "CVE-2026-4252 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-4252. Accessed: Jul. 13, 2026.
[12] National Vulnerability Database, "CVE-2026-4270 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-4270. Accessed: Jul. 13, 2026.
[13] National Vulnerability Database, "CVE-2026-28490 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-28490. Accessed: Jul. 13, 2026.
[14] National Vulnerability Database, "CVE-2026-28498 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-28498. Accessed: Jul. 13, 2026.
[15] National Vulnerability Database, "CVE-2026-29510 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-29510. Accessed: Jul. 13, 2026.
[16] National Vulnerability Database, "CVE-2026-29513 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-29513. Accessed: Jul. 13, 2026.
[17] National Vulnerability Database, "CVE-2026-29520 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-29520. Accessed: Jul. 13, 2026.
[18] National Vulnerability Database, "CVE-2026-29521 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-29521. Accessed: Jul. 13, 2026.
[19] National Vulnerability Database, "CVE-2026-3644 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-3644. Accessed: Jul. 13, 2026.
[20] National Vulnerability Database, "CVE-2026-4224 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-4224. Accessed: Jul. 13, 2026.
[21] National Vulnerability Database, "CVE-2026-4253 Detail." [Online]. Available: https://nvd.nist.gov/vuln/detail/CVE-2026-4253. Accessed: Jul. 13, 2026.
