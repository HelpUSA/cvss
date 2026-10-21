# HelpUS CVSS AI v4.0 — Methodological Evolution (R1 to R6.1)

This document traces the factual, comparative evolution of the HelpUS CVSS AI validation methodology across major revision generations: from early open-world heuristics to formal closed-world contracts and pre-registered anti-retuning governance.

---

## 1. Evolution Overview Matrix

| Generation / Milestone | Core Paradigm | Primary Structural Artifact | Verification Rigor | Key Limitation Discovered | Consequence for Next Cycle |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Genesis & R1** | Heuristic Prioritization & Dual-Engine | FIRST Concordance Harness | Unit tests + FIRST 486k vector concordance | Ambiguity in nomenclature ($B$ vs $BE$) and missing formal MacroVectors | Refactored notation; defined MacroVectors $EQ_1..EQ_6$; added 6-stage architecture |
| **Post-R1 & R2** | Machine-Verifiable Track | Independent Trace Verifier (`verify_trace_integrity.py`) | 464 independent assertions across 30 traces | Relied on open-world JSON parsing; narrative text unvalidated | Motivated adversarial and randomized mutation testing |
| **Revision R3** | Randomized Mutation Complement | Verifier-Agnostic Mutation Generator (`tools/generate_random_mutations.py`) | 120 randomized mutants (Seed 20261021) | Family F3 (subobject injection) 100% accepted ($0/16$ rejected) by open-world parser | Established empirical proof that open-world schemas cannot prevent attribute injection |
| **Revision R4 & R5** | Camera-Ready Consolidation | IEEE Double-Blind Article (7-9 pages) | Full regression suite + LaTeX 0 Overfull `\hbox` | Paper reached page ceiling; evaluation restricted to 30 historical cases | Target top-tier A1 security venues with large external held-out corpus |
| **Phase R6-A1** | Pre-Registered Closed-World & Governance | Schema v2 (`r6_schema_v2_validator.py`) + Decoupled Governance ($OVR$) | Pre-registered hypotheses (RQ-R6-1..4) + 938 held-out advisories | Preregistered 4-category taxonomy coupled v1-valid/v2-invalid solely to `UNDECLARED_FIELD` | T2 canonical run observed 30/30 unclassified cases due to `INVALID_TYPE` and `INVALID_ENUM` |
| **Phase R6.1** | Orthogonal State-Complete Compatibility | R6.1 Compatibility Contract (`r6_1_t2_compatibility_contract.json`) | State-complete Boolean product $\{v_1\} \times \{v_2\} \times \{\text{norm}\}$ + orthogonal error | Re-run pending formal authorization; held-out preserved in quarantine | Protocol deviation `R6-DEV-001` logged as `POST_RESULT_CHANGE`; ready for R6.1-T2R |

---

## 2. Detailed Generation Profiles

### Generation R1: Formalization of CVSS v4.0 Notation and MacroVectors
* **Objective**: Transition from informal contextual scoring to rigorous alignment with the FIRST CVSS v4.0 standard.
* **Inputs & Evidence**: 486,472 benchmark vectors from FIRST; 30 curated enterprise scenarios.
* **Methodology**: Formalized nomenclature distinguishing $B$ (Base), $BT$ (Base + Threat), $BE$ (Base + Environmental), and $BTE$ (Base + Threat + Environmental). Defined MacroVector lookup algorithms ($EQ_1$ to $EQ_6$).
* **Validation**: $486,472 / 486,472$ concordance with the FIRST reference implementation; 10,000 metamorphic executions ($HELPUS-METAMORPHIC-10K-G9B$) with 0 violations.
* **Result**: Proven numerical equivalence with the official standard.
* **Limitation Discovered**: Peer reviewers noted that while the math was verified, the JSON traces themselves lacked machine-checkable integrity guarantees.
* **What Changed Next**: Shifted focus in R2 to build an independent runtime verifier.
* **Preserved Historical Result**: 486,472 FIRST conformance and 10k metamorphic relations remain permanent invariants.

---

### Generation R2: The Independent Machine-Verifiable Track
* **Objective**: Enable third-party reviewers to audit all 30 scenario traces without installing the runtime web stack.
* **Inputs & Evidence**: 30 canonical JSON traces (`SCN-NVD-001.json` through `SCN-SYN-030.json`).
* **Methodology**: Built `tools/verify_trace_integrity.py` executing 464 independent assertions covering trace completeness, vector syntax, formula recomputation, and review status. Conducted LOEO priority sensitivity analysis.
* **Validation**: $464 / 464$ checks passed; 2/30 ($6.7\%$) LOEO sensitivity shifts observed.
* **Result**: Achieved machine-verifiable reproducibility.
* **Limitation Discovered**: Cataloged 34 explicit limitations. The verifier used standard Python `json.load()` (open-world), meaning arbitrary extra keys were silently ignored.
* **What Changed Next**: Designed mutation testing in R3 to measure operator detection boundaries.
* **Preserved Historical Result**: The 464 verifier assertions and 34 cataloged limitations remain frozen in R2 artifacts.

---

### Generation R3: Verifier-Agnostic Randomized Mutation
* **Objective**: Measure verifier robustness against unbiased, non-directed perturbations to eliminate operator-selection bias.
* **Inputs & Evidence**: 6 representative scenarios ($3\text{ NVD} + 3\text{ Synthetic}$); seed `20261021`.
* **Methodology**: Implemented an isolated generator applying 9 randomized mutation operators (F1–F9) across structural and field-level components.
* **Validation**: Submitted 120 applicable mutants to the verifier.
* **Result**: 83 rejected ($69.2\%$), 37 accepted ($30.8\%$).
* **Limitation Discovered**: Mutation Family F3 (attribute/subobject injection) resulted in **$0 / 16$ rejections** ($100\%$ accepted). The verifier was completely blind to undeclared subobjects.
* **What Changed Next**: Formulated closed-world schema contracts (Schema v2) as the next major architectural evolution.
* **Preserved Historical Result**: The $83/120$ ($69.2\%$) rejection rate and F3 $0/16$ finding remain permanent historical evidence.

---

### Generation R4 & R5: Conceptual Boundary Polish and Camera-Ready Freeze
* **Objective**: Integrate mutation findings into the IEEE manuscript and condense the text for camera-ready submission.
* **Inputs & Evidence**: 9-page IEEE double-blind LaTeX manuscript.
* **Methodology**: Detailed the open-world vs closed-world boundary in Section VII-A. Condensed the abstract to satisfy strict length limits while retaining all core metrics.
* **Validation**: LaTeX build with 0 Overfull `\hbox`; double-blind anonymity verified.
* **Result**: Camera-ready freeze tagged at `cc4418e` (merged via PR #47 `e5215b5`).
* **Limitation Discovered**: The 30-scenario corpus, while internally valid, is insufficient for top-tier security conferences (IEEE S&P, USENIX Security), which demand hundreds of external real-world cases.
* **What Changed Next**: Launched Phase R6 with pre-registered hypotheses and an external held-out corpus.
* **Preserved Historical Result**: R5 camera-ready PDF and Overleaf bundle remain cryptographically sealed.

---

### Generation R6: Pre-Registration, External Held-Out, and Closed-World Schema v2
* **Objective**: Scale validation to top-tier A1 standards with pre-registered hypotheses, a 938-case external held-out corpus, and strict closed-world validation.
* **Inputs & Evidence**: 938 eligible CVSS v4.0 advisories from GitHub Advisory Database (Sept 2026); 30 canonical historical traces.
* **Methodology**: Enacted pre-registered falsification rules (`r6_a1_preregistration.md`). Specified and implemented Schema v2 (`r6_schema_v2_validator.py`) with recursive closed-world typing (`additionalProperties: false`), and built the decoupled Governance Override Model ($OVR$).
* **Validation**: 39 implementation unit/contract tests passing ($100\%$). Executed Experiment T2 (Backward Compatibility).
* **Result**: Schema v1 validated 30/30 ($100\%$). Schema v2 validated 0/30 ($0\%$).
* **Limitation Discovered (The T2 Gap)**: The pre-registered 4-category compatibility model assumed traces would be `V1_VALID_V2_VALID` and that any v1-valid/v2-invalid trace would fail due to `UNDECLARED_FIELD`. In reality, historical traces failed v2 due to `INVALID_TYPE` (12 NVD) and `INVALID_ENUM` (18 Synthetic). All 30 traces were unclassifiable under the frozen model.
* **What Changed Next**: Refused silent coercion; halted execution under `NEEDS_REVIEW` and logged formal protocol deviation `R6-DEV-001`.
* **Preserved Historical Result**: The 30 unclassified outcomes are permanently preserved in `validation/article/r6_t2/`.

---

### Generation R6.1: Orthogonal State-Complete Compatibility Taxonomy
* **Objective**: Resolve the modeling gap of Experiment T2 without altering the locked Schema v2 validator or rewriting historical results.
* **Inputs & Evidence**: The 30 canonical historical traces; protocol deviation `R6-DEV-001`.
* **Methodology**: Formalized an orthogonal, state-complete taxonomy partitioning the Cartesian space $\{v_1\} \times \{v_2\} \times \{\text{norm}\}$ into 5 macro categories, while isolating diagnostic causes into an independent orthogonal dimension (`v2_error_category`).
* **Validation**: Formal verification of contract completeness; JSON syntax validation; leak audit.
* **Result**: Taxonomy frozen in `validation/article/r6_1_t2_compatibility_taxonomy.md` (commit `bfaece2`).
* **Current Status**: R6.1-T2R rerun is pre-registered and ready for execution upon authorization.
