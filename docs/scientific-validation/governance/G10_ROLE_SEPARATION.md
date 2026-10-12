# Matriz de Segregação de Funções e Papéis para Custódia C1 e C2 (Gate G10)

**Documento**: `G10_ROLE_SEPARATION.md`  
**Versão**: `1.3` (Revisado per CG-20261010-013 e CG-20261010-014)  
**Data**: 12 de Outubro de 2026  
**Finalidade**: Definir formalmente as fronteiras operacionais, vedações de acesso, matriz de segregação de deveres (*Segregation of Duties — SoD*) e regras de custódia técnica no modelo de Custódia em Duas Etapas (*Two-Stage Custody*).

---

## 1. Princípios de Segregação e Estado de Congelamento

1. **Estado de Congelamento**: O status técnico da base de código do motor inferencial é denominado **`ENGINEERING_FREEZE_CANDIDATE`**. O gate global **`SAFE_TO_FREEZE` permanece estritamente `NO`** durante toda a tramitação, até que os Gates G9 (Aprovação Ética Formal do CEP) e G10 (Custódia Independente) estejam plenamente concluídos e auditados.
2. **Segregação Zero entre Desenvolvedores e Dados Confirmatórios**: A equipe de engenharia e desenvolvimento não possui acesso, controle de execução ou capacidade de intervenção sobre os dados brutos ou sobre o runtime pós-deslacre.

---

## 2. Definição dos Papéis do Protocolo

| Papel | Titular / Responsável | Atribuições Principais | Vedações Absolutas |
|---|---|---|---|
| **Custodiante Independente Titular** | Auditor Externo Independente A | Guarda lógica do cofre cifrado C1/C2, custódia do Componente de Chave A (Dual-Control 2-of-2), manutenção do log append-only com ancoragem externa, liberação da Etapa 1 (*Reference Release*) e supervisão da Etapa 2. | Proibido de inspecionar predições do modelo antes do bloqueio do padrão-ouro; proibido de alterar código ou modelos. |
| **Co-Custodiante Independente Suplente** | Auditor Externo Independente B | Guarda do Componente de Chave B (Dual-Control 2-of-2), suplência técnica formal e co-validação de integridade nos checkpoints operacionais. | Mesmas vedações do custodiante titular. |
| **Pesquisador Responsável (PI)** | Wagner Santos (`helpus.ecommerce@gmail.com`) | Gestão metodológica, submissão ao CEP competente via fluxo SINEP, subscrição formal da ordem de requisição de deslacre após cumprimento dos gates. | **Não detém chave técnica de decifragem**; proibido de acessar cenários brutos individuais ou alterar vetores após o congelamento. |
| **Comitê de Ética em Pesquisa (CEP)** | CEP Competente conforme fluxo SINEP | Avaliação ética do protocolo, emissão de parecer e acompanhamento regulatório institucional. | **Não possui custódia operacional de chaves criptográficas técnicas**. |
| **Equipe de Desenvolvimento IA** | Engenheiros HelpUS / Antigravity | Manutenção do candidato a congelamento (`ENGINEERING_FREEZE_CANDIDATE`) até a homologação. | **Cegamento Total e Sem Controle de Execução**: Proibido de visualizar cenários de C1/C2 e proibido de operar o runtime durante o deslacre. |
| **Painel de Especialistas (5 avaliadores)** | 5 Especialistas Independentes em Segurança | Avaliação cega dos cenários na Etapa 1 (*Reference Release*), pontuação individual, participação nas sessões de adjudicação colegiada. | Proibidos de conhecer predições HelpUS, de compartilhar notas antes da sessão de adjudicação e de manter interesse financeiro no resultado. |
| **AUTOMATED_CONFIRMATORY_RUNNER** | Runtime Pré-Congelado e Contêinerizado (*Air-gapped*) | Execução determinística e automatizada de uma única passada (*one-shot*) dos cenários de teste através do binário congelado, sem operador humano. | Incapaz de comunicação externa (egress desativado); material de memória destruído por higienização segura (*memory wiping*). |
| **Auditor Estatístico Independente** | Perito Estatístico Externo | Execução estrita do Plano de Análise Estatística (`G9_SAP_v1.0.md`) sobre os resultados lacrados, utilizando script analítico congelado. | Proibido de realizar testes post-hoc não pré-especificados ou calibrações retrospectivas. |

---

## 3. Matriz de Segregação de Funções (SoD Matrix por Fase)

| Ação Operacional | Fase | Custodiante Titular (Chave A) | Co-Custodiante Suplente (Chave B) | Pesquisador Responsável | Equipe Dev / IA | Painel de Especialistas | Runner Automatizado | Estatístico Independente |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Criptografia inicial de C1/C2 | Fase 1 | **EXECUTA** | Co-Participa | Autoriza Metadados | **VEDADO** | **VEDADO** | N/A | **VEDADO** |
| Guarda de Chave Criptográfica | Todas | **CHAVE A** | **CHAVE B** | **VEDADO** | **VEDADO** | **VEDADO** | N/A | **VEDADO** |
| Declaração de `SAFE_TO_FREEZE` | Fase 1 a 4 | **`NO`** | **`NO`** | **`NO`** | **`NO`** | N/A | N/A | **`NO`** |
| Liberação de Cenários à Avaliação Humana | Fase 2 | **LIBERA ENTRADAS** | Valida | Ciência | **VEDADO** | **RECEBE ENTRADAS** | N/A | Supervisiona |
| Avaliação e Pontuação de Vetores | Fase 3 | Registra | Registra | **VEDADO** | **VEDADO** | **AVALIA / PONTUA** | N/A | Tabula |
| Trancamento do Padrão-Ouro (SHA-256) | Fase 3 | **LACRA HASH** | Co-Assina | Ciência | **VEDADO** | Aprova Adjudicação | N/A | **AUDITA HASH** |
| Cerimônia Dual-Control de Deslacre | Fase 4 | **APLICA CHAVE A** | **APLICA CHAVE B** | Requisita | **VEDADO** | N/A | N/A | Testemunha |
| Execução Técnica pós-deslacre | Fase 4 | Supervisiona | Supervisiona | Supervisiona | **VEDADO** | N/A | **EXECUTA ONE-SHOT** | Supervisiona |
| Visualização de Saídas Brutas Pré-Lacre | Fase 4 | **VEDADO** | **VEDADO** | **VEDADO** | **VEDADO** | N/A | Grava e Cifra | **VEDADO** |
| Alteração de Código/Pesos pós-deslacre | Fase 4/5 | **VEDADO** | **VEDADO** | **VEDADO** | **VEDADO TOTAL** | **VEDADO** | N/A | **VEDADO** |
| Execução do Script Estatístico SAP | Fase 5 | Testemunha | Testemunha | Testemunha | **VEDADO** | Testemunha | N/A | **EXECUTA SCRIPT** |

---

## 4. Salvaguardas Contra Violação de Papéis

1. Se qualquer operador da equipe de desenvolvimento intervir no ambiente pós-deslacre, o experimento confirmatório é automaticamente abortado e desqualificado.
2. Nenhuma chave criptográfica parcial pode ser transferida, combinada ou armazenada fora da cerimônia formal de decifragem autorizada.
