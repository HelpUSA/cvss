---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - dataset
  - schema
  - cvss-v4
  - environmental-metrics
  - article
---

# Article dataset schema: CVSS v4.0 Environmental Metrics with AI/watcher assistance

Planned dataset:

- `data/article/cvss40_environmental_scenarios.csv`

## Required fields

| Field | Type | Required | Purpose |
|---|---|---:|---|
| `scenario_id` | string | yes | Stable scenario identifier |
| `cve_id` | string | no | CVE if available |
| `vulnerability_summary` | string | yes | Short vulnerability description |
| `official_cvss_v4_vector` | string | yes | Official or assigned CVSS v4.0 vector |
| `cvss_b_score` | number | yes | Base score |
| `cvss_b_severity` | string | yes | Base severity label |
| `asset_class` | string | yes | Type of affected asset |
| `deployment_context` | string | yes | How the system is deployed |
| `internet_exposure` | string | yes | Exposure level |
| `privilege_context` | string | yes | Account or privilege context |
| `compensating_controls` | string | yes | Controls such as WAF, segmentation, hardening, monitoring |
| `confidentiality_requirement` | string | yes | Candidate CR value and rationale |
| `integrity_requirement` | string | yes | Candidate IR value and rationale |
| `availability_requirement` | string | yes | Candidate AR value and rationale |
| `candidate_modified_metrics` | string | yes | Candidate Modified Base metrics |
| `threat_context` | string | no | Threat or exploit information |
| `supplemental_context` | string | no | Supplemental observations |
| `evidence_links` | string | yes | Evidence references or local evidence IDs |
| `evidence_summary` | string | yes | Human-readable evidence summary |
| `watcher_recommendation` | string | yes | AI/watcher recommendation text |
| `uncertainty_flags` | string | yes | Missing/conflicting evidence markers |
| `review_required` | boolean | yes | Whether human review is required |
| `human_review_status` | enum | yes | `required`, `reviewed`, or `not_required` |
| `base_priority` | string | yes | Priority from Base-only view |
| `environmental_priority` | string | yes | Priority after Environmental-aware assessment |
| `priority_delta` | number | yes | Difference between priorities |
| `trace_json` | string | yes | Path or ID of trace artifact |

## Controlled values

### `internet_exposure`

- `public`
- `restricted`
- `internal`
- `isolated`
- `unknown`

### `human_review_status`

- `required`
- `reviewed`
- `not_required`

### `base_priority` and `environmental_priority`

- `critical`
- `high`
- `medium`
- `low`
- `defer`

## Rule

No candidate Environmental metric should be treated as final unless `human_review_status` is explicit. The article may report watcher-assisted candidate values, evidence coverage, and trace completeness, but must not report autonomous official scoring.

<!-- BEGIN CVSS40_PHASE4_DATASET_METADATA_20260710 -->
## Phase 4 dataset metadata

The dataset may include extra metadata columns beyond the core schema:

- `scenario_source`
- `cvss_source`
- `source_url`
- `published`
- `last_modified`
- `vuln_status`

Rows with `scenario_source = nvd_cvss_v4_with_curated_environment` use a real NVD CVE record with CVSS v4.0 data when available, while the local Environmental context is curated for article evaluation.

Rows with `scenario_source = curated_synthetic_no_cve` are synthetic curated scenarios with assigned CVSS v4.0 vectors for workflow testing. They must not be presented as official CVE scores.
<!-- END CVSS40_PHASE4_DATASET_METADATA_20260710 -->

<!-- BEGIN CVSS40_PHASE4B_NVD_CANDIDATES_20260710 -->
## Phase 4B NVD candidate scan

The NVD candidate scan was run at `20260710T124619Z`.

Outputs:

- `data/article/cvss40_nvd_candidates.csv`
- `data/article/cvss40_environmental_scenarios.backup.20260710T124619Z.csv`
- `validation/article/cvss40_scenario_metrics.json`

If NVD candidates were found, the script promoted them into the main scenario dataset while preserving explicit scenario source labels. NVD rows use real CVE/CVSS v4.0 source data, but local Environmental context remains curated for article evaluation.
<!-- END CVSS40_PHASE4B_NVD_CANDIDATES_20260710 -->

<!-- BEGIN CVSS40_PHASE4C_NVD_SAFE_PAGED_SCAN_20260710 -->
## Phase 4C NVD safe paged scan

The NVD safe paged scan was run at `20260713T162235Z`.

Changes from Phase 4B:

- Uses smaller NVD pages.
- Reads the full HTTP response instead of truncating at 8 MB.
- Scans both published-date and last-modified-date windows.
- Preserves a dataset backup before promotion.

Outputs:

- `data/article/cvss40_nvd_candidates.csv`
- `data/article/cvss40_environmental_scenarios.backup.20260713T162235Z.csv`
- `validation/article/cvss40_scenario_metrics.json`
<!-- END CVSS40_PHASE4C_NVD_SAFE_PAGED_SCAN_20260710 -->
