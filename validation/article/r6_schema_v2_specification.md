# R6 Schema v2 Specification (Closed-World Contract)

## 1. Specification Status & Metadata
* **Document Version**: 2.0.0
* **Status**: `SPECIFIED_NOT_IMPLEMENTED`
* **Parent Preregistration Commit**: `c0b4025d9f560b8e525accd17e1b075cd23a355b`
* **Held-Out Lock Commit**: `12bf6c456054656a1bbc198d7e3729d2675098b2`
* **Base Commit (Working Head)**: `2346859b319eac9146273b215eca796147816837`
* **Anti-Retuning Lock**: `LOCKED_PRIOR_TO_IMPLEMENTATION_AND_TESTS`
* **Implementation State**: `NOT_IMPLEMENTED`
* **Tests Executed**: `false`
* **Results Available**: `false`

---

## 2. Design Goal
The primary objective of **Schema v2** is to make explicit the machine-checkable structural contract governing vulnerability evidence traces and verification inputs. Under Schema v2, undeclared attributes, arbitrary subobject injections, and undocumented fields are rejected where semantically appropriate by enforcing deterministic closed-world policies across the entire schema hierarchy.

Crucially, Schema v2 is designed as an independent experimental hypothesis for Phase R6. It **does not rewrite, retroactively alter, or invalidate** historical experimental baselines, including the R5 open-world verification results.

---

## 3. Versioning and Schema Hierarchy
1. **Schema v1 (Historical Baseline)**:
   - Defined under open-world JSON parsing conventions.
   - Preserves historical fidelity of R2–R5 experimental campaigns.
   - Retains the exact empirical result of Mutation Family F3 (subobject/attribute injection: 0/16 rejected, 16/16 accepted) as a valid finding demonstrating open-world contract boundaries.
2. **Schema v2 (R6 Closed-World Candidate)**:
   - Formally restricts input trace objects to declared properties, well-typed fields, validated enums, bounded ranges, and explicit extension points.
   - Does **not** replace Schema v1 retroactively in existing frozen manifests or publications.
3. **Change Control**:
   - Any modification to this normative specification following its initial cryptographic commit requires a logged protocol deviation in `validation/article/r6_a1_protocol_deviation_log.md`.
   - Any post-result change prompted by empirical test observations must be formally classified as `POST_RESULT_CHANGE` and disclosed in publication artifacts.

---

## 4. Object-by-Object Closed-World Policy
Rather than relying solely on a blanket `additionalProperties: false` directive at the root level, Schema v2 applies an explicit, object-by-object policy across all structural components of the trace schema:

| Structural Component | Schema Classification | Undeclared Fields Behavior | Missing Field Behavior | Null Value Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **`TraceRoot`** | `CLOSED_WORLD_REQUIRED` | `REJECT` (`UNKNOWN_FIELD`) | `REJECT` if required; default if optional | `REJECT` for mandatory objects |
| **`EnvironmentalEvidence`** | `CLOSED_WORLD_REQUIRED` | `REJECT` (`UNKNOWN_FIELD`) | `REJECT` if required | `REJECT` on non-nullable scalar fields |
| **`CompensatingControlItem`** | `CLOSED_WORLD_REQUIRED` | `REJECT` (`UNKNOWN_FIELD`) | `REJECT` (`MISSING_REQUIRED_FIELD`) | `REJECT` |
| **`EvidenceLinkItem`** | `CLOSED_WORLD_REQUIRED` | `REJECT` (`UNKNOWN_FIELD`) | `REJECT` (`MISSING_REQUIRED_FIELD`) | `REJECT` |
| **`CandidateEnvironmentalAssessment`** | `CLOSED_WORLD_REQUIRED` | `REJECT` (`UNKNOWN_FIELD`) | `REJECT` if required | `REJECT` |
| **`CandidateModifiedMetrics`** | `CLOSED_WORLD_REQUIRED` | `REJECT` (`UNKNOWN_FIELD`) | Optional fields default to `X` | `REJECT` |
| **`PriorityComparison`** | `CLOSED_WORLD_REQUIRED` | `REJECT` (`UNKNOWN_FIELD`) | `REJECT` (`MISSING_REQUIRED_FIELD`) | `REJECT` |
| **`GovernanceOverrideRecord`** | `CLOSED_WORLD_REQUIRED` | `REJECT` (`UNKNOWN_FIELD`) | Coherent with authorization state | Nullable only when override not applied |
| **`TraceExtensionPoint` (`extensions`)**| `OPEN_EXTENSION_POINT_ALLOWED` | `ACCEPT_WITH_NAMESPACING` | Optional (default empty object) | Allowed if explicit null |
| **`ReservedKeywords` (`delta_audit`, etc.)**| `RESERVED_FOR_FUTURE_VERSION` | `REJECT` (`RESERVED_FIELD`) | N/A (prohibited) | `REJECT` |

### 4.1 Detailed Object Specifications

#### A. `TraceRoot` (`CLOSED_WORLD_REQUIRED`)
* **Permitted Fields**:
  - `scenario_id`: `string` (required, pattern: `^(SCN-(NVD|SYN)-\d{3}|GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4})$`)
  - `scenario_source`: `string` (required, enum: `["nvd_cvss_v4_with_curated_environment", "synthetic_expert_scenario", "github_advisory_database_reviewed"]`)
  - `cve_id`: `string` or `null` (optional, pattern: `^CVE-\d{4}-\d{4,}$`)
  - `official_or_assigned_cvss_v4_vector`: `string` (required, valid CVSS v4.0 vector string starting with `CVSS:4.0/`)
  - `cvss_b_score`: `string` or `number` (required, range: `0.0` to `10.0`)
  - `cvss_b_severity`: `string` (required, enum: `["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]`)
  - `environmental_evidence`: `EnvironmentalEvidence` (required)
  - `candidate_environmental_assessment`: `CandidateEnvironmentalAssessment` (required)
  - `priority_comparison`: `PriorityComparison` (required)
  - `governance_override`: `GovernanceOverrideRecord` (optional, default omitted)
  - `extensions`: `TraceExtensionPoint` (optional, default `{}`)
  - `boundary`: `string` (required, normative boundary statement)
* **Unknown Fields**: Strictly rejected with `UNKNOWN_FIELD`.

#### B. `EnvironmentalEvidence` (`CLOSED_WORLD_REQUIRED`)
* **Permitted Fields**:
  - `asset_class`: `string` (required, non-empty)
  - `deployment_context`: `string` (required, non-empty)
  - `internet_exposure`: `string` (required, enum: `["public", "dmz", "internal", "isolated"]`)
  - `privilege_context`: `string` (required, non-empty)
  - `compensating_controls`: `array` of `CompensatingControlItem` (required, list of objects)
  - `evidence_links`: `array` of `EvidenceLinkItem` (required, list of objects)
  - `evidence_summary`: `string` (required, non-empty string)
* **Unknown Fields**: Strictly rejected with `UNKNOWN_FIELD`.

#### C. `CompensatingControlItem` (`CLOSED_WORLD_REQUIRED`)
* **Permitted Fields**:
  - `control_id`: `string` (required, non-empty)
  - `control_type`: `string` (required, enum: `["network_firewall", "waf", "edr", "segmentation", "mfa", "least_privilege", "rate_limiting", "custom_compensating_control"]`)
  - `status`: `string` (required, enum: `["enforced", "planned", "inactive", "partial"]`)
  - `description`: `string` (optional, default `""`)
* **Unknown Fields**: Strictly rejected with `UNKNOWN_FIELD`.

#### D. `EvidenceLinkItem` (`CLOSED_WORLD_REQUIRED`)
* **Permitted Fields**:
  - `link_id`: `string` (required, non-empty)
  - `uri_or_reference`: `string` (required, non-empty)
  - `confidence`: `string` (required, enum: `["high", "medium", "low", "unverified"]`)
* **Unknown Fields**: Strictly rejected with `UNKNOWN_FIELD`.

#### E. `CandidateEnvironmentalAssessment` (`CLOSED_WORLD_REQUIRED`)
* **Permitted Fields**:
  - `confidentiality_requirement`: `string` (required, enum: `["H", "M", "L", "X"]`)
  - `integrity_requirement`: `string` (required, enum: `["H", "M", "L", "X"]`)
  - `availability_requirement`: `string` (required, enum: `["H", "M", "L", "X"]`)
  - `candidate_modified_metrics`: `CandidateModifiedMetrics` (required)
  - `watcher_recommendation`: `string` (required, non-empty)
  - `uncertainty_flags`: `array` of `string` (required, list of valid string tokens)
  - `human_review_status`: `string` (required, enum: `["required", "completed", "waived", "pending_review"]`)
* **Unknown Fields**: Strictly rejected with `UNKNOWN_FIELD`.

#### F. `CandidateModifiedMetrics` (`CLOSED_WORLD_REQUIRED`)
* **Permitted Fields**:
  - `MAV`: `string` (optional, enum: `["N", "A", "L", "P", "X"]`, default `"X"`)
  - `MAC`: `string` (optional, enum: `["N", "L", "H", "X"]`, default `"X"`)
  - `MAT`: `string` (optional, enum: `["N", "P", "X"]`, default `"X"`)
  - `MPR`: `string` (optional, enum: `["N", "L", "H", "X"]`, default `"X"`)
  - `MUI`: `string` (optional, enum: `["N", "P", "A", "X"]`, default `"X"`)
  - `MVC`: `string` (optional, enum: `["H", "L", "N", "X"]`, default `"X"`)
  - `MVI`: `string` (optional, enum: `["H", "L", "N", "X"]`, default `"X"`)
  - `MVA`: `string` (optional, enum: `["H", "L", "N", "X"]`, default `"X"`)
  - `MSC`: `string` (optional, enum: `["H", "L", "N", "X"]`, default `"X"`)
  - `MSI`: `string` (optional, enum: `["S", "H", "L", "N", "X"]`, default `"X"`)
  - `MSA`: `string` (optional, enum: `["S", "H", "L", "N", "X"]`, default `"X"`)
  - `CR`: `string` (optional, enum: `["H", "M", "L", "X"]`, default `"X"`)
  - `IR`: `string` (optional, enum: `["H", "M", "L", "X"]`, default `"X"`)
  - `AR`: `string` (optional, enum: `["H", "M", "L", "X"]`, default `"X"`)
* **Unknown Fields**: Strictly rejected with `UNKNOWN_FIELD`.

#### G. `PriorityComparison` (`CLOSED_WORLD_REQUIRED`)
* **Permitted Fields**:
  - `base_priority`: `string` (required, enum: `["CRITICAL", "HIGH", "MEDIUM", "LOW"]`)
  - `environmental_priority`: `string` (required, enum: `["CRITICAL", "HIGH", "MEDIUM", "LOW"]`)
  - `priority_delta`: `string` or `number` (required, numeric step difference)
* **Unknown Fields**: Strictly rejected with `UNKNOWN_FIELD`.

---

## 5. Extension Safety and Delimited Extension Points
To prevent arbitrary attribute injection while still accommodating domain-specific extensions, Schema v2 isolates all non-standard attributes into an explicit extension point:
1. **Designated Location**: Extensions are permitted **only** under the top-level property `extensions: {}`.
2. **Namespace Requirement**: Every child key within `extensions` must adhere to an explicit, colon-delimited or underscore-delimited vendor namespace matching regex `^[a-z0-9_]{3,30}:[a-z0-9_]{2,50}$` (e.g., `helpus:telemetry_hook`, `acme_sec:cluster_id`).
3. **Core Subobject Isolation**: No extension attributes are permitted inside core normative subobjects (`environmental_evidence`, `candidate_environmental_assessment`, `priority_comparison`, `governance_override`). Unrecognized properties placed directly in core subobjects are strictly rejected.
4. **Reserved Fields**: Properties named `delta_audit`, `formula_override`, `dynamic_weights`, or `runtime_bypass` are classified as `RESERVED_FOR_FUTURE_VERSION` and rejected with `RESERVED_FIELD` across all scopes.

---

## 6. Backward Compatibility Taxonomy
Inputs originating from Schema v1 systems are deterministically classified under one of four normative compatibility categories:

1. **`V1_VALID_V2_VALID`**:
   - The trace conforms to all Schema v1 requirements and contains strictly declared Schema v2 fields with valid types, enums, and structures.
   - Example: Standard canonical traces SCN-NVD-001 through SCN-SYN-030.
2. **`V1_VALID_V2_INVALID_UNDECLARED_FIELD`**:
   - The trace was valid under Schema v1 due to open-world tolerance of extraneous attributes, but is rejected under Schema v2 due to closed-world enforcement.
   - Example: The 16 F3 subobject/attribute injection mutants from the R3 campaign.
3. **`V1_INVALID_V2_INVALID`**:
   - The trace violates core syntax, missing required fields, or type constraints in both Schema v1 and Schema v2.
   - Example: Mutants with missing required fields (F1) or corrupted enum tokens (F2).
4. **`V1_VALID_V2_VALID_NORMALIZED`**:
   - The trace contains minor structural representations permitted under v1 that resolve deterministically through documented, pre-registered normalizers without coercion (e.g., numeric string score representations parsed to standard decimal format).

---

## 7. F3 Historical Boundary
* **Empirical Baseline**: During the R3 canonical randomized mutation campaign, Mutation Family F3 (attribute and subobject injection) yielded `0/16` rejections (`16/16` accepted) under Schema v1.
* **Normative Principle**: This historical result represents an accurate, reproducible observation of the Schema v1 open-world contract. It is **not** a flaw, an operational defect, or a bug to be retroactively erased.
* **Separation of Claims**: Schema v2 establishes a new closed-world contract to test the experimental hypothesis that strict structural boundaries reject undeclared injections. This specification explicitly forbids claiming pre-implementation success or pre-announcing a 16/16 rejection rate on F3 until Phase R6-2 execution is formally authorized and conducted.

---

## 8. Normalization vs. Schema Validation Boundary
* **Strict Separation of Concerns**: Schema validation evaluates whether an input conforms to structural, typing, and closed-world constraints. Evidence normalization transforms raw external feeds into standardized evidentiary representations.
* **No Silent Coercion**: The normalizer is prohibited from silently stripping undeclared fields, rewriting invalid enums, or masking structural corruption to force an invalid payload to pass Schema v2 validation.
* **Fail-Closed Execution**: If an input payload fails Schema v2 structural validation, execution halts immediately with a deterministic error code prior to policy evaluation, Equation 8 scoring, or governance routing.

---

## 9. Error Contract
Schema v2 validation failures must return machine-readable diagnostics conforming to standardized error categories:

* `UNKNOWN_FIELD`: Property not declared in closed-world object specification.
* `MISSING_REQUIRED_FIELD`: Mandatory property absent from payload.
* `INVALID_TYPE`: Property value does not match defined primitive or composite type.
* `INVALID_ENUM`: Value does not belong to authorized token enumeration.
* `INVALID_RANGE`: Numerical value outside defined boundary `[min, max]`.
* `INVALID_NESTED_OBJECT`: Malformed child object or structure.
* `RESERVED_FIELD`: Attempt to inject reserved or prohibited architectural keywords.
* `INVALID_EXTENSION_NAMESPACE`: Extension property lacking required vendor namespace.

---

## 10. Security and Robustness Motivation & Claim Boundary
Enforcing closed-world structural validation significantly diminishes the attack surface for parser differentials, payload tampering, and spurious field injection.

However, **closed-world validation does not prove semantic correctness, operational safety, or organizational ground truth**. A structurally valid Schema v2 trace may still encapsulate inaccurate environmental assertions, biased human judgments, or incorrect contextual assumptions. Claims of formal verification are strictly restricted to machine-checkable structural adherence.
