# R6 Differential CVSS v4.0 Validation Preregistration
## Test Suite: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40`

* **Document Version**: 1.0.0
* **Protocol Version**: R6.1
* **Research Question Linkage**: **RQ-R6-4** (*"Qual é o grau de concordância e quais classes de discrepância, se houver, são observadas entre o scorer primário CVSS v4.0 e uma implementação secundária independente sob um corpus de vetores pré-definido?"*)
* **Execution Status**: `PREREGISTERED_NOT_EXECUTED`
* **Parent Preregistration Section**: [`validation/article/r6_a1_preregistration.md §6`](file:///d:/AntiG/cvss/validation/article/r6_a1_preregistration.md)
* **Contract Specification**: [`validation/article/r6_differential/r6_differential_comparator_contract.json`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_comparator_contract.json)
* **Corpus Manifest**: [`validation/article/r6_differential/r6_differential_vector_corpus_manifest.json`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_vector_corpus_manifest.json)
* **Execution Plan**: [`validation/article/r6_differential/r6_differential_execution_plan.md`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_execution_plan.md)
* **Acquisition Plan**: [`validation/article/r6_differential/r6_differential_acquisition_plan.md`](file:///d:/AntiG/cvss/validation/article/r6_differential/r6_differential_acquisition_plan.md)
* **Target Success / Agreement Rate**: Formally `null` (scientific falsification study; zero pre-fixed target agreement rate).
* **Expected Agreement Rate**: Formally `null`.
* **Held-Out Corpus Quarantine**: `STRICTLY_LOCKED` (`held_out_allowed = false`, `held_out_accessed = false`).

---

## 1. Scientific Motivation & Context

In vulnerability scoring research, relying on a single codebase introduces single-implementation bias, risking that subtle mathematical bugs, macro-vector lookup table errors, or boundary rounding distortions in the parser go unnoticed.

Under the IEEE R6 protocol, Test Suite `TEST-SUITE-R6-DIFFERENTIAL-CVSS40` implements a formal differential testing campaign comparing the primary CVSS v4.0 scoring implementation used by HelpUS against an independent, open-source secondary implementation across a massive, exhaustively defined corpus of 486,472 canonical vectors.

### Falsifiable Hypothesis H-R6-4:
$$\mathbf{H\text{-}R6\text{-}4}: \text{The primary and secondary independent implementations will produce equivalent normalized CVSS v4.0 scores, severity ratings, and nomenclature for all valid vectors in the preregistered differential corpus.}$$

Every observed divergence will be rigorously preserved, categorized, and reported in full without suppression, ad-hoc tuning, or post-hoc vector exclusion.

---

## 2. Implementations Under Comparison

### 2.1 Primary Implementation Under Test
* **Engine/Module**: [`core/cvss_calculator.py`](file:///d:/AntiG/cvss/core/cvss_calculator.py) utilizing the pinned Red Hat Product Security `cvss` Python library (version 3.6).
* **Repository**: `https://github.com/RedHatProductSecurity/cvss`
* **Implementation Freeze Commit**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
* **FIRST Conformance Baseline**: Validated against the FIRST reference test suites (`tests/cvss_v4_conformance/`).
* **Scope Boundary**: Evaluates purely CVSS v4.0 mathematical scoring semantics and vector canonicalization. Excludes governance override logic, Schema v2 trace wrapping, and Equation 8 environmental policy weighting.

### 2.2 Selected Independent Secondary Comparator
* **Project Name**: **`cvss4py`**
* **Repository URL**: `https://github.com/bjedwards/cvss4py`
* **Maintainer / Organization**: Benjamin Edwards (Independent Security Researcher / SEI).
* **License**: MIT License (Permissive open-source, fully auditable).
* **CVSS v4.0 Support Evidence**: Dedicated clean-room Python implementation of the CVSS v4.0 specification, lookup tables, and scoring equations.
* **Independence Justification**: Developed completely independently from Red Hat Product Security and the HelpUS codebase. Implemented from the published FIRST specification without shared code.
* **Execution Environment**: Native Python, executable 100% offline following acquisition.
* **Known Limitations**: Focuses primarily on Base and Threat/Environmental vector scoring without heavy wrapper abstraction.

### 2.3 Formally Rejected Comparator Candidates
To prevent the appearance of cherry-picking, alternative candidates were formally evaluated and rejected:
1. **`FIRSTdotorg/cvss-v4-calculator` (JavaScript / Node.js)**:
   - *Reason for Rejection as Secondary Comparator*: Its lookup files already serve as the ground-truth reference data generator for the FIRST fixtures in the project repository; furthermore, requiring a Node.js runtime creates extraneous environment dependencies when an independent Python implementation is available.
2. **`pandatix/go-cvss` (Go) / `scm-rs/cvss-rs` (Rust)**:
   - *Reason for Rejection*: Requiring external compiler toolchains (Go compiler, Cargo/Rust toolchain) introduces significant cross-platform environment friction and potential container compilation discrepancies during independent replication.
3. **Web-based Calculators & Remote APIs (NVD API, FIRST Online Calculator)**:
   - *Reason for Rejection*: Violates the mandatory protocol requirement of deterministic, offline, and hermetic execution.

---

## 3. Fixed Vector Corpus Specification

The differential testing corpus is derived exclusively from the official, pinned FIRST reference vector dataset already verified and stored in the repository:

* **Source Repository**: `https://github.com/FIRSTdotorg/cvss-resources` (pinned commit `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`).
* **Local Path**: [`tests/fixtures/cvss_resources/vectorFiles/`](file:///d:/AntiG/cvss/tests/fixtures/cvss_resources/vectorFiles/)
* **Fixture Files & Manifest**:
  1. `macro-vectors`: 270 vectors (SHA-256: `f653914506e697a94a18b690c051144b295626c534737fb79c589a61c1e0e8a3`)
  2. `reference-vectors`: 66,299 valid vectors (66,331 lines; SHA-256: `fdcb3de3485354ff36577b41b2fcf7f8056785fb6d6bf6c6eed97e7d3bc934bf`)
  3. `base-threat-vectors`: 419,904 valid vectors (SHA-256: `eb9cf89bab6712f368fe65c43f884e1ca4750e4e30181fabad4a61aaecccede1`)
* **Total Evaluated Denominator**:
  $$\text{Primary Denominator } (D) = \mathbf{486{,}472 \text{ valid canonical CVSS v4.0 vectors}}$$
  $$(269 \text{ macro} + 66{,}299 \text{ reference} + 419{,}904 \text{ base-threat} = 486{,}472)$$
* **Ordering Rule**: Strict lexicographical ordering by vector string as defined in the source fixture files.
* **Zero Selection Filtering**: Zero post-observation exclusions; all valid vectors in the corpus are evaluated.

---

## 4. Compared Outputs & Equivalence Rules

For every vector in the corpus, the runner evaluates the following outputs:

1. **Numeric CVSS v4.0 Score**:
   - *Equivalence Rule*: Exact equality to 1 decimal place. Under CVSS v4.0 specification rules, scores are rounded using $\text{Math.round}(x \times 10) / 10$. Both engines must yield the identical rounded float (absolute delta $|\Delta| < 0.0001$).
2. **Qualitative Severity Rating**:
   - *Equivalence Rule*: Case-insensitive string match across standard FIRST tiers:
     - `None` ($0.0$)
     - `Low` ($0.1 - 3.9$)
     - `Medium` ($4.0 - 6.9$)
     - `High` ($7.0 - 8.9$)
     - `Critical` ($9.0 - 10.0$)
3. **Vector Nomenclature & Prefix**:
   - *Equivalence Rule*: Standardized vector prefix `CVSS:4.0/` and metric order validity.

---

## 5. Differential Classification Taxonomy

Each evaluated vector is classified into exactly one mutually exclusive primary category:

| Taxonomy Category | Definition | Interpretation |
| :--- | :--- | :--- |
| **`EXACT_MATCH`** | Numeric score, severity rating, and vector prefix are bit-for-bit / string-equivalent. | Full concordant implementation. |
| **`SCORE_MISMATCH`** | Numeric scores diverge by $\ge 0.1$, regardless of severity label. | Algorithmic or lookup discrepancy. |
| **`SEVERITY_MISMATCH`** | Numeric scores match, but qualitative severity ratings disagree. | Boundary interval discrepancy. |
| **`VECTOR_NORMALIZATION_MISMATCH`** | Scores and severity match, but metric serialization order diverges. | Syntax normalization discrepancy. |
| **`VALIDITY_DISAGREEMENT`** | One implementation parses the vector as valid while the other rejects it as invalid. | Parsing grammar divergence. |
| **`COMPARATOR_UNSUPPORTED_CASE`** | Vector contains metric combinations explicitly unsupported by the secondary comparator. | Documented scope boundary. |
| **`EXECUTION_ERROR`** | Unhandled exception or runtime crash during vector evaluation. | Implementation defect. |

### Primary Mismatch Precedence Rule:
$$\text{EXECUTION\_ERROR} > \text{VALIDITY\_DISAGREEMENT} > \text{COMPARATOR\_UNSUPPORTED\_CASE} > \text{SCORE\_MISMATCH} > \text{SEVERITY\_MISMATCH} > \text{VECTOR\_NORMALIZATION\_MISMATCH} > \text{EXACT\_MATCH}$$

The sum of primary classifications across the corpus must equal the denominator exactly:
$$\sum \text{Categories} = 486{,}472$$

---

## 6. Strict Scientific Guardrails

1. **Anti-Retuning Lock**:
   No code in the primary engine or secondary comparator may be modified during or after execution to artificially eliminate observed mismatches.
2. **Neutral Discrepancy Reporting**:
   Mismatches are not assumed to be errors of either engine automatically; they are reported raw as empirical findings and subjected to separate post-hoc adversarial review.
3. **Held-Out Corpus Isolation**:
   Access to `validation/article/r6_heldout/*` is strictly barred throughout this experiment (`held_out_allowed = false`, `held_out_accessed = false`). No vectors are drawn from the held-out corpus.
4. **Equation 8 Invariance**:
   Equation 8 formulas, weights, and environmental logic are completely excluded from this test and remain 100% untouched.
5. **Deterministic Rerun Parity**:
   The execution must be re-executed in a second independent pass asserting 100% bitwise parity.
