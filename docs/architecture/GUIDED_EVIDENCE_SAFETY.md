# Guided evidence safety — UX increment

Date: 2026-10-15
Branch: chatgpt/ux-guided-evidence-safety

## Problem

The guided assessment workflow had three unsafe convenience defaults in the evidence-entry step:

- reachability defaulted to INTERNAL_ROUTED;
- evidence quality defaulted to SUFFICIENT;
- telemetry age defaulted to 0 days.

Those defaults make the form easier to submit, but they can accidentally convert "not evaluated yet" into structured environmental facts.

For an evidence-grounded CVSS workflow this is the wrong failure mode.

## Change

The form now defaults unresolved facts to an explicit unknown state:

- reachability -> UNKNOWN / "Ainda não avaliei";
- evidence quality -> UNKNOWN / "Ainda não avaliei";
- telemetry age -> blank, serialized as null until the user provides a value.

The deterministic engine can then preserve fail-closed ABSTAIN behavior rather than receiving optimistic values by default.

## Contextual help

A new inline component appears before the evidence form and explains:

1. preserve the published CVSS-B vector;
2. do not modify Base metrics to reflect local context;
3. only classify reachability when topology is actually known;
4. only mark evidence sufficient when it is verifiable and fresh;
5. ABSTAIN is a valid safety outcome, not a calculation failure.

This uses progressive disclosure via details/summary blocks so the main workflow stays compact.

## Regression protection

web/tests/guided-evidence-safety.test.ts verifies that:

- INTERNAL_ROUTED is not the default;
- SUFFICIENT is not the default;
- UNKNOWN is available as a first-class choice;
- blank telemetry age is not silently coerced to zero;
- inline guidance preserves unknown-state and ABSTAIN semantics.

## What this does not change

- CVSS arithmetic;
- environmental rule catalog;
- FIRST reference scorer;
- ABSTAIN rules;
- TTL thresholds;
- tenant authorization;
- persistence schema;
- historical research artifacts.

## Next recommended UX increments

These require browser/product validation before expanding implementation:

- inspect the complete assessment page at 375px/768px/1440px and adjust visual density if needed;
- consider a dedicated Evidence Library instead of growing the run form indefinitely;
- consider optional CR/IR/AR advanced input behind progressive disclosure;
- make the current workflow step visually persistent across the assessment pages;
- add friendly field-level validation for malformed CVSS vectors before submission;
- consider source metadata fields such as source URL/advisory reference without making them mandatory;
- verify keyboard/focus behavior of details/summary help blocks;
- verify unknown/null evidence is rendered clearly in persisted history and audit receipts.
