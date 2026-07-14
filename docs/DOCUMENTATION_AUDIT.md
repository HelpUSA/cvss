---
status: active
last_updated: 2026-07-14
owner: "Wagner / CVSS project"
tags:
  - cvss
  - documentation
  - audit
aliases:
  - "CVSS Documentation Audit"
---

# Documentation audit

## Escopo

Auditoria integral da pasta `docs/`, com 108 arquivos lidos antes das alterações.

## Problemas centrais encontrados

- índice orientado por fases históricas do artigo, sem MOC operacional;
- status antigo orientando abandonar Next.js e usar somente deploy estático;
- planos e handoffs com prioridades conflitantes;
- mistura entre protótipo, demo e produto operacional;
- deploy público tratado como confirmado por registros históricos;
- status científico sem uma declaração curta e inequívoca sobre a espera dos três revisores;
- links internos em Markdown no índice, apesar do padrão Obsidian.

## Decisões aplicadas

- [[00_Index]] tornou-se o MOC principal;
- [[CURRENT_PHASE_STATUS]], [[NEXT_ACTIONS]], [[ROADMAP]] e [[ARCHITECTURE]] são as fontes operacionais;
- histórico científico foi preservado e não foi reescrito como resultado;
- funcionalidades foram classificadas como real, parcial, demo ou ausente;
- foram criadas notas focadas para [[WEB_APPLICATION]], [[AUTH_RBAC]], [[DATABASE]] e [[WATCHER]];
- a orientação “somente estático” foi marcada como supersedida para o produto operacional;
- deploy passou a exigir nova verificação;
- links das notas centrais usam wikilinks.

## Arquivos centrais alterados ou criados

- `docs/00_Index.md`
- `docs/README.md`
- `docs/CURRENT_PHASE_STATUS.md`
- `docs/NEXT_ACTIONS.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE.md`
- `docs/CURRENT_HANDOFF.md`
- `docs/01_Project_Overview.md`
- `docs/06_Data_Model.md`
- `docs/07_Testing_and_Validation.md`
- `docs/08_Dashboard_and_Exports.md`
- `docs/09_Paper_or_Article.md`
- `docs/ARTICLE_STATUS.md`
- `docs/DEPLOYMENT_VERIFICATION.md`
- `docs/99_Obsidian_Conventions.md`
- `docs/WEB_APPLICATION.md`
- `docs/AUTH_RBAC.md`
- `docs/DATABASE.md`
- `docs/WATCHER.md`
- `docs/DOCUMENTATION_AUDIT.md`

## Limites

Não foram acessadas nem modificadas respostas, submissões, chaves de adjudicação ou artefatos privados de revisores.

## Validação

Os resultados finais de links, testes, build, diff, commit e push devem ser registrados somente após execução real.

## Notas relacionadas

[[00_Index]] · [[CURRENT_PHASE_STATUS]] · [[NEXT_ACTIONS]] · [[07_Testing_and_Validation]]

<!-- verified-validation-2026-07-14:start -->
## Resultado verificado em 2026-07-14

A auditoria operacional da documentação foi executada sobre 102 notas Markdown.

### Estrutura do vault

- Wikilinks quebrados: `0`.
- Wikilinks ambíguos: `0`.
- Links Markdown internos para notas `.md`: `0`.
- Atividades ordenadas em [[NEXT_ACTIONS]]: `12`, numeradas de 1 a 12.
- Links obrigatórios ausentes no MOC [[00_Index]]: `0`.
- Afirmações indevidas sobre autenticação pronta, produção pronta, resultados dos revisores ou alterações automáticas do watcher: `0`.
- `git diff --check`: aprovado.

### Validação do código

- `python -m pytest -q`: `52 passed`.
- `node --check app.js`: aprovado.
- `npx.cmd tsc --noEmit`: aprovado.
- `npm.cmd run build`, em `web/`: aprovado.
- `python scripts/validate_real_pipeline.py`: aprovado.
- Geração do Prisma Client 6.19.0: aprovada.
- Build Next.js 15.5.18: aprovado.

### Falha técnica identificada

`python -m compileall app` não foi aprovado porque dois protótipos Python antigos possuem erros sintáticos:

- `app/web/dashboard.py`: aspas escapadas incorretamente na chamada de `st.spinner`, além de texto com codificação corrompida.
- `app/web/fastapi_server.py`: importações e configuração de CORS malformadas, incluindo `From`, `exports`, `CARS middleware` e símbolos FastAPI incorretos.

Esses arquivos não foram corrigidos nesta atualização porque o escopo é documental. A falha confirma que a camada FastAPI/Streamlit deve permanecer classificada como **parcial e não operacional** até a conclusão da atividade 2 de [[NEXT_ACTIONS]].

### Decisão de fechamento

A documentação pode ser versionada porque seus validadores passaram e porque a falha de compilação foi identificada, registrada e não é causada pelas alterações documentais.

A Fase 0 ainda não deve ser considerada formalmente encerrada. Seu fechamento depende da correção ou retirada dos protótipos Python inválidos e da repetição de `python -m compileall app`.
<!-- verified-validation-2026-07-14:end -->
