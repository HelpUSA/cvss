# R6.1 Differential CVSS v4.0 Validation Preregistration (Clarified Protocol R1)
## Test Suite: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R1`

* **Document Version**: 1.0.0-R1
* **Protocol Version**: R6.1
* **Protocol Deviation Reference**: **`R6-DEV-004`** (`PRE_RESULT_CHANGE`)
* **Research Question Linkage**: **`RQ-R6-4`** (*Differential Scorer Concordance*)
* **Execution Status**: `PREREGISTERED_CLARIFIED_NOT_EXECUTED`
* **Parent Historical Preregistration**: [`validation/article/r6_differential/r6_differential_preregistration.md`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_preregistration.md) (commit `a7fddabdb10ee5086b35d5967ad8e1f6ea258ef4`)
* **Comparator Acquisition Freeze**: [`validation/article/r6_differential/r6_differential_comparator_acquisition_manifest.json`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_comparator_acquisition_manifest.json) (commit `c9dcbd25199216aa1cfc3eb9a936ac6ca09587ea`)
* **Comparator Pinned Commit**: `cvss4py` at `9fe705cdb7d4a222770e0561f046d3e3f061088a`
* **Vector Corpus Pinned Commit**: `FIRSTdotorg/cvss-resources` at `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`
* **Target Success / Agreement Rate**: Formally `null` (scientific falsification study; zero target threshold).
* **Expected Agreement Rate**: Formally `null`.
* **Observed Evaluation Vectors**: **0** (strictly zero evaluation results observed prior to this clarification).
* **Held-Out Corpus Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`, `held_out_accessed = false`).

---

## 1. Rationale for Clarified Protocol R1 (`PRE_RESULT_CHANGE`)

Following the successful acquisition and integrity freezing of the independent comparator `cvss4py` (Order 279), a formal read-only capability audit (Order 280) identified an instrumentation inconsistency between the original preregistered mismatch precedence and the real capabilities of the comparator:

1. **Absence of Native Vector String Serializer**:
   `cvss4py` evaluates parsed vector objects and returns float scores; it does not contain an inverse serializer to re-emit canonical vector strings. Under literal application of the original precedence hierarchy (`COMPARATOR_UNSUPPORTED_CASE > SCORE_MISMATCH > VECTOR_NORMALIZATION_MISMATCH > EXACT_MATCH`), the absence of this auxiliary string formatting capability would either cause 100% of the 486,472 vectors to be flagged as `COMPARATOR_UNSUPPORTED_CASE` or permanently prevent any `EXACT_MATCH`, completely obscuring the primary scientific endpoint of mathematical scoring concordance.
2. **Ambiguity in Severity Exposure**:
   `cvss4py` returns numeric scores as floats without a native `.severity` string method. The original preregistration listed severity tiers, but was ambiguous as to whether qualitative severity must be comparator-native or derived deterministically.
3. **Pre-Result Correction Safeguard**:
   Because **zero vectors have been executed** and **zero scientific match/mismatch results are known**, protocol version `R1` clarifes the measurement model strictly **`PRE_RESULT_CHANGE`** under deviation `R6-DEV-004`, eliminating confounding from unsupported formatting capabilities while preserving the 486,472-vector corpus, the comparator, and the mathematical equivalence rules unchanged.

---

## 2. Primary Scientific Endpoint: Exact Numeric Score Concordance

The primary evaluation endpoint of `RQ-R6-4` is strictly:
$$\mathbf{Primary\ Scientific\ Endpoint}: \text{\textbf{Exact Numeric Score Concordance (CVSS v4.0 Decimal Score)}}$$

For each of the 486,472 canonical vectors, the primary engine ([`core/cvss_calculator.py`](file:///d:/AntiG/cvss/core/cvss_calculator.py) / Red Hat `cvss` 3.6) and the independent comparator (`cvss4py` commit `9fe705c`) compute their independent floating-point scores.

### Equivalence Rule:
* Both engines must compute an identical numeric score to 1 decimal place under CVSS v4.0 specification rules ($\text{Math.round}(x \times 10) / 10$).
* Equivalence criterion:
  $$|\text{score}_{\text{primary}} - \text{score}_{\text{secondary}}| < 0.0001$$
* Zero tolerance adjustments or post-hoc threshold widenings are permitted.

---

## 3. Secondary Derived Diagnostic: Severity Concordance

Qualitative severity ratings are evaluated as an orthogonal diagnostic dimension derived deterministically from the numeric score using the standard FIRST CVSS v4.0 specification intervals (§4.2):

$$\text{Severity}(S) = \begin{cases}
\texttt{"None"}, & S = 0.0 \\
\texttt{"Low"}, & 0.1 \le S \le 3.9 \\
\texttt{"Medium"}, & 4.0 \le S \le 6.9 \\
\texttt{"High"}, & 7.0 \le S \le 8.9 \\
\texttt{"Critical"}, & 9.0 \le S \le 10.0
\end{cases}$$

* **Independence & Determinism**: The mapping function is a pure mathematical transformation applied symmetrically to both score outputs without invoking either engine.
* **Non-Interference**: Severity differences operate as a secondary diagnostic flag (`derived_severity_match: bool`) and do not precede or mask numeric score mismatches.

---

## 4. Reclassification of Vector Serialization & Nomenclature

1. **Vector Serialization**:
   Formally designated as `CAPABILITY_DIAGNOSTIC_NOT_PRIMARY_ENDPOINT`.
   - `comparator_native_vector_serializer = false` is recorded as a global capability property of `cvss4py`.
   - Fabricating a serializer adapter using the HelpUS engine is strictly barred.
   - Vector serialization differences do not withdraw vectors from the denominator and do not alter primary classification.
2. **Nomenclature / Prefix Validation**:
   - `nomenclature_input_prefix_accepted = true` is recorded as a parser diagnostic confirming that `cvss4py` validates the mandatory `CVSS:4.0/` prefix.

---

## 5. Clarified Primary Classification Taxonomy ($D = 486{,}472$)

Every vector in the canonical corpus is classified into exactly one mutually exclusive primary category:

| Primary Category | Definition | Scientific Meaning |
| :--- | :--- | :--- |
| **`EXECUTION_ERROR`** | Unhandled exception or runtime crash during evaluation. | Implementation or parser defect. |
| **`VALIDITY_DISAGREEMENT`** | One implementation parses the valid corpus vector while the other rejects it as invalid. | Parsing grammar divergence on valid standard input. |
| **`SCORE_MISMATCH`** | Both engines parse the vector, but numeric scores differ by $\ge 0.1$. | Algorithmic or lookup discrepancy between implementations. |
| **`EXACT_SCORE_MATCH`** | Both engines parse the vector and yield bit-for-bit identical rounded scores ($|\Delta| < 0.0001$). | Full concordant scoring implementation. |

### Clarified Precedence Hierarchy:
$$\mathbf{EXECUTION\_ERROR} > \mathbf{VALIDITY\_DISAGREEMENT} > \mathbf{SCORE\_MISMATCH} > \mathbf{EXACT\_SCORE\_MATCH}$$

* **Denominator Conservation**:
  The four primary categories are mutually exclusive, exhaustive, and must sum to the primary scientific denominator:
  $$\text{EXECUTION\_ERROR} + \text{VALIDITY\_DISAGREEMENT} + \text{SCORE\_MISMATCH} + \text{EXACT\_SCORE\_MATCH} = \mathbf{486{,}472}$$

---

## 6. Immutable Denominator & Core Guardrails

1. **Denominator Invariance**:
   $$\text{Primary Denominator } (D) = \mathbf{486{,}472 \text{ canonical CVSS v4.0 vectors}}$$
   $$(269 \text{ macro} + 66{,}299 \text{ reference} + 419{,}904 \text{ base-threat} = 486{,}472)$$
2. **Zero In-Flight Modifications**: Neither engine may be modified during execution.
3. **Raw Mismatch Capture**: Any observed score divergence will be captured raw with input vector, engine outputs, and delta.
4. **Deterministic Rerun Parity**: 100% bitwise parity required between Run 1 and Run 2.
5. **Held-Out Quarantine**: Access to `validation/article/r6_heldout/*` remains strictly barred throughout differential testing.
