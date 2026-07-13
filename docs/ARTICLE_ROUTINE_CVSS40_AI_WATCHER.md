---
status: active
last_updated: 2026-07-09
owner: "Wagner / CVSS project"
tags: [article-routine, cvss-v4, ai-watcher, environmental-metrics, ieee]
---

# Article routine: CVSS v4.0 Environmental Metrics with AI/watcher assistance

## Target outcome

Prepare a strong English IEEE-style double-blind paper for a future cybersecurity or intelligent systems conference.

Working title:

> Operationalizing CVSS v4.0 Environmental Metrics with AI-Assisted Evidence Collection and Traceability

## Core thesis

CVSS v4.0 already defines Base, Threat, Environmental, and Supplemental metric groups. The challenge addressed by our work is not the absence of Environmental metrics, but the operational difficulty of selecting Environmental metric values consistently and justifiably in a real consumer environment.

The proposed contribution is an AI/watcher-assisted workflow that supports the analyst by collecting evidence, suggesting candidate Environmental metric values, recording uncertainty, requiring review status, and exporting reproducible trace artifacts.

## Non-negotiable boundaries

- Preserve official CVSS v4.0 semantics.
- Do not modify the official CVSS formula.
- Do not present watcher output as autonomous official scoring.
- Present the watcher as analyst assistance.
- State that current validation is artifact/reproducibility validation, not production validation.
- State that human expert adjudication is future work unless actual expert review is completed.
- Do not claim predictive superiority.

## Routine phases

### Phase 1 - Official CVSS v4.0 reading and extraction

Read FIRST main page, specification, user guide, implementation guide, examples, FAQ, calculator notes, and data representation materials.

Deliverable: `docs/CVSS40_OFFICIAL_READING_NOTES.md`

### Phase 2 - Contribution mapping

Map each project feature to an official CVSS v4.0 concept.

Deliverable: `docs/ARTICLE_CVSS40_CONTRIBUTION_MAP.md`

### Phase 3 - Dataset design

Prepare 30 to 50 curated vulnerability scenarios.

Deliverables:

- `data/article/cvss40_environmental_scenarios.csv`
- `docs/ARTICLE_DATASET_SCHEMA.md`

### Phase 4 - Pipeline/schema update

Add fields for official CVSS v4 vector, CVSS-B score, candidate Environmental metrics, evidence links, uncertainty flags, human review status, watcher recommendation, review requirement, candidate CVSS-BE score if computed, base priority, environmental priority, priority delta, and trace JSON.

### Phase 5 - Evaluation run

Compute scenario count, evidence coverage, percentage of recommendations linked to evidence, uncertainty flags, human-review-required flags, priority changes, average/max priority delta, trace completeness, and reproducibility status.

### Phase 6 - Article rewrite

Rewrite the manuscript around AI-assisted Environmental metric assessment.

### Phase 7 - Double-blind and conference readiness

Remove author names, affiliations, personal emails, public GitHub links, HelpUSA/Wagner references, acknowledgments, and public dashboard URLs that identify authorship.
