# Web application Round 3 required patches

## 1. Operational policy separation

Remove direct hard-coded mapping:

`CVSS score -> P0/P1/P2/P3/P4`

from the scientific endpoint. The route replacement supplied with this package requires an explicit versioned `operationalPolicy`. Without it, return `PENDING_POLICY_REVIEW` while preserving the CVSS-BE assessment.

## 2. Canonicalization

Replace the previous canonicalizer with the supplied surrogate-safe recursive implementation. Run the expanded local contract tests, then independently validate against a pinned JCS/RFC 8785 corpus before claiming formal conformance.

## 3. HITL authorization

Do not equate `human_approval_required=true` with enforced authorization. In the actual repository, provide evidence for:

- verified authenticated session/token;
- issuer/audience verification where applicable;
- verified identity/email state;
- role/permission lookup;
- protected approval/rejection mutation;
- negative unauthorized test;
- positive authorized test;
- reviewer identity in audit receipt.

If this is not fully implemented, public copy must say only `human review required`.

## 4. Custom-domain verification

After deployment, verify `https://cvss.helpusbr.com` itself in PT/EN/ES. A temporary Vercel alias is not sufficient for G8.

Forbidden/qualify terms until independently supported:

- `30 Cenários Validados`
- `100% correctness/agreement`
- `zero hallucination`
- `guaranteed mathematical compliance`
- `immutable proof`
- `guaranteed compliance`
- development-stage `25%` presented as a validated false-positive/noise-reduction KPI.

## 5. Freshness semantics

Python, Web, tests and documentation must consume one versioned freshness policy. Do not show `300 seconds` in UI while the engine is enforcing a different 1-day/7-day policy unless those values belong to explicitly different named evidence classes.
