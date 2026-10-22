# CVSS Article Current Status

## Status

Campanha experimental R6-A1 concluída com sucesso e congelada no repositório. Manuscrito IEEE e monografia consolidados e compilados. Adjudicação humana independente permanece pendente como trabalho futuro (`human_adjudication_completed = false`).

## Evidência disponível e congelada

- **Dataset B histórico**: 30 cenários de benchmark de desenvolvimento.
- **Campanha Metamórfica**: 10.000 execuções com zero violações em 4 relações metamórficas.
- **Conformidade FIRST**: 486.472 vetores avaliados contra FIRST commit `d766d0c` com 100% de conformidade.
- **Schema v2 Closed-World (T2R & T3)**: 30/30 rejeições de formatos legados não canonicalizados (12 INVALID_TYPE, 18 INVALID_ENUM); 120/120 mutações rejeitadas no replay (16/16 injeções F3 rejeitadas).
- **Mutações v2 (T4R & NF2-R)**: 75/90 rejeições atribuíveis em T4R; 15/15 rejeições em companion NF2-R.
- **Governança Downstream (T5-R & T6)**: 8/8 invariantes atendidos em T5-R com fórmula da Equação 8 invariante e zero overrides autônomos; T6 com 2/4 representáveis normativamente e 2/4 demandando evidência externa, zero dados inventados.
- **Validação Diferencial R2**: 454.047/461.444 exatos (98,3970%) e 25.028/25.028 concordâncias negativas (100,0%) contra `cvss4py` sob paridade determinística.
- **Transferência Held-Out T7**: $N=938$ avisos do GitHub Advisory Database com 339 calculáveis nominais e 599 rejeições fail-closed sem invenção de dados; 938/938 traces verificados em 3.232 verificações de diagnóstico sob paridade determinística.
- **Manuscrito IEEE**: `article/ieee/cvss40_double_blind.tex` (compilado em `cvss40_double_blind.pdf`, 17 páginas).
- **Monografia (Book)**: `book_latex/main.tex` (compilado em `main.pdf`, 51 páginas).

## Evidência ainda não executada (trabalho futuro)

- Adjudicação humana presencial/cega com especialistas do domínio (`human_adjudication_completed = false`).
- Protocolo confirmatório G10B e datasets confirmatórios C1 e C2 permanecem selados e não executados.

## Proteções e Governança

- Protocolo de desvios R6-DEV-001 a R6-DEV-005 formalmente auditado e registrado.
- Invariantes de governança INV-G1 a INV-G8 plenamente respeitadas.
- Zero sobrescrita retroativa de resultados históricos.
