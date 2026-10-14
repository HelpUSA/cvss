# Repository docs update matrix

Copy/update the following under `docs/scientific-validation/` in the real project.

| Document | Required update |
|---|---|
| `README_ANTIGRAVITY_FIRST.md` / return manifest | State latest gate status and canonical artifact hashes only. |
| `CVSS_CALCULATOR_PROVENANCE.md` | Pin real package/repo/version/commit; do not call third-party implementation “official FIRST”. |
| `CVSS_V4_CONFORMANCE_REPORT.md` | Regenerate from full pinned reference corpus + negative tests. Keep 10-vector suite as smoke only. |
| `DATASET_SOURCE_AUDIT.md` | Reconcile to one canonical Dataset B and document every source-backed v4 assessment. |
| `EXPERIMENT_PROTOCOL_v1.0_DRAFT.md` | Keep C1/C2 prospective; reconcile expert count, freshness policy, eligibility, CI method and ethics status. |
| `HELDOUT_CUSTODY_PROTOCOL.md` | Preserve zero-retuning and C1/C2 custody. |
| `BENCHMARK_RERUN_POLICY.md` | Preserve technical-rerun vs retuning distinction. |
| `FAILURE_TAXONOMY.md` | Keep and use in future error adjudication. |
| `EVIDENCE_QUALITY_PROTOCOL.md` | Align freshness thresholds with the actual versioned policy used by core and Web. |
| `ETHICS_REVIEW_CHECKLIST.md` | Do not claim approval/exemption without formal institutional determination. |
| `EXPERT_COI_FORM.md` | Keep; reconcile panel size across all docs. |
| `EXPERT_CONSENT_TEMPLATE.md` | Keep; use only after institutional/ethical requirements are confirmed. |
| `TEST_REPORT.md` | Regenerate from raw full-suite logs; clarify overlapping subsets. |
| `LATEX_QUALITY_REPORT.md` | Regenerate from a fresh clean build; do not copy old warning counts. |
| `BUILD_MANIFEST.json` | Regenerate last from actual delivered files. |
| `WEB_APP_CHANGELOG.md` | Record exact production commit/deployment and copy changes. |
| `WEB_APP_REQUIRED_PATCHES.md` | Replace/update using `WEB_APP_REQUIRED_PATCHES_V2.md`. |
| `TODO_EXTERNAL_VALIDATION.md` | Keep outstanding ethics/experts/C1/C2/preregistration/custody items only; remove tasks actually completed. |
| `STATISTICAL_REPRODUCIBILITY_REPORT.md` | Preserve generated Fisher results and exact method labels; include script/tool versions. |
| `BOOK_CHANGELOG.md` | Merge the new book changes from `BOOK_CHANGES_APPLIED.md`. |
| `PROJECT_INVENTORY.md` | Correct Node/Next/Python/toolchain versions to match the actual repository. |

Also add the independent audit documents from this package so future work does not regress to the inconsistent state.
