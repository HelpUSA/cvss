---
status: active
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, commit-checklist, validation, article]
---

# CVSS v4.0 article commit checklist

Generated UTC: `2026-07-13T16:53:57.038654+00:00`

## Current validation status

- Scenario validation: expected `CVSS40_SCENARIO_DATASET_VALIDATION_OK`
- Docs validation: expected `CVSS40_DOCS_VALIDATION_OK`
- Phase 5 results validation: expected `CVSS40_PHASE5_ARTICLE_RESULTS_VALIDATION_OK`
- Phase 6 manuscript validation: expected `CVSS40_PHASE6_MANUSCRIPT_VALIDATION_OK`
- `git diff --check`: expected rc=0

## Current dataset status

- Scenario count: 30
- NVD/CVSS v4.0 rows: 12
- Synthetic rows: 18
- Evidence coverage: 100.0%
- Trace completeness: 100.0%
- Priority shift count: 22
- Priority shift percentage: 73.33%

## Files likely intended for commit

Docs:

- `docs/CVSS40_OFFICIAL_READING_NOTES.md`
- `docs/CVSS40_OFFICIAL_SOURCE_SCAN.md`
- `docs/CVSS40_PHASE1_READING_QUEUE.md`
- `docs/ARTICLE_CLAIM_GUARDRAILS_CVSS40.md`
- `docs/ARTICLE_CVSS40_AI_WATCHER_STRATEGY.md`
- `docs/ARTICLE_CVSS40_CONTRIBUTION_MAP.md`
- `docs/ARTICLE_DATASET_SCHEMA.md`
- `docs/ARTICLE_DATASET_PROVENANCE_CVSS40.md`
- `docs/ARTICLE_EVALUATION_RESULTS_CVSS40.md`
- `docs/ARTICLE_EXPERIMENT_DESIGN_CVSS40.md`
- `docs/ARTICLE_IEEE_SKELETON_CVSS40_AI_WATCHER.md`
- `docs/ARTICLE_PHASE3_IMPLEMENTATION_PLAN_CVSS40.md`
- `docs/ARTICLE_PIPELINE_INTEGRATION_AUDIT_CVSS40.md`
- `docs/ARTICLE_ROUTINE_CVSS40_AI_WATCHER.md`
- `docs/CONFERENCE_TARGET_PROFILE.md`

Data and validation:

- `data/article/cvss40_environmental_scenarios.csv`
- `data/article/cvss40_nvd_candidates.csv`
- `validation/article/cvss40_scenario_metrics.json`
- `validation/article/cvss40_scenario_validation_report.md`
- `validation/article/trace/*.json`

Generated article material:

- `article/generated/cvss40_ieee_manuscript_draft.md`
- `article/generated/cvss40_dataset_summary_table.md`
- `article/generated/cvss40_priority_shift_table.md`
- `article/generated/cvss40_traceability_table.md`
- `article/generated/cvss40_evaluation_design_section.md`
- `article/generated/cvss40_results_section.md`
- `article/generated/cvss40_discussion_section.md`
- `article/generated/cvss40_limitations_section.md`

Tools:

- `tools/article_cvss40_phase1_source_scan.py`
- `tools/article_cvss40_phase2_notes_and_map.py`
- `tools/article_cvss40_phase3_pipeline_audit.py`
- `tools/article_cvss40_phase4_seed_dataset.py`
- `tools/article_cvss40_phase4b_nvd_candidates.py`
- `tools/article_cvss40_phase4c_nvd_safe_paged_scan.py`
- `tools/article_cvss40_phase5_generate_results.py`
- `tools/article_cvss40_phase6_integrate_manuscript.py`
- `tools/validate_article_cvss40_docs.py`
- `tools/validate_article_cvss40_scenarios.py`
- `tools/validate_article_phase3_pipeline_audit.py`
- `tools/validate_article_phase5_results.py`
- `tools/validate_article_phase6_manuscript.py`

## Files to review before commit

Backup CSVs were created during dataset promotion attempts. Review whether to commit or exclude:

- `data/article/cvss40_environmental_scenarios.backup.*.csv`

Recommendation: do not commit transient backups unless needed for audit history. Keep one intentional backup only if desired, or move backups outside the repo before commit.

## Safe claim boundary

The paper may claim:

- AI/watcher-assisted Environmental metric assessment.
- Evidence-backed candidate recommendations.
- Human-reviewable workflow.
- Traceability and reproducibility support.
- Hybrid dataset with NVD/CVSS v4.0 rows plus curated Environmental contexts.

The paper must not claim:

- The workflow modifies CVSS v4.0.
- AI autonomously produces official CVSS scores.
- Production validation.
- Predictive superiority.
- Replacement of human analysts.
