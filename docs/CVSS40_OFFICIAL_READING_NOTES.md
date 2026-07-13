---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - cvss
  - cvss-v4
  - official-reading
  - environmental-metrics
  - ai-watcher
  - article
---

# CVSS v4.0 official reading notes for the AI/watcher article

Generated UTC: `2026-07-10T11:15:05.254114+00:00`

This file is an article working note. It summarizes what must be verified and cited from the official FIRST CVSS v4.0 documentation. It intentionally avoids copying large portions of official documentation.

## Source inventory status

| Source | HTTP status | Title | Text length | Headings | Environmental hits | Threat hits | Supplemental hits | Error |
|---|---:|---|---:|---:|---:|---:|---:|---|
| `main` | 200 | Common Vulnerability Scoring System | 9093 | 2 | 2 | 9 | 2 |  |
| `specification` | 200 | CVSS v4.0 Specification Document | 81342 | 42 | 37 | 44 | 29 |  |
| `user_guide` | 200 | CVSS v4.0 User Guide | 67434 | 51 | 21 | 37 | 13 |  |
| `implementation_guide` | 200 | CVSS v4.0 Consumer Implementation Guide | 65005 | 44 | 48 | 61 | 14 |  |
| `examples` | 200 | CVSS v4.0 Examples | 143693 | 58 | 39 | 64 | 7 |  |
| `faq` | 200 | CVSS v4.0 Frequently Asked Questions | 59282 | 48 | 19 | 41 | 19 |  |
| `calculator` | 200 | Common Vulnerability Scoring System Version 4.0 Calculator | 7403 | 0 | 0 | 5 | 0 |  |
| `data_representations` | 200 | Common Vulnerability Scoring System Data Representations | 18139 | 8 | 17 | 9 | 2 |  |

## Official sources to cite in the manuscript

- FIRST CVSS v4.0 main page: `https://www.first.org/cvss/v4.0/`
- FIRST CVSS v4.0 Specification Document: `https://www.first.org/cvss/v4.0/specification-document`
- FIRST CVSS v4.0 User Guide: `https://www.first.org/cvss/v4.0/user-guide`
- FIRST CVSS v4.0 Implementation Guide: `https://www.first.org/cvss/v4.0/implementation-guide`
- FIRST CVSS v4.0 Examples: `https://www.first.org/cvss/v4.0/examples`
- FIRST CVSS v4.0 FAQ: `https://www.first.org/cvss/v4.0/faq`
- FIRST CVSS v4.0 Calculator: `https://www.first.org/cvss/calculator/4.0`
- FIRST CVSS data representations: `https://www.first.org/cvss/data-representations`

## Article-safe interpretation

CVSS v4.0 already provides a richer structure than a Base-only score. The article should therefore avoid presenting the project as a new scoring standard or as an extension that modifies CVSS. The project should be framed as an operational workflow that helps a consumer organization apply Environmental metric assessment in a more evidence-backed, reviewable, and reproducible way.

## Core official concepts to preserve

### Base metrics

Base metrics represent intrinsic vulnerability characteristics. In the article, Base metrics should be treated as the official severity foundation. The prototype must preserve this information and must not overwrite or relabel it as operational risk.

Article use:

- Store official Base vector and Base score separately.
- Display Base-only priority as a baseline.
- Never claim the system improves the Base score.

### Threat metrics

Threat metrics represent information that may change over time, such as exploit or threat-related context. The watcher may help collect or timestamp threat evidence, but must not be described as authoritative threat intelligence unless a validated threat-intelligence source and process are implemented.

Article use:

- Treat threat evidence as contextual input.
- Record source, timestamp, and uncertainty.
- Flag missing or conflicting evidence.

### Environmental metrics

Environmental metrics represent characteristics relevant to a specific consumer environment. This is the strongest fit for the article because the watcher can help collect local evidence, suggest candidate metric values, and attach justification.

Article use:

- Focus the paper on Environmental metric assessment.
- Treat AI/watcher outputs as candidate recommendations.
- Require `human_review_status` before treating any candidate value as final.
- Preserve traceability between evidence and recommendation.

### Supplemental metrics

Supplemental metrics provide additional context and should not be presented as directly modifying the official final score. The watcher can capture supplemental observations, but these should be reported as supporting context.

Article use:

- Capture supplemental signals as optional context.
- Use them in discussion or operational prioritization, not as a formula change.
- Avoid saying supplemental values change CVSS-BTE directly.

### CVSS-B, CVSS-BT, CVSS-BE, CVSS-BTE

The paper must label scores based on which metric groups are used. This avoids mixing Base-only severity with Threat/Environmental-aware scoring.

Article use:

- Use explicit labels in tables and dashboard output.
- Do not report a score without its vector and metric-group label.
- Compare Base-only versus Environmental-aware assessment clearly.

## Main problem statement

Although CVSS v4.0 defines Environmental metrics for adapting vulnerability severity to a consumer's environment, selecting those metrics remains an evidence-intensive and judgment-dependent task for human analysts. Local asset criticality, deployment context, exposure, compensating controls, and business requirements are often distributed across documentation, configuration, and operational knowledge. This creates difficulty in consistency, auditability, and reproducibility.

## Proposed contribution

The project proposes an AI/watcher-assisted workflow that supports consumer-side Environmental metric assessment by:

1. Collecting local environmental evidence.
2. Structuring evidence into scenario fields.
3. Suggesting candidate Environmental metric values.
4. Linking each suggestion to explicit evidence.
5. Recording uncertainty and missing evidence.
6. Requiring human review status.
7. Exporting traceable CSV, JSON, manifest, and report artifacts.
8. Comparing Base-only and Environmental-aware prioritization.

## Claims allowed

- The prototype preserves official CVSS v4.0 semantics.
- The watcher assists Environmental metric assessment.
- Outputs are evidence-backed candidate recommendations.
- Human review status is explicit.
- The method improves traceability and reproducibility of the assessment workflow.
- The evaluation reports evidence coverage, trace completeness, uncertainty flags, and priority shifts across curated scenarios.

## Claims prohibited

- The system improves CVSS.
- The system changes or extends the official CVSS formula.
- The watcher autonomously produces official CVSS scores.
- AI replaces human analysts.
- The prototype is validated in production.
- The method proves predictive superiority.
- The article introduces new official Environmental metrics.
- Supplemental metrics directly modify the official CVSS-BTE score.

## Manuscript sentence to use

Although CVSS v4.0 defines Environmental metrics for adapting vulnerability severity to a consumer's environment, selecting those metrics remains an evidence-intensive and judgment-dependent task for human analysts. This work proposes an AI/watcher-assisted workflow that collects, structures, and traces environmental evidence to support reproducible CVSS v4.0 Environmental metric assessment without modifying the official CVSS standard.

## Immediate use in the article

Use this document to write:

- Background section.
- Problem statement.
- Contribution list.
- Evaluation boundaries.
- Limitations and threats to validity.
