# Official and contextual CVSS integration plan

## Principle

Official CVSS output and contextual operational prioritization must remain separate objects. The official_cvss object is produced from the CVSS vector. The contextual_environmental object may use business and infrastructure evidence, but it must not be labeled as official CVSS unless the official environmental formula is implemented.

## Output contract

- official_cvss: version, vector, base_score, base_severity, temporal_score, environmental_score, subscores.
- contextual_environmental: contextual_score, contextual_severity, decision, delta_from_official_base, trace.
- evidence: CVE, source URLs, asset, environment, business context, control context.

## Next implementation

Add a wrapper that accepts a finding row with cvss_vector and contextual fields, emits both official_cvss and contextual_environmental, and preserves traceability.
