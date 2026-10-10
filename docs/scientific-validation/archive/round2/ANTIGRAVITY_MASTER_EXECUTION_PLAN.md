# ANTIGRAVITY MASTER EXECUTION PLAN - HelpUS CVSS AI Round 2

## Objective

Apply the latest independent audit to the **real local repository**, `cvss.helpusbr.com`, `docs/scientific-validation/`, Dataset B, calculator validation, test infrastructure, and the monograph. Return one internally consistent artifact and an explicit release-gate decision.

**Current status: `SAFE_TO_FREEZE = NO`.**

Do not start C1/C2 held-out execution until all local technical/documentary gates below pass.

---

## Absolute rules

1. Do not invent results, source vectors, compliance, expert decisions, ethics approval, scores, latency, or statistical outcomes.
2. Do not edit a report to make tests appear successful. Reports must be generated from raw artifacts.
3. Do not silently convert CVSS v3.1 to v4.0.
4. Dataset B is development/regression data, not independent validation.
5. C1/C2 remain prospective until the final freeze.
6. If a previously held-out set is used to tune rules, it is no longer held-out.
7. Preserve all source provenance and version information.

---

# PHASE 1 - Integrate the book baseline

Use the separate ZIP:

`helpus_cvss_ai_monograph_overleaf_chatgpt_round2.zip`

as the new **pre-freeze monograph baseline**.

Do not overwrite its corrections with older chapter files.

The book already applies these changes:

- Allodi et al. / FDSE 2017 metadata and historical framing;
- CVSS v3.0-era study separated from v4 confirmation;
- Dataset B development-only language;
- source assessment terminology instead of blanket NVD authorship;
- specification-conformant/pinned calculator wording instead of “official FIRST engine”;
- corrected fail-safe formulation;
- no unsupported universal 1.5 ms/10 us claim;
- exploratory EPSS moved out of the confirmatory contribution;
- exact historical CI method and generated macros;
- Appendix C separates legacy development labels from P0-P4 disposition;
- unused/unverified bibliography entries removed;
- fresh build in the review environment: zero overfull boxes and zero undefined citations/references.

After Dataset B reconciliation, regenerate the book again from the canonical dataset. Do not hand-edit numeric tables.

---

# PHASE 2 - Fix the Python core bug and add path coverage

## 2.1 `core/cvss_environmental_engine.py`

The delivered artifact had a concrete bug:

- abstention branch called `score()`;
- module imported only `compare`.

Apply the supplied replacement/reference patch:

`patch_files/code_core/cvss_environmental_engine.py`

Minimum change:

```python
from core.cvss40 import compare, score
```

## 2.2 Add regression test

Integrate:

`patch_files/tests/test_cvss_environmental_abstention_path.py`

This must execute `calculate()` with insufficient evidence and verify that it returns an abstention result rather than raising `NameError`.

## 2.3 Coverage expectations

Add/retain end-to-end coverage for:

- valid Environmental inference;
- abstention path;
- invalid v3/numeric-only input;
- source scoring;
- candidate synthesis;
- calculator call;
- no automatic downgrade on insufficient evidence.

---

# PHASE 3 - Make the artifact independently reproducible

The previous ZIP did not reproduce `119/119` when executed outside the original workstation.

## 3.1 Package structure

Tests must import exactly the package tree shipped in the artifact.

Do not ship:

`code_core/`

while tests import:

`core.*`

unless an installation/build step explicitly performs that mapping.

Preferred final artifact:

```text
repo/
  core/
  app/
  web/
  tests/
  scripts/
  docs/
  pyproject.toml / requirements lock
  package.json
  package-lock.json
```

## 3.2 Python dependencies

Include the actual dependency definition and lock/pin strategy used by the repository.

The artifact must install the exact CVSS, SciPy and test dependencies from documented commands.

## 3.3 Node dependencies

Include the actual lockfile and pinned Node/npm versions.

Current documentation must match the actual `package.json`; do not describe Next.js 14 if the project uses Next.js 15.5.x.

## 3.4 Remove machine-specific paths

Remove paths such as:

`<repo>/web`

from tests/scripts.

Use repository-relative paths based on the test file/project root.

## 3.5 Raw logs

Return raw logs for:

- complete pytest run;
- Node tests/typecheck/build;
- parity tests;
- calculator corpus;
- dataset validation;
- book build;
- production smoke tests.

## 3.6 Test counting

Report a single overall full-suite count.

Example:

`pytest full collection: 119 passed`.

If parity=19 and smoke=10 are subsets of those 119, explicitly label them `overlapping subsets`; do not present them as additional independent tests.

---

# PHASE 4 - Replace pseudo-JCS with real canonicalization

The delivered Web route used:

```ts
JSON.stringify(auditPayload, Object.keys(auditPayload).sort())
```

and labeled it RFC 8785/JCS.

That is unacceptable because sorting only the top-level replacer is not recursive and may exclude nested evidence keys from the serialized receipt.

## Required action

Integrate a proper recursive RFC 8785/JCS implementation or a vetted JCS package.

The package contains a review implementation:

`patch_files/code_web/lib/jcs.ts`

and contract examples:

`patch_files/tests/jcs_contract_examples.ts`.

These are a starting point. Before production claims of RFC 8785 conformance:

1. pin the canonicalization implementation/version;
2. execute a formal JCS/RFC test corpus;
3. store raw conformance results;
4. test nested objects, arrays, Unicode, number serialization and rejection of non-JSON finite values.

The hash must cover the full nested evidence object.

---

# PHASE 5 - Remove permissive scientific defaults from the API

The previous route silently supplied a default CVE, vector, evidence quality, telemetry age, reachability, policy ID and asset properties.

This directly violates fail-safe semantics.

Apply the principles in:

`patch_files/code_web/api/analyze-environment/route.ts`.

The production endpoint should require explicit:

- `cveId`;
- `baseVector`;
- source provenance metadata;
- evidence object;
- evidence quality;
- evidence timestamp/age policy inputs;
- reachability evidence.

Missing evidence must never become `SUFFICIENT` by default.

Demo presets may be implemented only as explicit fixtures selected by the UI and marked as synthetic/demo in provenance.

---

# PHASE 6 - Remove public manual metric overrides

Do not allow an untrusted request to set `MAV`, `MAC`, CR/IR/AR, etc. through arbitrary `manualOverrides` on the scientific analysis endpoint.

Reviewer override must be a separate authenticated HITL action with:

- authenticated reviewer;
- authorization check;
- previous value;
- proposed value;
- rationale;
- timestamp;
- incident/change ticket;
- policy/ruleset version;
- audit receipt.

---

# PHASE 7 - Versioned CR/IR/AR policy mapping

The Python core already moved in the correct direction.

The Web implementation must match it.

Remove route-local rules such as:

- `pciScope -> CR:H`;
- `payment -> CR:H`;
- `businessCriticality=high -> IR:H`.

Instead load/apply a versioned organization policy:

```text
organization_policy_id
policy_version
effective_date
security_requirements mapping
```

The same policy must be used in expert materials when CR/IR/AR are evaluated.

Compliance scope is evidence to a local policy; it is not itself a CVSS metric value.

---

# PHASE 8 - Prove HITL authorization instead of only returning flags

The previous endpoint returned:

- `humanReviewGate`;
- `hitlSupervisionRequired`.

That does not prove authorization enforcement.

If production claims SuperAdmin or authorized-reviewer enforcement, the artifact must demonstrate:

1. authenticated session;
2. permission/role check;
3. protected approval/rejection transition;
4. unauthorized request denial;
5. audit event bound to authenticated identity;
6. receipt/provenance of final decision.

If this exists elsewhere in the full repo, include the code/tests/evidence in the next artifact.

If it does not exist, change claims to:

`human review required` / `authorization enforcement pending integration`.

---

# PHASE 9 - Reconcile Dataset B to ONE canonical corpus

This is a release blocker.

The previous return package had:

- Markdown summary using 2023/2024 CVEs;
- CSV/book using 2026 CVEs.

Choose one canonical Dataset B and make it the single source of truth.

## 9.1 Canonical files

Recommended:

```text
data/dataset_b/scenarios.json
data/dataset_b/source_assessments.json
```

or a single carefully versioned CSV/JSON pair generated from one source.

## 9.2 Verify every real-CVE assessment

For all 12 real-CVE rows record:

- CVE;
- affected product;
- assessment provider;
- CVSS version;
- full source vector;
- nomenclature B/BT/etc.;
- score;
- severity;
- source URL/record ID;
- published/update/retrieval time;
- origin type.

## 9.3 Origin enum

Use at least:

- `CNA_PUBLISHED`
- `NVD_ANALYZED`
- `INVESTIGATOR_AUTHORED`
- `SYNTHETIC`

## 9.4 CVSS v3.1 records

Do not call a v3.1 source vector a source-backed v4.0 record.

Do not convert automatically.

For the main v4 benchmark, preferably replace those records with actual source-backed v4 assessments.

## 9.5 B vs BT

If `E:P/E:A/E:U` or another explicit Threat metric is present, preserve the actual nomenclature and do not call it pure CVSS-B.

## 9.6 Automated equality gate

Create a test that asserts the scenario IDs/CVEs/counts used by:

- canonical data;
- Markdown report;
- LaTeX table;
- Web fixtures

are generated from or equal to the same canonical dataset.

---

# PHASE 10 - Calculator validation against a full pinned corpus

The 10-vector suite is only a smoke/regression test.

Before freeze:

1. pin the Red Hat `cvss` package version/repository information;
2. pin a specific FIRST/reference resource revision;
3. execute the complete applicable valid-vector set;
4. execute negative/invalid vectors;
5. emit machine-readable results;
6. document passed/failed counts and every mismatch;
7. compare backend and Web outputs on a broader shared corpus.

Do not call the third-party library `official FIRST engine`.

Recommended wording:

`pinned CVSS v4.0 implementation evaluated against FIRST reference resources`.

Any unexplained score mismatch blocks freeze.

---

# PHASE 11 - Synchronize the public Web site

Review all PT/EN/ES copy.

Remove/qualify:

- “30 cenários validados”;
- “100% concordância”;
- “100% correto”;
- “zero hallucination”;
- “guaranteed” / “garantia” language unsupported by experiment;
- “immutable proof”;
- guaranteed compliance;
- development `25%` or historical `60%` as validated effectiveness/noise-reduction KPIs.

Use:

- `Dataset B - development benchmark`;
- `held-out independent validation pending`;
- `deterministic given the same versioned inputs/rules`;
- `tamper-evident receipt` where appropriate;
- `supports audit/governance` rather than `proves compliance`.

Capture production smoke-test evidence after deployment in PT/EN/ES.

---

# PHASE 12 - Book/Overleaf synchronization

After canonical Dataset B is complete:

1. regenerate all Dataset B tables from the canonical machine-readable source;
2. regenerate figures;
3. regenerate LaTeX numeric macros;
4. rerun Fisher script/macros;
5. build from a clean directory;
6. run bibliography;
7. ensure:
   - 0 undefined citations;
   - 0 undefined references;
   - 0 overfull boxes;
8. render all pages and visually inspect landscape tables/algorithms;
9. generate a fresh `BUILD_MANIFEST.json` from the final delivered files.

Do not reuse an older manifest.

The supplied Round 2 Overleaf ZIP is the baseline for these changes.

---

# PHASE 13 - Historical 2017 terminology

Across book, Web, docs and reports:

Use conventional reference:

`Allodi et al. (FDSE 2017)`.

Describe the sample consistently with the source as 29 MSc students unless the original experiment artifacts provide a more precise supported characterization.

Treat the 2017 corpus as a CVSS v3.0-era human-factors baseline.

It is not a CVSS v4.0 gold standard.

If later re-annotated under v4.0, that is a separate Dataset A2.

---

# PHASE 14 - Bibliography audit

Revalidate every cited item.

Remove unused/unverified entries.

Check:

- authors;
- title;
- venue;
- year;
- DOI/source;
- claim support.

Do not reintroduce the previously suspect Munaiah/Manadhata/SSVC entries unless independently verified and actually cited.

---

# PHASE 15 - Freshness policy consistency

Unify:

- Python core;
- Web endpoint;
- protocol;
- evidence-quality document;
- tests.

Use a versioned evidence freshness policy rather than inconsistent values such as 300 seconds in one report and 1/7 days in another.

Store:

- freshness policy ID/version;
- telemetry profile;
- threshold used;
- evidence timestamp.

---

# PHASE 16 - Documentation reconciliation

Update `docs/scientific-validation/` using `DOCS_UPDATE_MATRIX.md`.

Specific inconsistencies to eliminate:

- 3 experts vs 5 experts;
- 300 seconds vs 1/7 days;
- Next.js 14 vs 15.5.x;
- “3 external actions” while listing 4;
- references to missing `IRB_ETHICS_PROTOCOL.md`;
- stale PDF/build hashes;
- stale conformance results;
- `official FIRST engine` terminology.

---

# PHASE 17 - Build manifest

Generate at the END of the pipeline.

Include at minimum:

- Git SHA;
- branch/release;
- Python version;
- Node/npm version;
- dependency lock hashes;
- calculator version;
- ruleset version;
- organization-policy version;
- canonical Dataset B hash;
- book source hash/ZIP hash;
- PDF hash/bytes/pages;
- build timestamp;
- TeX toolchain.

Manifest must match the exact delivered artifacts.

---

# PHASE 18 - Do not begin C1/C2 until all local gates pass

External activities remain pending:

- ethics/IRB/CEP determination;
- expert consent/COI;
- independent held-out scenario custody;
- expert pre-adjudication ratings;
- adjudication;
- C1 evaluation;
- C2 evaluation;
- public preregistration if claimed.

Do not fabricate completion.

---

# Required final return package

Return a new package containing:

## A. Repository evidence
- exact changed-file list;
- Git diff/stat;
- commit SHA;
- branch;
- lockfiles;
- toolchain versions.

## B. Tests
- raw complete pytest log;
- raw Node test/typecheck/build logs;
- backend/frontend parity raw results;
- JCS conformance result;
- full calculator reference-corpus result;
- dataset consistency tests.

## C. Dataset
- canonical Dataset B source;
- provenance audit;
- generated summary;
- proof that book/Web/report are synchronized.

## D. Web
- deployed commit/version;
- API sample requests/responses for:
  - valid evidence;
  - missing evidence;
  - stale evidence;
  - conflicting evidence;
  - unauthorized HITL action;
- PT/EN/ES smoke-test evidence.

## E. Book
- final PDF;
- final Overleaf ZIP;
- clean build log/report;
- fresh build manifest.

## F. Scientific docs
- updated `docs/scientific-validation/` tree;
- external TODO list;
- final gate report.

## G. Final explicit decision

End the report with exactly one of:

`SAFE_TO_FREEZE = YES`

or

`SAFE_TO_FREEZE = NO`

and list every remaining blocker.

---

# Final principle

Do not optimize for a favorable result. Optimize for an artifact that a skeptical external reviewer can reproduce and audit.

Only after the repository, data, Web, book and documentation are internally consistent should the project move from pre-freeze engineering into the independent held-out experiment.
