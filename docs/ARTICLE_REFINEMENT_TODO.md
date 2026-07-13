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


<!-- BEGIN CVSS40_AI_WATCHER_TODO_20260709 -->
## CVSS v4.0 AI/watcher revision tasks

- Rewrite title and abstract around CVSS v4.0 Environmental metric assessment.
- Add background on CVSS v4.0 Base, Threat, Environmental, and Supplemental groups.
- Explain that the prototype does not modify official CVSS semantics or formulas.
- Define the human difficulty of Environmental metric selection: context, evidence, judgment, consistency, and auditability.
- Describe AI/watcher as analyst assistance, not autonomous scoring.
- Build a 30 to 50 scenario evaluation dataset.
- Add fields for evidence links, uncertainty, human-review status, candidate Environmental metric choices, and priority deltas.
- Generate trace artifacts: manifest, adjustment trace summary/report, and before/after comparison.
- Add result metrics: evidence coverage, trace completeness, uncertainty flags, priority shifts, average/max delta.
- Add limitations: no production validation, no human expert adjudication yet, no predictive superiority claim.
- Prepare a double-blind IEEE manuscript for a later conference.
<!-- END CVSS40_AI_WATCHER_TODO_20260709 -->
