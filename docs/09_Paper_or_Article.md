# Paper or Article

## Status

- status: active
- last_updated: 2026-07-01
- owner: Wagner / CVSS project
- related_files: docs/ARTICLE_PLAN_PT.md, docs/ARTICLE_STATUS.md, docs/ARTICLE_REBOOT_PLAN.md, docs/ARTICLE_REFINEMENT_TODO.md

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
