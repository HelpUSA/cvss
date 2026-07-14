---
status: active
last_updated: 2026-07-14
owner: "Wagner / CVSS project"
tags:
  - cvss
  - web
  - nextjs
aliases:
  - "CVSS Web Application"
---

# Web application

## Estado atual

A camada web contém uma experiência de dashboard/página única e artefatos de demonstração. Ela não deve ser descrita como aplicação multiusuário pronta.

## Estrutura-alvo

- Área pública: apresentação, documentação e entrada.
- Área autenticada: ambientes, importações, inventário, achados, análises, tratamentos e relatórios.
- Área administrativa: usuários, organizações, membros, papéis, políticas, auditoria e operação do sistema.

## Primeiro fluxo real

1. Operador entra no sistema.
2. Cria ou seleciona um ambiente.
3. Envia CSV ou JSON.
4. Visualiza validação e prévia.
5. Confirma a importação.
6. Consulta ativos e vulnerabilidades encontrados.

SARIF, CycloneDX, SPDX e conectores ficam para uma fase posterior.

## Dependências

[[AUTH_RBAC]] · [[DATABASE]] · [[WATCHER]] · [[ARCHITECTURE]] · [[08_Dashboard_and_Exports]]

## Superfície web canônica

A única interface web suportada é a aplicação Next.js em `web/`. Prisma com PostgreSQL define a camada de persistência. Dashboards ou servidores web Python paralelos não fazem parte da arquitetura suportada e exigiriam uma decisão arquitetural explícita, contratos, testes e integração operacional documentados.
