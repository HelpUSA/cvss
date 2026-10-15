# Consolidated Guided UX Review — 1→5

Date: 2026-10-15
Base: scientific-validation after PR #38

## Purpose

Stop feature expansion temporarily and validate whether the complete product is understandable to a new operator.

The system now includes:
- guided 5-step workflow;
- vector validation;
- Evidence Library and provenance;
- safe evidence reuse;
- deterministic result explanation;
- advanced CR/IR/AR;
- Threat Exploit Maturity;
- Supplemental Metrics.

Each capability passed isolated validation. The remaining risk is compositional complexity.

## Code-level findings before browser review

### 1. Steps 1–3 are comparatively simple

Projects, Environments and Assessments each have:
- one clear purpose;
- a stepper;
- a primary creation action;
- a next-step CTA.

This pattern is working well.

### 2. Step 4 is now the complexity hotspot

AssessmentRunForm currently mixes:
- source provider;
- evidence reuse;
- provenance;
- Base vector;
- reachability;
- evidence quality;
- telemetry freshness;
- CR/IR/AR;
- Supplemental Metrics;
- Threat Exploit Maturity;
- firewall/WAF context.

Most advanced sections are collapsed, but their placement still interrupts the mental model of the basic path.

The browser review must determine whether the form should be visually reorganized into:

A. Essential for first run
- source provider
- Base vector
- reachability
- evidence quality
- evidence age/freshness
- optional firewall evidence
- Execute

B. Optional evidence helpers
- reuse prior evidence
- source provenance

C. Advanced CVSS context
- Threat E
- CR/IR/AR
- Supplemental Metrics

No semantics or payload contracts should change solely for this reorganization.

### 3. Step 5 has high information density

The result page currently contains:
- main reading panel;
- result explanation;
- Supplemental summary;
- three metric cards;
- source/context vectors;
- ABSTAIN detail when applicable;
- traceability hashes and engine information;
- multiple next actions.

This is correct but may be too much for first-glance consumption.

Browser review should test whether progressive disclosure is needed for:
- full vectors;
- hashes/engine commit;
- detailed traceability.

The understandable explanation and score comparison should remain visible.

### 4. Navigation terminology may need refinement

Sidebar currently uses:
- 1. Projetos
- 2. Ambientes
- 3–5. Avaliações

This is compact but hides the 5-step mental model.

Do not change this blindly. Test whether users understand that Steps 4 and 5 live inside an Assessment.

### 5. “Comece aqui” currently marks Steps 4 and 5 from the same completedRuns signal

This is acceptable as a coarse progress indicator but can feel imprecise.
Do not add schema/state just for this unless browser testing proves it creates confusion.

## Product goal for this round

A first-time operator should be able to answer, on every page:

1. Where am I?
2. What do I need to do now?
3. What can I safely ignore?
4. What happens after I click the primary action?
5. Where do I go next?

The default route should not require understanding advanced CVSS terminology.

## Non-goals

No new:
- metrics;
- scoring logic;
- schema;
- threat feeds;
- AI;
- policies;
- expert/HITL gates;
- risk score;
- C1/C2 changes.

This round is UX consolidation only.
