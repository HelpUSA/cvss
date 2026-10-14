# HELPUS Cognitive Assurance Layer (HCAL)
## Optional AI Augmentation Architecture for HelpUS CVSS AI v4.0

**Document Version:** 1.0.0  
**Status:** PROPOSED ARCHITECTURE — NON-BLOCKING OPTIONAL LAYER  
**Date:** 2026-10-13

## 1. Principle

The HelpUS CVSS platform must remain fully functional from ingestion to final deterministic CVSS output with no external AI service available.

Formal invariant:

**AI_ENHANCEMENT_MUST_BE_NON_BLOCKING**

The core pipeline remains:

`Evidence Ingestion -> Asset Context Profile -> Environmental Rule Engine -> Metric Resolver -> Canonical FIRST CVSS Engine -> Prioritization / Report / Ticket`

The optional AI layer begins only after or alongside evidence preparation and must never become a required dependency of scoring.

## 2. Architectural Separation

### 2.1 Deterministic Plane
Responsible for:
- evidence ingestion;
- context normalization;
- environmental rule execution;
- metric resolution;
- CVSS vector construction;
- deterministic FIRST scoring;
- prioritization;
- audit trail;
- primary operational output.

This plane must continue working when every AI connector is disabled, unavailable, rate-limited, misconfigured, or offline.

### 2.2 Intelligence Plane — HCAL
HCAL is optional and may provide:
- semantic review of reports/advisories;
- inconsistency detection;
- context-gap detection;
- executive summaries;
- explanatory narratives;
- suggested evidence checks;
- report enrichment;
- cross-model review;
- post-facto quality assurance;
- adversarial review of deterministic decisions.

HCAL has no direct authority to calculate or overwrite the final CVSS score.

## 3. Operating Modes

### MODE 0 — CORE_AUTONOMOUS
No external AI services are used.

Expected behavior:
- full pipeline completes;
- CVSS vectors and scores are produced;
- reports/tickets are generated;
- `AI_ENRICHMENT_STATUS = NOT_REQUESTED` or `NOT_AVAILABLE`.

### MODE 1 — SINGLE_AI_AUGMENTATION
One configured AI provider receives an approved analysis package and returns structured findings.

### MODE 2 — MULTI_AI_ASSURANCE
Two or more independent AI providers review the same normalized package and return structured findings for comparison.

The product must not require specific brands. ChatGPT, Gemini, local models, enterprise models, or future providers are replaceable adapters.

## 4. AI Analysis Packages

The CVSS platform may generate explicit export packages such as:

### 4.1 Vulnerability Analysis Package
- CVE/advisory identifier;
- source advisory excerpt or normalized facts;
- source/base vector;
- environmental vector;
- Asset Context Profile subset;
- triggered environmental rules;
- evidence references/hashes;
- final deterministic score;
- uncertainty/abstention flags.

### 4.2 Environment Review Package
- sanitized topology summary;
- reachability classification;
- control inventory;
- dependency graph summary;
- policy classifications;
- evidence age/freshness;
- contradiction flags.

### 4.3 Executive Risk Package
- deterministic findings;
- severity/prioritization;
- affected services;
- remediation status;
- evidence-backed rationale.

## 5. AI Return Contract

AI responses should be structured and machine-readable.

Example schema:

```json
{
  "finding_id": "AI-0041",
  "type": "context_inconsistency",
  "severity": "medium",
  "claim": "Network-isolation evidence conflicts with routing metadata.",
  "evidence_refs": ["NET-21", "CMDB-18"],
  "confidence": 0.91,
  "recommended_action": "verify_route",
  "authoritative_candidate": false
}
```

## 6. Two Return Classes

### 6.1 Non-Authoritative Return
May be incorporated directly into enriched reports:
- explanation;
- executive summary;
- remediation suggestion;
- hypothesis;
- anomaly warning;
- investigation recommendation.

These outputs must be labeled as AI-generated advisory content.

### 6.2 Authoritative-Candidate Return
Potentially relevant to metric resolution, such as:
- possible new exposure fact;
- possible authentication prerequisite;
- possible dependency;
- possible control effectiveness fact.

These returns must **not** alter CVSS metrics directly.

Required path:

`AI finding -> evidence validation -> policy/rule validation -> metric resolver -> deterministic FIRST engine`

Only validated evidence may influence metrics.

## 7. Multi-AI Review

In MODE 2, providers return normalized findings independently.

The comparison engine may classify:
- unanimous finding;
- partial agreement;
- full disagreement;
- provider-specific finding.

Agreement increases review priority but does not create normative authority.

Formal invariant:

**AI_CONSENSUS != CVSS_AUTHORITY**

For any semantic path that is allowed to generate metric candidates, existing governance still applies:

**STRICT_QUORUM_DELTA = 0 at metric level**

and final score calculation remains deterministic.

## 8. Failure and Graceful Degradation

AI-provider failure must never block the deterministic core.

Examples:
- timeout -> continue core flow;
- API failure -> continue core flow;
- malformed response -> discard AI return;
- quota exceeded -> continue core flow;
- one provider unavailable in multi-AI mode -> degrade to configured policy or skip enrichment;
- all providers unavailable -> `AI_ENRICHMENT_STATUS = NOT_AVAILABLE`.

Core completion target under complete AI outage:

**CORE_COMPLETION_WITH_AI_UNAVAILABLE = 100% for all otherwise valid core cases**

This is a testable architectural requirement, not a claim until verified.

## 9. Privacy and Security

Before sending any package to an external provider:
- minimize data;
- remove credentials/secrets;
- pseudonymize or remove internal identifiers where feasible;
- classify the package;
- enforce provider-specific policy;
- log exactly what was transmitted;
- support client opt-out;
- support local/private models;
- prevent prompt-injection content from controlling system instructions;
- validate and sanitize returned structured data.

Recommended connector classes:
- `EXTERNAL_AI_PROVIDER`;
- `PRIVATE_ENTERPRISE_AI`;
- `LOCAL_MODEL`.

## 10. Auditability

Each optional AI transaction should record:
- package hash;
- provider adapter/version;
- model identifier where available;
- request timestamp;
- response hash;
- normalized findings;
- validation decision;
- whether any finding became validated evidence;
- resulting report version;
- no direct score override flag.

## 11. Product Positioning

Possible product tiers/modules:
- `HelpUS CVSS Autonomous` — deterministic core only;
- `HelpUS CVSS Cognitive Assurance` — optional single-AI enrichment;
- `HelpUS CVSS Multi-AI Assurance` — optional multi-model review.

No tier may weaken deterministic scoring guarantees.

## 12. Scientific Claim Guardrail

Preferred description:

> The proposed system provides a deterministic and fully autonomous CVSS v4.0 environmental-scoring pipeline augmented by an optional, non-blocking AI assurance layer for contextual anomaly detection, explanation, and evidence-backed refinement. AI services do not participate in the normative scoring function and are not required for system completion.

## 13. Current Status

This document specifies an optional future augmentation layer.

It does not change:
- G1-G8 closed state;
- G9A/G9B/G10A current audit status;
- deterministic score authority;
- C1/C2 seals;
- SAFE_TO_FREEZE state.
