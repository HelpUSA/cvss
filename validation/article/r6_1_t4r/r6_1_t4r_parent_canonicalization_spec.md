# R6.1-T4R Specification: Deterministic Parent Canonicalization

* **Protocol Version**: R6.1
* **Protocol Deviation Reference**: `R6-DEV-002` (`POST_RESULT_CHANGE`)
* **Objective**: Establish a deterministically canonicalized baseline of historical scenarios that satisfy Schema v2 structural constraints prior to mutation injection, eliminating confounding from pre-existing parent invalidity.

---

## 1. Principles of Canonicalization
1. **Zero Retrospective Optimization**: Canonicalization rules are derived exclusively from the normative specification ([`validation/article/r6_schema_v2_specification.md`](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md)) and the structural gaps identified in T2/T2R.
2. **Semantic Non-Interference**: Canonicalization preserves all nominal Equation 8 inputs, asset classifications, and operational priority comparisons.
3. **No Invention of Information**: If a scenario contains attributes that cannot be unambiguously mapped to Schema v2 enums without fabricating context (e.g. `internet_exposure = 'restricted'` or `environmental_priority = 'defer'`), it is classified as `PARENT_CANONICALIZATION_NOT_POSSIBLE_WITHOUT_NEW_INFORMATION` and excluded from the T4R evaluation denominator.

---

## 2. Canonicalization Rules Applied

| Field Path | Original Historical Format | Canonicalized Schema v2 Format | Spec Justification | Information Preserved |
| :--- | :--- | :--- | :--- | :--- |
| `root.cve_id` | Empty string `""` in synthetic scenarios | Literal `null` | Spec §4.1.A (`cve_id: string or null`) | Reflects absence of CVE ID without inventing arbitrary IDs |
| `environmental_evidence.compensating_controls` | Flat narrative string (e.g. `"WAF active"`) | Array of `CompensatingControlItem` (`control_id`, `control_type`, `status: "enforced"`, `description`) | Spec §4.1.C | 100% of the narrative string preserved in `description` |
| `environmental_evidence.evidence_links` | Semicolon-delimited URL string | Array of `EvidenceLinkItem` (`link_id`, `uri_or_reference`, `confidence: "high"`) | Spec §4.1.D | Exact original URLs preserved |
| `candidate_environmental_assessment.{CR, IR, AR}` | Narrative string with prefix (e.g. `"CR:H - confidentiality is high..."`) | Standard single-letter enum token (`"H"`, `"M"`, `"L"`, `"X"`) | Spec §4.1.E | Metric letter requirement parsed directly from prefix |
| `candidate_environmental_assessment.uncertainty_flags` | String token (e.g. `"NONE"`) | Array of string tokens (`[]` if `"NONE"`) | Spec §4.1.E | Array typing enforced |
| `candidate_environmental_assessment.candidate_modified_metrics` | String representation | Dictionary of neutral modified metrics (`"X"`) | Spec §4.1.F | Valid composite container instantiated |
| `priority_comparison.base_priority`, `environmental_priority` | Lowercase strings (`"low"`, `"medium"`, etc.) | Uppercase enum tokens (`"LOW"`, `"MEDIUM"`, `"HIGH"`, `"CRITICAL"`) | Spec §4.1.G | Casing normalized without semantic shift |
| `root.extensions` | Omitted | Initialized empty dictionary `{}` | Spec §5.1 | Valid extension point |

---

## 3. Canonicalization Corpus Breakdown

* **Total Historical Scenarios Examined**: 30
* **Successfully Canonicalized to `v2_valid = True`**: **15**
  - NVD Scenarios (7): `SCN-NVD-001`, `SCN-NVD-004`, `SCN-NVD-006`, `SCN-NVD-007`, `SCN-NVD-008`, `SCN-NVD-009`, `SCN-NVD-012`
  - Synthetic Scenarios (8): `SCN-SYN-015`, `SCN-SYN-016`, `SCN-SYN-017`, `SCN-SYN-020`, `SCN-SYN-023`, `SCN-SYN-024`, `SCN-SYN-025`, `SCN-SYN-028`
* **Uncanonicalizable without New Information**: **15**
  - 12 Scenarios with `internet_exposure = 'restricted'`: `SCN-NVD-002`, `003`, `005`, `010`, `011`, `SCN-SYN-013`, `018`, `019`, `021`, `026`, `027`, `029`
  - 3 Scenarios with `environmental_priority = 'defer'`: `SCN-SYN-014`, `022`, `030`
* **Frozen T4R Denominator**:
  $$\text{Denominator T4R} = 15 \text{ valid canonical parents} \times 6 \text{ mutation families} = 90 \text{ applicable mutants}$$
