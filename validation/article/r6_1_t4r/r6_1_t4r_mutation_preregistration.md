# R6.1-T4R Mutation Testing Preregistration
## Versioned Rerun on Validated Canonical Schema v2 Parents

* **Primary Experiment ID**: `R6.1-T4R-PRIMARY`
* **Companion Experiment ID**: `R6.1-T4R-NF2R-COMPANION`
* **Protocol Version**: R6.1
* **Protocol Deviation ID**: `R6-DEV-002` (`POST_RESULT_CHANGE` with `PRE_RESULT_CLARIFICATION`)
* **Status**: `PREREGISTERED_NOT_EXECUTED`
* **Specification Freeze**: `090ad8b727e674aac8e95864fe7740b15092ea60`
* **Implementation Freeze**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
* **Parent Manifest**: [`validation/article/r6_1_t4r/r6_1_t4r_parent_manifest.json`](file:///D:/AntiG/cvss/validation/article/r6_1_t4r/r6_1_t4r_parent_manifest.json)
* **Parent Count**: Exactly 15 validated Schema v2-compliant historical traces
* **Expected Detection Rate**: `null`
* **Target Success Rate**: `null`
* **Held-Out Quarantine**: `LOCKED_UNACCESSED` (`held_out_allowed = false`)

---

## 1. Scientific Architecture: Separation of Primary and Companion Campaigns

To ensure strict methodological rigor and prevent denominator ambiguity, the R6.1-T4R evaluation is partitioned into two distinct, unmerged campaigns:

1. **`R6.1-T4R-PRIMARY`**:
   - Evaluates the **exact 6 original mutation families** ($NF_1$–$NF_6$) from the frozen T4 preregistration on the 15 certified Schema v2-valid canonical parents.
   - **Primary Denominator**: Exactly $15 \text{ parents} \times 6 \text{ families} = \mathbf{90 \text{ applicable mutants}}$.
   - $NF_2$ remains in the primary campaign without retrospective adjustment.
2. **`R6.1-T4R-NF2R-COMPANION`**:
   - Evaluates the companion operator $NF_2\text{-R}$ formulated post-result to isolate core subobject extension injection ([Spec §5.3](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md#L173)).
   - **Companion Denominator**: Exactly $15 \text{ parents} \times 1 \text{ operator} = \mathbf{15 \text{ applicable mutants}}$.
   - Classified as an exploratory post-result companion hypothesis.
3. **Prohibition of Combined Primary Rate**:
   - The 15 companion evaluations shall **never** be combined with the 90 primary evaluations to produce a single primary mutation detection rate.
   - Any consolidated display must be explicitly designated as `DESCRIPTIVE_COMBINED_ONLY`.

---

## 2. Refined Attribution Taxonomy (Mutually Exclusive)

Every mutant evaluation resolves to **exactly one** primary state, guaranteeing that primary category sums equal the denominator:

### 2.1 Primary Attribution State (Mutually Exclusive)
1. **`ATTRIBUTABLE_MUTATION_DETECTION`**:
   - `parent.v2_valid == True`
   - `mutant.v2_valid == False`
   - Primary rejection error matches the intended normative property under test.
2. **`PARENT_INVALID_PRECONDITION_FAILURE`**:
   - `parent.v2_valid == False` (Precondition guard state; verified as 0 by pre-execution validation of all 15 canonical parents).
3. **`ATTRIBUTION_UNRESOLVED`**:
   - `mutant.v2_valid == True` (accepted mutation / contract boundary observation), OR
   - Rejection occurs due to an unclassifiable side-effect.

### 2.2 Orthogonal Diagnostic Flag
* **`mutation_specific_error_additionally_observed`**: `boolean` (`true` / `false`)
  - Evaluated in non-fail-fast (`fail_fast=False`) multi-error diagnostics to confirm that the specific structural assertion corresponding to the mutated path was triggered.

---

## 3. Preregistered Mutation Families

### 3.1 Primary Campaign ($NF_1$–$NF_6$, $N=90$)
1. **`NF1`** (`extension_unnamespaced_key_injection`):
   - Injects unnamespaced key into `extensions`.
   - Expected Category: `INVALID_EXTENSION_NAMESPACE`.
2. **`NF2`** (`core_field_shadowing_in_extensions`):
   - Injects `custom_audit:cvss_b_score: 1.0` into `extensions`.
   - Evaluated as an extension boundary observation (namespaced keys permitted without shadow collision checks in frozen validator).
3. **`NF3`** (`reserved_architectural_keyword_injection`):
   - Injects `formula_override: {"bypass_eq8": true}` at root.
   - Expected Category: `RESERVED_FIELD`.
4. **`NF4`** (`nested_array_item_undeclared_property`):
   - Injects undeclared property `kernel_enforced: true` into `compensating_controls[0]`.
   - Expected Category: `UNKNOWN_FIELD`.
5. **`NF5`** (`explicit_null_on_non_nullable_scalar`):
   - Sets non-nullable scalar `environmental_evidence.asset_class = null`.
   - Expected Category: `INVALID_TYPE`.
6. **`NF6`** (`schema_downgrade_header_injection`):
   - Injects `$schema` header into root.
   - Expected Category: `UNKNOWN_FIELD`.

### 3.2 Companion Subexperiment ($NF_2\text{-R}$, $N=15$)
* **`NF2-R`** (`core_subobject_extension_attribute_injection`):
  - Injects namespaced attribute `vendor:telemetry_hook` directly into `environmental_evidence` ([Spec §5.3](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md#L173)).
  - Expected Category: `UNKNOWN_FIELD`.

---

## 4. Denominator & Corpus Accounting

$$\begin{aligned}
\text{Total Historical Scenarios Examined} &= 30 \\
\text{Certified Schema v2-Valid Canonical Parents} &= 15 \\
\text{Uncanonicalizable Scenarios (Excluded)} &= 15 \ (\text{ambiguous enums 'restricted' / 'defer'}) \\
\mathbf{\text{Primary Denominator}} \ (NF_1\text{--}NF_6) &= 15 \times 6 = \mathbf{90 \text{ mutants}} \\
\mathbf{\text{Companion Denominator}} \ (NF_2\text{-R}) &= 15 \times 1 = \mathbf{15 \text{ mutants}}
\end{aligned}$$
