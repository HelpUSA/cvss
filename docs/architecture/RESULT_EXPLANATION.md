# Result explanation increment

Date: 2026-10-15

## Goal

Make the result page answer four practical questions before showing the technical detail:

1. What changed?
2. Why?
3. What evidence supported the outcome?
4. What should the user do next?

## Implementation

A deterministic presentation helper derives explanation text only from persisted run facts:

- status;
- source score;
- final score;
- decision;
- candidate metrics;
- abstention reasons;
- evidence source type;
- evidence reference;
- capture time.

It does not call AI and does not infer facts that are not present in the run.

A new RunExplanation component appears before the metric grid on the result page.

## Completed runs

For completed runs, the explanation says whether the numeric score changed and lists candidate contextual metrics that were recorded by the engine.

If no candidate metric exists, it explicitly says no contextual metric was applied.

## Abstained runs

For ABSTAINED runs, the explanation preserves the abstention reasons exactly as persisted and recommends correcting missing/stale/conflicting evidence and executing a new run.

It never invents an environmental result.

## Architectural boundary

This increment does not modify:

- canonical scorer;
- CVSS vector generation;
- environmental rules;
- evidence freshness thresholds;
- ABSTAIN policy;
- EvidenceSnapshot storage;
- C1/C2;
- historical runs.

## UX principle

The result page should lead with an understandable explanation and then expose score, vectors, hashes and engine metadata for auditability.
