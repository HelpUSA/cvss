# HelpUS CVSS AI - Antigravity Round 3 master execution plan

## Decision before execution

`SAFE_TO_FREEZE = NO`

Do not start confirmatory C1/C2 execution yet.

The Round-2 return fixed important issues, but the latest independent audit still found internal blockers. This package supplies drop-in replacements for the changes that can safely be prepared without inventing external data.

## 1. Merge strategy

- Diff every file under `copy_into_repo/` against the real local repository.
- Copy the supplied file verbatim when the local file has not advanced beyond the Round-2 artifact.
- If the local repository is newer, merge by intent rather than blindly overwriting.
- Preserve unrelated local features.
- After merging, run the full repository test/build suite and update only current evidence-based status documents.

## 2. Immediate drop-in source replacements

Apply/merge:

- `web/src/lib/jcs.ts`
- `web/scripts/test_jcs_conformance.ts`
- `web/src/app/api/analyze-environment/route.ts`
- `web/scripts/test_analyze_route.ts`
- `.github/workflows/real-pipeline.yml`
- `.gitignore`
- `tests/test_gitignore_contract.py`
- `scripts/check_execution_package_consistency.py`
- `scripts/upgrade_dataset_b_provenance_schema.py`
- `scripts/validate_dataset_b_provenance_v2.py`

## 3. JCS/RFC 8785

The supplied canonicalizer fixes the missing lone-surrogate validation and retains recursive object sorting, array preservation, finite-number enforcement, and deterministic UTF-8 hashing behavior.

However, local contract tests are not enough to state formal RFC 8785 conformance.

Required before claiming conformance:

- pin an independent JCS/RFC 8785 corpus or established implementation/version;
- run the complete applicable corpus;
- store raw canonical-byte comparisons;
- store corpus revision;
- regenerate the conformance report automatically.

Until then public/document wording must say:

`JCS-compatible canonicalization implementation; formal RFC 8785 conformance pending pinned corpus validation.`

## 4. P0-P4 must be policy-driven

Remove direct endpoint logic such as:

- score >= 9 -> P0
- score >= 7 -> P1
- score >= 4 -> P2

The supplied route accepts a versioned `operationalPolicy.scoreBands` object.

If no operational policy is supplied:

- CVSS-BE inference may still complete;
- operational disposition must be `PENDING_POLICY_REVIEW`;
- do not guess P0-P4.

Operational policy should be versioned and auditable independently of the CVSS engine.

## 5. CR/IR/AR

Continue the current fail-safe rule:

- no direct PCI/payment/business-criticality -> CR/IR/AR hard-coding;
- values may be consumed only as an explicit resolved mapping associated with `organizationPolicyId` + `policyVersion`;
- if requirements are supplied without policy metadata, abstain.

Longer term, load the mapping from a server-side versioned policy registry instead of trusting arbitrary client-side values.

## 6. Calculator validation gate G1

The current 22-case suite is a smoke/regression suite only.

Do not describe it as the complete FIRST reference corpus.

Pin a commit of:

`https://github.com/FIRSTdotorg/cvss-resources`

The FIRST repository explicitly identifies `vectorFiles` as CVSS v4.0 calculator validation resources.

Required:

- repo URL;
- exact commit SHA;
- exact files consumed;
- valid-case total;
- negative-case total;
- one raw row per vector/case;
- expected score/rejection;
- observed score/rejection;
- delta;
- PASS/FAIL;
- parser errors must fail, not silently skip;
- zero unexplained mismatches.

Also pin:

- Python calculator package/version;
- package/repository commit where available;
- frontend calculator package/version;
- backend/frontend parity corpus.

G1 remains FAIL/PENDING until this is complete.

## 7. Dataset B provenance - schema v2

The current single Dataset B is structurally better, but CVSS-BT rows still conflate two concepts:

1. provider-reported Base-only score/severity;
2. score recomputed from the complete source vector containing Threat metrics.

Apply/run:

- `scripts/upgrade_dataset_b_provenance_schema.py`
- manually re-audit provider-reported facts from source records;
- set `provider_reported_score_audit_status=AUDITED` only after verification;
- run `scripts/validate_dataset_b_provenance_v2.py`.

Required fields:

- `source_cvss_v4_vector`
- `source_nomenclature`
- `provider_reported_base_score`
- `provider_reported_base_severity`
- `provider_reported_score_audit_status`
- `recomputed_full_vector_score`
- `recomputed_full_vector_severity`
- `score_semantics`

Do not infer a provider Base score from a BT vector.

In summaries/tables rename ambiguous `Base Vector` headings to `Source CVSS v4.0 Vector` when the vector may include Threat metrics.

After audit, regenerate from the single source of truth:

- CSV/JSON;
- Markdown provenance summary;
- Book tables;
- figures;
- Web fixtures;
- statistics.

## 8. Portable artifact reproducibility G2

Distinguish:

- repository-full profile;
- portable-ZIP profile.

The portable artifact must run after clean extraction without `.git`, machine-specific paths, or undeclared global dependencies.

The supplied Git contract test now explicitly skips the repository-only assertion when `.git` metadata is absent.

Include in the final artifact:

- `requirements.txt` / `pyproject.toml` plus a documented Python lock strategy;
- Node `package-lock.json`;
- importable `core/` and `app/` trees;
- required `.github/workflows/real-pipeline.yml` if workflow tests are shipped;
- all portable test dependencies;
- no `D:/...` or other absolute paths;
- raw clean-extraction logs.

Report separately:

`repository-full: X passed / Y failed / Z skipped`

`portable-artifact: X passed / Y failed / Z skipped`

Do not claim a ZIP reproduces N/N passes if it cannot execute those tests independently.

## 9. HITL / SuperAdmin claim

The Round-2 API correctly states `authorization_enforced_by_this_route=false`.

Therefore `SuperAdmin enforcement proven` is not supported by this route alone.

In the real repository, either provide testable enforcement evidence for:

- server-side authentication/session validation;
- issuer/audience validation if applicable;
- verified identity state;
- server-side role lookup;
- protected review mutation;
- unauthenticated rejection;
- authenticated non-authorized rejection;
- authorized approval/rejection success;
- reviewer identity in the receipt;
- no client-only authorization decision;

or reduce all public/document claims to:

`human review required`.

Use `HITL_AUTHORIZATION_EVIDENCE_REQUIREMENTS.md`.

## 10. Production website G8

Verify the actual custom domain:

`https://cvss.helpusbr.com`

Do not close G8 because a temporary Vercel alias contains newer code.

Perform PT/EN/ES smoke tests after the custom-domain deployment is active.

Use `PUBLIC_SITE_COPY_ROUND3.md` as restrained replacement copy.

Remove/qualify unsupported phrases including:

- 30 validated scenarios;
- 100% correctness/agreement;
- zero hallucination;
- mathematical guarantee;
- immutable proof/contract;
- guaranteed compliance;
- development-stage 25% presented as validated noise/false-positive reduction.

Also verify the public UI does not display a stale freshness rule (for example `<300s`) while the actual engine uses a different policy.

## 11. Freshness policy

Create one versioned freshness policy consumed by:

- Python core;
- Web API;
- UI copy;
- tests;
- protocol docs.

Store:

- policy ID;
- version;
- evidence class/profile;
- threshold;
- effective date.

Do not leave separate 300-second vs 1-day/7-day semantics unless they are explicitly different named evidence classes.

## 12. Documentation cleanup G7

Apply the supplied docs under `docs/scientific-validation/`.

Make `CURRENT_RELEASE_GATE_STATUS.md` the only authoritative status page.

Archive stale Round-1/Round-2 status/completion documents under an archive tree instead of leaving mutually contradictory current files.

Use `DOCS_ARCHIVE_PLAN.md`.

Current status must not simultaneously say:

- G1-G8 PASS;
- full FIRST corpus pending;
- website sync pending;
- source re-audit pending.

## 13. Expert count

Resolve once before protocol freeze.

Round-3 recommendation: 5 independent experts if recruitment/resources allow.

If the final decision is 5, update every current protocol/TODO/ethics/custody/manuscript method document to 5.

If 5 is infeasible, amend the protocol before viewing held-out results and use the chosen count consistently.

Do not change the count after C1/C2 results are observed.

## 14. Book baseline

Use the accompanying Round-3 Overleaf ZIP as the new textual baseline.

It already:

- clarifies development-only Dataset B;
- states full calculator/source/held-out/ethics validation remains pending;
- makes P0-P4 explicitly organization-policy driven;
- removes implication that cryptographic signing is automatically required/implemented for risk acceptance;
- clarifies legacy `Defer` values as operational-development labels rather than CVSS severity;
- moderates enterprise-preset validation wording.

Local build result:

- 41 pages;
- 0 undefined citations;
- 0 undefined references;
- 0 overfull hboxes.

After Dataset B provenance v2 is fully audited, regenerate Appendix C/Table 6.1 again from the canonical dataset.

## 15. Ethics and external validation

Do not fabricate or auto-close:

- CEP/IRB/ethics determination;
- signed consent;
- signed COI;
- expert scores;
- adjudication;
- C1/C2 held-out results;
- public preregistration.

These remain external/procedural gates.

## 16. C1/C2 remain blocked

Do not reveal/run C1/C2 until internal gates are actually closed and engine/rules/policies/calculators/dependencies/protocol are pinned.

If engine behavior changes after viewing held-out scenarios, the set is no longer confirmatory held-out data and a new set is required.

## 17. Required final return package

Return one self-contained artifact containing:

1. exact changed-file list;
2. Git diff/stat;
3. Git SHA;
4. Python/Node lock/dependency files;
5. raw repository-full test log;
6. raw portable-artifact test log;
7. pinned FIRST repository commit;
8. raw full FIRST vector-corpus results;
9. raw negative-case results;
10. backend/frontend parity results;
11. JCS independent-conformance results;
12. canonical Dataset B v2;
13. provider source-audit evidence/summary;
14. generated book tables/macros;
15. authenticated HITL authorization tests or reduced claim;
16. custom-domain PT/EN/ES production smoke evidence;
17. fresh final Book PDF;
18. final Overleaf ZIP;
19. final build manifest matching those exact bytes;
20. updated `docs/scientific-validation/current/`;
21. archive of stale prior-round status docs;
22. remaining external TODOs;
23. explicit gate table G1-G10;
24. final statement `SAFE_TO_FREEZE = YES` or `NO` with evidence-based justification.

## 18. Freeze rule

Do not optimize the protocol after seeing held-out results.

Do not alter reports to match desired conclusions.

Do not replace absent source facts with inferred values.

A release gate passes only when the current artifact contains machine-readable evidence that supports the claim.
