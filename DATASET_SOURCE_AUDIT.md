# DATASET_SOURCE_AUDIT.md
# Auditoria de Proveniência, CNAs e Estrutura dos Datasets

Este documento estabelece o registro de auditoria dos registros CVE, proveniência de dados primários e a separação formal dos corpora de validação científica do projeto HelpUS CVSS AI.

---

## 1. Classificação e Proveniência Institucional

Em estrita conformidade com a governança da FIRST e do ecossistema de vulnerabilidades:
- **FIRST**: Mantenedor e guardião da especificação matemática normativa do CVSS v4.0.
- **CNA (CVE Numbering Authority)**: Entidade primária autoritária responsável pelo registro, atribuição de CVE e autoria da análise de métricas CVSS associada.
- **NVD (National Vulnerability Database / NIST)**: Entidade que indexa e enriquece os registros. Frequentemente exibe os dados fornecidos pelo CNA sob a nota *"CNA-published CVSS v4.0 score indexed by NVD"*, podendo ou não possuir análise independente concluída.

---

## 2. Auditoria Individual dos 12 Registros CVE Reais do Dataset B

| Scenario ID | CVE ID | CNA Publicador | Status NVD / Fonte | Score Base | Severidade | Origem do Vetor Base (`base_vector_origin`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SCN-NVD-001` | `CVE-2026-4251` | `cna@vuldb.com` | VulDB / NVD Indexed | 1.1 | LOW | `CNA_PUBLISHED` |
| `SCN-NVD-002` | `CVE-2026-4252` | `cna@vuldb.com` | VulDB / NVD Indexed | 8.9 | HIGH | `CNA_PUBLISHED` |
| `SCN-NVD-003` | `CVE-2026-4270` | `ff89ba41-3aa1...` | CNA / NVD Indexed | 6.8 | MEDIUM | `CNA_PUBLISHED` |
| `SCN-NVD-004` | `CVE-2026-28490` | `security-advisories@github.com` | GitHub Advisory / NVD Indexed | 8.3 | HIGH | `CNA_PUBLISHED` |
| `SCN-NVD-005` | `CVE-2026-28498` | `security-advisories@github.com` | GitHub Advisory / NVD Indexed | 8.2 | HIGH | `CNA_PUBLISHED` |
| `SCN-NVD-006` | `CVE-2026-29510` | `disclosure@vulncheck.com` | VulnCheck / NVD Indexed | 5.1 | MEDIUM | `CNA_PUBLISHED` |
| `SCN-NVD-007` | `CVE-2026-29513` | `disclosure@vulncheck.com` | VulnCheck / NVD Indexed | 5.1 | MEDIUM | `CNA_PUBLISHED` |
| `SCN-NVD-008` | `CVE-2026-29520` | `disclosure@vulncheck.com` | VulnCheck / NVD Indexed | 5.1 | MEDIUM | `CNA_PUBLISHED` |
| `SCN-NVD-009` | `CVE-2026-29521` | `disclosure@vulncheck.com` | VulnCheck / NVD Indexed | 5.1 | MEDIUM | `CNA_PUBLISHED` |
| `SCN-NVD-010` | `CVE-2026-3644` | `cna@python.org` | Python Software Foundation / NVD | 6.0 | MEDIUM | `CNA_PUBLISHED` |
| `SCN-NVD-011` | `CVE-2026-4224` | `cna@python.org` | Python Software Foundation / NVD | 6.0 | MEDIUM | `CNA_PUBLISHED` |
| `SCN-NVD-012` | `CVE-2026-4253` | `cna@vuldb.com` | VulDB / NVD Indexed | 2.0 | LOW | `CNA_PUBLISHED` |

---

## 3. Taxonomia Formal dos Datasets do Projeto

### DATASET A1 — Historical Human Benchmark (Santos et al., ESSoS 2017)
- **Natureza**: Dados históricos empíricos de participantes humanos avaliando dificuldade de cálculo ambiental.
- **Amostra**: $N=348$ instâncias avaliadas por 29 profissionais/pesquisadores independentes em topologias simples (flat) e complexas (segmentadas).
- **Escopo**: 12 vulnerabilidades históricas de 2016.
- **Padrão Utilizado**: CVSS v3.0 (especificação vigente na época).
- **Papel Metodológico**: Linha de base histórica sobre fadiga cognitiva humana em redes segmentadas. **Não é e não deve ser tratado como avaliação nativa de CVSS v4.0.**

### DATASET B — Development Benchmark ($n=30$)
- **Natureza**: Conjunto de desenvolvimento, calibração e teste de regressão do motor HelpUS AI.
- **Composição**: 12 cenários baseados em CVEs reais publicadas por CNAs em 2026 + 18 cenários sintéticos controlados cobrindo matriz de ativos empresariais e classes de severidade.
- **Papel Metodológico**: Validação de arquitetura interna, integridade de parsing e verificação de pipeline determinístico. **Não constitui prova final de generalização externa.**

### DATASET C1 — Independent Diverse Held-Out Set (Planejado / Protocolo Congelado)
- **Natureza**: Conjunto de teste cego externo para avaliação confirmatória.
- **Requisitos de Custódia**: Cenários concebidos de forma independente, sem acesso ou ajuste sobre o motor HelpUS já congelado.
- **Avaliadores**: Painel de especialistas independentes cegados em relação às predições do HelpUS.
- **Papel Metodológico**: Responder à RQ1 (Eficácia e Concordância Exata de Métricas).

### DATASET C2 — Adversarial Safety Challenge Set (Planejado / Protocolo Congelado)
- **Natureza**: Conjunto de estresse e segurança focado em condições adversas ou ambíguas (telemetria incompleta, rotas conflitantes, NAT ambíguo, VPN, gateways industriais).
- **Papel Metodológico**: Responder à RQ2 (Severe False Downgrade Rate - SFDR) e RQ3 (Taxa de Abstenção Segura e Fail-Safe).
