---
status: active
last_updated: 2026-07-01
owner: "Wagner / CVSS project"
tags:
  - cvss
  - testing
  - validation
aliases:
  - "CVSS Tests"
  - "Validation"
related_files:
  - core/cvss31.py
  - core/cvss_environmental_engine.py
  - core/cvss_real_world.py
  - docs/TEST_REPORT.md
---

# Testing and Validation


## Current validations

Compilation validation passed for:

- ``core/cvss31.py``
- ``core/cvss_environmental_engine.py``
- ``core/cvss_real_world.py``

Official core has been manually checked against examples returning 9.8, 8.8, and 6.1.

## Real-world wrapper smoke

The wrapper smoke used this vector:


``CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H``

Expected official output:

- base score: 9.8
- severity: Critical

Observed wrapper smoke:

- ``official_cvss`` present
- ``contextual_environmental`` present
- ``evidence`` present
- contextual score can differ from the official score without overwriting it

## Next test

Add a permanent test for ``assess_finding(row)``, preferably ``tests/test_real_world_wrapper.py``.

See [[05_Real_World_Wrapper]] and [[real_world/REAL_WORLD_VALIDATION_PROTOCOL]].
