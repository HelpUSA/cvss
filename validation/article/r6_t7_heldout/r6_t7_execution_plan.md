# R6-T7 Execution Plan: Dual-Pass Deterministic Evaluation

* **Experiment**: `TEST-SUITE-R6-T7-HELDOUT-TRANSFER`
* **Label**: `R6-T7-HELDOUT`
* **Research Question**: `RQ-R6-1`
* **Status**: `PREREGISTERED_FROZEN_AWAITING_HELDOUT_AUTHORIZATION`

---

## 1. Execution Stages

### Stage 0: Fail-Closed Gate Authorization Verification
Before reading or opening any file in `validation/article/r6_heldout/`, the runner must:
1. Verify that `--authorize-held-out-access` is passed.
2. Verify that `--auth-token` matches the SHA-256 of the frozen preregistration commit.
3. Verify that the parent repository HEAD is clean and matches the frozen commit baseline.
4. If any check fails, abort immediately with exit code `2` (`QUARANTINED_LOCKED_ABORT`). Zero held-out bytes may be read.

### Stage 1: Manifest Integrity Verification
Once unlocked, verify cryptographic checksums of:
- `eligible_corpus_manifest.json` (`b09a8cc45147f25073103c005d87b4244ea9e03a8233b7059fbd310cc13a22cf`)
- `acquisition_metadata.json` (`0821b7cc11a6c3e967fad38e0607140fd2f90a3ecbd3f6dbd1011ebbc5f756b4`)
Verify that the number of eligible records in memory is exactly $N = 938$.

### Stage 2: Dual-Pass Processing Protocol
1. **Pass 1 (Run 1)**:
   - For each advisory $i \in [1, 938]$ (sorted deterministically by canonical GHSA identifier):
     - Pass advisory evidence to `SchemaV2Validator`.
     - Record validation stage, errors, and classification under the pre-registered taxonomy.
     - Evaluate Equation 8 nominal metrics (if valid).
     - Check governance override encapsulation (if operational deviation indicated).
     - Run independent trace verifier to confirm machine-checkable trace integrity.
   - Record Run 1 aggregate counts and per-record outcome hashes.

2. **Pass 2 (Run 2)**:
   - Completely re-initialize the processing pipeline in a fresh memory environment.
   - Repeat the exact processing pipeline over all 938 records.
   - Record Run 2 aggregate counts and per-record outcome hashes.

### Stage 3: Deterministic Parity Assertion
Assert bit-for-bit identity:
$$\forall i \in [1, 938]: \text{Outcome}_{\text{Run 1}}(i) \equiv \text{Outcome}_{\text{Run 2}}(i)$$
$$\text{Checksum}(\text{Run 1 Manifest}) == \text{Checksum}(\text{Run 2 Manifest})$$
If any disparity is detected, flag `DETERMINISTIC_PARITY_FAILED` and halt without publishing results.

### Stage 4: Artifact Generation and Freezing
Generate execution deliverables in `validation/article/r6_t7_heldout/`:
- `r6_t7_execution_manifest.json`
- `r6_t7_results.json`
- `r6_t7_summary.md`
- `SHA256SUMS_RESULTS.txt`
Commit results in a dedicated execution commit.
