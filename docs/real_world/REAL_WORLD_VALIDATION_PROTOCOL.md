# Real-world validation protocol

## Purpose

Define how the system should be validated before being described as useful in real operational settings.

## Validation tiers

### Tier 1: Formula correctness

Known CVSS vectors must reproduce official expected scores.

### Tier 2: Scenario reproducibility

The same scenario package must always produce the same outputs.

### Tier 3: Real CVE evidence

Real vulnerabilities must include source references, vector strings, affected assets, and environmental assumptions.

### Tier 4: Expert review

Human experts review whether contextual prioritization is reasonable. This is future work until explicitly completed.

## Required validation record

- CVE or finding identifier.
- Official vector and score.
- Environment context.
- Contextual score.
- Trace output.
- Source evidence.
- Reviewer decision, if available.

## Current status

The project currently satisfies prototype reproducibility but not full real-world validation.
