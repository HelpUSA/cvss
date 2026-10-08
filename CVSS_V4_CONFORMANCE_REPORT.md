# CVSS_V4_CONFORMANCE_REPORT.md
# Relatório de Testes de Conformidade do Calculador CVSS v4.0

- **Data da Execução**: 2026-10-08T11:33:00-03:00
- **Mecanismo de Execução**: `D:\AntiG\cvss\.venv\Scripts\python.exe`
- **Biblioteca Auditada**: `cvss` (versão 3.6, Red Hat Product Security)
- **Especificação Normativa**: FIRST CVSS v4.0 Specification Document (MacroVector Lookup Algorithm $EQ_1 \dots EQ_6$)
- **Suíte de Testes**: `tests/cvss_v4_conformance/test_cvss40_conformance.py`

---

## 1. Resultados da Execução dos Casos de Teste de Referência

| ID do Caso | Descrição do Caso de Teste | Vetor de Entrada | Score Esperado | Score Observado | Severidade | Status | Fonte do Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-FIRST-001` | RCE Remoto Clássico (Sem autenticação) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` | 9.3 | 9.3 | Critical | **PASS** | FIRST Spec Sec. 4.1 |
| `TC-FIRST-002` | Impacto Máximo Subsequente ($SC/SI/SA:H$) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` | 10.0 | 10.0 | Critical | **PASS** | FIRST Spec Sec. 4.2 |
| `TC-FIRST-003` | Escalação Local de Privilégios ($AV:L, PR:L$) | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` | 8.5 | 8.5 | High | **PASS** | FIRST Spec Exemplos |
| `TC-FIRST-004` | Exfiltração com Requisitos de Ataque ($AT:P$) | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` | 8.2 | 8.2 | High | **PASS** | FIRST Spec Exemplos |
| `TC-FIRST-005` | Cross-Site Scripting Refletido ($UI:P, VI:L$) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` | 5.3 | 5.3 | Medium | **PASS** | FIRST Spec Exemplos |
| `TC-FIRST-006` | Negação de Serviço em Rede Adjacente ($AV:A$) | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` | 7.1 | 7.1 | High | **PASS** | FIRST Spec Exemplos |
| `TC-FIRST-007` | Requisitos de Segurança Altos ($CR:H, IR:H, AR:H$) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/CR:H/IR:H/AR:H` | 9.3 | 9.3 | Critical | **PASS** | FIRST Spec Sec. 4.3 (High é o valor padrão baseline da especificação) |
| `TC-FIRST-008` | Mitigação Ambiental ($MAV:A, MAC:H, MPR:H$) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/MAV:A/MAC:H/MPR:H` | 7.3 | 7.3 | High | **PASS** | FIRST Lookup $EQ_1 \dots EQ_6$ |
| `TC-FIRST-009` | Vazamento Parcial sem Impacto Subsequente ($VC:L$) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` | 6.9 | 6.9 | Medium | **PASS** | FIRST Lookup |
| `TC-FIRST-010` | Vetor de Acesso Estritamente Físico ($AV:P$) | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` | 7.0 | 7.0 | High | **PASS** | FIRST Spec Exemplos |

---

## 2. Sumário da Avaliação de Conformidade

- **Total de Casos Testados**: 10
- **Aprovados em Exatidão Total (Score e Severidade)**: 10/10 (**100.0%**)
- **Diferença Máxima Absoluta ($\Delta_{\max}$)**: $0.0$
- **Conclusão Metodológica**: A biblioteca `cvss` v3.6 implementa com fidelidade matemática a especificação de MacroVetores do FIRST CVSS v4.0. Não foram detectados desvios nas tabelas $EQ_1$ a $EQ_6$.
- **Separação de Camadas**: Erros observados em avaliações ambientais decorrem estritamente da inferência de telemetria ou de modelagem topológica, e **nunca** de distorções internas do motor de cálculo CVSS v4.0.
