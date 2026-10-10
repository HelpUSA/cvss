# G1 - FIRST CVSS v4.0 reference-corpus gate

## Required source

Pin a specific commit of `FIRSTdotorg/cvss-resources`. The repository README identifies `vectorFiles` as test-vector sets for CVSS v4.0 calculator validation and warns that helper-library accuracy is not guaranteed without validation.

Record:

- repository URL;
- commit SHA;
- checkout timestamp;
- exact vector files consumed;
- parser version/hash;
- calculator implementation/version/commit;
- execution command.

## Required execution

1. Execute all applicable valid vector records in the pinned corpus.
2. Execute negative/invalid cases supplied by the pinned resources, if present.
3. Do not silently skip parser failures.
4. Store one machine-readable row per test:
   - test/source file;
   - vector;
   - expected score or expected rejection;
   - observed score/rejection;
   - absolute delta;
   - PASS/FAIL;
   - error text.
5. Produce a summary from the raw rows; do not hand-edit the pass count.

## Release criterion

G1 passes only when there are zero unexplained mismatches across the complete applicable pinned corpus. Any intentionally excluded file/category must be listed with a technical rationale.

The current 22-case suite remains a smoke/regression suite and must never be relabelled as the full FIRST corpus.
