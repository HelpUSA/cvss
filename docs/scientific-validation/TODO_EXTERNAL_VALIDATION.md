# TODO_EXTERNAL_VALIDATION.md
# Itens Restritos à Validação Humana e Especialistas Externos

Este documento delimita formalmente as etapas metodológicas que **NÃO PODEM** ser executadas de forma autônoma pela IA (Antigravity), sob pena de contaminação estatística, circularidade ou fabricação de dados científicos.

---

## 1. Itens que Exigem Especialistas e Humanos Externos

1. **Recrutamento e Cegamento do Painel de Especialistas**:
   - Recrutar 3 especialistas independentes em segurança de redes e CVSS com formulário COI assinado.
   - Status: `TODO / PENDING_EXPERT_RECRUITMENT`.
2. **Avaliação Cega Independente (Blind Scoring)**:
   - Apresentação dos cenários C1 e C2 aos especialistas sem revelar predições do HelpUS.
   - Status: `TODO / PENDING_EXPERT_EVALUATION`.
3. **Sessão de Adjudicação de Divergências**:
   - Condução da sessão entre especialistas para resolver discordâncias entre avaliadores e gerar o *Adjudicated Reference Set*.
   - Status: `TODO / PENDING_ADJUDICATION`.
4. **Homologação Ética Institucional (IRB / CEP)**:
   - Submissão formal do protocolo e termo de consentimento ao comitê de ética da instituição acadêmica (UnitN / UFCG / Comitê competente) ou emissão de declaração formal de isenção.
   - Status: `TODO / PENDING_INSTITUTIONAL_ETHICS_APPROVAL`.
5. **Concepção dos Cenários Held-Out (C1 e C2)**:
   - Criação de novos cenários operacionais complexos por engenheiros de rede externos que não tiveram contato com as regras do `ai_evidence_engine.py`.
   - Status: `TODO / PENDING_EXTERNAL_SCENARIO_DESIGN`.
6. **Pré-Registro Público do Protocolo (Open Science Framework / OSF ou Zenodo)**:
   - Depósito público e timestamped do arquivo `EXPERIMENT_PROTOCOL_v1.0.md` e do hash do motor antes da execução de C1/C2.
   - Status: `TODO / PENDING_PUBLIC_PREREGISTRATION`.


## Release gates added by ChatGPT review

7. **FIRST comprehensive calculator reference-set validation** - `PENDING_LOCAL_REFERENCE_CORPUS_RUN`.
8. **Re-audit 12 Dataset B source assessments and nomenclature** - `PENDING_SOURCE_RETRIEVAL`.
9. **Full clean-environment repository test run** - `PENDING_LOCAL_FULL_TEST_SUITE`.
10. **Backend/frontend CVSS parity test** - `PENDING_LOCAL_PARITY_TEST`.
11. **Production website scientific-claim synchronization** - `PENDING_WEB_PATCH`.
12. **Recompile and visually inspect the final Overleaf artifact after all local merges** - `PENDING_FINAL_BUILD_CHECK`.
