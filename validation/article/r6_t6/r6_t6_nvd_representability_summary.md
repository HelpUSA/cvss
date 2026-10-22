# R6-T6 Canonical Summary: Historical NVD Representability Check
## Test Suite: `TEST-SUITE-R6-T6-NVD-REPRESENTABILITY` ($N = 4$)

* **Status**: `COMPLETED_UNFROZEN`
* **Research Question**: `RQ-R6-3`
* **Execution Timestamp**: `2026-10-21T20:11:44Z`
* **Preregistration Freeze**: `5a6c8c67088a8ed26e2cbf91a5e3317ceffb2925`
* **Implementation Freeze**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
* **Primary Scientific Denominator**: $D = 4$ canonical historical NVD cases
* **Execution Checks Count**: 12 verification checks (4 cases $\times$ 3 checks)
* **Deterministic Rerun Parity**: `PASS` (Run 1 bit-for-bit identical to Run 2)
* **Held-Out Corpus Quarantine**: `UNTOUCHED` (`held_out_accessed = false`)
* **Equation 8 Nominal Formula Invariance**: `PRESERVED` (`Eq8_modified = false`)
* **Human Adjudication**: `NOT_PERFORMED` (`human_adjudication_completed = false`)

---

## 1. Executive Summary & Taxonomy Distribution

The T6 experiment evaluated the representability of the 4 historical NVD operational deviation cases from R5 under the frozen Schema v2 and Governance Override contracts. The evaluation strictly followed the preregistered 4-category taxonomy with zero information invention.

| Classification Category | Count ($N=4$) | Percentage | Spec Interpretation |
| :--- | :---: | :---: | :--- |
| **`REPRESENTABLE_DIRECTLY`** | **0** | **0.0%** | Legacy R5 v1 traces lack structured composite arrays for controls and evidence links. |
| **`REPRESENTABLE_BY_NORMATIVE_STRUCTURAL_TRANSFORMATION`** | **2** | **50.0%** | Full Schema v2 closed-world validity achieved via deterministic array-wrapping without data mutation. Operational deviation cleanly encapsulated via `GovernanceOverrideRecord`. |
| **`NOT_REPRESENTABLE_WITHOUT_NEW_INFORMATION`** | **2** | **50.0%** | Legacy exposure token `'restricted'` is outside Schema v2 closed-world enum. Resolving this would require inventing unverified network topology context. |
| **`REPRESENTABILITY_AMBIGUOUS_UNDER_FROZEN_CONTRACT`** | **0** | **0.0%** | Zero ambiguous classifications; all cases map deterministically to mutually exclusive categories. |
| **Total Evaluated** | **4** | **100.0%** | Sum of categories matches primary denominator exactly ($0 + 2 + 2 + 0 = 4$). |

---

## 2. Denominator Accounting & Reporting Isolation

$$\text{Primary Denominator } (D) = \mathbf{4 \text{ historical NVD cases}}$$

* **Strict Isolation**: These 4 representability evaluations measure structural and governance expressiveness. In accordance with strict methodological governance, they are **never** aggregated with mutation detection rates ($N=90$, $N=15$) or synthetic fixture unit tests ($N=8$).
* **Target Success Rate**: Formally documented as `null` (exploratory representability study).
* **Expected Success Rate**: Formally documented as `null`.

---

## 3. Case Synthesis & Findings

| Case ID | Source Scenario | CVE ID | Asset Class | Internet Exposure | Nominal Eq. 8 | Practitioner | Primary Classification | Governance Reason Code |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **T6.1** | `SCN-NVD-001` | CVE-2026-4251 | `public_web_application` | `public` | `MEDIUM` | `LOW` | `REPRESENTABLE_BY_NORMATIVE_STRUCTURAL_TRANSFORMATION` | `CONTROL_COMPENSATION` |
| **T6.2** | `SCN-NVD-003` | CVE-2026-4270 | `identity_provider` | `restricted` (out-of-enum) | `HIGH` | `HIGH` | `NOT_REPRESENTABLE_WITHOUT_NEW_INFORMATION` | N/A (Enum Gap) |
| **T6.3** | `SCN-NVD-007` | CVE-2026-29513 | `ot_monitoring_gateway` | `internal` | `CRITICAL` | `MEDIUM` | `REPRESENTABLE_BY_NORMATIVE_STRUCTURAL_TRANSFORMATION` | `EXPOSURE_CONTEXT_EXCEPTION` |
| **T6.4** | `SCN-NVD-011` | CVE-2026-4224 | `identity_provider` | `restricted` (out-of-enum) | `HIGH` | `HIGH` | `NOT_REPRESENTABLE_WITHOUT_NEW_INFORMATION` | N/A (Enum Gap) |

### Key Scientific Insights:
1. **Separation of Policy Ground Truth from Operational Discretion**: For cases T6.1 and T6.3, the frozen Governance Override contract successfully decoupled the nominal mathematical scoring of Equation 8 from human practitioner operational downgrades. Equation 8 remained 100% nominal and bit-for-bit invariant while full audit trails (`CONTROL_COMPENSATION`, `EXPOSURE_CONTEXT_EXCEPTION`) were formally generated.
2. **Honest Closed-World Enforcement**: Cases T6.2 and T6.4 highlight that Schema v2 closed-world enumeration strictly rejects unverified legacy tokens (`'restricted'`). The system refuses to fabricate network topology assumptions (`information_invention_allowed = false`), documenting an empirical boundary where external deployment information is mandatory.
3. **Cross-Consistency with T4R Parent Canonicalization**: The findings are 100% congruent with the T4R parent canonicalization specification: `SCN-NVD-001` and `SCN-NVD-007` were successfully canonicalized in T4R, whereas `SCN-NVD-003` and `SCN-NVD-011` were classified as uncanonicalizable without new information.

---

## 4. Epistemological Claim Boundaries

1. **No Retrospective Retuning**:
   The $2/4$ transformable and $2/4$ unrepresentable outcome is reported factually. No post-hoc enum additions or relaxation of closed-world validation rules were performed.
2. **No Claim of Autonomous Ground Truth Remediation**:
   Demonstrating representability confirms schema expressiveness; it does not prove that practitioner operational downgrades were objectively optimal or correct.
3. **No Claim of Human Expert Adjudication**:
   Governance override records evaluated in T6 verify contract state mechanics and role-based audit fields; they do not represent real-time human expert adjudication (`human_adjudication_completed: false`).
4. **Equation 8 Immutability**:
   Equation 8 was not altered, reweighted, or bypassed in any manner (`eq8_modified: false`).
