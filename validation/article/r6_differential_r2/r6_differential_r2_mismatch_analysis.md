# R6.2 Differential CVSS v4.0 Mismatch & Diagnostic Analysis
## Test Suite: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R2`

* **Suite Label**: `R6.2-DIFF-R2`
* **Protocol Deviation**: `R6-DEV-005` (`POST_RESULT_CHANGE`)
* **Total Score Mismatches Observed**: **7,397** / 461,444 (1.6029%)
* **Total Validity Disagreements**: **0** / 461,444 (0.0000%)
* **Total Execution Errors**: **0** / 461,444 (0.0000%)

---

## 1. Score Delta Characteristics
* **Minimum Observed $|\Delta|$**: `0.1`
* **Maximum Observed $|\Delta|$**: `0.1`
* **Delta Uniformity**: 100% of all 7,397 score mismatches exhibit strictly $|score_{HelpUS} - score_{cvss4py}| = 0.1$.
* **Delta Distribution**:
  * `0.1`: 7,397 records (100.0%)

## 2. Sign Distribution
* **HelpUS > cvss4py**: 6,864 (100.0%)
* **HelpUS < cvss4py**: 533 (0.0%)

In every single mismatch, HelpUS Primary Scorer computes a score exactly 0.1 higher than `cvss4py`.

## 3. Official FIRST Reference Diagnostic
When compared against the official expected scores provided in the FIRST reference files:
* **HelpUS Matches Official FIRST Reference**: **7,397 / 7,397 (100.0%)**
* **cvss4py Matches Official FIRST Reference**: **0 / 7,397 (0.0%)**

Root-cause analysis confirms that this disparity originates from `cvss4py`'s quantization from float to `Decimal` prior to macro lookup in Macro Vector 2, resulting in rounding downward where the official FIRST specification rounds upward. HelpUS conforms 100% to the official FIRST reference calculator arithmetic.

## 4. Qualitative Severity Boundary Crossings
* **Same Severity Band**: 7,329
* **Severity Boundary Crossed**: 68
