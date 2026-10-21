---
status: active
last_updated: 2026-10-21
owner: "Wagner / CVSS project"
tags:
  - cvss
  - research
  - article
aliases:
  - "CVSS Article"
  - "Paper"
related_files:
  - docs/ARTICLE_PLAN_PT.md
  - docs/ARTICLE_STATUS.md
  - docs/ARTICLE_REBOOT_PLAN.md
  - docs/ARTICLE_REFINEMENT_TODO.md
---

# Paper or Article

## Estado atual

A campanha experimental R6-A1 foi formalmente concluída e seus resultados foram congelados no repositório. O manuscrito IEEE (`article/ieee/cvss40_double_blind.tex`) e a monografia (`book_latex/main.tex`) foram consolidados e compilados com sucesso.

### Evidências experimentais congeladas da campanha R6-A1:
1. **Schema v2 Closed-World (T2R / T3)**:
   - T2R: 30/30 traces históricos classificados como `V1_VALID_V2_INVALID` (12 `INVALID_TYPE`, 18 `INVALID_ENUM`), confirmando a rejeição estrita de formatos legados não canonicalizados.
   - T3 Replay: 120/120 mutações rejeitadas sob Schema v2, eliminando a brecha histórica de injeção de subobjetos ($F3$: 16/16 rejeições sob v2 vs 0/16 sob v1).
2. **Mutações Específicas do Schema v2 (T4R / NF2-R)**:
   - T4 original causally confounded; rerun desacoplado T4R em 15 pais canônicos ($N=90$) com 75/90 rejeições atribuíveis (83,33%).
   - Companion NF2-R ($N=15$) verificando 15/15 rejeições de shadowing de campos centrais na raiz do schema.
3. **Contrato de Governança Downstream (T5-R / T6)**:
   - T5-R: 8/8 fixtures com status PASS em todos os 8 invariantes de governança (INV-G1 a INV-G8). Parâmetros e pesos nominais da Equação 8 permaneceram rigorosamente invariantes; zero overrides autônomos.
   - T6: Representabilidade em 4 CVEs do NVD (12 checks de diagnóstico), demonstrando 2/4 representáveis por transformação estrutural normativa e 2/4 demandando nova evidência, com zero invenção de dados.
4. **Validação Diferencial Independente (Differential R2)**:
   - Comparador secundário: `cvss4py` (commit `9fe705c`).
   - Endpoint Numérico ($D_{\text{numeric}} = 461.444$ vetores calculáveis): 454.047 concordâncias numéricas exatas (98,3970%), 7.397 mismatches ($|\Delta| = 0,1$, 100% coincidentes com o gabarito oficial do FIRST), 0 divergências de validade, 0 erros de execução.
   - Endpoint de Validação Sintática ($D_{\text{validation}} = 25.028$ vetores malformados): 25.028 concordâncias de rejeição sintática (100,0%).
   - Paridade determinística dual-pass: PASS.
5. **Transferência Externa para Corpus Held-Out (T7)**:
   - Corpus externo de $N=938$ avisos reais do GitHub Advisory Database, coletado e quarentenado antes do acesso experimental.
   - 339 casos nominais calculáveis (36,1407%) e 599 rejeições fail-closed por ausência de evidência obrigatória (63,8593%).
   - Zero dados inventados; zero overrides autônomos.
   - 938/938 traces verificados com sucesso pelo verificador independente de traces através de 3.232 verificações de diagnóstico. Paridade determinística: PASS.

## Regras de integridade e Limites Epistemológicos

- **Adjudicação Humana por Especialistas**: Permanece não executada nesta etapa (`human_adjudication_completed = false`). Não fabricar respostas humanas nem inferir concordância prévia.
- **Isolamento Fail-Closed**: Os datasets confirmatórios C1 e C2 permanecem criptograficamente selados sob o gatekeeper G10B (`scripts/g10b_confirmatory_gate.py`) como trabalho futuro.
- **Rastreabilidade pós-T7**: O acesso histórico ao corpus held-out de 938 casos está formalmente registrado (`held_out_accessed = true`).

## Relação com o produto

A camada contextual HelpUS e os contratos de governança operam downstream, mantendo a separação estrita da especificação oficial do CVSS v4.0.
