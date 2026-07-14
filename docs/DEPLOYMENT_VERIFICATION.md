# Deployment verification

## Estado atual

O deploy público atual não está verificado por esta auditoria. Registros históricos mencionam caminhos estáticos e domínios diferentes, e houve relato recente de domínio servindo conteúdo não relacionado. Portanto, nenhuma URL deve ser tratada como produção válida sem nova inspeção pública e confirmação do projeto Vercel associado.

## Requisitos para considerar validado

- domínio e projeto corretos;
- commit e branch implantados identificados;
- conteúdo esperado do CVSS visível;
- rotas e assets sem erro;
- variáveis e banco corretos;
- health checks dos componentes;
- smoke test autenticado quando o produto existir;
- rollback documentado.

## Direção

A documentação antiga que orientava abandonar Next.js e manter somente um site estático está supersedida para o produto operacional. O dashboard estático pode permanecer como demo, mas não é a arquitetura-alvo.

## Notas relacionadas

[[00_Index]] · [[ARCHITECTURE]] · [[WEB_APPLICATION]] · [[ROADMAP]] · [[07_Testing_and_Validation]]
