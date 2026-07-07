# Real Pipeline Gate Status - 2026-07-06

## Branch

real-world-cvss

## Implemented controls

- Real Trivy assessment MVP with normalized output.
- Zero-findings dashboard baseline at web/data/real_assessment.json.
- Baseline refresh helper with non-zero finding protection.
- Consolidated local validation gate at scripts/validate_real_pipeline.py.
- GitHub Actions CI gate at .github/workflows/real-pipeline.yml.
- CI workflow contract test at tests/test_ci_workflow_contract.py.

## Current validation command

powershell
python scripts/validate_real_pipeline.py


The gate performs:

- Python tool compilation.
- Real baseline refresh.
- Full Python test suite.
- node --check app.js.
- git diff --check.
- Next.js production build.

## Fresh scan command

powershell
python scripts/validate_real_pipeline.py --run-scan


Use this before committing refreshed scan evidence. The refresh step refuses to publish a non-zero finding baseline unless --allow-findings is explicitly provided for investigation work.

## Latest local validation

- Baseline refresh: finding_count=0.
- Test suite: 33 passed.
- Web build: successful.
- Gate result: REAL_PIPELINE_VALIDATION_OK.

## Recent commits

- cb0dfa2 - Add real pipeline validation gate.
- d49645f - Add CI gate for real pipeline.
- 37fb858 - Add CI workflow contract test.

## Operational notes

The CI workflow validates the committed zero-findings baseline and build path. It intentionally does not run a fresh Trivy scan by default. Fresh scan evidence remains a local pre-commit action so findings can be reviewed before publishing dashboard baseline changes.

## Suggested next controls

- Add release notes for the real pipeline milestone.
- Add a manual evidence refresh checklist for reviewers.
- Add optional artifact upload for manual scan runs if CI-based scan evidence is later desired.
