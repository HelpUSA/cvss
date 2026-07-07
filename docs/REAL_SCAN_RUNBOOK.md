# Real CVSS scan runbook

This runbook explains how to generate and validate the real Trivy baseline used by the dashboard.

## Purpose

The real assessment flow imports scanner evidence from Trivy and keeps the CVSS layers separate:

- `official_cvss`: score and severity reported by scanner sources.
- `contextual_environmental`: local prioritization based on asset context.
- `evidence`: scanner metadata, package, installed version, fixed version, and source file.

The contextual score is a prioritization aid only. It is not official CVSS.

## Prerequisites

Install Trivy and make it available on `PATH, or install it through WinGet. The runner also searches common WinGet package folders when `trivy` is not directly available on `PATH.

Windows example:

```powershell
winget install --id AquaSecurity.Trivy --source winget --accept-package-agreements --accept-source-agreements
```

## Default command

From the repository root:

```powershell
python tools/run_real_assessment.py --scanner trivy --target .
```

By default, the runner writes:

- raw Trivy JSON to `outputs/scans/trivy_latest.json`
- normalized assessment JSON to `outputs/assessments/latest_assessment.json`

## Faster recurring scan

For routine automation, use vulnerability scanning only and skip generated or heavy folders:

```powershell
python tools/run_real_assessment.py --scanner trivy --target . --trivy-scanners vuln --trivy-skip-dirs .git,.venv,web/.next,web/node_modules --raw-output outputs/scans/trivy_latest.json --output outputs/assessments/latest_assessment.json
```

## Dashboard baseline

The dashboard reads a committed copy of the latest normalized baseline from:

```text
web/data/real_assessment.json
```

After refreshing `outputs/assessments/latest_assessment.json`, copy the result into `web/data/real_assessment.json` before building or deploying the web app.

## Success criteria

A clean baseline should satisfy all of the following:

```powershell
python -m pytest -q
node --check app.js
cd web
npm run build
```

The normalized assessment should report:

```json
{
  "summary": {
    "finding_count": 0,
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0
  }
}
```

## When findings appear

1. Confirm the finding is from a committed dependency or source artifact, not a generated folder.
2. Update or patch the affected dependency when safe.
3. Re-run the real assessment.
4. Keep scanner evidence and contextual prioritization separate.
5. Commit the refreshed `outputs/assessments/latest_assessment.json` and `web/data/real_assessment.json` only after validation passes.

## Full local validation gate

After changing the real scan pipeline, run the consolidated validator:

```powershell
python scripts/validate_real_pipeline.py
```

The validator compiles the Python tooling, refreshes `web/data/real_assessment.json`, runs the Python test suite, checks `app.js`, verifies whitespace with `git diff --check`, and builds the web dashboard.

For a fresh Trivy scan before refreshing the dashboard baseline:

```powershell
python scripts/validate_real_pipeline.py --run-scan
```

By default, the refresh step refuses to publish a non-zero finding baseline. Use `--allow-findings` only for investigation branches where exposing current findings in the dashboard is intentional.

## CI validation gate

The repository includes `.github/workflows/real-pipeline.yml` to run the real pipeline gate on pushes and pull requests targeting `real-world-cvss`.

The workflow installs Python and Node dependencies, then runs:

```powershell
python scripts/validate_real_pipeline.py
```

The CI job intentionally does not run a fresh Trivy scan by default. It validates the committed zero-findings baseline and the dashboard build path. Use the local `--run-scan` mode when you need to refresh scan evidence before committing.

## CI workflow contract test

The CI workflow contract is covered by:

```powershell
python -m pytest tests/test_ci_workflow_contract.py -q
```

This test protects the workflow from accidentally dropping the `real-world-cvss` branch gate, dependency install steps, or the consolidated validator command.
## Manual evidence refresh checklist

Reviewer-facing evidence refresh steps are maintained in:

```text
docs/checklists/real-evidence-refresh.md
```

Use that checklist before committing refreshed Trivy evidence or dashboard baseline changes.
