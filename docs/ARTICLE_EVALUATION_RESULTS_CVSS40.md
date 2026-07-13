---
status: draft
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, article, evaluation, results, environmental-metrics]
---

# CVSS v4.0 AI/watcher article: Evaluation and Results package

Generated UTC: `2026-07-13T16:32:32.078162+00:00`

## Dataset summary

| Metric | Value |
|---|---|
| Scenario count | 30 |
| NVD CVSS v4.0 rows | 12 |
| Synthetic curated rows | 18 |
| Evidence coverage | 100.00% |
| Trace completeness | 100.00% |
| Uncertainty rate | 100.00% |
| Human review required rows | 30 |
| Priority shift count | 22 |
| Priority shift percentage | 73.33% |
| Average priority delta | 0.2 |
| Maximum priority delta | 2.0 |
| Minimum priority delta | -3.0 |

## Dataset source distribution

| Scenario source | Count |
|---|---|
| curated_synthetic_no_cve | 18 |
| nvd_cvss_v4_with_curated_environment | 12 |

## CVSS-B severity distribution

| CVSS-B severity | Count |
|---|---|
| CRITICAL | 3 |
| HIGH | 9 |
| LOW | 5 |
| MEDIUM | 13 |

## Exposure distribution

| Internet exposure | Count |
|---|---|
| internal | 7 |
| isolated | 4 |
| public | 7 |
| restricted | 12 |

## Asset class distribution

| Asset class | Count |
|---|---|
| database_server | 4 |
| developer_workstation | 4 |
| identity_provider | 4 |
| internal_admin_console | 4 |
| isolated_lab_system | 4 |
| ot_monitoring_gateway | 3 |
| public_api_gateway | 3 |
| public_web_application | 4 |

## Priority transition distribution

| Base priority | Environmental-aware priority | Count |
|---|---|---|
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

## NVD/CVSS v4.0 scenario rows

| Scenario | CVE | CVSS-B score | Severity | Base priority | Environmental priority | Delta |
|---|---|---|---|---|---|---|
| SCN-NVD-001 | CVE-2026-4251 | 1.1 | LOW | low | low | 0 |
| SCN-NVD-002 | CVE-2026-4252 | 8.9 | HIGH | high | medium | -1 |
| SCN-NVD-003 | CVE-2026-4270 | 6.8 | MEDIUM | medium | high | 1 |
| SCN-NVD-004 | CVE-2026-28490 | 8.3 | HIGH | high | critical | 1 |
| SCN-NVD-005 | CVE-2026-28498 | 8.2 | HIGH | high | high | 0 |
| SCN-NVD-006 | CVE-2026-29510 | 5.1 | MEDIUM | medium | low | -1 |
| SCN-NVD-007 | CVE-2026-29513 | 5.1 | MEDIUM | medium | medium | 0 |
| SCN-NVD-008 | CVE-2026-29520 | 5.1 | MEDIUM | medium | high | 1 |
| SCN-NVD-009 | CVE-2026-29521 | 5.1 | MEDIUM | medium | high | 1 |
| SCN-NVD-010 | CVE-2026-3644 | 6.0 | MEDIUM | medium | low | -1 |
| SCN-NVD-011 | CVE-2026-4224 | 6.0 | MEDIUM | medium | high | 1 |
| SCN-NVD-012 | CVE-2026-4253 | 2.0 | LOW | low | medium | 1 |

## Draft article text

# Evaluation Design section draft

This evaluation uses a curated hybrid scenario dataset to assess whether an AI/watcher-assisted workflow can support reproducible CVSS v4.0 Environmental metric assessment. The dataset contains 30 scenarios: 12 scenarios are based on real NVD vulnerability records with CVSS v4.0 data, and 18 scenarios are synthetic curated cases used to preserve controlled variation across asset classes and deployment contexts.

For all scenarios, the official or assigned CVSS v4.0 Base vector and CVSS-B score are stored separately from the AI/watcher Environmental assessment fields. The local Environmental context is curated for article evaluation and includes asset class, deployment context, exposure, privilege assumptions, compensating controls, candidate Security Requirements, candidate Modified Base metric rationale, evidence summaries, uncertainty flags, and human review status.

The evaluation measures workflow properties rather than predictive superiority. The reported metrics are scenario count, evidence coverage, trace completeness, uncertainty flag coverage, explicit human review status, priority shifts between Base-only and Environmental-aware views, and the distribution of curated environment profiles. Watcher outputs are treated as evidence-backed candidate recommendations and not as autonomous official CVSS scores.


# Results section draft

The generated scenario dataset contains 30 scenarios. Of these, 12 use real NVD CVE records with CVSS v4.0 data and curated local Environmental contexts, while 18 are explicitly marked as curated synthetic scenarios. Evidence coverage reached 100.00%, and trace completeness reached 100.00%, indicating that each scenario contains evidence fields and a corresponding trace artifact.

All 30 scenarios retain explicit human review status, with 30 marked as requiring review. This is consistent with the paper's boundary that AI/watcher output is a recommendation rather than a final official score. Uncertainty flags are present in 100.00% of scenarios, reflecting intentionally conservative handling of curated local context, threat-state uncertainty, and review requirements.

Priority changed in 22 of 30 scenarios (73.33%) when moving from the Base-only view to the Environmental-aware view. The average priority delta was 0.2, with a maximum upward shift of 2.0 and a maximum downward shift of -3.0. These shifts show that the workflow can operationally differentiate vulnerability handling based on consumer-specific context while preserving the official CVSS v4.0 Base information as a separate baseline.


# Discussion section draft

The results support the feasibility of using an AI/watcher-assisted workflow to structure Environmental metric assessment around evidence, uncertainty, and reviewability. The workflow does not change the CVSS v4.0 formula and does not claim to produce autonomous official scores. Instead, it separates official Base severity from consumer-side Environmental assessment support.

The hybrid dataset improves over a purely synthetic evaluation by incorporating real NVD CVE records with CVSS v4.0 data. However, the Environmental contexts remain curated to evaluate the workflow under controlled assumptions. This design is appropriate for a method/prototype paper, but it should not be presented as evidence of production effectiveness or predictive superiority.

The strongest contribution is traceability: each scenario links the candidate Environmental assessment to evidence summaries, uncertainty flags, review status, and trace JSON. This makes the decision path inspectable and supports reproducibility. The main practical implication is that security teams can use the workflow to make Environmental assessment more explicit and auditable, while keeping final metric selection under human review.


# Limitations section draft

This work has several limitations. First, the dataset is curated and partially synthetic. Although part of the dataset uses real NVD CVE records with CVSS v4.0 data, the local Environmental contexts are curated for evaluation and do not represent production deployment measurements.

Second, the workflow does not validate predictive superiority, exploit likelihood, or real-world remediation outcomes. The evaluation measures traceability, evidence coverage, uncertainty handling, review status, and priority shifts, not whether the resulting priorities are objectively superior in production.

Third, the AI/watcher recommendations are not final official CVSS scores. The workflow requires explicit human review status, and final Environmental metric decisions remain analyst responsibility.

Fourth, threat context is treated conservatively. Unless a validated threat-intelligence process is integrated, threat-related fields should be interpreted as contextual evidence requiring review.

Finally, independent expert adjudication has not yet been completed. Future work should compare watcher-assisted recommendations with assessments by multiple security analysts and measure inter-rater agreement, review effort, and decision consistency.


## Claim boundary

The article may describe the dataset as hybrid because it contains real NVD/CVSS v4.0 rows and curated synthetic rows. It must also state that the consumer Environmental context is curated and that watcher recommendations remain human-reviewable candidates, not autonomous official CVSS scores.
