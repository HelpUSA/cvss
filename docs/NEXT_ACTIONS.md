# CVSS next actions

Updated: 
2026-05-28 11:42:01

## Completed now

- Article PDF build artifact exists at article/main.pdf.
- Automated watcher IA validation artifacts are generated and committed.
- Delivery manifest is present.
- Dashboard source includes automated watcher IA validation panel.
- Public production domain still appears to serve an older dashboard build.

## Recommended next sequence

1. Treat cvss.helpusbr.com freshness as an operational deployment or alias issue.
2. Debug Vercel project binding and domain routing in a dedicated deployment pass.
3. Expand curated scenario coverage after production routing is resolved or in parallel.
4. Regenerate curated summary, validation queue, automated IA rows, and article inputs after each new scenario batch.
5. Keep human expert validation only as future comparative work, not as a project blocker.

## Current stop condition

Core manuscript and reproducibility deliverables are complete. The only unresolved item is public production dashboard freshness.

## Static root deployment reset - 
2026-05-28 12:45:36

Prepared a static root dashboard in index.html and vercel.json to avoid Next.js, npm build, Python serverless, and custom Root Directory behavior. If the old Vercel project continues to use Production Overrides, create a new clean Vercel project from repository root and move cvss.helpusbr.com after verifying the static markers.


## Research sequence and usable site planning - 
2026-05-28 13:08:00

Added docs/RESEARCH_SEQUENCE.md, docs/INTERACTIVE_SITE_PLAN.md, and docs/PIPELINE_ARTIFACT_MAP.md. The fully usable site begins after the research method, input schema, output schema, scoring engine, pilot scenario, scenario expansion, and static research dashboard are stable.


## Scenario runner and dashboard refresh checkpoint

The pilot scenario now has a standardized vulnerabilities.csv, a scenario runner, regenerated before/after comparison output, refreshed curated summary, validation queue, automated IA validation outputs, and a refreshed static dashboard generated from pipeline values. Continue by expanding curated scenarios and completing scripts/rebuild_all.ps1.


## Curated scenario expansion checkpoint

Expanded curated scenarios to include internet_exposed_webapp, internal_erp_segmented, payment_database_zone, and cloud_storage_misconfiguration in addition to the PCI segmented lab pilot. Regenerated scenario outputs, curated summary, validation queue, IA validation outputs, article inputs, and static dashboard.


## Current phase status checkpoint - 
2026-05-28 13:34:05

Added docs/CURRENT_PHASE_STATUS.md summarizing completed research pipeline, static dashboard, interactive MVP, export converter, and the next checkpoint sequence.


## Evidence enrichment checkpoint - 
2026-05-28 13:59:31

Scenario evidence files were generated for all current curated scenarios. Next work: improve scripts/rebuild_all.ps1 to include PDF build and then update article Results and Discussion.


## Production success checkpoint - 
2026-05-28 14:58:03

The public site now serves the interactive static MVP. Next work continues on research depth: richer scenario evidence, stronger engine traceability, full rebuild orchestration, article Results/Discussion refinement, and export-to-scenario workflow hardening.


## Next editorial checkpoint - 
2026-05-28 15:06:30

Next work: refine manuscript prose into a submission-ready narrative, optionally replace synthetic placeholder CVEs with real cited CVEs, and add exportable site reports.


## Interactive MVP deployment checkpoint

Verified the interactive export converter, reran the rebuild wrapper, and attempted a static production deployment. The site now includes the static interactive environmental CVSS calculator and export/conversion path.


## Interactive MVP deployment checkpoint

Verified the interactive export converter, reran the rebuild wrapper, and attempted a static production deployment. The site now includes the static interactive environmental CVSS calculator and export/conversion path.


## Interactive MVP deployment checkpoint

Verified the interactive export converter, reran the rebuild wrapper, and attempted a static production deployment. The site now includes the static interactive environmental CVSS calculator and export/conversion path.


## Interactive MVP deployment checkpoint

Verified the interactive export converter, reran the rebuild wrapper, and attempted a static production deployment. The site now includes the static interactive environmental CVSS calculator and export/conversion path.


## Submission package checkpoint - 
2026-05-28 15:28:35

Next work: inspect article PDF narrative quality, decide whether to keep synthetic CVEs or replace them with real cited CVEs, and strengthen the official-CVSS-vs-prototype-policy explanation.


## Remaining research branch - 
2026-05-28 15:29:30

Optional future branch: implement official CVSS environmental formula support and compare it with the prototype scoring policy. Current submission package can proceed as a prototype methodology article if language remains explicit.


<!-- BEGIN ARTICLE_CVSS40_AI_WATCHER_NEXT_ACTIONS_20260709 -->
## Article next actions: CVSS v4.0 Environmental AI/watcher

1. Update the paper title, abstract, and contribution list to focus on AI-assisted CVSS v4.0 Environmental metric assessment.
2. Design a 30 to 50 scenario dataset.
3. Extend the pipeline/schema to store evidence, uncertainty, human-review status, and candidate Environmental metric recommendations.
4. Generate or refresh trace artifacts:
   - outputs/evidence/latest/manifest.json
   - validation/trace/adjustment_trace_summary.csv
   - validation/trace/adjustment_trace_report.md
   - validation/trace/before_after_comparison.csv
5. Produce quantitative result tables for the article.
6. Rewrite Evaluation, Results, Discussion, and Limitations.
7. Prepare an anonymized IEEE double-blind manuscript package.
8. Search for the next appropriate IEEE/Scopus cybersecurity or intelligent systems conference once the article reaches this level.
<!-- END ARTICLE_CVSS40_AI_WATCHER_NEXT_ACTIONS_20260709 -->

<!-- BEGIN CVSS40_AI_WATCHER_ROUTINE_20260709 -->
## Operational routine for the CVSS v4.0 AI/watcher article

1. Complete official CVSS v4.0 reading notes.
2. Build the contribution map against official CVSS v4.0 concepts.
3. Define the 30 to 50 scenario dataset schema.
4. Generate initial curated scenarios.
5. Extend the pipeline to store evidence, uncertainty, human review status, and candidate Environmental metrics.
6. Export trace artifacts and before/after comparison.
7. Generate quantitative result tables.
8. Rewrite article sections around AI-assisted Environmental metric assessment.
9. Prepare IEEE double-blind manuscript.
10, Search for the next appropriate IEEE or Scopus cybersecurity/intelligent systems conference only after article-grade evidence quality is reached.
<!-- END CVSS40_AI_WATCHER_ROUTINE_20260709 -->

<!-- BEGIN CVSS40_PHASE1_SOURCE_SCAN_NEXT_20260710 -->
## CVSS v4.0 Phase 1 source scan completed

Next actions:

1. Review `docs/CVSS40_OFFICIAL_SOURCE_SCAN.md`.
2. Expand `docs/CVSS40_OFFICIAL_READING_NOTES.md` with verified official definitions.
3. Confirm terminology for Base, Threat, Environmental, Supplemental, CVSS-B, CVSS-BT, CVSS-BE, and CVSS-BTE.
4. Update the contribution map so every watcher capability maps to an official CVSS v4.0 concept.
5. Move to the 30 to 50 scenario dataset design only after the official reading notes are verified.
<!-- END CVSS40_PHASE1_SOURCE_SCAN_NEXT_20260710 -->

<!-- BEGIN CVSS40_PHASE2_NOTES_MAP_NEXT_20260710 -->
## CVSS v4.0 Phase 2 completed

Next actions:

1. Review official reading notes and confirm all statements against FIRST documentation.
2. Start populating `data/article/cvss40_environmental_scenarios.csv` with 30 to 50 scenarios.
3. Add validation for evidence coverage, review status, uncertainty flags, and trace completeness.
4. Generate result tables from the dataset.
5. Rewrite article sections using the safe claim guardrails.
<!-- END CVSS40_PHASE2_NOTES_MAP_NEXT_20260710 -->

<!-- BEGIN CVSS40_PHASE3_PIPELINE_AUDIT_NEXT_20260710 -->
## CVSS v4.0 Phase 3 pipeline audit completed

Next actions:

1. Review `docs/ARTICLE_PIPELINE_INTEGRATION_AUDIT_CVSS40.md`.
2. Start the scenario dataset with 30 to 50 rows.
3. Add a dataset validator for article-grade evidence fields.
4. Generate article result tables from the dataset.
5. Integrate stable outputs into the dashboard only after validation passes.
<!-- END CVSS40_PHASE3_PIPELINE_AUDIT_NEXT_20260710 -->

<!-- BEGIN CVSS40_PHASE4_DATASET_SEED_NEXT_20260710 -->
## CVSS v4.0 Phase 4 dataset seed completed

Next actions:

1. Review `data/article/cvss40_environmental_scenarios.csv`.
2. Review `validation/article/cvss40_scenario_validation_report.md`.
3. Use `python -X utf8 tools/validate_article_cvss40_scenarios.py` after any dataset edit.
4. Improve synthetic or curated local contexts where needed.
5. Generate article-ready result tables and then rewrite Evaluation/Results.
<!-- END CVSS40_PHASE4_DATASET_SEED_NEXT_20260710 -->

<!-- BEGIN CVSS40_PHASE4B_NVD_CANDIDATES_NEXT_20260710 -->
## CVSS v4.0 Phase 4B NVD candidate scan completed

Next actions:

1. Check source counts in `validation/article/cvss40_scenario_metrics.json`.
2. If NVD rows remain zero, keep the article framed as curated-scenario workflow validation.
3. If NVD rows are present, describe the dataset as hybrid: real NVD CVSS v4.0 vulnerability records plus curated consumer Environmental contexts.
4. Continue to article result generation and Evaluation/Results rewrite.
<!-- END CVSS40_PHASE4B_NVD_CANDIDATES_NEXT_20260710 -->

<!-- BEGIN CVSS40_PHASE4C_NVD_SAFE_PAGED_SCAN_NEXT_20260710 -->
## CVSS v4.0 Phase 4C NVD safe paged scan completed

Next actions:

1. Check `validation/article/cvss40_scenario_metrics.json`.
2. If NVD rows are present, describe the dataset as hybrid.
3. If NVD rows remain zero, continue with curated-scenario workflow validation and keep the limitation explicit.
4. Generate article-ready Evaluation and Results text from the current metrics.
<!-- END CVSS40_PHASE4C_NVD_SAFE_PAGED_SCAN_NEXT_20260710 -->

<!-- BEGIN CVSS40_PHASE5_EVALUATION_RESULTS_NEXT_20260713 -->
## CVSS v4.0 Phase 5 Evaluation/Results completed

Next actions:

1. Review `docs/ARTICLE_EVALUATION_RESULTS_CVSS40.md`.
2. Integrate generated Evaluation, Results, Discussion, and Limitations into the IEEE manuscript skeleton.
3. Tighten language to maintain the safe claim boundary.
4. Run full validation.
5. Prepare a commit once docs, dataset, generated tables, and validation scripts are stable.
<!-- END CVSS40_PHASE5_EVALUATION_RESULTS_NEXT_20260713 -->

<!-- BEGIN CVSS40_PHASE6_MANUSCRIPT_NEXT_20260713 -->
## CVSS v4.0 Phase 6 manuscript integration completed

Next actions:

1. Review `article/generated/cvss40_ieee_manuscript_draft.md`.
2. Review `docs/ARTICLE_COMMIT_CHECKLIST_CVSS40.md`.
3. Decide whether to keep or remove transient backup CSV files before commit.
4. Run full validation one more time.
5. Commit the article docs, dataset, generated tables, trace artifacts, and validation scripts.
<!-- END CVSS40_PHASE6_MANUSCRIPT_NEXT_20260713 -->
