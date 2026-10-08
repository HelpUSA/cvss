# BOOK_CHANGELOG.md
# Registro de Alterações do Monograph / Livro Acadêmico

- **Versão Atual**: `v1.3-scientific-validation-refactor`
- **Data**: 2026-10-08

---

## 1. Alterações Estruturais e Conceituais

1. **Separação Explícita entre Severidade Técnica e Prioridade Operacional (Capítulo 6)**:
   - Severidade técnica CVSS: restrita aos níveis normativos FIRST (`None`, `Low`, `Medium`, `High`, `Critical`).
   - Disposição operacional organizacional: formalizada nos níveis de prioridade `P0_IMMEDIATE`, `P1_EXPEDITED`, `P2_SCHEDULED`, `P3_MONITOR`, `P4_DEFER_RECOMMENDED`.
   - Remoção de `Defer` da escala CVSS; especificação de que `P4` não implica aceitação tácita de risco sem homologação humana formal.
2. **Declaração Formal do Dataset B como Development Benchmark (Capítulo 6)**:
   - Os 30 cenários contemporâneos foram formalizados como **Dataset B (Development Benchmark)**, com a declaração expressa de que servem para calibração arquitetural interna e testes de regressão, e não como validação final confirmatória.
3. **Formalização dos Datasets A1, C1 e C2 (Capítulo 6)**:
   - Inclusão formal do Dataset A1 (Santos et al., 2017) como contexto histórico de erro humano em CVSS v3.0.
   - Especificação dos protocolos planejados para Dataset C1 (Independent Diverse Held-Out Set) e Dataset C2 (Adversarial Safety Challenge Set), sem antecipação de resultados não executados.
4. **Formulações Matemáticas de Avaliação (Capítulo 6)**:
   - Adicionadas as equações formais de $\text{FDR}_{\text{CVSS}}$, $\text{SFDR}_{\text{CVSS}}$, *Abstention Sensitivity* e *Unsafe Non-Abstention Rate*.
5. **Expansão Rigorosa de Ameaças à Validade (Capítulo 8)**:
   - Dividida nas quatro seções canônicas: *Construct Validity*, *Internal Validity*, *External Validity* e *Conclusion Validity*.
6. **Harmonização Estatística (Capítulo 2 e Apêndice B)**:
   - Teste exato de Fisher bicaudal padronizado em $p = 4.2 \times 10^{-6}$, $\text{OR} \approx 3.4$, 95% CI $[1.91, 6.18]$.
   - Remoção de notações heterogêneas e suposições não comprovadas.
