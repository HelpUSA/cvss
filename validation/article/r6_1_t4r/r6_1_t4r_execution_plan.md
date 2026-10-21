# R6.1-T4R Execution Plan: Valid-Parent Mutation Rerun

* **Primary Experiment ID**: `R6.1-T4R-PRIMARY`
* **Companion Experiment ID**: `R6.1-T4R-NF2R-COMPANION`
* **Status**: `PREREGISTERED_NOT_EXECUTED`
* **Execution Authorization**: `PENDING_FUTURE_SUPERVISOR_ORDER`
* **Parent Contract**: [`validation/article/r6_1_t4r/r6_1_t4r_contract.json`](file:///D:/AntiG/cvss/validation/article/r6_1_t4r/r6_1_t4r_contract.json)
* **Parent Manifest**: [`validation/article/r6_1_t4r/r6_1_t4r_parent_manifest.json`](file:///D:/AntiG/cvss/validation/article/r6_1_t4r/r6_1_t4r_parent_manifest.json)

---

## 1. Execution Protocol Overview
When officially authorized by technical order, the execution runner shall execute the following partitioned pipeline:

### 1.1 Phase 1: Primary Campaign ($N = 90$)
1. Ingest the 15 certified Schema v2-compliant parents from [`validation/article/r6_1_t4r/canonical_parents/`](file:///D:/AntiG/cvss/validation/article/r6_1_t4r/canonical_parents/).
2. Re-verify in-memory that all 15 parents yield `valid == True` under `validate_trace_v2()`.
3. Apply each of the 6 primary mutation operators ($NF_1$–$NF_6$) deterministically across all 15 parents, producing exactly $15 \times 6 = 90$ mutants.
4. Submit each mutant to `validate_trace_v2()` under both `fail_fast=True` (nominal) and `fail_fast=False` (diagnostic).
5. Categorize each primary evaluation into the mutually exclusive states:
   - `ATTRIBUTABLE_MUTATION_DETECTION`
   - `PARENT_INVALID_PRECONDITION_FAILURE`
   - `ATTRIBUTION_UNRESOLVED`

### 1.2 Phase 2: Companion Subexperiment ($N = 15$)
1. Apply the companion operator $NF_2\text{-R}$ across the same 15 certified parents, producing exactly $15 \times 1 = 15$ companion mutants.
2. Submit each companion mutant to `validate_trace_v2()`.
3. Report companion results in a completely separate results block.

---

## 2. Denominator Accounting & Reporting Isolation

$$\begin{aligned}
\mathbf{\text{Primary Denominator}} \ (NF_1\text{--}NF_6) &= 15 \times 6 = \mathbf{90 \text{ applicable mutants}} \\
\mathbf{\text{Companion Denominator}} \ (NF_2\text{-R}) &= 15 \times 1 = \mathbf{15 \text{ applicable mutants}}
\end{aligned}$$

* **Reporting Directive**: The primary mutation detection rate shall be computed strictly with denominator $D = 90$. The companion result shall be reported strictly with denominator $D = 15$. Under no circumstance shall a consolidated rate (e.g. out of 105) be presented as the primary detection outcome.

---

## 3. Strict Scientific Guardrails
* **No Retrospective Tuning**: If $NF_2$ yields `ATTRIBUTION_UNRESOLVED` (boundary acceptance), it must be reported factually without code modifications.
* **Held-Out Quarantine**: Zero reference to `validation/article/r6_heldout/*`.
* **Historical Baseline Fidelity**: Original T4 artifacts in `validation/article/r6_t4/` remain permanently frozen.
