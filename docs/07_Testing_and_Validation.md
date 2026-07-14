---
status: active
last_updated: 2026-07-14
owner: "Wagner / CVSS project"
tags:
  - cvss
  - testing
  - validation
aliases:
  - "CVSS Tests"
  - "Validation"
related_files:
  - core/cvss31.py
  - core/cvss_environmental_engine.py
  - core/cvss_real_world.py
  - docs/TEST_REPORT.md
---

# Testing and Validation

## Objetivo atual

Fechar a Fase 0 com evidência reproduzível, separando teste aprovado, comando indisponível e funcionalidade ainda ausente.

## Matriz mínima

- Python: `python -m pytest -q`.
- Sintaxe JavaScript: `node --check app.js`.
- TypeScript: `npx tsc --noEmit` no diretório `web`, quando suportado pelo projeto.
- Next.js: `npm run build` no diretório `web`.
- Python adicional: compilação/importação dos módulos relevantes.
- Documentação: links Obsidian resolvidos, nomes consistentes e `git diff --check`.

O projeto não possui atualmente um script `npm run lint` confirmado; a ausência do comando deve ser registrada como comando indisponível, não como falha funcional.

## Critérios

- Não registrar “passou” sem saída real do comando.
- Registrar versão, comando, código de saída e falha relevante.
- Distinguir teste de protótipo de teste de fluxo operacional.
- Não usar dados ou respostas privadas dos revisores.

## Cobertura futura

Autenticação, isolamento organizacional, importações, fila, watcher, decisões, tratamentos, relatórios, uploads, segurança e E2E.

## Notas relacionadas

[[00_Index]] · [[TEST_REPORT]] · [[CURRENT_PHASE_STATUS]] · [[DEPLOYMENT_VERIFICATION]]

<!-- verified-validation-2026-07-14:start -->
## Validation snapshot — 2026-07-14

| Verificação | Resultado |
|---|---|
| Auditoria de 102 notas Markdown | Aprovada |
| Wikilinks quebrados ou ambíguos | 0 |
| Links Markdown internos para `.md` | 0 |
| Próximas atividades ordenadas | 12 de 12 |
| Pytest | 52 testes aprovados |
| JavaScript `app.js` | Aprovado |
| TypeScript `--noEmit` | Aprovado |
| Build Next.js | Aprovado |
| Validador do pipeline real | Aprovado |
| `git diff --check` | Aprovado |
| `python -m compileall app` | Reprovado em dois protótipos antigos |

### Bloqueio remanescente da Fase 0

A compilação completa de `app/` encontrou erros sintáticos em:

- `app/web/dashboard.py`;
- `app/web/fastapi_server.py`.

Os testes automatizados existentes não importam esses dois módulos e, por isso, os 52 testes podem passar mesmo com os protótipos inválidos.

O estado correto é:

- engine e pipeline testados: funcionais;
- Next.js e TypeScript: compiláveis;
- FastAPI e Streamlit em `app/web`: parciais e não operacionais;
- autenticação, RBAC e fluxo multiusuário: ausentes;
- Fase 0: ainda aberta até a resolução desses dois módulos.
<!-- verified-validation-2026-07-14:end -->
