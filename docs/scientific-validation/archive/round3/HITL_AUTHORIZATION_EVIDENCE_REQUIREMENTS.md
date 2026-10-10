# HITL authorization evidence requirements

Do not claim `SuperAdmin enforcement implemented` merely because an API response contains a review-required flag.

To close this claim, the artifact must include and test:

1. authentication middleware/session validation;
2. token issuer/audience checks when token-based identity is used;
3. verified identity/email state as applicable;
4. server-side role/permission lookup;
5. protected approval/rejection mutation endpoint;
6. negative test: unauthenticated request rejected;
7. negative test: authenticated non-authorized user rejected;
8. positive test: authorized reviewer may approve/reject;
9. reviewer identifier captured in the audit record;
10. review reason, timestamp, assessment ID, policy/ruleset/calculator versions;
11. no authorization decision based solely on client-side UI state.

If the real application already implements these controls, include the actual source paths and raw test evidence in the next artifact. If not, public wording must remain `human review required` rather than `SuperAdmin enforcement proven`.
