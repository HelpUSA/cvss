# R6.1-T4R Primary Campaign: Family Comparison and Structural Analysis
## Experiment: `R6.1-T4R-PRIMARY` ($N = 90$)

This document provides a comparative diagnostic analysis across the 6 primary mutation families evaluated on the 15 certified Schema v2 canonical parents.

---

## 1. Comparative Family Diagnostic Matrix

| Family ID | Target Structural Path | Target Scope | Normative Clause | Rejection Rate ($k/15$) | Detection Rate ($k/15$) | Diagnostic Error Category |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **NF1** | `root.extensions.unprefixed_telemetry_flag` | Extensions Point | Spec §5.2 | **15/15 (100%)** | **15/15 (100%)** | `INVALID_EXTENSION_NAMESPACE` |
| **NF2** | `root.extensions.custom_audit:cvss_b_score` | Extensions Point | Spec §5.3 | **0/15 (0%)** | **0/15 (0%)** | `None` (Boundary Accepted) |
| **NF3** | `root.formula_override` | Root Object | Spec §4, §5.4 | **15/15 (100%)** | **15/15 (100%)** | `RESERVED_FIELD` |
| **NF4** | `root.environmental_evidence.compensating_controls[0].kernel_enforced` | Nested Collection | Spec §4.1.C | **15/15 (100%)** | **15/15 (100%)** | `UNKNOWN_FIELD` |
| **NF5** | `root.environmental_evidence.asset_class` | Core Scalar | Spec §4, §4.1 | **15/15 (100%)** | **15/15 (100%)** | `INVALID_TYPE` |
| **NF6** | `root.$schema` | Root Header | Spec §3, §8 | **15/15 (100%)** | **15/15 (100%)** | `UNKNOWN_FIELD` |

---

## 2. Source-Stratified Detection Performance

### 2.1 NVD Canonical Parents ($N_{\text{{parents}}} = 7$, $N_{\text{{mutants}}} = 42$)
* **Families Tested**: $NF_1$–$NF_6$ across SCN-NVD-001, 004, 006, 007, 008, 009, 012.
* **Mutants Rejected**: 35 / 42 (83.3%)
* **Attributable Detections**: 35 / 42 (83.3%)
* **Boundary Accepted ($NF_2$)**: 7 / 42 (16.7%)

### 2.2 Synthetic Canonical Parents ($N_{\text{{parents}}} = 8$, $N_{\text{{mutants}}} = 48$)
* **Families Tested**: $NF_1$–$NF_6$ across SCN-SYN-015, 016, 017, 020, 023, 024, 025, 028.
* **Mutants Rejected**: 40 / 48 (83.3%)
* **Attributable Detections**: 40 / 48 (83.3%)
* **Boundary Accepted ($NF_2$)**: 8 / 48 (16.7%)

> **Parity Observation**: Detection rates are identical across real NVD and synthetic corpora (83.3% rejection, 83.3% attributable detection), confirming that closed-world schema enforcement functions uniformly irrespective of trace narrative density.

---

## 3. Comparison with Historical T4 Baseline

| Metric | Original T4 Baseline (Historical) | R6.1-T4R-PRIMARY (Current) | Difference / Methodological Significance |
| :--- | :---: | :---: | :--- |
| **Parent Corpus** | 30 uncanonicalized traces | 15 certified v2-compliant traces | Eliminates parent precondition invalidity |
| **Parent Precondition Failures** | 90 / 180 (50.0%) | **0 / 90 (0.0%)** | **100% clean baseline attribution** |
| **Denominator** | 180 mutants | **90 mutants** | Strict valid-parent denominator ($D=90$) |
| **Rejection Rate** | 165 / 180 (91.7%) | **75 / 90 (83.3%)** | True closed-world rejection rate |
| **Attributable Detection Rate** | 75 / 180 (41.7%) | **75 / 90 (83.3%)** | **+41.6 pp attributable detection clarity** |
| **Confounded Attributions** | 90 / 180 (50.0%) | **0 / 90 (0.0%)** | **Completely resolved under R6-DEV-002** |
