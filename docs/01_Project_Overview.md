---
status: active
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - overview
  - documentation
aliases:
  - "CVSS Project Overview"
related_files:
  - docs/README.md
  - docs/00_Index.md
  - docs/CURRENT_HANDOFF.md
  - docs/real_world/REAL_WORLD_PHASE_STATUS.md
---

# Project Overview


## Purpose

This project builds an application, article, and prototype for practical vulnerability assessment using official CVSS v3.1 plus a separate contextual operational layer.

The project must support research, implementation, validation, dashboarding, and exportable evidence.

## Scope

The scope is real-world vulnerability prioritization.

The system should keep the official CVSS calculation intact while adding contextual information such as asset exposure, segmentation, compensating controls, PCI scope, exploitability evidence, and business criticality.

## Non-negotiable boundary

``official_cvss` is not a business-risk score. It is the result of the official CVSS vector calculation only.

``contextual_environmental` is a prioritization layer. It may use environmental and operational evidence, but it must not be labeled as official CVSS.

See [[decisions/ADR-001-official-vs-contextual-separation]], [[02_Architecture]], and [[real_world/OFFICIAL_CONTEXTUAL_INTEGRATION]].
