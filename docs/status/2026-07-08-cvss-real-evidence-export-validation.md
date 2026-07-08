# CVSS real evidence export validation

Date: 2026-07-08
Branch: real-world-cvss

## Scope

This status note closes the real evidence export hardening cycle for the CVSS dashboard branch.

The validated surface includes:

- optional local evidence export through `python scripts/validate_real_pipeline.py --export-evidence`;
- export helper JSON validation, CLI defaults, custom CLI inputs, and non-zero finding guardrails;
- manifest metadata contracts for `schema`, `schema_version`, UTC `generated_at`, `finding_count`, copied `files`, `source_paths`, `scan_summary`, and `assessment_summary`;
- operational checklist coverage for reviewing `outputs/evidence/latest/manifest.json`;
- CI boundary coverage so local evidence bundles are not exported as public CI artifacts by default.

## Final validation command

```bash
python scripts/validate_real_pipeline.py --export-evidence
```

This command is expected to run the full local gate, including Python compilation, baseline refresh, pytest, `node --check`, `git diff --check`, the Next.js build, and the final evidence export step.

## Bundle review expectations

After the full gate succeeds, review:

```text
outputs/evidence/latest/manifest.json
```

The bundle should remain local-only and ignored by Git through the existing `outputs/evidence/` ignore boundary. The manifest must point to copied files inside the bundle and preserve the original input paths for auditability.

## CI boundary

The public CI workflow must continue to validate the real pipeline without publishing `outputs/evidence/` as a workflow artifact. Evidence export is an explicit local/review operation unless a future change deliberately introduces a reviewed artifact policy.
