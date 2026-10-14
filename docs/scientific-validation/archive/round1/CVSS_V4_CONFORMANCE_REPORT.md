# CVSS v4.0 Calculator Validation Status

## Status

The earlier package incorrectly described a hand-curated 10-vector suite as a complete
FIRST conformance test and contained two stale expected values.  This revision corrects
those two smoke-test oracles and explicitly narrows the claim.

### Corrected smoke/regression suite

- TC-SMOKE-007 (`CR:H/IR:H/AR:H` on the 9.3 reference Base vector): expected **9.3 / Critical**.
- TC-SMOKE-008 (`MAV:A/MAC:H/MPR:H` on the same Base vector): expected **7.3 / High**.
- The local project should regenerate `conformance_results.json` from the test file; no
  JSON result copied from the previous 8/10 run should be treated as current evidence.

The 10-vector suite is useful for regression detection only.  It is **not sufficient** to
claim comprehensive calculator conformance.

## Publication-grade validation required before experimental freeze

FIRST's CVSS SIG publishes `FIRSTdotorg/cvss-resources`, including `vectorFiles` reference
data comprising roughly fifty thousand valid full metric strings plus negative tests.  The
FIRST FAQ explicitly recommends this reference set for validating calculator implementations.

Before the final engine/protocol freeze, Antigravity must:

1. obtain a pinned revision of `FIRSTdotorg/cvss-resources`;
2. record repository URL, commit SHA and hashes of the input reference files;
3. run the Python `cvss` implementation used by HelpUS against the complete applicable
   reference set and negative tests;
4. generate machine-readable results and this Markdown report automatically;
5. report observed pass/fail counts and maximum score delta without manual editing;
6. block the experimental release if any unexplained scoring discrepancy remains.

Recommended wording until that run exists:

> The HelpUS backend uses the Red Hat Product Security `cvss` Python package and has passed
> a selected smoke/regression suite. Comprehensive validation against the FIRST CVSS v4.0
> reference corpus is pending and is a release gate for the held-out experiment.

Authoritative resources:
- https://github.com/FIRSTdotorg/cvss-resources
- https://www.first.org/cvss/v4.0/faq
- https://www.first.org/cvss/v4.0/specification-document
- https://www.first.org/cvss/v4.0/implementation-guide
