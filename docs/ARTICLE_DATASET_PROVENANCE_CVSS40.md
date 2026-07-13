---
status: active
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, dataset, provenance, nvd, article]
---

# CVSS v4.0 article dataset provenance

Generated UTC: `2026-07-13T16:32:32.078162+00:00`

## Summary

| Metric | Value |
|---|---|
| Scenario count | 30 |
| NVD CVSS v4.0 rows | 12 |
| Synthetic curated rows | 18 |
| Evidence coverage | 100.00% |
| Trace completeness | 100.00% |
| Uncertainty rate | 100.00% |
| Human review required rows | 30 |
| Priority shift count | 22 |
| Priority shift percentage | 73.33% |
| Average priority delta | 0.2 |
| Maximum priority delta | 2.0 |
| Minimum priority delta | -3.0 |

## Source distribution

| Scenario source | Count |
|---|---|
| curated_synthetic_no_cve | 18 |
| nvd_cvss_v4_with_curated_environment | 12 |

## CVSS-B severity distribution

| CVSS-B severity | Count |
|---|---|
| CRITICAL | 3 |
| HIGH | 9 |
| LOW | 5 |
| MEDIUM | 13 |

## Exposure distribution

| Internet exposure | Count |
|---|---|
| internal | 7 |
| isolated | 4 |
| public | 7 |
| restricted | 12 |

## Asset class distribution

| Asset class | Count |
|---|---|
| database_server | 4 |
| developer_workstation | 4 |
| identity_provider | 4 |
| internal_admin_console | 4 |
| isolated_lab_system | 4 |
| ot_monitoring_gateway | 3 |
| public_api_gateway | 3 |
| public_web_application | 4 |

## Priority transition distribution

| Base priority | Environmental-aware priority | Count |
|---|---|---|
| critical | critical | 3 |
| high | critical | 4 |
| high | defer | 1 |
| high | high | 2 |
| high | medium | 2 |
| low | defer | 2 |
| low | high | 1 |
| low | low | 1 |
| low | medium | 1 |
| medium | critical | 2 |
| medium | defer | 1 |
| medium | high | 6 |
| medium | low | 2 |
| medium | medium | 2 |

## NVD/CVSS v4.0 rows

| Scenario | CVE | CVSS-B score | Severity | Base priority | Environmental priority | Delta |
|---|---|---|---|---|---|---|
| SCN-NVD-001 | CVE-2026-4251 | 1.1 | LOW | low | low | 0 |
| SCN-NVD-002 | CVE-2026-4252 | 8.9 | HIGH | high | medium | -1 |
| SCN-NVD-003 | CVE-2026-4270 | 6.8 | MEDIUM | medium | high | 1 |
| SCN-NVD-004 | CVE-2026-28490 | 8.3 | HIGH | high | critical | 1 |
| SCN-NVD-005 | CVE-2026-28498 | 8.2 | HIGH | high | high | 0 |
| SCN-NVD-006 | CVE-2026-29510 | 5.1 | MEDIUM | medium | low | -1 |
| SCN-NVD-007 | CVE-2026-29513 | 5.1 | MEDIUM | medium | medium | 0 |
| SCN-NVD-008 | CVE-2026-29520 | 5.1 | MEDIUM | medium | high | 1 |
| SCN-NVD-009 | CVE-2026-29521 | 5.1 | MEDIUM | medium | high | 1 |
| SCN-NVD-010 | CVE-2026-3644 | 6.0 | MEDIUM | medium | low | -1 |
| SCN-NVD-011 | CVE-2026-4224 | 6.0 | MEDIUM | medium | high | 1 |
| SCN-NVD-012 | CVE-2026-4253 | 2.0 | LOW | low | medium | 1 |

## Boundary

NVD rows use real NVD CVE records and CVSS v4.0 data where present in the dataset. The local Environmental context attached to those rows is curated for article evaluation. Synthetic rows are explicitly marked as `curated_synthetic_no_cve` and must not be presented as official CVE scoring.

The dataset supports workflow evaluation: evidence coverage, trace completeness, uncertainty handling, review status, and priority shifts. It does not prove production effectiveness or predictive superiority.
