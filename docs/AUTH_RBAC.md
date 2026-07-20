---
status: active
last_updated: 2026-07-20
owner: "Wagner / CVSS project"
tags:
  - cvss
  - authentication
  - rbac
aliases:
  - "CVSS Authentication and RBAC"
---

# Authentication and RBAC

## Estado atual

A fundação de autenticação está parcialmente operacional.

Auth-1A entregou o schema aditivo de usuários, sessões, contas,
organizações, memberships, projetos, ambientes, convites,
recuperação e auditoria de segurança.

Auth-1B conecta Better Auth ao Prisma/PostgreSQL e implementa login,
logout, sessão persistida, rota de autenticação, tela de acesso,
área protegida, bloqueio de contas inativas e bootstrap explícito
do primeiro `PLATFORM_ADMIN`.

## Controles implementados

- login por e-mail e senha;
- logout;
- sessão persistida no PostgreSQL;
- Argon2id personalizado;
- registro público desabilitado;
- página pública separada da área autenticada;
- validação autoritativa da sessão no servidor;
- middleware usado apenas para redirecionamento otimista;
- bloqueio de sessão para usuários suspensos ou desabilitados;
- bootstrap administrativo idempotente sem exposição de segredo.

## Limites atuais

A autenticação operacional não conclui o RBAC.

Ainda faltam:

- seleção de organização;
- resolução de membership ativa;
- autorização por ação e recurso;
- isolamento organizacional das consultas;
- proteção contra IDOR entre tenants;
- administração de membros, projetos e ambientes;
- invariantes transacionais do último ADMIN;
- recuperação de acesso com entrega de token.

## Papéis previstos

- `ADMIN`
- `OPERATOR`
- `REVIEWER`
- `VIEWER`
- `PLATFORM_ADMIN`

`PLATFORM_ADMIN` é uma capacidade global separada das memberships e
não concede acesso implícito ao conteúdo das organizações.

## Dependências

[[DATABASE]] · [[WEB_APPLICATION]] · [[ARCHITECTURE]] ·
[[07_Testing_and_Validation]] · [[auth/AUTH1B_OPERATIONAL_AUTH]]
