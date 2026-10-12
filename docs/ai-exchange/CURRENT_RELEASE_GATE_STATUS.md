# Current Release Gate Status — Round 5 Reconciled Status

**This file is the single authoritative release-gate status.**

**SAFE_TO_FREEZE = NO**

| Gate | Status | Evidence | Last Reviewer |
|---|---|---|---|
| G1 — CVSS calculator / FIRST corpus | **PASS** | Runner estrito `run_first_reference_corpus_round4.py` executado contra o corpus completo de `vectorFiles` da FIRST (486.472 casos no total, abrangendo `macro`, `reference` e `base_threat`): 486.472/486.472 passaram com 0 divergências contra o commit pinado `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`. Hashes e tamanhos de fixtures canônicos LF verificados em `scripts/fetch_first_fixtures.py`. Evidência em `outputs/first-reference-corpus-round4.json` (`gate_pass: true`). | Antigravity / FIRST reference audit |
| G2 — Portable reproducibility | **PASS** | Artefato portátil `helpus_cvss_ai_portable_artifact_round4.zip` construído via `build_portable_artifact_round4.py`. Execução clean-room comprovada em diretório temporário isolado com ambiente virtual limpo (`venv`) e instalação de dependências travadas do `requirements.lock` via `verify_portable_artifact_round4.py`: 98 passed, 0 failed, 24 skipped (`outputs/pytest-portable.log`). Suíte completa do repositório: 122 passed, 0 failed, 0 skipped (`outputs/pytest-full.log`). | Antigravity / Clean room audit |
| G3 — Core fail-safe semantics | **PASS (engineering)** | Comportamento preservado e validado em 122 testes unitários: abstenção em evidência ausente/desconhecida/obsoleta/conflitante; roteamento interno -> MAV:N; adjacente -> MAV:A; firewall != MAC:H; HA != AR:L; requisitos exigem política versionada. | Antigravity / Pytest suite |
| G4 — Web semantics / JCS / Auth & HITL | **PASS** | Endpoint protegido server-side `/api/review/decision` implementado com validação de sessão autorizada BetterAuth e restrição ao perfil PLATFORM_ADMIN. Falhas de consulta ao banco retornam HTTP 503 e falhas de persistência de auditoria retornam HTTP 500 (10/10 testes aprovados em `outputs/hitl-review-decision-security-tests.json`). Rota `/api/analyze-environment` com 11/11 testes aprovados (`outputs/web_api_tests_results.json`). JCS recursivo em conformidade local (15/15 testes). | Antigravity / Web route tests |
| G5 — Dataset B provenance / synchronization | **PASS** | Reconciliação canônica via `finalize_dataset_b_after_g1.py` recomputando diretamente pelo scorer oficial validado no G1. Proveniência gravada em `outputs/dataset_b_finalization_provenance.json` com `g1_evidence_sha256` idêntico ao hash do artefato G1 (`a6105c66df1c3e3185b9f1d4a30085574524126c374eb42dcd85fb472e0c8916`). 30 cenários, 12 CVEs reais, 0 erros. | Antigravity / Provenance auditor |
| G6 — Book integrity / Synchronization | **PASS (Round-4 rebuild)** | Monografia LaTeX corrigida e sincronizada. `book_latex/BUILD_MANIFEST_CHATGPT_ROUND4.json` alinhado exatamente com os arquivos fonte committed, `main.pdf` (1.224.761 bytes) e o arquivo `helpus_cvss_ai_monograph_overleaf_final_round4.zip` (3.003.075 bytes) commitado no Git. | Antigravity / Monograph auditor |
| G7 — Documentation consistency | **PASS** | Documentação reconciliada com evidências machine-readable brutas: 122 testes do repositório, 98 testes portáteis em venv isolado, 10 testes de decisão HITL com fail-closed, 486.472 casos do corpus FIRST. Status mantido em estrita consistência com os logs de execução. | Antigravity / Documentation auditor |
| G8 — Production synchronization | **PASS** | Domínio de produção `https://cvss.helpusbr.com/` verificado diretamente via `scripts/audit_public_site_claims_round4.py` (`outputs/production-copy-audit-round4.json`: `pass: true`, 0 alegações proibidas). Snapshot HTML bruto ao vivo preservado e commitado em `outputs/production-live-snapshot.html` (73.781 bytes, SHA-256 `77ed5fbeaef5ceac2603097cf2a76ade74504ac3c646491ea5ef4933a846be7d`). | Antigravity / Production smoke test |
| G9 — Human-study governance | **PENDING EXTERNAL** | Determinação de comitê de ética institucional (IRB/CEP ou dispensa formal), TCLE (Termo de Consentimento Livre e Esclarecido) assinado e declaração de conflito de interesses (COI) para os 5 especialistas independentes. | Comitê de Ética / Em espera |
| G10 — Held-out custody C1/C2 | **PENDING PROCEDURAL / EXTERNAL** | Custódia final, cegamento, lacre de protocolo e congelamento definitivo de regras/código/dependências antes da exposição aos conjuntos confirmatórios C1/C2. C1/C2 permanecem inviolados e não executados. | Custodiante Externo / Em espera |

---

## Regra de Congelamento (Freeze Rule)

`SAFE_TO_FREEZE = NO` é estritamente mantido até que os gates procedimentais e externos G9 e G10 sejam concluídos. Nenhum teste nos conjuntos confirmatórios mantidos sob custódia (C1/C2) foi executado ou aberto.
