# R6-T6 Execution Plan: Historical NVD Representability Check
## Test Suite: `TEST-SUITE-R6-T6-NVD-REPRESENTABILITY`

* **Status**: `PREREGISTERED_NOT_EXECUTED`
* **Execution Authorization**: `PENDING_FUTURE_SUPERVISOR_ORDER`
* **Parent Contract**: [`validation/article/r6_t6/r6_t6_nvd_representability_contract.json`](file:///D:/AntiG/cvss/validation/article/r6_t6/r6_t6_nvd_representability_contract.json)
* **Case Set**: [`validation/article/r6_t6/r6_t6_nvd_representability_cases.json`](file:///D:/AntiG/cvss/validation/article/r6_t6/r6_t6_nvd_representability_cases.json)
* **Target Modules**:
  * [`core/r6_schema_v2_validator.py`](file:///D:/AntiG/cvss/core/r6_schema_v2_validator.py)
  * [`core/r6_governance_override.py`](file:///D:/AntiG/cvss/core/r6_governance_override.py)
  * [`core/cvss40_environmental_policy.py`](file:///D:/AntiG/cvss/core/cvss40_environmental_policy.py)
* **Held-Out Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`)

---

## 1. Execution Pipeline Overview

When officially authorized and dispatched by supervisor technical order, the execution runner shall execute the following deterministic, offline verification pipeline:

### 1.1 Phase 1: Pre-Execution Guard
1. Verify presence and SHA-256 integrity of the 4 original NVD scenario files in `validation/article/trace/`.
2. Ingest and parse [`validation/article/r6_t6/r6_t6_nvd_representability_cases.json`](file:///D:/AntiG/cvss/validation/article/r6_t6/r6_t6_nvd_representability_cases.json), asserting exactly 4 canonical cases.
3. Verify that Equation 8 nominal calculator `recompute_p_env_nominal` is accessible and unmodified.
4. Verify that access to `validation/article/r6_heldout/*` is completely blocked.

### 1.2 Phase 2: Three-Dimensional Case Evaluation ($N = 4$)
For each case ($T6.1$ through $T6.4$), execute the three verification checks:

1. **Check 1: Schema v2 Direct & Transformative Validation**:
   * Attempt direct validation of original trace against `validate_schema_v2()`.
   * If invalid, test whether deterministic normative structural transformation (wrapping controls into structured items, parsing URI links) yields a valid Schema v2 trace without inventing new attributes.
   * Check whether closed-world enum violations (e.g., `internet_exposure = 'restricted'`) prevent valid representation.

2. **Check 2: Governance Override Encapsulation**:
   * Construct and evaluate a formal `GovernanceOverrideRecord` representing the operational priority deviation.
   * Verify that `evaluate_governance_override()` produces valid audit fields, correct reason code mapping (`CONTROL_COMPENSATION`, `EXPOSURE_CONTEXT_EXCEPTION`), and preserves human authorization requirements.

3. **Check 3: Equation 8 Nominal Formula Invariance**:
   * Execute `recompute_p_env_nominal()` on the case's base priority and asset class.
   * Confirm that nominal calculation is bit-for-bit identical before and after governance pipeline execution, with zero modification to mathematical weights.

### 1.3 Phase 3: Classification Assignment
Assign each case to exactly one mutually exclusive category:
* `REPRESENTABLE_DIRECTLY`
* `REPRESENTABLE_BY_NORMATIVE_STRUCTURAL_TRANSFORMATION`
* `NOT_REPRESENTABLE_WITHOUT_NEW_INFORMATION`
* `REPRESENTABILITY_AMBIGUOUS_UNDER_FROZEN_CONTRACT`

### 1.4 Phase 4: Deterministic Parity Rerun
Re-execute all evaluations in a second independent pass in memory and require 100% bitwise/data-structure match across all recorded classification fields.

### 1.5 Phase 5: Artifact Generation
Emit all outputs into `validation/article/r6_t6/`:
1. `r6_t6_nvd_representability_results.json`
2. `r6_t6_nvd_representability_summary.md`
3. `r6_t6_nvd_representability_case_matrix.md`
4. `SHA256SUMS_RESULTS.txt`

---

## 2. Denominator Accounting & Reporting Isolation

$$\text{Primary Scientific Denominator } (D) = \mathbf{4 \text{ historical NVD cases}}$$
$$\text{Execution Checks Count} = \mathbf{12 \text{ verification checks}}$$

* **No Merging**: T6 representability results measure schema expressiveness and must **never** be aggregated with mutation detection rates ($N=90$, $N=15$) or synthetic contract fixtures ($N=8$).
* **Target Success Rate**: Formally `null` (exploratory study).
* **Expected Success Rate**: Formally `null`.

---

## 3. Strict Scientific Guardrails
* **Held-Out Quarantine**: Zero query, file-open, or reference to `validation/article/r6_heldout/*`.
* **Zero Information Invention**: If a case requires substantive data not present in the original trace, it must be classified as `NOT_REPRESENTABLE_WITHOUT_NEW_INFORMATION`.
* **Formula Immutability**: Equation 8 weights and calculation logic are strictly nominal and invariant.
* **No Premature Execution**: This execution plan is strictly locked until a formal technical order is issued.
