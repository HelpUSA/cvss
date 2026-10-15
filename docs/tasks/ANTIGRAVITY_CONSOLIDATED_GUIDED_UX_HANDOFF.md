# Antigravity handoff — consolidated 1→5 UX audit

Repository: HelpUSA/cvss
Branch: chatgpt/consolidated-guided-ux-review
Base: scientific-validation

## Mission

Perform a real-browser, first-time-user audit of the full operational flow after PRs 29–38.

Do not add features.

The goal is to reduce cognitive load and make the path obvious.

## Required path

Use a disposable tenant and complete:

Login
→ Organization
→ Comece aqui
→ Step 1 Project
→ Step 2 Environment
→ Step 3 Vulnerability/Assessment
→ Step 4 Evidence
→ Step 5 Result
→ Evidence Library
→ return to Assessment
→ optional reuse

Test at:
- 1440px
- 768px
- 375px

## Persona

Assume the operator:
- knows basic vulnerability management;
- can copy a published CVSS vector;
- does NOT know every CVSS v4.0 metric;
- should be able to complete a basic run without opening advanced sections.

## Main acceptance test

A basic first run must be achievable while leaving all advanced controls untouched.

The user should only need to understand:
- source vector;
- environment reachability;
- evidence quality/freshness;
- execute;
- read result.

## Step 4 audit

This is the highest-priority page.

Evaluate whether the current visual order is too dense.

Current capabilities include:
- source provider
- reuse
- provenance
- Base vector
- reachability
- evidence quality
- freshness
- CR/IR/AR
- Supplemental
- Threat E
- firewall/WAF

If browser evidence confirms cognitive overload, reorganize VISUALLY into:

1. ESSENCIAL PARA EXECUTAR
   - source provider
   - Base vector
   - reachability
   - evidence quality
   - evidence freshness
   - firewall/WAF if it remains simple

2. OPCIONAL — EVIDÊNCIA E PROVENANCE
   - reuse existing evidence
   - source provenance

3. AVANÇADO — CVSS v4.0
   - Threat E
   - CR/IR/AR
   - Supplemental Metrics

Advanced groups should remain collapsed by default.

Do not change payload semantics.

Do not change defaults.

Do not auto-fill advanced metrics.

## Step 5 audit

The first viewport should prioritize:

1. result status;
2. source vs contextual score;
3. plain-language explanation;
4. next action.

Technical details may be moved behind progressive disclosure if browser testing shows overload:
- full vectors;
- hashes;
- engine commit;
- traceability details.

Do NOT hide technical data completely.

## Navigation audit

Test whether “3–5. Avaliações” is understandable.

If not, prefer wording that explains containment without inventing dead links, e.g.:
“3–5. Avaliações e resultados”

Only change if it is demonstrably clearer.

## “Comece aqui” audit

Verify each card answers:
- what this step means;
- whether prerequisite exists;
- primary action.

Do not add more theory.

## Language audit

Flag and simplify unexplained terms visible on the basic path:
- ABSTAIN
- provenance
- nomenclature
- candidate metrics
- threat intelligence
- modified metrics

Advanced terminology can remain inside advanced disclosures.

Basic path should use plain Portuguese first, acronym second.

## Browser behavior

Check:
- primary CTA visibility without excessive scrolling;
- no accidental open advanced sections;
- keyboard navigation;
- 200% zoom;
- mobile overflow;
- long vector/hash wrapping;
- empty states;
- error states;
- ABSTAIN state;
- successful result state.

## Allowed changes

Only evidence-based UX consolidation:
- reorder existing sections;
- add/remove visual dividers;
- shorten copy;
- change headings;
- improve CTA labels;
- collapse technical detail;
- adjust spacing;
- improve mobile layout;
- clarify terminology.

## Forbidden changes

Do not alter:
- scorer;
- FIRST arithmetic;
- Environmental rules;
- Threat E semantics;
- CR/IR/AR semantics;
- Supplemental semantics;
- ABSTAIN;
- TTL;
- tenant authorization;
- schema;
- C1/C2.

## Quality gates after any change

cd web
npm ci
npx prisma validate
npx prisma generate
npm run typecheck
npm run test:saas:unit
npm run build

pytest tests/

Then real-pipeline.

## Required report

Create:
docs/reviews/ANTIGRAVITY_CONSOLIDATED_GUIDED_UX_REPORT.md

Report:

ANTIGRAVITY CONSOLIDATED UX REPORT

Tested HEAD:

Basic first run without advanced controls:
PASS / FAIL

Step 1 clarity:
PASS / NEEDS_CHANGE

Step 2 clarity:
PASS / NEEDS_CHANGE

Step 3 clarity:
PASS / NEEDS_CHANGE

Step 4 clarity:
PASS / NEEDS_CHANGE

Step 4 advanced separation:
PASS / NEEDS_CHANGE

Step 4 primary CTA visibility:
PASS / NEEDS_CHANGE

Step 5 first-glance comprehension:
PASS / NEEDS_CHANGE

Step 5 technical density:
PASS / NEEDS_CHANGE

Comece aqui:
PASS / NEEDS_CHANGE

Sidebar:
PASS / NEEDS_CHANGE

Evidence Library:
PASS / NEEDS_CHANGE

Evidence reuse:
PASS / NEEDS_CHANGE

ABSTAIN comprehension:
PASS / NEEDS_CHANGE

Desktop:
PASS / FAIL

Tablet:
PASS / FAIL

Mobile:
PASS / FAIL

Accessibility:
PASS / FAIL

Changes made:
[list]

Quality gates:
[result]

CI:
PASS / FAIL / RUNNING

Residual issues:
[list]

Recommendation:
MERGE / FIX_REQUIRED

## Final rule

Do not optimize for maximum information on screen.

Optimize for:
“Can a new operator complete the correct next action without needing prior training?”

If yes, preserve the simpler design.
