---
status: active
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - contextual
  - implementation
aliases:
  - "Environmental Engine"
  - "Contextual Prioritization Engine"
related_files:
  - core/cvss_environmental_engine.py
  - docs/real_world/OFFICIAL_CONTEXTUAL_INTEGRATION.md
---

# Contextual Engine


## Code

Primary implementation: ../core/cvss_environmental_engine.py

## Responsibility

The contextual engine produces an environmental or operational prioritization score from real-world evidence.

It may use fields such as:

- internet exposure
- network segmentation
- firewall restrictions
- compensating controls
- PCI scope
- business criticality

## Current implementation note

The file had lost Python indentation and was repaired on 2026-07-01. After the repair, ``py_compile`` passed for:

- ../core/cvss31.py
- ../core/cvss_environmental_engine.py
- ../core/cvss_real_world.py

## Boundary

The contextual engine must not modify or redefine the official CVSS score.

See [[decisions/ADR-001-official-vs-contextual-separation]] and [[02_Architecture]].
