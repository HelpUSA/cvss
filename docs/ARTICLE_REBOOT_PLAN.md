#
# Article Reboot Plan

## Decision

`article/` is the canonical manuscript directory. Legacy IEEE drafts, root ZIP files, backup `.tex.bak_*` files, and obsolete helper scripts have been moved under `_archive/`.

## Scientific direction

The article continues the prior study on the difficulty of CVSS Environmental assessment. The new contribution is a watcher-enabled evidence pipeline that turns contextual scoring into a reproducible and auditable workflow.

## Experimental comparison

1. Historical human baseline from the prior study.
2. Deterministic rule-based baseline.
3. Language-model baseline without local tool access.
4. AI Bridge watcher workflow with local evidence access and multi-agent review.

## Main metrics

- CR/IR/AR exact match.
- Modified metric exact match, especially MAV.
- Environmental score error.
- Correct before-after effect direction.
- Reproducibility across repeated runs.
- Evidence coverage.
- Audit-trace completeness.

## Blocking issue

Existing demonstration outputs must be regenerated from clean run manifests before final results are claimed, because previous output files may reflect mixed runs.
