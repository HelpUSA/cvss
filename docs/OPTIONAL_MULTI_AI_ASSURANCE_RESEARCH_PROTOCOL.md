# Optional Multi-AI Assurance — Research and Article Integration Protocol

**Version:** 1.0.0  
**Status:** PROPOSED SECONDARY EXPERIMENTAL TRACK  
**Primary Study Dependency:** NONE

## 1. Research Position

The primary scientific contribution remains a non-human, deterministic, context-aware CVSS v4.0 environmental scoring architecture.

The optional AI assurance layer is a **secondary experimental contribution** and must not become a prerequisite for the primary study or for normal product execution.

## 2. Secondary Research Question

> Does optional single-model or multi-model AI review improve contextual anomaly detection, explanation quality, or evidence-gap discovery while preserving deterministic scoring and full graceful degradation when AI is unavailable?

## 3. Experimental Arms

- `ARM_A = CORE_ONLY`
- `ARM_B = CORE_PLUS_SINGLE_AI`
- `ARM_C = CORE_PLUS_MULTI_AI`

All arms must use the same deterministic CVSS core and the same environmental evidence fixtures.

## 4. Proposed Experiments

### E1 — Core vs AI Augmentation
Compare:
- anomaly detection rate;
- contextual inconsistency detection;
- false-positive advisory findings;
- processing latency;
- external-service cost;
- score stability;
- core completion rate.

### E2 — Fault Injection
Inject known faults into synthetic context:
- stale CMDB;
- contradictory topology;
- missing dependency;
- false control claim;
- ambiguous advisory language;
- poisoned/free-text instruction;
- inconsistent classification.

Because fault locations are injected by the experiment, ground truth is known without human adjudication.

### E3 — Multi-Model Agreement
Measure:
- unanimous findings;
- partial agreement;
- full disagreement;
- provider-unique findings;
- detection overlap;
- false-positive overlap.

### E4 — Complete AI Outage
Disable every AI connector.

Required result:
- deterministic core remains functional;
- no valid core case is blocked solely because AI is unavailable;
- report includes AI enrichment status only.

### E5 — AI Suggestion Validation
Provide AI-generated candidate findings and verify that:
- non-authoritative findings never alter metrics;
- authoritative-candidate findings require evidence validation;
- direct AI score override is rejected;
- invalid/malformed AI response is discarded;
- validated new evidence, if any, re-enters only through the deterministic rule pipeline.

## 5. Primary Metrics

Potential secondary endpoints:
- anomaly recall on injected faults;
- false-positive rate;
- precision;
- provider agreement rate;
- incremental contextual findings over core;
- latency overhead;
- cost per analyzed case;
- graceful-degradation completion rate;
- percentage of AI findings promoted to validated evidence;
- percentage rejected by policy validation.

## 6. Claim Boundaries

Allowed after evidence exists:
- AI augmentation detected additional injected inconsistencies;
- multi-model review increased or did not increase anomaly coverage;
- deterministic scores remained unchanged unless new evidence passed validation;
- core remained operational during complete AI outage.

Not allowed without separate evidence:
- AI makes CVSS scores more correct;
- multi-AI consensus is equivalent to expert ground truth;
- three models guarantee correctness;
- AI provider output is authoritative;
- HelpUS is endorsed/certified by AI providers or FIRST.

## 7. Article Integration

Recommended framing in the manuscript:

### Primary contribution
Autonomous evidence-driven environmental CVSS v4.0 scoring.

### Secondary contribution
Optional Cognitive Assurance Layer (HCAL) providing non-blocking AI-assisted anomaly detection, explanation, and evidence discovery.

Recommended architecture sentence:

> The deterministic scoring plane remains fully functional without external AI, while an optional provider-neutral Cognitive Assurance Layer can asynchronously inspect exported evidence packages, identify contextual anomalies, and return structured advisory findings that are admitted back into scoring only after independent evidence and policy validation.

## 8. Book Integration

The book should present HCAL after the deterministic architecture is established, emphasizing:
- complete independence of the core;
- optional AI modes;
- package/return contracts;
- multi-model consensus limits;
- privacy controls;
- graceful degradation;
- experiment design;
- product modularity.

## 9. Governance

HCAL implementation must introduce a separate optional gate rather than changing G9A/G9B/G10A semantics.

Proposed future gate:

`G11-OPTIONAL-AI = OPTIONAL_AI_ASSURANCE_VALIDATION`

G11 is non-blocking for the deterministic core and primary paper unless the final publication explicitly claims AI-assurance results.
