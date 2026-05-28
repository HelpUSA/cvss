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

