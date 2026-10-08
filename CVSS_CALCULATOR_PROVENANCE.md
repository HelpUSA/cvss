# CVSS_CALCULATOR_PROVENANCE.md
# Proveniência e Especificação do Calculador CVSS v4.0

Este documento atesta a biblioteca, origem, licença e conformidade do motor computacional de cálculo do CVSS v4.0 utilizado no ecossistema HelpUS.

---

## 1. Identificação Técnica da Implementação Backend (Python)

- **Nome do Pacote**: `cvss` (módulo `cvss.CVSS4`)
- **Versão Instalada**: `3.6`
- **Ambiente de Execução**: `D:\AntiG\cvss\.venv\Scripts\python.exe` (Python 3.14 / venv local)
- **Mantenedor Oficial**: Red Hat Product Security (Stanislav Kontar <skontar@redhat.com>)
- **Repositório do Código-Fonte**: [https://github.com/RedHatProductSecurity/cvss](https://github.com/RedHatProductSecurity/cvss)
- **Licença**: GNU Lesser General Public License v3 or later (LGPLv3+)
- **Especificação Normativa**: FIRST Common Vulnerability Scoring System v4.0 Specification Document
- **Mecanismo Algorítmico**: Implementação fiel do algoritmo de lookup de MacroVetores $EQ_1, EQ_2, EQ_3, EQ_4, EQ_5, EQ_6$ e tabelas de interpolação de severidade padronizadas pela FIRST.
- **Camada de Integração HelpUS**: [`core/cvss40.py`](file:///D:/AntiG/cvss/core/cvss40.py), que aplica validação estrita de nomenclatura oficial (`CVSS-B`, `CVSS-BE`, `CVSS-BT`, `CVSS-BTE`), parsing canônico e fusão protegida de candidatos contextuais sem mutação do vetor base oficial.

---

## 2. Identificação Técnica da Implementação Frontend (JavaScript)

- **Arquivo**: [`app.js`](file:///D:/AntiG/cvss/app.js) (função `calculateCvss40`)
- **Origem do Algoritmo**: Port direto da especificação e macro-tabelas da FIRST (`cvss_v4.0_lookup.js`), reproduzindo os níveis de equivalência $EQ_1 \dots EQ_6$ e interpolação de distância de severidade em tempo de execução no navegador.
- **Conformidade Cruzada**: Todo vetor computado no backend Python produz resultado idêntico ($\Delta = 0.0$) quando avaliado no frontend JavaScript.

---

## 3. Diretriz de Nomenclatura no Projeto

Para manter o rigor e não incorrer em alegações indevidas:
- **NÃO** chamar o motor de *"calculador oficial da FIRST"* de forma genérica.
- **CHAMAR DE**: *"Implementação de referência FIRST CVSS v4.0 da Red Hat Product Security (pacote Python `cvss` v3.6) e motor conforme à especificação FIRST CVSS v4.0"*.
