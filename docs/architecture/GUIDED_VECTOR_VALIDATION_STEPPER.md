# Guided vector validation and persistent workflow stepper

Date: 2026-10-15

## Goal

Reduce two common operator errors:

1. submitting malformed CVSS v4.0 vectors and only discovering the problem after the API call;
2. losing track of the current workflow stage while moving across Projects, Environments, Assessments, Evidence and Results.

## Vector validation

A new client-safe helper validates the vector structure before submission:

- requires prefix CVSS:4.0;
- requires all Base metrics;
- rejects duplicate metrics;
- rejects unknown metric names;
- rejects invalid values;
- recognizes Threat / Environmental usage and reports CVSS-B / CVSS-BT / CVSS-BE / CVSS-BTE.

It does not calculate score and does not replace the canonical engine.

The form now shows:
- a positive "Vetor válido" state with detected nomenclature;
- the first actionable validation error inline;
- aria-invalid when appropriate;
- submission blocked when a non-empty vector is invalid.

The API/server remains the authority and must continue validating input independently.

## Unknown telemetry age

The "Idade da evidência" field is no longer browser-required. Blank is preserved as null so the engine can fail closed rather than force the user to invent a value.

The validity-window field remains explicit.

## Workflow stepper

A shared GuidedWorkflowStepper is now rendered on:

1. Projects
2. Environments
3. Assessments
4. Evidence
5. Result

Completed steps show a check mark, the current step is highlighted, and future steps remain neutral.

The component is informational only; it does not bypass authorization or workflow prerequisites.

## Scope intentionally excluded

- score calculation;
- environmental rule changes;
- Evidence Library;
- advanced CR/IR/AR input;
- production deployment;
- C1/C2;
- AI behavior.

## Validation required

Antigravity should run the full web quality gates, test malformed/valid vectors in-browser, verify screen-reader/keyboard behavior, and inspect horizontal stepper scrolling on mobile.
