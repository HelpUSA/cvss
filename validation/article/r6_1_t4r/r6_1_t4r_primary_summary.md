# R6.1-T4R Primary Campaign: Execution & Attribution Summary
## Experiment: `R6.1-T4R-PRIMARY` ($N = 90$)

* **Protocol Version**: R6.1
* **Protocol Deviation**: `R6-DEV-002` (Clarified Denominators)
* **Execution Timestamp**: `2026-10-21T18:56:51.208592+00:00`
* **Preregistration Commit**: `d89656d929dd6a784c604a944ef33b57f5978f47`
* **Denominator Clarification Commit**: `83d8996b5377f0a531648aee7a747cfda1d2f782`
* **Parent Corpus**: Exactly 15 certified Schema v2-compliant canonical traces
* **Primary Families**: 6 original families ($NF_1$–$NF_6$)
* **Companion Subexperiment ($NF_2$-R)**: NOT EXECUTED in this order (`PREREGISTERED_NOT_EXECUTED`)
* **Combined Rate Prohibition**: STRICTLY ENFORCED (Primary denominator $D = 90$, no combined 105 rate)
* **Deterministic Rerun Parity**: **PASS** (100% data-structure match)
* **Held-Out Quarantine**: **PRESERVED** (`held_out_accessed = false`)

---

## 1. Aggregate Execution Metrics ($D = 90$)

| Metric Category | Count | Percentage of Primary Denominator ($N=90$) |
| :--- | :---: | :---: |
| **Total Applicable Mutants** | **90** | **100.0%** |
| **Mutated Inputs Rejected** | **75** | **83.3%** |
| **Mutated Inputs Accepted (Boundary)** | **15** | **16.7%** |
| **Attributable Mutation Detections** | **75** | **83.3%** |
| **Parent Precondition Failures** | **0** | **0.0%** |
| **Attribution Unresolved** | **15** | **16.7%** |

> [!NOTE]
> **Attribution Rule & Distinction**:
> `Mutated input rejection rate` measures raw non-conformance detection (83.3%).
> `Attributable mutation detection rate` requires both rejection and normative diagnostic evidence match (83.3%).
> In this primary evaluation, every rejected mutant triggered the exact expected error category, yielding perfect alignment between raw rejection and attributable detection for all rejecting families ($NF_1, NF_3, NF_4, NF_5, NF_6$).

---

## 2. Per-Family Breakdown

| Family ID | Family Name | Generated | Rejected | Accepted | Attributable Detections | Unresolved / Boundary | Primary Error Category |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **NF1** | `extension_unnamespaced_key_injection` | 15 | 15 | 0 | 15 | 0 | `INVALID_EXTENSION_NAMESPACE` (15/15) |
| **NF2** | `core_field_shadowing_in_extensions` | 15 | 0 | 15 | 0 | 15 | None (Boundary Accepted: 15/15) |
| **NF3** | `reserved_architectural_keyword_injection` | 15 | 15 | 0 | 15 | 0 | `RESERVED_FIELD` (15/15) |
| **NF4** | `nested_array_item_undeclared_property` | 15 | 15 | 0 | 15 | 0 | `UNKNOWN_FIELD` (15/15) |
| **NF5** | `explicit_null_on_non_nullable_scalar` | 15 | 15 | 0 | 15 | 0 | `INVALID_TYPE` (15/15) |
| **NF6** | `schema_downgrade_header_injection` | 15 | 15 | 0 | 15 | 0 | `UNKNOWN_FIELD` (15/15) |
| **Total** | **All 6 Families** | **90** | **75** | **15** | **75** | **15** | — |

---

## 3. Specific Analysis of Family NF2 ($N = 15$)

Family $NF_2$ (`core_field_shadowing_in_extensions`) injected `custom_audit:cvss_b_score: 1.0` into the `extensions` dictionary across all 15 valid canonical parents.

* **Outcome**: 15/15 mutants were **ACCEPTED** by the frozen Schema v2 validator (`mutant_v2_valid = True`).
* **Attribution Classification**: Classified strictly as `ATTRIBUTION_UNRESOLVED` with `boundary_behavior_observed = True`.
* **Root Cause & Contract Boundary**:
  As specified in [Spec §5.2](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md#L158), `root.extensions` is an open extension point that permits vendor-namespaced keys conforming to `^[a-z0-9_]{3,30}:[a-z0-9_]{2,50}$`. The frozen validator does not enforce cross-dictionary shadow collision checking against core metric names within the open extension container.
* **Anti-Retuning Compliance**:
  In accordance with anti-retuning guardrails, the validator was **not** retrospectively tuned to reject these mutants. The finding is documented factually as an observed contract boundary. The companion operator $NF_2$-R (which injects into closed core subobjects) remains segregated in its own companion preregistration.

---

## 4. Epistemological Boundaries & Methodological Claims

1. **No Claims of Completeness or Proof**:
   This experiment provides empirical evidence on a controlled evaluation corpus of 15 canonical traces and 90 synthesized mutants; it does not constitute formal verification or a mathematical proof of total schema correctness.
2. **No Statistical Sampling Inference**:
   The 15 canonical traces represent a deterministic, purposive historical benchmark, not an independently and identically distributed (i.i.d.) statistical sample. No population-level hypothesis testing is inferred.
3. **No External Generalization Claim**:
   Results reflect the specific contractual boundaries of the IEEE R6 closed-world schema specification and cannot be generalized to arbitrary enterprise telemetry formats without empirical validation.
4. **No Environmental Ground Truth Claim**:
   Schema validation certifies syntactic and structural compliance; it does not validate the physical correctness of real-world environmental controls.
