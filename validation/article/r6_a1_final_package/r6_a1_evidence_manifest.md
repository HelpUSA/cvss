# HelpUS CVSS v4.0 R6-A1 Evidence Manifest

## 1. Executive Summary
This document forms the human-readable evidence manifest for the camera-ready research artifact package of Campaign R6-A1.

- **Package ID**: `HELPUS-CVSS-R6-A1-CAMERA-READY-PACKAGE`
- **Branch**: `research/r6-a1-schema-governance-implementation`
- **Consolidation Commit**: `716f820f162e5494f1455312eff12270763cf333`
- **Package Created UTC**: `2026-10-21T23:34:00Z`

## 2. Complete Commit Lineage
1. **R5 Historical Freeze**: `cc4418e062101f5259c15e51dc9a1bc2fd9c3e88`
2. **R6 Specification Freeze**: `090ad8b727e674aac8e95864fe7740b15092ea60`
3. **R6 Implementation Freeze**: `43664e58b4f7852d0a03c6b21ab043dec2529be9`
4. **R6.1 Taxonomy Freeze**: `bfaece26f9f718672be6b754ad83497ac7f102ea`
5. **T2R Compatibility Freeze**: `aa215569bddb2e1b341a62317cf3206d0d465a21`
6. **T3 Replay Freeze**: `c77599be1ceac1cd39d9e552eb51196cbe427f5e`
7. **T4R Primary Freeze**: `c9ba1e28811588364c56cc7111a67cbb0929b765`
8. **NF2-R Companion Freeze**: `2996e3511c73623ef152dbf610516a54cb35328c`
9. **T5-R Governance Freeze**: `6c25b757a1360b1e813b4338918ec8c91ad69d29`
10. **T6 Representability Freeze**: `8272f7dfa82d739ff09e9303acd9d12c38368cc1`
11. **R2 Differential Preregistration**: `1bbd1b6b29abd25d5e7dc5b677fee3dae28ec6cb`
12. **R2 Differential Results Freeze**: `32407259b9e8b07f84316c5057bf885ec29e8e8f`
13. **T7 Held-Out Preregistration**: `978694618574a8962e5dc8b6c0111bc792110685`
14. **T7 Held-Out Results Freeze**: `a1053b4240fad485b5dc55f7e16f0f5326e94285`
15. **Manuscript Consolidation**: `716f820f162e5494f1455312eff12270763cf333`

## 3. Frozen Scientific Results
- **Differential Validation (R2)**:
  - Numeric Endpoint (D_numeric = 461,444): 454,047 exact matches (98.3970%), 7,397 mismatches (1.6030%, all |Delta|=0.1 and 100% matching FIRST official values), 0 validity disagreements, 0 execution errors.
  - Validation Endpoint (D_validation = 25,028): 25,028 syntax rejection concordance (100.0%).
  - Deterministic rerun parity: PASS.
- **External Held-Out Transfer (T7)**:
  - N=938 eligible advisories (September 2026, GitHub Advisory Database).
  - 339 nominal-calculable (36.1407%), 599 fail-closed rejections under missing mandatory evidence (63.8593%).
  - Zero data invented; zero autonomous overrides.
  - Independent trace verifier: 938/938 traces PASS across 3,232 diagnostic checks. Deterministic parity: PASS.
- **Schema v2 and Mutations**:
  - T2R: 30/30 historical parents invalid under v2 (12 INVALID_TYPE, 18 INVALID_ENUM).
  - T3 Replay: 120/120 rejected; F3 subobject injection 16/16 rejected under v2 (vs 0/16 under v1).
  - T4R Primary: 75/90 attributable rejections across 15 canonical parents.
  - NF2-R Companion: 15/15 attributable rejections (UNKNOWN_FIELD) on root boundary.
- **Governance Override**:
  - T5-R: 8/8 fixtures PASS across INV-G1..INV-G8; Equation 8 nominal formula invariant; autonomous overrides identically zero.
  - T6: N=4 cases; 2/4 representable normatively, 2/4 requiring new evidence, zero data invented.
