# Round 4 Master Execution Plan

## Objective

Close the remaining **internal** pre-freeze blockers without fabricating evidence. Do not run confirmatory C1/C2 yet.

## Phase A — Repair G1: calculator conformance

1. Pin the exact FIRST `cvss-resources` commit used for `vectorFiles`.
2. Execute `scripts/run_first_reference_corpus_round4.py` and preserve every result/mismatch.
3. Do not waive ±0.1 mismatches.
4. Differentially compare the same 159 boundary cases with a pinned FIRST reference calculator implementation / official reference implementation if available.
5. If the current Python `cvss` scorer diverges while the FIRST reference implementation matches `vectorFiles`, replace/patch the scoring kernel rather than special-casing test vectors.
6. Re-run the entire valid + negative corpus.
7. G1 closes only with zero unexplained mismatches and machine-readable evidence.

## Phase B — Repair G2: portable artifact

1. Restore/include every package imported by tests, notably `app/`.
2. Include `.github/workflows/real-pipeline.yml`, `.gitignore`, Python dependency metadata, Node lockfile and all required scripts.
3. Remove absolute developer paths.
4. Use `scripts/build_portable_artifact_round4.py` to build the artifact.
5. Extract into a clean directory/environment and execute the portable profile.
6. Report repository-full and portable-artifact results separately, including skips and reasons.

## Phase C — G4 Web/JCS/HITL

1. Retain policy-driven P0–P4; no hard-coded direct CVSS-score mapping in the scientific API.
2. Run local JCS contracts and the RFC 8785 published example test.
3. Do not claim formal RFC 8785 conformance until validated against a pinned independent corpus.
4. Either provide reproducible authenticated/authorized HITL mutation tests (unauthenticated reject, unauthorized reject, authorized SuperAdmin accept/reject) or reduce claims to `human review required`.

## Phase D — G5 Dataset B synchronization

1. Treat `data/dataset_b/source_assessments_v2.csv` as the canonical Dataset B source.
2. Re-audit provider Base scores and source vector semantics.
3. Run `scripts/generate_dataset_b_round4_outputs.py`.
4. Generate book tables, provenance report and Web fixtures from the same source.
5. Verify scenario/CVE IDs across generated artifacts with `scripts/compare_dataset_ids_across_artifacts.py`.
6. Never collapse provider-reported Base and recomputed B+T full-vector score into one ambiguous field.

## Phase E — G7 documentation cleanup

1. Keep `CURRENT_RELEASE_GATE_STATUS.md` as the sole current status.
2. Move obsolete status/report documents to `archive/round1`, `archive/round2`, `archive/round3`.
3. Standardize n=5 expert wording.
4. Rebuild reports/manifests from raw outputs rather than editing PASS/FAIL text manually.

## Phase F — G8 production synchronization

1. Patch PT/EN/ES public copy using `PUBLIC_SITE_COPY_ROUND4.md`.
2. Remove unsupported certainty claims.
3. Ensure Dataset B production fixtures originate from schema v2.
4. Deploy to the **custom domain**.
5. Run `scripts/audit_public_site_claims_round4.py` against the custom domain and archive raw output.
6. Verify the production dataset does not surface stale CVEs/scenario IDs.

## Phase G — Final book rebuild

1. Use the Round-4 Overleaf baseline supplied with this package.
2. Regenerate Dataset B tables from the final canonical schema-v2 source.
3. Run the Round-4 book-term checker.
4. Fresh build: LaTeX -> BibTeX -> LaTeX -> LaTeX.
5. Require zero undefined references, zero undefined citations and zero overfull boxes.
6. Generate a new build manifest matching the exact PDF and ZIP bytes.

## Phase H — Reassess gates

Only after A–G, update the authoritative gate table. If G1–G8 pass and only G9/G10 remain, proceed to institutional/external steps. Do not expose C1/C2 before the technical and protocol freeze.
