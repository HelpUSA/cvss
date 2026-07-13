# Reviewer response intake rules

## Storage

Returned files must be placed in:

`article/expert_review/reviewer_responses/`

This directory is intentionally ignored by Git.

## File naming

Use:

`reviewer_RXX_responses.csv`

Example:

`reviewer_R01_responses.csv`

## Required structural checks

Every response file must:

- contain exactly 30 scenario rows;
- use the assigned reviewer code;
- use the assigned packet version;
- preserve the assigned presentation order;
- contain no duplicate scenario IDs;
- use evidence-sufficiency and confidence values from 1 to 5;
- use a permitted decision status;
- contain a reviewed vector and priority when status is `complete`;
- explain missing evidence or ambiguity when deferred.

## Validation command

Run:

`python -X utf8 tools/validate_expert_reviewer_response.py <response-file>`

A machine-readable report may be produced with:

`--report <report-file.json>`

## Preservation

The originally returned file must be preserved before cleaning, correcting, or
adjudicating data.
