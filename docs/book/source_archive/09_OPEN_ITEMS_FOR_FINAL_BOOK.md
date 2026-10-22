# HelpUS CVSS AI v4.0 — Open Items and Gaps for Final Book

This document catalogs the outstanding gaps, pending experimental results, and editorial tasks required before the final technical monograph can be published. It ensures complete transparency regarding what remains unfinished.

---

## 1. History Gaps (`HISTORY_GAP`)

1. **Early Genesis Sessions (May 2026)**:
   - *Description*: Raw conversational transcripts prior to October 2026 occurred across earlier chat sessions outside the current Antigravity thread (`52c43697-a431-4abf-a13d-6a5d1cb0b95b`).
   - *Status*: Reconstructed from Git commit logs, `docs/ADR-001`, and early markdown notes.
   - *Action for Book*: Cross-reference local backup archives in `_archive/legacy_zips_patches/` to recover any specific developer dialogue.
2. **Intermediate Deliberation Contexts in External Tabs**:
   - *Description*: Certain multi-agent debates between Gemini and ChatGPT in late September 2026 were bridged via text envelopes; some transient UI chat text was not stored in the repository.
   - *Status*: Core consensus and decisions are preserved in `ai-bridge-local/logs/` and Git commit messages.

---

## 2. Figure and Vector Gaps (`FIGURE_GAP`)

1. **High-Resolution Vector Rendering of Core Mermaid Diagrams**:
   - *Description*: The 11 standalone Mermaid diagrams in [`figures/`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/) and the 20 figures in the inventory currently exist as text-based `.mmd` files.
   - *Action for Book*: Render all 20 figures to vector PDF/SVG using headless Mermaid CLI (`@mermaid-js/mermaid-cli`) or TikZ for seamless inclusion in LaTeX.
2. **Reconstruction of CEP Plataforma Brasil Form Workflow**:
   - *Description*: Diagram `FIG-ETH-004` represents the ethical workflow textually; an official high-resolution flowchart matching Brazilian regulatory standards should be prepared for Chapter 10.

---

## 3. Pending Experimental Executions (`EXPERIMENT_PENDING`)

1. **Experiment R6.1-T2R (Backward Compatibility Rerun)**:
   - *Status*: `PREREGISTERED_NOT_EXECUTED`.
   - *Requirement*: Awaiting official supervisor authorization to execute the rerun under the frozen R6.1 orthogonal taxonomy.
2. **Experiment T3 (Mutation Replay on Schema v2)**:
   - *Status*: `NOT_EXECUTED`.
   - *Requirement*: Re-evaluate the 120 randomized mutants from R3 under Schema v2 to empirically test the hypothesis that closed-world validation rejects Family F3 injections.
3. **Experiment T4 (New Target Mutants)**:
   - *Status*: `NOT_EXECUTED`.
   - *Requirement*: Generate and evaluate newly structured mutation families targeting closed-world boundaries.
4. **Experiment T6 (NVD Representability & Generalization)**:
   - *Status*: `NOT_EXECUTED`.
5. **Experiment T7 (External Held-Out Corpus Evaluation)**:
   - *Status*: `NOT_EXECUTED` (Quarantine strictly maintained; `held_out_accessed = false`).
   - *Requirement*: Execute the full contextual pipeline across the 938 locked GitHub Advisory Database cases.

---

## 4. Human Adjudication & Clinical Validation (`AUTHORSHIP/DOUBLE_BLIND`)

1. **Double-Blind Anonymity De-Anonymization**:
   - *Current State*: The IEEE article and repository maintain strict double-blind protocols; institution names, author identities, and specific hospital infrastructure identifiers are redacted.
   - *Action for Book*: Once the academic review cycle is complete, the book will restore full authorship credits, laboratory acknowledgments, and ethical dossier numbers.
2. **Independent Expert Adjudication Execution**:
   - *Current State*: `PROTOCOL_SPECIFIED_NOT_COMPLETED`.
   - *Action for Book*: If human panel adjudication is completed under the pre-registered protocol, include the inter-rater reliability metrics (Fleiss' Kappa / Krippendorff's Alpha) in Chapter 10.

---

## 5. Editorial and Manuscript Finalization (`EDITORIAL_PENDING`)

1. **Top-Tier A1 Article Freeze**:
   - *Status*: The manuscript for top-tier security venues (IEEE S&P / USENIX Security) is currently in pre-registration phase (R6-A1).
   - *Action for Book*: Update Chapter 11 and Chapter 12 with final acceptance reviews, camera-ready diffs, and artifact evaluation badges.
2. **Epilogue and Post-R6 Retrospective**:
   - *Action for Book*: Chapter 17 (Lessons Learned) and Chapter 18 (Roadmap) require writing after the full Phase R6 empirical results are analyzed.

---

## 6. Artifact Verification Ledger (`ARTIFACT_PENDING`)

1. **Overleaf Monograph Companion ZIP Update**:
   - *Current Baseline*: `book_latex/helpus_cvss_ai_monograph_overleaf_final_round4.zip` (50 pages).
   - *Action for Book*: Compile the 18-chapter extended monograph into a refreshed Overleaf bundle once all chapters are drafted.
