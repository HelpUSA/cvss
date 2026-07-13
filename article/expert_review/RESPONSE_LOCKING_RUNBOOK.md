# Expert reviewer response locking runbook

## Purpose

This runbook defines how an independently completed reviewer response is
received, validated, preserved, and cryptographically locked.

The process does not require access to the adjudication answer key.

## Incoming files

Place returned files in:

`article/expert_review/reviewer_responses/incoming/`

Expected naming:

`reviewer_RXX_responses.csv`

## Validation without locking

Run:

`python -X utf8 tools/intake_and_lock_expert_reviewer_response.py <response-file>`

This validates the response but does not create an accepted lock.

## Validation and locking

After confirming that the received file is the original reviewer submission,
run:

`python -X utf8 tools/intake_and_lock_expert_reviewer_response.py <response-file> --lock`

The tool:

1. runs the strict response validator;
2. calculates the response SHA-256 value;
3. preserves an exact original copy;
4. creates a locked read-only copy;
5. preserves the machine-readable validation report;
6. records the lock in the private local registry;
7. prevents replacement by a different response for the same reviewer.

## Failed responses

Structurally invalid responses are copied to:

`article/expert_review/reviewer_responses/quarantine/`

A failed response must not be manually converted into an accepted locked
response. The reviewer should correct the original submission and return a new
file.

## Protection boundary

The following remain local and ignored by Git:

- original responses;
- locked responses;
- validation reports;
- quarantine files;
- response-lock registry;
- reviewer contact information;
- adjudication answer key.

## Before opening the answer key

Confirm that:

- every planned reviewer has one locked response;
- every locked response has a passing validation report;
- every original and locked copy has the expected SHA-256 value;
- no reviewer response was replaced;
- the answer-key commitment still matches the local answer key.

The answer key must remain unopened until all independent responses are locked.
