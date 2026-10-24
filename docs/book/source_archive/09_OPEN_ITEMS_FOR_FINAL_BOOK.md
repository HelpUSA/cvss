# HelpUS CVSS AI v4.0 — Open Items and Gaps for Final Book

This document catalogs the outstanding editorial, publication, and human-validation items that remain after completion of the R6-A1 experimental campaign. It supersedes the earlier pre-execution status language and is reconciled against the frozen repository state as of 2026-10-24.

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

## 3. Completed R6-A1 Experimental Campaign (`EXPERIMENT_COMPLETE`)

The experimental items previously listed here as pending have now been executed and frozen in Git. They are no longer blockers for the current book revision:

1. **R6.1-T2R — Backward Compatibility Rerun**
   - *Status*: `COMPLETED_FROZEN`.
   - *Result*: 30/30 legacy/non-canonical records rejected under the orthogonal compatibility taxonomy (12 `INVALID_TYPE`, 18 `INVALID_ENUM`).

2. **T3 — Historical Mutation Replay on Schema v2**
   - *Status*: `COMPLETED_FROZEN`.
   - *Result*: 120/120 historical mutations rejected, including 16/16 Family F3 injections.

3. **T4R / NF2-R — Closed-World Mutation Campaign**
   - *Status*: `COMPLETED_FROZEN`.
   - *Result*: 75/90 attributable rejections in the primary valid-parent campaign and 15/15 rejections in the NF2-R companion campaign.

4. **T5-R — Governance Contract Verification**
   - *Status*: `COMPLETED_FROZEN`.
   - *Result*: 8/8 governance invariants satisfied; Equation 8 remained unchanged; zero autonomous overrides were introduced.

5. **T6 — NVD Representability**
   - *Status*: `COMPLETED_FROZEN`.
   - *Result*: 2/4 cases were normatively representable; 2/4 correctly required external environmental evidence, with no invented data.

6. **Differential Validation R2**
   - *Status*: `COMPLETED_FROZEN`.
   - *Result*: 454,047/461,444 exact score matches (98.3970%) and 25,028/25,028 negative-case agreements against `cvss4py` under deterministic parity conditions.

7. **T7 — External Held-Out Transfer**
   - *Status*: `COMPLETED_FROZEN`.
   - *Result*: 938 GitHub Advisory Database records evaluated; 339 nominally calculable and 599 fail-closed rejections; all 938 traces verified across 3,232 diagnostic checks.

The remaining confirmatory work is distinct from R6-A1: expert adjudication and the separately governed G10B/C1/C2 confirmatory protocol remain future work and must not be conflated with the completed R6-A1 held-out transfer.

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
   - *Status*: R6-A1 experimentation is complete and frozen; the manuscript has undergone post-R6 editorial consolidation and camera-ready typography review.
   - *Action for Book*: Keep Chapter 11 and Chapter 12 synchronized with the actual submission venue, acceptance/review outcome, and artifact-evaluation status as those external events occur.
2. **Epilogue and Post-R6 Retrospective**:
   - *Action for Book*: Chapter 17 can now incorporate the completed R6-A1 empirical retrospective. Chapter 18 remains intentionally forward-looking and should clearly separate validated results from proposed future research.

---

## 6. Artifact Verification Ledger (`ARTIFACT_PENDING`)

1. **Overleaf Monograph Companion ZIP Update**:
   - *Current Baseline*: the consolidated monograph is recorded as 51 pages in `docs/ARTICLE_STATUS.md`; the older Round-4 Overleaf ZIP remains a historical 50-page artifact.
   - *Action for Book*: produce a refreshed Overleaf bundle and cryptographic manifest after the 18-chapter editorial expansion is materially drafted; do not label the historical Round-4 ZIP as the current book.
