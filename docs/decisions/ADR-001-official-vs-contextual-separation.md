---
status: accepted
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - adr
  - decision
  - official-cvss
  - contextual
aliases:
  - "ADR-001"
  - "Official vs Contextual Separation"
related_files:
  - docs/real_world/OFFICIAL_CONTEXTUAL_INTEGRATION.md
  - docs/real_world/OFFICIAL_CVSS_INTEGRATION_DESIGN.md
  - core/cvss31.py
  - core/cvss_environmental_engine.py
  - core/cvss_real_world.py
---

# ADR-001 Official CVSS vs Contextual Separation


## Context

The project combines an official CVSS v3.1 calculation with a real-world contextual prioritization layer.

The central risk is terminology drift: contextual prioritization must not be presented as official CVSS.

## Decision

Expose two separate outputs:

- official_cvss: calculated only from the official CVSS v3.1 vector.
- contextual_environmental: calculated from operational and environmental evidence.

## Consequences

Code, exports, dashboard labels, documentation, and article language must preserve this distinction.

See also [[02_Architecture]], [[05_Real_World_Wrapper]], and [[real_world/OFFICIAL_CONTEXTUAL_INTEGRATION]].
