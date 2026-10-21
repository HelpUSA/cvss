# R6.1-T2R vs. Original T2: Detailed Side-by-Side Comparison

## 1. Executive Comparison Overview

This document provides a side-by-side comparative analysis between the original **Experiment T2** (executed under protocol R6-A1, commit `43664e5`) and the rerun **Experiment R6.1-T2R** (executed under protocol R6.1, commit `bfaece2`).

---

## 2. Side-by-Side Results Matrix ($N = 30$)

| Evaluated Dimension | Original T2 Baseline (`validation/article/r6_t2/`) | Rerun R6.1-T2R (`validation/article/r6_1_t2r/`) | Discrepancy / Invariance State |
| :--- | :--- | :--- | :--- |
| **Taxonomy Model** | Restrictive 4-Category Model (Seção 6 Spec v2) | Orthogonal 5-State Complete Model (R6.1) | Structural Model Evolution (`POST_RESULT_CHANGE`) |
| **Total Inputs Evaluated** | `30` (12 NVD + 18 Synthetic) | `30` (12 NVD + 18 Synthetic) | **Identical** ($100\%$ invariant) |
| **Schema v1 Pass Rate** | `30 / 30 PASS` (`100.0%`) | `30 / 30 PASS` (`100.0%`) | **Identical** ($100\%$ invariant) |
| **Schema v2 Pass Rate** | `0 / 30 PASS` (`0.0%`) | `0 / 30 PASS` (`0.0%`) | **Identical** ($100\%$ invariant) |
| **Normalization Used** | `0 / 30` (`false`) | `0 / 30` (`false`) | **Identical** ($100\%$ invariant) |
| **`INVALID_TYPE` Errors** | `12` (`100%` of NVD scenarios) | `12` (`100%` of NVD scenarios) | **Identical** ($100\%$ invariant) |
| **`INVALID_ENUM` Errors** | `18` (`100%` of Synthetic scenarios) | `18` (`100%` of Synthetic scenarios) | **Identical** ($100\%$ invariant) |
| **`UNKNOWN_FIELD` Errors**| `0` (`0.0%`) | `0` (`0.0%`) | **Identical** ($100\%$ invariant) |
| **`V1_VALID_V2_VALID`** | `0` (`0.0%`) | `0` (`0.0%`) | **Identical** |
| **`V1_VALID_V2_INVALID_UNDECLARED_FIELD`** | `0` (`0.0%`) | N/A (Subsumed by orthogonal model) | Deprecated in R6.1 |
| **`V1_VALID_V2_INVALID`** | N/A (Not available in original model) | `30` (`100.0%`) | **Resolved by R6.1 Taxonomy** |
| **`UNCLASSIFIED_BY_MODEL`**| `30` (`100.0%`) | `0` (`0.0%`) | **Resolved by Complete State Space** |
| **Experiment Status** | `EVALUATION_COMPLETED_NEEDS_REVIEW` | `COMPLETED` | Successfully concluded |

---

## 3. Epistemological and Methodological Guarantees

1. **R6.1-T2R Does NOT Retroactively Correct T2**:
   - The original Experiment T2 is not an operational mistake that has been overwritten or erased.
   - The original files in `validation/article/r6_t2/` remain byte-identical on disk, serving as primary evidence of the modeling gap in the initial preregistered protocol.
2. **Validator Evidence Remains Invariant**:
   - The underlying validator core was not touched (`core/r6_schema_v2_validator.py` commit `43664e5`).
   - The exact same errors (`INVALID_TYPE` on flat compensating controls, `INVALID_ENUM` on empty CVE IDs) occurred in both executions.
3. **Transparent Protocol Governance**:
   - The transition between T2 and R6.1-T2R was governed entirely by formal protocol deviation `R6-DEV-001`, classified explicitly as `POST_RESULT_CHANGE`.
   - The new taxonomy was frozen in `bfaece2` before R6.1-T2R was authorized and executed.
