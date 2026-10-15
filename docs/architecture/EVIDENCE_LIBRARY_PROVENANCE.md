# Evidence Library and provenance increment

Date: 2026-10-15

## Goal

Expose the EvidenceSnapshot data model that already exists in the operational schema instead of creating a duplicate evidence subsystem.

## Implementation

### Evidence Library

New route:

/app/[organizationSlug]/evidence

It lists tenant-scoped EvidenceSnapshot records with:
- project/environment;
- source type;
- source reference;
- captured_at;
- expires_at;
- canonical hash;
- number of runs using the snapshot.

The page is read-only in this increment. It does not mutate historical evidence.

### Guided provenance input

The assessment run form now offers an optional progressive-disclosure section:

- source reference (URL, advisory ID or other reference);
- captured_at datetime.

If captured_at is blank, execution time is used.

The existing run API already supports sourceReference and capturedAt, so this increment reuses the current persistence contract and requires no Prisma migration.

### Result traceability

Run result pages now show:
- evidence source type;
- evidence reference;
- existing canonical hash and capture timestamp.

## Architectural boundary

This PR does not:
- change CVSS arithmetic;
- change environmental rules;
- create a new evidence table;
- allow editing historical snapshots;
- automatically reuse stale snapshots;
- introduce CR/IR/AR advanced inputs.

## Future reuse model

A future increment can add "Use existing evidence" by selecting an EvidenceSnapshot and copying its immutable metadata into a new evaluation context only after freshness and scope checks are explicit. Historical snapshots must never be mutated in place.
