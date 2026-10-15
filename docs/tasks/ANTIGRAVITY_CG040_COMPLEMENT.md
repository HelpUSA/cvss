# Antigravity continuation — CG-040 Gemini audit validation

Date: 2026-10-15
Branch: chatgpt/cg040-gemini-audit-validation

## Read first

Read `docs/reviews/GEMINI_AUDIT_VALIDATION_2026-10-15.md`.

Do not implement Gemini's recommendations verbatim.

## What ChatGPT already did

- restored authenticated GitHub read/write access;
- located repository HelpUSA/cvss;
- confirmed PR #28 and PR #29 are merged;
- created this isolated branch from scientific-validation;
- independently reviewed Gemini's seven recommendations;
- classified accepted/rejected/conditional items;
- preserved the rule that the canonical FIRST engine remains deterministic and policy-neutral.

## What Antigravity should complement

1. Inspect the current canonical scorer implementation and identify the exact EQ3/EQ6 lower-macrovector logic.
2. Run/reference official FIRST v4.0 test vectors or reference calculator behavior and report parity.
3. Produce an exhaustive or sufficiently complete machine-checked experiment for proposed sensitivity short-circuit behavior. Do not encode the AR/VA/SA example unless proven.
4. Inspect Evidence/Context schemas and propose the smallest additive TTL/freshness change that does not contaminate the canonical scorer.
5. Inspect current audit-ledger serialization and determine whether RFC 8785 is already implemented, partially implemented, or absent.
6. If NFC normalization exists, identify precisely where it happens and whether it occurs before or after the canonical hash boundary.
7. Inspect metamorphic tests and propose corrected MR-5/MR-6 implementations.
8. Return exact files changed, tests added, commands run, and outputs.

## Safety / scope

- Do not retune the frozen deterministic baseline casually.
- Do not open or use sealed C1/C2 material for tuning.
- Do not invent new score semantics.
- Do not call CVSS Base a risk score.
- Do not make presence-of-control imply control-effectiveness.
- Do not add mandatory AI/HITL/expert dependencies.

## Expected return

A commit or PR on top of this branch with:
- code findings;
- tests;
- minimal justified fixes;
- reproducible commands/results;
- a short residual-risk list.
