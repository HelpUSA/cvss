# R6.1 Experiment T2R: Backward Compatibility Rerun Plan

## 1. Plan Overview & Governance Metadata
* **Experiment Identifier**: `R6.1-T2R-BACKWARD-COMPATIBILITY`
* **Protocol Version**: `R6.1`
* **Protocol Deviation Reference**: `R6-DEV-001` (`POST_RESULT_CHANGE`)
* **Taxonomy Reference**: `validation/article/r6_1_t2_compatibility_taxonomy.md`
* **Contract Reference**: `validation/article/r6_1_t2_compatibility_contract.json`
* **Specification Baseline Commit**: `090ad8b727e674aac8e95864fe7740b15092ea60`
* **Implementation Freeze Commit**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
* **Execution Status**: `PREREGISTERED_NOT_EXECUTED` (Will NOT be executed under this order)
* **Target Output Directory**: `validation/article/r6_1_t2r/` (completely isolated from `validation/article/r6_t2/`)
* **Held-Out Quarantined**: `True` (`held_out_accessed = false`)

---

## 2. Rerun Scope and Methodological Boundary

### 2.1 Preserved Components (Strictly Unchanged)
1. **Input Corpus**: The exact 30 canonical historical scenarios:
   - 12 NVD scenarios: `SCN-NVD-001` through `SCN-NVD-012`
   - 18 Synthetic scenarios: `SCN-SYN-013` through `SCN-SYN-030`
2. **Schema v1 Baseline Validator**: The historical open-world validator in `core/r6_schema_v2_validator.py` (`validate_trace_v1`).
3. **Schema v2 Validator Core**: The frozen closed-world validator implementation at commit `43664e58b4f7852d0a03c6b21ab043dec2529be9` (`validate_trace_v2`).
4. **Validation Evidence**: All raw validation results (`v1_valid`, `v2_valid`, `errors`) will be computed dynamically without modification to core validator semantics.

### 2.2 Modified Component (Taxonomic Layer Only)
The sole modification in `R6.1-T2R` is the compatibility classifier mapping layer:
- The classifier maps the tuple $(v_1, v_2, \text{norm})$ to the 5-state complete taxonomy defined in `r6_1_t2_compatibility_taxonomy.md`.
- For $v_1 = \text{valid} \land v_2 = \text{invalid}$, the category is assigned as `V1_VALID_V2_INVALID`, and the diagnostic error category is stored orthogonally in `v2_error_category`.

---

## 3. Storage and Immutability Safeguards

1. **New Dedicated Output Directory**: All artifacts from `R6.1-T2R` must be written exclusively to `validation/article/r6_1_t2r/`:
   - `r6_1_t2r_backward_compatibility_results.json`
   - `r6_1_t2r_backward_compatibility_summary.md`
   - `SHA256SUMS.txt`
2. **Strict Immutability of Original T2**: Under no circumstances will any file in `validation/article/r6_t2/` be modified, overwritten, or renamed. The original T2 results remain preserved as primary evidence of the R6 protocol gap.
3. **Held-Out Quarantine**: Experiment `R6.1-T2R` operates exclusively on the 30 historical traces. The held-out corpus in `validation/article/r6_heldout/` will not be opened or accessed.
4. **Separation from Downstream Experiments**: The rerun will not execute T3 (mutation replay), T4 (new mutations), T6 (NVD representability), or T7 (held-out evaluation).

---

## 4. Execution Protocol (For Future Authorized Execution Order)

When authorized by a future technical order, execution will proceed as follows:
1. Initialize target directory `validation/article/r6_1_t2r/`.
2. Load each of the 30 canonical traces in memory.
3. Execute `validate_trace_v1(trace)`.
4. Execute `validate_trace_v2(trace)`.
5. Classify compatibility using the R6.1 orthogonal taxonomy.
6. Record detailed diagnostics including orthogonal `v2_error_category`.
7. Persist results JSON, summary markdown, and SHA-256 manifest.
8. Perform independent deterministic rerun verification in memory.
