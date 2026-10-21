# R6.1-T4R Mutation Testing Preregistration
## Versioned Rerun on Validated Canonical Schema v2 Parents

* **Experiment ID**: `R6.1-T4R-VALID-PARENT-MUTATION-RERUN`
* **Protocol Version**: R6.1
* **Protocol Deviation ID**: `R6-DEV-002` (`POST_RESULT_CHANGE`)
* **Status**: `PREREGISTERED_NOT_EXECUTED`
* **Specification Freeze**: `090ad8b727e674aac8e95864fe7740b15092ea60`
* **Implementation Freeze**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
* **Parent Manifest**: [`validation/article/r6_1_t4r/r6_1_t4r_parent_manifest.json`](file:///D:/AntiG/cvss/validation/article/r6_1_t4r/r6_1_t4r_parent_manifest.json)
* **Parent Count**: Exactly 15 validated Schema v2-compliant historical traces
* **Expected Detection Rate**: `null`
* **Target Success Rate**: `null`
* **Held-Out Quarantine**: `LOCKED_UNACCESSED` (`held_out_allowed = false`)

---

## 1. Scientific Purpose & Hypotheses
Following Auditorial Order `CMD-CVSS-IEEE-R6-A1-T4-ATTRIBUTION-AUDIT-258`, Experiment T4R reruns the novel Schema v2 mutation campaign on a certified baseline of 15 canonicalized historical traces that are 100% valid under Schema v2 prior to mutation.

By guaranteeing `parent.v2_valid == True`, T4R resolves the causal confounding observed in T4 and provides an unambiguous measurement of runtime mutation-kill.

---

## 2. Refined Attribution Taxonomy (Mutually Exclusive)

To eliminate reporting overlap, T4R defines a strict, partition-based attribution model:

### 2.1 Primary Attribution State (Mutually Exclusive — Sums Exactly to Denominator)
Every mutant evaluation resolves to **exactly one** primary state:
1. **`ATTRIBUTABLE_MUTATION_DETECTION`**:
   - `parent.v2_valid == True`
   - `mutant.v2_valid == False`
   - Primary rejection error matches the intended normative property under test.
2. **`PREEXISTING_PARENT_INVALIDITY`**:
   - `parent.v2_valid == False`
   - (By design in T4R, this state will be $0$ because all 15 parents are certified v2-valid prior to injection).
3. **`ATTRIBUTION_UNRESOLVED`**:
   - `mutant.v2_valid == True` (accepted mutation / contract boundary observation), OR
   - Rejection occurs due to an unclassifiable side-effect.

### 2.2 Orthogonal Diagnostic Flag
* **`mutation_specific_error_additionally_observed`**: `boolean` (`true` / `false`)
  - Evaluated in non-fail-fast (`fail_fast=False`) multi-error diagnostics to confirm that the specific structural assertion corresponding to the mutated path was triggered.

---

## 3. Preregistered Mutation Families

T4R preserves the exact operator definitions from the original T4 preregistration:

1. **`NF1`** (`extension_unnamespaced_key_injection`):
   - Injects unnamespaced key into `extensions`.
   - Expected Rejection: `INVALID_EXTENSION_NAMESPACE`.
2. **`NF2`** (`core_field_shadowing_in_extensions`):
   - Injects `custom_audit:cvss_b_score: 1.0` into `extensions`.
   - Evaluated as a contract boundary finding (the current validator permits namespaced keys without shadow collision checking).
3. **`NF2-R`** (`core_subobject_extension_attribute_injection` - Diagnostic Companion):
   - Injects namespaced attribute `vendor:telemetry_hook` directly into `environmental_evidence`, evaluating Spec §5.3 (prohibition of extension attributes inside core subobjects).
   - Expected Rejection: `UNKNOWN_FIELD`.
4. **`NF3`** (`reserved_architectural_keyword_injection`):
   - Injects `formula_override: {"bypass_eq8": true}` at root.
   - Expected Rejection: `RESERVED_FIELD`.
5. **`NF4`** (`nested_array_item_undeclared_property`):
   - Injects undeclared property `kernel_enforced: true` into `compensating_controls[0]`.
   - Expected Rejection: `UNKNOWN_FIELD`.
6. **`NF5`** (`explicit_null_on_non_nullable_scalar`):
   - Sets non-nullable scalar `environmental_evidence.asset_class = null`.
   - Expected Rejection: `INVALID_TYPE`.
7. **`NF6`** (`schema_downgrade_header_injection`):
   - Injects `$schema` header into root.
   - Expected Rejection: `UNKNOWN_FIELD`.

---

## 4. Denominator & Input Corpus
* **Corpus**: 15 certified v2-valid canonical parents (`validation/article/r6_1_t4r/canonical_parents/*.json`).
* **Families**: 6 primary families ($NF_1$–$NF_6$).
* **Total Primary Denominator**:
  $$\text{Denominator T4R} = 15 \times 6 = 90 \text{ applicable mutants}$$
* If $NF_2\text{-R}$ is evaluated alongside as a 7th diagnostic family, the extended evaluation comprises $15 \times 7 = 105$ mutants.
