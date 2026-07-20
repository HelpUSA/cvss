# Current handoff

## Estado entregue

A Fase 0 está encerrada e a Fase 1 está ativa.

Auth-1A entregou o schema aditivo de identidade e tenant.

Auth-1B entrega autenticação operacional com Better Auth, Prisma,
Argon2id, login, logout, sessão persistida, rota de autenticação,
página protegida, bloqueio de usuários inativos e bootstrap
explícito do primeiro administrador da plataforma.

## Próxima atividade

Implementar Auth-1C:

- resolução segura da organização ativa;
- memberships ativas;
- RBAC por ação e recurso;
- navegação por organização, projeto e ambiente;
- proteção contra IDOR entre tenants;
- invariantes do último ADMIN;
- testes de isolamento organizacional;
- remoção de consultas globais do domínio operacional.

## Restrições

- Não declarar a autenticação como RBAC completo.
- Não conceder acesso de tenant implicitamente ao `PLATFORM_ADMIN`.
- Não confiar em IDs de organização ou papéis enviados pelo cliente.
- Não aplicar migrations de produção sem validação específica.
- Não executar bootstrap automaticamente durante build ou deploy.
- Não fabricar respostas ou resultados dos revisores.
- Não acessar artefatos privados de resposta ou adjudicação.
- O watcher apenas propõe mudanças.

## Estado científico

A pesquisa permanece pausada corretamente. Não existem três respostas
humanas independentes recebidas e bloqueadas.

## Notas relacionadas

[[00_Index]] · [[CURRENT_PHASE_STATUS]] · [[NEXT_ACTIONS]] ·
[[ROADMAP]] · [[ARCHITECTURE]] · [[AUTH_RBAC]] ·
[[auth/AUTH1B_OPERATIONAL_AUTH]]
