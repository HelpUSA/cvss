# Data source plan for real-world CVSS

## Required data sources

- CVE identifiers.
- Official or trusted CVSS vectors.
- Advisory/source URL.
- Affected asset type.
- Exposure context.
- Control context.
- Business criticality.

## Candidate source categories

- NVD records.
- Vendor advisories.
- CISA KEV where relevant.
- Internal scanner exports.
- Manual security review evidence.

## Repository rule

Raw source data and derived scenario artifacts must be separated. Derived artifacts should be reproducible from source evidence when possible.
