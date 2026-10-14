# HelpUS CVSS — FIRST-Aligned Guided UX

**Status:** implementation + production audit guidance  
**Scope:** public site and operational SaaS UX only  
**Frozen deterministic baseline:** `007fe79a6cd0e843fe6a9f837444720e23a4bcad`

## 1. Problem observed

The product had accumulated several different purposes on the same screens:

- scientific demonstration;
- operational SaaS;
- research metrics;
- infrastructure scanner concepts;
- mitigation/what-if concepts;
- authentication and administration;
- older mandatory HITL/expert-review language.

This makes it difficult for a first-time operator to know what to do next.

The preferred product rule is:

> One practical question per page, one obvious next action, and optional detail only when the user asks for it.

## 2. FIRST patterns adopted

The UX should feel familiar to users who already know the FIRST CVSS v4.0 resources.

Relevant FIRST patterns:

1. Separate metric groups and concepts rather than present one undifferentiated risk score:
   Base, Threat, Environmental and Supplemental.
2. Show human-readable metric names together with abbreviations.
3. Keep the vector visible and preserve the source vector.
4. Display score nomenclature:
   `CVSS-B`, `CVSS-BT`, `CVSS-BE`, `CVSS-BTE`.
5. Put contextual help close to the question/metric.
6. Link directly to the Specification, User Guide, Examples and reference calculator.
7. Treat CVSS Base as severity, not as a complete organizational risk score.
8. For consumers, enrich vulnerability data with asset/environment data.

HelpUS should follow those concepts without copying the FIRST calculator layout literally.

## 3. HelpUS operational workflow

The practical path is now:

1. **Organization** — choose the tenant.
2. **Project** — define the system/product scope.
3. **Environment** — define where it is deployed.
4. **Assessment** — bind a CVE/vulnerability to the environment.
5. **Origin + evidence** — preserve CVSS-B and submit verifiable environmental facts.
6. **Result/history** — review CVSS nomenclature, vector, evidence hash, run receipt and prior runs.

The tenant “Comece aqui” page is the roadmap. Individual pages handle the actual work.

## 4. Progressive disclosure

Do not place all advanced concepts on the first screen.

### Public home

Only answer:

- What is HelpUS?
- What is the practical flow?
- Do I want a demo or the authenticated workspace?

### Demo

Only show enough fields to demonstrate:

- CVE;
- source vector;
- source provider;
- reachability;
- evidence quality/freshness;
- result or ABSTAIN.

No tenant persistence and no research dashboard.

### Workspace

Each page advances one stage:

- Projects;
- Environments;
- Assessments;
- Evidence/execution;
- Results/history.

### Advanced detail

Keep rule hashes, build hashes, raw receipts, policy versions and audit data on result/detail screens, not on the entry screen.

## 5. Governance language

The primary system is autonomous-by-default and deterministic.

Remove from current operational UX:

- mandatory expert review;
- mandatory HITL;
- claims that AI agents directly calculate CVSS;
- claims that a human must approve every score;
- “ground truth by expert” as a primary-study dependency.

Allowed:

- optional organizational review workflow;
- Reviewer role for an organization whose policy requires review;
- historical human-study material preserved as legacy/optional research documentation.

The UI should say:

`Review is optional according to organizational policy and never changes CVSS arithmetic.`

## 6. AI language

The frozen primary architecture does not require an LLM at runtime.

Operational UI should not say:

- “AI calculates the score”;
- “AI extracts the metric and decides the score”;
- “AI expert gate”.

Preferred wording:

- deterministic rules resolve supported metric candidates;
- deterministic CVSS scorer calculates the score;
- optional AI assurance, if later enabled, is secondary/non-authoritative.

## 7. Production-site mismatch observed

The publicly reachable site at `https://cvss.helpusbr.com` was observed serving an older, much denser experience containing language/features such as:

- “AI Watcher”;
- “Priorização de Risco com IA”;
- “Gate de Homologação Humana”;
- “Acesso Exclusivo SuperAdmin Master”;
- “Aprovação HITL”;
- scientific Dataset B content mixed with operational UI;
- multiple scanner/what-if/policy-as-code features on the same public page.

This does not match the current SaaS architecture or the non-human primary-study governance.

Antigravity must verify which deployment/project/domain currently serves this content and ensure the production domain is rebuilt from the canonical current branch after this PR merges.

Do not merely patch the old HTML. Confirm the production deployment source.

## 8. Current implementation in this UX round

Implemented:

- new minimal public landing at `/`;
- public stateless demo moved to `/demo`;
- demo payload fixed to use `sourceAssessmentMeta`;
- tenant `/guide` “Comece aqui” roadmap;
- explicit step numbering in Projects and Environments;
- new Assessments list/create page;
- new assessment evidence/execution page;
- new run result/history page;
- FIRST nomenclature helper;
- next-action recommendation on tenant overview;
- simplified workspace organization selection;
- Google-only login wording;
- removal of mandatory human-review semantics from the TypeScript operational analysis service;
- stale AI/HITL wording removed from reusable quick-guide/methodology components.

## 9. Result-page standard

Every published/displayed CVSS score should, wherever technically possible, show:

- score;
- vector;
- nomenclature;
- source/provider;
- whether environmental metrics were used.

Do not publish a naked numeric score when the vector/nomenclature is available.

## 10. Next UX increments

After this round:

1. inline metric glossary/help using FIRST definitions in concise paraphrase;
2. optional advanced section for CR/IR/AR policy-backed requirements;
3. tenant Evidence Library page;
4. optional tenant Review queue;
5. global SuperAdmin organization lifecycle UI;
6. distributed demo rate limiting;
7. production browser E2E through Google login;
8. accessibility and mobile walkthrough;
9. multilingual UX only after the Portuguese workflow is stable.

## 11. Acceptance path

A first-time authorized operator should be able to answer “what do I do next?” at every screen:

`Login -> Organization -> Comece aqui -> Project -> Environment -> Assessment -> Evidence -> Result`

If a user needs documentation to discover the next URL, the UX has failed.
