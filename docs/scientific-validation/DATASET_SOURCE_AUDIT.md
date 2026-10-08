# Dataset Source Audit

## Institutional provenance terminology

- **FIRST** maintains the CVSS specification and reference resources.
- **CNA** organizations maintain CVE records under their authority and may publish CVSS assessments.
- **NVD** indexes and may enrich vulnerability records. A score displayed by NVD may have been supplied by a CNA; provenance must therefore be recorded explicitly.

## Critical correction: score nomenclature

The legacy project CSV used the column name `cvss_b_score` even when the stored source vector contained an explicit Threat metric such as `E:P`. In CVSS v4.0, the displayed nomenclature must reflect the explicitly selected metric groups. Such records are **CVSS-BT**, not pure CVSS-B.

This review therefore adds:

`data/article/dataset_b_source_assessments_normalized.csv`

with separate fields for `source_cvss_v4_vector`, `source_nomenclature`, `source_score`, `source_severity`, provider information, and legacy operational disposition. The original CSV remains only as a compatibility artifact and must not be used as the canonical scientific source.

## Required local-source audit before freeze

Antigravity must re-query or re-validate each of the 12 real CVE source assessments from the authoritative CNA/NVD records available to the local project, add a real `retrieved_at` timestamp, preserve all competing assessments when multiple providers exist, and record which assessment was selected and why. No v3.1-to-v4.0 conversion may be invented.

## Dataset roles

- **A1 - Historical Human Results:** Allodi et al., FDSE 2017; CVSS v3.0 historical human-factors evidence.
- **B - Development Benchmark:** 30 current scenarios used for architecture development/regression; not evidence of generalization.
- **C1 - Independent Diverse Held-Out Set:** planned effectiveness evaluation.
- **C2 - Adversarial Safety Challenge Set:** planned safety/fail-safe evaluation.

The historical repository folder may contain `ESSOS-2017` in its path, but the publication is **Future Data and Security Engineering (FDSE 2017)** and should be cited as Allodi et al.
