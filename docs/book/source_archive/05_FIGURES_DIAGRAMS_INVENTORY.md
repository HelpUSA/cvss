# HelpUS CVSS AI v4.0 — Figures and Diagrams Inventory

This inventory catalogs the architectural diagrams, sequence flows, state machines, and experimental pipelines developed across all project phases. Standalone diagram source files are preserved under [`docs/book/source_archive/figures/`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/).

---

## 1. Inventory Summary
* **Total Identified Diagrams in Archive**: 87 unique Mermaid blocks.
* **Core Curated Figures for Monograph**: 20 primary architectural figures.
* **Standalone `.mmd` Files Extracted**: 11 standalone diagram sources.
* **Status Legend**:
  - `CURRENT`: Actively used in ongoing R6/R6.1 specifications.
  - `CANDIDATE_FOR_BOOK`: High pedagogical and historical value for monograph publication.
  - `HISTORICAL`: Documents a specific past milestone or baseline.
  - `SUPERSEDED`: Architecture evolved into a later version, but preserved for comparative analysis.

---

## 2. Core Monograph Figure Registry

| Figure ID | Title / Description | Diagram Type | Phase / Origin | Source Reference | Status | Candidate Book Chapter | Editorial Redraw? | Standalone File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FIG-ARCH-001** | Dual-Engine Separation: Official Calculator Core vs Contextual Environmental Policy | `flowchart TD` | Phase 1 (Genesis) | Step 127 / ADR-001 | `CANDIDATE_FOR_BOOK` | Chapter 3 (Architecture) | YES (Vector Polish) | [`fig01_cvss40_core_architecture.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig01_cvss40_core_architecture.mmd) |
| **FIG-PIPE-002** | Evidence Ingestion, Network Interface Auto-Discovery and Assessment Trigger | `flowchart LR` | Phase 1 / Scanner | Step 303 / 342 | `HISTORICAL` | Chapter 4 (Evidence Pipeline) | YES (Vector Polish) | [`fig02_evidence_pipeline.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig02_evidence_pipeline.mmd) |
| **FIG-COMM-003** | Local AI Bridge Multi-Agent Orchestration Architecture (:8766 Gateway) | `flowchart LR` | Phase 2 / Tooling | Step 8466 / HU-STD-048 | `CANDIDATE_FOR_BOOK` | Chapter 16 (Multi-Agent Collab) | YES (Vector Polish) | [`fig03_ai_bridge_inter_agent.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig03_ai_bridge_inter_agent.mmd) |
| **FIG-ETH-004** | Plataforma Brasil / CEP Ethical Approval Workflow for Clinical & Enterprise Vulnerability Trials | `flowchart LR` | Phase 2 / Ethical | Step 9587 / CEP Dossier | `HISTORICAL` | Chapter 10 (Governance & Ethics) | NO | Extracted in notes |
| **FIG-E2E-005** | Playwright Synthetic E2E Isolation on Disposable PostgreSQL with Viewport Matrix | `flowchart TD` | PR #41 / PR #42 | Step 16246 / PR-42 | `CANDIDATE_FOR_BOOK` | Chapter 16 (Testing & QA) | NO | Extracted in notes |
| **FIG-PUB-006** | Dual Publication Baseline Freeze Pipeline (IEEE Article + Companion Monograph) | `flowchart TD` | Publication Freeze | Step 19733 / `5226f74` | `HISTORICAL` | Chapter 11 (Publication Journey) | YES | [`fig04_publication_freeze_dual_pipeline.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig04_publication_freeze_dual_pipeline.mmd) |
| **FIG-FORM-007** | CVSS v4.0 Formal Nomenclature ($B, BT, BE, BTE$) and MacroVectors ($EQ_1..EQ_6$) | `flowchart TD` | Revision R1 | Step 20180 / R1-083 | `CANDIDATE_FOR_BOOK` | Chapter 2 (CVSS v4.0 Formalism) | NO | [`fig05_cvss40_macrovector_nomenclature.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig05_cvss40_macrovector_nomenclature.mmd) |
| **FIG-DEC-008** | Tripartite Consensus & Strategic Adoption of Option A (Standardized Adjudication Protocol) | `flowchart TD` | Post-R1 Consolidation | Step 20861 / POSTR1-084 | `CANDIDATE_FOR_BOOK` | Chapter 10 (Governance Model) | YES | [`fig06_adjudication_protocol_option_a.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig06_adjudication_protocol_option_a.mmd) |
| **FIG-VER-009** | Independent Trace Verifier Architecture: 464 Structural & Recomputational Checks | `flowchart TD` | Revision R2 | Step 22138 / `c41065e` | `CANDIDATE_FOR_BOOK` | Chapter 6 (Independent Verifier) | YES | [`fig07_trace_verifier_r2_pipeline.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig07_trace_verifier_r2_pipeline.mmd) |
| **FIG-SENS-010** | Leave-One-Evidence-Out (LOEO) Priority Sensitivity & Permutation Stability Matrix | `flowchart TD` | Revision R2 | Step 22820 / CMD-160 | `CANDIDATE_FOR_BOOK` | Chapter 7 (Empirical Corpus) | YES | [`fig08_priority_sensitivity_loeo.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig08_priority_sensitivity_loeo.mmd) |
| **FIG-MUT-011** | Verifier-Agnostic Randomized Mutation Campaign (Seed 20261021: 83 Rejected / 37 Accepted) | `flowchart TD` / `pie` | Revision R3 | Step 23779 / `073fa7d` | `CANDIDATE_FOR_BOOK` | Chapter 8 (Mutation Testing) | YES (Combined Pie+Flow) | [`fig09_r3_randomized_mutation_pipeline.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig09_r3_randomized_mutation_pipeline.mmd) |
| **FIG-REV-012** | Major Revision R3 End-to-End Hardening & Synchronous Artifact Freeze | `flowchart TD` | Revision R3 | Step 24126 / R3-Freeze | `HISTORICAL` | Chapter 8 (Mutation Testing) | NO | Extracted in notes |
| **FIG-REV-013** | Micro-Revision R4 Conceptual Polish & Subobject Injection Clarification Pipeline | `flowchart TD` | Revision R4 | Step 24239 / `cb8ab69` | `SUPERSEDED` | Chapter 11 (Publication Journey) | NO | Extracted in notes |
| **FIG-REV-014** | Micro-Revision R5 Camera-Ready Pipeline (Abstract Polish & Commit `cc4418e`) | `flowchart TD` | Revision R5 | Step 24301 / `cc4418e` | `HISTORICAL` | Chapter 11 (Publication Journey) | NO | Extracted in notes |
| **FIG-PRER-015** | Phased Preregistration Lifecycle for Top-Tier A1 Security Venues (R6-0 to R6-7) | `flowchart TD` | Phase R6-0 | `R6_A1_ROADMAP.md` | `CURRENT` | Chapter 12 (A1 Strategy) | NO | Extracted in notes |
| **FIG-CORP-016** | Deterministic External Held-Out Acquisition & Exclusion Pipeline (947 -> 938) | `flowchart TD` | Phase R6-2 | Step 24650 / `12bf6c4` | `CURRENT` | Chapter 13 (Held-Out Design) | YES | Extracted in notes |
| **FIG-SCH-017** | Dual Validation Evaluation Engine: Schema v1 (Open-World) vs Schema v2 (Closed-World) | `flowchart TD` | Phase R6-1 / T2 | Step 25138 / `CMD-239` | `CURRENT` | Chapter 14 (Schema v2 Design) | YES | [`fig10_r6_schema_validation_architecture.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig10_r6_schema_validation_architecture.mmd) |
| **FIG-TAX-018** | R6.1 Orthogonal State-Complete Compatibility Taxonomy ($5 \times 8$ State Matrix) | `flowchart TD` | Phase R6.1 | Step 25188 / `bfaece2` | `CURRENT` | Chapter 15 (T2 Unexpected Finding) | YES (Vector Polish) | [`fig11_r6_1_orthogonal_compatibility_taxonomy.mmd`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/fig11_r6_1_orthogonal_compatibility_taxonomy.mmd) |
| **FIG-GOV-019** | Decoupled Governance Override Architecture ($OVR$) and Equation 8 Mathematical Invariance | `flowchart LR` | Phase R6-1 | Specification Doc | `CURRENT` | Chapter 14 (Schema v2 Design) | YES | Extracted in notes |
| **FIG-VER-020** | Secondary Scorer Concordance Verification Pipeline (Differential CVSS v4.0 Engine) | `flowchart LR` | Phase R6-3 | RQ-R6-4 Design | `CURRENT` | Chapter 5 (Canonical Compatibility) | YES | Extracted in notes |

---

## 3. Preservation of Historical & Superseded Figures

The companion book explicitly retains figures that were superseded during research. For example:
* **FIG-REV-013 (R4 Pipeline)** was superseded by the R5 camera-ready pipeline, but illustrates how the team clarified open-world parsing prior to abstract condensation.
* **FIG-PUB-006 (Publication Freeze)** represents the original 7-page IEEE article baseline before the major revision cycles expanded it into a 9-page machine-verifiable manuscript.
