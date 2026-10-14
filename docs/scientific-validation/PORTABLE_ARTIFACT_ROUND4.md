# Portable Artifact Requirements — Round 4

A review ZIP is not reproducible merely because tests passed in the developer's checkout.

## Repository-full profile

Executed in the real Git checkout. May test Git metadata, CI files and repository-only behavior.

## Portable-artifact profile

Executed after extracting the distributed ZIP in a clean directory. It must contain/install everything required for the scientific test profile.

Minimum contents:

- `core/`
- `app/` (if tests import it)
- `tests/`
- `scripts/`
- `data/dataset_b/`
- `docs/scientific-validation/`
- `.github/workflows/real-pipeline.yml`
- `.gitignore`
- `requirements.txt`
- `pyproject.toml`
- `pytest.ini`
- `web/package.json`
- `web/package-lock.json`
- `web/src/`
- `web/scripts/`
- pinned FIRST fixtures, or a deterministic fetch script that verifies repository URL + commit SHA before tests.

## Report format

Report separately:

- repository-full: passed / failed / skipped;
- portable-artifact: passed / failed / skipped.

A repository-only test that is skipped in the ZIP must be reported as SKIP, never silently counted as PASS.
