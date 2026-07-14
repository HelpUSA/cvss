# Next actions

Estas são as 12 atividades oficiais, em ordem. Uma atividade posterior não deve antecipar alegações de conclusão das anteriores.

1. **Concluir a auditoria completa da documentação.** Registrar arquivos lidos e alterados, contradições corrigidas, classificação de funcionalidades como real, parcial, demo ou ausente, pausa do artigo aguardando três revisores, validadores executados, commit, push e estado Git final limpo.
2. **Fechar formalmente a Fase 0.** Executar `pytest`, build Next.js, verificações JavaScript/TypeScript e registrar o estado real de FastAPI, Prisma/PostgreSQL e watcher, incluindo matriz funcional/parcial/ausente e riscos técnicos.
3. **Definir a arquitetura operacional.** Fechar responsabilidades e comunicação entre Next.js, API/FastAPI, PostgreSQL com Prisma, fila de análise e worker Python.
4. **Implementar autenticação e RBAC no backend.** Incluir login, logout, sessões, recuperação, rotas protegidas, bootstrap do administrador, papéis `ADMIN`, `OPERATOR` e `REVIEWER` e isolamento por organização.
5. **Expandir o modelo de dados.** Incluir usuários, organizações, membros, papéis, ambientes, ativos, componentes, vulnerabilidades, achados, evidências, importações, execuções do watcher, decisões, tratamentos, ações e auditoria, com migrations, seed e testes.
6. **Substituir a página única/demo por uma aplicação pública, autenticada e administrativa.**
7. **Entregar o primeiro fluxo real.** O operador entra, cria um ambiente, envia CSV/JSON, valida, pré-visualiza, importa ativos e vulnerabilidades e consulta o inventário. SARIF, CycloneDX, SPDX e conectores ficam para uma etapa posterior.
8. **Integrar o watcher operacional.** Achado, ativo, contexto e evidência produzem CVSS original, prioridade contextual, justificativa, confiança, incerteza e tratamento proposto. A execução deve iniciar, ser acompanhada, persistida, versionada e reprocessável. O watcher propõe; nunca altera o ambiente automaticamente.
9. **Implementar o fluxo de tratamento.** Correção, mitigação, prioridade, responsável, prazo, aprovação ou rejeição humana, justificativa, status, evidência de conclusão e reanálise.
10. **Entregar relatórios e auditoria.** Permitir consulta por ambiente, ativo, vulnerabilidade, prioridade, tratamento, período e execução do watcher.
11. **Criar o portal de revisores somente após o fluxo operacional.** Preservar cegamento, atribuição individual, submissão final, bloqueio e compatibilidade com o protocolo científico.
12. **Preparar produção.** Cobrir testes unitários, integração e E2E, segurança, uploads, segredos, observabilidade, backups, tratamento de erros, CI/CD, deploy e validação pública.

## Prioridades imediatas

- Finalizar e versionar a documentação.
- Fechar a Fase 0.
- Implementar autenticação/RBAC e o modelo básico de usuários, organizações e ambientes.

## Primeiro marco demonstrável

Um operador autenticado cria um ambiente, importa dados reais e visualiza os ativos e vulnerabilidades encontrados.

## Critérios de execução

- Não promover demo a funcionalidade operacional.
- Não declarar deploy atual sem verificação pública.
- Não tratar priorização contextual como CVSS oficial.
- Não produzir resultados científicos antes das respostas bloqueadas dos três revisores.

## Notas relacionadas

[[00_Index]] · [[CURRENT_PHASE_STATUS]] · [[ROADMAP]] · [[ARCHITECTURE]]
