---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags: [cvss-v4, pipeline-audit, environmental-metrics, ai-watcher, article]
---

# Article pipeline integration audit

Generated UTC: `2026-07-10T11:33:21.155486+00:00`

## Purpose

This audit identifies where the repository already contains CVSS, evidence, trace, dashboard, validation, and prioritization logic, so the CVSS v4.0 Environmental Metrics article work can be integrated without guessing.

## Dataset status

| Item | Value |
| --- | --- |
| Dataset path | data/article/cvss40_environmental_scenarios.csv |
| Exists | True |
| Rows | 0 |
| Columns | 27 |
| Missing required columns | none |

## Relevant file categories

| Category | Relevant files |
| --- | ---: |
| article | 12 |
| dashboard | 4 |
| dataset | 1 |
| docs | 86 |
| evidence-output | 5 |
| pipeline/script | 5 |
| validation | 7 |

## Top relevant files

| Rank | File | Category | Score | Size |
| ---: | --- | --- | ---: | ---: |
| 1 | docs/ARTICLE_PIPELINE_INTEGRATION_AUDIT_CVSS40.md | docs | 314 | 9474 |
| 2 | docs/CVSS40_OFFICIAL_SOURCE_SCAN.md | docs | 267 | 14611 |
| 3 | docs/CVSS40_OFFICIAL_READING_NOTES.md | docs | 207 | 7435 |
| 4 | docs/NEXT_ACTIONS.md | docs | 188 | 8637 |
| 5 | docs/ARTICLE_CVSS40_AI_WATCHER_STRATEGY.md | docs | 145 | 3271 |
| 6 | docs/ARTICLE_STATUS.md | docs | 143 | 10483 |
| 7 | docs/CURRENT_HANDOFF.md | docs | 127 | 13968 |
| 8 | docs/CURRENT_PHASE_STATUS.md | docs | 102 | 5407 |
| 9 | docs/ARTICLE_CVSS40_CONTRIBUTION_MAP.md | docs | 99 | 3153 |
| 10 | docs/09_Paper_or_Article.md | docs | 98 | 3155 |
| 11 | docs/ARTICLE_EXPERIMENT_DESIGN_CVSS40.md | docs | 93 | 2114 |
| 12 | docs/ARTICLE_ROUTINE_CVSS40_AI_WATCHER.md | docs | 93 | 3057 |
| 13 | docs/00_Index.md | docs | 89 | 3172 |
| 14 | docs/ARTICLE_DATASET_SCHEMA.md | docs | 86 | 2886 |
| 15 | docs/reorg_report_20260517_133208.json | docs | 85 | 4019 |
| 16 | docs/ARTICLE_LANGUAGE_AUDIT.md | docs | 84 | 4384 |
| 17 | docs/EXPERIMENTAL_RUNS.md | docs | 84 | 9073 |
| 18 | docs/REAL_SCAN_RUNBOOK.md | docs | 81 | 6657 |
| 19 | article/sections/03_related_work_and_gap.tex | article | 78 | 3443 |
| 20 | docs/ARTICLE_REFINEMENT_TODO.md | docs | 78 | 2330 |
| 21 | docs/ARTICLE_PHASE3_IMPLEMENTATION_PLAN_CVSS40.md | docs | 73 | 1877 |
| 22 | docs/ARTICLE_IEEE_SKELETON_CVSS40_AI_WATCHER.md | docs | 65 | 2076 |
| 23 | docs/ARTICLE_PLAN_PT.md | docs | 63 | 2416 |
| 24 | docs/ROADMAP.md | docs | 62 | 7800 |
| 25 | article/sections/07_expected_evaluation.tex | article | 61 | 7082 |
| 26 | docs/BROADER_STUDY_PROTOCOL.md | docs | 60 | 5215 |
| 27 | docs/ARTICLE_CLAIM_GUARDRAILS_CVSS40.md | docs | 56 | 2077 |
| 28 | docs/PUBLIC_CONTRACT_VALIDATION_STATUS.md | docs | 56 | 1551 |
| 29 | docs/CVSS40_PHASE1_READING_QUEUE.md | docs | 48 | 1712 |
| 30 | docs/checklists/real-evidence-refresh.md | docs | 46 | 3954 |
| 31 | docs/DEPLOYMENT_VERIFICATION.md | docs | 45 | 3918 |
| 32 | docs/ENGINE_TRACEABILITY_PLAN.md | docs | 44 | 1254 |
| 33 | scripts/run_curated_scenarios.py | pipeline/script | 43 | 2229 |
| 34 | validation/ai_review/outputs/ai_validation_rows.csv | validation | 43 | 3286 |
| 35 | docs/real_world/OFFICIAL_CONTEXTUAL_INTEGRATION.md | docs | 42 | 1092 |
| 36 | docs/02_Architecture.md | docs | 41 | 1273 |
| 37 | docs/PIPELINE_ARTIFACT_MAP.md | docs | 40 | 2785 |
| 38 | docs/real_world/REAL_WORLD_PHASE_STATUS.md | docs | 39 | 1511 |
| 39 | docs/05_Real_World_Wrapper.md | docs | 38 | 1622 |
| 40 | article/sections/02_background.tex | article | 36 | 1227 |
| 41 | docs/REAL_ENVIRONMENT_AUTOMATION_PLAN.md | docs | 36 | 3871 |
| 42 | docs/real_world/REAL_WORLD_IMPLEMENTATION_PLAN.md | docs | 36 | 2589 |
| 43 | docs/status/2026-07-08-cvss-real-evidence-export-validation.md | docs | 36 | 1751 |
| 44 | docs/decisions/ADR-001-official-vs-contextual-separation.md | docs | 35 | 1168 |
| 45 | docs/07_Testing_and_Validation.md | docs | 34 | 1478 |
| 46 | docs/CLOUD_DEPLOYMENT.md | docs | 34 | 2335 |
| 47 | docs/RESEARCH_SEQUENCE.md | docs | 34 | 2540 |
| 48 | scripts/export_real_evidence.py | pipeline/script | 33 | 5072 |
| 49 | data/article/cvss40_environmental_scenarios.csv | dataset | 32 | 494 |
| 50 | article/main.tex | article | 31 | 2088 |
| 51 | web/src/app/DashboardClient.tsx | dashboard | 31 | 10173 |
| 52 | docs/releases/2026-07-06-real-pipeline.md | docs | 30 | 3192 |
| 53 | docs/01_Project_Overview.md | docs | 28 | 1348 |
| 54 | docs/04_Contextual_Engine.md | docs | 28 | 1149 |
| 55 | docs/status/2026-07-07-cvss-real-pipeline-evidence-export.md | docs | 28 | 1054 |
| 56 | docs/06_Data_Model.md | docs | 27 | 1097 |
| 57 | docs/ARCHITECTURE.md | docs | 27 | 1964 |
| 58 | docs/real_world/OFFICIAL_CVSS_INTEGRATION_DESIGN.md | docs | 26 | 1088 |
| 59 | article/sections/08_threats_to_validity.tex | article | 25 | 1570 |
| 60 | article/sections/09_conclusion.tex | article | 25 | 1374 |
| 61 | docs/03_CVSS_Official_Core.md | docs | 25 | 1004 |
| 62 | docs/REVIEWER_ASSESSMENT_FORM.md | docs | 25 | 1439 |
| 63 | docs/status/2026-07-08-cvss-real-evidence-export-pr-note.md | docs | 25 | 1303 |
| 64 | docs/INTERACTIVE_SITE_PLAN.md | docs | 24 | 2185 |
| 65 | docs/08_Dashboard_and_Exports.md | docs | 23 | 994 |
| 66 | validation/trace/adjustment_trace_report.md | validation | 23 | 533 |
| 67 | article/sections/01_introduction.tex | article | 22 | 1616 |
| 68 | docs/FINAL_READINESS_CHECKLIST.md | docs | 22 | 1016 |
| 69 | docs/README.md | docs | 22 | 939 |
| 70 | docs/submission_package/README.md | docs | 21 | 917 |
| 71 | article/sections/04_ai_bridge_approach.tex | article | 20 | 1461 |
| 72 | docs/PROTOTYPE_SCORING_POLICY.md | docs | 20 | 1257 |
| 73 | docs/AUTOMATED_VALIDATION_STATUS.md | docs | 18 | 2757 |
| 74 | validation/comparison_protocol/README.md | validation | 18 | 1476 |
| 75 | validation/expert_packet/README.md | validation | 18 | 1171 |
| 76 | article/sections/05_case_study_design.tex | article | 16 | 1507 |
| 77 | docs/10_Changelog.md | docs | 16 | 987 |
| 78 | docs/real_world/CVSS31_CORE_COMPATIBILITY.md | docs | 16 | 464 |
| 79 | docs/ARTICLE_REBOOT_PLAN.md | docs | 15 | 1180 |
| 80 | docs/CONFERENCE_TARGET_PROFILE.md | docs | 14 | 1651 |

## Required field implementation visibility

| Field | Mentioned in implementation files? |
| --- | --- |
| scenario_id | data/article/cvss40_environmental_scenarios.csv |
| cve_id | data/article/cvss40_environmental_scenarios.csv |
| vulnerability_summary | data/article/cvss40_environmental_scenarios.csv |
| official_cvss_v4_vector | data/article/cvss40_environmental_scenarios.csv |
| cvss_b_score | data/article/cvss40_environmental_scenarios.csv |
| cvss_b_severity | data/article/cvss40_environmental_scenarios.csv |
| asset_class | data/article/cvss40_environmental_scenarios.csv |
| deployment_context | data/article/cvss40_environmental_scenarios.csv |
| internet_exposure | data/article/cvss40_environmental_scenarios.csv |
| privilege_context | data/article/cvss40_environmental_scenarios.csv |
| compensating_controls | scripts/run_curated_scenarios.py, data/article/cvss40_environmental_scenarios.csv, scripts/convert_interactive_export.py, scripts/run_engine_smoke.py |
| confidentiality_requirement | data/article/cvss40_environmental_scenarios.csv |
| integrity_requirement | data/article/cvss40_environmental_scenarios.csv |
| availability_requirement | data/article/cvss40_environmental_scenarios.csv |
| candidate_modified_metrics | data/article/cvss40_environmental_scenarios.csv |
| threat_context | data/article/cvss40_environmental_scenarios.csv |
| supplemental_context | data/article/cvss40_environmental_scenarios.csv |
| evidence_links | data/article/cvss40_environmental_scenarios.csv |
| evidence_summary | data/article/cvss40_environmental_scenarios.csv |
| watcher_recommendation | data/article/cvss40_environmental_scenarios.csv |
| uncertainty_flags | data/article/cvss40_environmental_scenarios.csv |
| review_required | data/article/cvss40_environmental_scenarios.csv |
| human_review_status | data/article/cvss40_environmental_scenarios.csv |
| base_priority | data/article/cvss40_environmental_scenarios.csv |
| environmental_priority | data/article/cvss40_environmental_scenarios.csv |
| priority_delta | data/article/cvss40_environmental_scenarios.csv |
| trace_json | scripts/run_curated_scenarios.py, data/article/cvss40_environmental_scenarios.csv |

## Integration gaps

- The dataset currently exists as a schema/header seed unless rows have been added.
- New CVSS v4.0 Environmental assessment fields must remain separated from official CVSS Base fields.
- The pipeline should not treat watcher recommendations as final scores without explicit `human_review_status`.
- Result tables for the article still need to be generated from the scenario dataset.
- Trace artifacts should connect each recommendation to evidence, uncertainty, and review status.

## Recommended implementation order

1. Keep this audit as the current integration map.
2. Populate 30 to 50 curated scenarios in `data/article/cvss40_environmental_scenarios.csv`.
3. Add a scenario validator that checks required fields, controlled values, evidence coverage, review status, and trace references.
4. Add result generation for article tables.
5. Only after dataset validation, connect outputs to dashboard or existing pipeline modules.

## Important boundary

This audit does not prove CVSS v4.0 formula implementation. It only maps repository integration points for the article workflow.
