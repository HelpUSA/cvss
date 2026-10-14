# Reproducibility and artifact requirements

The next returned ZIP must reproduce its own claims from a clean environment.

## Python

Include the actual repository packaging/dependencies:
- `pyproject.toml` + lockfile, or
- pinned `requirements.txt`/lock equivalent.

Tests must import the same package layout shipped in the artifact. Do not ship `code_core/` while tests import `core.*` unless the install/build step explicitly maps it.

## Node/Web

Include:
- `package.json`;
- `package-lock.json` (or the actual pinned package-manager lockfile);
- Node/npm versions;
- no machine-specific absolute paths.

Replace paths such as `<repo>/web` with repository-relative resolution.

## Raw logs

Ship raw:
- pytest log;
- Node/typecheck/unit-test log;
- backend/frontend parity results;
- calculator-corpus results;
- LaTeX build log summary;
- deployment smoke-test evidence.

## Test accounting

Report one unambiguous full-suite count, e.g.:
`pytest full collection: 119 passed`.

If subsets are included, mark them as overlapping subsets and do not visually sum them.

## Calculator corpus

Pin the exact reference-corpus revision and store machine-readable results. The 10-vector smoke suite is only regression/smoke coverage.

## Build manifest

Generate the manifest at the end of the build, never copy an older manifest. It must include:
- source Git SHA;
- toolchain versions;
- build timestamp;
- PDF SHA256/size/pages;
- Overleaf ZIP SHA256;
- dataset SHA256;
- calculator/ruleset/policy versions.
