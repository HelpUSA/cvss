# R6-T6 Preregistration: Historical NVD Representability Check
## Test Suite: `TEST-SUITE-R6-T6-NVD-REPRESENTABILITY`

* **Document Version**: 1.0.0
* **Protocol Version**: R6.1
* **Research Question Linkage**: **RQ-R6-3** (*"Uma camada estruturada de governance override pode tornar os desvios operacionais auditáveis sem modificar a política nominal da Eq. 8?"*)
* **Execution Status**: `PREREGISTERED_NOT_EXECUTED`
* **Parent Plan Section**: [`validation/article/r6_r6_1_test_plan.md §2 (T6)`](file:///D:/AntiG/cvss/validation/article/r6_r6_1_test_plan.md)
* **Contract Specification**: [`validation/article/r6_t6/r6_t6_nvd_representability_contract.json`](file:///D:/AntiG/cvss/validation/article/r6_t6/r6_t6_nvd_representability_contract.json)
* **Case Set**: [`validation/article/r6_t6/r6_t6_nvd_representability_cases.json`](file:///D:/AntiG/cvss/validation/article/r6_t6/r6_t6_nvd_representability_cases.json)
* **Target Modules**:
  * [`core/r6_schema_v2_validator.py`](file:///D:/AntiG/cvss/core/r6_schema_v2_validator.py) (Schema v2 closed-world validation)
  * [`core/r6_governance_override.py`](file:///D:/AntiG/cvss/core/r6_governance_override.py) (Governance override encapsulation)
  * [`core/cvss40_environmental_policy.py`](file:///D:/AntiG/cvss/core/cvss40_environmental_policy.py) (Equation 8 nominal calculation)
* **Target Success Rate**: Formally `null` (exploratory representability study; no pre-fixed success claims).
* **Expected Success Rate**: Formally `null`.
* **Held-Out Corpus Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`)

---

## 1. Scientific Motivation & Context

During the R5 validation campaign, 4 out of 12 NVD scenarios exhibited operational deviations between nominal formula output (Equation 8) and curated practitioner annotations:
1. `SCN-NVD-001` (CVE-2026-4251): Nominal `MEDIUM` vs Practitioner `LOW`
2. `SCN-NVD-003` (CVE-2026-4270): Nominal `HIGH` vs Practitioner `HIGH` (with non-standard exposure `restricted`)
3. `SCN-NVD-007` (CVE-2026-29513): Nominal `CRITICAL` vs Practitioner `MEDIUM` (-2 delta operational suppression)
4. `SCN-NVD-011` (CVE-2026-4224): Nominal `HIGH` vs Practitioner `HIGH` (with non-standard exposure `restricted`)

In traditional vulnerability management, such discrepancies are either hidden, patched into scoring algorithms via post-hoc heuristic weights, or left in informal narrative footnotes. 

Under the IEEE R6 protocol, **Equation 8 remains strictly nominal and mathematically invariant**. Test Suite T6 investigates whether the structured Schema v2 and Governance Override contracts can faithfully represent, encapsulate, and audit these 4 real-world operational deviations without:
1. Mutating Equation 8 weights or calculation logic;
2. Inventing missing semantic information not present in the original evidence;
3. Retuning reason codes post hoc to force a cosmetic 30/30 agreement.

---

## 2. Operational Definition of Representability

Representability is evaluated under a strict, mutually exclusive four-state taxonomy:

1. **`REPRESENTABLE_DIRECTLY`**:
   The historical trace conforms directly to Schema v2 and the governance contract without requiring any structural conversion or field transformations.
2. **`REPRESENTABLE_BY_NORMATIVE_STRUCTURAL_TRANSFORMATION`**:
   The trace can be brought into complete conformance with Schema v2 and the governance contract via deterministic, rule-based structural wrapping (e.g., converting legacy delimited strings into arrays of structured control/link items) **without adding, altering, or inventing substantive semantic facts**.
3. **`NOT_REPRESENTABLE_WITHOUT_NEW_INFORMATION`**:
   The trace violates a closed-world contract rule (such as an un-enumerated enum value like `restricted`) and cannot be resolved without making an ungrounded substantive choice that would invent new architectural information.
4. **`REPRESENTABILITY_AMBIGUOUS_UNDER_FROZEN_CONTRACT`**:
   The frozen specification contains competing or contradictory rules that prevent deterministic classification under the existing contract.

> [!IMPORTANT]
> **Distinction of Concepts**:
> * **Schema Validity**: Syntactic conformance to JSON schema constraints.
> * **Representability**: Expressive capability of the data model to capture operational reality without information loss or invention.
> * **Semantic Ground Truth**: Objective correctness of human operational decisions (which T6 does not evaluate).

---

## 3. Case-Level Preconditions and Criteria ($N = 4$)

### Case T6.1: `SCN-NVD-001` (CVE-2026-4251)
* **Operational Characteristic**: Operational downgrade from Eq. 8 nominal `MEDIUM` ($s=2$) to practitioner `LOW` ($s=1$).
* **Structural Issue**: Legacy narrative controls and links are formatted as strings.
* **Governance Issue**: Requires formal governance override record (`pre_override_priority = "MEDIUM"`, `post_override_priority = "LOW"`, `reason_code = "CONTROL_COMPENSATION"` or `"DOCUMENTED_ENVIRONMENTAL_EXCEPTION"`).
* **Information Invention Prohibition**: Prohibited from modifying base CVSS metrics or adding non-existent network protections.
* **Semantic Preservation Criterion**: Compensating control text must be preserved verbatim in structured items.

### Case T6.2: `SCN-NVD-003` (CVE-2026-4270)
* **Operational Characteristic**: High-criticality identity provider component.
* **Structural Issue**: `internet_exposure` is `"restricted"`, outside Schema v2 closed-world enum `['public', 'dmz', 'internal', 'isolated']`.
* **Governance Issue**: Operational priority (`HIGH`) matches nominal policy (`HIGH`).
* **Information Invention Prohibition**: Coercing `"restricted"` to `"dmz"` or `"internal"` without explicit network topology evidence in the trace is strictly prohibited.
* **Semantic Preservation Criterion**: Identity component trust boundary must remain intact.

### Case T6.3: `SCN-NVD-007` (CVE-2026-29513)
* **Operational Characteristic**: Strong operational suppression (-2 delta) from nominal `CRITICAL` ($s=4$) to practitioner `MEDIUM` ($s=2$).
* **Structural Issue**: Legacy controls and links formatted as strings.
* **Governance Issue**: Two-level governance override record (`pre_override_priority = "CRITICAL"`, `post_override_priority = "MEDIUM"`, `reason_code = "EXPOSURE_CONTEXT_EXCEPTION"` or `"CONTROL_COMPENSATION"`).
* **Information Invention Prohibition**: Prohibited from altering OT telemetry monitoring definitions or claiming external connectivity.
* **Semantic Preservation Criterion**: OT telemetry segmentation context must be preserved verbatim.

### Case T6.4: `SCN-NVD-011` (CVE-2026-4224)
* **Operational Characteristic**: Identity integration component with 4 distinct evidence URI links.
* **Structural Issue**: `internet_exposure` is `"restricted"` and narrative links contain semicolon-delimited URLs.
* **Governance Issue**: Nominal policy (`HIGH`) matches operational priority (`HIGH`).
* **Information Invention Prohibition**: Fabricating deployment tier to bypass closed-world enum is strictly barred.
* **Semantic Preservation Criterion**: All 4 URI references must be preserved without loss.

---

## 4. Denominator & Execution Accounting

$$\text{Primary Scientific Denominator } (D) = \mathbf{4 \text{ historical NVD cases}}$$
$$\text{Execution Checks Count} = \mathbf{12 \text{ verification checks}} \quad (4 \text{ cases} \times 3 \text{ dimensions})$$

### The Three Verification Dimensions per Case:
1. **Schema v2 Conformance**: Evaluates syntactic and closed-world structural validity.
2. **Governance Encapsulation**: Evaluates override record completeness, role separation, and reason codes.
3. **Equation 8 Invariance**: Asserts that Equation 8 nominal calculation is computed identically before and after governance processing.

---

## 5. Epistemological Claim Boundaries

1. **No Target Claim of Full Representability**:
   No target of 4/4 representability is claimed. Cases requiring new information (`NOT_REPRESENTABLE_WITHOUT_NEW_INFORMATION`) will be reported honestly as authentic contract boundary findings.
2. **No Claim of Human Expert Adjudication**:
   Evaluation relies strictly on machine-checkable contract rules and historical R5 documents. Human expert adjudication remains formally `NOT_COMPLETED`.
3. **Equation 8 Formula Immutability**:
   Equation 8 weights and calculation logic remain 100% untouched.
4. **Held-Out Quarantine**:
   Access to `validation/article/r6_heldout/*` is strictly barred throughout T6.
