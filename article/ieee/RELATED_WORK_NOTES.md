---
status: active
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, related-work, epss, ssvc, vulnerability-prioritization]
---

# Phase 10 related-work notes

## Positioning

The article positions the watcher as an evidence and traceability layer for
CVSS v4.0 Environmental assessment.

It does not claim to replace:

- CVSS severity;
- EPSS exploit prediction;
- SSVC stakeholder-specific decisions;
- enterprise patch-management governance;
- human analysts.

## Literature groups

### CVSS and contextualization

- FIRST CVSS v4.0 specification, user guide, and implementation guide.
- Fruhwirth and Mannisto, 2009: CVSS prioritization with context information.
- Howland, 2023: critique of treating CVSS as a complete prioritization system.
- Jung, Li, and Bechor, 2022: context-aware vulnerability prioritization.

### Stakeholder decisions

- Spring et al., 2021: SSVC version 2.0 and stakeholder-specific decision trees.

### Threat prediction

- Jacobs et al., 2020: exploit prediction and remediation efficiency.
- Jacobs et al., 2021: EPSS framework.
- Jacobs et al., 2023: community-driven EPSS model development.

### Enterprise management

- NIST SP 800-40 Rev. 4: prioritization within enterprise patch management.

### Comparative evidence

- Koscinski et al., 2025: empirical comparison of CVSS, SSVC, EPSS, and
  Exploitability Index.

## Dataset boundary

- Total scenarios: 30
- Real NVD/CVSS v4.0 records: 12
- Curated synthetic records: 18
- Real NVD rows use curated consumer Environmental contexts.
- The contexts are not sourced from NVD.
- Priority delta is a custom operational category delta.
