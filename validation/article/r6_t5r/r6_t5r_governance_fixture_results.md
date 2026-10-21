# R6.1-T5R Canonical Fixture Results Matrix
## Test Suite: `TEST-SUITE-R6-T5R-GOVERNANCE-CONTRACT` ($N = 8$)

* **Protocol Version**: R6.1 (`R6-DEV-003`, `POST_RESULT_CHANGE`)
* **Execution Timestamp**: `2026-10-21T19:44:24.656786+00:00`
* **Preregistration Freeze**: `5c9b918a5a16d22e0ad5ef3981d84925de931fca`
* **Implementation Freeze**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`

---

## Fixture Evaluation Matrix ($D = 8$)

| Fixture ID | Source T5 ID | Fixture Title | Nominal Priority | Actual Governance Decision | Final Authorized Priority | Override Applied | Status | Failure / Diagnostic Note |
| :---: | :---: | :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| `T5R.1` | `T5.1` | override_not_requested | `LOW` | `NOMINAL_PRESERVED` | `LOW` | `False` | **PASS** | — |
| `T5R.2` | `T5.2` | requested_not_approved | `MEDIUM` | `UNAUTHORIZED_REQUEST_REJECTED` | `MEDIUM` | `False` | **PASS** | — |
| `T5R.3` | `T5.3` | approved_valid_override | `LOW` | `OVERRIDE_APPLIED_SUCCESSFULLY` | `MEDIUM` | `True` | **PASS** | — |
| `T5R.4` | `T5.4` | missing_reason_code_fails_closed | `HIGH` | `FAIL_CLOSED_MISSING_REASON_CODE` | `HIGH` | `False` | **PASS** | — |
| `T5R.5` | `T5.5` | empty_evidence_fails_closed | `MEDIUM` | `FAIL_CLOSED_EMPTY_EVIDENCE` | `MEDIUM` | `False` | **PASS** | — |
| `T5R.6` | `T5.6` | self_authorization_rejected | `LOW` | `FAIL_CLOSED_SELF_AUTHORIZATION` | `LOW` | `False` | **PASS** | — |
| `T5R.7` | `T5.7` | malformed_transition_rejected | `MEDIUM` | `INVALID_STATE_TRANSITION_REJECTED` | `MEDIUM` | `False` | **PASS** | — |
| `T5R.8` | `T5.8` | nominal_formula_intact | `MEDIUM` | `NOMINAL_CALCULATION_UNMODIFIED` | `HIGH` | `True` | **PASS** | — |

---

## Technical Notes per Fixture

* **T5R.1 (`override_not_requested`)**: Confirms that when no override is initiated, nominal priority governs without review requirements.
* **T5R.2 (`requested_not_approved`)**: Confirms that pending or rejected requests fail closed to nominal and flag human review.
* **T5R.3 (`approved_valid_override`)**: Confirms full audit trail generation and clean priority transition when all formal prerequisites are satisfied.
* **T5R.4 (`missing_reason_code_fails_closed`)**: Confirms Invariant G3 enforcement when mandatory reason code is absent.
* **T5R.5 (`empty_evidence_fails_closed`)**: Confirms Invariant G3 enforcement when supporting evidence IDs array is empty.
* **T5R.6 (`self_authorization_rejected`)**: Confirms Invariant G4 enforcement preventing autonomous agents or individuals from self-authorizing overrides.
* **T5R.7 (`malformed_transition_rejected`)**: Confirms lifecycle state transition enforcement rejecting invalid jumps.
* **T5R.8 (`nominal_formula_intact`)**: Confirms Invariant G2 and G6 enforcement: Equation 8 nominal policy calculation is intact ('MEDIUM') and authorized override applies cleanly.
