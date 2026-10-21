# R6 Governance Override Specification

## 1. Specification Status & Metadata
* **Document Version**: 1.0.0
* **Status**: `SPECIFIED_NOT_IMPLEMENTED`
* **Parent Preregistration Commit**: `c0b4025d9f560b8e525accd17e1b075cd23a355b`
* **Held-Out Lock Commit**: `12bf6c456054656a1bbc198d7e3729d2675098b2`
* **Base Commit (Working Head)**: `2346859b319eac9146273b215eca796147816837`
* **Formula Immutability**: `Eq. 8 strictly nominal; delta_audit absent`
* **Implementation State**: `NOT_IMPLEMENTED`
* **Tests Executed**: `false`
* **Results Available**: `false`

---

## 2. Architectural Position
The Governance Override layer is positioned strictly as an **external post-scoring control boundary**. It operates cleanly downstream of policy computation and does **not** alter, parameterize, or perturb the mathematical formulation of Equation 8.

### Pipeline Flow
```
[Raw Evidence]
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
[Optional Governance Override Layer] ──► (Fail-Closed Gate)
      │
      ├──────────────────────┬──────────────────────┐
      ▼                      ▼                      ▼
[NOT_REQUESTED /       [APPROVED]             [REJECTED]
 REJECTED / INVALID]         │                      │
      │                Authorized Post-       Nominal Preserved
Nominal Preserved      Override Priority      Audit Trail Retained
      │                      │                      │
      └──────────────────────┴──────────────────────┘
                             │
                             ▼
              [Final Authorized Trace Record]
```

Under this architectural separation:
1. Equation 8 computes the nominal environmental priority based strictly on established mathematical weights and input vectors.
2. The nominal output (`nominal_policy_priority`) is irrevocably recorded in the trace.
3. No heuristic correction terms, post-hoc delta functions (e.g., `delta_audit(e)`), or dynamic weight modifiers are introduced into Equation 8.
4. Any deviation from the nominal priority must be mediated through an explicit, auditable, and role-authorized governance record.

---

## 3. Minimum Data Model
The governance override record is represented by the following schema within the trace:

```json
{
  "override_id": "OVR-2026-0001",
  "case_id": "SCN-NVD-001",
  "nominal_policy_priority": "LOW",
  "pre_override_priority": "LOW",
  "post_override_priority": "MEDIUM",
  "override_requested": true,
  "override_applied": true,
  "reason_code": "DOCUMENTED_ENVIRONMENTAL_EXCEPTION",
  "reason_text_optional": "Critical internal segment behind isolating gateway.",
  "evidence_ids": ["EVID-LINK-01", "EVID-LINK-03"],
  "authorization_state": "APPROVED",
  "authorized_by_role": "SECURITY_LEAD",
  "authorization_timestamp": "2026-10-21T12:00:00Z",
  "review_required": false,
  "trace_link": "validation/article/trace/SCN-NVD-001.json",
  "schema_version": "1.0.0"
}
```

### Field Definitions:
* `override_id`: `string` (required, unique identifier matching `^OVR-\d{4}-\d{4,}$`).
* `case_id`: `string` (required, reference to vulnerability trace identifier).
* `nominal_policy_priority`: `string` (required, enum: `["CRITICAL", "HIGH", "MEDIUM", "LOW"]`, exact output of Eq. 8).
* `pre_override_priority`: `string` (required, priority state immediately prior to override application).
* `post_override_priority`: `string` (required, priority state resulting from governance action; identical to nominal if not applied).
* `override_requested`: `boolean` (required, indicates whether an override was formally requested).
* `override_applied`: `boolean` (required, true only if formally authorized and executed).
* `reason_code`: `string` (conditional, required if `override_applied == true`, enum defined in Section 5).
* `reason_text_optional`: `string` or `null` (optional, contextual technical commentary).
* `evidence_ids`: `array` of `string` (conditional, required non-empty array if `override_applied == true`).
* `authorization_state`: `string` (required, enum defined in Section 4).
* `authorized_by_role`: `string` or `null` (conditional, required if approved; role-based token to preserve double-blind review integrity).
* `authorization_timestamp`: `string` or `null` (conditional, ISO 8601 UTC timestamp required if authorized).
* `review_required`: `boolean` (required, true if manual human review remains pending).
* `trace_link`: `string` or `null` (optional, relative path or URI to corresponding trace artifact).
* `schema_version`: `string` (required, semantic version of override contract, e.g., `"1.0.0"`).

---

## 4. Authorization States and Transition Rules
The governance layer defines five mutually exclusive authorization states:

* **`NOT_REQUESTED`**: Default initial state. No governance override has been initiated.
* **`REQUESTED`**: An override request has been logged and accompanied by supporting evidence, awaiting adjudication.
* **`APPROVED`**: An authorized authority has reviewed and approved the override.
* **`REJECTED`**: The override request was formally reviewed and dismissed; nominal priority governs.
* **`SUPERSEDED`**: A previously approved or requested override has been rendered obsolete by newer evidence or re-assessment.

### State Transition Matrix
| Current State | Permitted Next States | Conditions / Requirements |
| :--- | :--- | :--- |
| `NOT_REQUESTED` | `REQUESTED` | Explicit submission with `case_id` and initial proposed priority. |
| `REQUESTED` | `APPROVED` | Valid role authorization, non-empty `evidence_ids`, valid `reason_code`. |
| `REQUESTED` | `REJECTED` | Authority rejects request; explanation recorded, nominal priority retained. |
| `REQUESTED` | `SUPERSEDED` | New evidence arrives or trace is invalidated prior to adjudication. |
| `APPROVED` | `SUPERSEDED` | Subsequent environmental reassessment invalidates previous override. |
| `REJECTED` | `REQUESTED` | Re-opening allowed only upon submission of new, distinct `evidence_ids`. |
| `SUPERSEDED` | None (Terminal) | Archived for audit trail. |

Any transition not explicitly listed above is prohibited and results in an immediate `INVALID_STATE_TRANSITION` error.

---

## 5. Reason Codes Enumeration
To prevent unconstrained or subjective justifications, `reason_code` is strictly constrained to a finite, semantically justified enumeration:

1. **`DOCUMENTED_ENVIRONMENTAL_EXCEPTION`**: A documented, formal enterprise architecture exception modifies baseline exposure assumptions.
2. **`CONTROL_COMPENSATION`**: Verified, active compensating controls (e.g., dedicated hardware air-gapping, validated virtual patching) neutralize the attack vector.
3. **`ASSET_CRITICALITY_EXCEPTION`**: The affected host possesses designated high-criticality or low-criticality business designation overriding generic asset class heuristics.
4. **`EXPOSURE_CONTEXT_EXCEPTION`**: Verified micro-segmentation or perimeter routing prevents remote exploitability despite nominal network vector assignment.
5. **`EVIDENCE_CONFLICT_REQUIRES_REVIEW`**: Contradictory threat intelligence feeds or telemetry inputs require operational prioritization hold pending forensic adjudication.
6. **`OTHER_REQUIRES_DOCUMENTED_JUSTIFICATION`**: Exceptional condition not covered above; requires mandatory non-empty `reason_text_optional` exceeding 30 characters.

---

## 6. Formal Invariants
The governance override layer enforces the following non-negotiable invariants:

* **Invariant G1 (Authorization Prerequisite)**: An override cannot be applied (`override_applied == true`) unless `authorization_state == "APPROVED"` and `authorized_by_role` is populated.
* **Invariant G2 (Nominal Preservation)**: The computed value of Equation 8 must always be preserved intact in `nominal_policy_priority` and must never be overwritten, mutated, or omitted.
* **Invariant G3 (Mandatory Justification)**: If `override_applied == true`, `reason_code` must be a valid enum token and `evidence_ids` must contain at least one valid identifier.
* **Invariant G4 (Separation of Roles / No Self-Authorization)**: An automated watcher, autonomous scorer, or requesting entity cannot authorize its own override request. `authorized_by_role` must represent a distinct governance role.
* **Invariant G5 (No Autonomous Override)**: The core CVSS scorer is strictly prohibited from autonomously triggering, applying, or synthesizing an override without external governance dispatch.
* **Invariant G6 (Eq. 8 Formula Invariance)**: Equation 8 weights ($w_{\text{base}}, w_{\text{context}}, w_{\text{control}}$) and scoring logic remain strictly constant. No dynamic terms (such as `delta_audit`) may be added to the mathematical equation.
* **Invariant G7 (Audit Reproducibility)**: The combination of `nominal_policy_priority`, `reason_code`, `evidence_ids`, and `authorized_by_role` must allow an independent auditor to reconstruct the exact rationale of the decision.

---

## 7. Human Authorization & Double-Blind Representation
* **Architectural Constraint**: Human authorization is established as an architectural requirement for applying priority overrides in production.
* **Double-Blind Protection**: In compliance with scientific double-blind peer review requirements, authorization records use role-based descriptors (`SECURITY_LEAD`, `MASTER_SUPERADMIN`, `INCIDENT_COMMANDER`) rather than identifiable personal names or email addresses.
* **Status Claim Boundary**: This specification mandates human authorization as a technical prerequisite. However, **it does not assert or claim that comprehensive empirical human validation of all scenarios has been completed**. Where human review is pending, `review_required` must remain `true`.

---

## 8. Handling of Historical R5 NVD Deviations
During the R5 validation campaign, 4 out of 12 NVD scenarios exhibited operational deviations between nominal formula output and curated practitioner annotations.

* **Methodological Role**: These 4 historical cases may be used during Phase R6 testing solely as representability test fixtures to confirm that the governance override data structure can faithfully encapsulate and audit such deviations.
* **Prohibition Against Overfitting**: The reason codes, state transitions, and constraints defined in this specification have been drafted based on general security engineering principles. They **must not** be reverse-engineered or retrofitted to force a synthetic 30/30 reproduction on the R5 dataset. Achieving 30/30 nominal agreement is explicitly **not** an objective or success criterion of the specification.

---

## 9. Fail-Closed Behavior
Any governance override payload that is malformed, missing mandatory fields, failing invariant checks, or lacking valid authorization must fail closed:
1. `override_applied` remains `false`.
2. `post_override_priority` remains strictly equal to `nominal_policy_priority`.
3. `review_required` is set to `true`.
4. A deterministic error log entry is emitted into the verification trace.
5. In no circumstance does a malformed override silently alter the operational priority.

---

## 10. Claim Boundary
The governance override specification provides **process auditability, traceability, and accountability** for security triage decisions. It formalizes *who* authorized an exception, *why*, and on what *evidence*.

It **does not prove that an authorized human judgment was technically optimal, free from operational bias, or reflective of objective ground truth**. Scientific claims must remain strictly confined to verification contract enforcement.
