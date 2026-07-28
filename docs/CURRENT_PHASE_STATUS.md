# CVSS current phase status

Atualizado em 2026-07-14.

## SÃ­ntese

A pesquisa cientÃ­fica estÃ¡ preservada e pausada no ponto correto: existem 30 cenÃ¡rios, pacotes cegos para trÃªs revisores, compromisso criptogrÃ¡fico da chave, gate de prÃ©-anÃ¡lise e motor estatÃ­stico da Fase 15. Ainda nÃ£o existem respostas humanas recebidas e bloqueadas. Portanto, nÃ£o hÃ¡ resultado de concordÃ¢ncia, validaÃ§Ã£o por especialistas ou conclusÃ£o estatÃ­stica a declarar.

O foco ativo passou a ser transformar os protÃ³tipos existentes em uma aplicaÃ§Ã£o operacional multiusuÃ¡rio. A Fase 0 estÃ¡ em fechamento documental e tÃ©cnico; ela somente poderÃ¡ ser considerada encerrada apÃ³s a execuÃ§Ã£o e o registro das validaÃ§Ãµes atuais.

## Matriz de realidade

| Ãrea | ClassificaÃ§Ã£o | Estado verificÃ¡vel |
|---|---|---|
| CÃ¡lculo CVSS oficial v3.1 | Real | ImplementaÃ§Ã£o Python e testes existentes no repositÃ³rio. |
| PriorizaÃ§Ã£o contextual separada | Real | Motor, regras, rastros e wrapper real-world existem; nÃ£o equivalem a CVSS oficial. |
| CenÃ¡rios cientÃ­ficos | Real | Conjunto de 30 cenÃ¡rios e artefatos de protocolo preservados. |
| Gate de prÃ©-anÃ¡lise e motor da Fase 15 | Real | Implementados com bloqueio para impedir anÃ¡lise antes da liberaÃ§Ã£o correta. |
| Dashboard estÃ¡tico e exportaÃ§Ãµes | Demo funcional | Ãšteis para demonstraÃ§Ã£o, mas nÃ£o constituem o produto multiusuÃ¡rio. |
| Next.js, Prisma e PostgreSQL | Parcial | HÃ¡ dashboard e modelos bÃ¡sicos `Run`, `Assessment`, `Comparison` e `AuditEvent`; o domÃ­nio operacional ainda nÃ£o estÃ¡ completo. |
| FastAPI | ProtÃ³tipo parcial | Existe servidor/protÃ³tipo Python; contrato operacional e integraÃ§Ã£o definitiva ainda precisam ser fechados. |
| Watcher | ProtÃ³tipo parcial | O motor propÃµe anÃ¡lises em fluxo demonstrativo; nÃ£o existe ainda ciclo operacional persistido, versionado e multiusuÃ¡rio. |
| AutenticaÃ§Ã£o, sessÃµes e recuperaÃ§Ã£o | Ausente | NÃ£o hÃ¡ fluxo operacional confirmado de login, logout, sessÃ£o, recuperaÃ§Ã£o ou bootstrap administrativo. |
| RBAC e isolamento organizacional | Ausente | PapÃ©is `ADMIN`, `OPERATOR` e `REVIEWER` e isolamento por organizaÃ§Ã£o ainda nÃ£o estÃ£o implementados. |
| ImportaÃ§Ã£o real CSV/JSON | Ausente | NÃ£o existe ainda o primeiro fluxo operacional de validar, prÃ©-visualizar e importar ativos e vulnerabilidades. |
| Tratamentos e aprovaÃ§Ã£o humana | Ausente | CorreÃ§Ã£o, mitigaÃ§Ã£o, aceite/rejeiÃ§Ã£o, responsÃ¡vel, prazo e evidÃªncia de conclusÃ£o ainda nÃ£o formam um fluxo persistido. |
| RelatÃ³rios operacionais e auditoria completa | Ausente | A estrutura atual nÃ£o cobre todas as consultas, decisÃµes e execuÃ§Ãµes do watcher. |
| Portal de revisores | Ausente no produto | O protocolo cientÃ­fico existe, mas o portal somente serÃ¡ construÃ­do depois do fluxo operacional principal. |
| ProduÃ§Ã£o pÃºblica atual | NÃ£o verificada | ConfiguraÃ§Ã£o e domÃ­nio precisam ser confirmados; documentaÃ§Ã£o antiga nÃ£o deve ser tratada como prova de deploy atual. |

## Prioridades imediatas

1. Finalizar e versionar esta auditoria documental.
2. Fechar formalmente a Fase 0 com testes e builds atuais.
3. Implementar autenticaÃ§Ã£o/RBAC e o modelo bÃ¡sico de usuÃ¡rios, organizaÃ§Ãµes e ambientes.

## Primeiro marco demonstrÃ¡vel

Um operador autenticado cria um ambiente, importa dados reais em CSV ou JSON e visualiza os ativos e vulnerabilidades encontrados.

## RestriÃ§Ãµes cientÃ­ficas

- NÃ£o fabricar respostas, resultados, concordÃ¢ncia ou validaÃ§Ã£o de especialistas.
- NÃ£o abrir nem alterar a chave de adjudicaÃ§Ã£o antes do token de liberaÃ§Ã£o.
- NÃ£o acessar ou modificar respostas, submissÃµes ou artefatos privados dos revisores.
- Manter o artigo e a estatÃ­stica pausados atÃ© a entrega e o bloqueio das respostas dos trÃªs revisores independentes.

## Notas relacionadas

[[00_Index]] Â· [[NEXT_ACTIONS]] Â· [[ROADMAP]] Â· [[ARCHITECTURE]] Â· [[ARTICLE_STATUS]]

<!-- verified-validation-2026-07-14:start -->
## Verified validation status â€” 2026-07-14

A auditoria documental passou com 102 notas, nenhum wikilink quebrado ou ambÃ­guo, nenhum link Markdown interno para notas `.md`, MOC completo e exatamente 12 prÃ³ximas atividades.

TambÃ©m passaram:

- 52 testes Pytest;
- verificaÃ§Ã£o de sintaxe de `app.js`;
- verificaÃ§Ã£o TypeScript sem emissÃ£o;
- build de produÃ§Ã£o do Next.js;
- validador do pipeline real;
- `git diff --check`.

A Fase 0 foi encerrada em 14 de julho de 2026 apÃ³s a retirada dos protÃ³tipos web Python isolados e a aprovaÃ§Ã£o da compilaÃ§Ã£o Python, dos 52 testes, da verificaÃ§Ã£o JavaScript, do TypeScript, do Prisma, do build Next.js, do pipeline real, da auditoria das 102 notas Obsidian e do `git diff --check`.

A linha de base encerrada preserva Next.js como interface web canÃ´nica, Prisma com PostgreSQL como persistÃªncia canÃ´nica e Python restrito Ã  engine CVSS, ao watcher e ao processamento interno explicitamente suportado.
<!-- verified-validation-2026-07-14:end -->

<!-- auth1b-operational-2026-07-20:start -->
## Auth-1B operational update â€” 2026-07-20

Auth-1B supersedes the earlier matrix entries that described
authentication as absent.

The locally validated implementation now includes:

- Better Auth with Prisma/PostgreSQL;
- Argon2id credential hashing;
- login and logout;
- persistent sessions;
- disabled public registration;
- protected `/app` area;
- authoritative server-side account validation;
- explicit PLATFORM_ADMIN bootstrap.

RBAC, active organization resolution and tenant isolation remain
pending for Auth-1C.
<!-- auth1b-operational-2026-07-20:end -->

<!-- auth1c-tenant-authorization-2026-07-20:start -->
## Auth-1C tenant authorization update â€” 2026-07-20

Auth-1C establishes the first operational organization boundary.

Locally validated capabilities:

- server-resolved organization slug;
- ACTIVE membership requirement;
- ACTIVE organization requirement;
- explicit ADMIN, OPERATOR, REVIEWER and VIEWER permission matrix;
- PLATFORM_ADMIN without implicit tenant access;
- protected organization routes;
- tenant-scoped project and environment reads;
- not-found behavior shared by unknown and unauthorized tenants;
- automated Auth-1C contract;
- production Next.js build.

This does not yet complete the whole RBAC milestone. Administrative
mutations, the last-active-ADMIN invariant, invitations, password
recovery delivery and cross-tenant integration/E2E tests remain pending.
<!-- auth1c-tenant-authorization-2026-07-20:end -->

<!-- auth1d-tenant-administration-2026-07-20:start -->
## Auth-1D tenant administration update â€” 2026-07-20

Auth-1D adds locally validated organization and tenant administration:

- organization creation restricted to ACTIVE PLATFORM_ADMIN;
- first ACTIVE ADMIN membership created transactionally;
- membership creation for existing ACTIVE users;
- membership role and status changes;
- last-active-ADMIN protection;
- Serializable transactions with bounded P2034 retry;
- tenant-scoped project creation;
- tenant-scoped environment creation with project ownership validation;
- same-origin mutation protection;
- SecurityAuditEvent for every successful mutation;
- administrative user interfaces;
- Auth-1B, Auth-1C and Auth-1D contract validation;
- production Next.js build.

The schema remains unchanged and no migration, bootstrap, push or deploy
was executed.

Fase 1 still requires invitation acceptance, recovery delivery,
disposable PostgreSQL integration, real concurrency tests and
cross-tenant E2E validation.
<!-- auth1d-tenant-administration-2026-07-20:end -->

<!-- auth1e-phase-2026-07-20:start -->
## Auth-1E account lifecycle update â€” 2026-07-20

Delivered locally:

- password reset request without account enumeration;
- SHA-256 storage of opaque token hashes;
- Argon2id password replacement;
- reset token expiration, single use and revocation;
- automatic revocation of all sessions after reset;
- invitation creation, delivery, revocation and acceptance;
- exact invitation email matching against the active session;
- controlled membership creation or reactivation;
- user session listing without token exposure;
- individual, other-session and all-session revocation;
- SecurityAuditEvent coverage;
- Resend email adapter with idempotency;
- Auth-1B through Auth-1E contracts;
- Next.js production build and Python pipeline.

The Prisma schema remains unchanged. No migration, database push,
bootstrap, push or deploy was executed.
<!-- auth1e-phase-2026-07-20:end -->

<!-- auth1f-online-phase-2026-07-21:start -->
## Auth-1F Online â€” 2026-07-21

Prepared:

- GitHub Actions orchestration;
- disposable PostgreSQL 16 service container;
- PostgreSQL client and health check;
- disposable Prisma schema application;
- real password reset integration;
- real invitation integration;
- real session revocation integration;
- concurrent token-consumption tests;
- cross-tenant authorization test;
- Auth-1B through Auth-1E regressions;
- Next.js production build;
- Python pipeline;
- Vercel Preview verification through Pull Request checks.

Railway production is not accessed or changed.

The local computer is used only as a Git client and file editor.
<!-- auth1f-online-phase-2026-07-21:end -->

<!-- AUTH1G_STATUS_BEGIN -->
## Auth-1G — Browser E2E

**Estado:** implementação enviada para validação online.

O gate executa o Auth-1F com banco vazio, provisiona dois tenants
descartáveis e valida login, cookies, isolamento e revogação de sessões.
<!-- AUTH1G_STATUS_END -->
