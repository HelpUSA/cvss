---
status: active
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - documentation
  - obsidian
  - conventions
aliases:
  - "Obsidian Conventions"
  - "Vault Conventions"
related_files:
  - docs/README.md
  - docs/00_Index.md
---

# Obsidian Conventions

## Purpose

This note defines how the `docs/` folder should be maintained as an Obsidian-compatible Markdown vault.

## Note format

Each maintained note should use:

- YAML frontmatter at the top.
- One H1 title.
- Short sections.
- Internal links in Obsidian style, such as [[02_Architecture]].
- Relative code paths for implementation references, such as `../core/cvss_real_world.py`.

## Required properties

Use these properties when practical:

- `status`
- `last_updated`
- `owner`
- `tags`
- `aliases`
- `related_files`

## Linking policy

Prefer linking to an existing note instead of duplicating long content.

Use existing legacy notes as source references, especially:

- [[CURRENT_HANDOFF]]
- [[ARCHITECTURE]]
- [[TEST_REPORT]]
- [[real_world/OFFICIAL_CONTEXTUAL_INTEGRATION]]
- [[real_world/REAL_WORLD_PHASE_STATUS]]

## CVSS terminology rule

Never label contextual prioritization as official CVSS.

Use [[decisions/ADR-001-official-vs-contextual-separation]] as the controlling decision record.
