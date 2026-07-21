# CVSS current phase status

Atualizado em 2026-07-14.

## Síntese

A pesquisa científica está preservada e pausada no ponto correto: existem 30 cenários, pacotes cegos para três revisores, compromisso criptográfico da chave, gate de pré-análise e motor estatístico da Fase 15. Ainda não existem respostas humanas recebidas e bloqueadas. Portanto, não há resultado de concordância, validação por especialistas ou conclusão estatística a declarar.

O foco ativo passou a ser transformar os protótipos existentes em uma aplicação operacional multiusuário. A Fase 0 está em fechamento documental e técnico; ela somente poderá ser considerada encerrada após a execução e o registro das validações atuais.

## Matriz de realidade

| Área | Classificação | Estado verificável |
|---|---|---|
| Cálculo CVSS oficial v3.1 | Real | Implementação Python e testes existentes no repositório. |
| Priorização contextual separada | Real | Motor, regras, rastros e wrapper real-world existem; não equivalem a CVSS oficial. |
| Cenários científicos | Real | Conjunto de 30 cenários e artefatos de protocolo preservados. |
| Gate de pré-análise e motor da Fase 15 | Real | Implementados com bloqueio para impedir análise antes da liberação correta. |
| Dashboard estático e exportações | Demo funcional | Úteis para demonstração, mas não constituem o produto multiusuário. |
| Next.js, Prisma e PostgreSQL | Parcial | Há dashboard e modelos básicos `Run`, `Assessment`, `Comparison` e `AuditEvent`; o domínio operacional ainda não está completo. |
| FastAPI | Protótipo parcial | Existe servidor/protótipo Python; contrato operacional e integração definitiva ainda precisam ser fechados. |
| Watcher | Protótipo parcial | O motor propõe análises em fluxo demonstrativo; não existe ainda ciclo operacional persistido, versionado e multiusuário. |
| Autenticação, sessões e recuperação | Ausente | Não há fluxo operacional confirmado de login, logout, sessão, recuperação ou bootstrap administrativo. |
| RBAC e isolamento organizacional | Ausente | Papéis `ADMIN`, `OPERATOR` e `REVIEWER` e isolamento por organização ainda não estão implementados. |
| Importação real CSV/JSON | Ausente | Não existe ainda o primeiro fluxo operacional de validar, pré-visualizar e importar ativos e vulnerabilidades. |
| Tratamentos e aprovação humana | Ausente | Correção, mitigação, aceite/rejeição, responsável, prazo e evidência de conclusão ainda não formam um fluxo persistido. |
| Relatórios operacionais e auditoria completa | Ausente | A estrutura atual não cobre todas as consultas, decisões e execuções do watcher. |
| Portal de revisores | Ausente no produto | O protocolo científico existe, mas o portal somente será construído depois do fluxo operacional principal. |
| Produção pública atual | Não verificada | Configuração e domínio precisam ser confirmados; documentação antiga não deve ser tratada como prova de deploy atual. |

## Prioridades imediatas

1. Finalizar e versionar esta auditoria documental.
2. Fechar formalmente a Fase 0 com testes e builds atuais.
3. Implementar autenticação/RBAC e o modelo básico de usuários, organizações e ambientes.

## Primeiro marco demonstrável

Um operador autenticado cria um ambiente, importa dados reais em CSV ou JSON e visualiza os ativos e vulnerabilidades encontrados.

## Restrições científicas

- Não fabricar respostas, resultados, concordância ou validação de especialistas.
- Não abrir nem alterar a chave de adjudicação antes do token de liberação.
- Não acessar ou modificar respostas, submissões ou artefatos privados dos revisores.
- Manter o artigo e a estatística pausados até a entrega e o bloqueio das respostas dos três revisores independentes.

## Notas relacionadas

[[00_Index]] · [[NEXT_ACTIONS]] · [[ROADMAP]] · [[ARCHITECTURE]] · [[ARTICLE_STATUS]]

<!-- verified-validation-2026-07-14:start -->
## Verified validation status — 2026-07-14

A auditoria documental passou com 102 notas, nenhum wikilink quebrado ou ambíguo, nenhum link Markdown interno para notas `.md`, MOC completo e exatamente 12 próximas atividades.

Também passaram:

- 52 testes Pytest;
- verificação de sintaxe de `app.js`;
- verificação TypeScript sem emissão;
- build de produção do Next.js;
- validador do pipeline real;
- `git diff --check`.

A Fase 0 foi encerrada em 14 de julho de 2026 após a retirada dos protótipos web Python isolados e a aprovação da compilação Python, dos 52 testes, da verificação JavaScript, do TypeScript, do Prisma, do build Next.js, do pipeline real, da auditoria das 102 notas Obsidian e do `git diff --check`.

A linha de base encerrada preserva Next.js como interface web canônica, Prisma com PostgreSQL como persistência canônica e Python restrito à engine CVSS, ao watcher e ao processamento interno explicitamente suportado.
<!-- verified-validation-2026-07-14:end -->

<!-- auth1b-operational-2026-07-20:start -->
## Auth-1B operational update — 2026-07-20

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
## Auth-1C tenant authorization update — 2026-07-20

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
## Auth-1D tenant administration update — 2026-07-20

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
## Auth-1E account lifecycle update — 2026-07-20

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
