# R6-A1 Preregistration

## 1. Motivation
R6 é uma extensão científica pré-planejada para aumentar a validade externa, auditabilidade e independência de verificação do R5, orientada à submissão em venues A1 de segurança (IEEE S&P / USENIX Security / ACM CCS / NDSS). O R5 permanece como baseline histórico congelado e imutável. Todos os protocolos, hipóteses e limites epistemológicos aqui estabelecidos foram pré-registrados antes de qualquer nova coleta de dados ou execução experimental.

## 2. R6 Research Questions
- **RQ-R6-1**: O contrato de verificação mantém integridade e cobertura em um novo corpus externo held-out, independente dos 30 casos R5?
- **RQ-R6-2**: Como schema v2 closed-world altera detecção de mutações e compatibilidade comparado ao open-world v1?
- **RQ-R6-3**: Uma camada estruturada de governance override pode tornar os desvios operacionais auditáveis sem modificar a política nominal da Eq. 8?
- **RQ-R6-4 (Differential Scorer Concordance)**: Qual é o grau de concordância e quais classes de discrepância, se houver, são observadas entre o scorer primário CVSS v4.0 e uma implementação secundária independente sob um corpus de vetores pré-definido?

## 3. External Held-Out Corpus Protocol
O protocolo detalhado e congelado do corpus held-out encontra-se especificado em `validation/article/r6_a1_heldout_corpus_protocol.md`, regido pelos seguintes princípios fixados ANTES de qualquer coleta:
- Fonte primária: `GitHub Advisory Database reviewed global advisories` (excluindo malware).
- Fonte secundária de cross-check: `OSV_POST_LOCK_ONLY` (consulta estritamente posterior ao lacre do corpus primário, com zero autoridade de seleção).
- Janela temporal imutável: `2026-09-01T00:00:00Z` até `2026-10-01T00:00:00Z` (último mês civil completo anterior ao freeze do pré-registro).
- Regra determinística de inclusão/exclusão com chave canônica `GHSA ID`; exclusão de unreviewed, malware e sobreposição com R5.
- Tamanho natural da janela registrado inicialmente; se redução for necessária, aplicação de ordenação pseudo-aleatória determinística via SHA-256 com seed do commit `c0b4025d9f560b8e525accd17e1b075cd23a355b`.
- Zero reutilização dos 30 cenários R5 e zero escolha manual por conveniência ou resultado.
- Limite estrito de externalidade: advisories públicos testam transferência do contrato de verificação e não constituem ground truth de métricas ambientais organizacionais sem contexto controlado explicitamente rotulado.
- Provenance completo, snapshot imutável e hash SHA-256 gerados sob controle fail-closed antes da análise.
*Nota de Governança*: O corpus NÃO é coletado nesta ordem; este documento define exclusivamente o protocolo.

## 4. Schema v2 Closed-World Protocol
- Tratar closed-world como hipótese experimental do R6, NÃO como correção retroativa do R5.
- Definir recursivamente quais objetos do trace rejeitam atributos não declarados (`additionalProperties: false` em toda a hierarquia de objetos e sub-objetos).
- `additionalProperties: false` aplicado somente após especificação prévia de eventuais pontos formais de extensão.
- Preservar o resultado F3 (0/16 rejeitados no open-world v1) do R5 integralmente como baseline.
- Comparar v1 open-world vs v2 closed-world de forma pareada sobre os 120 mutantes da campanha R3.
- NÃO alterar o schema v2 após observar os resultados da nova campanha de mutação.

## 5. Governance Override Protocol
- A Equação 8 permanece estritamente nominal e NÃO recebe termos de ajuste post-hoc como `delta_audit(e)`.
- Definir uma camada estruturada de governança separada da Eq. 8 contendo, no mínimo:
  - `nominal_policy_priority`
  - `pre_override_priority`
  - `post_override_priority`
  - `authorized_governance_override`
  - `reason_code`
  - `evidence_ids`
  - `authorization_state`
  - `review_required`
- O override deve ser explícito, rastreável, formalmente human-authorized e nunca silencioso (sem sobrescrever a pontuação nominal na origem).
- Os quatro casos com desvios operacionais do R5 (NVD overrides) NÃO podem ser usados para ajustar parâmetros com o objetivo de forçar artificialmente conformidade de 30/30.

## 6. Differential Validation Plan
- Planejar (sem executar nesta fase) a comparação sistemática com uma segunda implementação CVSS v4.0 independente e de código aberto sob corpus de vetores pré-definido.
- **Hipótese H-R6-4**: The primary and secondary implementations will produce equivalent normalized CVSS v4.0 scores, severity labels, and nomenclature for all inputs in the preregistered differential corpus.
- Toda e qualquer discrepância observada será rigorosamente preservada, documentada e reportada na íntegra, sem descarte, supressão ou ajuste ad-hoc.
- **Métricas Neutras de Comparação Diferencial**:
  - `exact score agreement count/rate`
  - `severity agreement count/rate`
  - `nomenclature agreement count/rate`
  - `parser acceptance disagreement count`
  - `vector canonicalization disagreement count`
  (Nenhum valor numérico ou taxa prévia é assumido ou registrado; avaliação estritamente pré-experimental).

## 7. Anti-Retuning Lock
Após o início das execuções experimentais do R6:
- Não alterar pesos de scoring após observar resultados do corpus held-out.
- Não modificar regras do schema para elevar artificialmente a taxa de rejeição de mutantes.
- Não remover casos difíceis, anômalos ou com falha de verificação.
- Não alterar critérios de inclusão após o download do corpus.
- Qualquer alteração metodológica forçada vira obrigatoriamente uma versão R6.1 e deve ser explicitamente declarada como desvio pós-resultado.

## 8. Claim Boundaries
É estritamente proibido alegar:
- Proibido alegar formal verification / mathematical proof (utilizar apenas: *machine-checkable verification*, *independent trace verification*, *specification conformance testing*, *metamorphic testing*).
- Population generalization para todo o ecossistema de vulnerabilidades sem desenho estatístico formal correspondente.
- Expert agreement sem adjudicação humana formalmente aprovada pelo CEP e concluída.
- Predictive superiority ou alegações de predição de incidentes futuros.
- Real-world risk reduction sem estudo de intervenção longitudinal.
- Autonomous scoring authority (o watcher é normalizador e resolvedor determinístico de políticas sob HITL obrigatório).

## 9. Governance Locks
- $G_{10B}$ = `NOT_AUTHORIZED_NOT_EXECUTED`
- $C_1 / C_2$ = `SEALED_NOT_USED under the existing fail-closed governance gate`
- Adjudicação Humana = `NOT_COMPLETED`

## 10. Framing
- Primary Framing Recomendado:
  `Auditable, machine-checkable, human-authorized operationalization of CVSS v4.0 Environmental metrics.`
- A priorização de vulnerabilidades é posicionada como aplicação e estudo de caso prático, e não como claim central de superioridade preditiva sobre outros sistemas.
