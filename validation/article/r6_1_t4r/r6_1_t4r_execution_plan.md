# R6.1-T4R Execution Plan: Valid-Parent Mutation Rerun

* **Experiment ID**: `R6.1-T4R-VALID-PARENT-MUTATION-RERUN`
* **Status**: `PREREGISTERED_NOT_EXECUTED`
* **Execution Authorization**: `PENDING_FUTURE_SUPERVISOR_ORDER`
* **Parent Contract**: [`validation/article/r6_1_t4r/r6_1_t4r_contract.json`](file:///D:/AntiG/cvss/validation/article/r6_1_t4r/r6_1_t4r_contract.json)
* **Parent Manifest**: [`validation/article/r6_1_t4r/r6_1_t4r_parent_manifest.json`](file:///D:/AntiG/cvss/validation/article/r6_1_t4r/r6_1_t4r_parent_manifest.json)

---

## 1. Execution Protocol Overview
When officially authorized by technical order, the execution runner shall:
1. Load the 15 certified Schema v2-compliant parents from [`validation/article/r6_1_t4r/canonical_parents/`](file:///D:/AntiG/cvss/validation/article/r6_1_t4r/canonical_parents/).
2. Re-verify in-memory that each parent evaluates to `valid == True` under [`core/r6_schema_v2_validator.py`](file:///D:/AntiG/cvss/core/r6_schema_v2_validator.py).
3. Apply each of the 6 primary mutation operators ($NF_1$–$NF_6$) deterministically across all 15 parents, producing exactly $15 \times 6 = 90$ mutants (plus 15 companion mutants for $NF_2\text{-R}$).
4. Submit each mutant to `validate_trace_v2()` under both `fail_fast=True` (nominal) and `fail_fast=False` (diagnostic).
5. Categorize each evaluation into the mutually exclusive primary attribution states:
   - `ATTRIBUTABLE_MUTATION_DETECTION`
   - `PREEXISTING_PARENT_INVALIDITY` (expected 0)
   - `ATTRIBUTION_UNRESOLVED`
6. Persist results in `validation/article/r6_1_t4r/r6_1_t4r_mutation_results.json` and generate summary documentation.

---

## 2. Denominator Accounting

$$\begin{aligned}
\text{Total Valid Parents} &= 15 \\
\text{Primary Mutation Families} &= 6 \ (NF_1, NF_2, NF_3, NF_4, NF_5, NF_6) \\
\text{Frozen Primary Denominator} &= 15 \times 6 = 90 \text{ applicable mutants} \\
\text{Companion Family} \ (NF_2\text{-R}) &= 15 \text{ mutants} \\
\text{Total Exhaustive Evaluation} &= 105 \text{ mutants}
\end{aligned}$$

---

## 3. Strict Scientific Guardrails
* **No Retrospective Tuning**: If $NF_2$ is accepted as a boundary observation, it must be recorded factually without altering validator code.
* **Held-Out Quarantine**: Zero reference to `validation/article/r6_heldout/*`.
* **Historical Baseline Fidelity**: Original T4 artifacts in `validation/article/r6_t4/` remain frozen and unmodified.
