---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - article
  - claim-guardrails
  - cvss-v4
  - environmental-metrics
  - ai-watcher
---

# Claim guardrails for the CVSS v4.0 AI/watcher article

## Safe positioning

The project should be positioned as:

> An AI/watcher-assisted workflow for evidence-backed, human-reviewable CVSS v4.0 Environmental metric assessment.

## Do

Use these phrases:

- "AI-assisted"
- "watcher-assisted"
- "evidence-backed recommendation"
- "candidate Environmental metric value"
- "human-reviewable"
- "human review status"
- "uncertainty flag"
- "trace artifact"
- "CVSS v4.0 semantics are preserved"
- "official CVSS formula is not modified"
- "consumer-side Environmental assessment"
- "artifact and reproducibility validation"

## Do not

Avoid these phrases unless explicitly negated as a limitation:

- "improves CVSS"
- "fixes CVSS"
- "replaces CVSS"
- "new CVSS score"
- "new official Environmental metrics"
- "autonomous official scoring"
- "AI replaces analysts"
- "validated in production"
- "proves better prediction"
- "proves real-world effectiveness"
- "modifies the CVSS formula"

## Required limitation language

The paper must state:

1. The prototype does not modify the official CVSS v4.0 standard.
2. Watcher output is a recommendation, not an autonomous final score.
3. Human review remains required for final Environmental metric decisions.
4. Current evaluation is based on curated scenarios.
5. Current validation demonstrates reproducibility and traceability, not production effectiveness.
6. Independent expert adjudication is future work unless actually completed.

## Review checklist before submission

- Does every score table identify the metric group label?
- Does every Environmental recommendation have evidence?
- Does every recommendation have a review status?
- Are uncertainty flags reported?
- Are official CVSS fields separated from watcher fields?
- Does the article avoid claiming predictive superiority?
- Does the article cite FIRST CVSS v4.0 official documentation?
