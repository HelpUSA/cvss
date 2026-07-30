# Current handoff

## Estado entregue

A Fase 0 está encerrada.

A Fase 1 possui os seguintes marcos versionados:

- Auth-1A: schema aditivo de identidade e tenant;
- Auth-1B: autenticação e sessões operacionais;
- Auth-1C: contexto organizacional, RBAC e leitura tenant-scoped;
- Auth-1D: administração de organizações, memberships, projetos e
  ambientes com auditoria e invariantes;
- Auth-1E: recuperação de senha, convites e revogação de sessões;
- Auth-1F: integração online com PostgreSQL descartável e gates reais;
- Auth-1G: Browser E2E com login pela interface, cookies `HttpOnly`,
  isolamento cross-tenant e revogação de sessões.

O Auth-1G foi integrado à branch `real-world-cvss` pelo Pull Request `#2`.
O merge commit atual é
`0508fee56be4c2cf0ca7803f2d8251fe6f2162e7`.
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

## Próxima atividade

Concluir as validações operacionais restantes da Fase 1:

- executar recuperação de senha e convites em sandbox controlado do
  provedor de e-mail;
- revisar compatibilidade com Edge Runtime;
- ensaiar migrations em ambiente semelhante à produção;
- preparar o procedimento de deployment e aceitação;
- manter produção fora do escopo até autorização expressa.

Depois do fechamento controlado da Fase 1, iniciar a Fase 2 com importação
CSV/JSON tenant-scoped.
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
## Auth-1G — Browser E2E — encerramento

O Auth-1G está integrado em `real-world-cvss`.

Referências:

- Pull Request: `#2`;
- commit Auth-1G: `f21f80cbd31a5446153e1657c6ef67129327dd71`;
- merge commit: `0508fee56be4c2cf0ca7803f2d8251fe6f2162e7`;
- Real Pipeline Gate: execução `30321808705`, concluída com sucesso;
- Auth-1G Browser E2E: execução `30321871354`, concluída com sucesso.

O schema Prisma permaneceu inalterado. Nenhum merge adicional do Auth-1G,
deployment manual, deployment de produção ou rollback é necessário.

O próximo responsável deve trabalhar nas validações restantes de e-mail,
Edge Runtime e migrations. Produção exige checkpoint e autorização
separados.
<!-- AUTH1G_HANDOFF_END -->
