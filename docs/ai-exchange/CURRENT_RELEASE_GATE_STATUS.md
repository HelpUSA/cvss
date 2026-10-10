# Current Release Gate Status — Round 4 Authoritative Status

**This file is the single authoritative release-gate status.** Older status documents must be moved under `docs/ai-exchange/archive/` and must not be interpreted as current.

**SAFE_TO_FREEZE = NO**

| Gate | Status | Evidence | Last Reviewer |
|---|---|---|---|
| G1 — CVSS calculator / FIRST corpus | **PASS** | Executado runner estrito Round-4 contra FIRST corpus completo (66.568 casos): 41.540 vetores válidos avaliados com 0 divergências (delta histogram vazio); 25.028 casos negativos rejeitados com 0 falhas. Evidência em `outputs/first-reference-corpus-round4.json` com `gate_pass: true`. | Antigravity / FIRST reference audit |
| G2 — Portable reproducibility | **PASS** | Artefato portátil construído via `build_portable_artifact_round4.py` (`helpus_cvss_ai_portable_artifact_round4.zip`). Validação estrita via `verify_portable_artifact_round4.py` com zero missing e zero absolute path hits. Perfil isolado executado em diretório limpo: 98 passed, 0 failed, 24 skipped. Perfil full: 122 passed, 0 failed. | Antigravity / Clean room audit |
| G3 — Core fail-safe semantics | **PASS (engineering)** | Comportamento preservado e validado em 122 testes unitários: abstenção em evidência ausente/desconhecida/obsoleta/conflitante; roteamento interno -> MAV:N; firewall != MAC:H; HA != AR:L; requisitos exigem política versionada. | Antigravity / Pytest suite |
| G4 — Web semantics / JCS / HITL | **PASS (qualificado)** | Mapeamento P0-P4 desacoplado e guiado por política (7/7 testes em `test_analyze_route.ts`). Canonicalização JCS validada em 15/15 testes locais e exemplo da seção 3.2 da RFC 8785 aprovado. Qualificação: compatível com JCS; conformidade formal RFC 8785 pendente de corpus externo pinado. Governança HITL restrita ao SuperAdmin Master implementada com Google OAuth exclusivo. | Antigravity / Web route tests |
| G5 — Dataset B provenance / synchronization | **PASS** | Schema v2 canônico mantido e reconciliado após aprovação de G1 via `finalize_dataset_b_after_g1.py` gerando `data/dataset_b/source_assessments_final.csv`. Artefatos sincronizados via `generate_dataset_b_round4_outputs.py`. Verificação de IDs via `compare_dataset_ids_across_artifacts.py` com 0 erros no site e fixtures. | Antigravity / Provenance auditor |
| G6 — Book integrity | **PASS (Round-4 rebuild)** | Monografia recompilada via MiKTeX (46 páginas, 0 citações indefinidas, 0 referências indefinidas, 0 overfull boxes). Verificador de termos científicos `check_book_source_terms_round4.py` com 0 erros. Empacotado em `book_latex/helpus_cvss_ai_monograph_overleaf_final_round4.zip`. | Antigravity / MiKTeX LaTeX builder |
| G7 — Documentation consistency | **PASS** | Documentos obsoletos das rodadas 1, 2 e 3 arquivados. `check_execution_package_consistency_round4.py` executado com 0 erros e 0 notas. Painel padronizado estritamente em n=5 especialistas independentes. | Antigravity / Documentation auditor |
| G8 — Production synchronization | **PASS** | Deploy de produção realizado com sucesso no domínio customizado `https://cvss.helpusbr.com/`. Auditoria automatizada de claims científicos via `audit_public_site_claims_round4.py` executada contra o domínio real: 0 prohibited claims, `pass: true`. Evidência gravada em `outputs/production-copy-audit-round4.json`. | Antigravity / Production smoke test |
| G9 — Human-study governance | **PENDING EXTERNAL** | Determinação de comitê de ética institucional (IRB/CEP ou dispensa formal), TCLE (Termo de Consentimento Livre e Esclarecido) assinado e declaração de conflito de interesses (COI) para os 5 especialistas independentes. | Comitê de Ética / Em espera |
| G10 — Held-out custody C1/C2 | **PENDING PROCEDURAL / EXTERNAL** | Custódia final, cegamento, lacre de protocolo e congelamento definitivo de regras/código/dependências antes da exposição aos conjuntos confirmatórios C1/C2. | Custodiante Externo / Em espera |

---

## Regra de Congelamento (Freeze Rule)

`SAFE_TO_FREEZE = YES` é permitido exclusivamente quando todos os dez gates estiverem suportados por evidência machine-readable atual. Divergências ou percentuais como 99,76% não fecham G1 quando a regra do gate exige zero divergências não explicadas contra o corpus oficial.
