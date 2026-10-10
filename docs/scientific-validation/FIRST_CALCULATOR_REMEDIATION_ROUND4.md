# FIRST Calculator Remediation — Round 4

## Current fact

The previous pinned FIRST corpus run produced **159 valid-vector mismatches** (typically ±0.1) while negative cases passed. Under the project's own strict gate definition this is a **FAIL**, not a pass.

## Likely failure class

Boundary rounding/floating-point behavior is a plausible hypothesis and has been discussed publicly for the Python `cvss` implementation. This hypothesis must be tested; it must not be used to waive mismatches.

## Required remediation experiment

1. Pin:
   - FIRST `cvss-resources` commit;
   - current Python scorer package/version;
   - a FIRST reference calculator implementation/revision when available.
2. Use the exact same corpus rows for all implementations.
3. Persist every row: vector, expected, observed, delta, severity, implementation/version.
4. If the FIRST reference implementation matches corpus and Python does not:
   - adopt/pin the reference implementation as scoring kernel, **or**
   - port the exact arithmetic/rounding behavior and prove zero mismatches.
5. If both disagree with the corpus on the same rows, keep G1 open and document the upstream inconsistency.
6. Never create vector-specific exceptions or lookup-table behavior to make tests green.

## Acceptance criterion

`valid_failures == 0` and `negative_failures == 0`, or a formally documented normative upstream exception accepted before the experiment. No unexplained mismatch can be relabelled as PASS.
