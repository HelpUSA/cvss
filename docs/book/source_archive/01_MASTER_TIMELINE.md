# HelpUS CVSS AI v4.0 — Master Project Timeline

This document reconstructs the chronological history of the HelpUS CVSS AI v4.0 project, integrating records from the Antigravity session (`52c43697-a431-4abf-a13d-6a5d1cb0b95b`), Git commits, pull requests, AI Bridge interaction logs, and academic revision cycles.

---

## Epoch 1: Genesis, Core Implementation & FIRST Conformance (May – Oct 2026)

### 1. The Vulnerability Prioritization Crisis
* **Problem Statement**: CVSS Base scores reflect intrinsic severity, not operational urgency. Organizations face thousands of vulnerabilities with Base score $> 7.0$ while lacking local contextualization (network exposure, compensating controls, asset criticality).
* **Architectural Decoupling (ADR-001)**: The team established the strict separation between the **Official CVSS v4.0 Scorer** (pure specification adherence) and the **Contextual Environmental Policy Engine** (local priority adjustment).

### 2. Full FIRST Calculator Conformance Verification
* **Test Suite Scale**: 486,472 benchmark vectors evaluated against the official FIRST reference implementation.
* **Result**: **$486,472 / 486,472$ exact concordance** (0 score divergences, 0 severity category mismatches).
* **Metamorphic Testing Harness**:
  - Implemented 10,000 automated metamorphic tests across 4 Metamorphic Relations:
    * `MR-1`: Monotonicity under increased environmental impact.
    * `MR-2`: Invariance under cosmetic vector reordering.
    * `MR-3`: Bounded attenuation by verified compensating controls.
    * `MR-4`: Monotonic sensitivity to Internet exposure transitions.
  - **Empirical Outcome**: $10,000 / 10,000$ executions passed with **0 invariant violations** (Benchmark: `HELPUS-METAMORPHIC-10K-G9B`).

---

## Epoch 2: Controlled Empirical Corpus & Priority Shift Reconciliation

### 1. Construction of the 30-Scenario Controlled Corpus
* **Corpus Design**: 30 canonical scenarios split into:
  - 12 real-world NVD CVE records (`SCN-NVD-001` through `SCN-NVD-012`) paired with curated enterprise deployment profiles.
  - 18 curated synthetic expert fixtures (`SCN-SYN-013` through `SCN-SYN-030`) representing edge-case deployment topologies without official CVEs.

### 2. The 24 vs 22 Priority Shift Reconciliation
* **Initial Observation**: An early prototype reported 24 priority shifts due to a nominal scoring policy that directly adjusted intermediate continuous weights.
* **The Reconciliation Finding**: Under the standardized Environmental MacroVector discrete lookup table (EQ1..EQ6), the discrete environmental score absorbs subtle continuous adjustments. When evaluating true discrete operational priority changes, exactly **22 out of 30 scenarios (73.33%)** underwent operational priority shifts:
  - 10 upward shifts (elevated urgency due to public exposure or high asset criticality);
  - 12 downward shifts (attenuated urgency due to active WAF, EDR, network segmentation, or isolated topology);
  - 8 scenarios maintained parity with their Base priority.
* **Epistemological Discipline**: Rather than forcing continuous score hacks to claim 24 shifts, the project corrected all manuscripts and tables to report the honest, verifiable figure of **22/30 (73.33%)**.

---

## Epoch 3: Web Application, Multi-Agent AI Bridge & Ethical Clearance

### 1. CEP Plataforma Brasil Ethical Approval
* Ethical submission and approval via Plataforma Brasil for the evaluation protocol and expert review governance, ensuring research compliance before clinical and enterprise data testing.

### 2. Multi-Agent AI Bridge Architecture
* Development of the local inter-agent orchestration bridge (`ai-bridge-local` on port `:8766`).
* Standardized message envelope (`ai_bridge_local.envelope` v1) coordinating real-time collaboration between:
  - **Antigravity** (Primary local IDE agent & implementation engineer);
  - **ChatGPT** (Academic supervisor, LaTeX compiler, and editorial gatekeeper);
  - **Gemini** (Senior peer reviewer, IEEE Q1 validator, and compliance auditor);
  - **DeepSeek** (Adversarial code auditor and secondary cross-checker).

### 3. Web UI Hardening (PR #8 through PR #44)
* End-to-end development of the Next.js/React contextual vulnerability assessment web application.
* **PR #41**: Deterministic synthetic authentication on disposable isolated PostgreSQL.
* **PR #42**: Playwright E2E synthetic user journey stabilization across desktop, tablet, and mobile (390px) viewports.
* **PR #44**: Guided input assistance with zero-autofill guardrails, evidence validity presets, and WebKit mobile horizontal overflow guards.

---

## Epoch 4: Baseline Publication Freeze & IEEE Major Revision R1 (October 2026)

### 1. Publication Baseline Freeze (Commit `5226f74`)
* Simultaneous compilation and cryptographic locking of:
  - **Academic Double-Blind Article**: `article/ieee/cvss40_double_blind.pdf` (7 pages, IEEE Conference format).
  - **Monograph Companion Book**: `book_latex/main.pdf` (50 pages, comprehensive engineering guide).
  - Pinned FIRST reference commit: `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`.

### 2. IEEE Major Revision R1 (Commit `799657f`)
* Gemini Q1 peer review identified 4 core structural enhancement requests:
  - Clarification of CVSS v4.0 nomenclature ($B, BT, BE, BTE$);
  - Formal definition of MacroVectors $EQ_1$ to $EQ_6$;
  - 6-stage TikZ architecture diagram;
  - Table V detailing 12 real CVE records.
* Implemented in `article/ieee/cvss40_double_blind.tex` and verified with 0 Overfull `\hbox`.

### 3. Post-R1 Main Track Consolidation & Option A (Commit `29a087d`)
* Deliberation between Antigravity, ChatGPT, and Gemini regarding human adjudication in Section X.
* **Option A Adopted**: Reframed Section X as a **Standardized Adjudication Protocol Specification**, preserving the pre-registered fail-closed gatekeeper (`scripts/g10b_confirmatory_gate.py`) and maintaining confirmatory datasets $C_1, C_2$ strictly sealed.

---

## Epoch 5: Revision R2 — The Machine-Verifiable Track (Commit `c41065e`)

### 1. Independent Trace Verifier (`verify_trace_integrity.py`)
* Developed a completely standalone Python verifier independent of the runtime scoring engine.
* Enforced **464 independent assertions** across the 30 canonical JSON traces:
  - 100% trace completeness (all mandatory fields present);
  - Vector syntax correctness via `core.cvss40.parse_vector`;
  - Exact recomputation of $P_{\text{base}}, w_{\text{context}}, w_{\text{control}}, P_{\text{env}}$, and $\Delta_{\text{cat}}$ across 8 operational profiles;
  - Boundary isolation statements and non-autonomous review requirements.

### 2. Transparent Disclosure of 34 Limitations
* Rather than claiming infallible verification, the verifier cataloged **34 explicit boundary limitations** (e.g., narrative text free-form parsing, absence of dynamic semantic link verification, closed-world vs open-world assumptions).

### 3. Priority Sensitivity Analysis & LOEO Viability
* Evaluated Leave-One-Evidence-Out (LOEO) and weight perturbation across all 30 scenarios:
  - NVD Scenarios: $0 / 12$ sensitivity shifts ($0.0\%$);
  - Synthetic Scenarios: $2 / 18$ sensitivity shifts ($11.1\%$);
  - Total Corpus: $2 / 30$ sensitivity shifts ($6.7\%$), proving operational stability.

---

## Epoch 6: Revision R3 — Verifier-Agnostic Randomized Mutation (Commit `073fa7d`)

### 1. The Design: Mitigating Operator-Selection Bias
* To address the risk that structured mutation tests (M1–M8, 42 mutants) were hand-crafted to pass known checks, the team designed the **Verifier-Agnostic Randomized Mutation Complement**.
* Generator implemented in an isolated script (`tools/generate_random_mutations.py`) with zero imports from the verifier's assertion catalogs.
* Deterministic fixed seed: `20261021`.

### 2. The Canonical Run & Empirical Results
* 6 representative scenarios evaluated ($3 \text{ NVD} + 3 \text{ Synthetic}$), producing exactly **120 applicable mutants** (20 per scenario) across 9 mutation families (F1–F9):
  - **Total Rejections**: $83 / 120$ ($69.17\% \approx 69.2\%$);
  - **Total Accepted**: $37 / 120$ ($30.83\% \approx 30.8\%$).

### 3. The Discovery of the F3 Open-World Boundary
* **Mutation Family F3** (attribute and subobject injection): **$0 / 16$ rejections** ($16/16$ accepted).
* **Root Cause**: The historical Schema v1 parser operated under standard **open-world JSON semantics**—any extra, unrecognized JSON keys were quietly ignored as long as mandatory fields were intact.
* **19 Accepted Mutants in F5/F6**: Free-form text fields had no lexical grammars, allowing random string truncations to pass.
* **2 Accepted Mutants in F9**: Exposure flips without cross-field semantic invariants.
* **Scientific Integrity**: The team refused to alter the verifier or re-run the seed to inflate detection rates. The 37 accepted mutants were integrated directly into the manuscript as an honest scientific finding exposing the boundaries of the machine-checkable contract.

---

## Epoch 7: Revisions R4 and R5 — Conceptual Polish & Camera-Ready (Commit `cc4418e`)

### 1. Revision R4 (Commit `cb8ab69`)
* Deepened the epistemological distinction between open-world JSON parsing and closed-world contracts.
* Formalized subobject injection semantics in Section VII-A.

### 2. Revision R5 Camera-Ready Abstract Polish (Commit `cc4418e`, Merged via PR #47 `e5215b5`)
* Condensation of the abstract to meet strict IEEE length constraints while retaining all canonical metrics ($486,472$ FIRST vectors, $10,000$ metamorphic runs, $30$ scenarios, $22$ priority shifts, $464$ verifier checks, $120$ randomized mutants with $69.2\%$ rejection).
* Final manuscript tagged and sealed.

---

## Epoch 8: Revision R6 & R6.1 — The Quest for Top-Tier A1 (October 2026)

### 1. Phased Preregistration for Top-Tier A1 Venues (`c0b4025`)
* Objective: Elevate the work to top-tier security venues (IEEE S&P, USENIX Security, ACM CCS, NDSS).
* Strict preregistration protocol enacted (`r6_a1_preregistration.md`) with explicit falsification rules and anti-retuning locks.

### 2. External Held-Out Corpus Acquisition (`12bf6c4`)
* Acquired an independent, temporal-held-out corpus of 947 candidates from GitHub Advisory Database (Sept 2026):
  - 947 raw candidates scanned;
  - 9 malware/empty advisories excluded;
  - 938 eligible CVSS v4.0 cases locked into cryptographic quarantine (`validation/article/r6_heldout/`).
  - Quarantine rule: `held_out_accessed = false` (zero exploratory analysis).

### 3. Schema v2 Closed-World & Decoupled Governance Specification (`090ad8b`)
* **Schema v2**: Formalized strict object-by-object closed-world validation (`UNKNOWN_FIELD` rejection) to formally test the hypothesis that closed-world schemas reject F3 subobject injections.
* **Governance Override Record**: Engineered a structured, cryptographically signed operational override mechanism ($OVR$) that records exceptions without modifying the nominal Equation 8 policy.
* **Implementation Freeze (`43664e5`)**: Implemented both components in Python with 39/39 passing unit and contract tests.

### 4. Experiment T2 Execution & The Taxonomy Gap (`CMD-239`)
* Executed Experiment T2 (Backward Compatibility) against the 30 canonical historical traces.
* **Results**:
  - Schema v1 validation: $30 / 30 \text{ PASS}$ ($100\%$).
  - Schema v2 validation: $0 / 30 \text{ PASS}$ ($0\%$).
  - $12 \text{ NVD cases}$ rejected with `INVALID_TYPE` (`compensating_controls` is string, expected list of objects).
  - $18 \text{ Synthetic cases}$ rejected with `INVALID_ENUM` (`cve_id` is `""`, expected pattern or null).
* **The Gap**: The preregistered taxonomy had only one category for v1-valid/v2-invalid cases: `V1_VALID_V2_INVALID_UNDECLARED_FIELD`. Because the rejections were caused by types and enums, not undeclared fields, all 30 cases were classified as `UNCLASSIFIED_BY_FROZEN_COMPATIBILITY_MODEL`.
* **Fail-Closed Governance**: Antigravity refused to silently alter data or code, halting execution and reporting `R6_A1_T2_NEEDS_REVIEW`.

### 5. Protocol Deviation R6-DEV-001 & R6.1 Freeze (`bfaece2`)
* Formally approved and logged protocol deviation `R6-DEV-001` as a `POST_RESULT_CHANGE`.
* Created the **R6.1 Orthogonal State-Complete Taxonomy**:
  - Decoupled the 5 primary contract categories (`V1_VALID_V2_VALID`, `V1_VALID_V2_INVALID`, `V1_INVALID_V2_INVALID`, `V1_VALID_V2_VALID_NORMALIZED`, `V1_INVALID_V2_VALID`);
  - Moved diagnostic error classification to an orthogonal dimension (`v2_error_category`).
* Locked the R6.1 taxonomy prior to any rerun (`bfaece26f9f718672be6b754ad83497ac7f102ea`).
* Current status: Original T2 artifacts remain permanently immutable; R6.1-T2R rerun is preregistered and pending authorization.
