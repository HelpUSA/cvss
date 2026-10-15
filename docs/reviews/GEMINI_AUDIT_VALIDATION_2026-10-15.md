# CG-040 — Validation of Gemini architectural audit

Date: 2026-10-15
Project: HELPUS CVSS AI v4.0
Status: ChatGPT independent review

## Purpose

Record which Gemini recommendations are accepted, rejected, or require proof against the official FIRST CVSS v4.0 behavior before implementation.

## Decisions

### 1. EQ3 / EQ6 coupling — ACCEPT, P0

Treat EQ3 and EQ6 as a coupled macro-dimension when resolving lower macrovectors. Add regression tests covering valid/invalid combinations and compare against FIRST reference behavior.

### 2. Sensitivity short-circuit before HELPUS ABSTAIN — ACCEPT WITH REFORMULATION

The canonical CVSS engine must not invent an ABSTAIN concept. ABSTAIN belongs to the HELPUS evidence/policy resolver.

Before HELPUS abstains because an environmental/context predicate is unresolved, the resolver MAY compute a score envelope by varying only the unresolved HELPUS-derived metric domain.

If all admissible values produce the same canonical CVSS result, the unresolved predicate is mathematically irrelevant to the score and the workflow may continue while preserving the unresolved evidence state in the audit trail.

Do not hard-code claims such as “AR is always irrelevant when VA=N and SA=N” without exhaustive reference-backed proof.

### 3. Mandatory Decimal / ban on IEEE-754 — REJECT AS STATED

Do not change numeric representation merely because Gemini claimed a 1.5–2% divergence rate. That claim is not accepted without evidence.

Acceptance criterion is behavioral parity with the official FIRST v4.0 reference vectors/calculator. Numeric implementation is an internal choice as long as parity is exact for the validation corpus.

### 4. Evidence/control TTL — ACCEPT AS HELPUS EXTENSION, P1

TTL/freshness belongs to Evidence/Context Engine, not the canonical CVSS engine.

Recommended fields:
- observed_at
- freshness_policy / max_ttl_seconds
- evaluation_time
- freshness_state

Expired evidence must not silently justify a modified metric. Preserve stale evidence in the audit ledger and require policy-defined behavior.

### 5. Environmental control matrices — ACCEPT AS TAXONOMY ONLY

The proposed grouping into:
- access/surface controls
- local-impact containment
- lateral/subsequent-system confinement

is useful for rule organization.

However, no control may automatically reduce MAV/MAC/MAT/MPR/MUI/MVC/MVI/MVA/MSC/MSI/MSA merely because the control exists. A rule must prove that the control is effective, relevant to the specific exploit/impact path, and sufficiently evidenced.

### 6. Metamorphic MR-5 / MR-6 — ACCEPT WITH CHANGES

MR-5 is a candidate property and must be validated against the FIRST reference implementation before being promoted to a hard invariant.

MR-6 should use non-expansion, not unconditional strict contraction:

new_envelope ⊆ previous_envelope

Require strict contraction only when the new evidence eliminates at least one score-producing admissible state.

### 7. RFC 8785 / Unicode — CORRECT BEFORE IMPLEMENTATION

JCS/RFC 8785 can be used for canonical JSON hashing.

Do not describe NFC normalization as part of JCS. If HELPUS wants NFC, normalization must be a separately documented ingestion policy performed before data enters the canonical hashed domain; after canonical-domain entry the hashed representation must not be silently rewritten.

## Architectural boundary

Keep the canonical scorer minimal:

Evidence -> Context -> Policy/Metric Resolver -> valid CVSS vector -> Canonical FIRST Engine -> score/vector -> explanation/audit

The Canonical FIRST Engine must not own:
- AI confidence
- evidence freshness
- ABSTAIN policy
- expert/reviewer workflow
- organizational risk semantics
- provenance policy

Its contract is deterministic FIRST-compatible CVSS v4.0 calculation.

## Required validation work

1. Compare current scorer against official FIRST vectors/reference implementation.
2. Add focused EQ3/EQ6 regression tests.
3. Prove any sensitivity-short-circuit rule by exhaustive or reference-backed enumeration before activation.
4. Add evidence freshness schema/rules outside the scorer.
5. Add MR-5/MR-6 only after proving the expected property against the reference corpus.
6. Define canonicalization boundary before changing audit-ledger hashing.
7. Do not modify the frozen deterministic baseline without explicit evidence and change-control review.
