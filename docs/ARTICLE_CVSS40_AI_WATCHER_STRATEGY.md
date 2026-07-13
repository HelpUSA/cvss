---
status: active
last_updated: 2026-07-09
owner: "Wagner / CVSS project"
tags: [cvss, cvss-v4, environmental-metrics, ai-watcher, article]
---

# CVSS v4.0 AI/watcher article strategy

## Decision

The article should pivot from a generic contextual CVSS wrapper to an **AI-assisted evidence layer for CVSS v4.0 Environmental metric assessment**.

CVSS v4.0 already defines Base, Threat, Environmental, and Supplemental metric groups. The project should not claim to add official Environmental metrics or modify the official formula. The contribution is operational: helping analysts collect evidence, justify Environmental metric choices, trace uncertainty, and reproduce assessments.

## Revised thesis

Although CVSS v4.0 defines Environmental metrics for adapting vulnerability severity to a consumer's environment, selecting those metrics remains a difficult and evidence-intensive task for human analysts. This paper proposes an AI-assisted watcher workflow that collects, structures, and traces environmental evidence to support reproducible CVSS v4.0 Environmental metric assessment without modifying the official CVSS standard.

## Recommended titles

- Operationalizing CVSS v4.0 Environmental Metrics with AI-Assisted Evidence Collection and Traceability
- A Traceable AI-Assisted Evidence Layer for CVSS v4.0 Environmental Metric Assessment
- AI-Assisted Environmental Metric Assessment for CVSS v4.0 Vulnerability Prioritization

## Contribution boundaries

Allowed:
- AI/watcher assists Environmental metric assessment.
- Official CVSS v4.0 semantics are preserved.
- Outputs are evidence-backed recommendations, not autonomous official scores.
- Evaluation measures evidence coverage, trace completeness, reproducibility, uncertainty flags, and priority shifts.

Not allowed:
- AI replaces analysts.
- The project improves or changes the CVSS formula.
- The watcher produces official scores without review.
- The system is validated in production.
- The method proves predictive superiority.

## Evaluation plan

Use 30 to 50 curated vulnerability scenarios. For each scenario capture: identifier, CVSS Base vector/score, asset exposure, criticality, compensating controls, watcher evidence, suggested Environmental metric choices, uncertainty/human-review flags, Base-only priority, Environmental-aware priority, priority delta, and trace artifact reference.

Metrics: scenario count, evidence coverage, percentage of Environmental decisions linked to evidence, uncertainty flags, number/percentage of priority changes, average/max priority delta, top upward/downward shifts, reproducibility and trace completeness.

## Practical proof artifacts

Use or generate:
- scripts/validate_real_pipeline.py --export-evidence
- outputs/evidence/latest/manifest.json
- validation/trace/adjustment_trace_summary.csv
- validation/trace/adjustment_trace_report.md
- validation/trace/before_after_comparison.csv
- web/src/app
- docs/DEPLOYMENT_VERIFICATION.md

These support reproducibility and traceability, not production validation.

## IEEE/conference posture

Use ICITEICS-2026 as the reference profile, but do not rush that missed deadline. Prepare the next version as an English, IEEE-style, double-blind, 5 to 8 page method/prototype paper for a later venue.
