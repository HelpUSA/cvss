# Expert-review data codebook

## Identification fields

- `reviewer_code`: pseudonymous reviewer identifier.
- `packet_version`: randomized order version A or B.
- `review_scenario_id`: blinded scenario identifier.

## Timing fields

- `review_started_utc`: ISO 8601 UTC timestamp.
- `review_completed_utc`: ISO 8601 UTC timestamp.
- `review_duration_seconds`: total scenario review time.

## Rating fields

- `evidence_sufficiency_1_to_5`: evidence sufficiency rating.
- `confidence_1_to_5`: reviewer confidence.

## CVSS Environmental fields

- `reviewed_CR`, `reviewed_IR`, `reviewed_AR`: Security Requirements.
- `reviewed_MAV` through `reviewed_MSA`: Modified Base metrics.
- `reviewed_environmental_vector`: assembled reviewed vector.

## Operational field

- `reviewed_operational_priority`: prototype operational category. It is not an
  official CVSS score.

## Governance fields

- `evidence_missing`: concise missing-evidence description.
- `ambiguity_detected`: concise ambiguity description.
- `decision_status`: complete or deferred state.
- `reviewer_comments`: optional rationale.

## Protected comparison fields

The adjudication answer key contains watcher recommendations and original
scenario identifiers. It must remain unavailable to reviewers until their
independent assessments are locked.
