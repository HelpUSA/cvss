# Current handoff

## Estado entregue

A Fase 0 está encerrada.

A Fase 1 possui agora quatro marcos locais:

- Auth-1A: schema aditivo de identidade e tenant;
- Auth-1B: autenticação e sessões operacionais;
- Auth-1C: contexto organizacional e leitura tenant-scoped;
- Auth-1D: administração de organizações, memberships, projetos e
  ambientes com auditoria e invariantes.

## Capacidades Auth-1D

- PLATFORM_ADMIN cria organização;
- a criação inclui a primeira membership ADMIN;
- ADMIN adiciona usuários ativos existentes ao tenant;
- ADMIN altera papel e status de memberships;
- o último ADMIN ativo é protegido em transação Serializable;
- ADMIN e OPERATOR criam projetos e ambientes;
- ambientes validam o projeto dentro da organização;
- todas as mutações registram SecurityAuditEvent;
- as rotas exigem sessão, permissão, same-origin e JSON limitado.

## Próxima atividade

Fechar a Fase 1 com Auth-1E:

- convites;
- aceitação de convites;
- recuperação de acesso;
- revogação operacional de sessões;
- PostgreSQL descartável;
- testes concorrentes reais;
- testes E2E cross-tenant;
- documentação final da Fase 1.

Depois, iniciar a Fase 2 com importação CSV/JSON tenant-scoped.

## Restrições

- não confiar em organizationId, projectId ou role sem resolução;
- não conceder bypass de tenant ao PLATFORM_ADMIN;
- não remover o último ADMIN ativo;
- não executar migrations de produção sem validação específica;
- não executar bootstrap automaticamente;
- não fabricar resultados científicos;
- não acessar artefatos privados dos revisores;
- o watcher apenas propõe mudanças.

## Notas relacionadas

[[CURRENT_PHASE_STATUS]] · [[ROADMAP]] · [[ARCHITECTURE]] ·
[[AUTH_RBAC]] · [[auth/AUTH1D_TENANT_ADMINISTRATION]]
