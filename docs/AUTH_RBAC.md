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

## Estado atual

A fundação de autenticação e autorização organizacional está
operacional em nível local.

Auth-1A entregou o schema aditivo de identidade e tenant.

Auth-1B conectou Better Auth ao Prisma/PostgreSQL e implementou login,
logout, sessões persistidas, bloqueio de contas inativas e bootstrap
explícito do primeiro administrador da plataforma.

Auth-1C implementa:

- seleção de organização autorizada;
- resolução de membership no servidor;
- exigência de usuário, organização e membership ativos;
- matriz explícita de permissões;
- rotas organizacionais protegidas;
- consultas de projetos e ambientes limitadas ao tenant;
- endpoint de contexto organizacional;
- negação sem revelar se outro tenant existe;
- ausência de bypass implícito para PLATFORM_ADMIN.

## Papéis e permissões

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

Permanece reservado sem acesso operacional durante Auth-1.

### PLATFORM_ADMIN

É uma capacidade global separada de MembershipRole.

Não recebe acesso implícito aos dados de nenhuma organização. Para
entrar em um tenant, precisa possuir uma membership operacional ativa.

## Regras de isolamento

- organizationId e role recebidos do cliente nunca são confiáveis;
- o cliente fornece somente o slug da rota;
- o servidor resolve slug, usuário e membership;
- toda consulta organizacional usa o ID retornado por essa resolução;
- memberships suspensas ou revogadas são negadas;
- organizações suspensas ou arquivadas são negadas;
- acesso inexistente e não autorizado usa a mesma resposta externa.

## Limites atuais

Ainda faltam:

- mutações administrativas de memberships;
- criação operacional de projetos e ambientes;
- transação serializada do último ADMIN;
- convites e aceitação;
- recuperação de acesso com entrega;
- importação tenant-scoped;
- testes de integração com PostgreSQL descartável;
- testes E2E com usuários de tenants diferentes.

## Notas relacionadas

[[ARCHITECTURE]] · [[DATABASE]] · [[WEB_APPLICATION]] ·
[[auth/AUTH1B_OPERATIONAL_AUTH]] ·
[[auth/AUTH1C_TENANT_AUTHORIZATION]]
