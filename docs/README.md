# CVSS Documentation Hub

## Status

- status: active
- last_updated: 2026-07-01
- owner: Wagner / CVSS project
- related_files: docs/00_Index.md, docs/real_world/OFFICIAL_CONTEXTUAL_INTEGRATION.md, core/cvss_real_world.py

Start with [[00_Index]].

## Core rule

official_cvss must be calculated only from the official CVSS v3.1 vector.

contextual_environmental may use real-world evidence such as exposure, segmentation, compensating controls, PCI scope, and business criticality, but it must never be labeled as official CVSS.

See [[decisions/ADR-001-official-vs-contextual-separation]] and [[real_world/OFFICIAL_CONTEXTUAL_INTEGRATION]].
