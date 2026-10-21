# R6.1 Differential CVSS v4.0 Execution Plan (Clarified Protocol R1)
## Test Suite: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R1`

* **Document Version**: 1.0.0-R1
* **Protocol Version**: R6.1
* **Protocol Deviation Reference**: **`R6-DEV-004`** (`PRE_RESULT_CHANGE`)
* **Research Question Linkage**: **`RQ-R6-4`** (*Differential Scorer Concordance*)
* **Execution Status**: `PREREGISTERED_CLARIFIED_NOT_EXECUTED`
* **Execution Authorization**: `PENDING_FUTURE_SUPERVISOR_ORDER` (Strictly zero evaluation vectors executed under this order)
* **Parent Preregistration**: [`validation/article/r6_differential_r1/r6_differential_r1_preregistration.md`](file:///d:/AntiG/cvss/validation/article/r6_differential_r1/r6_differential_r1_preregistration.md)
* **Measurement Contract**: [`validation/article/r6_differential_r1/r6_differential_r1_measurement_contract.json`](file:///d:/AntiG/cvss/validation/article/r6_differential_r1/r6_differential_r1_measurement_contract.json)
* **Historical Baseline Contract**: [`validation/article/r6_differential/r6_differential_comparator_contract.json`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_comparator_contract.json)
* **Target Scorer**: [`core/cvss_calculator.py`](file:///d:/AntiG/cvss/core/cvss_calculator.py) (Red Hat `cvss` 3.6)
* **Secondary Comparator**: `cvss4py` (commit `9fe705cdb7d4a222770e0561f046d3e3f061088a`)
* **Vector Corpus**: FIRST CVSS v4.0 official corpus (486,472 vectors; commit `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`)
* **Held-Out Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`, `held_out_accessed = false`)

---

## 1. Execution Pipeline Overview

When officially dispatched by a dedicated supervisor technical order, the differential validation runner shall execute the following deterministic, offline verification pipeline:

### 1.1 Phase 1: Pre-Execution Environment & Cryptographic Integrity Guard
1. **Corpus Integrity Verification**:
   - Verify existence and cryptographic SHA-256 digests of all 3 FIRST vector fixture files in `tests/fixtures/cvss_resources/vectorFiles/`:
     * `01_macro_vectors.txt` (269 vectors)
     * `02_reference_vectors.txt` (66,299 vectors)
     * `03_base_threat_vectors.txt` (419,904 vectors)
   - Ensure total vector count strictly matches $D = 486{,}472$.
2. **Comparator Freeze Verification**:
   - Verify that the secondary comparator (`cvss4py`) is present in `external/comparators/cvss4py/` at pinned commit `9fe705cdb7d4a222770e0561f046d3e3f061088a` as recorded in [`validation/article/r6_differential/SHA256SUMS_COMPARATOR.txt`](file:///d:/AntiG/cvss/validation/article/r6_differential/SHA256SUMS_COMPARATOR.txt).
   - Ensure zero uncommitted local modifications in comparator directory.
3. **Quarantine & Invariance Enforcements**:
   - Assert that access to `validation/article/r6_heldout/*` is strictly barred.
   - Assert that Equation 8 nominal policy calculator is neither invoked nor modified.
   - Assert that no artificial serializer adapter is injected on behalf of `cvss4py`.

---

### 1.2 Phase 2: Batch Differential Evaluation ($D = 486{,}472$)

For each vector $v_i$ ($i \in \{1, \dots, 486{,}472\}$) in lexicographical order:

1. **Primary Scorer Evaluation**:
   - Pass vector $v_i$ to primary engine (`core/cvss_calculator.py` / Red Hat `cvss.CVSS4`).
   - Record validity status $V_{\text{primary}} \in \{\texttt{VALID}, \texttt{INVALID}, \texttt{CRASH}\}$.
   - If valid, extract numeric decimal score $S_{\text{primary}} \in [0.0, 10.0]$ and determine standard severity label $R_{\text{primary}}$.
2. **Independent Comparator Evaluation**:
   - Pass vector $v_i$ to `cvss4py.calculate_vector(...)`.
   - Record validity status $V_{\text{secondary}} \in \{\texttt{VALID}, \texttt{INVALID}, \texttt{CRASH}\}$.
   - If valid, extract numeric float score $S_{\text{secondary}} \in [0.0, 10.0]$ and derive standard qualitative severity $R_{\text{secondary}}$ via FIRST CVSS v4.0 §4.2 mapping.
3. **Primary Classification Assignment (Clarified Precedence)**:
   Evaluate using the strict hierarchy:
   $$\mathbf{EXECUTION\_ERROR} > \mathbf{VALIDITY\_DISAGREEMENT} > \mathbf{SCORE\_MISMATCH} > \mathbf{EXACT\_SCORE\_MATCH}$$
   - If $V_{\text{primary}} == \texttt{CRASH}$ or $V_{\text{secondary}} == \texttt{CRASH}$:
     $$\text{category} = \mathbf{EXECUTION\_ERROR}$$
   - Else if $V_{\text{primary}} \ne V_{\text{secondary}}$:
     $$\text{category} = \mathbf{VALIDITY\_DISAGREEMENT}$$
   - Else if $|S_{\text{primary}} - S_{\text{secondary}}| \ge 0.0001$:
     $$\text{category} = \mathbf{SCORE\_MISMATCH}$$
   - Else:
     $$\text{category} = \mathbf{EXACT\_SCORE\_MATCH}$$
4. **Secondary Diagnostic Dimensions (Orthogonal & Non-Masking)**:
   - Record derived severity agreement: $R_{\text{primary}} == R_{\text{secondary}}$.
   - Record comparator serializer capability: `comparator_native_vector_serializer = false`.
   - Record input nomenclature adherence: `nomenclature_input_prefix_accepted = true`.

---

### 1.3 Phase 3: Deterministic Parity Rerun

Following full corpus evaluation, the runner shall execute an immediate second evaluation pass (or verify full determinism across repeated invocations):
- Assert 100% bitwise parity of all classification counts:
  $$\Delta(\text{EXECUTION\_ERROR}) = 0,\quad \Delta(\text{VALIDITY\_DISAGREEMENT}) = 0$$
  $$\Delta(\text{SCORE\_MISMATCH}) = 0,\quad \Delta(\text{EXACT\_SCORE\_MATCH}) = 0$$
- Assert 100% identity of any captured mismatch records.

---

### 1.4 Phase 4: Output Generation & Artifact Freezing

All output artifacts shall be written exclusively to `validation/article/r6_differential_r1/`:
1. `r6_differential_r1_results.json`: Full machine-readable breakdown, taxonomy counts, and raw mismatch catalog.
2. `r6_differential_r1_summary.md`: Executive research report documenting concordance metrics, category distributions, and scientific conclusions.
3. `r6_differential_r1_mismatch_analysis.md`: Exhaustive analytical inspection of all observed discrepancies (if any).
4. `SHA256SUMS_RESULTS.txt`: Cryptographic checksums of all output files.

---

## 2. Denominator Accounting & Reporting Isolation

$$\text{Primary Scientific Denominator } (D) = \mathbf{486{,}472 \text{ canonical CVSS v4.0 vectors}}$$
$$(269 \text{ macro} + 66{,}299 \text{ reference} + 419{,}904 \text{ base-threat} = 486{,}472)$$

* **Complete Isolation**: Differential validation concordance measures third-party tool agreement across a standardized vector corpus. It must **never** be aggregated with or compared directly against:
  - Mutation testing detection rates (historical $N=120$, T4 $N=90$, T4R $N=15$);
  - Governance override contract fixtures (T5 $N=8$, T5R $N=8$);
  - NVD representability cases (T6 $N=4$);
  - Held-out schema generalization cases (T7 $N=938$).
* **Falsification Guard**:
  - Target agreement rate: Formally documented as `null`.
  - Expected agreement rate: Formally documented as `null`.

---

## 3. Strict Scientific Guardrails

1. **Quarantine Isolation**: Zero query, file-open, or reference to `validation/article/r6_heldout/*`.
2. **Zero Post-Hoc Tuning**: Neither engine may be adjusted post-observation to force higher concordance.
3. **No In-Flight Adaptation**: No proxy serializer shall be implemented on behalf of the secondary comparator.
4. **Execution Gate**: This execution plan is strictly locked in status `PREREGISTERED_CLARIFIED_NOT_EXECUTED`. Zero execution is permitted without an explicit execution order.
