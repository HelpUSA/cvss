---
status: draft
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - experiment-design
  - cvss-v4
  - environmental-metrics
  - ai-watcher
  - article
---

# Experiment design for the CVSS v4.0 AI/watcher article

## Goal

Evaluate whether an AI/watcher-assisted workflow can make CVSS v4.0 Environmental metric assessment more traceable, reviewable, and reproducible across curated vulnerability scenarios.

## Dataset

Use 30 to 50 curated scenarios.

Each scenario must include:

- Base CVSS v4.0 information.
- Asset and deployment context.
- Environmental evidence.
- Candidate Environmental metric recommendations.
- Uncertainty flags.
- Human review status.
- Base-only priority.
- Environmental-aware priority.
- Trace artifact reference.

## Evaluation metrics

| Metric | Description |
|---|---|
| Scenario count | Number of scenarios in dataset |
| Evidence coverage | Percentage of scenarios with non-empty evidence |
| Recommendation coverage | Percentage of scenarios with watcher recommendation |
| Trace completeness | Percentage of scenarios with trace artifact reference |
| Review explicitness | Percentage of scenarios with explicit human review status |
| Uncertainty rate | Percentage of scenarios with uncertainty flags |
| Priority shift count | Number of scenarios where Environmental-aware priority differs from Base-only priority |
| Priority shift percentage | Priority shift count divided by scenario count |
| Average priority delta | Mean delta between Base-only and Environmental-aware priority |
| Maximum upward shift | Largest increase in urgency |
| Maximum downward shift | Largest decrease in urgency |

## Interpretation boundaries

These metrics evaluate workflow quality, not predictive superiority. The evaluation can support claims about traceability, reproducibility, and operational differentiation. It cannot support claims about production effectiveness or superiority over CVSS.

## Required output tables for paper

- Dataset overview table.
- Evidence coverage table.
- Priority shift table.
- Trace completeness table.
- Limitation summary table.
