# R6 Differential Comparator Capability Audit: `cvss4py`
## Test Suite: `TEST-SUITE-R6-DIFFERENTIAL-CVSS40` (`RQ-R6-4`)

* **Acquired Package**: `cvss4py`
* **Pinned Commit**: `9fe705cdb7d4a222770e0561f046d3e3f061088a`
* **Local Vendor Staging**: [`external/comparators/cvss4py/`](file:///d:/AntiG/cvss/external/comparators/cvss4py/)
* **Audit Execution**: Static Source & AST Inspection (Strictly zero evaluation of the 486,472 test corpus)

---

## 1. Independence Verification

A complete source code audit was conducted on all 14 files of `cvss4py`:
1. **Zero Internal Imports**: The package contains zero imports from `core.*`, `app.*`, or any HelpUS project modules.
2. **Zero Red Hat Library Re-use**: The package contains zero imports or dependencies on `cvss` (`RedHatProductSecurity/cvss`). It implements metric mapping, macro-vector calculations, and lookup tables completely independently.
3. **Zero FIRST API Wrapping**: The package does not query FIRST online services; all data files (`eq_data.json`, `metric_data.json`) are self-contained local JSON tables.
4. **Conclusion**: **`INDEPENDENCE_AUDIT_PASS`**.

---

## 2. Capability Mapping against Preregistered Outputs

| Output Field in Preregistration | Directly Exposed by `cvss4py` API? | Source Mechanism in `cvss4py` | Execution Runner Strategy |
| :--- | :---: | :--- | :--- |
| **`parse_cvss40_vector`** | **YES** | `is_valid_vector()`, `vector_str_to_object()` | Direct invocation. |
| **`compute_numeric_score`** | **YES** | `score_vector()` in `score.py` | Direct invocation returning float to 1 decimal place. |
| **`expose_severity_label`** | **NO** | Not directly provided as an API string | **Deterministic Normative Mapping**: The runner maps the float score output from `cvss4py` directly to the standard FIRST CVSS v4.0 severity rating intervals (`None`, `Low`, `Medium`, `High`, `Critical`). |
| **`serialize_canonical_vector`** | **NO** | Vector remains a parsed Python dictionary | Excluded from primary mismatch; evaluated as orthogonal diagnostic syntax check. |
| **`detect_invalid_vectors`** | **YES** | Raises `SyntaxError`, `InvalidEqClass` or `is_valid_vector() == False` | Caught and categorized as `VALIDITY_DISAGREEMENT`. |

---

## 3. Arithmetic and Rounding Semantics Audit

Inspection of line 124 of [`cvss4py/score.py`](file:///d:/AntiG/cvss/external/comparators/cvss4py/cvss4py/score.py):
```python
return float(Decimal(base_score - total_adjustment).quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
```

* **Rounding Method**: `ROUND_HALF_UP` via Python `decimal.Decimal`.
* **Specification Conformance**: Strictly conforms to CVSS v4.0 specification Section 8.3 requiring standard half-up rounding at the single decimal place ($0.1$).
* **Compatibility Status**: **`ROUNDING_SEMANTICS_COMPATIBLE`**.

---

## 4. Runtime Output Handling (Stdlib Silence)

In `cvss4py/score.py`, development debug statements (`print("Macrovector: ", ...)`) exist in the source code.
* **Prohibition Against Patching**: The comparator source code must remain unmodified bit-for-bit.
* **Hermetic Execution Guard**: The execution runner shall invoke `cvss4py.score_vector` inside a `contextlib.redirect_stdout(io.StringIO())` context manager to completely suppress terminal I/O overhead without modifying a single line of third-party source code.

---

## 5. Dependency and Reproducibility Verification

* **External Dependencies**: **NONE** (`pyproject.toml` lists only `python = "^3.8"`).
* **Standard Library Modules Used**: `itertools`, `statistics`, `decimal`, `json`, `pkgutil`, `warnings`.
* **Offline Execution**: 100% executable offline without network or build tools.
* **Conclusion**: **`ACQUISITION_VERIFIED_READY_FOR_EXECUTION`**.
