# R6.2 Differential CVSS v4.0 Validation Preregistration (Corrected Measurement Protocol R2)
## Test Suite: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R2`

* **Document Version**: 2.0.0-R2
* **Protocol Version**: R6.2
* **Protocol Deviation Reference**: **`R6-DEV-005`** (`POST_RESULT_CHANGE`)
* **Research Question Linkage**: **`RQ-R6-4`** (*Differential Scorer Concordance*)
* **Execution Status**: `PREREGISTERED_FROZEN_NOT_EXECUTED`
* **Historical Experiment Predecessor**: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R1` (`R6.1-DIFF-R1`) in [`validation/article/r6_differential_r1/`](file:///d:/AntiG/cvss/validation/article/r6_differential_r1/)
* **Comparator Acquisition Freeze**: [`validation/article/r6_differential/r6_differential_comparator_acquisition_manifest.json`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_comparator_acquisition_manifest.json)
* **Comparator Pinned Commit**: `cvss4py` at `9fe705cdb7d4a222770e0561f046d3e3f061088a`
* **Vector Corpus Pinned Commit**: `FIRSTdotorg/cvss-resources` at `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`
* **Primary Numeric Denominator**: $D_{\text{numeric}} = 461{,}444$
* **Secondary Validation Denominator**: $D_{\text{validation}} = 25{,}028$
* **Total Corpus Records**: $D_{\text{total}} = 486{,}472$ ($461{,}444 + 25{,}028 = 486{,}472$)
* **Target Success / Agreement Rate**: Formally `null` (scientific falsification study; no target threshold).
* **Expected Agreement Rate**: Formally `null`.
* **Observed Evaluation Records for R2**: **0** (strictly zero execution results observed for R2).
* **Held-Out Corpus Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`, `held_out_accessed = false`).

---

## 1. Rationale for Corrected Protocol R2 (`POST_RESULT_CHANGE` under `R6-DEV-005`)

Following the complete execution of `TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R1` (Order 282/285) and subsequent adversarial audit and reconciliation (Order 288), two independent methodological defects were identified in the R1 experimental protocol:

### A. Classification Defect (Expected Exception Omission)
In runner R1 ([`scripts/run_r6_1_differential_experiment.py`](file:///d:/AntiG/cvss/scripts/run_r6_1_differential_experiment.py)), the tuple of expected validation exceptions for the comparator `cvss4py` was defined as:
```python
(cvss4py.classes.UnknownMetricValue, cvss4py.classes.InvalidEqClass, SyntaxError, ValueError, KeyError)
```
This tuple omitted `cvss4py.classes.MissingMetric`. When the 25,028 official FIRST negative/invalid test cases (which deliberately omit mandatory metrics) were evaluated, 13,126 cases raised `cvss4py.classes.MissingMetric`. Because this class was absent from the expected rejection tuple, it was caught by generic `except Exception as exc:`, flagging the run with `CRASH` and categorizing all 13,126 cases as `EXECUTION_ERROR`. These were not runtime engine crashes, but expected domain validation rejections.

### B. Corpus and Endpoint Eligibility Defect
Protocol R1 declared a primary endpoint of exact numeric score concordance, yet evaluated all 486,472 records under a single homogeneous denominator ($D = 486{,}472$). This aggregated 461,444 valid score-producing vectors together with 25,028 syntax-rejection test cases from `reference-vectors`. For the 11,902 negative cases where both engines rejected the input with recognized syntax exceptions, runner R1 categorized them as `EXACT_SCORE_MATCH`, conflating mutual syntax rejection with numeric float score equivalence.

### Immutability of Historical Evidence:
All artifacts and results of R1 in `validation/article/r6_differential_r1/` remain permanently preserved as frozen historical evidence. Protocol version R2 (`TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R2`) formalizes a versioned correction under deviation **`R6-DEV-005`** (`POST_RESULT_CHANGE`).

---

## 2. Decoupled Two-Endpoint Evaluation Model

To ensure epistemological clarity and avoid confounding mathematical calculation with syntax rejection, Protocol R2 formalizes two mutually independent, disjoint endpoints:

### 2.1 Primary Endpoint: Numeric Score Concordance ($D_{\text{numeric}} = 461{,}444$)
* **Target Population**: Strictly valid, complete, score-producing CVSS v4.0 vectors (`VALID_SCORE_VECTOR`).
* **Frozen Denominator**: $D_{\text{numeric}} = 461{,}444$.
* **Exclusion**: Zero negative or reference-invalid test cases are permitted in this endpoint.
* **Equivalence Criterion**:
  $$|\text{score}_{\text{primary}} - \text{score}_{\text{secondary}}| < 0.0001$$
* **Taxonomy & Precedence**:
  $$\mathbf{Precedence}: \texttt{EXECUTION\_ERROR} > \texttt{VALIDITY\_DISAGREEMENT} > \texttt{SCORE\_MISMATCH} > \texttt{EXACT\_SCORE\_MATCH}$$
* **Definitions**:
  1. `EXACT_SCORE_MATCH`: Both implementations accept the valid input and compute an identical numeric score within tolerance $|\Delta| < 0.0001$.
  2. `SCORE_MISMATCH`: Both implementations accept the valid input and compute numeric scores, but the scores differ ($|\Delta| \ge 0.0001$).
  3. `VALIDITY_DISAGREEMENT`: Exactly one implementation rejects an input formally classified as a valid score-producing vector by the eligibility manifest.
  4. `EXECUTION_ERROR`: An unexpected runtime crash or unhandled exception occurs that does not correspond to expected domain validation.

### 2.2 Secondary Endpoint: Negative Validation Concordance ($D_{\text{validation}} = 25{,}028$)
* **Target Population**: Strictly official FIRST negative and reference-invalid test cases (`NEGATIVE_VALIDATION_CASE`).
* **Frozen Denominator**: $D_{\text{validation}} = 25{,}028$.
* **Taxonomy & Precedence**:
  $$\mathbf{Precedence}: \texttt{NEGATIVE\_EXECUTION\_ERROR} > \texttt{NEGATIVE\_VALIDITY\_DISAGREEMENT} > \texttt{SYNTAX\_REJECTION\_CONCORDANCE}$$
* **Definitions**:
  1. `SYNTAX_REJECTION_CONCORDANCE`: Both implementations reject an input formally designated as negative/invalid by FIRST, regardless of differences in exception class or message.
  2. `NEGATIVE_VALIDITY_DISAGREEMENT`: Exactly one implementation accepts the negative case as valid, while the other rejects it.
  3. `NEGATIVE_EXECUTION_ERROR`: An unexpected runtime failure occurs outside the frozen expected validation exception contract.

---

## 3. Frozen Expected Validation Exceptions Contract

To prevent confusion between domain validation rejections and runtime failures, the exact exception classes representing expected validation behavior are frozen:

### Comparator (`cvss4py` @ `9fe705c`):
* `cvss4py.classes.UnknownMetricValue`
* `cvss4py.classes.InvalidEqClass`
* `cvss4py.classes.MissingMetric` (mandatory inclusion under R6-DEV-005)
* `cvss4py.classes.UnknownMetric`
* `SyntaxError`
* `ValueError`
* `KeyError`

### Primary Scorer (Red Hat `cvss` 3.6 / `CVSS4`):
* `cvss.exceptions.CVSS4MalformedError`
* `cvss.exceptions.CVSS4MandatoryError`
* `cvss.exceptions.CVSS4Error`
* `cvss.exceptions.CVSSError`
* `ValueError`
* `KeyError`

Any exception outside these frozen sets is strictly classified as `EXECUTION_ERROR` (for primary endpoint) or `NEGATIVE_EXECUTION_ERROR` (for secondary endpoint).

---

## 4. Anti-Retuning Declaration & Score Rounding Invariance

1. **Prior R1 Observations Acknowledged**:
   It is explicitly acknowledged that before preregistering R2, the following empirical findings from R1 are known:
   - 454,047 valid positive exact matches ($|\Delta| < 0.0001$).
   - 7,397 valid positive score mismatches, all with $|\Delta| = 0.1$.
   - 25,028 negative test cases with mutual rejection concordance.
   - 13,126 occurrences of `MissingMetric` misclassified in R1.
   - Root-cause association with `cvss4py` float-to-`Decimal` quantization in macro-vector 2.
2. **Prohibition of Retuning**:
   - Neither engine's arithmetic, rounding, or macro weights may be altered.
   - No tolerance widening ($|\Delta| \ge 0.0001$ remains `SCORE_MISMATCH`; no conversion of 0.1 deltas to matches).
   - No post-hoc exclusion of discordant vectors.
   - Target and expected match rates remain formally `null`.

---

## 5. Secondary Diagnostic Dimensions

1. **Official FIRST Reference Diagnostic**:
   For any valid score-producing vector with `SCORE_MISMATCH`, both computed scores are compared against the official FIRST reference score from `macro-scores`, `reference-scores`, or `base-threat-scores`:
   - `HELPUS_MATCHES_FIRST_REFERENCE_ONLY`
   - `CVSS4PY_MATCHES_FIRST_REFERENCE_ONLY`
   - `NEITHER_MATCHES_FIRST_REFERENCE`
   - `FIRST_REFERENCE_UNAVAILABLE`
   *This diagnostic analysis does not alter the primary classification.*

2. **Derived Severity Rating Concordance**:
   Qualitative severity bands derived via FIRST CVSS v4.0 Section 4.2 intervals:
   - `SAME_SEVERITY_BAND`
   - `SEVERITY_BOUNDARY_CROSSED`
   - `NOT_APPLICABLE`

---

## 6. Deterministic Parity Requirements

* Execution requires two consecutive, independent, full evaluation passes (Run 1 and Run 2) over the full corpus in identical canonical order.
* Per-record outcomes and aggregate category counts must match bit-for-bit between Run 1 and Run 2 (`ALL_PASS`).
