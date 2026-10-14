# Independent audit findings on the latest Antigravity execution package

## Decision

`SAFE_TO_FREEZE = NO`

## Verified positives

- ZIP integrity and supplied SHA-256 were consistent in the reviewed environment.
- The 42-page PDF in the Antigravity package was readable and the historical Fisher calculation was reproducible.
- The Python evidence engine incorporated major semantic improvements: internal routed reachability remains MAV:N; firewall presence does not automatically force MAC:H; high availability does not automatically force AR:L; explicit versioned policy is required for CR/IR/AR in the core engine.
- The project now has substantially better experimental-governance documentation.

## Blocking findings

1. **The delivered ZIP did not independently reproduce the advertised `119/119` test result.** Direct pytest collection failed because dependencies/package layout/full `app` tree were not included and a parity test contained a machine-specific `<repo>/web` path.
2. **Concrete Python bug:** `code_core/cvss_environmental_engine.py` called `score()` on the abstention path but did not import it.
3. **The Web route labeled a `JSON.stringify(..., sorted top-level keys)` construction as RFC 8785/JCS.** That is not recursive JCS and can omit nested evidence fields from the hash.
4. **The Web endpoint used permissive scientific defaults when evidence was omitted**, contradicting `missing evidence -> HUMAN_REVIEW_REQUIRED`.
5. **Web CR/IR fallback rules remained embedded in the route** (`pciScope/payment -> CR:H`, `businessCriticality -> IR:H`) rather than being loaded from a versioned organization policy mapping.
6. **The package did not prove SuperAdmin/HITL authorization enforcement.** It returned HITL flags but the route artifact did not demonstrate authentication/role checks or an authorized transition.
7. **Dataset B mismatch:** `03_DATASET_B_PROVENANCE_SUMMARY.md` described a 2023/2024 CVE set, while the actual CSV and book used a different 2026 CVE set.
8. **The alternate 2023/2024 list does not automatically solve CVSS v4 source provenance.** Several well-known records are commonly published with v3.1 source assessments; a v4 benchmark must use source-backed v4 records or mark investigator-authored assessments explicitly.
9. **Test-count reporting was ambiguous** because subsets (parity, smoke, etc.) were presented alongside the overall count without clarifying overlap.
10. **Stale build manifest:** a `docs` manifest described a different PDF hash/size/TeX toolchain than the PDF actually delivered.
11. **Fresh LaTeX rebuild did not reproduce the “0 overfull hboxes” statement.** The previous package produced layout warnings and visible clipping/overflow in some areas.
12. **Appendix C still mixed CVSS-like labels with `Defer`**, despite the conceptual separation between CVSS severity and local operational disposition.
13. **Historical terminology remained inconsistent:** conventional citation should be Allodi et al. (FDSE 2017); the study is a CVSS v3.0-era human-factors baseline, not a v4 ground truth.
14. **The book still used wording stronger than the actual calculator provenance**, e.g. “official FIRST engine,” although the implementation is a third-party/pinned library that still requires full reference-corpus validation.
15. **Unused/unverified bibliography entries remained.** An artifact for a top-tier venue must not contain unverifiable citations.
16. **The public Web site still showed development-stage claims as scientific validation**, including strong 30-scenario/100%/immutable/deterministic language that is inconsistent with the current protocol.
17. **Documentation drift:** expert count, freshness thresholds, Next.js version, external-action count, ethics filename, and other details differed across reports.

These findings must be reconciled in the real repository before the experimental freeze.
