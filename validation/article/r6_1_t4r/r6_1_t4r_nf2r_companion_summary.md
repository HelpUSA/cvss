# R6.1-T4R Companion Subexperiment: Execution & Attribution Summary
## Experiment: `R6.1-T4R-NF2R-COMPANION` ($N = 15$)

* **Experiment Type**: Post-Result Companion Subexperiment (Formulated post-T4 to isolate Spec §5.3)
* **Protocol Version**: R6.1
* **Protocol Deviation**: `R6-DEV-002`
* **Execution Timestamp**: `2026-10-21T19:05:58.845637+00:00`
* **Parent Corpus**: Exactly 15 certified Schema v2-compliant canonical traces
* **Tested Operator**: `NF2-R` (`core_subobject_extension_attribute_injection`)
* **Target Structural Path**: `root.environmental_evidence.vendor:telemetry_hook`
* **Normative Property**: Core normative subobjects are closed-world containers and strictly prohibit direct injection of vendor-namespaced extension attributes (Spec §5.3)
* **Companion Denominator**: Exactly 15 parents × 1 operator = 15 applicable mutants
* **Combined Rate Prohibition**: STRICTLY ENFORCED (Companion results must NEVER be merged into a 105 denominator)
* **Deterministic Rerun Parity**: **PASS** (100% data-structure match)
* **Held-Out Quarantine**: **PRESERVED** (`held_out_accessed = false`)

---

## 1. Aggregate Companion Metrics ($D = 15$)

| Metric Category | Count | Percentage of Companion Denominator ($N=15$) |
| :--- | :---: | :---: |
| **Total Companion Mutants** | **15** | **100.0%** |
| **Mutated Inputs Rejected** | **15** | **100.0%** |
| **Mutated Inputs Accepted** | **0** | **0.0%** |
| **Attributable Mutation Detections** | **15** | **100.0%** |
| **Parent Precondition Failures** | **0** | **0.0%** |
| **Attribution Unresolved** | **0** | **0.0%** |
| **Boundary Behavior Observed** | **0** | **0.0%** |

---

## 2. Diagnostic & Error Analysis

* **Primary Error Category**: `UNKNOWN_FIELD` in 15 / 15 cases (100.0%).
* **Primary Error Message**: `Undeclared property 'vendor:telemetry_hook' in closed-world object EnvironmentalEvidence`
* **Primary Error Path**: `root.environmental_evidence.vendor:telemetry_hook`
* **Attribution Alignment**: 100% of rejected mutants triggered the exact expected error category on the mutated path, confirming unambiguous causal detection under closed-world validation.

---

## 3. Scientific Relationship to Original NF2 Boundary

1. **Original NF2 Operator**:
   - Location: Injected into `root.extensions` (`root.extensions.custom_audit:cvss_b_score: 1.0`).
   - Outcome: 15 / 15 accepted under valid parents (boundary behavior of open extension point).
   - Finding: Confirms that namespaced extension attributes are permitted in `extensions` without cross-container shadow collision checks in the frozen validator.
2. **Companion NF2-R Operator**:
   - Location: Injected directly into core normative subobject `environmental_evidence`.
   - Outcome: 15 / 15 rejected and attributable (`UNKNOWN_FIELD`).
   - Finding: Confirms that closed-world schema enforcement strictly confines extensions to `root.extensions` and rejects extension attributes injected into core subobjects.
3. **No Retrospective Blending**:
   The two operators test fundamentally distinct structural scopes. They are reported under separate denominators ($D_{\text{primary}} = 90$, $D_{\text{companion}} = 15$) and must not be aggregated into a single consolidated detection rate.

---

## 4. Epistemological Boundaries & Methodological Claims

1. **No Completeness or Proof Claims**:
   The companion experiment evaluates a single targeted hypothesis on 15 canonical traces; it does not constitute a proof of universal schema security.
2. **Post-Result Formulation**:
   $NF_2$-R was designed after observing the original $NF_2$ boundary and is explicitly classified as an exploratory companion evaluation, not a pre-hoc primary hypothesis.
3. **No External Generalization**:
   Findings apply exclusively to the frozen IEEE R6 Schema v2 contract.
4. **No Environmental Ground Truth**:
   Syntactic rejection of undeclared fields does not validate the semantic or physical efficacy of real-world environmental controls.
