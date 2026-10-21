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
| `R6-DEV-004` | 2026-10-21T20:44:00Z | R6-A1 | RQ-R6-4 | `PRE_RESULT_CHANGE` | `APPROVED_BY_SUPERVISOR` | Pre-result clarification of differential validation measurement model (R6.1-DIFF-R1) reclassifying primary endpoint to exact numeric score concordance and removing comparator vector serializer requirement from precedence hierarchy to avoid false masking of 486,472 vectors prior to execution. |
| `R6-DEV-005` | 2026-10-21T22:15:00Z | R6-A1 | RQ-R6-4 | `POST_RESULT_CHANGE` | `APPROVED_BY_SUPERVISOR` | Identification of classification defect (cvss4py MissingMetric exception omitted from expected rejection tuple) and corpus eligibility conflation (evaluating 461,444 valid score vectors and 25,028 syntax rejection tests under single denominator); preregistration of corrected protocol R6.2-DIFF-R2 with decoupled dual endpoints and pre-filtered eligibility manifest. |

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

---

### Deviation ID: R6-DEV-004
- **Timestamp UTC**: 2026-10-21T20:44:00Z
- **Requested by**: AI Bridge Supervisor & HelpUS Research Team (`helpusdev@helpus.ai`)
- **Phase**: R6-A1 (Differential Validation CVSS v4.0)
- **Original preregistered rule**: `validation/article/r6_differential/r6_differential_preregistration.md` included `COMPARATOR_UNSUPPORTED_CASE` and `VECTOR_NORMALIZATION_MISMATCH` directly in the primary classification precedence hierarchy above `EXACT_MATCH`.
- **Trigger**: Capability audit of acquired comparator `cvss4py` revealed it does not implement vector string serialization or direct severity string methods. Under original precedence, 100% of 486,472 vectors would be classified as `COMPARATOR_UNSUPPORTED_CASE` or fail normalization, completely obscuring the core mathematical scoring concordance.
- **Proposed change**: Preregister clarified protocol R1 (`TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R1` in `validation/article/r6_differential_r1/`):
  - Primary endpoint: `EXACT_NUMERIC_SCORE_CONCORDANCE` ($|\text{score}_{\text{primary}} - \text{score}_{\text{secondary}}| < 0.0001$).
  - Clarified precedence hierarchy: `EXECUTION_ERROR > VALIDITY_DISAGREEMENT > SCORE_MISMATCH > EXACT_SCORE_MATCH`.
  - Orthogonal secondary diagnostic dimensions: `derived_severity_concordance` via FIRST §4.2 intervals; `native_vector_serializer` recorded as unsupported capability metadata; `nomenclature_input_prefix` validated.
  - Prohibition of synthetic serializer adapters.
- **Rationale**: Pre-result clarification eliminates instrumentation artifacts without altering the scientific question, corpus, or comparison engines.
- **Files affected**:
  - `validation/article/r6_a1_protocol_deviation_log.md` (this record)
  - `validation/article/r6_a1_experiment_registry.json`
  - `validation/article/r6_differential_r1/r6_differential_r1_preregistration.md`
  - `validation/article/r6_differential_r1/r6_differential_r1_measurement_contract.json`
  - `validation/article/r6_differential_r1/r6_differential_r1_execution_plan.md`
  - `validation/article/r6_differential_r1/r6_differential_r1_change_manifest.json`
  - `validation/article/r6_differential_r1/r6_differential_r1_runner_contract.json`
- **RQ/Hypothesis affected**: RQ-R6-4
- **Had any relevant results already been observed?**: NO (0 / 486,472 vectors evaluated; `observed_evaluation_vectors = 0`, `results_available = false`).
- **Classification**: `PRE_RESULT_CHANGE`
- **Potential bias introduced**: None; change is committed strictly before any corpus vector is executed.
- **Corrective action & Anti-Overfitting Safeguards**:
  1. **Corpus Denominator Invariance**: Strictly 486,472 vectors ($D = 486{,}472$) unchanged.
  2. **Pinned Commits Invariance**: Corpus commit `d766d0c` and comparator commit `9fe705c` unchanged.
  3. **Strict Zero-Tolerance Numeric Equivalence**: Absolute threshold $|\Delta| < 0.0001$ unmodified.
  4. **Engine Invariance**: Both engines unmodified; zero serializer adapters fabricated.
  5. **No Target Rates**: Formally documented as `target_agreement_rate = null` and `expected_agreement_rate = null`.
  6. **Held-Out Quarantine**: Held-out corpus remains strictly quarantined (`held_out_accessed = false`).
  7. **Core Invariance**: Equation 8 formula and weights unmodified.
- **Whether a new protocol version (R6.1+) is required**: YES (`R6.1-DIFF-R1`)
- **Approval state**: `APPROVED_BY_SUPERVISOR` (Order `CMD-CVSS-IEEE-R6-A1-DIFF-PRE-RESULT-CLARIFICATION-281`)


---

### Deviation ID: R6-DEV-005
- **Timestamp UTC**: 2026-10-21T22:15:00Z
- **Requested by**: AI Bridge Supervisor & HelpUS Research Team (`helpusdev@helpus.ai`)
- **Phase**: R6-A1 (Differential Validation CVSS v4.0 R2)
- **Original preregistered rule**: Protocol R1 (`TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R1` in `validation/article/r6_differential_r1/`) defined a single aggregated denominator $D = 486{,}472$ for numeric score concordance, defined expected validation exceptions without `cvss4py.classes.MissingMetric`, and collapsed mutual syntax rejections of invalid cases into `EXACT_SCORE_MATCH`.
- **Trigger**: Adversarial review and contract/corpus reconciliation (Order `CMD-CVSS-IEEE-R6-A1-DIFF-R1-ADVERSARIAL-RESULT-REVIEW-288`) following execution of `R6.1-DIFF-R1`.
- **Two Independent Defects Identified**:
  1. **Defect A: Classification Defect (Omission of Expected Validation Exception)**:
     `cvss4py.classes.MissingMetric` was omitted from the expected validation exception tuple in runner R1. As a result, 13,126 official FIRST negative test cases (deliberately missing required metrics) were caught by the generic `except Exception as exc:` clause and misclassified as `EXECUTION_ERROR` rather than syntax rejection.
  2. **Defect B: Corpus/Endpoint Eligibility Conflation**:
     Protocol R1 declared a primary endpoint of exact numeric score concordance on valid vectors, but evaluated both 461,444 valid score-producing vectors and 25,028 negative syntax-rejection test cases from `reference-vectors` within the single denominator $D = 486{,}472$, collapsing mutual rejections into `EXACT_SCORE_MATCH`.
- **Post-Result Declarations**:
  - The discovery occurred strictly AFTER observing full R1 results;
  - Zero R2 evaluation observations exist;
  - The modification is strictly a post-result correction and is formally versioned as R2;
  - R1 artifacts and counts remain permanently preserved as immutable historical evidence.
- **Proposed Change**: Preregister versioned protocol R2 (`TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R2` / `R6.2-DIFF-R2` in `validation/article/r6_differential_r2/`):
  - **Decoupled Endpoints**:
    * **Primary Endpoint**: Numeric Score Concordance ($D_{\text{numeric}} = 461{,}444$, valid score-producing vectors only). Precedence: `EXECUTION_ERROR > VALIDITY_DISAGREEMENT > SCORE_MISMATCH > EXACT_SCORE_MATCH`. Equivalence tolerance: $|\Delta| < 0.0001$.
    * **Secondary Endpoint**: Negative Validation Concordance ($D_{\text{validation}} = 25{,}028$, FIRST negative test cases only). Precedence: `NEGATIVE_EXECUTION_ERROR > NEGATIVE_VALIDITY_DISAGREEMENT > SYNTAX_REJECTION_CONCORDANCE`.
  - **Corpus Eligibility Pre-filtering**: Machine-readable eligibility manifest (`r6_differential_r2_corpus_eligibility_manifest.json`) classifying all 486,472 records strictly prior to execution.
  - **Expected Validation Exceptions Contract**: Explicit inclusion of `cvss4py.classes.MissingMetric` in comparator validation exceptions, alongside `UnknownMetricValue`, `InvalidEqClass`, `UnknownMetric`, `SyntaxError`, `ValueError`, and `KeyError`.
  - **FIRST Reference Diagnostic**: Secondary diagnostic analysis comparing primary and secondary scores against official FIRST reference values for any vector exhibiting `SCORE_MISMATCH`.
  - **Derived Severity Diagnostic**: Qualitative severity rating interval comparison (Section 4.2).
- **Rationale**: Eliminates measurement confounding between mathematical float arithmetic and syntax validation while maintaining complete epistemological transparency.
- **Files Affected**:
  - `validation/article/r6_a1_protocol_deviation_log.md` (this record)
  - `validation/article/r6_a1_experiment_registry.json`
  - `validation/article/r6_differential_r2/r6_differential_r2_corpus_eligibility_manifest.json`
  - `validation/article/r6_differential_r2/r6_differential_r2_preregistration.md`
  - `validation/article/r6_differential_r2/r6_differential_r2_measurement_contract.json`
  - `validation/article/r6_differential_r2/r6_differential_r2_execution_plan.md`
  - `validation/article/r6_differential_r2/r6_differential_r2_change_manifest.json`
  - `validation/article/r6_differential_r2/r6_differential_r2_runner_contract.json`
  - `scripts/run_r6_2_differential_experiment.py`
- **RQ/Hypothesis Affected**: `RQ-R6-4`
- **Had any relevant results already been observed?**: YES for R1 (454,047 exact matches, 7,397 mismatches at $|\Delta| = 0.1$, 25,028 negative cases); strictly NO for R2 (`observed_evaluation_records = 0`, `results_available = false`).
- **Classification**: `POST_RESULT_CHANGE`
- **Potential Bias Introduced & Anti-Retuning Safeguards**:
  1. **Strict Engine Arithmetic Invariance**: Neither HelpUS scorer nor `cvss4py` arithmetic/rounding is modified.
  2. **Zero Tolerance Retuning**: Delta of 0.1 remains strictly `SCORE_MISMATCH`; no tolerance expansion permitted.
  3. **Null Targets**: `target_match_rate = null` and `expected_match_rate = null`.
  4. **Corpus Partition Invariance**: Partition sum strictly preserved ($461{,}444 + 25{,}028 = 486{,}472$).
  5. **Held-Out Quarantine**: Strictly locked (`held_out_accessed = false`).
  6. **Equation 8 Invariance**: Formula and weights untouched.
- **Whether a new protocol version (R6.2+) is required**: YES (`R6.2-DIFF-R2`)
- **Approval state**: `APPROVED_BY_SUPERVISOR` (Order `CMD-CVSS-IEEE-R6-A1-DIFF-R2-PREREGISTER-FREEZE-289`)
