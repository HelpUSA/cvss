# HelpUS CVSS AI v4.0 — Candidate Book Chapter Map

This document establishes the provisional editorial outline for the comprehensive technical monograph and engineering companion book documenting HelpUS CVSS AI v4.0. It maps the 18 candidate chapters to source archive files, scientific artifacts, and figures.

---

## Master Chapter Architecture (18 Chapters)

### Chapter 1: The Vulnerability Prioritization Crisis
* **Purpose**: Establish why CVSS Base scores fail as operational prioritizers and why contextual environmental evaluation is essential.
* **Source Archive Files**: `01_MASTER_TIMELINE.md`, `02_ENGINEERING_DECISION_LOG.md` (ENG-DEC-001).
* **Scientific Artifacts Involved**: NVD statistics, CVE vulnerability volume benchmarks.
* **Candidate Figures**: FIG-ARCH-001, FIG-PIPE-002.
* **Current Completeness**: **HIGH** (Extensive material in early whitepapers and thesis chapters).
* **Dependencies**: None.

### Chapter 2: CVSS v4.0 Mathematical & Formal Foundations
* **Purpose**: In-depth exposition of the CVSS v4.0 specification, vector notation, MacroVectors ($EQ_1..EQ_6$), and metric combinations.
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 1 & 4), `07_METHOD_EVOLUTION_R1_TO_R6.md`.
* **Scientific Artifacts Involved**: FIRST CVSS v4.0 specification, `core/cvss40.py`.
* **Candidate Figures**: FIG-FORM-007.
* **Current Completeness**: **HIGH** (Formally defined and validated in R1).
* **Dependencies**: None.

### Chapter 3: System Architecture & Dual-Engine Decoupling
* **Purpose**: Detail the architectural separation between the official standard calculator and the local environmental policy engine (ADR-001).
* **Source Archive Files**: `02_ENGINEERING_DECISION_LOG.md` (ENG-DEC-001), `ADR-001`.
* **Scientific Artifacts Involved**: `core/cvss40.py`, `core/cvss40_environmental_policy.py`.
* **Candidate Figures**: FIG-ARCH-001.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 4: Automated Evidence Ingestion and Context Resolution
* **Purpose**: Explain how deployment topologies, internet exposure, compensating controls, and asset criticality are extracted and normalized.
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 3), `02_ENGINEERING_DECISION_LOG.md`.
* **Scientific Artifacts Involved**: `core/cvss40_trace_validator.py`, network discovery modules.
* **Candidate Figures**: FIG-PIPE-002.
* **Current Completeness**: **MEDIUM**.
* **Dependencies**: UI input schemas and telemetry documentation.

### Chapter 5: Canonical FIRST Conformance & Metamorphic Stability
* **Purpose**: Document the verification of the official calculator against 486,472 benchmark vectors and 10,000 metamorphic relation runs.
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 1), `02_ENGINEERING_DECISION_LOG.md` (ENG-DEC-002).
* **Scientific Artifacts Involved**: `HELPUS-METAMORPHIC-10K-G9B`, `outputs/first-reference-corpus-results.json`.
* **Candidate Figures**: FIG-VER-020.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 6: The Independent Machine-Checkable Trace Verifier
* **Purpose**: Present the design, implementation, and execution of the standalone runtime verifier (`verify_trace_integrity.py`) and its 464 checks.
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 5), `02_ENGINEERING_DECISION_LOG.md` (ENG-DEC-005).
* **Scientific Artifacts Involved**: `tools/verify_trace_integrity.py`, `validation/article/r2_canonical_trace_verification.json`.
* **Candidate Figures**: FIG-VER-009.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 7: The Controlled Curated Corpus & Priority Shift Findings
* **Purpose**: Describe the 30 canonical scenarios (12 NVD + 18 synthetic), the reconciliation of the 22 priority shifts (73.33%), and LOEO sensitivity.
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 2 & 5), `04_FAILURES_NEGATIVE_RESULTS_AND_RECOVERIES.md` (SCI-001).
* **Scientific Artifacts Involved**: `data/article/cvss40_environmental_scenarios.csv`, `validation/article/r2_priority_sensitivity_analysis.json`.
* **Candidate Figures**: FIG-SENS-010.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 8: Verifier-Agnostic Mutation Testing & Operator Bias
* **Purpose**: Address operator-selection bias; document the 120-mutant randomized campaign (seed 20261021) and the 83 rejected / 37 accepted split.
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 6), `02_ENGINEERING_DECISION_LOG.md` (ENG-DEC-006).
* **Scientific Artifacts Involved**: `tools/generate_random_mutations.py`, `validation/article/r3_randomized_mutation_testing.json`.
* **Candidate Figures**: FIG-MUT-011, FIG-REV-012.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 9: The Discovery of Open-World Boundaries & 34 Limitations
* **Purpose**: Transparent analysis of negative results: Family F3 (0/16 rejections), open-world JSON parsing, and the 34 verifier limitations.
* **Source Archive Files**: `03_SCIENTIFIC_DECISION_LOG.md`, `04_FAILURES_NEGATIVE_RESULTS_AND_RECOVERIES.md` (SCI-002, SCI-003).
* **Scientific Artifacts Involved**: `article/ieee/cvss40_double_blind.tex` (Section VII-A).
* **Candidate Figures**: FIG-MUT-011.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 10: Human Governance, Ethical Clearances, and Protocol Specifications
* **Purpose**: Detail the CEP Plataforma Brasil approval, fail-closed gatekeeping ($G_{10B}, C_1, C_2$), and Option A (Standardized Adjudication Protocol).
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 3 & 4), `03_SCIENTIFIC_DECISION_LOG.md` (Decision 2).
* **Scientific Artifacts Involved**: `scripts/g10b_confirmatory_gate.py`, CEP approval dossier.
* **Candidate Figures**: FIG-ETH-004, FIG-DEC-008.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 11: The Academic Journey: From First Draft to R5 Camera-Ready
* **Purpose**: Chronological narrative of the IEEE peer review cycles (R1, R2, R3, R4, R5), Overleaf builds, and abstract condensation.
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 4, 6, 7), `06_COMMITS_TAGS_AND_ARTIFACTS_INDEX.md`.
* **Scientific Artifacts Involved**: `docs/submission_package/article_main.pdf`, `FINAL_PUBLICATION_FREEZE_MANIFEST.json`.
* **Candidate Figures**: FIG-PUB-006, FIG-REV-014.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 12: The Quest for Top-Tier A1: Strategy and Pre-Registration
* **Purpose**: Rationalize why the team pursued top-tier security venues (IEEE S&P, USENIX Security) and formal pre-registration.
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 8), `docs/research/R6_A1_ROADMAP.md`.
* **Scientific Artifacts Involved**: `validation/article/r6_a1_preregistration.md`, `r6_a1_experiment_registry.json`.
* **Candidate Figures**: FIG-PRER-015.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 13: External Held-Out Corpus Design, Quarantining & Transfer Evaluation
* **Purpose**: Document the automated acquisition of 947 candidates from GitHub Advisory Database, exclusion of 9 malware records, the 938-case cryptographic lock, and the subsequent preregistered held-out transfer evaluation after quarantine release.
* **Source Archive Files**: `02_ENGINEERING_DECISION_LOG.md` (ENG-DEC-007), `03_SCIENTIFIC_DECISION_LOG.md` (Decision 7).
* **Scientific Artifacts Involved**: `tools/acquire_r6_heldout_corpus.py`, `validation/article/r6_heldout/`, T7 result and trace-verification artifacts.
* **Candidate Figures**: FIG-CORP-016.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 14: Closed-World Schema v2 & Decoupled Governance Implementation
* **Purpose**: Technical specification and implementation of recursive closed-world typing (`additionalProperties: false`) and the $OVR$ override model.
* **Source Archive Files**: `02_ENGINEERING_DECISION_LOG.md` (ENG-DEC-008, ENG-DEC-009).
* **Scientific Artifacts Involved**: `core/r6_schema_v2_validator.py`, `core/r6_governance_override.py`.
* **Candidate Figures**: FIG-SCH-017, FIG-GOV-019.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 15: From T2 Protocol Deviation to R6.1 Resolution
* **Purpose**: Deep-dive into the original 30/30 unclassified result, the taxonomy gap, the refusal to silently coerce data, the creation of the R6.1 orthogonal model, and the completed T2R compatibility rerun.
* **Source Archive Files**: `01_MASTER_TIMELINE.md` (Epoch 8), `04_FAILURES_NEGATIVE_RESULTS_AND_RECOVERIES.md` (SCI-004), `validation/article/r6_a1_protocol_deviation_log.md`.
* **Scientific Artifacts Involved**: `validation/article/r6_t2/`, `validation/article/r6_1_t2_compatibility_taxonomy.md`.
* **Candidate Figures**: FIG-TAX-018.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None for the experimental result. R6.1-T2R is complete and frozen; the chapter should now incorporate the rerun outcome and protocol-deviation resolution.

### Chapter 16: Multi-Agent Collaboration, Tooling, and E2E Quality Assurance
* **Purpose**: How Antigravity, ChatGPT, and Gemini collaborated via `ai-bridge-local`; Playwright synthetic user journeys; WebKit CSS fixes.
* **Source Archive Files**: `02_ENGINEERING_DECISION_LOG.md` (ENG-DEC-003, ENG-DEC-004), `04_FAILURES_NEGATIVE_RESULTS_AND_RECOVERIES.md` (OP-001..003).
* **Scientific Artifacts Involved**: `ai-bridge-local`, `tests/e2e/`.
* **Candidate Figures**: FIG-COMM-003, FIG-E2E-005.
* **Current Completeness**: **HIGH**.
* **Dependencies**: None.

### Chapter 17: Lessons Learned: Epistemological Rigor in Applied Security AI
* **Purpose**: Philosophical and practical takeaways: pre-registration in security engineering, the danger of metric vanity, and the value of honest boundaries.
* **Source Archive Files**: `03_SCIENTIFIC_DECISION_LOG.md`, `04_FAILURES_NEGATIVE_RESULTS_AND_RECOVERIES.md`.
* **Scientific Artifacts Involved**: Synthesized project retrospective.
* **Candidate Figures**: Conceptual summary matrices.
* **Current Completeness**: **HIGH** for the R6-A1 retrospective; additional publication lessons may be appended after external peer-review outcomes.
* **Dependencies**: None for the R6-A1 retrospective.

### Chapter 18: Research Roadmap: Toward Automated Autonomous Cyber Defense
* **Purpose**: Future outlook: scaling to hundreds of thousands of advisories, dynamic eBPF evidence collection, and formal verification with SMT solvers.
* **Source Archive Files**: `docs/research/R6_A1_ROADMAP.md` (Phase R6-7).
* **Scientific Artifacts Involved**: Long-term HelpUS architectural plans.
* **Candidate Figures**: Future architecture diagrams.
* **Current Completeness**: **MEDIUM** (intentionally forward-looking).
* **Dependencies**: External publication outcomes may refine priorities but are not required to draft the roadmap.
