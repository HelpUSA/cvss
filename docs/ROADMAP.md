# Operational roadmap

## Fase 0 — Fechamento da base

Estado: encerrada em 14 de julho de 2026.

Entregáveis: documentação coerente, inventário real/parcial/demo/ausente, arquitetura canônica com Next.js na interface web, Prisma com PostgreSQL na persistência e Python restrito à engine CVSS, watcher e processamento interno suportado, além de compilação, 52 testes, JavaScript, TypeScript, build, pipeline real, auditoria das 102 notas, riscos e Git limpo.

## Fase 1 — Fundação multiusuário

Entregáveis: arquitetura fechada, autenticação, sessões, recuperação, RBAC, organizações, membros e ambientes.

## Fase 2 — Domínio e importação

Entregáveis: modelo ampliado, migrations, seed, testes e primeiro fluxo CSV/JSON com validação, prévia, importação e inventário.

## Fase 3 — Aplicação web operacional

Entregáveis: áreas pública, autenticada e administrativa; navegação por organização e ambiente; estados de erro e permissão.

## Fase 4 — Watcher persistido

Entregáveis: fila, worker Python, execução acompanhável, resultados versionados, confiança, incerteza, justificativa, reprocessamento e trilha de auditoria. O watcher apenas propõe alterações.

## Fase 5 — Tratamentos, relatórios e auditoria

Entregáveis: decisões humanas, responsáveis, prazos, evidências de conclusão, reanálise, filtros e relatórios operacionais.

## Fase 6 — Portal científico

Pré-condição: fluxo operacional principal estável.

Entregáveis: atribuição individual, cegamento, submissão final, bloqueio e compatibilidade com o protocolo existente. Nenhuma estatística real será gerada antes das respostas humanas bloqueadas.

## Fase 7 — Produção

Entregáveis: testes unitários, integração e E2E, segurança, uploads, segredos, observabilidade, backups, erros, CI/CD, deploy e validação pública.

## Marco inicial de produto

Um operador autenticado cria um ambiente, importa CSV/JSON e visualiza ativos e vulnerabilidades.

## Notas relacionadas

[[00_Index]] · [[CURRENT_PHASE_STATUS]] · [[NEXT_ACTIONS]] · [[ARCHITECTURE]] · [[DEPLOYMENT_VERIFICATION]]

<!-- auth1b-roadmap-2026-07-20:start -->
## Fase 1 progress update — 2026-07-20

Delivered:

- Auth-1A schema and cryptographic foundation;
- Auth-1B operational login, logout, sessions, protected application
  area and explicit platform-administrator bootstrap.

Next:

- Auth-1C organization context, memberships, RBAC and tenant isolation.
<!-- auth1b-roadmap-2026-07-20:end -->
