# Documentation archive and status policy — Round 4

## One current status

Only `CURRENT_RELEASE_GATE_STATUS.md` may be treated as the present gate state.

## Archive older rounds

Move superseded files that contain old gate decisions/status claims to:

- `archive/round1/`
- `archive/round2/`
- `archive/round3/`

Historical documents may be retained for provenance, but add a banner:

> ARCHIVED — superseded. Do not use as current release-gate status.

## Expert panel

Use **n=5 independent experts** consistently throughout the current protocol package. If changed, amend all current documents before any held-out result is observed.

## Generated status

Build manifests, calculator reports, dataset summaries and test reports should be generated from machine-readable evidence where practical. Never keep a stale manual PASS when the raw result says FAIL.
