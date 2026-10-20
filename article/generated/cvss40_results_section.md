# Results section draft

The generated scenario dataset contains 30 scenarios. Of these, 12 use real NVD CVE records with CVSS v4.0 data and curated local Environmental contexts, while 18 are explicitly marked as curated synthetic scenarios. Evidence coverage reached 100.00%, and trace completeness reached 100.00%, indicating that each scenario contains evidence fields and a corresponding trace artifact.

All 30 scenarios retain an explicit human review requirement flag as an architectural governance constraint, ensuring that AI/watcher output is treated as a candidate recommendation rather than an autonomous official score. This workflow constraint does not represent completed independent expert adjudication. Uncertainty flags are present in 100.00% of scenarios, reflecting intentionally conservative handling of curated local context, threat-state uncertainty, and review requirements.

Priority changed in 22 of 30 scenarios (73.33%) when moving from the Base-only view to the Environmental-aware view. The average priority delta was 0.2, with a maximum upward shift of 2.0 and a maximum downward shift of -3.0. These shifts show that the workflow can operationally differentiate vulnerability handling based on consumer-specific context while preserving the official CVSS v4.0 Base information as a separate baseline.
