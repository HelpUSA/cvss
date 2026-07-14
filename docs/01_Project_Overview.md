---
status: active
last_updated: 2026-07-14
owner: "Wagner / CVSS project"
tags:
  - cvss
  - overview
  - documentation
aliases:
  - "CVSS Project Overview"
related_files:
  - docs/README.md
  - docs/00_Index.md
  - docs/CURRENT_HANDOFF.md
  - docs/real_world/REAL_WORLD_PHASE_STATUS.md
---

# Project Overview

## Propósito

Construir uma aplicação operacional para gestão e priorização de vulnerabilidades, preservando o cálculo CVSS oficial e adicionando uma camada contextual explicável e auditável.

## Frentes do projeto

- núcleo CVSS oficial;
- motor contextual e wrapper real-world;
- aplicação web multiusuário;
- importação e inventário;
- watcher e tratamentos;
- relatórios e auditoria;
- protocolo e artigo científico preservados.

## Limite não negociável

`official_cvss` é calculado somente a partir do vetor oficial. `contextual_environmental` é uma camada de priorização e não deve ser apresentada como CVSS oficial.

## Estado

Consulte [[CURRENT_PHASE_STATUS]] para a matriz real/parcial/demo/ausente e [[NEXT_ACTIONS]] para a ordem oficial de execução.

## Notas relacionadas

[[00_Index]] · [[ARCHITECTURE]] · [[ROADMAP]] · [[decisions/ADR-001-official-vs-contextual-separation]]
