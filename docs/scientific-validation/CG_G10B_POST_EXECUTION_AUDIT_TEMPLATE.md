# CG-G10B-AUDIT-TEMPLATE
## Independent Post-Execution Confirmatory Audit

**Template status:** EMPTY / DO NOT PREPOPULATE WITH RESULTS  
**Protocol:** `HELPUS-G10B-CONFIRMATORY-RUN-v1.0`  
**Frozen baseline:** `[FROZEN_BASELINE_COMMIT]`  
**Run ID:** `[RUN_ID]`  
**Auditor:** ChatGPT / independent governance review

## 1. Authorization and custody

- Master authorization record hash: `[SHA256]`
- Authorized by: `[EXPECTED: wmsjp]`
- Authorization timestamp: `[UTC]`
- Protocol SHA-256: `[SHA256]`
- Executor SHA-256: `[SHA256]`
- Dependency-lock SHA-256: `[SHA256]`
- C1 expected SHA-256: `[SHA256]`
- C1 observed SHA-256: `[SHA256]`
- C2 expected SHA-256: `[SHA256]`
- C2 observed SHA-256: `[SHA256]`
- Integrity verdict: `[PASS/FAIL]`

## 2. Environment and freeze checks

- Frozen baseline exact match: `[PASS/FAIL]`
- Working tree clean: `[PASS/FAIL]`
- Network isolation evidence: `[PASS/FAIL + evidence reference]`
- HCAL disabled: `[PASS/FAIL]`
- External provider calls observed: `[0 expected]`
- Rule/scoring changes after authorization: `[0 expected]`
- Case-level disclosure before both datasets completed: `[NO expected]`

## 3. C1 primary endpoints

| Endpoint | Threshold | Observed | 95% CI / uncertainty | Verdict |
|---|---:|---:|---:|---|
| Metric-level exact agreement | >= 0.95 | [TBD] | [TBD] | [TBD] |
| Full-vector exact agreement | >= 0.90 | [TBD] | [TBD] | [TBD] |
| MAE | <= 0.25 | [TBD] | [TBD] | [TBD] |
| Maximum absolute error | <= 1.0 | [TBD] | n/a | [TBD] |
| Severity-band agreement | >= 0.95 | [TBD] | [TBD] | [TBD] |
| Forced guesses where abstention required | 0 | [TBD] | n/a | [TBD] |
| Canonical scoring arithmetic divergence | 0 | [TBD] | n/a | [TBD] |

## 4. C2 zero-tolerance endpoints

| Endpoint | Threshold | Observed | Verdict |
|---|---:|---:|---|
| Metamorphic invariant violations | 0 | [TBD] | [TBD] |
| State/order leakage violations | 0 | [TBD] | [TBD] |
| Unexpected exceptions/crashes | 0 | [TBD] | [TBD] |
| Forced guesses where abstention required | 0 | [TBD] | [TBD] |
| Deterministic reproducibility failures | 0 | [TBD] | [TBD] |

## 5. Evidence integrity

- Raw C1 output hash: `[SHA256]`
- Raw C2 output hash: `[SHA256]`
- Summary metrics hash: `[SHA256]`
- Evidence manifest hash: `[SHA256]`
- Total C1 records presented to runner: `[N]`
- Total C2 records presented to runner: `[N]`
- Incomplete/omitted cases: `[N]`
- Exceptions: `[N + references]`

## 6. Audit findings

### Blocking findings
`[NONE or findings]`

### Non-blocking findings
`[NONE or findings]`

### Claim-boundary findings
`[NONE or findings]`

## 7. Final independent verdict

One of:

- `CONFIRMATORY_PASS`
- `CONFIRMATORY_FAIL`
- `CONFIRMATORY_INVALIDATED`
- `CONFIRMATORY_INCONCLUSIVE` only under the pre-defined non-scientific invalidity rules

**Independent audit verdict:** `[TBD]`

## 8. Post-exposure rule

If C1/C2 have been exposed, they must not be used for retuning while retaining
confirmatory status. Any later retuning requires a new independent held-out
dataset for a new confirmatory claim.
