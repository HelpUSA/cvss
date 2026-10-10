# Resumo Canônico de Proveniência do Dataset B

O arquivo `data/dataset_b_source_assessments_normalized.csv` constitui a **Single Source of Truth** do Dataset B, contendo 30 cenários normalizados.

### 1. Cenários com CVEs Reais (CNA / NVD Published) - n = 12

| Scenario ID | CVE ID | Origem / Provider | Base Vector | Nomenclature | Score | Severidade | Fonte Oficial |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `SCN-NVD-001` | `CVE-2026-4251` | cna@vuldb.com (CNA) | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/V...` | `CVSS-BT` | 1.1 | LOW | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-4251) |
| `SCN-NVD-002` | `CVE-2026-4252` | cna@vuldb.com (CNA) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/V...` | `CVSS-BT` | 8.9 | HIGH | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-4252) |
| `SCN-NVD-003` | `CVE-2026-4270` | ff89ba41-3aa1-4d27-914a-91399e9639e5 (CNA) | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/V...` | `CVSS-B` | 6.8 | MEDIUM | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-4270) |
| `SCN-NVD-004` | `CVE-2026-28490` | security-advisories@github.com (CNA) | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/V...` | `CVSS-B` | 8.3 | HIGH | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-28490) |
| `SCN-NVD-005` | `CVE-2026-28498` | security-advisories@github.com (CNA) | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/V...` | `CVSS-B` | 8.2 | HIGH | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-28498) |
| `SCN-NVD-006` | `CVE-2026-29510` | disclosure@vulncheck.com (CNA) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/V...` | `CVSS-B` | 5.1 | MEDIUM | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-29510) |
| `SCN-NVD-007` | `CVE-2026-29513` | disclosure@vulncheck.com (CNA) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/V...` | `CVSS-B` | 5.1 | MEDIUM | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-29513) |
| `SCN-NVD-008` | `CVE-2026-29520` | disclosure@vulncheck.com (CNA) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/V...` | `CVSS-B` | 5.1 | MEDIUM | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-29520) |
| `SCN-NVD-009` | `CVE-2026-29521` | disclosure@vulncheck.com (CNA) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/V...` | `CVSS-B` | 5.1 | MEDIUM | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-29521) |
| `SCN-NVD-010` | `CVE-2026-3644` | cna@python.org (CNA) | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/V...` | `CVSS-B` | 6.0 | MEDIUM | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-3644) |
| `SCN-NVD-011` | `CVE-2026-4224` | cna@python.org (CNA) | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/V...` | `CVSS-B` | 6.0 | MEDIUM | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-4224) |
| `SCN-NVD-012` | `CVE-2026-4253` | cna@vuldb.com (CNA) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/V...` | `CVSS-BT` | 2.0 | LOW | [NVD-indexed CNA record](https://nvd.nist.gov/vuln/detail/CVE-2026-4253) |

### 2. Cenários Sintéticos Controlados (Investigator-Assigned) - n = 18

| Scenario ID | Asset Class | Base Vector | Nomenclature | Score | Severidade | Origem |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `SCN-SYN-013` | `developer_workstation` | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/V...` | `CVSS-B` | 9.3 | CRITICAL | `SYNTHETIC` |
| `SCN-SYN-014` | `isolated_lab_system` | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/V...` | `CVSS-B` | 8.7 | HIGH | `SYNTHETIC` |
| `SCN-SYN-015` | `ot_monitoring_gateway` | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/V...` | `CVSS-B` | 7.1 | HIGH | `SYNTHETIC` |
| `SCN-SYN-016` | `public_api_gateway` | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/V...` | `CVSS-B` | 6.8 | MEDIUM | `SYNTHETIC` |
| `SCN-SYN-017` | `public_web_application` | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:A/V...` | `CVSS-B` | 4.8 | MEDIUM | `SYNTHETIC` |
| `SCN-SYN-018` | `internal_admin_console` | `CVSS:4.0/AV:P/AC:H/AT:P/PR:H/UI:A/V...` | `CVSS-B` | 2.1 | LOW | `SYNTHETIC` |
| `SCN-SYN-019` | `identity_provider` | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/V...` | `CVSS-B` | 9.3 | CRITICAL | `SYNTHETIC` |
| `SCN-SYN-020` | `database_server` | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/V...` | `CVSS-B` | 8.7 | HIGH | `SYNTHETIC` |
| `SCN-SYN-021` | `developer_workstation` | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/V...` | `CVSS-B` | 7.1 | HIGH | `SYNTHETIC` |
| `SCN-SYN-022` | `isolated_lab_system` | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/V...` | `CVSS-B` | 6.8 | MEDIUM | `SYNTHETIC` |
| `SCN-SYN-023` | `ot_monitoring_gateway` | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:A/V...` | `CVSS-B` | 4.8 | MEDIUM | `SYNTHETIC` |
| `SCN-SYN-024` | `public_api_gateway` | `CVSS:4.0/AV:P/AC:H/AT:P/PR:H/UI:A/V...` | `CVSS-B` | 2.1 | LOW | `SYNTHETIC` |
| `SCN-SYN-025` | `public_web_application` | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/V...` | `CVSS-B` | 9.3 | CRITICAL | `SYNTHETIC` |
| `SCN-SYN-026` | `internal_admin_console` | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/V...` | `CVSS-B` | 8.7 | HIGH | `SYNTHETIC` |
| `SCN-SYN-027` | `identity_provider` | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/V...` | `CVSS-B` | 7.1 | HIGH | `SYNTHETIC` |
| `SCN-SYN-028` | `database_server` | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/V...` | `CVSS-B` | 6.8 | MEDIUM | `SYNTHETIC` |
| `SCN-SYN-029` | `developer_workstation` | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:A/V...` | `CVSS-B` | 4.8 | MEDIUM | `SYNTHETIC` |
| `SCN-SYN-030` | `isolated_lab_system` | `CVSS:4.0/AV:P/AC:H/AT:P/PR:H/UI:A/V...` | `CVSS-B` | 2.1 | LOW | `SYNTHETIC` |

### 3. Garantia de Proveniência e Auditoria
- **Single Source of Truth:** `data/dataset_b/source_assessments_normalized.csv`
- **Freeze Timestamp:** `2026-10-08T21:30:00Z`
- **Validação Automatizada:** Testes em `tests/test_dataset_b_consistency.py` asseguram igualdade estrita entre o CSV, relatórios, tabelas LaTeX e dados do site.
