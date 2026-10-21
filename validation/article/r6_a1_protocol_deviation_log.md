# R6-A1 Protocol Deviation Log

**Initial Status**: `LOGGED_DEVIATIONS_PRESENT`
**Preregistration Base Commit**: `e5215b525c90696043b1d68ea5bf4ce4c88f2d41`
**Branch**: `research/r6-a1-schema-governance-implementation`
**Last Updated**: 2026-10-21T17:20:00Z

---

## 1. Governance Rules for Methodological Deviations

1. **Mandatory Logging**: Any alteration, refinement, or exception to the locked protocols established in `validation/article/r6_a1_preregistration.md` must be formally recorded in this log **BEFORE** continuing any experimental execution or code implementation.
2. **Strict Falsification Principle**:
   > **Any unlogged post-result methodological change invalidates the affected R6 claim until independently reviewed.**
3. **Classification of Changes**:
   - `PRE_RESULT_CHANGE`: Modification designed and committed prior to observing any output, trace, or validation result on the affected dataset.
   - `POST_RESULT_CHANGE`: Modification made after observing preliminary, partial, or full experimental outcomes. Any post-result change requires declaring an `R6.1+` iteration and preserving original unpatched results in the manuscript.

---

## 2. Template for Future Deviation Entries

When logging an unavoidable protocol adjustment, append an entry using the following standard template:

```markdown
### Deviation ID: DEV-R6-[YEAR][MONTH][DAY]-[SEQ]
- **Timestamp UTC**: YYYY-MM-DDTHH:MM:SSZ
- **Requested by**: [Name / Role]
- **Phase**: [R6-0 to R6-7]
- **Original preregistered rule**: [Exact quote or reference to preregistration section]
- **Proposed change**: [Precise specification of change]
- **Rationale**: [Objective technical necessity justifying the deviation]
- **Files affected**: [List of paths]
- **RQ/Hypothesis affected**: [RQ-R6-1, RQ-R6-2, RQ-R6-3, or RQ-R6-4]
- **Had any relevant results already been observed?**: YES / NO
- **Classification**: PRE_RESULT_CHANGE / POST_RESULT_CHANGE
- **Potential bias introduced**: [Explicit characterization of possible threat to validity]
- **Corrective action**: [Safeguards enacted to prevent data snooping or over-fitting]
- **Whether a new protocol version (R6.1+) is required**: YES / NO
- **Approval state**: PENDING / APPROVED_BY_SUPERVISOR / REJECTED
```

---

## 3. Deviation Record Table

| Deviation ID | Date UTC | Phase | RQ Affected | Classification | Approval State | Summary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `R6-DEV-001` | 2026-10-21T17:20:00Z | R6-A1 | RQ-R6-1, RQ-R6-2 | `POST_RESULT_CHANGE` | `APPROVED_BY_SUPERVISOR` | Generalization of T2 compatibility taxonomy from restrictive 4-category model to complete 5-state orthogonal model after observing 30/30 unclassified cases due to legitimate closed-world type and enum constraints. |

---

## 4. Logged Protocol Deviations

### Deviation ID: R6-DEV-001
- **Timestamp UTC**: 2026-10-21T17:20:00Z
- **Requested by**: AI Bridge Supervisor & HelpUS Research Team (`helpusdev@helpus.ai`)
- **Phase**: R6-A1 (Experiment T2 Backward Compatibility Evaluation)
- **Original preregistered rule**: Section 6 of `validation/article/r6_schema_v2_specification.md` defined a restrictive four-category taxonomy (`V1_VALID_V2_VALID`, `V1_VALID_V2_INVALID_UNDECLARED_FIELD`, `V1_INVALID_V2_INVALID`, `V1_VALID_V2_VALID_NORMALIZED`), coupling all `v1-valid / v2-invalid` outcomes exclusively to undeclared properties (`UNKNOWN_FIELD`).
- **Trigger**: The canonical deterministic execution of Experiment T2 (`CMD-CVSS-IEEE-R6-A1-T2-EXECUTE-239`) observed 30/30 inputs classified as `UNCLASSIFIED_BY_FROZEN_COMPATIBILITY_MODEL`. All 30 historical traces were valid under Schema v1 (`30/30 PASS`), but invalid under Schema v2 (`0/30 PASS`) due to legitimate closed-world constraints:
  - 12 NVD cases failed with `INVALID_TYPE` (`compensating_controls` is string narrative instead of array of structured objects);
  - 18 Synthetic cases failed with `INVALID_ENUM` (`cve_id` is empty string `""` instead of `null` or `^CVE-\d{4}-\d{4,}$`).
  Neither of these failure modes involved undeclared fields (`UNKNOWN_FIELD = 0`).
- **Proposed change**: Refine and freeze the compatibility taxonomy for protocol version `R6.1` by introducing an orthogonal, complete state-space model:
  - Primary compatibility categories:
    1. `V1_VALID_V2_VALID`
    2. `V1_VALID_V2_INVALID`
    3. `V1_INVALID_V2_INVALID`
    4. `V1_VALID_V2_VALID_NORMALIZED`
    5. `V1_INVALID_V2_VALID` (documented as anomalous/expansion state)
  - Diagnostic reason is captured orthogonally via `v2_error_category` using the existing frozen error enum from Section 9 of the specification (`UNKNOWN_FIELD`, `INVALID_TYPE`, `INVALID_ENUM`, `INVALID_RANGE`, `MISSING_REQUIRED_FIELD`, `RESERVED_FIELD`).
- **Rationale**: The original taxonomy contained a modeling gap by conflating the generic state `v1_valid && !v2_valid` with the specific error `UNKNOWN_FIELD`. An orthogonal model covers the full Boolean product $\{v1\_valid\} \times \{v2\_valid\}$ without ad-hoc category proliferation.
- **Files affected**:
  - `validation/article/r6_a1_protocol_deviation_log.md` (this record)
  - `validation/article/r6_1_t2_compatibility_taxonomy.md` (new specification for R6.1)
  - `validation/article/r6_1_t2_compatibility_contract.json` (new contract for R6.1)
  - `validation/article/r6_1_t2_rerun_plan.md` (rerun plan for R6.1-T2R)
  - `validation/article/r6_a1_experiment_registry.json` (governance status metadata update)
- **RQ/Hypothesis affected**: RQ-R6-1, RQ-R6-2
- **Had any relevant results already been observed?**: YES (Canonical T2 run observed 30/30 unclassified inputs).
- **Classification**: `POST_RESULT_CHANGE`
- **Potential bias introduced**: Post-hoc adjustment of evaluation taxonomy after observing experimental data.
- **Corrective action & Anti-Overfitting Safeguards**:
  1. **Original T2 Immutability**: Original T2 artifacts (`validation/article/r6_t2/r6_t2_backward_compatibility_results.json`, `r6_t2_backward_compatibility_summary.md`, `SHA256SUMS.txt`) remain byte-for-byte immutable and archived as canonical evidence of the frozen R6 protocol.
  2. **No Retroactive Reinterpretation**: No historical T2 file is modified or overwritten.
  3. **No Tailored Categories**: Categories are generic (`V1_VALID_V2_INVALID`) and do not mention specific fields, error types, or scenario subsets (no `V1_VALID_V2_INVALID_TYPE` category created).
  4. **Diagnostic Orthogonality**: The error diagnostic dimension utilizes the pre-existing, preregistered `SchemaErrorCategory` enum from Section 9 of `r6_schema_v2_specification.md`.
  5. **Denominator Invariance**: The evaluation denominator remains identical ($N = 30$ historical traces).
  6. **No Target Rates**: No target rate or expected distribution is preregistered for R6.1-T2R.
  7. **Quarantine Isolation**: Held-out corpus remains strictly quarantined (`held_out_accessed = false`).
  8. **Core Invariance**: Nominal Equation 8 formula in `core/cvss40_environmental_policy.py`, historical R5 results, and governance override semantics remain completely untouched.
- **Whether a new protocol version (R6.1+) is required**: YES (`R6.1`)
- **Approval state**: `APPROVED_BY_SUPERVISOR` (Order `CMD-CVSS-IEEE-R6-A1-T2-DEVIATION-FREEZE-241`)
