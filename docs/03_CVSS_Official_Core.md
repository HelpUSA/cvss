# CVSS Official Core

## Status

- status: active
- last_updated: 2026-07-01
- owner: Wagner / CVSS project
- related_files: core/cvss31.py, docs/real_world/CVSS31_CORE_COMPATIBILITY.md

## Code

Primary implementation: ../core/cvss31.py

## Responsibility

The official core calculates CVSS v3.x base scoring from the vector.

It must not use contextual information such as exposure, segmentation, controls, PCI scope, exploit intelligence, or business criticality.

## Known validation

Manual official-example validation already covered scores:

- 9.8
- 8.8
- 6.1

The current wrapper smoke also confirmed that vector ``CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`` returns official base score 9.8 and severity Critical.

## Related notes

- [[05_Real_World_Wrapper]]
- [[07_Testing_and_Validation]]
- [[real_world/OFFICIAL_CVSS_INTEGRATION_DESIGN]]
