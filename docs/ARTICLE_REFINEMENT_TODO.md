# Article refinement TODO

## Results section

- Report number of curated scenarios.
- Report number of findings and automated assessments.
- Report downgraded, unchanged, and upgraded counts.
- Include mean delta by scenario.
- Reference automated watcher IA validation outputs.

## Discussion section

- Explain that the interactive site is a static demonstrator.
- Avoid production-grade claims.
- Keep independent human expert validation as future work.
- Discuss deterministic adjustment policy as an auditable prototype.

## Methods section

- Describe scenario input schema.
- Describe pipeline output schema.
- Describe rebuild_all.ps1 orchestration.
- Describe public dashboard and export-to-scenario workflow.

## Traceability update - 
2026-05-28 15:00:01

Methods and Expected Evaluation should now reference trace_count, trace_total_adjustment, and trace_json in before_after_comparison.csv. The article should describe this as prototype deterministic adjustment traceability.


## Trace report artifact - 
2026-05-28 15:01:00

Use validation/trace/adjustment_trace_summary.csv and validation/trace/adjustment_trace_report.md as article-supporting traceability artifacts.

