# CVSS real pipeline evidence export status - 2026-07-07

## Current status

The real pipeline gate supports an explicit local evidence export mode:

```powershell
python scripts/validate_real_pipeline.py --export-evidence
```

The default validation gate and the GitHub Actions workflow intentionally do not generate `outputs/evidence/` bundles.

## Recently validated commits

```text
6e59bde Add evidence export gate ordering contracts
1e43658 Document CI evidence export boundary
f95cd82 Add validation gate evidence export option
```

## Local validation performed in this batch

- Evidence export gate contract tests pass.
- Optional export gate path passes with `--export-evidence --skip-build`.
- The default full gate is executed before this status document is committed.

## Operational notes

- `outputs/evidence/` is ignored by Git.
- Use `--allow-findings` with evidence export only for investigation branches.
- Review `outputs/evidence/latest/manifest.json` before attaching or archiving a generated bundle.
