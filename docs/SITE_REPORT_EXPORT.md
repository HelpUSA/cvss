# Site report export

The static interactive MVP now supports exporting a Markdown report for a single environmental CVSS assessment.

The exported report includes scenario, asset, CVE, base score, environmental score, delta, decision, rationale, and a caveat that the report is not independent human expert validation.

This remains a browser-side static export without Next.js, npm build, backend services, login, or database state.
