# Supplemental Metrics UX

Date: 2026-10-15

## Normative basis

FIRST CVSS v4.0 defines six optional Supplemental Metrics:

- Safety (S): X, N, P
- Automatable (AU): X, N, Y
- Recovery (R): X, A, U, I
- Value Density (V): X, D, C
- Vulnerability Response Effort (RE): X, L, M, H
- Provider Urgency (U): X, Clear, Green, Amber, Red

FIRST explicitly states that Supplemental Metrics do not affect the final numerical CVSS score. They convey additional extrinsic context that consumers may use in local prioritization or response processes.

## UX model

All Supplemental Metrics:
- live in a collapsed advanced panel;
- default to X / Not Defined;
- are optional;
- are persisted in EvidenceSnapshot metadata;
- are appended to the CVSS vector when explicitly defined;
- are displayed separately on the result page.

## Scoring boundary

Supplemental Metrics are intentionally NOT added to candidateMetrics.

candidateMetrics continues to represent Threat/Environmental metrics used in the score-producing enrichment path.

Supplemental values are carried separately as supplementalMetrics and merged only for vector enrichment.

## Result explanation

A dedicated SupplementalMetricsSummary component displays non-X values and explicitly states that they do not alter the numerical CVSS score.

## Server validation

The run route validates the exact FIRST value set for S/AU/R/V/RE/U and rejects malformed supplementalMetrics payloads.

## Out of scope

- local risk prioritization rules based on Supplemental Metrics;
- automated provider feed ingestion;
- policy weighting;
- scorer changes;
- C1/C2.
