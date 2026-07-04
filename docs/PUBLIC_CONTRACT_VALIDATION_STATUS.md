# CVSS Public Contract Validation Status

Date: 2026-07-04

## Result

Status: complete.

The public static CVSS dashboard has been deployed and validated at:

- https://cvss.helpusbr.com

## Contract validated

The public HTML and app bundle expose the current layered contract:

- official_cvss
- contextual_environmental
- evidence
- a caveat that contextual prioritization is not official CVSS

The public production check also confirms that unrelated or obsolete content is not being served:

- CVSS Environmental Dashboard: absent from public HTML and app bundle
- HairStyle Studio: absent from public HTML and app bundle

## Final public marker counts

HTML counts:

- Official CVSS + Contextual Prioritization Dashboard: 2
- official_cvss: 3
- contextual_environmental: 1
- evidence: 1
- not official CVSS: 1
- CVSS Environmental Dashboard: 0
- HairStyle Studio: 0

app.js counts:

- official_cvss: 14
- contextual_environmental: 7
- evidence: 18
- not official CVSS: 2
- CVSS Environmental Dashboard: 0
- HairStyle Studio: 0

## Local validation

The following local checks passed before this status document was committed:

- python -m pytest -q
- node --check app.js
- git diff --check

## Notes

The public dashboard contract is intentionally separated from the older research-prototype terminology. Internal research files may still refer to CVSS Environmental assessment, but the public static dashboard and exports must distinguish official CVSS from contextual prioritization.
