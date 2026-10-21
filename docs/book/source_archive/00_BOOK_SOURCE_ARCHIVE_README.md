# HelpUS CVSS AI v4.0 — Book Source Archive

## 1. Overview & Purpose

This archive serves as the official, permanent historical repository for the forthcoming **Technical Monograph & Engineering Companion Book** documenting the development, verification, and governance of the **HelpUS CVSS AI v4.0** system.

Unlike a compressed academic conference paper (such as the 9-page IEEE double-blind manuscript), the book is designed to provide an unvarnished, deep-dive account of the **entire scientific and engineering lifecycle**. It captures:
- Not just the final, polished algorithms, but the initial hypotheses and why they were revised;
- Architectural trade-offs, discarded alternatives, and multi-agent deliberations;
- Failures, timeouts, negative experimental results, and how they were systematically recovered;
- Formal protocol deviations (`POST_RESULT_CHANGE`) and the epistemological discipline required to prevent post-hoc retuning;
- Complete traceability from commit hashes, cryptographic manifests, and raw traces to the final publication artifacts.

---

## 2. Epistemological and Governance Guardrails

To prevent historical archival work from contaminating current academic submissions or ongoing experiments, the following invariants are strictly enforced:

1. **Strict Separation of Concerns**: This archive is purely **documental and editorial**. It does not alter, re-score, or retroactively reinterpret any experimental dataset.
2. **Scientific Baseline Immutability**:
   - The R5 camera-ready publication freeze remains immutable (`cc4418e` / `e5215b5`).
   - The R6 specification freeze (`090ad8b`) and implementation freeze (`43664e5`) remain locked.
   - The original Experiment T2 evaluation results (`validation/article/r6_t2/*`) remain byte-for-byte immutable.
   - Protocol deviation `R6-DEV-001` and the R6.1 orthogonal taxonomy (`bfaece2`) remain locked.
3. **Quarantine of Held-Out Data**: The held-out corpus in `validation/article/r6_heldout/` is **never opened or analyzed** for book drafting.
4. **Intocabilidade dos Gates de Governança**: Confirmatory datasets $C_1, C_2$ and gatekeeper script `scripts/g10b_confirmatory_gate.py` remain sealed and unexecuted.
5. **No Overclaims**: No claims of "formal verification", "autonomous AI scoring", or "100% bug-free operation" are permitted. The book explicitly details the 34 documented limitations and the 37 accepted randomized mutations.

---

## 3. Archive Inventory & Structure

The archive is organized into the following modules:

| Document | Title | Purpose |
| :--- | :--- | :--- |
| [`01_MASTER_TIMELINE.md`](file:///d:/AntiG/cvss/docs/book/source_archive/01_MASTER_TIMELINE.md) | Master Project Timeline | Comprehensive chronological evolution from initial CVSS v4.0 core to R6.1 |
| [`02_ENGINEERING_DECISION_LOG.md`](file:///d:/AntiG/cvss/docs/book/source_archive/02_ENGINEERING_DECISION_LOG.md) | Engineering Decision Log | Structured architectural decisions (context, alternatives, decisions, consequences) |
| [`03_SCIENTIFIC_DECISION_LOG.md`](file:///d:/AntiG/cvss/docs/book/source_archive/03_SCIENTIFIC_DECISION_LOG.md) | Scientific Decision Log | Epistemological decisions, preregistrations, guardrails, and non-claims |
| [`04_FAILURES_NEGATIVE_RESULTS_AND_RECOVERIES.md`](file:///d:/AntiG/cvss/docs/book/source_archive/04_FAILURES_NEGATIVE_RESULTS_AND_RECOVERIES.md) | Failures, Negative Results & Recoveries | Operational failures and scientific negative results (honest disclosure) |
| [`05_FIGURES_DIAGRAMS_INVENTORY.md`](file:///d:/AntiG/cvss/docs/book/source_archive/05_FIGURES_DIAGRAMS_INVENTORY.md) | Figures & Diagrams Inventory | Complete index of 87 Mermaid diagrams and system schematics |
| [`06_COMMITS_TAGS_AND_ARTIFACTS_INDEX.md`](file:///d:/AntiG/cvss/docs/book/source_archive/06_COMMITS_TAGS_AND_ARTIFACTS_INDEX.md) | Commits, Tags & Artifacts Index | SHA-1 commits, SHA-256 manifests, PDF builds, and Overleaf bundles |
| [`07_METHOD_EVOLUTION_R1_TO_R6.md`](file:///d:/AntiG/cvss/docs/book/source_archive/07_METHOD_EVOLUTION_R1_TO_R6.md) | Method Evolution (R1 to R6) | Technical comparison across major revision cycles R1, R2, R3, R4, R5, R6, R6.1 |
| [`08_BOOK_CHAPTER_CANDIDATE_MAP.md`](file:///d:/AntiG/cvss/docs/book/source_archive/08_BOOK_CHAPTER_CANDIDATE_MAP.md) | Candidate Book Chapter Map | Proposed 14-chapter architecture for the full monograph |
| [`09_OPEN_ITEMS_FOR_FINAL_BOOK.md`](file:///d:/AntiG/cvss/docs/book/source_archive/09_OPEN_ITEMS_FOR_FINAL_BOOK.md) | Open Items for Final Book | Outstanding items pending R6 execution, expert adjudication, and publication |
| [`book_source_manifest.json`](file:///d:/AntiG/cvss/docs/book/source_archive/book_source_manifest.json) | Machine-Readable Manifest | Cryptographic and structural metadata ledger of the source archive |
| [`figures/`](file:///d:/AntiG/cvss/docs/book/source_archive/figures/) | Standalone Diagram Sources | Extracted raw `.mmd` Mermaid source files for editorial publication |

---

## 4. How to Use this Archive During Book Authoring

When drafting chapters for the monograph:
1. Cross-reference narrative claims with commit SHAs in `06_COMMITS_TAGS_AND_ARTIFACTS_INDEX.md`.
2. Do not omit the negative findings detailed in `04_FAILURES_NEGATIVE_RESULTS_AND_RECOVERIES.md`—the book's educational and scientific authority stems from its complete transparency.
3. Use the raw diagram files in `figures/` as the starting point for high-resolution vector figures.
