# Results section draft

The generated scenario dataset contains 30 scenarios. Of these, 12 use real NVD CVE records with CVSS v4.0 data and curated local Environmental contexts, while 18 are explicitly marked as curated synthetic scenarios. Evidence coverage reached 100.00%, and trace completeness reached 100.00%, indicating that each scenario contains evidence fields and a corresponding trace artifact.

All 30 scenarios retain an explicit human review requirement flag as an architectural governance constraint, ensuring that candidate recommendations are treated as non-autonomous and subject to human authorization rather than an official score. This workflow constraint does not represent completed independent expert adjudication. Uncertainty flags are present in 100.00% of scenarios, reflecting intentionally conservative handling of curated local context, threat-state uncertainty, and review requirements.

Priority changed in 22 of 30 scenarios (73.33%) when moving from the Base-only view to the Environmental-aware view. Formally, priorities belong to the ordered set $\mathcal{P} = \langle \text{defer}, \text{low}, \text{medium}, \text{high}, \text{critical} \rangle$ under the ordinal mapping $g: \mathcal{P} \to \{0, 1, 2, 3, 4\}$. The Category Delta is defined as $\Delta_{\text{cat}} = g(P_{\text{env}}) - g(P_{\text{base}})$, with mean $\bar{\Delta}_{\text{cat}} = \frac{1}{30} \sum_{i=1}^{30} \Delta_{\text{cat}}^{(i)} = \frac{6.0}{30} = 0.2$, a maximum upward shift of +2.0 and a maximum downward shift of -3.0. These shifts show that the workflow can operationally differentiate vulnerability handling based on consumer-specific context while preserving the official CVSS v4.0 Base information as a separate baseline.

## Controlled Workflow Evaluation on 12 Real NVD CVEs

The controlled workflow evaluation incorporates 12 real CVE records from the National Vulnerability Database (NVD) published with official CVSS v4.0 metrics, paired with curated organizational deployment contexts. The table below details the 12 cases, reporting the official input score and nomenclature (CVSS-B or CVSS-BT), contextual score and nomenclature (CVSS-BE or CVSS-BTE), numeric score delta, and operational priority shift ($\Delta_{\text{cat}}$). This curated benchmark demonstrates operational workflow sensitivity under realistic vulnerability data rather than an independent sample of operational efficacy. Full 30-metric Base and Environmental vectors for all 12 cases are preserved in the reproducibility trace repository (alidation/article/trace/SCN-NVD-001.json through SCN-NVD-012.json) and data/article/cvss40_environmental_scenarios.csv.

| CVE ID | Input Type | Input Score | Context Type | Context Score | Score $\Delta$ | Priority Shift ($\Delta_{\text{cat}}$) |
|---|---|---:|---|---:|---:|---|
| CVE-2026-4251 | CVSS-BT | 1.1 | CVSS-BTE | 1.1 | 0.0 | low $	o$ low (0) |
| CVE-2026-4252 | CVSS-BT | 8.9 | CVSS-BTE | 8.8 | -0.1 | high $	o$ medium (-1) |
| CVE-2026-4270 | CVSS-B | 6.8 | CVSS-BE | 6.8 | 0.0 | medium $	o$ high (+1) |
| CVE-2026-28490 | CVSS-B | 8.3 | CVSS-BE | 8.3 | 0.0 | high $	o$ critical (+1) |
| CVE-2026-28498 | CVSS-B | 8.2 | CVSS-BE | 8.1 | -0.1 | high $	o$ high (0) |
| CVE-2026-29510 | CVSS-B | 5.1 | CVSS-BE | 5.1 | 0.0 | medium $	o$ low (-1) |
| CVE-2026-29513 | CVSS-B | 5.1 | CVSS-BE | 5.1 | 0.0 | medium $	o$ medium (0) |
| CVE-2026-29520 | CVSS-B | 5.1 | CVSS-BE | 5.1 | 0.0 | medium $	o$ high (+1) |
| CVE-2026-29521 | CVSS-B | 5.1 | CVSS-BE | 5.1 | 0.0 | medium $	o$ high (+1) |
| CVE-2026-3644 | CVSS-B | 6.0 | CVSS-BE | 5.9 | -0.1 | medium $	o$ low (-1) |
| CVE-2026-4224 | CVSS-B | 6.0 | CVSS-BE | 6.0 | 0.0 | medium $	o$ high (+1) |
| CVE-2026-4253 | CVSS-BT | 2.0 | CVSS-BTE | 2.0 | 0.0 | low $	o$ medium (+1) |
