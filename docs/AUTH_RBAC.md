---
status: active
last_updated: 2026-07-14
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

Autenticação, sessões, recuperação, rotas protegidas, bootstrap administrativo, RBAC e isolamento organizacional não estão confirmados como implementados no produto.

## Escopo da primeira implementação

- login e logout;
- sessão segura;
- recuperação de acesso;
- bootstrap do primeiro administrador;
- proteção de rotas e ações;
- associação entre usuário, organização e papel;
- isolamento de consultas e comandos por organização;
- auditoria de autenticação e decisões sensíveis.

## Papéis iniciais

- `ADMIN`: administra organização, membros, ambientes e políticas.
- `OPERATOR`: importa dados, executa análises e conduz tratamentos.
- `REVIEWER`: revisa propostas e registra decisões permitidas.

Permissões devem ser explícitas e testadas; o nome do papel não substitui a autorização por ação e recurso.

## Dependências

[[DATABASE]] · [[WEB_APPLICATION]] · [[ARCHITECTURE]] · [[07_Testing_and_Validation]]
