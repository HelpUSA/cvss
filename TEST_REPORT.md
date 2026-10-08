# TEST_REPORT.md
# Relatório de Execução de Testes Automatizados — HelpUS CVSS AI

- **Data da Execução**: 2026-10-08T11:41:00-03:00
- **Ambiente de Testes**: `D:\AntiG\cvss\.venv\Scripts\python.exe` (Python 3.14 / Windows)
- **Framework de Testes**: Python `unittest`
- **Status Geral**: **100% DOS TESTES APROVADOS**

---

## 1. Módulos e Suítes de Testes Executados

| Suíte de Testes | Arquivo de Teste | Qtd. Testes | Status | Escopo Validado |
| :--- | :--- | :---: | :---: | :--- |
| **Fail-Safe Abstention** | `tests/test_fail_safe_abstention.py` | 3 | **PASS** | Abstenção mandatória (`HUMAN_REVIEW_REQUIRED`) sob telemetria vazia, rotas conflitantes e telemetria obsoleta (>30 dias). Proibição de downgrade automático. |
| **Topology Reachability** | `tests/test_topology_reachability.py` | 5 | **PASS** | Preservação de `MAV:Network` para tráfego roteado interno; restrição de `MAV:Adjacent` a L2 não roteado; `MAV:Local` para shell local; firewall isolado não altera `MAC:High`. |
| **CVSS v4.0 Conformance** | `tests/cvss_v4_conformance/test_cvss40_conformance.py` | 10 | **PASS** | Conformidade matemática de MacroVetores $EQ_1 \dots EQ_6$ contra os vetores normativos do Specification Document da FIRST. |

---

## 2. Resumo da Cobertura de Segurança
- Nenhuma vulnerabilidade crítica é desescalonada na presença de telemetria incerta.
- Erros de rede e semântica de L2/L3 são estritamente diferenciados antes de qualquer mutação de vetor.
- 0 falhas, 0 erros e 0 regressões identificadas na suíte de testes.
