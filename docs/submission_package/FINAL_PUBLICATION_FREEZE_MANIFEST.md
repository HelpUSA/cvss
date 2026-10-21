# HelpUS CVSS Academic Publication Freeze Manifest

- **Correlation ID:** `CMD-CVSS-PUBLICATION-FREEZE-038`
- **Freeze Status:** `PUBLICATION_FREEZE_READY`
- **Timestamp (UTC):** `2026-10-20T20:25:00Z`
- **Git HEAD Commit:** `5f933313842101a9196716727e376a764611deaa`
- **FIRST Pinned Commit:** `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`

---

## 1. Status dos Artefatos de Publicação

### Artigo IEEE (Double-Blind Conference Format)
- **Status Oficial:** `SAFE_TO_SUBMIT`
- **Caminho Canônico do PDF:** `article/ieee/cvss40_double_blind.pdf`
- **Caminho no Pacote de Submissão:** `docs/submission_package/article_main.pdf`
- **SHA-256 do Artigo PDF:** `19c2f48c96eb859a38c926468e5240d85fbf826d3c27c1ee0872ce88ad1a905e`
- **Tamanho:** `181.653 bytes` (7 páginas)
- **Fonte LaTeX Canônica:** `article/ieee/cvss40_double_blind.tex` (SHA-256: `4eccba99a3fc2322392f9fa1d17f17dcf0997103624ad52e0a601938d3851da9`)
- **Auditoria Dupla-Cega:** 100% anônimo (/Author vazio, sem afiliações ou paths locais).

### Livro Monográfico (Comprehensive Reference Book)
- **Status Oficial:** `BOOK_READY_FOR_PUBLICATION`
- **Caminho Canônico do PDF:** `book_latex/main.pdf`
- **SHA-256 do Livro PDF:** `78ab00dcc822e52acbc102d0cba1d68ec21ec60fc6feb9265d4961c335837b02`
- **Tamanho:** `1.239.234 bytes` (50 páginas)
- **Fonte LaTeX Canônica:** `book_latex/main.tex` (SHA-256: `6803d1c92cc31d923f8792d325b63946976aefc05628132a2e5dc053aaae7c36`)
- **Pacote Overleaf Completo:** `book_latex/helpus_cvss_ai_monograph_overleaf_final_round4.zip` (SHA-256: `09effd8a0f045081b1028b5f3177464b0e1d4c26b8e2555053b564b184f15af5`)

---

## 2. Invariantes Científicos e Governança Selada

- **FIRST Reference Corpus (Round 5):** 486.472 / 486.472 casos exatos com 0 divergências contra o commit `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`.
- **Campanha Metamórfica:** 10.000 execuções com 0 violações de invariância (`HELPUS-METAMORPHIC-10K-G9B`, MR-1 a MR-4).
- **Cenários Empíricos:** 30 cenários híbridos (12 NVD v4.0 reais + 18 sintéticos) com 22 mudanças de prioridade operacional.
- **Protocolo Confirmatório G10B:** `PROTOCOL DEFINED / EXECUTION NOT AUTHORIZED`.
- **Datasets de Confirmação C1 e C2:** `SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE` sob o gatekeeper fail-closed `scripts/g10b_confirmatory_gate.py`.
- **Adjudicação Humana Especializada Independente:** `PENDING / NOT COMPLETED`. Protocolo pré-registrado em `article/expert_review/`.

---

## 3. Relatórios e Manifestos Vinculados

- `docs/submission_package/README.md`
- `docs/ARTICLE_IEEE_LATEX_READINESS_CVSS40.md`
- `book_latex/BUILD_MANIFEST_CHATGPT_ROUND4.json`
- `book_latex/LATEX_BUILD_REPORT_CHATGPT_ROUND4.md`
- `book_latex/ROUND4_BOOK_CHANGELOG.md`
- `outputs/metamorphic_campaign_10k_manifest.json`
- `outputs/first-reference-corpus-round4.json`
