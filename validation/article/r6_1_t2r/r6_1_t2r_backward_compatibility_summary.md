# R6.1 Experiment T2R: Backward Compatibility Evaluation Summary

## 1. Executive Summary & Epistemological Boundaries
* **Experiment Identifier**: `R6.1-T2R-BACKWARD-COMPATIBILITY`
* **Protocol Deviation Reference**: `R6-DEV-001` (`POST_RESULT_CHANGE`)
* **Taxonomy Reference Commit**: `bfaece26f9f718672be6b754ad83497ac7f102ea`
* **Specification Baseline Commit**: `090ad8b727e674aac8e95864fe7740b15092ea60`
* **Implementation Freeze Commit**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
* **Source Scope**: Controlled Canonical 30-Scenario Historical Corpus (`SCN-NVD-001`..`012`, `SCN-SYN-013`..`030`)
* **Total Evaluated Inputs**: `30`
* **Evaluation Status**: `COMPLETED`
* **Validation Evidence Parity with Original T2**: `100% MATCH` (`validation_evidence_matches_original_t2 = true`)
* **Held-Out Corpus Quarantined & Untouched**: `True` (`held_out_accessed = false`)

### Scientific Interpretation Boundary & Explicit Non-Claims
1. **Scope of Measurement**: Experiment R6.1-T2R evaluates purely the mapping of historical traces under the orthogonal 5-state compatibility taxonomy defined in R6.1 following protocol deviation `R6-DEV-001`.
2. **Explicit Non-Claims**:
   - R6.1-T2R **does not** measure external generalizability to unseen CVEs.
   - R6.1-T2R **does not** measure or validate natural language semantic correctness.
   - R6.1-T2R **does not** measure expert consensus or human panel agreement.
   - R6.1-T2R **does not** validate real-world Environmental metric ground truth.
   - R6.1-T2R **does not** demonstrate algorithmic or predictive superiority.
   - R6.1-T2R **does not** constitute mathematical formal verification (it remains runtime structural assertion checking).
3. **Historical Invariance**: The historical R5/R3 Mutation Family F3 empirical result ($0/16$ rejections under Schema v1 open-world) remains an immutable baseline and is **not** altered, retroactively erased, or reinterpreted.
4. **Original T2 Canonical Immutability**: The original Experiment T2 artifacts (`validation/article/r6_t2/*`) remain completely unchanged on disk, preserving the 30 unclassified outcomes as primary evidence of the initial protocol taxonomy gap.

---

## 2. Quantitative Results & Category Distribution

### R6.1 Compatibility Category Distribution ($N = 30$)
| Compatibility Category | Observed Count | Percentage |
| :--- | :--- | :--- |
| `V1_VALID_V2_VALID` | `0` | `0.0%` |
| `V1_VALID_V2_INVALID` | `30` | `100.0%` |
| `V1_INVALID_V2_INVALID` | `0` | `0.0%` |
| `V1_VALID_V2_VALID_NORMALIZED` | `0` | `0.0%` |
| `V1_INVALID_V2_VALID` (Anomalous) | `0` | `0.0%` |

### Independent Schema Validation Rates
* **Schema v1 Baseline Validator**: `30 / 30 PASS` (`100.0%`)
* **Schema v2 Closed-World Validator**: `0 / 30 PASS` (`0.0%`)
* **Normalization Applied**: `0` (`normalization_used = false` across all inputs)

### Orthogonal Diagnostic Breakdown (`v2_error_category`)
The diagnostic causes for the 30 `V1_VALID_V2_INVALID` outcomes are recorded orthogonally without altering the primary category label:
* **`INVALID_TYPE`**: `12 cases` (`100.0%` of NVD scenarios: `SCN-NVD-001` through `SCN-NVD-012`).
  - *Cause*: `compensating_controls` is stored as a flat narrative string (`str`) in historical traces, whereas Schema v2 strictly requires an array of structured objects (`list[CompensatingControlItem]`).
* **`INVALID_ENUM`**: `18 cases` (`100.0%` of Synthetic scenarios: `SCN-SYN-013` through `SCN-SYN-030`).
  - *Cause*: `cve_id` is stored as an empty string `""` in synthetic fixtures, whereas Schema v2 expects either `null` or a string strictly matching pattern `^CVE-\d{4}-\d{4,}$`.

---

## 3. Methodological Reproducibility & Integrity

* **Zero Discrepancy with Underlying Validator**: The underlying validator outputs (`v1_valid`, `v2_valid`, `v2_error_category`) were 100% identical between the original T2 run and R6.1-T2R.
* **Pure Taxonomic Resolution**: The transition from 30 unclassified cases in T2 to 30 `V1_VALID_V2_INVALID` cases in R6.1-T2R is solely a function of the improved, state-complete taxonomic model, which eliminated the false coupling between `v1-valid / v2-invalid` and `UNDECLARED_FIELD`.
* **Zero Post-Hoc Data Tampering**: No historical trace was rewritten or coerced.
