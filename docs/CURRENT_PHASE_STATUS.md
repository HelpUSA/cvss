# CVSS current phase status

Updated: 
2026-05-28 13:34:05

## Completed in current phase

- Research sequence and interactive-site order documented.
- Scenario input and pipeline output schemas documented.
- Deterministic environmental scoring engine checkpoint added.
- Pilot and additional curated scenarios added.
- Scenario runner generates before/after comparison and curated summary outputs.
- Automated watcher IA validation queue and outputs regenerated.
- Static dashboard refreshed from generated curated scenario values.
- Static interactive CVSS calculator MVP added to index.html.
- JSON, CSV, and pipeline JSON export path added for the interactive MVP.
- scripts/convert_interactive_export.py converts pipeline JSON into scenario package structure.

## Current public deployment model

The production site should remain a clean static Vercel project from repository root. Do not return to the old Next.js project or npm build path.

## Next checkpoint

1. Verify the clean Vercel static project autodeploys commit 6d6f44a or newer.
2. If production does not show the interactive MVP, redeploy the clean static project from Vercel UI, not the old Next.js project.
3. Add more realistic CVSS vectors and scenario evidence files for each curated scenario.
4. Fold converter, dashboard generation, article input generation, and PDF build into scripts/rebuild_all.ps1.
5. Update article Results and Discussion with multi-scenario totals and interactive MVP scope.

## Scenario evidence enrichment - 
2026-05-28 13:59:31

Added standardized evidence files to each curated scenario: topology.yaml, firewall_rules.yaml, business_impact.yaml, pci_scope.yaml, and expected_expert_labels.yaml. Rebuild wrapper was run to keep generated outputs synchronized.


## Article results and rebuild wrapper checkpoint - 
2026-05-28 14:00:31

Updated scripts/rebuild_all.ps1 to include article PDF build when LaTeX tooling is available. Added article text describing multi-scenario deterministic results and the interactive demonstrator scope.


## Interactive dashboard rebuild fix - 
2026-05-28 14:44:05

Fixed scripts/rebuild_all.ps1 so the generated static dashboard preserves the interactive environmental CVSS calculator section after rebuild. This prevents generated index.html from regressing to the non-interactive dashboard.


## Interactive dashboard rebuild fix - 
2026-05-28 14:44:31

Fixed scripts/rebuild_all.ps1 so the generated static dashboard preserves the interactive environmental CVSS calculator section after rebuild. This prevents generated index.html from regressing to the non-interactive dashboard.


## Production interactive MVP verified - 
2026-05-28 14:58:03

Production at https://cvss.helpusbr.com was visually confirmed to serve the clean static dashboard with the interactive environmental CVSS calculator, Export CSV, and Copy pipeline JSON controls. The clean static Vercel path is now the active production path.


## Engine trace output checkpoint - 
2026-05-28 14:59:01

The deterministic engine now emits per-assessment adjustment traces, and generated comparison CSVs include trace_count, trace_total_adjustment, and trace_json columns for auditability.


## Traceability article update - 
2026-05-28 15:00:01

Verified trace columns in generated scenario outputs and added manuscript text placeholders describing deterministic adjustment traceability.


## Trace report checkpoint - 
2026-05-28 15:01:00

Generated validation/trace/adjustment_trace_report.md and validation/trace/adjustment_trace_summary.csv. The dashboard now includes an adjustment traceability summary section.


## Rebuild and results package verification - 
2026-05-28 15:03:02

Verified results package artifacts and reran the rebuild wrapper. Added docs/REBUILD_REPORT.md summarizing scenarios, findings, assessments, verified commands, verified outputs, and the automated-validation caveat.


## Editorial and test checkpoint - 
2026-05-28 15:06:30

Added synthetic curated scenario policy, inserted synthetic-scenario language into article sections, added initial regression tests, and created docs/TEST_REPORT.md.


## Site report export checkpoint - 
2026-05-28 15:10:49

Added browser-side Markdown report export to the interactive MVP and documented it in docs/SITE_REPORT_EXPORT.md.


## Site report export checkpoint - 
2026-05-28 15:10:49

Added browser-side Markdown report export to the interactive MVP and documented it in docs/SITE_REPORT_EXPORT.md.


## Editorial submission package checkpoint - 
2026-05-28 15:28:35

Created article language audit, generated scenario and traceability result tables, and assembled docs/submission_package with manuscript PDF and core reproducibility summaries.


## Prototype scoring policy checkpoint - 
2026-05-28 15:29:30

Added docs/PROTOTYPE_SCORING_POLICY.md and manuscript language clarifying that the deterministic adjustment constants are a prototype scoring policy, not an official FIRST CVSS environmental formula implementation.


## Final readiness checklist - 
2026-05-28 15:30:06

Added docs/FINAL_READINESS_CHECKLIST.md summarizing ready artifacts, evidence boundaries, and the remaining strategic decision: submit as prototype methodology or implement official CVSS environmental formula comparison first.

