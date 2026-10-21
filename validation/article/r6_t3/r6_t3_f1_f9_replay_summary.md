# R6-A1 Experiment T3: Historical Mutation Replay (F1–F9) under Schema v2 Summary

## 1. Executive Summary & Epistemological Boundaries
* **Experiment Identifier**: `R6-T3-F1-F9-REPLAY`
* **Specification Baseline Commit**: `090ad8b727e674aac8e95864fe7740b15092ea60`
* **Implementation Freeze Commit**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
* **Historical Baseline Artifact**: `validation/article/r3_randomized_mutation_testing.json`
* **Total Replayed Mutants**: `120` (exact historical applicable corpus generated under seed `20261021`)
* **Evaluation Status**: `COMPLETED`
* **Held-Out Corpus Quarantined & Untouched**: `True` (`held_out_accessed = false`)

### Scientific Interpretation Boundary & Explicit Non-Claims
1. **Scope of Measurement**: Experiment T3 evaluates the deterministic re-execution of the 120 historical randomized mutants (Families F1–F9) against the frozen closed-world Schema v2 validator implementation.
2. **Explicit Non-Claims**:
   - T3 **is a controlled historical replay**, not a randomized statistical sample of all potential software perturbations.
   - T3 **does not** measure external generalizability to unseen software environments or arbitrary advisory formats.
   - T3 **does not** measure or validate natural language semantic correctness.
   - T3 **does not** measure human expert panel agreement or organizational consensus.
   - T3 **does not** establish real-world Environmental metric ground truth.
   - T3 **does not** imply algorithmic, heuristic, or operational superiority.
   - T3 **does not** constitute mathematical formal verification (it remains runtime structural assertion checking).
3. **Preservation of the Historical R5 Baseline**:
   - The historical R5/R3 empirical result ($83 / 120$ rejected, $37 / 120$ accepted, and Family F3 yielding $0 / 16$ rejections under Schema v1 open-world) remains a permanent, immutable scientific fact.
   - The Schema v2 outcomes are evaluated as **behavior under the new closed-world v2 contract**, and must never be framed as "fixing" or "correcting" an error in historical data.

---

## 2. Quantitative Results & Replay Distribution

### Overall Replay Outcome ($N = 120$)
* **Total Mutants Replayed**: `120`
* **Total Mutants Rejected under Schema v2**: `120` (`100.0%`)
* **Total Mutants Accepted under Schema v2**: `0` (`0.0%`)

### Per-Family Replay Breakdown (F1 through F9)
| Mutation Family | Group | Total Replayed | Historical v1 Rejected (R5) | Historical v1 Accepted (R5) | v2 Replay Rejected | v2 Replay Accepted | Primary v2 Error Categories Observed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`F1_structural_required_field_removal`** | Structural | `16` | `16` ($100\%$) | `0` ($0\%$) | `16` ($100\%$) | `0` ($0\%$) | `MISSING_REQUIRED_FIELD`: 16 |
| **`F2_structural_subobject_removal`** | Structural | `12` | `12` ($100\%$) | `0` ($0\%$) | `12` ($100\%$) | `0` ($0\%$) | `MISSING_REQUIRED_FIELD`: 3, `INVALID_TYPE`: 4, `INVALID_ENUM`: 5 |
| **`F3_structural_subobject_injection`** | Structural | `16` | `0` ($0\%$) | `16` ($100\%$) | `16` ($100\%$) | `0` ($0\%$) | `UNKNOWN_FIELD`: 6, `INVALID_TYPE`: 3, `INVALID_ENUM`: 7 |
| **`F4_structural_type_corruption`** | Structural | `15` | `15` ($100\%$) | `0` ($0\%$) | `15` ($100\%$) | `0` ($0\%$) | `INVALID_TYPE`: 15 |
| **`F5_field_string_truncation`** | Field-level | `13` | `6` ($46.2\%$) | `7` ($53.8\%$) | `13` ($100\%$) | `0` ($0\%$) | `INVALID_TYPE`: 6, `INVALID_ENUM`: 7 |
| **`F6_field_string_random_alteration`** | Field-level | `15` | `3` ($20.0\%$) | `12` ($80.0\%$) | `15` ($100\%$) | `0` ($0\%$) | `INVALID_TYPE`: 7, `INVALID_ENUM`: 8 |
| **`F7_field_numeric_perturbation`** | Field-level | `10` | `10` ($100\%$) | `0` ($0\%$) | `10` ($100\%$) | `0` ($0\%$) | `INVALID_TYPE`: 6, `INVALID_ENUM`: 4 |
| **`F8_field_numeric_swap_or_domain_shift`** | Field-level | `11` | `11` ($100\%$) | `0` ($0\%$) | `11` ($100\%$) | `0` ($0\%$) | `INVALID_TYPE`: 5, `INVALID_ENUM`: 6 |
| **`F9_field_valid_token_flip`** | Field-level | `12` | `10` ($83.3\%$) | `2` ($16.7\%$) | `12` ($100\%$) | `0` ($0\%$) | `INVALID_TYPE`: 7, `INVALID_ENUM`: 5 |
| **Total** | — | **`120`** | **`83`** ($69.2\%$) | **`37`** ($30.8\%$) | **`120`** ($100.0\%$) | **`0`** ($0.0\%$) | — |

---

## 3. Detailed Analysis of Mutation Family F3 (Subobject Injection)

* **Historical Baseline (Schema v1 Open-World)**:
  - Rejected: `0 / 16` (`0.0%`).
  - Accepted: `16 / 16` (`100.0%`).
  - *Context*: Under Schema v1 open-world JSON parsing, extraneous attributes were ignored as long as mandatory fields were present.
* **Observed Replay Behavior under Closed-World Schema v2**:
  - Rejected: `16 / 16` (`100.0%`).
  - Accepted: `0 / 16` (`0.0%`).
  - *Error Diagnostics under Fail-Fast*:
    - `UNKNOWN_FIELD`: `6 cases` (where the injected subobject or property was encountered prior to child type checks).
    - `INVALID_TYPE`: `3 cases` (injected on NVD traces failing on narrative compensating controls).
    - `INVALID_ENUM`: `7 cases` (injected on synthetic traces failing on empty CVE IDs).
* **Scientific Assessment**: Under the closed-world Schema v2 contract, every single F3 mutant is rejected prior to environmental scoring. This validates the core hypothesis of RQ-R6-2: closed-world schemas eliminate open-world attribute injection blind spots.
