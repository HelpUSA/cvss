# Matriz de Segregação de Funções e Papéis para Custódia C1 e C2 (Gate G10)

**Documento**: `G10_ROLE_SEPARATION.md`  
**Versão**: `1.1`  
**Data**: 12 de Outubro de 2026  
**Status**: Em conformidade com Diretivas CG-20261010-010 e CG-20261010-011  
**Finalidade**: Definir formalmente as fronteiras operacionais, vedações de acesso e matriz de segregação de deveres (*Segregation of Duties — SoD*) para os datasets confirmatórios C1 e C2 no modelo de Custódia em Duas Etapas (*Two-Stage Custody*).

---

## 1. Princípios Gerais de Segregação de Funções

A integridade do protocolo confirmatório HelpUS CVSS v4.0 apoia-se no princípio da segregação estrita de deveres para eliminar vieses de confirmação, vazamento de dados (*data leakage*) e contaminação de hiperparâmetros (*p-hacking* ou ajuste post-hoc).

Nenhum participante individual detém controle unilateral sobre os dados, sobre o ambiente de execução ou sobre os resultados do experimento.

---

## 2. Definição dos Papéis do Protocolo

| Papel | Titular / Responsável | Atribuições Principais | Vedações Absolutas |
|---|---|---|---|
| **Custodiante Independente Primário** | Auditor Externo Independente Credenciado | Guarda física/lógica do cofre cifrado C1/C2, custódia do Componente de Chave A (Dual-Control 2-of-2), custódia do log imutável de auditoria (*hash-chained*), liberação da Etapa 1 (*Reference Release*) e Etapa 2 (*Machine Unseal*). | Proibido de inspecionar saídas do modelo antes do congelamento e proibido de alterar código ou pesos do sistema. |
| **Custodiante Suplente** | Auditor Externo Substituto Formal | Suplência formal em caso de impedimento por força maior devidamente atestado do titular. | Mesmas vedações do custodiante titular. |
| **Pesquisador Responsável (PI)** | Wagner Santos (`helpus.ecommerce@gmail.com`) | Gestão metodológica geral, submissão ao CEP competente via Plataforma Brasil/SINEP, guarda do Componente de Chave B (Dual-Control), requisição formal de deslacre após cumprimento de todos os gates. | Proibido de acessar cenários brutos deslacrados individualmente ou alterar vetores após congelamento. |
| **Equipe de Desenvolvimento / Engenharia IA** | Engenheiros Antigravity / HelpUS | Desenvolvimento do motor inferencial, testes exploratórios restritos a datasets sintéticos de treino e Dataset B, empacotamento do executável congelado (*frozen binary/container*). | **Cegamento Absoluto**: Proibido de inspecionar qualquer cenário de C1/C2 em qualquer fase antes da publicação final dos resultados. |
| **Painel de Avaliadores Especialistas (5 membros)** | 5 Especialistas Independentes em Cibersegurança / CVSS | Avaliação cega dos cenários na Etapa 1 (*Reference Release*), pontuação individual, participação nas sessões de adjudicação colegiada. | Proibidos de conhecer predições do HelpUS, de compartilhar notas antes da sessão de adjudicação e de manter interesse financeiro no resultado. |
| **Estatístico / Auditor Independente de Resultados** | Perito Estatístico Externo | Execução estrita do Plano de Análise Estatística (`G9_SAP_v1.0.md`) utilizando o script congelado de cálculo, sem acesso aos hiperparâmetros de inferência. | Proibido de realizar testes post-hoc exploratórios não pré-especificados. |

---

## 3. As Cinco Fases Operacionais do Protocolo

O ciclo de vida do experimento confirmatório é estruturado em cinco fases sequenciais e estanques:

1. **Fase 1 — Pré-Registro, Congelamento Técnico e Tramitação Ética**:
   - Congelamento formal do código e artefatos de inferência (`SAFE_TO_FREEZE = YES` apenas após gates de engenharia).
   - Datasets C1 e C2 cifrados com esquema Dual-Control 2-of-2 (Componente A com Custodiante, Componente B com PI).
   - Submissão ética ao CEP competente via SINEP.
   - Equipe de desenvolvimento mantém C1/C2 estritamente lacrados.

2. **Fase 2 — Etapa 1 de Custódia: Liberação de Referência (*Reference Release*)**:
   - Autorização do CEP obtida e formalmente averbada.
   - Custodiante descriptografa e libera **exclusivamente os enunciados dos cenários de teste** (sem predições HelpUS) para os 5 especialistas do painel.
   - **Desenvolvedores permanecem 100% cegos**.

3. **Fase 3 — Avaliação Independente e Trancamento do Padrão-Ouro (*Gold Standard Lock*)**:
   - Especialistas submetem suas notas de forma individual e independente.
   - Realização da rodada de adjudicação formal mediada pelo auditor.
   - Fixação do consenso definitivo dos especialistas.
   - O Custodiante gera e publica o hash SHA-256 do arquivo de consenso (*Gold Standard Reference Lock*).

4. **Fase 4 — Etapa 2 de Custódia: Deslacre da Máquina (*Machine Unseal*)**:
   - Realização da Cerimônia Dual-Control (Custodiante Chave A + PI Chave B).
   - Execução em ambiente isolado (*clean-room*) do executável congelado HelpUS sobre os mesmos cenários de entrada de C1 e C2.
   - Geração e registro dos hashes SHA-256 das saídas inferenciais brutas.
   - Nenhuma nova inferência é permitida (*one-shot execution*).

5. **Fase 5 — Apuração Estatística e Divulgação Científica**:
   - Execução do script congelado de análise estatística (`evaluate_confirmatory.py`).
   - Apuração dos intervalos de confiança Clopper-Pearson, concordância Fleiss' Kappa / Gwet's AC1, SFDR e bootstrap.
   - Elaboração do relatório de auditoria e publicação na monografia.

---

## 4. Matriz de Segregação de Funções (SoD Matrix por Fase)

| Ação Operacional | Fase | Custodiante Independente | Pesquisador Responsável | Equipe Dev / IA | Painel de Especialistas | Estatístico Independente |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Criptografia inicial de C1/C2 | Fase 1 | **EXECUTA** | Co-Participa (Chave B) | **VEDADO** | **VEDADO** | **VEDADO** |
| Guarda da Chave Parcial A | Todas | **CUSTÓDIA EXCLUSIVA** | **VEDADO** | **VEDADO** | **VEDADO** | **VEDADO** |
| Guarda da Chave Parcial B | Todas | **VEDADO** | **CUSTÓDIA EXCLUSIVA** | **VEDADO** | **VEDADO** | **VEDADO** |
| Congelamento do Código / Executável | Fase 1 | **HOMOLOGA HASH** | Homologa | **EXECUTA** | N/A | **AUDITA HASH** |
| Visualização de Cenários C1/C2 | Fase 1 | Cifrado | Cifrado | **VEDADO** | **VEDADO** | Cifrado |
| Liberação de Cenários aos Especialistas | Fase 2 | **LIBERA ENTRADAS** | Autoriza | **VEDADO** | **RECEBE ENTRADAS** | Supervisiona |
| Visualização das Predições HelpUS | Fase 2/3 | **VEDADO** | **VEDADO** | **VEDADO** | **VEDADO** | **VEDADO** |
| Emissão de Notas dos Cenários | Fase 3 | Registra | **VEDADO** | **VEDADO** | **AVALIA / PONTUA** | Tabula |
| Trancamento do Padrão-Ouro (Hash) | Fase 3 | **LACRA E HASH** | Ciência | **VEDADO** | Aprova Adjudicação | **AUDITA HASH** |
| Cerimônia Dual-Control de Deslacre | Fase 4 | **APLICA CHAVE A** | **APLICA CHAVE B** | **VEDADO** | N/A | Supervisiona |
| Execução do Modelo Congelado | Fase 4 | **SUPERVISIONA** | Supervisiona | **RUN CONTROLADO** | N/A | Supervisiona |
| Alteração de Parâmetros/Código pós-deslacre | Fase 4/5 | **VEDAÇÃO TOTAL** | **VEDAÇÃO TOTAL** | **VEDAÇÃO TOTAL** | **VEDAÇÃO TOTAL** | **VEDAÇÃO TOTAL** |
| Execução do Script Estatístico SAP | Fase 5 | Testemunha | Testemunha | **VEDADO** | Testemunha | **EXECUTA SCRIPT** |
| Publicação de Relatório / Monografia | Fase 5 | Assina Parecer | Assina e Publica | Co-Autoria Técnica | Co-Autoria / Agradecimento | Emite Laudo |

---

## 5. Diretrizes de Tolerância a Falhas e Sanitização de Desvios

1. **Tentativa de Acesso Prematuro**:
   Qualquer tentativa de acesso não autorizado aos dados de teste por membros da equipe de engenharia resulta na desqualificação imediata do lote e abertura de processo administrativo de descarte dos dados comprometidos.
2. **Falha de Infraestrutura vs Rerun Proibido**:
   Conforme previsto no `G10_CUSTODY_CHARTER.md`, se ocorrer uma falha puramente técnica de hardware/SO antes da geração dos resultados do modelo, é permitida uma reinicialização restrita de infraestrutura sob ata circunstanciada do Custodiante e do Auditor Estatístico. Nenhuma reinicialização é permitida após a visualização das métricas preliminares.
