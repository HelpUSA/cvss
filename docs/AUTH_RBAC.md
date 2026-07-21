---
status: active
last_updated: 2026-07-20
owner: "Wagner / CVSS project"
tags:
  - cvss
  - authentication
  - authorization
  - rbac
  - multi-tenant
aliases:
  - "CVSS Authentication and RBAC"
---

# Authentication and RBAC

## Estado implementado

### Auth-1A

Schema aditivo para identidade, sessões, organizações, memberships,
projetos, ambientes, convites, recuperação e auditoria de segurança.

### Auth-1B

Better Auth com Prisma/PostgreSQL, credenciais locais, Argon2id, login,
logout, sessões persistidas, bloqueio de contas inativas e bootstrap
explícito de PLATFORM_ADMIN.

### Auth-1C

Contexto organizacional resolvido no servidor, membership e organização
ativas, papéis explícitos, consultas limitadas ao tenant e ausência de
bypass implícito para PLATFORM_ADMIN.

### Auth-1D

- criação de organização por PLATFORM_ADMIN;
- primeira membership ADMIN criada na mesma transação;
- criação de membership para usuário ativo existente;
- alteração de papel e status;
- proteção do último ADMIN ativo;
- criação tenant-scoped de projetos e ambientes;
- validação de que o projeto pertence ao tenant;
- auditoria de todas as mutações;
- proteção same-origin;
- transações Serializable com repetição de conflitos;
- interfaces administrativas.

## Matriz de papéis

### ADMIN

- leitura da organização;
- leitura e gestão de memberships;
- leitura e gestão de projetos;
- leitura e gestão de ambientes;
- execução de análises;
- revisão de decisões.

### OPERATOR

- leitura da organização;
- leitura e gestão de projetos;
- leitura e gestão de ambientes;
- execução de análises.

### VIEWER

- leitura da organização;
- leitura de projetos;
- leitura de ambientes.

### REVIEWER

Permanece reservado, sem acesso operacional durante Auth-1.

### PLATFORM_ADMIN

Capacidade global separada de MembershipRole.

Pode criar uma organização e torna-se o primeiro ADMIN dela, mas não
recebe acesso implícito a qualquer organização existente.

## Invariantes

- o último ADMIN ativo não pode ser rebaixado;
- o último ADMIN ativo não pode ser suspenso;
- o último ADMIN ativo não pode ser revogado;
- mutations do invariante usam transação Serializable;
- conflitos de concorrência são repetidos de forma limitada;
- organizationId e role fornecidos pelo cliente não são confiáveis;
- projectId fornecido pelo cliente precisa ser validado dentro do tenant;
- toda mutação gera SecurityAuditEvent.

## Limites restantes

- convites e aceitação por token;
- entrega de recuperação de acesso;
- testes com PostgreSQL descartável;
- testes concorrentes reais;
- testes E2E entre usuários de tenants diferentes;
- ciclo de vida de arquivamento de projetos, ambientes e organizações.

## Notas relacionadas

[[ARCHITECTURE]] · [[DATABASE]] · [[WEB_APPLICATION]] ·
[[auth/AUTH1B_OPERATIONAL_AUTH]] ·
[[auth/AUTH1C_TENANT_AUTHORIZATION]] ·
[[auth/AUTH1D_TENANT_ADMINISTRATION]]

<!-- auth1e-rbac-2026-07-20:start -->
## Auth-1E account lifecycle

ADMIN may create and revoke tenant invitations through the existing
membership:manage permission.

Invitation acceptance does not trust a userId or email supplied by the
browser. The server obtains both from the active session and requires the
session email to match the invitation.

Every user may manage only sessions belonging to their own authoritative
user ID.

Password reset is public but does not reveal whether an eligible account
exists. Successful reset revokes all user sessions.
<!-- auth1e-rbac-2026-07-20:end -->
