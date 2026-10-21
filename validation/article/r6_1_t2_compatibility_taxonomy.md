# R6.1 Experiment T2 Backward Compatibility Taxonomy (Orthogonal & Complete)

## 1. Specification Status & Governance Metadata
* **Document Version**: 2.1.0
* **Protocol Version**: `R6.1`
* **Status**: `FROZEN_PRIOR_TO_RERUN`
* **Parent Specification Commit**: `090ad8b727e674aac8e95864fe7740b15092ea60`
* **Implementation Freeze Commit**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
* **Protocol Deviation Reference**: `R6-DEV-001` (`POST_RESULT_CHANGE`)
* **Original T2 Experiment Immutability**: `LOCKED_CANONICAL_BASELINE` (`validation/article/r6_t2/*` is immutable)
* **Held-Out Corpus Quarantined**: `True` (`held_out_accessed = false`)
* **Execution State**: `NOT_EXECUTED` (frozen prior to future execution)

---

## 2. Background and Empirical Motivation

During the execution of Experiment T2 under protocol R6-A1 (`CMD-CVSS-IEEE-R6-A1-T2-EXECUTE-239`), the frozen four-category compatibility taxonomy proved structurally incomplete when evaluated against the canonical 30-scenario historical corpus:
* **Schema v1 Baseline**: `30 / 30 PASS` (`100.0%`).
* **Schema v2 Closed-World**: `0 / 30 PASS` (`0.0%`).
* **Observed Failure Modes**:
  - 12 NVD scenarios failed with `INVALID_TYPE` (`compensating_controls` formatted as narrative text rather than a structured object array).
  - 18 Synthetic scenarios failed with `INVALID_ENUM` (`cve_id` formatted as `""` rather than `null` or a validated pattern).
* **Taxonomy Deficiency**: The original taxonomy contained only `V1_VALID_V2_INVALID_UNDECLARED_FIELD`, which coupled any trace valid in v1 and invalid in v2 strictly to undeclared properties (`UNKNOWN_FIELD`). Because none of the 30 rejections were caused by undeclared fields, all 30 inputs were classified as `UNCLASSIFIED_BY_FROZEN_COMPATIBILITY_MODEL`.

Under protocol deviation `R6-DEV-001`, this document establishes an **orthogonal, state-complete classification taxonomy** for protocol `R6.1`.

---

## 3. The R6.1 Orthogonal Compatibility Taxonomy

Rather than proliferating ad-hoc composite categories, R6.1 decouples the **contract state classification** (the primary macro category) from the **diagnostic error reason** (`v2_error_category`).

### 3.1 Primary Compatibility Categories (State-Complete)

The primary category deterministically partitions the complete Cartesian state space $\{v1\_valid\} \times \{v2\_valid\} \times \{normalization\_used\}$:

| Primary Category | Definition | Interpretation & Boundary |
| :--- | :--- | :--- |
| **`V1_VALID_V2_VALID`** | $v_1 = \text{valid} \land v_2 = \text{valid} \land \neg \text{norm}$ | Conforms directly to both Schema v1 (open-world) and Schema v2 (closed-world) contracts without structural transformation. |
| **`V1_VALID_V2_INVALID`** | $v_1 = \text{valid} \land v_2 = \text{invalid} \land \neg \text{norm}$ | Conforms to historical Schema v1, but violates Schema v2 closed-world constraints (e.g., closed typing, strict enums, missing newly required child fields, or undeclared properties). Diagnostic reason is provided independently by `v2_error_category`. |
| **`V1_INVALID_V2_INVALID`** | $v_1 = \text{invalid} \land v_2 = \text{invalid}$ | Violates core syntax or structural constraints in both schema generations (e.g., missing mandatory root fields, malformed JSON). |
| **`V1_VALID_V2_VALID_NORMALIZED`** | $v_1 = \text{valid} \land v_2 = \text{valid} \land \text{norm}$ | Conforms to Schema v1 and achieves Schema v2 validity strictly through a pre-registered, idempotent normalizer without silent semantic coercion. |
| **`V1_INVALID_V2_VALID`** | $v_1 = \text{invalid} \land v_2 = \text{valid}$ | **Documented Anomalous State**: A payload that is invalid under v1 but valid under v2. While generally prohibited in monotonically restrictive evolutions, this state is formally retained in the taxonomy to ensure mathematical state-space completeness and detect unexpected validator regressions. |

---

### 3.2 Orthogonal Diagnostic Dimension (`v2_error_category`)

For any input classified as `V1_VALID_V2_INVALID` or `V1_INVALID_V2_INVALID`, the diagnostic reason is recorded in a separate orthogonal field, `v2_error_category`.

This field is strictly drawn from the predefined error enum established in Section 9 of the frozen `validation/article/r6_schema_v2_specification.md`:
* **`UNKNOWN_FIELD`**: Property not declared in the closed-world object specification (subsumes the previous `UNDECLARED_FIELD` concept).
* **`INVALID_TYPE`**: Property value does not match defined primitive or composite type (e.g., string vs list of objects).
* **`INVALID_ENUM`**: Value violates authorized token enumeration or regex pattern (e.g., malformed CVE ID format).
* **`INVALID_RANGE`**: Numerical score or metric value outside defined boundary $[min, max]$.
* **`MISSING_REQUIRED_FIELD`**: Mandatory property absent from payload.
* **`INVALID_NESTED_OBJECT`**: Malformed child object structure.
* **`RESERVED_FIELD`**: Attempt to inject prohibited architectural keywords (e.g., `delta_audit`).
* **`INVALID_EXTENSION_NAMESPACE`**: Extension property lacking required vendor namespace prefix.

No new error codes are introduced post-hoc.

---

## 4. Anti-Overfitting Safeguards

To prevent post-hoc bias and maintain scientific rigor following the observation of the initial T2 results, the following mandatory safeguards are locked:

1. **Generic Classification**: The category `V1_VALID_V2_INVALID` is completely generic and independent of specific error types such as `INVALID_TYPE` or `INVALID_ENUM`.
2. **Orthogonal Decoupling**: Diagnostic errors are isolated to `v2_error_category`; no combined composite categories (such as `V1_VALID_V2_INVALID_TYPE` or `V1_VALID_V2_INVALID_ENUM`) are permitted.
3. **Zero Case-Specific Logic**: No categorization rule or validator logic may inspect `scenario_id`, `cve_id`, scenario source (`nvd` vs `synthetic`), or target outcome.
4. **No Target Rates**: No expected percentage, pass rate, or target distribution is preregistered for the future rerun.
5. **Denominator Invariance**: The evaluation corpus remains strictly the 30 historical canonical scenarios (`SCN-NVD-001` through `SCN-SYN-030`).
6. **Pre-Rerun Freeze**: This taxonomy is locked and committed to the repository **BEFORE** any rerun is initiated.
7. **Post-Rerun Invariance**: Outcomes observed in future reruns cannot modify this taxonomy without a newly registered, supervisor-approved `POST_RESULT_CHANGE`.

---

## 5. Non-Regression and Architectural Invariants

* **Original T2 Canonical Immutability**: All artifacts in `validation/article/r6_t2/` remain completely unchanged, preserving the 30 unclassified results as empirical evidence of the original protocol.
* **Historical Baseline Invariance**: Mutation Family F3 empirical result ($0/16$ rejections under Schema v1 open-world) remains intact and valid.
* **Scoring Policy Invariance**: Equation 8 nominal formula in `core/cvss40_environmental_policy.py` is unaltered (`Eq8_modified = false`).
* **Prohibition of Delta Audit**: No `delta_audit` or scoring override mechanism is introduced.
* **Quarantine Enforcement**: Held-out corpus remains 100% quarantined (`held_out_accessed = false`).
