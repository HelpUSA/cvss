# HelpUS CVSS AI v4.0 — Non-Human Technical Validation Protocol

**Protocol Version:** 1.0.0  
**Status:** OFFICIAL PROTOCOL (Consensus CG-20261013-028 / GM-20261013-002)  
**Methodology:** Metamorphic Testing, Property-Based Invariant Verification & Adversarial Robustness  

---

## 1. Scientific Rational and Scope

The primary scientific validation of the **HELPUS CVSS AI v4.0** autonomous system is structured entirely around **reproducible, deterministic engineering evidence**, removing the subjectivity, inter-rater variability, and clinical/ethical recruitment bottlenecks of human expert panels.

By decoupling the primary study from human subjects, the validation satisfies rigorous standards of verification (IEEE/ACM and NIST AI RMF):
* Mathematical proofs against the canonical reference corpus (FIRST CVSS v4.0);
* Metamorphic property testing over tens of thousands of generated operational environments;
* Adversarial stress testing under corrupted, stale, and contradictory telemetry;
* Clean-room deterministic replay.

---

## 2. Experimental Pillars

```text
+-----------------------------------------------------------------------------------+
|                        HELPUS CVSS AI VALIDATION PILLARS                          |
+-----------------------------------------------------------------------------------+
| 1. Normative FIRST Conformance    | 486,472 Official Vectors (Gate G1: 0 divergence) |
| 2. Metamorphic Invariant Testing | 4 Core Properties (MR-1 to MR-4) across 10,000 runs|
| 3. Fail-Closed Abstention Path   | Graceful Degradation to ABSTAIN with Score Envelope |
| 4. Clean-Room Reproducibility    | Isolated Venv Execution & Bit-Identical Artifacts  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Metamorphic Relations (MR) Specification

A metamorphic relation defines an invariant relationship between the inputs and outputs of multiple executions of the system, even when an oracle for individual outputs is absent.

### MR-1: Monotonicity of Criticality
* **Definition:** Increasing the data classification or regulatory criticality of an asset must **never decrease** the Confidentiality or Integrity Requirements ($CR$ or $IR$), and must **never decrease** the resulting environmental score $Score_{env}$.
* **Formally:** 
  $$\forall e_1, e_2 \text{ where } \text{Criticality}(e_2) > \text{Criticality}(e_1) \implies CR(e_2) \ge CR(e_1) \land Score(e_2) \ge Score(e_1)$$

### MR-2: Defense Removal Monotonicity
* **Definition:** Removing an active defensive mitigation (e.g. disabling microsegmentation or disabling MFA) must **never produce a lower severity score** than the defended configuration.
* **Formally:**
  $$\text{Defenses}(e_{unprotected}) \subset \text{Defenses}(e_{protected}) \implies Score(e_{unprotected}) \ge Score(e_{protected})$$

### MR-3: Context Permutation Invariance
* **Definition:** Permuting the order of JSON keys, tags, or metadata declarations in the asset profile must **never alter the resolved metric values or the final score**.
* **Formally:**
  $$\forall \pi \in \text{Permutations}(\text{Evidence}) \implies f(\pi(\text{Evidence})) \equiv f(\text{Evidence})$$

### MR-4: Irrelevant Control Invariance
* **Definition:** Introducing an unrelated defensive control that does not map to the vulnerable component (e.g. adding a database backup tag to an unauthenticated network service) must **never alter the unrelated CVSS metrics**.
* **Formally:**
  $$\forall c_{irrelevant} \implies f(\text{Evidence} \cup \{c_{irrelevant}\}) \equiv f(\text{Evidence})$$

---

## 4. Adversarial and Corrupted Telemetry Testing

The system must demonstrate **100% fail-closed resilience** under intentionally poisoned or degraded telemetry:

1. **Stale Telemetry:** Telemetry age $> 1.0$ day for dynamic network reachability $\longrightarrow$ Engine transitions to `ABSTAIN` (`auto_downgrade_permitted: false`).
2. **Contradictory Tags:** Asset tagged simultaneously as `internet_exposed: true` and `airgapped: true` $\longrightarrow$ Engine detects conflict and transitions to `ABSTAIN`.
3. **Truncated IaC Profiles:** Missing mandatory schema fields $\longrightarrow$ Graceful emission of `HUMAN_REVIEW_REQUIRED` with Bounded Severity Envelope $[Score_{min}, Score_{max}]$.

---

## 5. Technical Release Gate Roadmap

In accordance with CG-20261013-028, the legacy human gates are remapped to technical gates:

| Gate | Name / Scope | Criteria | Status |
| :---: | :--- | :--- | :---: |
| **G1–G8** | Canonical Engineering Baseline | FIRST Corpus, Clean-Room, Security Tests, Production Byte-Identity | **PASS / CLOSED** |
| **G9-LEGACY** | Human Expert Study (CEP/IRB) | Retained as optional future extension | **PRESERVED_HISTORICAL** |
| **G9A** | Environmental Rule Catalog Verification | 100% test coverage of all declarative rules in Catalog v1.0.0 | **READY_FOR_EXECUTION** |
| **G9B** | Synthetic & Metamorphic Validation | 0 violations across MR-1, MR-2, MR-3, MR-4 on 10,000 synthetic profiles | **READY_FOR_EXECUTION** |
| **G10A** | Autonomous Context Pipeline Freeze | Bit-identical clean-room execution; cryptographic hash sealing | **PENDING_G9B** |
