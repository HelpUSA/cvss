---
status: active
last_updated: 2026-07-14
owner: "Wagner / CVSS project"
tags:
  - cvss
  - data-model
  - exports
aliases:
  - "CVSS Data Model"
related_files:
  - core/cvss_real_world.py
  - docs/schemas/PIPELINE_OUTPUT_SCHEMA.md
  - docs/schemas/SCENARIO_INPUT_SCHEMA.md
---

# Data Model

## Estado atual

O modelo científico e os formatos de saída existentes suportam protótipos e demonstrações. No produto web, o schema Prisma ainda cobre somente uma base pequena e precisa ser ampliado.

## Domínio operacional

O domínio-alvo está descrito em [[DATABASE]] e inclui identidade, organizações, ambientes, ativos, vulnerabilidades, evidências, importações, execuções, propostas, decisões, tratamentos, ações e auditoria.

## Regras

- preservar vetores e resultados oficiais;
- versionar análises contextuais;
- não sobrescrever decisões anteriores;
- registrar evidências usadas;
- isolar dados por organização;
- manter idempotência de importações e jobs.

## Formatos científicos e de integração

Os schemas e formatos históricos permanecem válidos como referências do motor e do artigo, mas não substituem migrations e entidades operacionais.

## Notas relacionadas

[[DATABASE]] · [[ARCHITECTURE]] · [[WATCHER]] · [[real_world/OFFICIAL_CONTEXTUAL_INTEGRATION]]
