# Real Evidence Refresh Checklist

Use this checklist when refreshing real Trivy scan evidence and updating the committed dashboard baseline.

## Scope

This applies to the `real-world-cvss` branch and the real pipeline artifacts:

- `outputs/scans/trivy_latest.json`
- `outputs/assessments/latest_assessment.json`
- `web/data/real_assessment.json`

## Pre-refresh checks

- Confirm the working tree is clean or unrelated changes are intentionally isolated.
- Confirm dependency changes have already been reviewed.
- Confirm the branch is intended for real scan evidence updates.
- Confirm Trivy  is installed locally or discoverable by the runner.

## Refresh evidence

Run the fresh scan gate:


```powershell
python scripts/validate_real_pipeline.py --run-scan
```

The command should:

- run Trivy vulnerability scanning;
- refresh raw scanner evidence;
- normalize scanner results into the assessment schema;
- refresh the dashboard baseline only when the normalized baseline has zero findings;
- run the full local validation gate.

## If findings appear

Do not publish a non-zero dashboard baseline by default.

For each finding, record:

- package or component;
- installed version;
- fixed version when available;
- CVE or advisory identifier;
- official CVSS source;
- contextual environment notes;
- remediation decision;
- owner or reviewer.

## Safe remediation path

1. Patch or upgrade the affected dependency.
2. Reinstall dependencies if needed.
3. Re-run `python scripts/validate_real_pipeline.py --run-scan`.
4. Confirm `finding_count=0`.
5. Review diffs in scanner output, normalized assessment output, and dashboard baseline.
6. Commit only after the consolidated gate passes.

## Investigation-only path

Use investigation mode only when intentionally exposing current findings in the dashboard for analysis:

```powershell
python scripts/validate_real_pipeline.py --run-scan --allow-findings
```

Before committing investigation output, confirm:

- the branch is not treated as a clean release baseline;
- release notes or status docs clearly identify the baseline as non-zero;
- stakeholders understand the findings are intentionally visible.

## Reviewer sign-off

Before merge or deployment, verify:

- `python scripts/validate_real_pipeline.py` passes;
- `web/data/real_assessment.json` reports `finding_count=0`, unless explicitly marked as investigation;
- scanner evidence and contextual prioritization remain separate;
- GitHub Actions passes on the pushed branch;
- release notes or status docs are updated when the pipeline behavior changes.

## Expected clean baseline


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
## Export review bundle

After the consolidated gate passes, export a review bundle for audit or handoff:

```powershell
python scripts/export_real_evidence.py --output-dir outputs/evidence/latest
```

Review `outputs/evidence/latest/manifest.json` before attaching or archiving the bundle.
