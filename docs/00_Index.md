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
  - "CVSS Index"
  - "Vault Index"
related_files:
  - docs/README.md
  - docs/99_Obsidian_Conventions.md
  - docs/CURRENT_HANDOFF.md
  - docs/real_world/REAL_WORLD_PHASE_STATUS.md
---

# CVSS Project MOC

> [!info] Fonte principal de navegação
> Este mapa organiza o estado operacional atual. Notas de fases anteriores permanecem como histórico, mas não substituem [[CURRENT_PHASE_STATUS]], [[ROADMAP]] e [[NEXT_ACTIONS]].

## Estado e direção

- [[CURRENT_PHASE_STATUS|Status atual]]
- [[NEXT_ACTIONS|Próximas ações]]
- [[ROADMAP|Roadmap operacional]]
- [[CURRENT_HANDOFF|Handoff atual]]
- [[DOCUMENTATION_AUDIT|Auditoria da documentação]]

## Arquitetura e produto

- [[ARCHITECTURE|Arquitetura operacional]]
- [[WEB_APPLICATION|Aplicação web]]
- [[AUTH_RBAC|Autenticação e RBAC]]
- [[DATABASE|Banco de dados]]
- [[WATCHER|Watcher e análise contextual]]
- [[04_Contextual_Engine|Motor contextual]]
- [[03_CVSS_Official_Core|Núcleo CVSS oficial]]
- [[05_Real_World_Wrapper|Wrapper real-world]]

## Qualidade e operação

- [[07_Testing_and_Validation|Testes e validação]]
- [[TEST_REPORT|Relatório de testes]]
- [[DEPLOYMENT_VERIFICATION|Deploy e verificação pública]]
- [[99_Obsidian_Conventions|Convenções do vault]]
- [[10_Changelog|Changelog]]

## Pesquisa científica

- [[09_Paper_or_Article|Artigo e protocolo]]
- [[ARTICLE_STATUS|Status do artigo]]
- [[ARTICLE_PHASE14_PREANALYSIS_GATE_CVSS40|Gate de pré-análise]]
- [[ARTICLE_PHASE15_GATED_ANALYSIS_CVSS40|Motor estatístico com gate]]
- [[ARTICLE_CLAIM_GUARDRAILS_CVSS40|Restrições de alegações]]

## Decisões controladoras

- [[decisions/ADR-001-official-vs-contextual-separation|Separação entre CVSS oficial e priorização contextual]]

## Regra central

`official_cvss` deriva somente do vetor CVSS oficial. A camada contextual pode usar evidências operacionais, mas nunca deve ser apresentada como CVSS oficial.
