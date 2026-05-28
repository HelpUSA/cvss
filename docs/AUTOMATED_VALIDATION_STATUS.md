# Automated validation status

Updated: 
2026-05-28 11:21:31

## Completed

- Automated watcher IA validation policy and workflow documented.
- Validation queue exists for curated scenarios.
- scripts/run_ai_validation_queue.ps1 generates rows, summary, and report artifacts.
- Article status and evaluation sections reference automated watcher IA validation rather than human expert validation.
- Dashboard source contains automated watcher IA validation summary panel.
- Local web build succeeds.

## Active artifacts

- validation/ai_review/outputs/ai_validation_rows.csv
- validation/ai_review/outputs/ai_validation_summary.csv
- validation/ai_review/reports/ai_validation_report.md
- validation/queues/curated_validation_queue.csv
- docs/AUTOMATED_VALIDATION_WORKFLOW.md
- validation/ai_review/ARTIFACT_MANIFEST.md

## Remaining operational issue

Production domain freshness remains the main operational issue if cvss.helpusbr.com does not expose the latest dashboard markers. This is a deploy or alias mapping concern, not a blocker for committed reproducible artifacts.

## Next implementation tasks

1. Expand curated scenario coverage.
2. Regenerate queue and automated IA validation outputs.
3. Improve manuscript tables from validation summaries.
4. Continue Vercel alias or production target diagnosis until production serves latest source.
5. Prepare final article PDF or draft build.

## Scenario expansion scan - 
2026-05-28 11:22:31

Scanned outputs/runs, curated summary, validation queue, and scenario-like folders to determine the next scenario expansion path. Continue by converting any available scenario fixtures into current curated run packages, regenerating outputs/curated_run_summary.csv, rebuilding validation/queues/curated_validation_queue.csv, and rerunning scripts/run_ai_validation_queue.ps1.

