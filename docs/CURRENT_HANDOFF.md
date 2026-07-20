# Current handoff

## Estado entregue

A Fase 0 está encerrada e a Fase 1 está em execução.

Auth-1A entregou o schema aditivo de identidade e tenant.

Auth-1B entregou autenticação operacional com Better Auth, Prisma,
Argon2id, login, logout, sessão persistida, área protegida e bootstrap
explícito do primeiro administrador da plataforma.

Auth-1C entrega o primeiro limite organizacional operacional:

- organização ativa resolvida por slug no servidor;
- membership ativa obrigatória;
- papéis e permissões explícitos;
- PLATFORM_ADMIN sem acesso implícito aos tenants;
- consultas de projetos e ambientes limitadas à organização;
- páginas e endpoint protegidos;
- negação uniforme para tenants inexistentes ou não autorizados.

## Próxima atividade

Implementar Auth-1D e o fechamento da Fase 1:

- criação e gestão de organizações;
- criação, convite, suspensão e revogação de memberships;
- criação de projetos e ambientes;
- invariantes transacionais do último ADMIN;
- auditoria de todas as mutações;
- testes em PostgreSQL descartável;
- testes concorrentes;
- testes E2E entre tenants;
- recuperação de acesso.

Depois, iniciar a Fase 2 com o domínio de importação CSV/JSON.

## Restrições

- Não confiar em organizationId ou role enviados pelo cliente.
- Não conceder bypass de tenant ao PLATFORM_ADMIN.
- Não usar consultas globais em fluxos autenticados.
- Não aplicar migrations de produção sem validação específica.
- Não executar bootstrap automaticamente.
- Não fabricar respostas ou resultados científicos.
- Não acessar artefatos privados dos revisores.
- O watcher apenas propõe mudanças.

## Notas relacionadas

[[CURRENT_PHASE_STATUS]] · [[ROADMAP]] · [[ARCHITECTURE]] ·
[[AUTH_RBAC]] · [[auth/AUTH1C_TENANT_AUTHORIZATION]]
