# R6-DIFF Execution Plan: Independent CVSS v4.0 Differential Testing
## Test Suite: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40`

* **Status**: `PREREGISTERED_NOT_EXECUTED`
* **Execution Authorization**: `PENDING_FUTURE_SUPERVISOR_ORDER`
* **Parent Contract**: [`validation/article/r6_differential/r6_differential_comparator_contract.json`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_comparator_contract.json)
* **Corpus Manifest**: [`validation/article/r6_differential/r6_differential_vector_corpus_manifest.json`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_vector_corpus_manifest.json)
* **Target Scorer**: [`core/cvss_calculator.py`](file:///d:/AntiG/cvss/core/cvss_calculator.py) (Red Hat `cvss` 3.6)
* **Secondary Comparator**: `cvss4py` (Benjamin Edwards)
* **Held-Out Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`, `held_out_accessed = false`)

---

## 1. Execution Pipeline Overview

When officially dispatched by supervisor technical order, the differential validation runner shall execute the following deterministic, offline verification pipeline:

### 1.1 Phase 1: Pre-Execution Environment & Integrity Guard
1. Verify presence and cryptographic SHA-256 digests of all 3 FIRST vector fixture files in `tests/fixtures/cvss_resources/vectorFiles/`.
2. Verify that the secondary comparator (`cvss4py`) was acquired and frozen under the preregistered acquisition plan, with zero uncommitted changes.
3. Assert that access to `validation/article/r6_heldout/*` is completely blocked.
4. Verify that Equation 8 nominal policy calculator is not invoked or modified.

### 1.2 Phase 2: Batch Differential Evaluation ($D = 486{,}472$)
For each vector $v_i$ in the canonical corpus:
1. **Primary Scorer Evaluation**:
   - Ingest $v_i$ into the primary engine (`core/cvss_calculator.py` / `cvss.CVSS4`).
   - Extract numeric score $S_{\text{primary}}$ and severity string $R_{\text{primary}}$.
2. **Secondary Scorer Evaluation**:
   - Ingest $v_i$ into the acquired `cvss4py` comparator.
   - Extract numeric score $S_{\text{secondary}}$ and severity string $R_{\text{secondary}}$.
3. **Equivalence & Precedence Classification**:
   - Check validity agreement ($V_{\text{primary}} == V_{\text{secondary}}$).
   - Check numeric score equality ($|S_{\text{primary}} - S_{\text{secondary}}| < 0.0001$).
   - Check severity label equality ($R_{\text{primary}}.\text{lower}() == R_{\text{secondary}}.\text{lower}()$).
   - Assign primary classification according to the strict precedence hierarchy.

### 1.3 Phase 3: Deterministic Parity Rerun
Re-execute all evaluations in a second independent pass in memory and require 100% bitwise/data-structure match across all recorded classification counts and mismatch records.

### 1.4 Phase 4: Output Generation
Emit all outputs into `validation/article/r6_differential/`:
1. `r6_differential_results.json`: Full machine-readable summary with mismatch records.
2. `r6_differential_summary.md`: Executive report with taxonomy breakdown.
3. `r6_differential_mismatch_analysis.md`: Detailed inspection of all observed discrepancies.
4. `SHA256SUMS_RESULTS.txt`: Cryptographic digests of generated outputs.

---

## 2. Denominator Accounting & Reporting Isolation

$$\text{Primary Scientific Denominator } (D) = \mathbf{486{,}472 \text{ canonical CVSS v4.0 vectors}}$$

* **No Merging**: Differential testing metrics measure cross-implementation concordance and must **never** be aggregated with mutation testing detection rates ($N=90$, $N=15$), governance fixtures ($N=8$), or held-out schema transfer cases ($N=938$).
* **Target Agreement Rate**: Formally documented as `null`.
* **Expected Agreement Rate**: Formally documented as `null`.

---

## 3. Strict Scientific Guardrails
* **Held-Out Isolation**: Zero query, file-open, or reference to `validation/article/r6_heldout/*`.
* **Zero Post-Hoc Tuning**: Neither engine may be adjusted post-observation to force a higher agreement rate.
* **No Premature Execution**: This execution plan is strictly locked until a formal technical order is issued.
