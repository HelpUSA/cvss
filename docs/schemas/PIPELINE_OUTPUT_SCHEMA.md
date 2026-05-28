# Pipeline output schema

The pipeline output schema defines how scenario inputs become research results, validation artifacts, article tables, and dashboard content.

## Required outputs

- outputs/runs/<run_id>/before_after_comparison.csv
- outputs/curated_run_summary.csv
- validation/queues/curated_validation_queue.csv
- validation/ai_review/outputs/ai_validation_rows.csv
- validation/ai_review/outputs/ai_validation_summary.csv
- validation/ai_review/reports/ai_validation_report.md
- docs/generated/automated_validation_article_inputs.md
- article/generated/automated_validation_summary_table.txt
- index.html

## before_after_comparison.csv required columns

- case_id
- run_id
- finding_id
- asset_id
- cve
- base_score
- base_severity
- environmental_score
- environmental_severity
- delta
- decision
- rationale

## Research rule

Outputs should be generated from committed scenario inputs and deterministic code whenever possible. Watcher/IA validation should be clearly labeled as automated, not human expert adjudication.
