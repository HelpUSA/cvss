---
status: active
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - data-model
  - exports
aliases:
  - "CVSS Data Model"
related_files:
  - core/cvss_real_world.py
  - docs/schemas/PIPELINE_OUTPUT_SCHEMA.md
  - docs/schemas/SCENARIO_INPUT_SCHEMA.md
---

# Data Model


## Input

The wrapper expects a row-like object with an official CVSS vector:

- ``cvss_vector``
- or ``vector``

Contextual fields may include:

- `minternet_exposed``
- ``network_segmented``
- ``firewall_restricted``
- ``compensating_controls``
- ``pci_in_scope``
- ``business_criticality``
- ``asset_id``
- ``cve``
- ``source_url``
- ``environment``

## Output

The wrapper output must remain split:

- `official_cvss` for official vector-derived results.
- `contextual_environmental` for contextual prioritization.
- `evidence` for asset scope, business, and source context.

## Export naming

Use prefixes to prevent confusion:

- `official_cvss_*`
- `contextual_*`
- `evidence_*`

See [[08_Dashboard_and_Exports]] and [[02_Architecture]].
