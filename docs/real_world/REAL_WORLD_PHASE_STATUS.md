# Real-world phase status

Updated: 
2026-05-28 15:35:16

Branch: real-world-cvss

## Started

- Created real-world implementation plan.
- Created official CVSS integration design.
- Created real-world validation protocol.
- Created data source plan.

## Next technical task

Inspect current engine and add an official-CVSS-compatible module with tests against known vector examples.

## Current warning

The current public MVP is useful as a demonstrator, but definitive real-world use requires official scoring compatibility, real CVE evidence, and stronger validation.

## CVSS v3.1 base-score checkpoint - 
2026-05-28 15:51:00

Added core/cvss31.py and tests/test_cvss31_official.py with known CVSS v3.1 base-score examples. Next task: integrate official_cvss output beside the contextual environmental layer without mixing semantics.


## CVSS v3.1 official base-score core verified

core/cvss31.py now compiles and reproduces known CVSS v3.1 base score examples: 9.8, 8.8, and 6.1. This is the first real-world official CVSS compatibility checkpoint.

