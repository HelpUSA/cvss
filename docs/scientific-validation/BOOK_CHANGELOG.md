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
   - Inclusão formal do Dataset A1 (Allodi et al., FDSE 2017) como contexto histórico de erro humano em CVSS v3.0.
   - Especificação dos protocolos planejados para Dataset C1 (Independent Diverse Held-Out Set) e Dataset C2 (Adversarial Safety Challenge Set), sem antecipação de resultados não executados.
4. **Formulações Matemáticas de Avaliação (Capítulo 6)**:
   - Adicionadas as equações formais de $\text{FDR}_{\text{CVSS}}$, $\text{SFDR}_{\text{CVSS}}$, *Abstention Sensitivity* e *Unsafe Non-Abstention Rate*.
5. **Expansão Rigorosa de Ameaças à Validade (Capítulo 8)**:
   - Dividida nas quatro seções canônicas: *Construct Validity*, *Internal Validity*, *External Validity* e *Conclusion Validity*.
6. **Harmonização Estatística (Capítulo 2 e Apêndice B)**:
   - Teste exato de Fisher bicaudal padronizado em $p = 4.2 \times 10^{-6}$, $\text{OR} \approx 3.4$, conditional exact 95% CI $[1.913, 6.184]$; the sample cross-product OR is 3.388 and the Fisher conditional estimate is approximately 3.377.
   - Remoção de notações heterogêneas e suposições não comprovadas.


## ChatGPT integration review - 2026-10-08

- Replaced remaining `ComputeOfficialFIRSTScore` naming with specification-conformant scoring terminology.
- Converted the main Dataset B matrix from mixed CVSS/`Defer` labels to explicit local P0-P4 operational dispositions.
- Regenerated Appendix C Dataset B presentation with source CVSS nomenclature (B/BT/BE/BTE).
- Added a canonical normalized Dataset B CSV so vectors with explicit Threat metrics are no longer mislabeled as Base-only scores.
- Narrowed calculator validation claim: 10-case suite is smoke/regression only; comprehensive FIRST reference-corpus run is now a release gate.
- Added explicit Antigravity web-application synchronization requirements and clean-test gates.

## ChatGPT final pre-freeze hardening pass

- Neutralized additional marketing-style prose in the Introduction and controlled case studies.
- Clarified that network segmentation is a policy/routing boundary and does not imply `MAV:A`.
- Reworded local-loopback classification so it is independent of a segmentation boolean.
- Renamed the historical discussion from "human cognitive failure" to "human assessment difficulty".
- Added a script-generated reproduction of Fisher's exact test and exact conditional OR/CI.
- Expanded the experimental-protocol draft with inclusion/exclusion, independent metric eligibility, ethics/COI, pilot/randomization, unresolved-reference handling, version freeze and technical-rerun rules.
- Corrected ethics language from claimed full anonymization to planned pseudonymization.

## ChatGPT final pre-freeze pass (2026-10-08)

Additional corrections in the final delivery:
- rebuilt the monograph cleanly with `pdflatex + bibtex8` and verified all 42 rendered pages;
- final PDF has zero undefined references/citations and zero overfull hboxes detected;
- simplified the MAV table abstention cell to avoid awkward identifier wrapping;
- synchronized the historical Fisher statistics with generated macros and a reproducibility script;
- retained Dataset B as development-stage evidence only and marked source provenance re-audit as a release gate;
- retained C1/C2 as planned work only; no prospective expert/held-out results were invented;
- supplied explicit Antigravity release gates for calculator corpus validation, source re-audit, full repository tests and production-web synchronization.
