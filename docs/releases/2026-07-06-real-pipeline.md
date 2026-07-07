# Real Pipeline Milestone Release Notes - 2026-07-06

## Summary

This release turns the CVSS dashboard branch into a validated real-environment security assessment pipeline. The implementation now supports importing or running Trivy scans, normalizing scanner evidence, refreshing a committed zero-findings dashboard baseline, and validating the full dashboard build path through local and CI gates.

## Highlights

- Added a Trivy-based real assessment runner.
- Added a normalized assessment schema with separated `official_cvss`, `contextual_environmental`, and `evidence` sections.
- Added a zero-findings real dashboard baseline at `web/data/real_assessment.json`.
- Added a baseline refresh helper that refuses non-zero findings by default.
- Added a consolidated local gate at `scripts/validate_real_pipeline.py`.
- Added GitHub Actions CI validation for the `real-world-cvss` branch.
- Added a CI workflow contract test to prevent accidental workflow drift.
- Documented the operational status in `docs/status/2026-07-06-real-pipeline-gate.md`.

## Validation status

Latest validated state:

- Baseline refresh: `finding_count=0`.
- Python test suite: `33 passed`.
- Static JavaScript check: `node --check app.js`.
- Whitespace check: `git diff --check`.
- Next.js production build: successful.
- Consolidated gate result: `REAL_PIPELINE_VALIDATION_OK`.

## Primary commands

Run the committed-baseline validation gate:

```powershell
python scripts/validate_real_pipeline.py
```

Run a fresh Trivy scan before refreshing evidence and dashboard baseline:

```powershell
python scripts/validate_real_pipeline.py --run-scan
```

Use investigation mode only when intentionally publishing a non-zero finding baseline:

```powershell
python scripts/validate_real_pipeline.py --run-scan --allow-findings
```

## CI behavior

The CI workflow validates committed evidence and the dashboard build path on pushes and pull requests targeting `real-world-cvss`.

CI intentionally does not run `--run-scan` by default. Fresh scan evidence remains a local pre-commit action so new findings can be reviewed before they are published into the dashboard baseline.

## Reviewer checklist

Before merging or deploying changes that affect real scan evidence:

1. Run `python scripts/validate_real_pipeline.py --run-scan` locally.
2. Review any findings before refreshing the dashboard baseline.
3. Confirm the committed baseline still reports `finding_count=0`, unless the branch is explicitly for investigation.
4. Run `python scripts/validate_real_pipeline.py`.
5. Confirm GitHub Actions passes on the pushed branch.

## Related commits

- `a7ca62d` - Add real environment Trivy assessment MVP.
- `2ac077b` - Fix web dependency vulnerabilities and add zero-findings baseline.
- `cb54439` - Optimize Trivy runner for automated scans.
- `11decef` - Expose real Trivy baseline in dashboard.
- `10b3aae` - Add real baseline refresh helper.
- `cb0dfa2` - Add real pipeline validation gate.
- `d49645f` - Add CI gate for real pipeline.
- `37fb858` - Add CI workflow contract test.
- `de010f7` - Document real pipeline gate status.
