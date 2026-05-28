# Automated validation artifact manifest

Generated artifacts used by the current automated watcher IA validation pipeline.

## Workflow

- docs/AUTOMATED_VALIDATION_WORKFLOW.md
- validation/ai_review/README.md
- scripts/run_ai_validation_queue.ps1

## Inputs

- validation/queues/curated_validation_queue.csv
- outputs/curated_run_summary.csv
- outputs/runs/

## Outputs

- validation/ai_review/outputs/ai_validation_rows.csv
- validation/ai_review/outputs/ai_validation_summary.csv
- validation/ai_review/reports/ai_validation_report.md

## Deferred future comparison

- validation/expert_packet/
- validation/comparison_protocol/

Human review is retained only as future comparative work and is not required to run or report the current system.
