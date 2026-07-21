# CVSS operational architecture

## Princípios

1. O cálculo CVSS oficial permanece separado da priorização contextual.
2. Toda proposta do watcher é explicável, persistida, versionada e sujeita a decisão humana.
3. A organização é a fronteira de isolamento de dados.
4. O PostgreSQL é a fonte operacional de verdade.
5. Protótipos atuais não devem ser descritos como produto completo.

## Componentes-alvo

### Next.js

Responsável pela interface pública, autenticada e administrativa, rotas de aplicação, validação de entrada, autorização no limite web e apresentação de inventário, análises, tratamentos, relatórios e auditoria.

### PostgreSQL e Prisma

Responsáveis por identidade, organizações, ambientes, domínio de vulnerabilidades, importações, execuções, propostas, decisões, tratamentos e auditoria. O schema atual é apenas uma base parcial.

### FastAPI

Responsável pelo contrato de cálculo e análise Python. Deve expor operações tipadas, idempotentes e observáveis, sem assumir o controle da autorização organizacional.

### Fila de análise

Responsável por desacoplar solicitações web do processamento Python, controlar tentativas, estados, idempotência, cancelamento e reprocessamento.

### Worker Python / watcher

Responsável por consumir achados, ativos, contexto e evidências; calcular CVSS original e camada contextual; produzir prioridade, justificativa, confiança, incerteza e tratamento proposto; persistir o resultado por meio do contrato operacional.

## Fluxo proposto

1. O usuário autenticado atua dentro de uma organização e ambiente autorizados.
2. A aplicação valida e persiste a importação.
3. Um job de análise é criado no banco e enviado à fila.
4. O worker carrega somente os dados autorizados do job.
5. O motor Python calcula e devolve um resultado versionado.
6. A aplicação apresenta a proposta.
7. Um humano aprova, rejeita ou ajusta com justificativa.
8. Toda mudança gera evento de auditoria.
9. Nova evidência pode iniciar reprocessamento sem sobrescrever o histórico.

## Estado atual

- Next.js: parcial, com dashboard/página única.
- Prisma/PostgreSQL: parcial, com modelos básicos.
- FastAPI: protótipo.
- Fila durável: ausente.
- Worker operacional persistido: ausente.
- Autenticação e RBAC: ausentes.
- Fluxo ponta a ponta multiusuário: ausente.

## Decisões pendentes da Fase 0/1

- Contrato entre Next.js e FastAPI.
- Tecnologia da fila.
- Estratégia de idempotência e versionamento.
- Limites transacionais entre importação, job e resultado.
- Política de retenção e auditoria.
- Estratégia de deploy dos componentes.

## Notas relacionadas

[[00_Index]] · [[WEB_APPLICATION]] · [[AUTH_RBAC]] · [[DATABASE]] · [[WATCHER]] · [[decisions/ADR-001-official-vs-contextual-separation]]

## Decisão arquitetural da Fase 0

A interface web canônica é a aplicação Next.js em `web/`. A persistência canônica usa Prisma com PostgreSQL. Python permanece restrito à engine CVSS, ao watcher e ao processamento interno explicitamente suportado. Não existe dashboard Python nem servidor FastAPI público paralelo. Os protótipos web Python anteriores foram retirados da árvore executável após auditoria confirmar ausência de dependências operacionais. O histórico permanece recuperável pelo Git a partir do commit `59c23c6`.

<!-- auth1b-architecture-2026-07-20:start -->
## Authentication architecture update — 2026-07-20

Better Auth is the operational authentication boundary for the Next.js
application. It uses the Prisma PostgreSQL adapter and the Auth-1A core
identity tables.

Middleware performs only an optimistic cookie-presence redirect.
Protected server components validate the session and authoritative user
status again.

Tenant authorization remains an application responsibility and is not
implicitly granted by authentication or by the PLATFORM_ADMIN role.
<!-- auth1b-architecture-2026-07-20:end -->

<!-- auth1c-architecture-2026-07-20:start -->
## Tenant authorization architecture — Auth-1C

Authenticated tenant routes use a server-resolved organization context.

The route slug is normalized and matched together with:

- the authenticated user ID;
- ACTIVE membership status;
- ACTIVE organization status;
- an explicit permission required by the route.

The authoritative organization ID produced by that resolution is the
only organization identifier accepted by downstream tenant queries.

PLATFORM_ADMIN is not an authorization bypass. It remains independent
from tenant memberships.

Unknown organizations and organizations outside the user boundary use
the same external not-found behavior to reduce tenant enumeration.
<!-- auth1c-architecture-2026-07-20:end -->

<!-- auth1d-architecture-2026-07-20:start -->
## Tenant mutation architecture — Auth-1D

Tenant mutations use three independent boundaries:

1. Better Auth validates the server-side session.
2. The organization context validates ACTIVE membership, ACTIVE
   organization and the route permission.
3. The mutation transaction revalidates resource ownership and
   invariants before writing.

Administrative transactions use Serializable isolation with bounded
retry for transaction conflicts.

The last-active-ADMIN invariant is evaluated inside the same transaction
that updates the membership.

Client-provided project IDs are accepted only after the project is
confirmed as ACTIVE and owned by the resolved organization.

Every successful administrative mutation appends a separate
SecurityAuditEvent without secrets.
<!-- auth1d-architecture-2026-07-20:end -->

<!-- auth1e-architecture-2026-07-20:start -->
## Account lifecycle architecture — Auth-1E

Password reset and invitation links use 256-bit opaque tokens.

Only SHA-256 token hashes are stored in PostgreSQL. Raw tokens exist only
while constructing the outbound link and are never included in logs,
responses or audit metadata.

Password reset confirmation revalidates the token inside a Serializable
transaction, updates the credential password with Argon2id, consumes the
token and deletes all sessions.

Invitation acceptance requires the authenticated user's normalized email
to match the invitation email exactly. The transaction creates or
reactivates the tenant membership and consumes the invitation.

Transactional email is delivered through the Resend HTTPS API using an
idempotency key derived from the database record identifier.
<!-- auth1e-architecture-2026-07-20:end -->
