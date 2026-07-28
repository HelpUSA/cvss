# Current handoff

## Estado entregue

A Fase 0 estÃ¡ encerrada.

A Fase 1 possui agora quatro marcos locais:

- Auth-1A: schema aditivo de identidade e tenant;
- Auth-1B: autenticaÃ§Ã£o e sessÃµes operacionais;
- Auth-1C: contexto organizacional e leitura tenant-scoped;
- Auth-1D: administraÃ§Ã£o de organizaÃ§Ãµes, memberships, projetos e
  ambientes com auditoria e invariantes.

## Capacidades Auth-1D

- PLATFORM_ADMIN cria organizaÃ§Ã£o;
- a criaÃ§Ã£o inclui a primeira membership ADMIN;
- ADMIN adiciona usuÃ¡rios ativos existentes ao tenant;
- ADMIN altera papel e status de memberships;
- o Ãºltimo ADMIN ativo Ã© protegido em transaÃ§Ã£o Serializable;
- ADMIN e OPERATOR criam projetos e ambientes;
- ambientes validam o projeto dentro da organizaÃ§Ã£o;
- todas as mutaÃ§Ãµes registram SecurityAuditEvent;
- as rotas exigem sessÃ£o, permissÃ£o, same-origin e JSON limitado.

## PrÃ³xima atividade

Fechar a Fase 1 com Auth-1E:

- convites;
- aceitaÃ§Ã£o de convites;
- recuperaÃ§Ã£o de acesso;
- revogaÃ§Ã£o operacional de sessÃµes;
- PostgreSQL descartÃ¡vel;
- testes concorrentes reais;
- testes E2E cross-tenant;
- documentaÃ§Ã£o final da Fase 1.

Depois, iniciar a Fase 2 com importaÃ§Ã£o CSV/JSON tenant-scoped.

## RestriÃ§Ãµes

- nÃ£o confiar em organizationId, projectId ou role sem resoluÃ§Ã£o;
- nÃ£o conceder bypass de tenant ao PLATFORM_ADMIN;
- nÃ£o remover o Ãºltimo ADMIN ativo;
- nÃ£o executar migrations de produÃ§Ã£o sem validaÃ§Ã£o especÃ­fica;
- nÃ£o executar bootstrap automaticamente;
- nÃ£o fabricar resultados cientÃ­ficos;
- nÃ£o acessar artefatos privados dos revisores;
- o watcher apenas propÃµe mudanÃ§as.

## Notas relacionadas

[[CURRENT_PHASE_STATUS]] Â· [[ROADMAP]] Â· [[ARCHITECTURE]] Â·
[[AUTH_RBAC]] Â· [[auth/AUTH1D_TENANT_ADMINISTRATION]]

<!-- auth1e-handoff-2026-07-20:start -->
## Auth-1E handoff

Auth-1E adds password reset, tenant invitations and self-service session
revocation without changing the Prisma schema.

Before production activation, configure:

- RESEND_API_KEY;
- AUTH_EMAIL_FROM;
- AUTH_PUBLIC_BASE_URL.

The next validation milestone is Auth-1F:

- start Docker Desktop or provision another disposable PostgreSQL;
- apply the existing schema only to the disposable database;
- execute real token, invitation and concurrency integration tests;
- execute cross-tenant E2E tests;
- validate email delivery in a controlled provider account;
- prepare production migration and deployment procedures.
<!-- auth1e-handoff-2026-07-20:end -->

<!-- auth1f-online-handoff-2026-07-21:start -->
## Auth-1F Online handoff

Auth-1F is validated through Pull Request checks targeting
`real-world-cvss`.

Responsibilities:

- GitHub stores the branch, Pull Request and workflow result;
- GitHub Actions provides a disposable PostgreSQL service container;
- Vercel produces the Preview Deployment;
- Railway production remains unchanged and outside the test boundary;
- GitHub Actions runs integration, regressions, build and Python tests.

The PostgreSQL service is destroyed with the hosted runner. There is no
persistent Auth-1F database to remove manually.

The next milestone after approval is browser-driven Auth-1G E2E.
<!-- auth1f-online-handoff-2026-07-21:end -->

<!-- AUTH1G_HANDOFF_BEGIN -->
## Auth-1G — Browser E2E

A branch `auth1g-browser-e2e` implementa Playwright com Chromium,
provisionamento descartável, login real, cookies `HttpOnly`, isolamento
cross-tenant com `404` e revogação das outras sessões.

O Pull Request deve ser revisado depois da aprovação dos gates. Nenhum
merge é executado automaticamente.
<!-- AUTH1G_HANDOFF_END -->
