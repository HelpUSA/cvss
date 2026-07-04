# Official CVSS + Contextual Prioritization Dashboard

Cloud prototype and research artifact for separating official CVSS v3.1 scoring from contextual operational prioritization.

The public static dashboard is available at:

- https://cvss.helpusbr.com

## Contract

The project keeps two layers separate:

- official_cvss: the official CVSS v3.1 base score and base severity.
- contextual_environmental: operational/contextual prioritization derived from local evidence. This is not official CVSS.
- evidence: scenario, asset, vulnerability, and local-context details used to explain the contextual prioritization result.

Legacy flat fields may still exist in the static UI for MVP compatibility, but exports should expose the layered contract above.

## Static dashboard

The static site is intentionally simple:

- index.html provides the dashboard shell and contract caveat.
- app.js computes the example output and exports JSON, CSV, Markdown, and pipeline JSON.
- STATIC_DEPLOYMENT.md documents static deployment markers and validation checks.

Expected public markers include:

- Official CVSS + Contextual Prioritization Dashboard
- official_cvss
- contextual_environmental
- evidence
- a caveat that contextual prioritization is not official CVSS

## Local validation

Run:

bash
python -m pytest -q
node --check app.js


The current validated branch is real-world-cvss.

## Deployment

The Vercel project is cvss under the help-us team. Production is aliased to:

- https://cvss.helpusbr.com

A production deploy from this static repository can be performed with:

bash
vercel --prod --yes


After deployment, validate that the production HTML and /app.js contain the layered contract markers and do not serve unrelated or older project content.

## Research prototype notes

Some internal Python modules, article files, and agent prompts still refer to CVSS Environmental assessment because they document the underlying research prototype. The public dashboard contract, however, must clearly distinguish official CVSS output from contextual prioritization.
