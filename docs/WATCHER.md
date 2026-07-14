---
status: active
last_updated: 2026-07-14
owner: "Wagner / CVSS project"
tags:
  - cvss
  - watcher
  - operations
aliases:
  - "CVSS Watcher"
---

# Watcher

## Estado atual

Existe um motor Python e um fluxo demonstrativo de análise contextual. Isso comprova regras, rastros e geração de resultados, mas ainda não constitui um watcher operacional multiusuário.

## Estado-alvo

O watcher recebe achado, ativo, contexto e evidência e produz:

- CVSS original;
- prioridade contextual separada;
- justificativa;
- confiança;
- incerteza;
- tratamento proposto;
- versão do motor e das regras;
- rastreabilidade das evidências usadas.

## Ciclo operacional

A execução deve poder ser iniciada, acompanhada, persistida, versionada, reprocessada e auditada. Falhas e tentativas precisam ser registradas.

## Limite de autoridade

O watcher propõe. Ele nunca altera automaticamente o ambiente, aceita risco, fecha vulnerabilidade, muda prioridade ou conclui tratamento. Essas ações exigem decisão humana autorizada e justificativa.

## Dependências

[[ARCHITECTURE]] · [[DATABASE]] · [[AUTH_RBAC]] · [[04_Contextual_Engine]] · [[07_Testing_and_Validation]]
