---
status: active
last_updated: 2026-07-14
owner: "Wagner / CVSS project"
tags:
  - cvss
  - dashboard
  - exports
aliases:
  - "CVSS Dashboard"
  - "CVSS Exports"
related_files:
  - docs/CLOUD_DASHBOARD_PLAN.md
  - docs/INTERACTIVE_SITE_PLAN.md
  - docs/INTERACTIVE_EXPORT_FORMAT.md
  - docs/SITE_REPORT_EXPORT.md
---

# Dashboard and Exports

## Estado atual

O dashboard estático, a página única e as exportações existentes são demonstrações úteis. Eles não oferecem autenticação, isolamento organizacional, workflow de tratamento ou operação multiusuário completa.

## Direção

A experiência será incorporada à [[WEB_APPLICATION]] com áreas pública, autenticada e administrativa. Exportações devem respeitar autorização, organização, ambiente, filtros e trilha de auditoria.

## Primeiro marco

Após login, o operador cria um ambiente, importa CSV/JSON e visualiza ativos e vulnerabilidades.

## Evolução posterior

Relatórios por ambiente, ativo, vulnerabilidade, prioridade, tratamento, período e execução do watcher.

## Notas relacionadas

[[WEB_APPLICATION]] · [[AUTH_RBAC]] · [[DATABASE]] · [[WATCHER]] · [[DEPLOYMENT_VERIFICATION]]
