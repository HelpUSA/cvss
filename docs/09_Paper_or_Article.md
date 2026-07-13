---
status: active
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - research
  - article
aliases:
  - "CVSS Article"
  - "Paper"
related_files:
  - docs/ARTICLE_PLAN_PT.md
  - docs/ARTICLE_STATUS.md
  - docs/ARTICLE_REBOOT_PLAN.md
  - docs/ARTICLE_REFINEMENT_TODO.md
---

# Paper or Article


## Article premise

The article should describe a practical prototype for vulnerability prioritization that preserves official CVSS v3.1 while explicitly separating contexual operational prioritization.

## Method boundary

When writing the article, use language such as:

- `official CVSS v3.1 base score`
- `contextual prioritization`
- `real-world environmental layer`

as separate concepts.

Avoid language that implies the contextual score is an official CVSS score.

## Evidence to include

- official CVSS v3.1 validation
- separate contextual layer design
- export field separation
- wrapper smoke results
- traceable evidence for adjustments

See [[ARTICLE_PLAN_PT]], [[ARTICLE_STATUS]], and [[decisions/ADR-001-official-vs-contextual-separation]].

<!-- BEGIN CVSS40_AI_WATCHER_DIRECTION_20260709 -->
## Strategic direction: CVSS v4.0 AI/watcher Environmental metric assessment

Date: 2026-07-09

The article should be repositioned around CVSS v4.0 Environmental metric assessment assisted by AI/watcher. CVSS v4.0 already includes official Base, Threat, Environmental, and Supplemental metric groups, so the project must not claim to add or modify official Environmental metrics.

The defensible contribution is an operational evidence layer: the watcher helps analysts collect environmental evidence, suggest candidate Environmental metric choices, link suggestions to evidence, record uncertainty, flag human-review needs, and generate reproducible trace artifacts.

Safe thesis:

> Although CVSS v4.0 defines Environmental metrics for adapting vulnerability severity to a consumer's environment, selecting those metrics remains a difficult and evidence-intensive task for human analysts. This paper proposes an AI-assisted watcher workflow that collects, structures, and traces environmental evidence to support reproducible CVSS v4.0 Environmental metric assessment without modifying the official CVSS standard.

Target paper posture: English IEEE-style method/prototype paper, double-blind, 5 to 8 pages, using ICITEICS-2026 requirements as a model but preparing for a later conference.
<!-- END CVSS40_AI_WATCHER_DIRECTION_20260709 -->

<!-- BEGIN CVSS40_AI_WATCHER_ROUTINE_20260709 -->
## Current article routine

The article now follows the CVSS v4.0 AI/watcher Environmental metric assessment routine:

- Read and cite official FIRST CVSS v4.0 documentation.
- Preserve official CVSS v4.0 semantics and formula.
- Treat AI/watcher output as evidence-backed recommendations requiring explicit review status.
- Build 30 to 50 curated vulnerability scenarios.
- Evaluate evidence coverage, trace completeness, uncertainty, human review status, and priority shifts.
- Prepare an English IEEE-style, double-blind 5 to 8 page method/prototype paper for a future conference.
<!-- END CVSS40_AI_WATCHER_ROUTINE_20260709 -->

<!-- BEGIN CVSS40_PHASE5_EVALUATION_RESULTS_20260713 -->
## Evaluation and Results status

The article now has generated Evaluation, Results, Discussion, and Limitations draft material based on the current scenario dataset.

Current dataset framing:

- Hybrid scenario dataset.
- Real NVD/CVSS v4.0 rows are used where available.
- Local Environmental context remains curated for workflow evaluation.
- Synthetic rows remain explicitly marked.
- Watcher outputs remain evidence-backed candidate recommendations requiring human review.
- The evaluation supports traceability/reproducibility claims, not production effectiveness or predictive superiority.
<!-- END CVSS40_PHASE5_EVALUATION_RESULTS_20260713 -->
