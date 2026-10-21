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
| `R6-DEV-002` | 2026-10-21T18:40:00Z | R6-A1 | RQ-R6-1, RQ-R6-2 | `POST_RESULT_CHANGE` | `APPROVED_BY_SUPERVISOR` | Identification of valid-parent confounding in Experiment T4 where 30 historical parents were valid only under v1 and invalid under v2; preregistration of versioned rerun R6.1-T4R on 15 deterministically canonicalized v2-valid parents. |
| `R6-DEV-003` | 2026-10-21T19:40:00Z | R6-A1 | RQ-R6-3 | `POST_RESULT_CHANGE` | `APPROVED_BY_SUPERVISOR` | Post-result identification of fixture/oracle inconsistency in Experiment T5 fixture T5.8 (injected nominal priority LOW for SCN-NVD-001 vs Eq. 8 computed nominal MEDIUM); preregistration of versioned rerun R6.1-T5R with minimal baseline alignment on T5R.8 while preserving original T5 (7/8) as historical finding. |

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

---

### Deviation ID: R6-DEV-002
- **Timestamp UTC**: 2026-10-21T18:40:00Z
- **Requested by**: AI Bridge Supervisor & HelpUS Research Team (`helpusdev@helpus.ai`)
- **Phase**: R6-A1 (Experiment T4 Novel Schema v2 Mutation Campaign)
- **Original preregistered rule**: In `validation/article/r6_t4/r6_t4_mutation_family_contract.json` and `r6_t4_mutation_family_preregistration.md`, the preconditions for families NF1–NF6 were defined as `valid_trace_root` / `valid_trace_with_controls`, referencing the 30 canonical historical scenarios. Detection was evaluated by `mutant.v2_valid == False`.
- **Trigger**: Auditorial Order `CMD-CVSS-IEEE-R6-A1-T4-ATTRIBUTION-AUDIT-258` revealed that all 30 historical scenarios are valid only under Schema v1 and are 100% invalid under Schema v2 prior to mutation (12 `INVALID_TYPE` on legacy narrative controls/links, 18 `INVALID_ENUM` on synthetic `cve_id: ""`). Consequently, while all 180 mutated inputs were rejected by the Schema v2 validator (`180/180 rejected`), the rejection cannot be causally attributed to the injected mutations under a fail-fast parser because the parent inputs were already rejected. Furthermore, for Family NF2 (`custom_audit:cvss_b_score` in extensions), the mutation matches the vendor namespace regex and is accepted by the validator; its rejection in T4 was 100% artifactual, masked by the pre-existing invalidity of the parent traces.
- **Proposed change**:
  1. **Preserve Original T4**: The original T4 campaign remains completely immutable in `validation/article/r6_t4/` with factually reported outcomes (`180/180 mutated inputs rejected; attribution confounded by v2-invalid parents`). No original T4 result will be overwritten or retroactively altered.
  2. **Refine Attribution Taxonomy**: For versioned reruns, replace overlapping status reporting with a mutually exclusive primary attribution model (`ATTRIBUTABLE_MUTATION_DETECTION`, `PREEXISTING_PARENT_INVALIDITY`, `ATTRIBUTION_UNRESOLVED`) and an orthogonal diagnostic flag (`mutation_specific_error_additionally_observed`).
  3. **Preregister Versioned Rerun `R6.1-T4R`**: Conduct a versioned rerun on certified Schema v2-compliant canonical parents:
     - 15 historical scenarios deterministically canonicalized to `v2_valid == True` without inventing new information (preserving all nominal Equation 8 inputs and narrative descriptions).
     - 15 historical scenarios with unresolved enums (`internet_exposure = 'restricted'` or `environmental_priority = 'defer'`) marked as `PARENT_CANONICALIZATION_NOT_POSSIBLE_WITHOUT_NEW_INFORMATION` and excluded from the T4R denominator.
     - Frozen denominator: $15 \text{ parents} \times 6 \text{ families} = 90 \text{ applicable mutants}$.
  4. **Boundary Finding Preservation**: NF2 is retained exactly as preregistered, acknowledging that vendor namespaced keys without shadow collision checks represent an authentic boundary property of the frozen validator implementation. Companion family NF2-R is preregistered to isolate core subobject injection.
- **Rationale**: Strict IEEE Q1 research integrity demands that mutation-kill claims reflect causal detection rather than inherited parent syntax errors.
- **Files affected**:
  - `validation/article/r6_a1_protocol_deviation_log.md` (this record)
  - `validation/article/r6_1_t4r/r6_1_t4r_parent_canonicalization_spec.md`
  - `validation/article/r6_1_t4r/r6_1_t4r_parent_manifest.json`
  - `validation/article/r6_1_t4r/r6_1_t4r_mutation_preregistration.md`
  - `validation/article/r6_1_t4r/r6_1_t4r_contract.json`
  - `validation/article/r6_1_t4r/r6_1_t4r_execution_plan.md`
  - `validation/article/r6_a1_experiment_registry.json`
- **RQ/Hypothesis affected**: RQ-R6-1, RQ-R6-2
- **Had any relevant results already been observed?**: YES (T4 canonical execution observed 180/180 rejected inputs under confounded parents).
- **Classification**: `POST_RESULT_CHANGE`
- **Potential bias introduced**: Construction of canonicalized parents after observing T4 outcomes.
- **Corrective action & Anti-Overfitting Safeguards**:
  1. **Canonicalization derived strictly from spec**: No transformation uses T4 results to choose repairs.
  2. **Refusal to guess**: Scenarios with ambiguous enums (`restricted`, `defer`) are excluded rather than coerced.
  3. **Original T4 Immutability**: All 4 result artifacts and 3 preregistration files of T4 remain byte-identical.
  4. **Held-Out Quarantine**: Held-out corpus remains untouched (`held_out_accessed = false`).
  5. **Core Equation 8 Invariance**: Policy scoring formula remains completely untouched.
- **Whether a new protocol version (R6.1+) is required**: YES (`R6.1-T4R`)
- **Approval state**: `APPROVED_BY_SUPERVISOR` (Order `CMD-CVSS-IEEE-R6-A1-T4-DEVIATION-AND-T4R-PREREG-259`)

#### Clarification Note: Pre-Result Denominator Clarification (Order 260)
- **Timestamp UTC**: 2026-10-21T18:55:00Z
- **Classification**: `PRE_RESULT_CLARIFICATION` (within scope of R6-DEV-002; zero T4R results observed)
- **Clarification**: Resolved potential ambiguity regarding primary vs. companion denominators. The primary campaign (`R6.1-T4R-PRIMARY`) is strictly frozen at $N = 15 \text{ canonical parents} \times 6 \text{ original families} = 90 \text{ mutants}$. The post-result companion operator is partitioned into an isolated subexperiment (`R6.1-T4R-NF2R-COMPANION`) with denominator $N = 15 \times 1 = 15 \text{ mutants}$. The construction of a combined single primary detection rate (out of 105) is explicitly prohibited. Approval state: `APPROVED_BY_SUPERVISOR` (Order `CMD-CVSS-IEEE-R6-A1-T4R-DENOMINATOR-CLARIFY-260`).

---

### Deviation ID: R6-DEV-003
- **Timestamp UTC**: 2026-10-21T19:40:00Z
- **Requested by**: AI Bridge Supervisor & HelpUS Research Team (`helpusdev@helpus.ai`)
- **Phase**: R6-A1 (Experiment T5 Governance Contract Evaluation)
- **Original preregistered rule**: Fixture `T5.8` (`nominal_formula_intact`) in `validation/article/r6_t5/r6_t5_governance_fixtures.json` was defined referencing case `SCN-NVD-001` with hardcoded `nominal_policy_priority = "LOW"` in the fixture and in `override_data`, with expected oracle `expected_override_applied: true`, `expected_final_priority: "HIGH"`, and `expected_diagnostics: ["GOVERNANCE_OVERRIDE_APPLIED_SUCCESSFULLY"]`.
- **Trigger**: Read-only adversarial audit `CMD-CVSS-IEEE-R6-A1-T5-GOVERNANCE-REVIEW-268` revealed that for `SCN-NVD-001` (`base_priority = "LOW"`, `asset_class = "public_web_application"`), Equation 8 computes nominal environmental priority as `"MEDIUM"` ($s_{\text{base}} = 1, w_{\text{context}} = 2, w_{\text{control}} = -1 \implies s_{\text{nominal}} = 2 \Rightarrow \text{MEDIUM}$). When passed to `evaluate_governance_override()`, the implementation at line 175 of `core/r6_governance_override.py` actively enforced Invariant G2, detecting that `payload_nominal ("LOW") != nominal_policy_priority ("MEDIUM")`, restoring `"MEDIUM"` and failing closed (`override_applied = False`), contradicting the fixture's expected oracle. The failure was classified as `FIXTURE_OR_ORACLE_DEFECT`.
- **Proposed change**:
  1. **Preserve Original T5**: The original T5 campaign remains completely immutable in `validation/article/r6_t5/` with factually reported outcomes (`7/8 PASS, 1/8 FAIL`). No original T5 file will be overwritten or retroactively altered.
  2. **Preregister Versioned Rerun `R6.1-T5R`**: Create `TEST-SUITE-R6-T5R-GOVERNANCE-CONTRACT` in `validation/article/r6_t5r/`:
     - Fixtures `T5R.1` to `T5R.7` remain semantically identical to `T5.1` to `T5.7` (zero change).
     - Fixture `T5R.8` applies minimal correction: aligns `nominal_policy_priority` in payload and preconditions with the actual Equation 8 nominal ground truth (`"MEDIUM"`), testing that when nominal priority is consistent with Equation 8, authorized override applies cleanly and Equation 8 nominal calculation remains intact in `priority_comparison.nominal_policy_priority`.
  3. **Denominator and Invariants**: Exactly 8 fixtures ($D = 8$). `target_success_rate = null`, `expected_pass_rate = null`.
- **Rationale**: Strict scientific integrity requires isolating and testing the Equation 8 nominal preservation invariant without confounding baseline nominal mismatch.
- **Files affected**:
  - `validation/article/r6_a1_protocol_deviation_log.md` (this record)
  - `validation/article/r6_a1_experiment_registry.json`
  - `validation/article/r6_t5r/r6_t5r_governance_preregistration.md`
  - `validation/article/r6_t5r/r6_t5r_governance_fixture_contract.json`
  - `validation/article/r6_t5r/r6_t5r_governance_fixtures.json`
  - `validation/article/r6_t5r/r6_t5r_governance_execution_plan.md`
  - `validation/article/r6_t5r/r6_t5_to_t5r_change_manifest.json`
- **RQ/Hypothesis affected**: RQ-R6-3
- **Had any relevant results already been observed?**: YES (Canonical T5 run observed 7/8 PASS, 1/8 FAIL on T5.8).
- **Classification**: `POST_RESULT_CHANGE`
- **Potential bias introduced**: Correction of test fixture after observing preliminary execution failure.
- **Corrective action & Anti-Overfitting Safeguards**:
  1. **Original T5 Immutability**: All original T5 artifacts and results remain byte-identical and permanently recorded as historical evidence ($7/8 \text{ PASS}, 1/8 \text{ FAIL}$).
  2. **Zero Implementation Modifications**: The implementation module `core/r6_governance_override.py` remains 100% untouched.
  3. **Zero Specification Modifications**: The specification `r6_governance_override_specification.md` remains 100% untouched.
  4. **Zero Formula Modifications**: Equation 8 weights and calculation logic remain 100% untouched.
  5. **Minimal Scope**: Only T5R.8 baseline is aligned with Eq. 8 ground truth; T5R.1 to T5R.7 remain semantically identical.
  6. **No Target Rates**: Formally `target_success_rate = null` and `expected_pass_rate = null`.
  7. **Held-Out Quarantine**: Held-out corpus remains untouched (`held_out_accessed = false`).
- **Whether a new protocol version (R6.1+) is required**: YES (`R6.1-T5R`)
- **Approval state**: `APPROVED_BY_SUPERVISOR` (Order `CMD-CVSS-IEEE-R6-A1-T5-DEVIATION-T5R-PREREGISTER-269`)
