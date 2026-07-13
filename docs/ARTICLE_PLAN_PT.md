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

<!-- BEGIN CVSS40_AI_WATCHER_PLAN_20260709 -->
## Strategic direction: CVSS v4.0 AI/watcher Environmental metric assessment

Date: 2026-07-09

The article should be repositioned around CVSS v4.0 Environmental metric assessment assisted by AI/watcher. CVSS v4.0 already includes official Base, Threat, Environmental, and Supplemental metric groups, so the project must not claim to add or modify official Environmental metrics.

The defensible contribution is an operational evidence layer: the watcher helps analysts collect environmental evidence, suggest candidate Environmental metric choices, link suggestions to evidence, record uncertainty, flag human-review needs, and generate reproducible trace artifacts.

Safe thesis:

> Although CVSS v4.0 defines Environmental metrics for adapting vulnerability severity to a consumer's environment, selecting those metrics remains a difficult and evidence-intensive task for human analysts. This paper proposes an AI-assisted watcher workflow that collects, structures, and traces environmental evidence to support reproducible CVSS v4.0 Environmental metric assessment without modifying the official CVSS standard.

Target paper posture: English IEEE-style method/prototype paper, double-blind, 5 to 8 pages, using ICITEICS-2026 requirements as a model but preparing for a later conference.
<!-- END CVSS40_AI_WATCHER_PLAN_20260709 -->
