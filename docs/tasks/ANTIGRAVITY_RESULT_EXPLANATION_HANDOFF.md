# Antigravity handoff — result explanation

Repository: HelpUSA/cvss
Branch: chatgpt/result-explanation
Base: scientific-validation

## Already implemented by ChatGPT

- deterministic run-explanation helper;
- result explanation component;
- explanation inserted before technical metric grid;
- completed-run score-change explanation;
- persisted candidate-metric list;
- ABSTAIN explanation based only on stored abstention reasons;
- evidence provenance summary;
- next-action guidance;
- responsive styling;
- regression tests.

## Required validation

Inside web/:
1. npm ci
2. npx prisma validate
3. npx prisma generate
4. npm run typecheck
5. npm run test:saas:unit
6. npm run build

Also run Python core suite if the real pipeline requires it.

## Browser cases

### Case A — completed and score changed
Confirm:
- source and final scores are both named;
- applied candidate metrics shown;
- provenance shown;
- technical score/vector cards remain below explanation.

### Case B — completed but numeric score unchanged
Confirm wording explicitly says context did not change numeric score.
Do not imply "no effect" if contextual metrics were still recorded.

### Case C — ABSTAIN
Confirm:
- no final environmental claim is invented;
- persisted abstention reasons are visible in plain language;
- next action asks user to correct evidence and rerun;
- CVSS-B remains available.

### Case D — no source reference
Confirm explanation says external reference was not informed without breaking layout.

## Safety checks

- helper must not call AI;
- helper must not recompute CVSS;
- helper must not transform candidate metrics into stronger causal claims;
- persisted facts remain the source of truth.

## Responsive/accessibility

Validate at 1440px, 768px and 375px.
Check headings, lists, reading order, zoom 200% and screen-reader semantics.

## Do not change

- scorer;
- rule catalog;
- ABSTAIN;
- TTL;
- EvidenceSnapshot schema;
- C1/C2.

## Return

Create:
docs/reviews/ANTIGRAVITY_RESULT_EXPLANATION_EXECUTION_REPORT.md

Include:
- tested head;
- tests/typecheck/build;
- changed-score case;
- unchanged-score case;
- ABSTAIN case;
- no-reference case;
- responsive/accessibility;
- files changed;
- residual issues;
- MERGE or FIX_REQUIRED.
