# CVSS research, article, and product sequence

This document defines the correct order of activities for the CVSS environmental scoring research project and article. The order is intended to prevent implementation work from running ahead of the scientific method.

## Current research question

Can an automated, evidence-linked pipeline adjust and justify CVSS environmental scoring using infrastructure context, segmentation, PCI scope, compensating controls, and business impact while producing reproducible and auditable artifacts?

## Current article scope

In scope: automated pipeline, curated scenarios, environmental CVSS adjustment, watcher/IA validation, reproducible artifacts, article tables, and public demonstrator dashboard.

Out of scope for the current article: completed independent human expert validation, production-grade multi-user application, persistent database, public API maturity, and enterprise deployment claims. Human expert comparison is future work.

## Correct sequence

1. Close the research question.
2. Close the current article scope.
3. Consolidate the methodology.
4. Standardize scenario input artifacts.
5. Standardize pipeline output artifacts.
6. Strengthen the CVSS environmental calculation engine.
7. Validate the current pilot scenario.
8. Expand curated scenarios.
9. Automate full rebuild of outputs.
10. Improve the static dashboard as a research-results report.
11. Update the article with consolidated results.
12. Review scientific language and limitations.
13. Generate the final article and reproducibility package.
14. Build the interactive site MVP.
15. Make the site export pipeline-compatible data.
16. Add site-side report generation.
17. Leave backend, persistence, login, and public API for a later product phase.

## Why the interactive site comes later

The interactive site must not define the scientific method. It should expose the method after the scenario schema, output schema, and scoring engine are stable. Otherwise the project risks building a user interface over an unstable research model.

## Current deployment decision

The public site is intentionally static at repository root. This avoids the previous Vercel/Next.js/Production Overrides failure mode and keeps public reproducibility stable.
