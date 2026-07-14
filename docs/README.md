---
status: active
last_updated: 2026-07-14
owner: "Wagner / CVSS project"
tags:
  - cvss
  - documentation
  - obsidian
  - index
aliases:
  - "CVSS Docs"
  - "Documentation Hub"
related_files:
  - docs/00_Index.md
  - docs/99_Obsidian_Conventions.md
  - docs/real_world/OFFICIAL_CONTEXTUAL_INTEGRATION.md
  - core/cvss_real_world.py
---

# CVSS Documentation Hub

A navegação principal está em [[00_Index]].

## Fontes operacionais

- [[CURRENT_PHASE_STATUS]]
- [[NEXT_ACTIONS]]
- [[ROADMAP]]
- [[ARCHITECTURE]]

## Regra central

`official_cvss` deriva somente do vetor CVSS oficial. A camada contextual pode usar evidências operacionais, mas nunca deve ser apresentada como CVSS oficial.

Consulte [[decisions/ADR-001-official-vs-contextual-separation]] e [[real_world/OFFICIAL_CONTEXTUAL_INTEGRATION]].
