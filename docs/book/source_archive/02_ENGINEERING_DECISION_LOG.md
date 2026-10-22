# HelpUS CVSS AI v4.0 — Engineering Decision Log

This log captures the architectural, algorithmic, and software engineering decisions made throughout the lifecycle of the project, including discarded paths and lessons learned.

---

### Decision ID: ENG-DEC-001
* **Date / Phase**: May 2026 / Phase 1
* **Context**: Initial implementation of the CVSS v4.0 calculator and contextual evaluation engine.
* **Observed Problem**: Directly mutating official CVSS metrics with local environment attributes risked producing non-standard vectors, breaking compliance with the FIRST standard.
* **Prior State**: Monolithic scoring prototypes intermingling Base metrics with operational flags.
* **Alternatives Considered**:
  1. Forking the official CVSS v4.0 specification to introduce direct score offsets.
  2. Maintaining a strict dual-engine architecture separating Official Base calculation from Environmental policy.
* **Decision Adopted**: Strict dual-engine decoupling formalized in `ADR-001-official-vs-contextual-separation.md`. The official core evaluates purely canonical vectors, while the contextual policy maps local evidence into Environmental metrics without mutating Base logic.
* **Rejected Alternatives & Rationale**: Alternative 1 was rejected because it would invalidate interoperability with NVD, CVE, and FIRST calculators.
* **Associated Implementation**: `core/cvss40.py` (official core) and `core/cvss40_environmental_policy.py` (contextual policy).
* **Validation**: 486,472 FIRST reference vector test suite ($100\%$ concordant).
* **Result**: Zero divergence from the FIRST standard.
* **Consequences**: Established clean architectural boundaries for all future research phases.
* **Limitations**: Environmental priority adjustments are bounded by the MacroVector lookup table discretization.
* **Commit / SHA**: Initial repository commits (pre-PR #8).
* **Related Correlation IDs**: `ADR-001`

---

### Decision ID: ENG-DEC-002
* **Date / Phase**: June 2026 / Metamorphic Testing
* **Context**: Need to verify algorithmic stability of the CVSS v4.0 implementation beyond static unit tests.
* **Observed Problem**: A standard unit test suite of hundreds of cases cannot exhaustively explore the combinatorial space of CVSS v4.0 vectors ($> 10^{10}$ combinations).
* **Prior State**: Static test vectors extracted from NVD.
* **Alternatives Considered**:
  1. Randomized fuzzing looking only for unhandled exceptions.
  2. Property-based metamorphic testing testing semantic invariance across vector transformations.
* **Decision Adopted**: Formalized 4 Metamorphic Relations (`MR-1` through `MR-4`) and built an automated test harness executing 10,000 randomized transformations.
* **Rejected Alternatives & Rationale**: Simple fuzzing was rejected because it does not verify numerical correctness or monotonicity of scoring logic.
* **Associated Implementation**: `tests/test_metamorphic_invariance.py` (Harness: `HELPUS-METAMORPHIC-10K-G9B`).
* **Validation**: 10,000 metamorphic executions.
* **Result**: $10,000 / 10,000$ executions passed with 0 invariant violations.
* **Consequences**: Provided mathematical proof of monotonic score behavior under impact transitions.
* **Limitations**: Metamorphic relations tested algorithmic properties of the scorer, not semantic truth of evidence.
* **Commit / SHA**: Milestone `HELPUS-METAMORPHIC-10K-G9B`.
* **Related Correlation IDs**: `REQ-METAMORPHIC-VERIFY-009`

---

### Decision ID: ENG-DEC-003
* **Date / Phase**: October 2026 / AI Bridge Local
* **Context**: Distributed multi-agent collaboration between local IDE (Antigravity), academic compiler (ChatGPT), and peer reviewer (Gemini).
* **Observed Problem**: Manual copy-pasting of complex technical reports between browser tabs introduced human transcription errors, dropped tokens, and latency.
* **Prior State**: Ad-hoc chat messaging across web interfaces.
* **Alternatives Considered**:
  1. Direct cloud API integration requiring third-party API keys and external infrastructure.
  2. Local lightweight HTTP Gateway (`127.0.0.1:8766`) with a strict JSON envelope (`ai_bridge_local.envelope`).
* **Decision Adopted**: Built `ai-bridge-local`, a local Python HTTP service with command queuing, token tracking, and correlation ID routing.
* **Rejected Alternatives & Rationale**: Direct cloud API was rejected to maintain local privacy, eliminate external credential leakage, and permit real-time browser session reuse.
* **Associated Implementation**: `d:\AntiG\ai-bridge-local` (`gateway_control_plane`, port 8766).
* **Validation**: Over 1,000 inter-agent dispatches successfully routed with status acknowledgments.
* **Result**: High-throughput, deterministic inter-agent communication pipeline.
* **Consequences**: Enabled fully auditable command logs across all agents.
* **Limitations**: Requires local background gateway process to remain active during collaboration.
* **Commit / SHA**: Local commits in `ai-bridge-local`.
* **Related Correlation IDs**: `HU-GEMINI-STD-ALIGN-048`, `REQ-ACADEMIC-STATUS-SYNC-027`

---

### Decision ID: ENG-DEC-004
* **Date / Phase**: October 2026 / PR #41 & PR #42
* **Context**: E2E testing of the web UI with Playwright.
* **Observed Problem**: Flaky E2E test failures caused by hydration races, client-side navigation timing, and database state pollution across viewport test runs.
* **Prior State**: Shared development database with non-deterministic timestamps.
* **Alternatives Considered**:
  1. Disabling E2E in CI and relying solely on unit tests.
  2. Disposable PostgreSQL instances per test run with deterministic auth cookies and mock tenant isolation.
* **Decision Adopted**: Implemented synthetic deterministic authentication (`test-only` Better Auth instance), seeded ephemeral PostgreSQL schemas, and synchronized pre-hydration DOM input values.
* **Rejected Alternatives & Rationale**: Disabling E2E was rejected because the web UI is a primary deliverable requiring production stability across mobile, tablet, and desktop.
* **Associated Implementation**: `tests/e2e/synthetic-auth.setup.ts`, `web/src/components/forms/management-form.tsx`.
* **Validation**: 3 consecutive green Playwright runs across Chromium, WebKit, and Mobile Chrome (390px).
* **Result**: Zero-flakiness E2E test pipeline.
* **Consequences**: Guaranteed that UI changes do not regress contextual vulnerability workflows.
* **Limitations**: Synthetic auth fixture restricted strictly to localhost/test databases.
* **Commit / SHA**: `ba529c6` (PR #41), `950a8f1` (PR #42).
* **Related Correlation IDs**: `PR-41`, `PR-42`

---

### Decision ID: ENG-DEC-005
* **Date / Phase**: October 2026 / Revision R2
* **Context**: Academic reviewers required machine-verifiable proof of trace integrity.
* **Observed Problem**: Verifying traces inside the runtime engine creates circular dependency (testing the code with the code itself).
* **Prior State**: Runtime assertions embedded in the application server.
* **Alternatives Considered**:
  1. Re-running the Next.js API in test mode.
  2. Standalone, zero-dependency Python verifier (`verify_trace_integrity.py`) executing 464 independent structural and recomputation assertions.
* **Decision Adopted**: Created `tools/verify_trace_integrity.py` with 18 companion unit tests. The verifier recomputes all scores independently from raw formulas.
* **Rejected Alternatives & Rationale**: Runtime API verification was rejected to ensure external auditors can verify traces without installing the full Node.js web stack.
* **Associated Implementation**: `tools/verify_trace_integrity.py`, `tests/test_verify_trace_integrity.py`.
* **Validation**: 464 checks evaluated across 30 traces ($100\%$ PASS).
* **Result**: Complete independent validation artifact (`r2_canonical_trace_verification.json`).
* **Consequences**: Provided verifiable empirical foundation for IEEE Revision R2.
* **Limitations**: Relied on open-world parsing; did not reject undeclared subobjects.
* **Commit / SHA**: `c41065e` (Revision R2 freeze).
* **Related Correlation IDs**: `CMD-CVSS-IEEE-R2-MACHINE-VERIFY-170`

---

### Decision ID: ENG-DEC-006
* **Date / Phase**: October 2026 / Revision R3
* **Context**: Need to rule out operator-selection bias in mutation testing.
* **Observed Problem**: Reviewers noted that structured mutants (M1–M8) might be tailored specifically to trigger known verifier checks.
* **Prior State**: 42 hand-crafted mutants.
* **Alternatives Considered**:
  1. Renaming structured mutants to sound random.
  2. Building an entirely separate, verifier-agnostic randomized mutation engine operating with a published fixed seed.
* **Decision Adopted**: Developed `tools/generate_random_mutations.py` with seed `20261021`, zero imports from the verifier, and 9 mutation operators (F1–F9).
* **Rejected Alternatives & Rationale**: Renaming was rejected as unscientific. An authentic randomized generator was required to genuinely test verifier robustness.
* **Associated Implementation**: `tools/generate_random_mutations.py`, `tools/run_randomized_mutations.py`.
* **Validation**: 120 applicable mutants generated across 6 scenarios; 83 rejected ($69.2\%$), 37 accepted ($30.8\%$).
* **Result**: Uncovered the F3 open-world boundary without altering code post-hoc.
* **Consequences**: Provided the pivotal empirical motivation for Schema v2.
* **Limitations**: Generated mutations operated on in-memory copies; canonical traces remained untouched.
* **Commit / SHA**: `073fa7d` (Revision R3 freeze).
* **Related Correlation IDs**: `CMD-CVSS-IEEE-R3-RANDOM-MUTATION-CANONICAL-181`

---

### Decision ID: ENG-DEC-007
* **Date / Phase**: October 2026 / Phase R6-2
* **Context**: External held-out corpus acquisition for top-tier A1 validation.
* **Observed Problem**: Ad-hoc scraping of advisories introduces temporal leakage and subjective cherry-picking.
* **Prior State**: Static 30 historical scenarios.
* **Alternatives Considered**:
  1. Manual curation of CVE records from October 2026.
  2. Fully automated, deterministic acquisition pipeline targeting GitHub Advisory Database with strict temporal boundaries.
* **Decision Adopted**: Implemented `tools/acquire_r6_heldout_corpus.py` fetching advisories published strictly between `2026-09-01T00:00:00Z` and `2026-10-01T00:00:00Z`, filtering for CVSS v4.0 metrics and excluding non-vulnerability malware notes.
* **Rejected Alternatives & Rationale**: Manual curation was rejected because it introduces human selection bias.
* **Associated Implementation**: `tools/acquire_r6_heldout_corpus.py`.
* **Validation**: Acquired 947 candidates, excluded 9 malware records, locked 938 eligible advisories.
* **Result**: Crytographically locked manifest in `validation/article/r6_heldout/` (SHA-256: `b09a8cc...`).
* **Consequences**: Created a true held-out corpus for future generalizability evaluation.
* **Limitations**: Corpus is held-out and quarantined; cannot be accessed during design phases.
* **Commit / SHA**: `2346859`, `12bf6c4`.
* **Related Correlation IDs**: `CMD-CVSS-IEEE-R6-A1-EXEC-ACQUIRE-226`

---

### Decision ID: ENG-DEC-008
* **Date / Phase**: October 2026 / Phase R6-1
* **Context**: Formalizing closed-world structural validation.
* **Observed Problem**: Open-world parsers silently accept arbitrary injected keys, creating parser differential vulnerabilities.
* **Prior State**: Schema v1 open-world validation.
* **Alternatives Considered**:
  1. Simple root-level `additionalProperties: false`.
  2. Recursive object-by-object closed-world policy with validated primitive and composite types (`TraceRoot`, `EnvironmentalEvidence`, `CompensatingControlItem`, `EvidenceLinkItem`).
* **Decision Adopted**: Implemented `core/r6_schema_v2_validator.py` enforcing strict object policies, namespaced extension points (`extensions: {}`), and prohibited reserved keywords (`delta_audit`).
* **Rejected Alternatives & Rationale**: Simple root-level check was rejected because it fails to catch injected attributes inside nested objects (`environmental_evidence`).
* **Associated Implementation**: `core/r6_schema_v2_validator.py`.
* **Validation**: 39 contract unit tests passing ($100\%$).
* **Result**: Robust closed-world validator that rejects undeclared properties.
* **Consequences**: Successfully formalizes the closed-world hypothesis for R6.
* **Limitations**: Stricter typing breaks unnormalized historical v1 traces that stored lists as narrative strings.
* **Commit / SHA**: `43664e5` (Implementation freeze).
* **Related Correlation IDs**: `CMD-CVSS-IEEE-R6-A1-IMPL-FREEZE-236`

---

### Decision ID: ENG-DEC-009
* **Date / Phase**: October 2026 / Phase R6-1
* **Context**: Operational exceptions required by enterprise change management.
* **Observed Problem**: Security teams sometimes need to override priority due to compensating factors not captured by standard formulas, tempting developers to add heuristic math to Equation 8.
* **Prior State**: Hardcoded priority overrides.
* **Alternatives Considered**:
  1. Introducing a continuous adjustment parameter ($\delta_{\text{audit}}$) into Equation 8.
  2. Structurally decoupled Governance Override Model ($OVR$) that logs authorization state, role, and justification without altering nominal formula scoring.
* **Decision Adopted**: Built `core/r6_governance_override.py`. The nominal score remains 100% pure; any operational override is recorded as an external, cryptographically traceable governance event.
* **Rejected Alternatives & Rationale**: Modifying Equation 8 was rejected to preserve FIRST conformance and mathematical purity.
* **Associated Implementation**: `core/r6_governance_override.py`.
* **Validation**: Unit tests verifying that override applications do not alter nominal Equation 8 outputs.
* **Result**: Auditable, enterprise-grade governance architecture.
* **Consequences**: Resolves the tension between operational flexibility and scientific compliance.
* **Limitations**: Overrides require Master SuperAdmin authorization to take effect.
* **Commit / SHA**: `43664e5`.
* **Related Correlation IDs**: `CMD-CVSS-IEEE-R6-A1-IMPL-FREEZE-236`

---

### Decision ID: ENG-DEC-010
* **Date / Phase**: October 2026 / Phase R6-A1 (T2 Execution)
* **Context**: Handling compatibility classification when canonical traces fail Schema v2 closed-world validation.
* **Observed Problem**: All 30 historical traces failed Schema v2 due to `INVALID_TYPE` (compensating controls stored as text) and `INVALID_ENUM` (empty `cve_id`), but the frozen taxonomy only had a category for `UNDECLARED_FIELD`.
* **Prior State**: 4-category compatibility taxonomy.
* **Alternatives Considered**:
  1. Silently coercing historical traces so they pass Schema v2.
  2. Forcing them into `V1_VALID_V2_INVALID_UNDECLARED_FIELD` even though the error was not an undeclared field.
  3. Fail-closed: Marking all 30 as `UNCLASSIFIED_BY_FROZEN_COMPATIBILITY_MODEL`, freezing original T2 artifacts, and logging a formal protocol deviation.
* **Decision Adopted**: Alternative 3 (Fail-Closed). Zero modification to data, code, or results; full disclosure to supervisors.
* **Rejected Alternatives & Rationale**: Alternatives 1 and 2 were rejected as scientific fraud. Pre-registration requires reporting reality, not forcing data to fit pre-conceived models.
* **Associated Implementation**: `validation/article/r6_t2/r6_t2_backward_compatibility_results.json`, `r6_a1_protocol_deviation_log.md` (`R6-DEV-001`).
* **Validation**: Deterministic rerun confirmed 100% reproducible gap.
* **Result**: Triggered the development of the R6.1 Orthogonal Compatibility Taxonomy.
* **Consequences**: Proved the integrity of the project's governance framework under stress.
* **Limitations**: Delayed R6 closeout until protocol deviation was approved.
* **Commit / SHA**: `bfaece2`.
* **Related Correlation IDs**: `CMD-CVSS-IEEE-R6-A1-T2-EXECUTE-239`, `CMD-CVSS-IEEE-R6-A1-T2-DEVIATION-FREEZE-241`
