# HelpUS CVSS v4.0 Campaign R6-A1 — Protocol Deviations Summary

All methodological deviations from the initial preregistration (`validation/article/r6_a1_preregistration.md`) were formally recorded in `validation/article/r6_a1_protocol_deviation_log.md` prior to continuation.

| Deviation ID | Date UTC | Phase | Type | Description and Resolution |
| :--- | :--- | :--- | :--- | :--- |
| `R6-DEV-001` | 2026-10-21T17:20Z | T2 | `POST_RESULT_CHANGE` | Refined restrictive 4-category taxonomy to orthogonal 5-state model after observing 30/30 legacy traces rejected under strict v2 typing and enum rules. Original T2 frozen; T2R executed. |
| `R6-DEV-002` | 2026-10-21T18:40Z | T4 | `POST_RESULT_CHANGE` | Identified causal confounding in T4 where 30 parents were legacy-invalid; executed versioned rerun R6.1-T4R on 15 canonical parents (N=90) with companion NF2-R (N=15). |
| `R6-DEV-003` | 2026-10-21T19:40Z | T5 | `POST_RESULT_CHANGE` | Diagnosed fixture T5.8 failure as baseline priority injected defect; executed versioned rerun R6.1-T5R (8/8 PASS) while preserving original T5 (7/8) as historical record. |
| `R6-DEV-004` | 2026-10-21T20:44Z | Diff R1 | `PRE_RESULT_CHANGE` | Clarified primary endpoint as exact numeric score concordance and removed comparator serialization requirement prior to observing any experimental output. |
| `R6-DEV-005` | 2026-10-21T22:15Z | Diff R2 | `POST_RESULT_CHANGE` | Decoupled calculable vectors (D_numeric=461,444) from syntax rejection tests (D_validation=25,028); executed corrected protocol R6.2-DIFF-R2. |
