# R6-T7 Held-Out Corpus Transfer Experiment Summary
## Suite: `TEST-SUITE-R6-T7-HELDOUT-TRANSFER` (`R6-T7-HELDOUT`)
### Research Question: `RQ-R6-1`

* **Execution Status**: `COMPLETED_UNFROZEN`
* **First Access Timestamp**: `2026-10-21T23:03:31.460895+00:00`
* **Preregistration Freeze Commit**: `978694618574a8962e5dc8b6c0111bc792110685`
* **Prerequisite R2 Commit**: `32407259b9e8b07f84316c5057bf885ec29e8e8f`
* **Corpus Denominator**: $N = 938$ eligible public advisories (September 2026 window).
* **Two-Pass Determinism**: **PASS** (100% bit-for-bit parity).
* **Held-Out Accessed**: `true`.
* **Human Adjudication Completed**: `false` (invariable).
* **Target Rate / Expected Rate**: `null` (exploratory empirical transfer study).

---

### Primary Outcome Counts ($N = 938$)

| Primary Outcome Category | Count (Run 1) | Count (Run 2) | Proportion | Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| `SCHEMA_V2_VALID_NOMINAL_CALCULABLE` | 339 | 339 | 36.1407% | Native published CVSS v4.0 vector present; Eq. 8 nominal calculated |
| `MISSING_MANDATORY_EVIDENCE_REJECTED` | 599 | 599 | 63.8593% | Lacks published CVSS v4.0 vector; rejected without information invention |
| `SCHEMA_V2_VALID_GOVERNANCE_OVERRIDE_DOCUMENTED` | 0 | 0 | 0.00% | No raw public advisory embeds governance overrides |
| `SCHEMA_V2_STRUCTURAL_INVALIDITY_REJECTED` | 0 | 0 | 0.00% | Zero syntax corruption detected in public JSON schema |
| `INSUFFICIENT_INFORMATION_UNRESOLVED` | 0 | 0 | 0.00% | All non-v4 records deterministic fail-closed under missing evidence |
| `EXECUTION_OR_ENVIRONMENT_ERROR` | 0 | 0 | 0.00% | Zero runtime execution errors |
| **Total Processed** | **938** | **938** | **100.00%** | **Denominator Sum Check: PASS** |

---

### Machine-Checkable Trace Verification
* `TRACE_VERIFICATION_PASS`: **938** (100.00%)
* `TRACE_VERIFICATION_FAIL`: **0** (0.00%)
* Total Diagnostic Checks Executed: **3232** (clearly distinct from population denominator $N = 938$).
