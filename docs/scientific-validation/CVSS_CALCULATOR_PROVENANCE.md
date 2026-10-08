# CVSS Calculator Provenance and Validation Gate

## Backend implementation

- Package: `cvss`
- Project version reported by the local HelpUS environment: `3.6`
- API used: `cvss.CVSS4`
- Upstream project: Red Hat Product Security (`RedHatProductSecurity/cvss`)
- License: LGPL-3.0-or-later (verify against the pinned upstream release used locally)
- Normative scoring specification: FIRST CVSS v4.0
- HelpUS adapter: `core/cvss40.py`

FIRST's public CVSS resources identify the Red Hat implementation as the origin of the
reference calculator code while also warning that helper-library output must be validated
against the FIRST reference corpus.  Accordingly, HelpUS must not describe the installed
Python package merely as an independently certified "official FIRST calculator".

## Required release identifiers

Before the held-out freeze, record in the project repository:

- exact Python package version;
- package hash / wheel or lockfile hash;
- Python runtime version;
- HelpUS `core/cvss40.py` Git commit;
- FIRST specification revision;
- FIRST `cvss-resources` commit SHA used for validation;
- machine-readable reference-set validation result.

## Current validation status

The bundled 10-vector test is a **smoke/regression suite**, not a comprehensive
conformance certificate.  Two stale hand-entered expectations in the previous package were
identified and corrected (TC-FIRST-007 and TC-FIRST-008).  Comprehensive validation against
the FIRST reference corpus remains `PENDING_RELEASE_GATE` and must be completed in the
local project environment before C1/C2 execution.

## Frontend JavaScript

The review package does not contain the production `app.js`; therefore this package cannot
independently substantiate backend/frontend score equivalence.  Antigravity must run a
cross-implementation corpus test locally and record the results before making a parity claim.
