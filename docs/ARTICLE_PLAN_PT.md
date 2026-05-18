# Plano do artigo — automação de CVSS Environmental com AI Bridge

## Pergunta de pesquisa

Como um sistema multiagente local, com acesso real a evidências do ambiente por meio do AI Bridge,
pode automatizar a avaliação de CVSS Environmental Metrics em cenários segmentados inspirados em PCI-DSS?

## Contribuição principal

O artigo propõe uma evolução do trabalho anterior: em vez de medir dificuldade humana,
mostra uma pipeline de automação baseada em evidências.

## Hipóteses iniciais

- H1: Agentes operando pelo AI Bridge conseguem gerar CR/IR/AR consistentes com um gabarito especialista.
- H2: A coleta de evidências locais reduz decisões ambientais sem justificativa.
- H3: A revisão multiagente reduz inconsistências entre escopo PCI-DSS, topologia e vetor CVSS.
- H4: A trilha auditável permite reconstruir cada decisão ambiental.

## Artefato mínimo

- Dataset estruturado.
- Pipeline Python reprodutível.
- Prompts multiagente.
- Envelopes watcher.
- Template LaTeX Overleaf.
- Saída demo.
