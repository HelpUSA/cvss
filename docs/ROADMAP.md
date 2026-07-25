# Operational roadmap

## Fase 0 â€” Fechamento da base

Estado: encerrada em 14 de julho de 2026.

EntregÃ¡veis: documentaÃ§Ã£o coerente, inventÃ¡rio real/parcial/demo/ausente, arquitetura canÃ´nica com Next.js na interface web, Prisma com PostgreSQL na persistÃªncia e Python restrito Ã  engine CVSS, watcher e processamento interno suportado, alÃ©m de compilaÃ§Ã£o, 52 testes, JavaScript, TypeScript, build, pipeline real, auditoria das 102 notas, riscos e Git limpo.

## Fase 1 â€” FundaÃ§Ã£o multiusuÃ¡rio

EntregÃ¡veis: arquitetura fechada, autenticaÃ§Ã£o, sessÃµes, recuperaÃ§Ã£o, RBAC, organizaÃ§Ãµes, membros e ambientes.

## Fase 2 â€” DomÃ­nio e importaÃ§Ã£o

EntregÃ¡veis: modelo ampliado, migrations, seed, testes e primeiro fluxo CSV/JSON com validaÃ§Ã£o, prÃ©via, importaÃ§Ã£o e inventÃ¡rio.

## Fase 3 â€” AplicaÃ§Ã£o web operacional

EntregÃ¡veis: Ã¡reas pÃºblica, autenticada e administrativa; navegaÃ§Ã£o por organizaÃ§Ã£o e ambiente; estados de erro e permissÃ£o.

## Fase 4 â€” Watcher persistido

EntregÃ¡veis: fila, worker Python, execuÃ§Ã£o acompanhÃ¡vel, resultados versionados, confianÃ§a, incerteza, justificativa, reprocessamento e trilha de auditoria. O watcher apenas propÃµe alteraÃ§Ãµes.

## Fase 5 â€” Tratamentos, relatÃ³rios e auditoria

EntregÃ¡veis: decisÃµes humanas, responsÃ¡veis, prazos, evidÃªncias de conclusÃ£o, reanÃ¡lise, filtros e relatÃ³rios operacionais.

## Fase 6 â€” Portal cientÃ­fico

PrÃ©-condiÃ§Ã£o: fluxo operacional principal estÃ¡vel.

EntregÃ¡veis: atribuiÃ§Ã£o individual, cegamento, submissÃ£o final, bloqueio e compatibilidade com o protocolo existente. Nenhuma estatÃ­stica real serÃ¡ gerada antes das respostas humanas bloqueadas.

## Fase 7 â€” ProduÃ§Ã£o

EntregÃ¡veis: testes unitÃ¡rios, integraÃ§Ã£o e E2E, seguranÃ§a, uploads, segredos, observabilidade, backups, erros, CI/CD, deploy e validaÃ§Ã£o pÃºblica.

## Marco inicial de produto

Um operador autenticado cria um ambiente, importa CSV/JSON e visualiza ativos e vulnerabilidades.

## Notas relacionadas

[[00_Index]] Â· [[CURRENT_PHASE_STATUS]] Â· [[NEXT_ACTIONS]] Â· [[ARCHITECTURE]] Â· [[DEPLOYMENT_VERIFICATION]]

<!-- auth1b-roadmap-2026-07-20:start -->
## Fase 1 progress update â€” 2026-07-20

Delivered:

- Auth-1A schema and cryptographic foundation;
- Auth-1B operational login, logout, sessions, protected application
  area and explicit platform-administrator bootstrap.

Next:

- Auth-1C organization context, memberships, RBAC and tenant isolation.
<!-- auth1b-roadmap-2026-07-20:end -->

<!-- auth1c-roadmap-2026-07-20:start -->
## Fase 1 progress â€” Auth-1C

Delivered:

- Auth-1A identity and tenant schema;
- Auth-1B operational authentication;
- Auth-1C active organization context, role matrix and tenant-scoped
  read boundaries.

Remaining before closing Fase 1:

- organization and membership administration;
- invitations;
- project and environment mutations;
- last-active-ADMIN transaction;
- password recovery delivery;
- PostgreSQL integration and cross-tenant E2E tests.
<!-- auth1c-roadmap-2026-07-20:end -->

<!-- auth1d-roadmap-2026-07-20:start -->
## Fase 1 progress â€” Auth-1D

Delivered:

- Auth-1A identity and tenant schema;
- Auth-1B operational authentication;
- Auth-1C tenant authorization boundary;
- Auth-1D organization, membership, project and environment mutations;
- append-only security audit for administrative mutations;
- protection of the last active tenant administrator.

Remaining before closing Fase 1:

- invitation creation and acceptance flow;
- password recovery delivery;
- explicit session revocation operations;
- disposable PostgreSQL integration tests;
- real concurrent last-ADMIN tests;
- cross-tenant E2E tests.
<!-- auth1d-roadmap-2026-07-20:end -->

<!-- auth1e-roadmap-2026-07-20:start -->
## Fase 1 progress â€” Auth-1E

Delivered:

- Auth-1A identity and tenant schema;
- Auth-1B operational authentication;
- Auth-1C tenant authorization;
- Auth-1D tenant administration and invariants;
- Auth-1E password reset, invitations and session revocation.

Remaining before production closure of Fase 1:

- provider credentials and verified sender domain;
- disposable PostgreSQL integration tests;
- real concurrent last-ADMIN and token-consumption tests;
- cross-tenant E2E tests;
- deployment migration rehearsal;
- production deployment and acceptance.
<!-- auth1e-roadmap-2026-07-20:end -->

<!-- auth1f-online-roadmap-2026-07-21:start -->
## Phase 1 progress â€” Auth-1F Online

Online validation architecture:

- GitHub branch and Pull Request;
- GitHub-hosted Ubuntu runner;
- disposable PostgreSQL service container;
- Vercel Preview Deployment;
- Railway production preserved without test mutations.

Remaining after Auth-1F approval:

- browser-driven cross-tenant E2E;
- real Better Auth cookie tests;
- controlled email-provider sandbox;
- Edge Runtime compatibility review;
- production-like migration rehearsal;
- production deployment and acceptance.
<!-- auth1f-online-roadmap-2026-07-21:end -->

<!-- AUTH1G_ROADMAP_BEGIN -->
## Auth-1G — Browser E2E

- [x] Playwright e Chromium.
- [x] Provisionamento descartável.
- [x] Login real pela interface.
- [x] Cookies `HttpOnly`.
- [x] Dois tenants independentes.
- [x] Isolamento cross-tenant com `404`.
- [x] Segunda sessão e revogação das outras sessões.
- [x] Regressões Auth-1B até Auth-1F.
- [x] Build e pipeline Python.
- [ ] Aprovação dos gates online.
- [ ] Revisão e merge do Pull Request.
<!-- AUTH1G_ROADMAP_END -->
