# Confirmatory Results Template — C1/C2

> **DO NOT POPULATE BEFORE THE G10B RUN IS COMPLETE AND SEALED.**
> This file is a manuscript integration template only. It contains no
> confirmatory result and must not be used to infer or preview C1/C2.

## Confirmatory evaluation design

The frozen deterministic HelpUS CVSS v4.0 baseline was evaluated under the
pre-registered G10B single-pass blind confirmatory protocol. C1 contained the
held-out real-world cases and C2 the held-out adversarial/metamorphic cases.
HCAL and external AI providers were disabled for the primary run.

Frozen baseline commit: `[FROZEN_COMMIT]`  
Protocol ID: `[PROTOCOL_ID]`  
Run ID: `[RUN_ID]`  
C1 SHA-256: `[C1_SHA256]`  
C2 SHA-256: `[C2_SHA256]`

## C1 — Real-world confirmatory results

| Endpoint | Pre-registered threshold | Observed | 95% CI / uncertainty | Verdict |
|---|---:|---:|---:|---|
| Metric-level exact agreement | >= 0.95 | [TBD] | [TBD] | [TBD] |
| Full-vector exact agreement | >= 0.90 | [TBD] | [TBD] | [TBD] |
| MAE (CVSS points) | <= 0.25 | [TBD] | [TBD] | [TBD] |
| Maximum absolute error | <= 1.0 | [TBD] | n/a | [TBD] |
| Severity-band agreement | >= 0.95 | [TBD] | [TBD] | [TBD] |
| Forced-guess rate where abstention required | 0 | [TBD] | n/a | [TBD] |
| FIRST-engine arithmetic divergence | 0 | [TBD] | n/a | [TBD] |

Additional descriptive statistics: median absolute error, 95th percentile
absolute error, per-metric confusion counts, abstention rate, and abstention
reason distribution.

## C2 — Adversarial/metamorphic confirmatory results

| Endpoint | Pre-registered threshold | Observed | Verdict |
|---|---:|---:|---|
| Metamorphic invariant violations | 0 | [TBD] | [TBD] |
| State/order leakage violations | 0 | [TBD] | [TBD] |
| Unexpected exceptions/crashes | 0 | [TBD] | [TBD] |
| Forced guesses where abstention required | 0 | [TBD] | [TBD] |
| Deterministic reproducibility failures | 0 | [TBD] | [TBD] |

## Overall confirmatory verdict

`[CONFIRMATORY_PASS | CONFIRMATORY_FAIL | CONFIRMATORY_INVALIDATED | CONFIRMATORY_INCONCLUSIVE]`

The verdict above must be copied from the immutable G10B execution evidence
manifest and must not be manually recomputed for presentation purposes.

## Claim boundary

C1/C2 results validate only the frozen deterministic baseline tested in the
recorded run. They do not constitute FIRST certification or endorsement.
HCAL, if evaluated later, must be reported separately as a secondary post-hoc
analysis and cannot alter the primary deterministic confirmatory result.
