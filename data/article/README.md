# Dataset B status

`dataset_b_source_assessments_normalized.csv` is the current structured **development** artifact.
It fixes CVSS nomenclature/provenance fields relative to the legacy CSV, but its 12 real-CVE
rows still require authoritative source re-retrieval and a real `retrieved_at` timestamp before
experimental freeze.

Do not regenerate it by blindly copying legacy `cvss_b_score` fields. The migration helper writes
`dataset_b_source_assessments_migrated_draft.csv` and marks every row as pending audit.

`validate_dataset_b.py` checks structural invariants only. It does **not** certify that external
CVE metadata, vectors, or scores are current/correct.
