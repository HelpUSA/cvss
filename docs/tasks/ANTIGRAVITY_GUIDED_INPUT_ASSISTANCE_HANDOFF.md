# Antigravity handoff — Guided Input Assistance UX

Repository: HelpUSA/cvss
Branch: chatgpt/guided-input-assistance
Base: scientific-validation

## User-reported problem

The user attempted the workflow step by step and felt uncertain in places where the product required typing values from scratch.

The objective is to make the product more selection-driven where that is safe:
- dropdowns;
- presets;
- editable templates;
- automatic slugs.

## Important constraint

Do NOT auto-fill technical facts merely to make the form easier.

Must remain factual/manual where appropriate:
- CVE;
- CVSS vector;
- source URL/advisory;
- threat-intelligence reference;
- exact provenance timestamp.

## Implemented changes

### Projects

Project creation now has:
- "Começar por um modelo (opcional)"
- ERP / Aplicação
- Portal / API
- Infraestrutura
- Serviço em nuvem
- Projeto geral

Selecting a model fills the initial name.

Slug is generated automatically from the name.

Slug remains editable.

Validate:
- accents normalize correctly;
- slug updates while user has not manually edited it;
- once user manually edits slug, later name changes do not overwrite it.

### Environments

Adds:
"Tipo de ambiente (atalho)"

Options:
- Produção
- Homologação
- Desenvolvimento
- DMZ
- Rede interna
- Cloud / Nuvem

Selection pre-fills the environment name and slug.

Custom name remains possible.

### Assessment title

Adds:
"Modelo de nome (opcional)"

Options:
- CVE + ambiente
- "Avaliação" + CVE + ambiente
- CVE + projeto + ambiente

Generated title remains editable.

The helper must use the actual CVE/environment/project currently selected.

### Assessment observation

Adds:
"Observação rápida (opcional)"

Options:
- Serviço acessível pela Internet
- Somente rede interna
- Ativo/serviço crítico
- Sem observação

The generated paragraph is editable.

The UI explicitly states that the text is a starting point and must be adjusted to real facts.

### Step 4 evidence

Adds:
"Idade da evidência — atalho"

Options:
- Coletada agora / hoje = 0
- 1 day
- 3 days
- 7 days
- 30 days

Adds:
"Validade máxima — atalho"

Options:
- 1 day
- 7 days
- 30 days
- 90 days

Original numeric inputs remain present.

## Browser audit required

Act as a first-time operator.

Check whether you can now complete the workflow with substantially less typing.

Evaluate:
1. Does the user understand the difference between a shortcut and factual evidence?
2. Do presets feel helpful rather than authoritative?
3. Is "Outro/personalizado" effectively possible by editing the filled value?
4. Does automatic slug generation reduce confusion?
5. Is keyboard/mobile operation clear?
6. Do templates update from current CVE/environment values correctly?

## Negative tests

Confirm:
- project template does not lock name;
- environment shortcut does not lock name;
- slug remains editable;
- manual slug is not unexpectedly overwritten;
- CVSS vector is never auto-populated with an example;
- CVE is never invented;
- observation template can be erased/edited;
- age presets do not hide manual numeric input;
- validity presets do not hide manual numeric input.

## E2E impact

Update Playwright selectors only if necessary.

Do not weaken existing synthetic user journey coverage.

The existing basic flow must still pass:
Project → Environment → Assessment → Run → Result.

Prefer using the new selection helpers in at least one E2E path so they become protected by regression testing.

## Quality gates

cd web
npm ci
npx prisma validate
npx prisma generate
npm run typecheck
npm run test:saas:unit
npm run build

pytest tests/

Then real-pipeline, including Synthetic User Journey E2E.

## Scope

Allowed:
- copy;
- helper selectors;
- templates;
- automatic slug behavior;
- accessibility labels;
- E2E selector updates.

Forbidden:
- scorer changes;
- CVSS math changes;
- schema migrations;
- auto-generated security facts;
- new AI feature;
- expert/HITL requirement.

## Required report

Create:
docs/reviews/ANTIGRAVITY_GUIDED_INPUT_ASSISTANCE_REPORT.md

Return:

==================================================
ANTIGRAVITY GUIDED INPUT ASSISTANCE REPORT
==================================================

Repository:
HelpUSA/cvss

PR:
#44

Tested HEAD:

Project model selector:
PASS / FAIL

Project automatic slug:
PASS / FAIL

Manual project slug preserved:
PASS / FAIL

Environment presets:
PASS / FAIL

Environment automatic slug:
PASS / FAIL

Assessment title templates:
PASS / FAIL

Assessment observation templates:
PASS / FAIL

Templates remain editable:
PASS / FAIL

CVE never invented:
PASS / FAIL

CVSS vector never auto-filled:
PASS / FAIL

Evidence age shortcuts:
PASS / FAIL

Evidence validity shortcuts:
PASS / FAIL

Manual numeric fields preserved:
PASS / FAIL

Desktop journey:
PASS / FAIL

Tablet journey:
PASS / FAIL

Mobile journey:
PASS / FAIL

Synthetic E2E:
PASS / FAIL

Typecheck:
PASS / FAIL

SaaS tests:
x/x

Python:
x/x

Build:
PASS / FAIL

Product defects found:

UX changes made:

Test changes made:

Residual issues:

Recommendation:
MERGE / FIX_REQUIRED

==================================================
