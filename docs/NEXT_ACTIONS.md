# Next actions

Estas são as 12 atividades oficiais, em ordem. Uma atividade posterior não deve antecipar alegações de conclusão das anteriores.

1. **Preservar a auditoria documental como gate contínuo.** Manter as 102 notas coerentes, sem wikilinks quebrados ou ambíguos, sem links Markdown internos `.md` e com registro reproduzível das validações, commits e estado final do Git.
2. **Preservar a linha de base da Fase 0.** Manter compilação Python, 52 testes, JavaScript, TypeScript, Prisma, build Next.js, pipeline real, auditoria das 102 notas e Git limpo como gates obrigatórios.
3. **Evoluir a arquitetura operacional canônica.** Manter Next.js como interface web, Prisma com PostgreSQL como persistência e Python restrito à engine CVSS, ao watcher e ao processamento interno suportado; qualquer API interna Python exige decisão arquitetural, contratos, testes e documentação.
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

- Manter a documentação versionada, coerente e auditável.
- Preservar os gates aprovados da linha de base da Fase 0.
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
