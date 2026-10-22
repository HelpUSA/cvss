# R6-A1 Experiment T4: Execution Plan
## Preregistered Operational Workflow for Novel Mutation Testing

* **Experiment ID**: `R6-T4-SCHEMA-V2-MUTATION-CAMPAIGN`
* **Status**: `PREREGISTERED_NOT_EXECUTED`
* **Parent Contract**: [`validation/article/r6_t4/r6_t4_mutation_family_contract.json`](file:///D:/AntiG/cvss/validation/article/r6_t4/r6_t4_mutation_family_contract.json)
* **Parent Preregistration**: [`validation/article/r6_t4/r6_t4_mutation_family_preregistration.md`](file:///D:/AntiG/cvss/validation/article/r6_t4/r6_t4_mutation_family_preregistration.md)
* **Execution Authorization**: `PENDING_FUTURE_ORDER`

---

## 1. Execution Preconditions
Prior to running Experiment T4, the execution runner must verify:
1. **Branch**: `research/r6-a1-schema-governance-implementation`.
2. **Implementation Freeze**: [`core/r6_schema_v2_validator.py`](file:///D:/AntiG/cvss/core/r6_schema_v2_validator.py) must match commit `43664e58b4f7852d0a03c6b21ab043dec2529be9`.
3. **Specification Freeze**: [`validation/article/r6_schema_v2_specification.md`](file:///D:/AntiG/cvss/validation/article/r6_schema_v2_specification.md) must match commit `090ad8b727e674aac8e95864fe7740b15092ea60`.
4. **Input Firewall**:
   - Zero read or reference to `validation/article/r6_heldout/*`.
   - Authorized inputs: 30 canonical historical scenarios (12 NVD, 18 Synthetic).
5. **No Target Tuning**: The execution script must not contain assertion heuristics or detection-rate thresholds.

---

## 2. Experimental Execution Matrix

| Step | Action | Description | Output Artifact |
| :---: | :--- | :--- | :--- |
| **1** | **Input Loading** | Ingest the 30 canonical historical traces without mutation. | In-memory clean traces |
| **2** | **Mutation Generation** | Apply families $NF_1$ through $NF_6$ exhaustively (1 mutant per scenario per family). | Exactly 180 candidate mutants |
| **3** | **Pre-Validation Integrity** | Confirm all 180 mutants satisfy bit-deterministic reproduction rules. | `180 / 180 applicable` |
| **4** | **Schema v2 Evaluation** | Submit each mutant to `validate_trace_v2()` in `core/r6_schema_v2_validator.py`. | Raw validation results (valid/invalid, error categories) |
| **5** | **Cross-Comparison** | In parallel, evaluate each mutant against `validate_trace_v1()` to establish open-world baseline compatibility. | v1 vs. v2 comparative matrix |
| **6** | **Artifact Persistence** | Serialize results, generate summary markdown, and compute SHA-256 digests. | `r6_t4_mutation_results.json`, `r6_t4_mutation_summary.md`, `SHA256SUMS.txt` |

---

## 3. Denominator & Family Partitioning

$$\begin{aligned}
\text{Total Mutants} &= 30 \text{ scenarios} \times 6 \text{ novel families} = 180 \\
NF_1 \ (\text{Unnamespaced Extension Key}) &= 30 \text{ mutants} \\
NF_2 \ (\text{Core Field Shadowing}) &= 30 \text{ mutants} \\
NF_3 \ (\text{Reserved Keyword Injection}) &= 30 \text{ mutants} \\
NF_4 \ (\text{Nested Array Property}) &= 30 \text{ mutants} \\
NF_5 \ (\text{Explicit Null on Non-Nullable Scalar}) &= 30 \text{ mutants} \\
NF_6 \ (\text{Schema Downgrade Injection}) &= 30 \text{ mutants}
\end{aligned}$$

---

## 4. Output Artifacts Specification (When Authorized)
When execution is officially authorized by technical order, the execution script shall generate:
* `validation/article/r6_t4/r6_t4_mutation_results.json`: Complete record of each mutant (scenario ID, family ID, operator, mutated payload diff, v2 result, v1 result, primary error category).
* `validation/article/r6_t4/r6_t4_mutation_summary.md`: Structured breakdown of per-family rejection rates, error category distribution, and claim boundary analysis.
* `validation/article/r6_t4/SHA256SUMS.txt`: Cryptographic checksum manifest.

---

## 5. Change Control Protocol
1. **Pre-Result Modifications**: If family definitions, operators, or target fields must be altered prior to execution, document as a formal protocol deviation in `validation/article/r6_a1_protocol_deviation_log.md` with label `PRE_RESULT_CHANGE`.
2. **Post-Result Freeze**: No operator, denominator, or applicability rule may be altered after observing execution results. Any unexpected result must be recorded as an honest scientific finding rather than tuned away.
