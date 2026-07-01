---
status: planned
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - dashboard
  - exports
aliases:
  - "CVSS Dashboard"
  - "CVSS Exports"
related_files:
  - docs/CLOUD_DASHBOARD_PLAN.md
  - docs/INTERACTIVE_SITE_PLAN.md
  - docs/INTERACTIVE_EXPORT_FORMAT.md
  - docs/SITE_REPORT_EXPORT.md
---

# Dashboard and Exports


## Dashboard labels

Dashboard labels must show two concepts separately:

- Official CVSS
- Contextual Prioritization

Do not display the contextual score as official CVSS.

## Exports

CSV and JSON exports should emit separate field families:

- ```official_cvss_*``
- ``contextual_*``
- ``evidence_*``

## Pipeline task

Integrate ``assess_finding()`` into the current pipeline/exporter without changing the official CVSS calculator.

See [[06_Data_Model]] and [[09_Paper_or_Article]].
