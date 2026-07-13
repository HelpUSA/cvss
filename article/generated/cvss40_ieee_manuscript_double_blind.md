# Operationalizing CVSS v4.0 Environmental Metrics with AI-Assisted Evidence Collection and Traceability

## Abstract

CVSS v4.0 defines Environmental metrics that allow vulnerability severity to be adapted to a consumer organization's deployment context. However, selecting Environmental metric values remains evidence-intensive because local asset criticality, exposure, compensating controls, and operational requirements are often distributed across multiple sources. This paper presents an AI/watcher-assisted workflow for collecting, structuring, and tracing environmental evidence used to support CVSS v4.0 Environmental metric assessment. The workflow preserves official CVSS v4.0 semantics and treats watcher output as evidence-backed candidate recommendations requiring human review, not as autonomous official scoring. We evaluate the approach using a hybrid dataset of 30 scenarios, including 12 real NVD/CVSS v4.0 vulnerability records and 18 curated synthetic scenarios. The evaluation reports evidence coverage, trace completeness, uncertainty flags, human review status, and priority shifts between Base-only and Environmental-aware views. Results show 100.0% evidence coverage, 100.0% trace completeness, and priority changes in 22 of 30 scenarios, supporting the feasibility of reproducible artifacts for assisting human review of Environmental metric choices.

## Keywords

CVSS v4.0; Environmental metrics; vulnerability prioritization; cybersecurity risk; artificial intelligence; traceability; reproducibility; human review.

## I. Introduction

The Common Vulnerability Scoring System is widely used to communicate vulnerability severity. In practice, however, vulnerability handling decisions often require more than a Base score. A vulnerability affecting an isolated lab asset, an identity provider, a public API gateway, or an operational technology monitoring component may require different remediation urgency even when the Base severity appears similar.

CVSS v4.0 provides a structured distinction between Base, Threat, Environmental, and Supplemental information [1], [2]. This distinction matters because Base metrics describe vulnerability characteristics, while Environmental metrics allow a consumer organization to represent local deployment context [2], [3]. The challenge addressed in this work is therefore operational rather than definitional: selecting Environmental metric values consistently requires evidence, local context, uncertainty handling, and reviewable decision records.

This paper proposes an AI/watcher-assisted workflow for Environmental metric assessment. The workflow collects and structures evidence, suggests candidate Environmental metric values, flags uncertainty, requires human review status, and exports trace artifacts. The contribution is a method and prototype workflow, not a new scoring standard.

## II. Background: CVSS v4.0 and Environmental Metrics

CVSS v4.0 separates vulnerability scoring and contextual information into metric groups including Base, Threat, Environmental, and Supplemental metrics [1], [2]. The workflow in this paper preserves that structure. Base CVSS information is stored separately as the severity baseline. Threat context is treated as time-sensitive evidence requiring review. Environmental assessment support is the main focus because it depends directly on consumer-side deployment context.

The workflow also preserves CVSS-B, CVSS-BT, CVSS-BE, and CVSS-BTE labeling discipline [2], [3]. Any score or priority table should identify which metric groups are represented and should not mix Base-only severity with Environmental-aware prioritization.

## III. Problem Statement

Although CVSS v4.0 defines Environmental metrics, applying them in a real consumer environment remains difficult. Analysts must determine asset importance, exposure, privilege context, compensating controls, confidentiality requirements, integrity requirements, availability requirements, and candidate Modified Base metric values. These inputs may be incomplete, distributed across multiple systems, or inconsistently documented.

This creates three practical problems. First, Environmental decisions may not be reproducible when the evidence trail is missing. Second, analysts may make inconsistent choices across similar assets. Third, remediation prioritization may over-rely on Base severity even when local context should change urgency.

## IV. Proposed AI/Watcher Workflow

The proposed workflow supports the analyst through eight steps: ingest vulnerability and Base CVSS v4.0 information; collect local environmental evidence; structure that evidence into scenario fields; suggest candidate Environmental metric values; attach evidence and rationale to each recommendation; flag uncertainty and missing evidence; require explicit human review status; and export CSV, JSON, report, and table artifacts for reproducibility.

The workflow does not modify the official CVSS v4.0 formula. It also does not present AI output as an autonomous official score. The intended output is a human-reviewable, evidence-backed recommendation.

## V. Prototype Architecture

The prototype uses a scenario dataset, validation scripts, trace JSON artifacts, generated Markdown tables, and article-ready result packages. Each scenario contains the Base vector and score, curated Environmental context, candidate Environmental assessment fields, evidence links, uncertainty flags, human review status, and priority comparison fields.

## VI. Evaluation Design

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

The generated scenario dataset contains 30 scenarios. Of these, 12 use real NVD CVE records with CVSS v4.0 data and curated local Environmental contexts, while 18 are explicitly marked as curated synthetic scenarios. Evidence coverage reached 100.00%, and trace completeness reached 100.00%, indicating that each scenario contains evidence fields and a corresponding trace artifact.

All 30 scenarios retain explicit human review status, with 30 marked as requiring review. This is consistent with the paper's boundary that AI/watcher output is a recommendation rather than a final official score. Uncertainty flags are present in 100.00% of scenarios, reflecting intentionally conservative handling of curated local context, threat-state uncertainty, and review requirements.

Priority changed in 22 of 30 scenarios (73.33%) when moving from the Base-only view to the Environmental-aware view. The average priority delta was 0.2, with a maximum upward shift of 2.0 and a maximum downward shift of -3.0. These shifts show that the workflow can operationally differentiate vulnerability handling based on consumer-specific context while preserving the official CVSS v4.0 Base information as a separate baseline.

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

### Traceability Table

| Metric | Value |
|---|---:|
| Rows with evidence | 30 |
| Rows with trace JSON | 30 |
| Rows with uncertainty flags | 30 |
| Rows requiring review | 30 |

## VIII. Discussion

The results support the feasibility of using an AI/watcher-assisted workflow to structure Environmental metric assessment around evidence, uncertainty, and reviewability. The workflow does not change the CVSS v4.0 formula and does not claim to produce autonomous official scores. Instead, it separates official Base severity from consumer-side Environmental assessment support.

The hybrid dataset improves over a purely synthetic evaluation by incorporating real NVD CVE records with CVSS v4.0 data. However, the Environmental contexts remain curated to evaluate the workflow under controlled assumptions. This design is appropriate for a method/prototype paper, but it should not be presented as evidence of production effectiveness or predictive superiority.

The strongest contribution is traceability: each scenario links the candidate Environmental assessment to evidence summaries, uncertainty flags, review status, and trace JSON. This makes the decision path inspectable and supports reproducibility. The main practical implication is that security teams can use the workflow to make Environmental assessment more explicit and auditable, while keeping final metric selection under human review.

## IX. Limitations and Threats to Validity

This work has several limitations. First, the dataset is curated and partially synthetic. Although part of the dataset uses real NVD CVE records with CVSS v4.0 data, the local Environmental contexts are curated for evaluation and do not represent production deployment measurements.

Second, the workflow does not validate predictive superiority, exploit likelihood, or real-world remediation outcomes. The evaluation measures traceability, evidence coverage, uncertainty handling, review status, and priority shifts, not whether the resulting priorities are objectively superior in production.

Third, the AI/watcher recommendations are not final official CVSS scores. The workflow requires explicit human review status, and final Environmental metric decisions remain analyst responsibility.

Fourth, threat context is treated conservatively. Unless a validated threat-intelligence process is integrated, threat-related fields should be interpreted as contextual evidence requiring review.

Finally, independent expert adjudication has not yet been completed. Future work should compare watcher-assisted recommendations with assessments by multiple security analysts and measure inter-rater agreement, review effort, and decision consistency.

## X. Conclusion

This paper presents an AI/watcher-assisted workflow for supporting CVSS v4.0 Environmental metric assessment through evidence collection, traceability, uncertainty flags, and explicit human review status. The method preserves official CVSS v4.0 semantics and does not modify the standard. The current hybrid dataset demonstrates that the workflow can produce reproducible artifacts and operational priority shifts across curated scenarios. Future work should add independent expert adjudication, measure inter-rater agreement, and evaluate the workflow in production-like settings.

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
