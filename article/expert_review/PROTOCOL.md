---
status: protocol-ready
last_updated: 2026-07-13
tags: [cvss-v4, expert-review, blinded-study, human-in-the-loop]
---

# Independent expert-review protocol

Generated UTC: `2026-07-13T22:35:04.593310+00:00`

## Objective

Evaluate whether independent vulnerability-management specialists agree with
the watcher-generated candidate CVSS v4.0 Environmental assessments.

This protocol evaluates agreement and review effort. It does not assume that
the watcher output or any single reviewer is an absolute ground truth.

## Study design

- Scenarios: 30
- Target reviewers: 3
- Planned reviewer-scenario assessments:
  90
- Packet versions: A and B
- Randomization seed: 20260713
- Design: blinded, independently completed, counterbalanced ordering

## Blinding

Reviewers receive:

- a pseudonymous scenario identifier;
- Base vector, Base score, and Base severity when available;
- deployment and asset context;
- security requirements;
- control and evidence information.

Reviewers do not receive:

- CVE identifiers;
- source URLs;
- watcher candidate metric values;
- watcher rationales;
- priority deltas;
- watcher uncertainty decisions;
- original scenario identifiers;
- adjudication answer keys.

## Review task

For every scenario, the reviewer should:

1. inspect the supplied Base information;
2. inspect consumer-side context and evidence;
3. select Security Requirement values;
4. select applicable Modified Base metrics;
5. construct or record an Environmental vector;
6. select an operational priority category;
7. rate evidence sufficiency from 1 to 5;
8. rate confidence from 1 to 5;
9. record missing evidence and ambiguity;
10. record the time required.

## Reviewer eligibility

Recommended reviewers should have practical or research experience in at least
two of the following areas:

- vulnerability management;
- CVSS interpretation;
- security operations;
- patch management;
- risk assessment;
- asset or exposure management.

Reviewer experience must be documented separately from scenario responses.

## Independence

Reviewers must complete their first-pass assessments independently. Discussion
between reviewers is permitted only during a later adjudication stage.

## Adjudication

After independent review:

1. compare reviewer responses;
2. compare reviewers with the watcher answer key;
3. identify disagreements per metric;
4. conduct a structured adjudication meeting;
5. record whether disagreement resulted from insufficient evidence,
   interpretation ambiguity, reviewer error, or watcher error;
6. preserve both original and adjudicated decisions.

## Data-handling boundary

The current packet contains controlled research scenarios. It must not be
combined with confidential production evidence without an approved data
handling process.

Reviewer identifiers should remain pseudonymous in research exports.
