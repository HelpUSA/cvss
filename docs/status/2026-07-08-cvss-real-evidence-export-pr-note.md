# PR note: real evidence export hardening

## Summary

This change set adds and hardens an optional local evidence export path for the real CVSS pipeline.

Highlights:

- Adds `--export-evidence` to the real pipeline validation gate.
- Exports a local review bundle under `outputs/evidence/latest/`.
- Preserves CI safety by keeping evidence export out of the default public workflow.
- Adds contract tests for gate ordering, export helper edge cases, JSON validation, CLI defaults/custom inputs, and manifest metadata.
- Documents the manifest review contract in the runbook and checklist.

## Validation

Use this command for final local verification:

```bash
python scripts/validate_real_pipeline.py --export-evidence
```

Expected coverage:

- Python compilation
- real baseline refresh
- full pytest suite
- JavaScript syntax check
- whitespace check via `git diff --check`
- Next.js build
- local evidence export
- manifest/bundle inspection

## Reviewer notes

The exported bundle is intentionally local and ignored by Git. Reviewers should inspect `outputs/evidence/latest/manifest.json` and confirm that the copied evidence files match the `files` map and that `source_paths` point back to the expected real scan, assessment, and dashboard baseline inputs.
