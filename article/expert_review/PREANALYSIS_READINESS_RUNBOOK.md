# Expert-review pre-analysis readiness gate

## Purpose

The pre-analysis gate prevents expert-review analysis and adjudication from
starting before all independent responses are valid, preserved, and
cryptographically locked.

## Gate requirements

Analysis is eligible for release only when:

1. every planned reviewer has exactly one active locked response;
2. reviewer and packet assignments match;
3. every locked response has exactly 30 scenario rows;
4. every stored validation report passed;
5. every locked response passes strict revalidation;
6. original and locked file hashes match the registry;
7. no reviewer has multiple active locked responses;
8. the response set contains every planned reviewer;
9. the local answer key matches its versioned SHA-256 commitment;
10. no structural error is present.

## Readiness check

Run:

`python -X utf8 tools/check_expert_review_preanalysis_readiness.py`

The command is expected to succeed while responses are still missing. Its
machine-readable local report identifies the missing reviewer locks.

The local report is stored at:

`article/expert_review/private/preanalysis/preanalysis_readiness_report.json`

## Strict readiness requirement

To require a complete response set, run:

`python -X utf8 tools/check_expert_review_preanalysis_readiness.py --require-ready`

This command returns a nonzero status until every gate requirement passes.

## Analysis release

After manually reviewing the complete readiness report, create the local release
token with:

`python -X utf8 tools/check_expert_review_preanalysis_readiness.py --require-ready --write-release`

The local release token is stored at:

`article/expert_review/private/preanalysis/analysis_release.json`

The token contains:

- the required and locked response counts;
- the reviewer-code set;
- a SHA-256 commitment for the complete response set;
- the verified answer-key SHA-256 value;
- the analysis release scope.

## Answer-key boundary

The readiness gate hashes the answer-key bytes to verify the existing commitment.
It does not parse the answer-key CSV or compare reviewer decisions with watcher
decisions.

Semantic answer-key access remains prohibited until the local release token is
created.

## Privacy boundary

The following remain local and ignored by Git:

- reviewer responses;
- original and locked copies;
- response validation reports;
- response hashes;
- readiness reports;
- analysis release tokens;
- reviewer registries;
- answer-key content.

## Current expected state

Before real reviewer responses are collected, the gate should report:

- status: `waiting_for_locked_responses`;
- locked response count: `0`;
- ready for analysis: `False`;
- structural error count: `0`.

This expected waiting state is not a failure.
