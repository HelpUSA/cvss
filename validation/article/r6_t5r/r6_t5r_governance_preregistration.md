# R6.1-T5R Preregistration: Governance Override Contract Tests (Versioned Rerun)
## Test Suite: `TEST-SUITE-R6-T5R-GOVERNANCE-CONTRACT`

* **Document Version**: 1.0.0
* **Protocol Version**: R6.1
* **Protocol Deviation ID**: `R6-DEV-003`
* **Classification**: `POST_RESULT_CHANGE`
* **Research Question Linkage**: **RQ-R6-3** (*"Uma camada estruturada de governance override pode tornar os desvios operacionais auditáveis sem modificar a política nominal da Eq. 8?"*)
* **Execution Status**: `PREREGISTERED_NOT_EXECUTED`
* **Parent Experiment**: [`TEST-SUITE-R6-T5-GOVERNANCE-CONTRACT`](file:///D:/AntiG/cvss/validation/article/r6_t5/r6_t5_governance_preregistration.md) (Historical result: 7/8 PASS, 1/8 FAIL)
* **Specification Baseline**: [`validation/article/r6_governance_override_specification.md`](file:///D:/AntiG/cvss/validation/article/r6_governance_override_specification.md)
* **Contract Specification**: [`validation/article/r6_governance_override_contract.json`](file:///D:/AntiG/cvss/validation/article/r6_governance_override_contract.json)
* **Target Implementation Module**: [`core/r6_governance_override.py`](file:///D:/AntiG/cvss/core/r6_governance_override.py)
* **Target Success Rate**: `null`
* **Expected Pass Rate**: `null`
* **Held-Out Corpus Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`)

---

## 1. Architectural Foundations & Historical Context

During the canonical execution of the initial T5 suite (`TEST-SUITE-R6-T5-GOVERNANCE-CONTRACT`), 7 out of 8 fixtures passed their frozen oracles. Fixture `T5.8` failed because the preregistered fixture input hardcoded a nominal policy priority of `'LOW'`, whereas Equation 8 for the referenced scenario `SCN-NVD-001` (`base_priority = 'LOW'`, `asset_class = 'public_web_application'`) mathematically computes a nominal environmental priority of `'MEDIUM'`. 

The implementation in [`core/r6_governance_override.py`](file:///D:/AntiG/cvss/core/r6_governance_override.py) actively detected the mismatch, correctly enforced Invariant G2 by neutralizing the forged nominal priority, and failed closed under Invariant G8. Formal adversarial review `CMD-CVSS-IEEE-R6-A1-T5-GOVERNANCE-REVIEW-268` classified this failure as `FIXTURE_OR_ORACLE_DEFECT`.

This versioned rerun (`R6.1-T5R`) corrects the baseline nominal contradiction in `T5R.8` while preserving all historical T5 results intact.

```
[Raw Evidence Traces]
       │
       ▼
[Evidence Normalization]
       │
       ▼
[Nominal Policy Evaluation: Equation 8]
       │
       ▼
[nominal_policy_priority] (Computed, Immutable, Recorded in Trace)
       │
       ▼
[Governance Override Layer: core/r6_governance_override.py]
       │
       ├──────────────────────┬──────────────────────┐
       ▼                      ▼                      ▼
[NOT_REQUESTED /        [APPROVED]             [REJECTED]
 UNAUTHORIZED]                │                      │
       │                Authorized Post-       Nominal Preserved
Nominal Preserved       Override Priority      Audit Trail Retained
       │                      │                      │
       └──────────────────────┴──────────────────────┘
                              │
                              ▼
               [Final Authorized Trace Record]
```

### Core Invariants Tested:
* **Invariant G1 (Authorization Prerequisite)**: An override cannot be applied (`override_applied == true`) unless `authorization_state == "APPROVED"` and `authorized_by_role` is explicitly populated.
* **Invariant G2 (Nominal Preservation)**: The computed value of Equation 8 must always be preserved intact in `nominal_policy_priority` and must never be overwritten, mutated, or omitted.
* **Invariant G3 (Mandatory Justification & Evidence)**: If `override_applied == true`, `reason_code` must be a valid closed-world enum token and `evidence_ids` must contain at least one valid identifier.
* **Invariant G4 (Separation of Roles / No Self-Authorization)**: An automated watcher or requesting entity cannot authorize its own override request. `authorized_by_role` must represent a distinct governance role.
* **Invariant G5 (No Autonomous Override)**: The core CVSS scorer is strictly prohibited from autonomously triggering, applying, or synthesizing an override without external governance dispatch.
* **Invariant G6 (Eq. 8 Formula Invariance)**: Equation 8 weights ($w_{\text{base}}, w_{\text{context}}, w_{\text{control}}$) and scoring logic remain strictly constant. No dynamic terms (such as `delta_audit`) may be added.
* **Invariant G7 (Audit Reproducibility)**: The combination of `nominal_policy_priority`, `reason_code`, `evidence_ids`, and `authorized_by_role` must allow an independent auditor to reconstruct the exact rationale of the decision.
* **Invariant G8 (Fail-Closed Default)**: Any malformed record, missing mandatory field, unapproved request, or invariant breach automatically fails closed, ensuring `override_applied = false`, `post_override_priority = nominal_policy_priority`, and `review_required = true`.

---

## 2. Automatic vs. Human-Authorized Boundary

| Decision / Verification Layer | Mechanical / Automated Validation | Human-Authorized Prerequisite | Fail-Closed Fallback |
| :--- | :---: | :---: | :--- |
| **Schema Conformance** | **YES** (Syntax, non-empty fields, valid UUIDs) | NO | `override_applied = false` |
| **State Transitions** | **YES** (Enforces DAG lifecycle state machine) | NO | `INVALID_STATE_TRANSITION` |
| **Role Separation** | **YES** (Asserts `requester_role != authorized_by_role`) | NO | `GOVERNANCE_SELF_AUTHORIZATION_REJECTED` |
| **Justification Syntax** | **YES** (Asserts valid enum and text length > 30 for OTHER) | NO | `GOVERNANCE_MISSING_REASON_CODE_REJECTED` |
| **Evidence Linkage** | **YES** (Asserts `len(evidence_ids) >= 1`) | NO | `GOVERNANCE_EMPTY_EVIDENCE_REJECTED` |
| **Priority Override Application** | NO | **YES** (`SECURITY_LEAD`, `MASTER_SUPERADMIN`, `INCIDENT_COMMANDER`) | **Fail-closed: Nominal governs** |

> [!IMPORTANT]
> **No Autonomous Scoring Authority**: The system possesses zero authority to invent, grant, or apply overrides on its own initiative. In the absence of an explicit, valid human authorization record, the nominal Equation 8 output governs unconditionally.

---

## 3. Versioned Fixture Definitions ($N = 8$)

The test suite consists of exactly 8 versioned fixtures mapped 1:1 to T5.1–T5.8:

### Fixture T5R.1: `override_not_requested` (Semantically Identical to T5.1)
* **Target Property**: When `override_requested == false`, `override_applied` must be false and nominal priority governs unconditionally.
* **Expected Decision**: `NOMINAL_PRESERVED` (`override_applied = false`, `final_priority = LOW`, `review_required = false`).

### Fixture T5R.2: `requested_not_approved` (Semantically Identical to T5.2)
* **Target Property**: An override request in `REQUESTED` state fails closed to nominal priority pending adjudication.
* **Expected Decision**: `UNAUTHORIZED_REQUEST_REJECTED` (`override_applied = false`, `final_priority = MEDIUM`, `review_required = true`).

### Fixture T5R.3: `approved_valid_override` (Semantically Identical to T5.3)
* **Target Property**: A fully authorized override meeting all invariants transitions priority cleanly and retains full audit trail.
* **Expected Decision**: `OVERRIDE_APPLIED_SUCCESSFULLY` (`override_applied = true`, `final_priority = MEDIUM`, `review_required = false`).

### Fixture T5R.4: `missing_reason_code_fails_closed` (Semantically Identical to T5.4)
* **Target Property**: An approved override missing mandatory `reason_code` fails closed under Invariant G3.
* **Expected Decision**: `FAIL_CLOSED_MISSING_REASON_CODE` (`override_applied = false`, `final_priority = HIGH`, `review_required = true`).

### Fixture T5R.5: `empty_evidence_fails_closed` (Semantically Identical to T5.5)
* **Target Property**: An approved override with empty `evidence_ids: []` fails closed under Invariant G3.
* **Expected Decision**: `FAIL_CLOSED_EMPTY_EVIDENCE` (`override_applied = false`, `final_priority = MEDIUM`, `review_required = true`).

### Fixture T5R.6: `self_authorization_rejected` (Semantically Identical to T5.6)
* **Target Property**: An override where `requester_role == authorized_by_role` fails closed under Invariant G4.
* **Expected Decision**: `FAIL_CLOSED_SELF_AUTHORIZATION` (`override_applied = false`, `final_priority = LOW`, `review_required = true`).

### Fixture T5R.7: `malformed_transition_rejected` (Semantically Identical to T5.7)
* **Target Property**: Direct lifecycle jump from `NOT_REQUESTED` to `APPROVED` without intermediate `REQUESTED` state is rejected.
* **Expected Decision**: `INVALID_STATE_TRANSITION_REJECTED` (`is_valid = false`, transition rejected).

### Fixture T5R.8: `nominal_formula_intact` (Corrected Baseline derived from Eq. 8)
* **Target Property**: Equation 8 nominal policy calculation is bit-for-bit identical before and after governance pipeline execution, with zero modification to mathematical weights, and an authorized override applies cleanly when the nominal baseline matches Equation 8 ground truth (`MEDIUM`).
* **Input State**: Execution of `execute_governance_pipeline()` across `SCN-NVD-001_v2_canonical.json` with `nominal_policy_priority = "MEDIUM"` and authorized override to `"HIGH"`.
* **Expected Decision**: `NOMINAL_CALCULATION_UNMODIFIED` (`priority_comparison.nominal_policy_priority == "MEDIUM"`, `override_applied == true`, `final_authorized_priority == "HIGH"`).
* **Expected Diagnostic**: `GOVERNANCE_OVERRIDE_APPLIED_SUCCESSFULLY`.

---

## 4. Denominator & Execution Accounting

$$\text{Primary Denominator } (D) = \mathbf{8 \text{ canonical fixtures}}$$
$$\text{Execution Case Count} = \mathbf{8 \text{ cases}}$$

* **Deterministic Construction Rule**: Purely programmatic generation of canonical fixtures; zero random sampling.
* **Target Success Rate**: Formally `null` (exploratory verification suite; no pre-fixed success claims).
* **Expected Pass Rate**: Formally `null`.
* **Held-Out Corpus Isolation**: Access to `validation/article/r6_heldout/*` is **STRICTLY PROHIBITED**.

---

## 5. Epistemological Claim Boundaries

1. **Historical Record Preservation**:
   The T5 original result ($7/8 \text{ PASS}, 1/8 \text{ FAIL}$) remains part of the permanent scientific record. T5-R does not erase or overwrite historical outcomes.
2. **No Claims of Ground Truth**:
   Verification of governance overrides confirms process auditability, traceability, and invariant conformance; it does **not** validate that human decisions reflect objective technical truth.
3. **No Claim of Human Expert Adjudication**:
   These fixtures test contract logic using synthetic role tokens; they do **not** constitute an empirical study of human consensus or operational expert review.
