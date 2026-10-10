# Dataset B reconciliation plan

## Current inconsistency

The latest Antigravity package contained two incompatible descriptions of Dataset B:

- `03_DATASET_B_PROVENANCE_SUMMARY.md`: 2023/2024 CVE list.
- `data/dataset_b_source_assessments_normalized.csv` and the book: 2026 CVE list.

These cannot both be the canonical Dataset B.

## Required action

1. Choose exactly one canonical `dataset_b.csv/json` under version control.
2. Generate all summaries, LaTeX tables, figures and site fixtures from that file.
3. Do not hand-maintain a second CVE list in Markdown.
4. For every real-CVE row, independently verify:
   - CVE ID;
   - affected product/version;
   - assessment provider;
   - CVSS version;
   - full source vector;
   - nomenclature (B/BT/etc.);
   - score/severity;
   - URL/source record ID;
   - publication/update/retrieval timestamps.
5. If only v3.1 is source-backed, do not silently convert it to v4.0.
6. An investigator-authored v4.0 vector must be flagged and excluded from claims about CNA/NVD-published v4.0 assessments.
7. Preserve provider-specific assessments rather than overwriting one with another.

## Machine-readable provenance fields

At minimum:
- scenario_id
- cve_id
- source_cvss_version
- source_vector_full
- source_nomenclature
- source_score
- source_severity
- metric_provider
- provider_role
- source_system
- source_record_id
- source_url
- published_at
- last_modified_at
- retrieved_at
- record_version
- base_vector_origin
- asset_class
- deployment_context
- operational_disposition
- review_required

## Release gate

No Dataset B table or Web metric should be published until `CSV == reports == book == Web fixtures` by automated test.
