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
