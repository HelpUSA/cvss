# Gated expert-review analysis runbook

## Purpose

The Phase 15 engine calculates expert-review statistics only after the Phase 14
local analysis-release token exists.

## Blocked-state verification

Before all independent responses are locked, run:

`python -X utf8 tools/run_expert_review_gated_analysis.py --check-blocked`

The expected result is:

- release token absent;
- analysis blocked;
- answer key not semantically opened;
- no analysis output generated.

## Release validation

After all Phase 14 gates pass, run:

`python -X utf8 tools/run_expert_review_gated_analysis.py --validate-release`

This revalidates:

- the complete reviewer set;
- one locked response per reviewer;
- original and locked file hashes;
- stored validation reports;
- strict reviewer-response validation;
- the response-set commitment;
- the answer-key commitment.

## Analysis command

Only after release validation:

`python -X utf8 tools/run_expert_review_gated_analysis.py`

## Private outputs

The following remain local and ignored by Git:

- `article/expert_review/private/analysis/expert_review_analysis.json`
- `article/expert_review/private/analysis/expert_review_scenario_summary.csv`
- `article/expert_review/private/analysis/analysis_run_manifest.json`

## Measures

The engine calculates:

- completion and defer rates;
- exact Environmental-vector unanimity;
- operational-priority unanimity;
- Fleiss' kappa;
- pairwise Cohen's kappa;
- watcher/reviewer match rates;
- evidence-sufficiency summaries;
- confidence summaries;
- review-duration summaries.

Agreement does not establish correctness, and watcher agreement is not an
official CVSS validation.
