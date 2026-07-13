---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags: [cvss-v4, implementation-plan, environmental-metrics, article]
---

# Phase 3 implementation plan: CVSS v4.0 AI/watcher article

## Objective

Move from documentation to executable article evidence without changing official CVSS semantics.

## Step 1 — Scenario dataset

Create 30 to 50 scenarios in:

- `data/article/cvss40_environmental_scenarios.csv`

Every row must include:

- Official or assigned CVSS v4.0 Base vector.
- CVSS-B score and severity.
- Local deployment context.
- Environmental evidence.
- Candidate Environmental metric values.
- Watcher recommendation.
- Uncertainty flags.
- Human review status.
- Base-only and Environmental-aware priority.
- Trace reference.

## Step 2 — Scenario validation

Create a validator that checks:

- Required columns exist.
- Required fields are not empty.
- Controlled values are valid.
- `human_review_status` is explicit.
- Evidence is present.
- Trace reference is present.
- Priority values are valid.
- No row claims autonomous official scoring.

## Step 3 — Article result generation

Generate:

- Dataset summary.
- Evidence coverage.
- Review status summary.
- Uncertainty summary.
- Priority shift summary.
- Trace completeness summary.

Target outputs:

- `validation/article/cvss40_scenario_validation_report.md`
- `validation/article/cvss40_scenario_metrics.json`
- `article/generated/cvss40_dataset_summary_table.md`
- `article/generated/cvss40_priority_shift_table.md`
- `article/generated/cvss40_traceability_table.md`

## Step 4 — Manuscript integration

Use generated outputs to write:

- Evaluation Design.
- Results.
- Discussion.
- Limitations.

## Step 5 — Dashboard/pipeline integration

Only after the dataset and article metrics are stable, connect the new fields to dashboard or existing pipeline outputs.
