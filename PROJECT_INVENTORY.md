# PROJECT_INVENTORY.md
# Inventário Completo de Recursos Locais — Projeto HelpUS CVSS AI

Este documento cataloga todos os artefatos, repositórios, bases de dados históricas, scripts estatísticos, artigos científicos e referências bibliográficas identificados localmente no ambiente de desenvolvimento e pesquisa.

---

## 1. Código da Aplicação e Motores de Priorização

| Caminho Local | Descrição do Componente | Relevância | Status Atual | Risco de Desatualização |
| :--- | :--- | :--- | :--- | :--- |
| `D:\AntiG\cvss\app.js` | Lógica central da aplicação web (JavaScript). Contém simulador CVSS v4.0, presets históricos (Trento 2017, Joe, Christine), i18n, visualizador SVG de topologia e integração What-If. | **Crítica** (Core da UI e motor client-side) | Atualizado com terminologia determinística e presets 2017 | Baixo |
| `D:\AntiG\cvss\index.html` | Interface do usuário e painéis (Simulador, Scanner Dinâmico, Auditoria Científica, Calculadora What-If, Modal Virtual Patch). | **Crítica** (Interface com usuário/avaliadores) | Atualizado sem claims inflados (25.0% de transição, sem 60% arbitrário) | Baixo |
| `D:\AntiG\cvss\core\cvss40.py` | Implementação Python da especificação oficial FIRST CVSS v4.0 baseada nas macro-tabelas $EQ_1 \dots EQ_6$. | **Crítica** (Motor de referência backend) | Funcional e validado com vetores canônicos | Baixo |
| `D:\AntiG\cvss\core\ai_evidence_engine.py` | Motor simbólico determinístico em dois estágios: coleta de evidências $\to$ dedução de métricas candidatas com abstenção (`HUMAN_REVIEW_REQUIRED`). | **Crítica** (Núcleo da contribuição científica HelpUS) | Implementado com checagem de reachability e semântica estrita de MAV | Baixo |
| `D:\AntiG\cvss\tools\local_network_scanner.py` | Sonda de telemetria ativa local (sockets, ARP, rotas do host). | Alta (Extração de evidências operacionais) | Funcional | Médio (requer privilégios de rede) |
| `D:\AntiG\cvss\tools\build_reproducible_benchmark.py` | Script que processa o dataset CSV e gera tabelas e gráficos em LaTeX de forma reprodutível. | **Crítica** (Reprodutibilidade científica) | Operando e sincronizado | Baixo |

---

## 2. Fontes da Monografia / Livro Acadêmico (LaTeX)

| Caminho Local | Descrição do Componente | Relevância | Status Atual | Risco de Desatualização |
| :--- | :--- | :--- | :--- | :--- |
| `D:\AntiG\cvss\book_latex\main.tex` | Arquivo mestre do monograph LaTeX. Define pacotes, estrutura e metadados. | **Crítica** (Estrutura do documento) | Sincronizado com cabeçalhos corrigidos (`fancyhdr`) | Baixo |
| `D:\AntiG\cvss\book_latex\references.bib` | Base bibliográfica BibTeX (artigos IEEE, ACM, NIST, ISO, FIRST). | **Crítica** (Fundamentação científica) | Auditado; referências históricas e normativas presentes | Baixo |
| `D:\AntiG\cvss\book_latex\chapters\` | 8 Capítulos temáticos cobrindo fundamentos, arquitetura, telemetria, governança HITL, avaliação empírica e estudos de caso. | **Crítica** (Conteúdo textual e formal) | Revisado para rigor de conferência; terminologia moderada | Baixo |
| `D:\AntiG\cvss\book_latex\chapters\table_6_1_generated.tex` | Tabela 6.1 gerada automaticamente com a matriz de transição ($n=30$). | **Crítica** (Evidência empírica central) | Gerado a partir do CSV de benchmark | Baixo |
| `D:\AntiG\cvss\book_latex\chapters\appendix_c_historical_dataset.tex` | Apêndice C com a tabela landscape detalhando todos os 30 cenários. | **Crítica** (Auditabilidade do dataset) | Gerado automaticamente com ajuste landscape | Baixo |
| `D:\AntiG\cvss\book_latex\figures\` | Figuras vetoriais (PDF) e de alta resolução (PNG) dos gráficos e topologias de 2017. | Alta (Evidências visuais) | Geradas via matplotlib a 300 DPI | Baixo |
| `D:\AntiG\cvss\helpus_cvss_ai_monograph_overleaf.zip` | Pacote ZIP completo empacotado para o Overleaf. | **Crítica** (Entregável para revisão externa) | Atualizado com 37 arquivos limpos | Baixo |

---

## 3. Datasets e Materiais de Pesquisa Histórica (Trento / NeCS 2017)

| Caminho Local | Descrição do Componente | Relevância | Status Atual | Risco de Desatualização |
| :--- | :--- | :--- | :--- | :--- |
| `D:\AntiG\cvss\data\article\cvss40_environmental_scenarios.csv` | **Dataset B (Development Benchmark)**: 30 cenários contemporâneos (12 reais baseados em CVEs recentes + 18 sintéticos). | **Crítica** (Benchmark de desenvolvimento do motor) | Congelado e auditado para $n=30$ | Médio (exige rotulagem de proveniência formal) |
| `d:\Documents\OneDrive\Wagner\doutorado\UnitN\SVN\Papers\ESSOS-2017\Data\R\dataset.csv` | **Dataset A1 (Historical Human Results)**: Dados brutos de 29 participantes avaliando 12 CVEs em redes simples e complexas no estudo de Santos et al. (2017). | **Histórica Inestimável** (Origem primária dos dados de erro humano) | Preservado intacto; somente leitura | Nulo (dado histórico imutável) |
| `d:\Documents\OneDrive\Wagner\doutorado\UnitN\SVN\Papers\ESSOS-2017\Data\R\analysis.R` | Script R original de 2017 executando o teste exato de Fisher ($p = 4.2 \times 10^{-6}$), ANOVA e Kruskal-Wallis. | **Metodológica Primária** (Comprovação da fórmula estatística) | Preservado intacto; confirma $p = 4.2 \times 10^{-6}$ e Odds Ratio $\approx 3.4$ | Nulo (código histórico de referência) |
| `d:\Documents\OneDrive\Wagner\doutorado\UnitN\SVN\Papers\ESSOS-2017\Data\CVSSEnvData.csv` | Dados de pontuação ambiental por participante e por cenário em 2017. | Alta (Validação detalhada de variância humana) | Preservado intacto | Nulo |
| `d:\Documents\OneDrive\Wagner\doutorado\greenfielddata\Artigos anteriores\Estimating the Assessment Difficulty of CVSS Environmental Metrics - An Experiment.pdf` | Artigo original publicado em 2017 (*Santos et al., ESSoS 2017*). | **Científica Primária** (Artigo de referência da coautoria de Wagner Santos) | Publicado em conferência internacional | Nulo |
| `d:\Documents\OneDrive\Wagner\doutorado\UnitN\SVN\CyberOperationalRisk\Data\UNITN-PaloAlto\fw_traffic_log.csv` | Logs reais de firewall corporativo Palo Alto da Universidade de Trento. | Alta (Base para modelagem de evidências reais de telemetria) | Preservado intacto | Médio (logs de 2016-2017) |
| `d:\Documents\OneDrive\Wagner\doutorado\UnitN\SVN\CyberOperationalRisk\Data\VCDB Financial sector\Data\original.csv` | Base de incidentes VERIS Community Database (VCDB) do setor bancário e financeiro. | Média (Base para discussões de risco operacional financeiro) | Preservado intacto | Médio |

---

## 4. Diretriz de Integridade
Os arquivos históricos contidos em `d:\Documents\OneDrive\Wagner\doutorado\` são fontes primárias de prova e **NÃO SERÃO ALTERADOS**. Toda derivação, re-anotação ou processamento será executada estritamente dentro do workspace `D:\AntiG\cvss\`.
