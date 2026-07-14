---
status: active
last_updated: 2026-07-14
owner: "Wagner / CVSS project"
tags:
  - cvss
  - database
  - prisma
  - postgresql
aliases:
  - "CVSS Database"
---

# Database

## Estado atual

O schema Prisma atual contém uma base limitada com `Run`, `Assessment`, `Comparison` e `AuditEvent`. Isso é parcial e não representa o domínio operacional completo.

## Modelo-alvo

- usuários;
- organizações;
- membros;
- papéis e permissões;
- ambientes;
- ativos;
- componentes;
- vulnerabilidades;
- achados;
- evidências;
- importações e linhas de importação;
- execuções do watcher e jobs;
- propostas e versões de análise;
- decisões humanas;
- tratamentos;
- ações e evidências de conclusão;
- eventos de auditoria.

## Requisitos

- chaves e restrições organizacionais;
- índices para consultas operacionais;
- migrations versionadas;
- seed mínimo e reproduzível;
- testes de integridade e isolamento;
- histórico imutável para propostas e decisões;
- idempotência de importações e execuções.

## Notas relacionadas

[[ARCHITECTURE]] · [[AUTH_RBAC]] · [[WATCHER]] · [[06_Data_Model]] · [[07_Testing_and_Validation]]
