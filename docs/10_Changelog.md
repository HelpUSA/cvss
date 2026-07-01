---
status: active
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - changelog
aliases:
  - "CVSS Changelog"
related_files:
  - docs/README.md
  - docs/00_Index.md
---

# Changelog


## 2026-07-01


- Created Obsidian-style documentation hub with [[00_Index]] and [[README]].
- Added the [[decisions/ADR-001-official-vs-contextual-separation]] decision record.
- Added atomic notes for project overview, architecture, official CVSS core, contextual engine, real-world wrapper, data model, testing, dashboard/exports, and article writing.
- Repaired indentation in ``core/cvss_environmental_engine.py`` after it was found during validation.
- Validated wrapper smoke for ``CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`` with official score 9.8.

## Next

- Add permanent wrapper test.
- Integrate the wrapper into CSV/JSON exports.
- Update the dashboard to display Official CVSS and Contextual Prioritization as separate concepts.
