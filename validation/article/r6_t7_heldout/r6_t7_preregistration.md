# R6-T7 Preregistration: External Held-Out Transfer Protocol
## Test Suite: `TEST-SUITE-R6-T7-HELDOUT-TRANSFER` (Label: `R6-T7-HELDOUT`)

* **Document Version**: 1.0.0
* **Protocol Version**: R6.1
* **Research Question Linkage**: **RQ-R6-1** (*"O contrato de verificação mantém integridade e cobertura em um novo corpus externo held-out, independente dos 30 casos R5?"*)
* **Execution Status**: `PREREGISTERED_FROZEN_AWAITING_HELDOUT_AUTHORIZATION`
* **Parent Commit (Freeze Baseline)**: `32407259b9e8b07f84316c5057bf885ec29e8e8f` (R6.2-DIFF-R2 results freeze)
* **Parent Plan Reference**: [`validation/article/r6_r6_1_test_plan.md §2 (T7)`](file:///D:/AntiG/cvss/validation/article/r6_r6_1_test_plan.md)
* **Corpus Protocol Reference**: [`validation/article/r6_a1_heldout_corpus_protocol.md`](file:///D:/AntiG/cvss/validation/article/r6_a1_heldout_corpus_protocol.md)
* **Target Artifact**: Quarantined 938 Public Advisories (`validation/article/r6_heldout/*`)
* **Target Success Rate**: `null` (exploratory empirical transfer evaluation; zero target cherry-picking)
* **Expected Success Rate**: `null`
* **Held-Out Access State**: `held_out_accessed = false` (Zero records read, zero CVE/GHSA IDs enumerated)
* **Human Adjudication State**: `human_adjudication_completed = false`
* **Equation 8 Status**: Strictly nominal and unchanged (`eq8_modified = false`)
* **Execution Gate**: `QUARANTINED_LOCKED` (Aborts fail-closed unless explicit supervisor authorization citing this freeze commit is supplied)

---

## 1. Scientific Motivation and Context

In empirical cybersecurity and evaluation science, machine-readable specifications developed on benchmark suites are susceptible to subtle overfitting (the "benchmark over-tuning" hazard). The R5 experimental foundation utilized 30 canonical scenarios (12 NVD real-world scenarios and 18 synthetic edge cases).

Test Suite **T7** addresses research question **RQ-R6-1**:
> *"O contrato de verificação mantém integridade e cobertura em um novo corpus externo held-out, independente dos 30 casos R5?"*

The goal is to measure the contract transferability, syntactic conformance, and audit expressiveness of Schema v2, the downstream Governance Override mechanism, and the machine-checkable trace verifier on an independently collected, quarantined external corpus of public security advisories without altering Equation 8 or inventing missing semantic facts.

---

## 2. Quarantined Held-Out Corpus Provenance & Frozen Metadata

The held-out dataset was collected and sealed prior to model execution in strict adherence to [`validation/article/r6_a1_heldout_corpus_protocol.md`](file:///D:/AntiG/cvss/validation/article/r6_a1_heldout_corpus_protocol.md):

* **Source**: GitHub Advisory Database (`type=reviewed`, global security advisories).
* **Temporal Window**: `2026-09-01T00:00:00Z` to `2026-10-01T00:00:00Z` (exclusive).
* **Candidate Count Acquired**: 947 raw candidates.
* **Exclusions Applied**: 9 records excluded prior to lock, all matching pre-registered criterion `MALWARE_ADVISORY`.
* **R5 Scenario Overlap**: Exactly 0 overlaps (`r5_overlap_count = 0`).
* **Eligible Corpus Denominator**: $N = 938$ advisories.
* **Normative Upstream Commits**:
  * Protocol Freeze: `106049618eff5e2f2a34aa591475c4a042bdba37`
  * Acquisition Tool Freeze: `2346859b319eac9146273b215eca796147816837`
  * Corpus Lock Freeze: `12bf6c456054656a1bbc198d7e3729d2675098b2`
* **Frozen Metadata Hashes (from authorized manifest metadata, without accessing records)**:
  * `eligible_corpus_manifest.json`: `b09a8cc45147f25073103c005d87b4244ea9e03a8233b7059fbd310cc13a22cf`
  * `acquisition_metadata.json`: `0821b7cc11a6c3e967fad38e0607140fd2f90a3ecbd3f6dbd1011ebbc5f756b4`
  * `inclusion_exclusion_ledger.json`: `171c89aa26404da7728d10ccc69b7eea6bb2b271ad9df50cb569e0ff8040c69c`
  * `raw_source_snapshot.json`: `eb0d5e80dfd6827896aa87315f1f9fd63748f243ae831185c068cf4c35641df2`

---

## 3. Unit of Analysis & Denominator Rule

* **Unit of Analysis**: Each individual eligible advisory record in the held-out corpus ($N = 938$).
* **Exhaustive Evaluation**: The evaluation denominator is fixed at exactly $N = 938$.
* **Zero Post-Hoc Exclusions**: No record may be discarded, filtered, or excluded based on CVSS score, difficulty, missing fields, or unexpected schema failure. Corrupt or unparseable records are classified explicitly in the failure taxonomy.

---

## 4. Mutually Exclusive Outcome Taxonomy

Every record processed in T7 must map to exactly one mutually exclusive primary classification state, plus an orthogonal trace verification result:

### 4.1 Primary Operational Outcomes
1. **`SCHEMA_V2_VALID_NOMINAL_CALCULABLE`**:
   The advisory payload conforms completely to Schema v2 closed-world validation and possesses nominal CVSS v4.0 metrics enabling direct evaluation under Equation 8 without governance overrides.
2. **`SCHEMA_V2_VALID_GOVERNANCE_OVERRIDE_DOCUMENTED`**:
   The advisory conforms to Schema v2 and explicitly documents an operational governance override, including pre-override priority, post-override priority, approved reason code, and audit trail, preserving downstream auditability.
3. **`SCHEMA_V2_STRUCTURAL_INVALIDITY_REJECTED`**:
   The advisory payload violates Schema v2 closed-world structural constraints (e.g., unknown fields, schema version confusion, invalid metric bounds, invalid enum literals).
4. **`MISSING_MANDATORY_EVIDENCE_REJECTED`**:
   The advisory lacks mandatory structural evidence required by the input specification (e.g., missing base vector, empty vulnerability identifier, null required envelope fields).
5. **`INSUFFICIENT_INFORMATION_UNRESOLVED`**:
   The advisory lacks necessary contextual information for deterministic environmental mapping, and resolving it would require inventing information in violation of the anti-invention invariant.
6. **`EXECUTION_OR_ENVIRONMENT_ERROR`**:
   An unexpected runtime exception or environmental failure occurred during execution.

### 4.2 Orthogonal Trace Verification Outcomes
For all valid records that produce a verification trace:
* **`TRACE_VERIFICATION_PASS`**: The independent machine-checkable verifier validates all proof steps, hash chains, and mathematical assertions.
* **`TRACE_VERIFICATION_FAIL`**: The verifier detects a discrepancy, corrupted hash, or invalid transition in the execution trace.

---

## 5. Methodological Invariants & Epistemological Boundaries

1. **Equation 8 Invariance**:
   Equation 8 remains purely nominal and immutable. No coefficient, weight, or threshold may be altered to improve held-out performance.
2. **Downstream Governance Override**:
   Governance overrides are strictly post-scoring operations. They do not alter formula calculations and must never be triggered autonomously without human review (`human_review_status = "required"`).
3. **Zero Information Invention**:
   No heuristic default or synthetic guess may be substituted for missing real-world evidence. If an advisory lacks an attribute, that attribute remains null/absent.
4. **Anti-Retuning Prohibition**:
   The following baselines are permanently frozen and known prior to T7 execution:
   - R5 historical results (SCN-NVD-001..012, SCN-SYN-013..030)
   - T2/T2R, T3 Replay, T4/T4R/NF2-R, T5/T5-R, T6 NVD Representability
   - R6 Differential R1 and R2 results
   - Schema v2 specification and validator
   - Governance override specification
   No modification of these specifications is permitted following the observation of T7 held-out data. Any change necessitates a formal protocol deviation and a versioned rerun.
5. **Statistical Reporting Policy**:
   - `target_rate = null`
   - `expected_rate = null`
   - All reports must report empirical counts and raw proportions.
   - Wilson Score confidence intervals or inferential hypothesis tests are disallowed by default, as the held-out corpus constitutes an exhaustive census of the pre-registered temporal window ($N = 938$), not a random probability sample.
   - Diagnostic check counts must never be conflated with scenario sample size.

---

## 6. Determinism & Dual-Pass Parity Protocol

Execution of T7 must follow the two-pass deterministic parity requirement:
1. **Run 1**: Complete execution over all 938 eligible records.
2. **Run 2**: Complete independent re-execution over all 938 eligible records.
3. **Parity Check**:
   $$\text{Run 1 Output} \equiv \text{Run 2 Output} \quad (\text{100\% bit-for-bit parity across all records})$$
   Any discrepancy flags non-determinism, requiring an immediate run failure.

---

## 7. Fail-Closed Authorization Gate

The held-out dataset remains strictly quarantined behind a fail-closed execution firewall:
* The runner is initialized in state `QUARANTINED_LOCKED`.
* Execution is unconditionally blocked until a dedicated supervisory order explicitly releases the held-out gate.
* The release token must specifically reference the SHA-256 hash and Git commit SHA of this T7 Preregistration Freeze.
