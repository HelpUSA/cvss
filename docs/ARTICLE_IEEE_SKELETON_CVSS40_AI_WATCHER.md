---
status: draft
last_updated: 2026-07-09
owner: "Wagner / CVSS project"
tags: [article, ieee, cvss-v4, ai-watcher]
---

# IEEE paper skeleton: AI-assisted CVSS v4.0 Environmental metric assessment

## Working title

Operationalizing CVSS v4.0 Environmental Metrics with AI-Assisted Evidence Collection and Traceability

## Abstract draft

CVSS v4.0 defines Environmental metrics that allow vulnerability severity to be adapted to a consumer organization's deployment context. However, selecting those metrics remains an evidence-intensive task that depends on local asset criticality, exposure, compensating controls, and analyst judgment. This paper presents an AI-assisted watcher workflow for collecting, structuring, and tracing environmental evidence used to support CVSS v4.0 Environmental metric assessment. The prototype preserves official CVSS v4.0 semantics and treats watcher output as reviewable evidence-backed recommendations rather than autonomous official scoring. We evaluate the approach using curated vulnerability scenarios and report evidence coverage, trace completeness, uncertainty flags, and priority shifts between Base-only and Environmental-aware assessment. The results demonstrate the feasibility of using reproducible artifacts to support human review of Environmental metric choices, while highlighting limitations including curated scenarios and the absence of completed independent expert adjudication.

## Keywords

CVSS v4.0, vulnerability prioritization, environmental metrics, cybersecurity risk, artificial intelligence, traceability, reproducibility.

## Structure

1. Introduction
2. Background: CVSS v4.0 and Environmental Metrics
3. Problem Statement
4. Proposed AI/watcher Workflow
5. Prototype Architecture
6. Evaluation Design
7. Results
8. Discussion
9. Limitations and Threats to Validity
10. Conclusion

## Mandatory limits

- AI/watcher helps structure evidence, not replace analysts.
- CVSS v4.0 semantics are preserved.
- Human review remains required.
- No production validation claim.
- No predictive superiority claim.

<!-- BEGIN CVSS40_PHASE5_GENERATED_EVALUATION_RESULTS_20260713 -->
## Generated Evaluation/Results material

Use the following generated files when expanding the IEEE manuscript:

- `article/generated/cvss40_evaluation_design_section.md`
- `article/generated/cvss40_results_section.md`
- `article/generated/cvss40_discussion_section.md`
- `article/generated/cvss40_limitations_section.md`
- `docs/ARTICLE_EVALUATION_RESULTS_CVSS40.md`
- `docs/ARTICLE_DATASET_PROVENANCE_CVSS40.md`

Current dataset framing: hybrid dataset with real NVD/CVSS v4.0 vulnerability records plus curated consumer Environmental contexts and explicitly marked synthetic scenarios.
<!-- END CVSS40_PHASE5_GENERATED_EVALUATION_RESULTS_20260713 -->
