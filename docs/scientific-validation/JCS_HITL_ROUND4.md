# JCS and HITL release gate — Round 4

## JCS

The local implementation now recursively sorts object keys, preserves arrays, rejects non-finite numbers and rejects lone UTF-16 surrogates. This supports a **JCS-compatible** claim.

Do not state `RFC 8785 conformant` until a pinned independent conformance corpus is executed and archived. The published RFC example is a useful regression test but not a complete conformance program.

## HITL

A field such as `human_review_required=true` proves only that the API requests human review. It does not prove authorization enforcement.

To claim SuperAdmin enforcement, the artifact must include/test the real protected mutation path:

1. unauthenticated request -> rejected;
2. authenticated non-authorized user -> rejected;
3. authorized SuperAdmin -> approve/reject accepted;
4. reviewer identity, assessment ID, rationale, timestamp, policy/ruleset/calculator version persisted;
5. audit receipt generated from the canonical payload.

If these tests cannot be distributed/reproduced, use the narrower claim: **human review required; production authorization enforcement is a deployment control outside this artifact**.
