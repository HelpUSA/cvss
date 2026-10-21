# R6-1 Future Test Plan: Schema v2 and Governance Override Contracts

## 1. Plan Overview & Protocol Governance
* **Document Version**: 1.0.0
* **Status**: `PLANNED_NOT_EXECUTED`
* **Parent Preregistration Commit**: `c0b4025d9f560b8e525accd17e1b075cd23a355b`
* **Held-Out Lock Commit**: `12bf6c456054656a1bbc198d7e3729d2675098b2`
* **Specification Baseline Commit**: `2346859b319eac9146273b215eca796147816837`
* **Execution Status**: `ZERO_TESTS_EXECUTED`
* **Scientific Code Implementation State**: `NOT_IMPLEMENTED`
* **Results Available**: `false`

### Mandatory Protocol Guardrails
1. **Specification-First Principle**: This document pre-registers future test designs, suites, and evaluation criteria prior to writing code or observing empirical results.
2. **Anti-Retuning Lock**: Test assertions, acceptable thresholds, and evaluation logic are frozen. Post-observation changes must be formally logged as `POST_RESULT_CHANGE` in `validation/article/r6_a1_protocol_deviation_log.md`.
3. **No Target Claims**: No target success rate (e.g., 100% or 16/16) is asserted in this specification. All outcomes will be reported transparently regardless of result.
4. **Held-Out Firewall**: The 938 frozen held-out vulnerability cases must remain quarantined and untouched during schema and governance implementation.

---

## 2. Test Suite Specifications (T1–T7)

### T1 — Schema Unit Contract Tests
* **Identifier**: `TEST-SUITE-R6-T1-SCHEMA-UNIT`
* **Execution Status**: `STATUS: PLANNED_NOT_EXECUTED`
* **Target Artifact**: Schema v2 Validator / Parser
* **Objective**: Verify that individual structural rules, field boundaries, and type constraints defined in `validation/article/r6_schema_v2_specification.md` are strictly enforced in isolation.

#### Planned Test Cases:
1. `T1.1_valid_declared_fields`: Inputs conforming strictly to declared properties across all 8 objects are accepted.
2. `T1.2_unknown_core_field_rejected`: Injecting an undeclared property into root or core objects (`environmental_evidence`, `candidate_environmental_assessment`, `priority_comparison`) raises `UNKNOWN_FIELD`.
3. `T1.3_nested_unknown_field_rejected`: Injecting undeclared attributes inside nested array items (`CompensatingControlItem`, `EvidenceLinkItem`) raises `UNKNOWN_FIELD`.
4. `T1.4_valid_extension_namespace_accepted`: Properties located inside `extensions: {}` matching `^[a-z0-9_]{3,30}:[a-z0-9_]{2,50}$` are accepted.
5. `T1.5_invalid_extension_namespace_rejected`: Non-namespaced or malformed properties inside `extensions: {}` raise `INVALID_EXTENSION_NAMESPACE`.
6. `T1.6_missing_required_field`: Omitting mandatory attributes (e.g., `scenario_id`, `asset_class`, `base_priority`) raises `MISSING_REQUIRED_FIELD`.
7. `T1.7_invalid_type`: Providing a boolean or number for a string field (or string for number) raises `INVALID_TYPE`.
8. `T1.8_invalid_enum`: Supplying non-enumerated tokens for metrics (e.g., `internet_exposure: "wide_open"`) raises `INVALID_ENUM`.
9. `T1.9_invalid_range`: Supplying scores outside `[0.0, 10.0]` raises `INVALID_RANGE`.
10. `T1.10_null_handling`: Submitting `null` for non-nullable scalar fields raises `INVALID_TYPE`.
11. `T1.11_reserved_field_handling`: Injecting reserved architectural keywords (`delta_audit`, `formula_override`) raises `RESERVED_FIELD`.

---

### T2 — Backward Compatibility Classification
* **Identifier**: `TEST-SUITE-R6-T2-BACKWARD-COMPAT`
* **Execution Status**: `STATUS: PLANNED_NOT_EXECUTED`
* **Target Artifact**: Canonical R2–R5 Dataset Traces (SCN-NVD-001 through SCN-SYN-030)
* **Objective**: Deterministically evaluate and classify all historical baseline traces against Schema v2 without retroactive coercion or silent modifications.

#### Planned Classification Taxonomy:
* **`V1_VALID_V2_VALID`**: Traces meeting all v1 and v2 constraints without modification.
* **`V1_VALID_V2_INVALID_UNDECLARED_FIELD`**: Traces valid under v1 open-world but failing v2 closed-world due to undeclared properties.
* **`V1_INVALID_V2_INVALID`**: Traces violating structural constraints in both specifications.
* **`V1_VALID_V2_VALID_NORMALIZED`**: Traces resolving validly via pre-registered deterministic normalizers.

#### Reporting Requirement:
Every observed divergence must be cataloged in the compatibility matrix. No incompatibility may be masked by relaxing schema rules post hoc.

---

### T3 — Historical R5 F1–F9 Mutation Replay
* **Identifier**: `TEST-SUITE-R6-T3-F1-F9-REPLAY`
* **Execution Status**: `STATUS: PLANNED_NOT_EXECUTED`
* **Target Artifact**: R3 Canonical 120 Randomized Mutants
* **Objective**: Re-evaluate the exact 120 applicable mutants generated under seed `20261021` using Schema v2, preserving original mutation families and denominators.

#### Protocol Integrity Safeguards:
1. **Preservation of Denominators**: The 120 applicable mutants, 6 representative scenarios, and family allocations (F1: 16, F2: 12, F3: 16, F4: 15, F5: 13, F6: 15, F7: 10, F8: 11, F9: 12) remain strictly fixed.
2. **Historical Integrity of F3**: The R5 open-world result for Family F3 (`0/16` rejected, `16/16` accepted) remains an immutable historical baseline.
3. **No Target Claim**: Schema v2 is tested to observe how many F3 mutants are rejected under closed-world enforcement. No pre-fixed target rejection rate is claimed.

---

### T4 — New Schema-v2-Specific Mutation Campaign
* **Identifier**: `TEST-SUITE-R6-T4-SCHEMA-V2-MUTATIONS`
* **Execution Status**: `STATUS: PLANNED_NOT_EXECUTED`
* **Target Artifact**: Synthetic and NVD Traces with Schema-Specific Perturbations
* **Objective**: Assess the sensitivity and discrimination of Schema v2 against targeted structural boundary perturbations.

#### Pre-Registered Mutation Operator Families:
* **`M-V2-01` (Nested Undeclared Field)**: Injection of arbitrary properties inside nested objects.
* **`M-V2-02` (Reserved Keyword Collision)**: Direct insertion of reserved tokens (`delta_audit`, `runtime_bypass`).
* **`M-V2-03` (Malformed Extension Namespace)**: Injection of extension properties lacking vendor prefix.
* **`M-V2-04` (Type Mutation on Deep Subobjects)**: Corrupting primitive types within subobject arrays.
* **`M-V2-05` (Enum Boundary Violation)**: Corrupting newly restricted enumeration tokens.

*Note: Mutation counts, random seeds, and specific denominator allocations will be frozen in a dedicated lock manifest prior to campaign execution.*

---

### T5 — Governance Override Contract Tests
* **Identifier**: `TEST-SUITE-R6-T5-GOVERNANCE-CONTRACT`
* **Execution Status**: `STATUS: PLANNED_NOT_EXECUTED`
* **Target Artifact**: Governance Override Verification Module
* **Objective**: Validate all 8 formal invariants (INV-G1 through INV-G8) and state transitions defined in `validation/article/r6_governance_override_specification.md`.

#### Planned Verification Scenarios:
1. `T5.1_override_not_requested`: Verify that if `override_requested == false`, `override_applied` cannot be true.
2. `T5.2_requested_not_approved`: Verify that a requested override with status `REQUESTED` or `REJECTED` leaves nominal priority unchanged.
3. `T5.3_approved_valid_override`: Verify that a fully authorized record with valid role, timestamp, reason code, and evidence transitions priority cleanly and logs complete audit trail.
4. `T5.4_missing_reason_code_fails_closed`: An approved override missing `reason_code` fails closed: `override_applied = false`, `post_override_priority = nominal`.
5. `T5.5_empty_evidence_fails_closed`: An approved override with empty `evidence_ids: []` fails closed.
6. `T5.6_self_authorization_rejected`: A trace where the watcher/requester role matches `authorized_by_role` fails closed.
7. `T5.7_malformed_transition_rejected`: Direct jump from `NOT_REQUESTED` to `APPROVED` without intermediate `REQUESTED` state is rejected with `INVALID_STATE_TRANSITION`.
8. `T5.8_nominal_formula_intact`: Confirm Equation 8 calculation is identical before and after governance processing.

---

### T6 — Historical Representability Check (Four R5 NVD Deviations)
* **Identifier**: `TEST-SUITE-R6-T6-NVD-REPRESENTABILITY`
* **Execution Status**: `STATUS: PLANNED_NOT_EXECUTED`
* **Target Artifact**: SCN-NVD-001, SCN-NVD-003, SCN-NVD-007, and SCN-NVD-011
* **Objective**: Verify that the governance override data structure can faithfully encapsulate, represent, and audit the operational context of historical NVD deviations.

#### Boundary Constraints:
1. **No Tuning of Reason Codes**: Reason codes in the contract are pre-registered and must not be altered to match historical text.
2. **No 30/30 Target**: Reproducing 30/30 nominal agreement is **not** an objective or success criterion.
3. **Auditability, Not Correctness**: Passing these cases through the governance schema verifies schema expressiveness and audit trail completeness, not that human determinations were ground truth.

---

### T7 — Held-Out Corpus Firewall
* **Identifier**: `TEST-SUITE-R6-T7-HELDOUT-FIREWALL`
* **Execution Status**: `STATUS: PLANNED_NOT_EXECUTED`
* **Target Artifact**: Quarantined 938 Public Advisories (`validation/article/r6_heldout/*`)
* **Objective**: Strictly enforce that the held-out dataset remains unaccessed, unread, and unprocessed during all development and tuning of Schema v2 and Governance Override modules.

#### Firewall Rules:
1. **Complete Isolation**: No parser, normalizer, or test script may load or query `validation/article/r6_heldout/eligible_corpus_manifest.json` during the implementation phase.
2. **Pre-Execution Gate**: Execution on the held-out corpus may commence only after:
   - Schema v2 implementation is committed and frozen.
   - Governance override implementation is committed and frozen.
   - Test suites T1–T6 have passed in an isolated staging environment.
   - Official authorization order is dispatched by HelpUS supervision.
3. **Leak / Tamper Penalty**: Any accidental or premature processing of held-out records constitutes a severe protocol deviation requiring immediate disclosure and invalidation of downstream claims.

---

## 3. Change Control & Deviation Logging
* **Freeze Boundary**: Following the commit of this test plan, all testing procedures are subject to strict change control.
* **Pre-Execution vs. Post-Execution Changes**:
  - Clarifications made prior to executing code must be logged as `PRE_EXECUTION_REFINEMENT`.
  - Any parameter, threshold, or test rule change made after viewing experimental outputs must be classified as `POST_RESULT_CHANGE`.
* **Prohibition Against Silent Tweaks**: Silent adjustments to improve mutation rejection rates, compatibility metrics, or reviewer benchmarks are strictly prohibited.
