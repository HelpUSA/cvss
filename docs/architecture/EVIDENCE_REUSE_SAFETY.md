# Safe evidence reuse

Date: 2026-10-15

## Goal

Allow operators to reuse preserved evidence as a starting point for a new run without mutating history, crossing tenant/environment boundaries, or trusting stale age values supplied by the browser.

## Safety model

A reusable snapshot must:

- belong to the exact same Environment;
- belong to the authenticated tenant;
- not be expired;
- remain immutable;
- create a new EvidenceSnapshot for the new run;
- preserve lineage through reusedEvidenceSnapshotId;
- have telemetry age recomputed from the original capturedAt on the server.

## UI behavior

The Step 4 form now exposes an optional reuse selector populated only with snapshots from the current Environment.

Expired snapshots remain visible for historical context but are disabled.

Selecting a snapshot prefills:

- reachability;
- evidence quality;
- firewall flag;
- max telemetry age;
- source reference;
- original capture time.

The displayed telemetry age is recalculated client-side for user clarity, but the server recalculates it again and remains authoritative.

## Server enforcement

The run API validates reusedEvidenceSnapshotId against:

- environmentId;
- tenant organizationId.

It rejects missing/foreign snapshots and expired snapshots.

When reuse is valid:

- sourceType becomes GUIDED_REUSE;
- evidenceObject.telemetryAgeDays is recomputed from original capturedAt;
- evidenceObject.reusedEvidenceSnapshotId is recorded;
- a brand-new EvidenceSnapshot is created;
- the original snapshot is never updated or deleted.

## Out of scope

- editing historical evidence;
- cross-environment reuse;
- automatic reuse without operator selection;
- changing TTL thresholds;
- changing CVSS scorer/rules;
- opening C1/C2.
