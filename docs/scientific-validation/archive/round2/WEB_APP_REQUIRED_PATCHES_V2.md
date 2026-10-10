# Web application required patches - Round 2

Target: `cvss.helpusbr.com` and its local repository.

## 1. Remove silent scientific defaults

The API must not silently fabricate a default CVE, vector, evidence quality, telemetry age, reachability class, organization-policy ID, business criticality or firewall status.

Required scientific inputs must be explicit. If evidence is missing, either return HTTP 400 for malformed input or return an abstention result; never silently create “SUFFICIENT” evidence.

Demo presets may exist only as explicitly selected UI fixtures and should be marked `demoScenario=true`/`synthetic=true` in provenance.

## 2. Remove public manual metric overrides

Do not accept arbitrary `manualOverrides` from an unauthenticated/untrusted client. Any reviewer override must be a distinct authenticated HITL action with identity, rationale, timestamp and policy authorization.

## 3. CR/IR/AR policy engine

Remove hard-coded rules such as:
- PCI/payment -> CR:H
- high business criticality -> IR:H

Instead load a versioned policy object:
- `organization_policy_id`
- `policy_version`
- explicit `securityRequirements` mapping or rules stored in that policy.

The receipt must retain policy ID/version.

## 4. RFC 8785/JCS

The previous top-level-key `JSON.stringify` approach is not JCS and may omit nested fields.

Use a tested recursive canonicalizer or a vetted RFC 8785 library. Validate against an RFC/JCS conformance corpus before labeling production receipts `RFC 8785 conformant`.

The patch package includes `patch_files/code_web/lib/jcs.ts` as a review implementation and contract examples. Treat it as a baseline that still requires formal conformance execution in the full repository.

## 5. Receipt content

The hash input should include at least:
- schema version;
- CVE/assessment ID;
- source assessment and provider provenance;
- full evidence object;
- candidate metrics;
- Environmental output or abstention;
- local operational recommendation;
- review state;
- policy/ruleset/calculator versions;
- generation timestamp.

Hash, digital signature, Merkle proof and trusted timestamp remain separate controls.

## 6. HITL authorization

Returning `humanReviewGate=true` is not authorization enforcement.

If the real product requires SuperAdmin/authorized reviewer approval, demonstrate and test:
- authenticated session;
- role/permission check;
- protected approval transition;
- immutable/tamper-evident audit event for that transition;
- rejection for unauthorized users.

Until then documentation must say `human review required`, not `SuperAdmin enforcement proven`.

## 7. UI layers

Display separately:
1. Source assessment/provenance.
2. HelpUS-derived CVSS v4.0 Environmental result.
3. Local P0-P4 operational recommendation.
4. Evidence/provenance.
5. HITL review/abstention.

Never call the HelpUS vector “official.”

## 8. Marketing/scientific copy

Remove or qualify:
- 30 validated scenarios;
- 100% correctness/agreement;
- zero hallucination;
- mathematical guarantee beyond deterministic computation;
- immutable proof;
- guaranteed regulatory compliance;
- 25%/60% “noise reduction” as a validated effectiveness claim.

Dataset B is development/regression evidence only.

## 9. PT/EN/ES smoke tests

After deployment capture screenshots or text snapshots for all languages and verify equivalent scientific caveats.
