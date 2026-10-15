# Sensitivity envelope and uncertainty policy

Status: additive post-freeze utility; not wired into the frozen deterministic resolver by default.

## Purpose

HELPUS uses fail-closed evidence handling. That policy must not be weakened by guessing missing context. At the same time, an unresolved contextual metric may sometimes be mathematically irrelevant to the resulting CVSS scalar score.

The safe method is to enumerate admissible metric values through the same canonical scorer already used by HELPUS and compute [score_min, score_max].

If every admissible assignment produces the same score, the unresolved metric is score-invariant for that vector/domain.

This does not mean the evidence became known, the metric has a guessed value, the audit uncertainty disappears, or CVSS semantics changed. It only proves that the unresolved domain does not change the scalar score.

## Implementation

core/cvss_sensitivity.py provides score_envelope(), bounded Cartesian enumeration, candidate-metric validation, and envelope_is_non_expanding().

It intentionally does not mutate Base metrics, decide whether ABSTAIN should be bypassed, change the environmental rule catalog, or change the canonical scorer.

## Corrected uncertainty property

For a prior envelope E=[S_min,S_max] and a later evidence-constrained subset E'=[S'_min,S'_max], the required property is non-expansion:

- S'_min >= S_min
- S'_max <= S_max

Strict contraction is required only if the new evidence removes at least one state that contributes a distinct score outcome/boundary.

## Activation rule

Do not wire score-invariance into the production ABSTAIN decision until:
1. metric-domain derivation is explicitly specified;
2. admissible values come from deterministic evidence/policy rules;
3. the behavior is cross-checked by the pinned FIRST reference gate;
4. the audit record preserves the unresolved evidence fact;
5. no frozen-study artifact is silently retuned.
