# Dataset B provenance schema v2

## Problem being corrected

For CVSS-BT rows, a score recomputed from the complete source vector must not be presented as though it were necessarily the provider's published **Base-only** score. CVSS nomenclature communicates which metric groups were explicitly used.

## Required fields

Keep the source vector and nomenclature, but separate provider facts from local recomputation:

- `source_cvss_v4_vector`
- `source_nomenclature` (`CVSS-B`, `CVSS-BT`, `CVSS-BE`, `CVSS-BTE`)
- `metric_provider`
- `provider_role`
- `source_system`
- `source_record_id`
- `source_url`
- `published_at`
- `last_modified_at`
- `retrieved_at`
- `base_vector_origin`

Provider-reported fields:

- `provider_reported_base_score`
- `provider_reported_base_severity`
- `provider_reported_score_audit_status`

Local computed fields:

- `recomputed_full_vector_score`
- `recomputed_full_vector_severity`
- `score_semantics`

## Rules

1. Do not infer a provider Base score from a complete BT vector.
2. Do not populate provider-reported fields until the source record has been re-audited.
3. A BT source may legitimately have a different complete-vector B+T score from its Base-only score.
4. Book tables and Web source panels must label vector nomenclature explicitly.
5. Dataset B remains development-only regardless of provenance quality.
