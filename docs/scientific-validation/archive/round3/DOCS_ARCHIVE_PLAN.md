# Scientific-validation documentation archive plan

The current package contains status documents from multiple historical rounds. Before freeze:

1. Create:
   - `docs/scientific-validation/current/`
   - `docs/scientific-validation/archive/round1/`
   - `docs/scientific-validation/archive/round2/`

2. Put the authoritative current documents under `current/` or keep a single top-level pointer:
   - `CURRENT_RELEASE_GATE_STATUS.md`
   - `EXPERIMENT_PROTOCOL_v1.0_DRAFT.md`
   - `HELDOUT_CUSTODY_PROTOCOL.md`
   - `BENCHMARK_RERUN_POLICY.md`
   - `FIRST_REFERENCE_CORPUS_GATE.md`
   - `JCS_CONFORMANCE_GATE.md`
   - `DATASET_B_PROVENANCE_SCHEMA_V2.md`
   - `PORTABLE_ARTIFACT_PROFILE.md`
   - `EVIDENCE_QUALITY_PROTOCOL.md`
   - `ETHICS_REVIEW_CHECKLIST.md`
   - `EXPERT_COI_FORM.md`
   - `EXPERT_CONSENT_TEMPLATE.md`

3. Move stale/contradictory Round-1/Round-2 completion summaries to archive. Do not delete them if they are useful provenance.

4. `CURRENT_RELEASE_GATE_STATUS.md` is the only authoritative source for PASS/PARTIAL/FAIL/PENDING states.

5. Resolve the expert count once in the final protocol. Do not allow `3 experts` and `5 experts` in simultaneous current documents.
