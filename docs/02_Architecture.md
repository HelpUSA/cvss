# Architecture

## Status

- status: active
- last_updated: 2026-07-01
- owner: Wagner / CVSS project
- related_files: core/cvss31.py, core/cvss_environmental_engine.py, core/cvss_real_world.py, docs/real_world/OFFICIAL_CONTEXTUAL_INTEGRATION.md

## Main components

The architecture has three separate responsibilities:

- [[03_CVSS_Official_Core]] calculates official CVSS v3.1 outputs from the vector.
- [[04_Contextual_Engine]] applies operational and environmental adjustments.
- [[05_Real_World_Wrapper]] combines both outputs without merging their meaning.

## Output contract

The wrapper should return:

- ``official_cvss`
- ``contextual_environmental`
- ``evidence`

This contract prevents the contextual result from being confused with official CVSS.

## Pipeline direction

The downstream pipeline, exports, dashboard, and article language should use explicit field names:

- ``official_cvss_*`` for vector-derived CVSS fields.
- ``contextual_*`` for environmental/prioritization fields.
- ``evidence_*`` for supporting data and traceability.

See [[06_Data_Model]], [[08_Dashboard_and_Exports]], and [[09_Paper_or_Article]].
