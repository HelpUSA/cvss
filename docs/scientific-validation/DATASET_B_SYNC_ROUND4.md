# Dataset B synchronization — Round 4

## Canonical source

`data/dataset_b/source_assessments_v2.csv`

Dataset B is **development/regression only**.

## Required semantics

Keep these concepts distinct:

- provider-reported Base score/severity;
- source vector;
- source nomenclature (`CVSS-B`, `CVSS-BT`, etc.);
- locally recomputed score/severity for the complete source vector;
- local operational disposition P0–P4.

For explicit Threat metric vectors, a B+T score must not be presented as though it were the provider's pure Base score.

## Generation rule

The following artifacts must be generated from the same canonical source:

- provenance Markdown;
- book Appendix C tables;
- Chapter 6 development distribution;
- Web development fixture;
- scenario/CVE ID lists;
- any descriptive counts.

No manually maintained parallel list of Dataset B CVEs is permitted.

## Required checks

- 30 scenario IDs unique;
- 12 real-CVE development contexts + 18 synthetic fixtures, if that composition is retained;
- every BT source row has audited provider Base fields and full-vector recomputation fields;
- Web/book/report scenario IDs match the canonical CSV exactly;
- no site demo labelled Dataset B may use a CVE absent from canonical Dataset B.

## Final canonical score view — only after G1

Do not overwrite legacy provenance fields to make vectors/scores appear consistent. After G1 reaches strict PASS, run `scripts/finalize_dataset_b_after_g1.py`. It creates a final view with `canonical_source_score` / `canonical_source_severity` derived from the complete source vector while retaining the original provider/legacy fields for auditability.
