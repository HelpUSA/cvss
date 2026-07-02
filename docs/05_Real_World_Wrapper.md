---
status: active
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - wrapper
  - implementation
aliases:
  - "CVSS Real World Wrapper"
  - "assess_finding"
related_files:
  - core/cvss_real_world.py
  - core/cvss31.py
  - core/cvss_environmental_engine.py
---

# Real World Wrapper


## Code

Primary implementation: ../core/cvss_real_world.py

## Responsibility

The wrapper function ``assess_finding(row)`` combines the official CVSS core and the contextual engine while preserving separate output labels.

## Current output

The wrapper returns:

- `official_cvss`
- `contextual_environmental`
- ``evidence`

## Smoke validation

Smoke run on 2026-07-01 used:

``CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H``

Observed result:

- official base score: 9.8
- official base severity: Critical
- contextual score: 10.0
- contextual severity: Critical
- contextual decision: upgraded
- top-level keys: ``official_cvss``, ``contextual_environmental``, ``evidence`

## Current implementation status

Completed integration work covers:

- Permanent wrapper contract testing in ``tests/test_real_world_wrapper.py``.
- CSV, JSON, Markdown, and audit-trace export layers in ``tests/test_reporting_outputs.py``.
- AI Bridge orchestrator output layers in ``tests/test_ai_bridge_orchestrator.py``.
- Rule-engine official/contextual row layers in ``tests/test_rule_engine_layers.py``.
- Dashboard/export language documented in [[08_Dashboard_and_Exports]].

See [[06_Data_Model]], [[07_Testing_and_Validation]], and [[08_Dashboard_and_Exports]].
