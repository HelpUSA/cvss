# FAILURE_TAXONOMY.md
# Taxonomia Formal de Falhas em Priorização Ambiental de Vulnerabilidades

Para garantir rastreabilidade analítica rigorosa em conformidade com as diretrizes de engenharia de software empírica, qualquer divergência observada entre o HelpUS e o gabarito de referência de especialistas é classificada segundo as 9 categorias formais abaixo:

---

## 1. Categorias de Erro

| Código da Falha | Nome Formal | Definição Operacional |
| :--- | :--- | :--- |
| `ERR-SRC` | `SOURCE_ERROR` | Erro presente no registro original do CVE (ex: vetor Base incorreto atribuído pelo CNA ou dados corrompidos no NVD). |
| `ERR-EVP` | `EVIDENCE_PARSER_ERROR` | Falha do extrator de telemetria ao ler arquivos de configuração, logs de firewall ou saída de scanner. |
| `ERR-TOP` | `TOPOLOGY_ERROR` | Erro na representação topológica (ex: assumir adjacência de broadcast L2 quando há roteamento L3 ou firewall intermediário). |
| `ERR-MIN` | `METRIC_INFERENCE_ERROR` | Inferência incorreta de métrica nominal candidata (ex: inferir `MAV:Adjacent` quando a rota permitia tráfego roteado). |
| `ERR-VSY` | `VECTOR_SYNTHESIS_ERROR` | Erro na montagem da string do vetor canônico CVSS-BE ou na fusão com o vetor Base. |
| `ERR-CAL` | `CVSS_CALCULATOR_ERROR` | Discrepância na tabela de busca ou no algoritmo de interpolação do calculador CVSS v4.0. |
| `ERR-POL` | `POLICY_MAPPING_ERROR` | Atribuição divergente de requisitos organizacionais (`CR`, `IR`, `AR`) por falha na interpretação da política de segurança corporativa. |
| `ERR-UNA` | `UNSAFE_NON_ABSTENTION` | Falha crítica de segurança: o sistema realizou um desescalonamento automático da vulnerabilidade quando as evidências eram ambíguas, conflitantes ou insuficientes. |
| `ERR-UAB` | `UNNECESSARY_ABSTENTION` | O sistema solicitou revisão humana desnecessária (`HUMAN_REVIEW_REQUIRED`) apesar de existirem evidências suficientes e inequívocas para decisão automatizada. |

---

## 2. Processo de Classificação
Toda discrepância detectada em avaliações com especialistas independentes será submetida a **dupla revisão cega** com registro de causa-raiz antes do cálculo dos desfechos secundários.
