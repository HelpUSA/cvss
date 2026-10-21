# R6-T5 Execution Plan: Governance Override Contract Verification
## Test Suite: `TEST-SUITE-R6-T5-GOVERNANCE-CONTRACT`

* **Status**: `PREREGISTERED_NOT_EXECUTED`
* **Execution Authorization**: `PENDING_FUTURE_SUPERVISOR_ORDER`
* **Parent Contract**: [`validation/article/r6_t5/r6_t5_governance_fixture_contract.json`](file:///D:/AntiG/cvss/validation/article/r6_t5/r6_t5_governance_fixture_contract.json)
* **Fixture Set**: [`validation/article/r6_t5/r6_t5_governance_fixtures.json`](file:///D:/AntiG/cvss/validation/article/r6_t5/r6_t5_governance_fixtures.json)
* **Target Module**: [`core/r6_governance_override.py`](file:///D:/AntiG/cvss/core/r6_governance_override.py)
* **Held-Out Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`)

---

## 1. Execution Pipeline Overview

When officially dispatched by technical order, the execution runner shall execute the following deterministic, offline verification pipeline:

### 1.1 Phase 1: Pre-Execution Guard
1. Verify presence and SHA-256 integrity of [`core/r6_governance_override.py`](file:///D:/AntiG/cvss/core/r6_governance_override.py).
2. Ingest and parse [`validation/article/r6_t5/r6_t5_governance_fixtures.json`](file:///D:/AntiG/cvss/validation/article/r6_t5/r6_t5_governance_fixtures.json), verifying that exactly 8 fixtures are loaded with zero schema violations.
3. Assert that Equation 8 nominal policy calculator function is accessible and unmodified.

### 1.2 Phase 2: Fixture Evaluation ($N = 8$)
Execute each of the 8 canonical fixtures sequentially against the frozen implementation:
* **T5.1**: Evaluate `evaluate_governance_override()` with `override_requested = false`. Assert `override_applied == False`, `final_priority == 'LOW'`.
* **T5.2**: Evaluate with `authorization_state = 'REQUESTED'`. Assert `override_applied == False`, `final_priority == 'MEDIUM'`, `review_required == True`.
* **T5.3**: Evaluate with `authorization_state = 'APPROVED'`, valid role, reason, and evidence. Assert `override_applied == True`, `final_priority == 'MEDIUM'`.
* **T5.4**: Evaluate approved override with `reason_code = null`. Assert `override_applied == False`, `final_priority == 'HIGH'`, `review_required == True`, `INV-G3` triggered.
* **T5.5**: Evaluate approved override with `evidence_ids = []`. Assert `override_applied == False`, `final_priority == 'MEDIUM'`, `review_required == True`, `INV-G3` triggered.
* **T5.6**: Evaluate with `requester_role == authorized_by_role`. Assert `override_applied == False`, `final_priority == 'LOW'`, `review_required == True`, `INV-G4` triggered.
* **T5.7**: Evaluate `transition_authorization_state('NOT_REQUESTED', 'APPROVED')`. Assert `(False, error)` returned with `INVALID_STATE_TRANSITION`.
* **T5.8**: Execute `execute_governance_pipeline()` across a canonical trace. Assert nominal calculation matches raw Eq. 8 calculation and weights are unmodified (`INV-G2`, `INV-G6`).

### 1.3 Phase 3: Deterministic Parity Rerun
Re-execute all 8 fixtures in a second independent pass in memory and require 100% bitwise/data-structure match across all recorded evaluation fields.

### 1.4 Phase 4: Artifact Generation
Emit all test outputs into `validation/article/r6_t5/`:
1. `r6_t5_governance_results.json`
2. `r6_t5_governance_summary.md`
3. `SHA256SUMS_T5_RESULTS.txt`

---

## 2. Denominator Accounting & Reporting Isolation

$$\text{Primary Denominator } (D) = \mathbf{8 \text{ canonical fixtures}}$$

* **Reporting Mandate**: Results from T5 shall be reported in their own dedicated results block and registry section.
* **No Merging**: T5 results measure governance contract conformance and must **never** be aggregated with Schema v2 mutation detection rates ($N=90$, $N=15$).
* **Target Success Rate**: Formally `null` (exploratory verification suite; no pre-fixed success claims).

---

## 3. Strict Scientific Guardrails
* **Held-Out Quarantine**: Zero query, file-open, or reference to `validation/article/r6_heldout/*`.
* **Formula Immutability**: Equation 8 weights and calculation are strictly nominal and invariant.
* **No Autonomous Overrides**: Automatic overrides are strictly prohibited by Invariant G5.
