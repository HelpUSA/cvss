# CVSS engine traceability plan

The deterministic engine is currently useful as a reproducible checkpoint, but the article needs clearer traceability from input fields to score adjustments.

## Required traceability per assessment

- Base CVSS vector and score.
- Environmental context fields.
- Adjustment factors applied.
- Direction and magnitude of each adjustment.
- Final environmental score and severity.
- Rationale text.
- Source scenario evidence files.

## Next implementation checkpoint

Extend before_after_comparison.csv with adjustment trace columns or a companion JSON file per run. The interactive MVP should expose the same trace and export it in pipeline JSON.

## Research caution

Adjustment constants are deterministic research parameters. They should be described as a prototype scoring policy, not as official FIRST CVSS environmental metric implementation unless the full official formula is implemented and cited.

## Traceability implementation checkpoint - 
2026-05-28 14:59:01

Implemented adjustment trace output in core/cvss_environmental_engine.py and propagated trace_count, trace_total_adjustment, and trace_json into before_after_comparison.csv through scripts/run_curated_scenarios.py.

