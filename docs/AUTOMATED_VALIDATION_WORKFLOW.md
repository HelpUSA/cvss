# Automated CVSS validation workflow

This document describes the active validation workflow for the project. The workflow is fully automated and watcher IA mediated. It does not require independent human expert action for current progress.

## Active inputs

- validation/queues/curated_validation_queue.csv
- outputs/curated_run_summary.csv
- outputs/runs/<run_id>/before_after_comparison.csv when available
- outputs/runs/<run_id>/scenario evidence files when available

## Main command

powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_ai_validation_queue.ps1

## Active outputs

- validation/ai_review/outputs/ai_validation_rows.csv
- validation/ai_review/outputs/ai_validation_summary.csv
- validation/ai_review/reports/ai_validation_report.md

## Interpretation

The generated rows are automated watcher IA judgments over committed deterministic artifacts. They are suitable for audit, reporting, dashboard display, and manuscript evidence for an automated validation pipeline. They must not be described as independent human expert adjudication.

## Human review status

Human expert review is optional future work. It can later be compared against the watcher IA output, but it is not a dependency of the current project or manuscript pipeline.

## Reproducibility checklist

1. Build or update curated runs.
2. Regenerate validation queue.
3. Run scripts/run_ai_validation_queue.ps1.
4. Verify rows, summary, and report exist.
5. Commit generated artifacts and handoff updates.
