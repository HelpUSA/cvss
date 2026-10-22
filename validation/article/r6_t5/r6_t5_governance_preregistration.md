# R6-T5 Preregistration: Governance Override Contract Tests
## Test Suite: `TEST-SUITE-R6-T5-GOVERNANCE-CONTRACT`

* **Document Version**: 1.0.0
* **Protocol Version**: R6.1
* **Research Question Linkage**: **RQ-R6-3** (*"Uma camada estruturada de governance override pode tornar os desvios operacionais auditáveis sem modificar a política nominal da Eq. 8?"*)
* **Execution Status**: `PREREGISTERED_NOT_EXECUTED`
* **Specification Baseline**: [`validation/article/r6_governance_override_specification.md`](file:///D:/AntiG/cvss/validation/article/r6_governance_override_specification.md)
* **Contract Specification**: [`validation/article/r6_governance_override_contract.json`](file:///D:/AntiG/cvss/validation/article/r6_governance_override_contract.json)
* **Target Implementation Module**: [`core/r6_governance_override.py`](file:///D:/AntiG/cvss/core/r6_governance_override.py)
* **Target Success Rate**: `null`
* **Expected Pass Rate**: `null`
* **Held-Out Corpus Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`)

---

## 1. Architectural Foundations & Invariant Safeguards

The Governance Override layer functions strictly as an **external post-scoring control boundary**, operating downstream of Equation 8 nominal policy evaluation. It formalizes exceptions to nominal priority without mutating mathematical weights or scoring algorithms.

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

A central methodological requirement of R6 is the formal delineation between machine-executable logic and human decision authority:

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

## 3. Canonical Fixture Definitions ($N = 8$)

The test suite consists of exactly 8 canonical, non-redundant fixtures derived directly from the specification:

### Fixture T5.1: `override_not_requested`
* **Target Property**: When `override_requested == false`, `override_applied` must be false and nominal priority governs unconditionally.
* **Input State**: Record with `override_requested = false` and `authorization_state = "NOT_REQUESTED"`.
* **Expected Decision**: `NOMINAL_PRESERVED` (`override_applied = false`, `final_priority = nominal`, `review_required = false`).
* **Expected Diagnostic**: `GOVERNANCE_OVERRIDE_NOT_REQUESTED`.

### Fixture T5.2: `requested_not_approved`
* **Target Property**: An override request in `REQUESTED` state fails closed to nominal priority pending adjudication.
* **Input State**: Record with `override_requested = true` and `authorization_state = "REQUESTED"`.
* **Expected Decision**: `UNAUTHORIZED_REQUEST_REJECTED` (`override_applied = false`, `final_priority = nominal`, `review_required = true`).
* **Expected Diagnostic**: `GOVERNANCE_UNAUTHORIZED_OVERRIDE_REJECTED`.

### Fixture T5.3: `approved_valid_override`
* **Target Property**: A fully authorized override meeting all invariants transitions priority cleanly and retains full audit trail.
* **Input State**: Record with `authorization_state = "APPROVED"`, `authorized_by_role = "SECURITY_LEAD"`, valid `reason_code`, non-empty `evidence_ids`, and distinct `requester_role = "WATCHER_AUTOMATION"`.
* **Expected Decision**: `OVERRIDE_APPLIED_SUCCESSFULLY` (`override_applied = true`, `final_priority = post_override_priority`, `review_required = false`).
* **Expected Diagnostic**: `GOVERNANCE_OVERRIDE_APPLIED_SUCCESSFULLY`.

### Fixture T5.4: `missing_reason_code_fails_closed`
* **Target Property**: An approved override missing mandatory `reason_code` fails closed under Invariant G3.
* **Input State**: Record with `authorization_state = "APPROVED"`, but `reason_code = null`.
* **Expected Decision**: `FAIL_CLOSED_MISSING_REASON_CODE` (`override_applied = false`, `final_priority = nominal`, `review_required = true`).
* **Expected Diagnostic**: `GOVERNANCE_MISSING_REASON_CODE_REJECTED` (`INV-G3`).

### Fixture T5.5: `empty_evidence_fails_closed`
* **Target Property**: An approved override with empty `evidence_ids: []` fails closed under Invariant G3.
* **Input State**: Record with `authorization_state = "APPROVED"`, valid reason code, but `evidence_ids = []`.
* **Expected Decision**: `FAIL_CLOSED_EMPTY_EVIDENCE` (`override_applied = false`, `final_priority = nominal`, `review_required = true`).
* **Expected Diagnostic**: `GOVERNANCE_EMPTY_EVIDENCE_REJECTED` (`INV-G3`).

### Fixture T5.6: `self_authorization_rejected`
* **Target Property**: An override where `requester_role == authorized_by_role` fails closed under Invariant G4 (no self-authorization).
* **Input State**: Record where both `requester_role` and `authorized_by_role` equal `"SECURITY_LEAD"`.
* **Expected Decision**: `FAIL_CLOSED_SELF_AUTHORIZATION` (`override_applied = false`, `final_priority = nominal`, `review_required = true`).
* **Expected Diagnostic**: `GOVERNANCE_SELF_AUTHORIZATION_REJECTED` (`INV-G4`).

### Fixture T5.7: `malformed_transition_rejected`
* **Target Property**: Direct lifecycle jump from `NOT_REQUESTED` to `APPROVED` without intermediate `REQUESTED` state is rejected.
* **Input State**: Invocation of `transition_authorization_state("NOT_REQUESTED", "APPROVED")`.
* **Expected Decision**: `INVALID_STATE_TRANSITION_REJECTED` (`is_valid = false`, transition rejected).
* **Expected Diagnostic**: `INVALID_STATE_TRANSITION`.

### Fixture T5.8: `nominal_formula_intact`
* **Target Property**: Equation 8 nominal policy calculation is bit-for-bit identical before and after governance pipeline execution.
* **Input State**: Execution of `execute_governance_pipeline()` across a canonical trace.
* **Expected Decision**: `NOMINAL_CALCULATION_UNMODIFIED` (`priority_comparison.nominal_policy_priority == pre_calc nominal priority`).
* **Expected Diagnostic**: Equation 8 weights and calculation unmodified (`INV-G2`, `INV-G6`).

---

## 4. Denominator & Execution Accounting

$$\text{Primary Denominator } (D) = \mathbf{8 \text{ canonical fixtures}}$$
$$\text{Execution Case Count} = \mathbf{8 \text{ cases}}$$

* **Deterministic Construction Rule**: Purely programmatic generation of canonical fixtures; zero random sampling.
* **Target Success Rate**: Formally `null` (exploratory verification suite; no pre-fixed success claims).
* **Held-Out Corpus Isolation**: Access to `validation/article/r6_heldout/*` is **STRICTLY PROHIBITED** during T5.

---

## 5. Epistemological Claim Boundaries

1. **No Claims of Ground Truth**:
   Verification of governance overrides confirms process auditability, traceability, and invariant conformance; it does **not** validate that human decisions reflect objective technical truth or optimal risk decisions.
2. **No Claim of Human Expert Adjudication**:
   These fixtures test contract logic using synthetic role tokens; they do **not** constitute an empirical study of human consensus or operational expert review.
3. **No Claim of Predictive Superiority**:
   Governance overrides document human operational interventions and do not demonstrate superior vulnerability remediation outcomes.
