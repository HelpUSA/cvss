# R6.2 Differential CVSS v4.0 Validation Executive Summary
## Test Suite: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R2`

* **Protocol Version**: R6.2
* **Protocol Deviation**: **`R6-DEV-005`** (`POST_RESULT_CHANGE`)
* **Research Question**: **`RQ-R6-4`**
* **Status**: `COMPLETED_UNFROZEN`
* **Preregistration Commit**: `1bbd1b6b29abd25d5e7dc5b677fee3dae28ec6cb`
* **Runner SHA-256**: `b2b9d925c853f523e52ea661eeac3991eb4290077fa874187759b6871ce7cc82`
* **Deterministic Parity**: **PASS** (100% across Run 1 and Run 2)

---

## 1. Primary Endpoint: Numeric Score Concordance ($D_{numeric} = 461,444$)

| Primary Category | Run 1 Count | Run 1 Rate | Run 2 Count | Run 2 Rate | Concordance Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`EXACT_SCORE_MATCH`** | **454,047** | **98.3970%** | **454,047** | **98.3970%** | **PERFECT REPEATABILITY** |
| `SCORE_MISMATCH` ($|\Delta| = 0.1$) | 7,397 | 1.6030% | 7,397 | 1.6030% | PERFECT REPEATABILITY |
| `VALIDITY_DISAGREEMENT` | 0 | 0.0000% | 0 | 0.0000% | ZERO DISAGREEMENT |
| `EXECUTION_ERROR` | 0 | 0.0000% | 0 | 0.0000% | ZERO ERROR |
| **Total Processed** | **461,444** | **100.0000%** | **461,444** | **100.0000%** | **100% SUM PARITY** |

---

## 2. Secondary Endpoint: Negative Validation Concordance ($D_{validation} = 25,028$)

| Negative Validation Category | Run 1 Count | Run 1 Rate | Run 2 Count | Run 2 Rate | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`SYNTAX_REJECTION_CONCORDANCE`** | **25,028** | **100.0000%** | **25,028** | **100.0000%** | **FULL REJECTION PARITY** |
| `NEGATIVE_VALIDITY_DISAGREEMENT` | 0 | 0.0000% | 0 | 0.0000% | ZERO DISAGREEMENT |
| `NEGATIVE_EXECUTION_ERROR` | 0 | 0.0000% | 0 | 0.0000% | ZERO ERROR |
| **Total Processed** | **25,028** | **100.0000%** | **25,028** | **100.0000%** | **100% SUM PARITY** |

---

## 3. Secondary Diagnostics Summary

### 3.1 FIRST Reference Score Attribution on Score Mismatches ($N = 7,397$)
* **`HELPUS_MATCHES_FIRST_REFERENCE_ONLY`**: **7,397** (100.00%)
* `CVSS4PY_MATCHES_FIRST_REFERENCE_ONLY`: 0 (0.00%)
* `NEITHER_MATCHES_FIRST_REFERENCE`: 0 (0.00%)
* `FIRST_REFERENCE_UNAVAILABLE`: 0 (0.00%)

### 3.2 Derived Qualitative Severity Rating Concordance ($N = 461,444$)
* `SAME_SEVERITY_BAND`: 461,376 (99.9853%)
* `SEVERITY_BOUNDARY_CROSSED`: 68 (0.0147%)

---

## 4. Run Execution Timings & Invariants
* **Run 1 Duration**: 92.01s (5287 rec/s)
* **Run 2 Duration**: 94.31s (5158 rec/s)
* **Held-Out Accessed**: `false` (strictly quarantined)
* **T7 State**: `QUARANTINED_LOCKED`
* **Human Adjudication**: `false` (pending supervisor review)
