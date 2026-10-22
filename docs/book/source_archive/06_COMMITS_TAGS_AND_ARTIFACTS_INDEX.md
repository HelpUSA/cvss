# HelpUS CVSS AI v4.0 — Commits, Tags, and Artifacts Index

This index provides a cryptographic and factual record of all milestone Git commits, released tags, publication bundles, and experimental manifests produced across the research program.

---

## 1. Master Milestone Git Commit Index

| Full Commit SHA | Short SHA | Phase / Lifecycle | Commit Subject / Purpose | Associated Tag | Governance Status | Parent Commit SHA |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `bfaece26f9f718672be6b754ad83497ac7f102ea` | `bfaece2` | Phase R6.1 | `docs(research): preregister R6.1 T2 compatibility taxonomy deviation` | — | `DEVIATION_FROZEN` | `43664e58b4f7852d0a03c6b21ab043dec2529be9` |
| `43664e58b4f7852d0a03c6b21ab043dec2529be9` | `43664e5` | Phase R6-1 | `feat(research): freeze R6 A1 schema v2 and governance implementation` | — | `IMPLEMENTATION_FROZEN` | `090ad8b727e674aac8e95864fe7740b15092ea60` |
| `090ad8b727e674aac8e95864fe7740b15092ea60` | `090ad8b` | Phase R6-1 | `docs(research): freeze R6 A1 schema v2 and governance specification` | — | `SPECIFICATION_FROZEN` | `2346859b319eac9146273b215eca796147816837` |
| `2346859b319eac9146273b215eca796147816837` | `2346859` | Phase R6-2 | `tools(research): add reproducible R6 held-out corpus acquisition` | — | `TOOLING_LOCKED` | `12bf6c456054656a1bbc198d7e3729d2675098b2` |
| `12bf6c456054656a1bbc198d7e3729d2675098b2` | `12bf6c4` | Phase R6-2 | `data(research): freeze R6 A1 held-out corpus` | — | `CORPUS_QUARANTINED` | `106049618eff5e2f2a34aa591475c4a042bdba37` |
| `106049618eff5e2f2a34aa591475c4a042bdba37` | `1060496` | Phase R6-0 | `docs(research): freeze R6 A1 held-out corpus protocol` | — | `PROTOCOL_LOCKED` | `c0b4025d9f560b8e525accd17e1b075cd23a355b` |
| `c0b4025d9f560b8e525accd17e1b075cd23a355b` | `c0b4025` | Phase R6-0 | `docs(research): preregister R6 A1 validation design` | — | `PREREGISTRATION_LOCKED` | `e5215b525c90696043b1d68ea5bf4ce4c88f2d41` |
| `e5215b525c90696043b1d68ea5bf4ce4c88f2d41` | `e5215b5` | Phase R5 | `Merge PR #47: IEEE camera-ready R5 abstract polish` | — | `MAIN_BASELINE` | `cc4418e062101f5259c15e51dc9a1bc2fd9c3e88` |
| `cc4418e062101f5259c15e51dc9a1bc2fd9c3e88` | `cc4418e` | Phase R5 | `docs(article): seal IEEE camera-ready R5 abstract polish` | `v4.0.0-ieee-camera-ready-r5` | `CAMERA_READY_FROZEN` | `97931e12bb6be09407ba8db4d860fa1fb826d345` |
| `cb8ab692e5425679f220377f0a6d07e6005ee2e6` | `cb8ab69` | Phase R4 | `docs(article): seal IEEE major revision R4 conceptual polish` | `v4.0.0-ieee-major-revision-r4` | `HISTORICAL_FREEZE` | `073fa7d20fbbfce8ef78201eb652bb2d977e2ff4` |
| `073fa7d20fbbfce8ef78201eb652bb2d977e2ff4` | `073fa7d` | Phase R3 | `docs(article): seal IEEE major revision R3 reviewer hardening` | `v4.0.0-ieee-major-revision-r3` | `HISTORICAL_FREEZE` | `c41065ebdd93c6febb4597bae3487e1f8b61b517` |
| `c41065ebdd93c6febb4597bae3487e1f8b61b517` | `c41065e` | Phase R2 | `docs(article): seal IEEE major revision R2 machine-verifiable track` | `v4.0.0-ieee-major-revision-r2` | `HISTORICAL_FREEZE` | `29a087d1973ff5b3cb4786435ba52d76f8279ce8` |
| `29a087d1973ff5b3cb4786435ba52d76f8279ce8` | `29a087d` | Post-R1 | `docs(article): seal post-R1 main-track consolidation` | `v4.0.0-post-r1-consolidation` | `HISTORICAL_FREEZE` | `cb4391e6b823e20e19dc242bf541eb20c02be556` |
| `cb4391e6b823e20e19dc242bf541eb20c02be556` | `cb4391e` | Post-R1 | `docs(article): seal post-review editorial polish` | `v4.0.0-ieee-major-revision-r1-editorial` | `HISTORICAL_FREEZE` | `799657f2010839e160a0b27b38d7bb6d7a46c241` |
| `799657f2010839e160a0b27b38d7bb6d7a46c241` | `799657f` | Phase R1 | `docs(article): seal IEEE major revision R1` | `v4.0.0-ieee-major-revision-r1` | `HISTORICAL_FREEZE` | `5226f74a0c8bb194c7b805c87de64fe786d5e751` |
| `5226f74a0c8bb194c7b805c87de64fe786d5e751` | `5226f74` | Genesis Freeze | `chore(freeze): seal publication baseline for IEEE article and monograph companion book` | `v4.0.0-publication-freeze` | `GENESIS_FREEZE` | Pre-freeze development |

---

## 2. Cryptographic Hashes of Key Artifacts (SHA-256)

### A. Academic Publication Packages (R5 Camera-Ready & Baseline)
* **Double-Blind IEEE LaTeX Source**:
  - Path: `article/ieee/cvss40_double_blind.tex`
  - SHA-256: `4eccba99a3fc2322392f9fa1d17f17dcf0997103624ad52e0a601938d3851da9`
* **Canonical IEEE Article PDF (R5 Camera-Ready)**:
  - Path: `docs/submission_package/article_main.pdf` (also at `article/ieee/cvss40_double_blind.pdf`)
  - Size: 181,653 bytes (7 pages)
  - SHA-256: `19c2f48c96eb859a38c926468e5240d85fbf826d3c27c1ee0872ce88ad1a905e`
* **Overleaf Article Submission Bundle**:
  - Path: `docs/submission_package/cvss40_ieee_article_overleaf.zip`
  - Size: 28,397 bytes
  - SHA-256: Verified in `FINAL_PUBLICATION_FREEZE_MANIFEST.json`
* **Monograph Companion Book LaTeX Source**:
  - Path: `book_latex/main.tex`
  - SHA-256: `6803d1c92cc31d923f8792d325b63946976aefc05628132a2e5dc053aaae7c36`
* **Monograph Companion Book PDF**:
  - Path: `book_latex/main.pdf`
  - Size: 1,239,234 bytes (50 pages)
  - SHA-256: `78ab00dcc822e52acbc102d0cba1d68ec21ec60fc6feb9265d4961c335837b02`
* **Monograph Overleaf Companion Bundle**:
  - Path: `book_latex/helpus_cvss_ai_monograph_overleaf_final_round4.zip`
  - Size: 1,985,575 bytes
  - SHA-256: `09effd8a0f045081b1028b5f3177464b0e1d4c26b8e2555053b564b184f15af5`

---

### B. Experimental Validation Datasets & Evidence Manifests

* **Canonical 30-Scenario Environmental Dataset**:
  - Path: `data/article/cvss40_environmental_scenarios.csv`
  - Content: 30 scenarios (12 real NVD + 18 synthetic expert profiles)
  - Canonical Invariant: 22 priority shifts ($73.33\%$)
* **Revision R2 Trace Verification Manifest**:
  - Path: `validation/article/r2_canonical_trace_verification.json`
  - Scope: 464 assertions across 30 traces ($100\%$ PASS)
* **Revision R3 Randomized Mutation Testing Manifest**:
  - Path: `validation/article/r3_randomized_mutation_testing.json`
  - Scope: 120 mutants (seed 20261021; 83 rejected, 37 accepted)
  - Size: 99,401 bytes
  - SHA-256: `32e273f1f0be0f631301edc9b1e2448d013586bf0a9c1e7b05688e6dcf1ac790`
* **Revision R3 Randomized Mutation Cases Ledger**:
  - Path: `validation/article/r3_randomized_mutation_cases.csv`
  - Size: 24,463 bytes
  - SHA-256: `60a38411df1753899f444a5e61895795dcdf9b4403327a1a0c6f2ff4b589d84c`
* **Phase R6 External Held-Out Corpus Manifest (Quarantined)**:
  - Path: `validation/article/r6_heldout/eligible_corpus_manifest.json`
  - Scope: 938 eligible CVSS v4.0 advisories from GitHub Advisory Database
  - SHA-256: `b09a8cc45147f25073103c005d87b4244ea9e03a8233b7059fbd310cc13a22cf`
* **Experiment T2 Canonical Backward Compatibility Results (Immutable Baseline)**:
  - Path: `validation/article/r6_t2/r6_t2_backward_compatibility_results.json`
  - Size: 14,501 bytes
  - SHA-256: `20173fcf95bbe7da936d2e5f1dc6c5d3b1a9dfcd58ff0fab77495e743e8c47f9`
* **Experiment T2 Canonical Summary Report**:
  - Path: `validation/article/r6_t2/r6_t2_backward_compatibility_summary.md`
  - Size: 5,636 bytes
  - SHA-256: `4618275fc4b16d066f2d8d3908c1cb6a8e67cf243a68db5ed4165373b2d73102`
* **Experiment T2 Cryptographic Ledger**:
  - Path: `validation/article/r6_t2/SHA256SUMS.txt`
  - Size: 216 bytes
  - SHA-256: `6f3bfd5cbb7aea4290e2f92f97ce49b000fd44b1d16f354d15df1afcea509ac0`
