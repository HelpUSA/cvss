---
status: active
last_updated: 2026-07-14
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

## Escopo

A pasta `docs/` é mantida como vault Obsidian e documentação versionada do projeto.

## Formato

- Preserve o frontmatter existente.
- Use frontmatter em novas notas mantidas quando isso seguir o padrão das notas vizinhas.
- Não crie propriedades ou tags redundantes.
- Use um único H1 por nota.
- Prefira seções curtas e links para a fonte de verdade.

## Links internos

Use wikilinks, por exemplo `[[ARCHITECTURE]]` ou `[[real_world/OFFICIAL_CONTEXTUAL_INTEGRATION|Integração oficial/contextual]]`.

Links Markdown permanecem adequados para URLs externas e arquivos fora do vault. Não use link Markdown para outra nota quando um wikilink resolver o mesmo destino.

## Fonte de verdade

- Estado: [[CURRENT_PHASE_STATUS]]
- Ordem de trabalho: [[NEXT_ACTIONS]]
- Roadmap: [[ROADMAP]]
- Arquitetura: [[ARCHITECTURE]]
- Navegação: [[00_Index]]

Notas históricas devem apontar para essas fontes quando sua orientação estiver supersedida.

## Terminologia

Nunca rotule priorização contextual como CVSS oficial. A decisão controladora é [[decisions/ADR-001-official-vs-contextual-separation]].
