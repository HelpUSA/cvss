# Portable artifact profile

The project must distinguish two reproducibility targets.

## A. Repository-full profile

Runs inside a real Git checkout and may validate:

- `.gitignore` behavior;
- GitHub Actions workflow contracts;
- full application/auth/database integration;
- production build paths.

## B. Portable-ZIP profile

Runs after extracting a release artifact to a clean directory with no `.git` metadata and no machine-specific paths.

The portable package must include:

- Python dependency declaration/lock strategy;
- Node package lock;
- actual importable package layout;
- all files required by portable tests;
- documented setup commands;
- raw test logs generated from the clean extraction.

Repository-only tests must either:

- have the required repository artifact included; or
- explicitly skip with a documented reason in the portable profile.

Do not claim that a ZIP independently reproduces `N/N passed` when the published ZIP cannot execute those tests from a clean extraction.
