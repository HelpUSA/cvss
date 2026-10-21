# R6-A1 Experiment T4: Mutation Family Preregistration
## Schema v2 Novel Mutation Families (Closed-World Contract Testing)

* **Experiment ID**: `R6-T4-SCHEMA-V2-MUTATION-CAMPAIGN`
* **Protocol Version**: R6.1
* **Status**: `PREREGISTERED_NOT_EXECUTED`
* **Parent Specification Freeze**: `090ad8b727e674aac8e95864fe7740b15092ea60`
* **Parent Implementation Freeze**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
* **Parent T3 Freeze**: `c77599be1ceac1cd39d9e552eb51196cbe427f5e`
* **Held-Out Quarantine**: `LOCKED_UNACCESSED` (`held_out_allowed = false`)
* **Expected Detection Rate**: `null` (strictly prohibited prior to execution)
* **Target Success Rate**: `null` (strictly prohibited prior to execution)
* **Execution State**: `NOT_EXECUTED`

---

## 1. Scientific Objective
The objective of Experiment T4 is to evaluate the normative Schema v2 closed-world structural contract against **novel mutation families** specifically designed to test structural boundaries introduced in Schema v2 that were **not** evaluated by the historical randomized mutation families $F_1$–$F_9$ (from the R3/R5/T3 campaigns).

Experiment T4 does not aim to demonstrate a preconceived 100% detection rate. Instead, it measures the exact runtime enforcement boundaries of the frozen validator ([`core/r6_schema_v2_validator.py`](file:///D:/AntiG/cvss/core/r6_schema_v2_validator.py)) on deep object boundaries, namespaced extension safety, reserved keyword prevention, null-vs-missing distinctions, and schema version downgrades.

---

## 2. Derivation Baseline & Epistemological Boundaries
In strict compliance with HelpUS research governance:
1. **Derivation Source**: Families are derived **exclusively** from:
   - [`validation/article/r6_schema_v2_specification.md`](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md)
   - [`validation/article/r6_schema_v2_contract.json`](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_contract.json)
   - [`validation/article/r6_governance_override_specification.md`](file:///D:/AntiG/cvss/validation/article/r6_governance_override_specification.md)
   - [`validation/article/r6_r6_1_test_plan.md`](file:///D:/AntiG/cvss/validation/article/r6_r6_1_test_plan.md)
   - [`core/r6_schema_v2_validator.py`](file:///D:/AntiG/cvss/core/r6_schema_v2_validator.py) (read-only architectural structural reference).
2. **Prohibited Derivation Bases**:
   - Zero derivation from historical T3 execution outcomes ($120/120$).
   - Zero derivation from T2/T2R exploratory runs.
   - Zero access to or inspiration from the quarantined held-out corpus (`validation/article/r6_heldout/*`).
   - Zero optimization against validator branch conditions.

---

## 3. Preregistered Novel Mutation Families (NF1–NF6)

### Family NF1: Unnamespaced or Malformed Key in Extension Point
* **Family ID**: `NF1`
* **Title**: `extension_unnamespaced_key_injection`
* **Normative Property Under Test**: Trace extensions must strictly conform to vendor-namespaced syntax `^[a-z0-9_]{3,30}:[a-z0-9_]{2,50}$` under `TraceRoot.extensions` ([Spec §5.2](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md#L170)).
* **Source Spec Section**: `r6_schema_v2_specification.md` §5.2 (`TraceExtensionPoint`).
* **Mutation Operator**: Injects an un-namespaced bare key (e.g. `"unprefixed_telemetry": true`) or invalid namespace delimiter (e.g. `"bad/vendor:metric": 1`) into `extensions`.
* **Valid Source-Input Precondition**: Valid `TraceRoot` object.
* **Deterministic Construction Rule**: Ensure `extensions` dictionary exists; assign `extensions["unprefixed_telemetry_flag"] = "unauthorized_bypass"`.
* **Applicability Rule**: Applicable to all 30 historical canonical scenarios.
* **Expected Validation Stage**: Stage 1 (Closed-World Schema / Extension Integrity).
* **Detection Criterion**: Rejection with `INVALID_EXTENSION_NAMESPACE` or `UNKNOWN_FIELD`.
* **Accepted / Boundary Criterion**: Accepted if extension point permissively allows bare keys.
* **Compatible Error Categories**: `["INVALID_EXTENSION_NAMESPACE", "UNKNOWN_FIELD"]`.
* **Exclusions**: Core subobjects (covered by standard closed-world rejection).
* **Overlap with F1–F9**: `NONE`. (Historical F1–F9 never tested the designated `extensions` point; F3 injected undeclared properties directly into root or `environmental_evidence`).
* **Rationale**: Validates the vendor namespace isolation mechanism designed to support safe extensibility without polluting core trace semantics.

---

### Family NF2: Core Field Shadowing via Extension Point
* **Family ID**: `NF2`
* **Title**: `core_field_shadowing_in_extensions`
* **Normative Property Under Test**: Extension attributes must not duplicate, mirror, or shadow core normative metric keys ([Spec §5.3](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md#L173)).
* **Source Spec Section**: `r6_schema_v2_specification.md` §5.3.
* **Mutation Operator**: Injects a syntactically valid namespaced key whose suffix or body targets a core metric (e.g. `"helpus:cvss_b_score": 0.0` or `"acme_sec:priority_comparison": {...}`).
* **Valid Source-Input Precondition**: Valid `TraceRoot` with declared core metrics.
* **Deterministic Construction Rule**: In `extensions`, inject `"custom_audit:cvss_b_score": 1.0`.
* **Applicability Rule**: Applicable to all 30 historical canonical scenarios.
* **Expected Validation Stage**: Stage 1 (Closed-World Schema / Extension Integrity).
* **Detection Criterion**: Rejection with `UNKNOWN_FIELD`, `INVALID_EXTENSION_NAMESPACE`, or explicit shadowing check failure.
* **Accepted / Boundary Criterion**: Accepted if extension keys are treated strictly as opaque metadata without collision detection.
* **Compatible Error Categories**: `["UNKNOWN_FIELD", "INVALID_EXTENSION_NAMESPACE", "RESERVED_FIELD"]`.
* **Exclusions**: Non-colliding valid domain extensions.
* **Overlap with F1–F9**: `NONE`.
* **Rationale**: Prevents external payload injectors from using the extension mechanism to introduce ambiguous or conflicting scoring claims.

---

### Family NF3: Injection of Reserved Architectural Keywords
* **Family ID**: `NF3`
* **Title**: `reserved_architectural_keyword_injection`
* **Normative Property Under Test**: Forward-reserved architectural keywords (`delta_audit`, `formula_override`, `dynamic_weights`, `runtime_bypass`) are strictly prohibited across all trace scopes ([Spec §4 & §5.4](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md#L175)).
* **Source Spec Section**: `r6_schema_v2_specification.md` §4 (Table) and §5.4.
* **Mutation Operator**: Injects one of the 4 reserved keywords into `TraceRoot` or subobjects.
* **Valid Source-Input Precondition**: Valid `TraceRoot`.
* **Deterministic Construction Rule**: Set `trace["formula_override"] = {"bypass_eq8": true}` at the root level.
* **Applicability Rule**: Applicable to all 30 historical canonical scenarios.
* **Expected Validation Stage**: Stage 1 (Closed-World Schema Validation).
* **Detection Criterion**: Rejection with `RESERVED_FIELD` or `UNKNOWN_FIELD`.
* **Accepted / Boundary Criterion**: Accepted only if parser fails to intercept reserved keywords.
* **Compatible Error Categories**: `["RESERVED_FIELD", "UNKNOWN_FIELD"]`.
* **Exclusions**: Arbitrary non-reserved string keys.
* **Overlap with F1–F9**: `NONE`. (F3 used arbitrary dummy keys like `extra_field_123`; never tested architectural keyword guards).
* **Rationale**: Confirms that reserved protocol keywords are blocked fail-closed to prevent premature or unauthorized execution feature triggers.

---

### Family NF4: Deep Closed-World Violation in Nested Array Elements
* **Family ID**: `NF4`
* **Title**: `nested_array_item_undeclared_property`
* **Normative Property Under Test**: Closed-world property rejection applies recursively to composite array elements (`compensating_controls[i]`, `evidence_links[i]`) and metric containers ([Spec §4.1.C, D, F](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md#L83-L135)).
* **Source Spec Section**: `r6_schema_v2_specification.md` §4.1.C, §4.1.D, §4.1.F.
* **Mutation Operator**: Injects an undeclared property into an array element (`compensating_controls[0]["control_vendor"] = "Acme"`) or into `candidate_modified_metrics["MXP"] = "X"`.
* **Valid Source-Input Precondition**: Valid trace with non-empty `compensating_controls` or `candidate_modified_metrics`.
* **Deterministic Construction Rule**: If `compensating_controls` has items, add `"kernel_enforced": true` to `compensating_controls[0]`; otherwise add `"MXP": "X"` to `candidate_modified_metrics`.
* **Applicability Rule**: Applicable to all 30 historical canonical scenarios.
* **Expected Validation Stage**: Stage 1 (Closed-World Schema Validation).
* **Detection Criterion**: Rejection with `UNKNOWN_FIELD` on the nested item path.
* **Accepted / Boundary Criterion**: Accepted only if closed-world enforcement fails to traverse nested arrays.
* **Compatible Error Categories**: `["UNKNOWN_FIELD", "INVALID_NESTED_OBJECT"]`.
* **Exclusions**: Top-level root or top-level subobject mutations (historical F3).
* **Overlap with F1–F9**: `PARTIAL`. (F3 tested root and first-level `environmental_evidence`; NF4 isolates leaf-node elements inside collections and specialized metric containers).
* **Rationale**: Distinguishes shallow schema validation from comprehensive deep structural schema validation.

---

### Family NF5: Explicit Null on Mandatory Non-Nullable Scalar Field
* **Family ID**: `NF5`
* **Title**: `explicit_null_on_non_nullable_scalar`
* **Normative Property Under Test**: Mandatory non-nullable scalar fields (`asset_class`, `official_or_assigned_cvss_v4_vector`, `base_priority`) must reject explicit `null` literal assignments ([Spec §4 & §4.1](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md#L47-L80)).
* **Source Spec Section**: `r6_schema_v2_specification.md` §4 (Table) and §4.1.
* **Mutation Operator**: Replaces mandatory non-nullable scalar value with literal `null`.
* **Valid Source-Input Precondition**: Valid trace with populated non-nullable fields.
* **Deterministic Construction Rule**: Set `environmental_evidence["asset_class"] = None` (literal JSON `null`).
* **Applicability Rule**: Applicable to all 30 historical canonical scenarios.
* **Expected Validation Stage**: Stage 1 (Closed-World Schema Validation).
* **Detection Criterion**: Rejection with `INVALID_TYPE` or `MISSING_REQUIRED_FIELD`.
* **Accepted / Boundary Criterion**: Accepted only if parser silently coerces `null` to empty string or default.
* **Compatible Error Categories**: `["INVALID_TYPE", "MISSING_REQUIRED_FIELD"]`.
* **Exclusions**: Deletion of the property key (which constitutes historical F1). The key must be present with literal `null`.
* **Overlap with F1–F9**: `PARTIAL`. (F1 removed the key; NF5 preserves the key and specifically tests parser null-coercion semantics).
* **Rationale**: Verifies that the schema cleanly enforces the null-vs-missing distinction required for high-assurance data serialization.

---

### Family NF6: Schema Version Confusion / Downgrade Injection
* **Family ID**: `NF6`
* **Title**: `schema_downgrade_header_injection`
* **Normative Property Under Test**: Payloads cannot manipulate schema validation mode or force fallback to open-world v1 parsing via injected version headers or mode flags ([Spec §3, §4.1.A, §8](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md#L30-L46)).
* **Source Spec Section**: `r6_schema_v2_specification.md` §3, §4.1.A, §8.
* **Mutation Operator**: Injects undeclared schema mode override attributes (e.g. `"$schema": "v1"`, `"schema_version": "1.0.0"`, `"validation_mode": "permissive"`).
* **Valid Source-Input Precondition**: Valid `TraceRoot`.
* **Deterministic Construction Rule**: Set `trace["$schema"] = "https://helpus.org/schemas/v1/open_world.json"`.
* **Applicability Rule**: Applicable to all 30 historical canonical scenarios.
* **Expected Validation Stage**: Stage 1 (Closed-World Schema Validation).
* **Detection Criterion**: Rejection with `UNKNOWN_FIELD` (refusing to recognize downgrade headers as valid v2 root properties).
* **Accepted / Boundary Criterion**: Accepted only if validator dynamically switches to v1 open-world mode and allows extraneous fields.
* **Compatible Error Categories**: `["UNKNOWN_FIELD", "INVALID_TYPE"]`.
* **Exclusions**: Legitimate v2 headers if officially specified in contract.
* **Overlap with F1–F9**: `NONE`.
* **Rationale**: Protects the verification pipeline against protocol confusion and downgrade attacks attempting to bypass closed-world validation.

---

## 4. Adversarial Self-Review & Excluded Candidate Families

| Candidate ID | Proposed Concept | Adversarial Evaluation | Status | Rationale for Exclusion |
| :--- | :--- | :--- | :--- | :--- |
| **`EXC-1`** | Invalid Enum in Modified Metrics | Corrupting metric values (e.g. `MAV: "INVALID"`) | `EXCLUDED_FROM_T4` | Redundant with historical F4 (type corruption) and F9 (token flips); represents trivial unit test coverage rather than novel v2 structural boundary. |
| **`EXC-2`** | Numeric Score Out of Range | Setting `cvss_b_score: 11.5` | `EXCLUDED_FROM_T4` | Redundant with historical F7/F8 numeric perturbation operators. |
| **`EXC-3`** | Malformed CVSS Vector String | Corrupting prefix `CVSS:4.0/` | `EXCLUDED_FROM_T4` | Tested extensively by FIRST reference scoring engine; does not evaluate Schema v2 closed-world structural governance. |

---

## 5. Denominator Rule & Input Firewall

### 5.1 Denominator Rule
* **Corpus**: Complete historical canonical corpus of **30 scenarios**:
  - 12 NVD-derived scenarios: `SCN-NVD-001` through `SCN-NVD-012`
  - 18 Synthetic expert scenarios: `SCN-SYN-013` through `SCN-SYN-030`
* **Families**: 6 novel families ($NF_1$ through $NF_6$).
* **Construction**: Exactly 1 deterministic mutant per scenario per family.
* **Total Applicable Denominator**:
  $$\text{Denominator} = 30 \text{ scenarios} \times 6 \text{ families} = 180 \text{ applicable mutants}$$
* **Exhaustive Application**: Zero down-sampling, zero stochastic selection, zero heuristic filtering.
* **No Retrospective Retuning**: The denominator is fixed at 180 prior to execution.

### 5.2 Input Firewall
* **Quarantined Materials**: `validation/article/r6_heldout/*` is strictly prohibited.
* **Authorized Inputs**: Exclusively pre-R6 historical/controlled canonical traces.
* **Confirmation**: `held_out_allowed = false`, `held_out_accessed = false`.

---

## 6. Pre-Registration Change Control
* Any alteration to family definitions, operators, or applicability prior to execution must be recorded as a `PRE_RESULT_CHANGE` in the protocol deviation log.
* Any modification following the observation of T4 execution results must be classified as a `POST_RESULT_CHANGE` and flagged in publication manifests.
* Silent modifications are strictly prohibited.
