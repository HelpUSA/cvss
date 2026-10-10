# Round 3 pre-freeze implementation note

This document converts the latest independent audit into executable repository changes.

## Changes supplied as drop-in files

1. `web/src/lib/jcs.ts`
   - recursive canonicalization;
   - finite-number enforcement;
   - explicit rejection of lone UTF-16 surrogates;
   - no formal RFC 8785 claim until an independent pinned corpus is executed.

2. `web/scripts/test_jcs_conformance.ts`
   - expands local contracts to include lone-surrogate rejection and hash invariance;
   - output explicitly states that local tests are not the formal conformance corpus.

3. `web/src/app/api/analyze-environment/route.ts`
   - removes direct CVSS-score-to-P0/P4 hard-coding;
   - requires an explicit versioned `operationalPolicy` to produce P0-P4;
   - without a policy, CVSS-BE can still be calculated but the operational result is `PENDING_POLICY_REVIEW`;
   - keeps fail-safe abstention and provenance hashing;
   - does not claim this route enforces authorization.

4. `web/scripts/test_analyze_route.ts`
   - adds tests for missing evidence, stale/conflicting evidence, missing operational policy, explicit versioned policy, policy mismatch, and CR/IR/AR without policy metadata.

5. `.github/workflows/real-pipeline.yml`
   - supplies the repository workflow expected by the test contracts.

6. `.gitignore`
   - ensures raw evidence exports remain uncommitted.

7. `tests/test_gitignore_contract.py`
   - preserves the repository contract while explicitly skipping the Git-only assertion in a portable ZIP that has no `.git` metadata.

8. `scripts/upgrade_dataset_b_provenance_schema.py`
   - creates a v2 provenance table without fabricating provider-reported Base scores;
   - computes the complete-vector score separately;
   - marks provider-reported Base values `PENDING_SOURCE_REAUDIT` until independently verified.

9. `scripts/validate_dataset_b_provenance_v2.py`
   - intentionally blocks release while BT provider Base fields are not independently audited.

10. `scripts/check_execution_package_consistency.py`
    - catches Dataset B cross-format drift, BT semantic conflation, JCS regressions, direct P0-P4 score mapping, status-file contradictions, and unsupported marketing claims when source snapshots are included.

## Files not supplied as authoritative replacements

- Authentication/SuperAdmin code: the latest artifact does not include enough of the authenticated application layer to safely replace it. Antigravity must patch the real repository and provide tests proving token/session validation, role authorization, protected approval mutation and audit identity.
- Full FIRST reference-corpus runner: Antigravity must pin a concrete `FIRSTdotorg/cvss-resources` revision and adapt the repository runner to the exact `vectorFiles` formats present at that revision. The local 22-case suite must remain labelled smoke/regression.
- Provider-reported Base scores: these must be re-audited from source records. The supplied migration deliberately leaves those values blank rather than guessing.
