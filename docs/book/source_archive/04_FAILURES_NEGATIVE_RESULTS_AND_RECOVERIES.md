# HelpUS CVSS AI v4.0 — Failures, Negative Results, and Systematic Recoveries

An authentic technical monograph must not present research as an effortless, linear triumph. This document provides an honest, comprehensive account of the operational failures, negative experimental results, and methodological breakdowns encountered during the development of HelpUS CVSS AI v4.0, along with the systematic recovery procedures enacted to maintain scientific integrity.

---

## Part 1: Operational Failures and Systematic Recoveries

### Failure OP-001: WebKit Mobile Select Option ScrollWidth Expansion (PR #44)
* **Problem**: On iOS Safari and WebKit viewports (390px mobile width), dropdown `<select>` elements with long option labels (such as enterprise compensating control descriptions) silently expanded the parent container's `scrollWidth`, causing horizontal layout breakage and jitter.
* **Detection**: Automated Playwright mobile viewport regression suite running against WebKit in CI.
* **Why it Mattered**: The web interface is designed for security operators responding to incidents on mobile devices; horizontal overflow breaks touch targets and degrades emergency usability.
* **Action**:
  1. Isolated the CSS cause: WebKit's native `<select>` implementation calculates minimum intrinsic width based on option text length even when parent elements have `overflow: hidden`.
  2. Applied defensive CSS rules: clamped `.management-form select` to `max-width: 100%`, applied `text-overflow: ellipsis`, and styled wrapper `.field` containers with `min-width: 0` to prevent flexbox child blowout.
* **Outcome**: Verified horizontal stability across 390px, 768px, and 1280px viewports without truncating functional form values.
* **Lesson Learned**: Native browser form controls behave disparately across browser rendering engines; E2E tests must include real WebKit rendering rather than relying solely on Chromium emulation.

---

### Failure OP-002: Model Timeout Events and Read-Only State Recovery
* **Problem**: During complex long-running operations (such as multi-file LaTeX compilation, 464-assertion trace verification, and 120-mutant batch generation), external AI agents (e.g., ChatGPT or Antigravity subagents) occasionally encountered gateway read timeouts (`MODEL_TIMEOUT`) or connection resets.
* **Detection**: Gateway command monitoring via `ai-bridge-local` logs showing unacknowledged dispatches or truncated tool outputs.
* **Why it Mattered**: If an agent re-executes an operation after a timeout without verifying disk state, it risks creating duplicate files, re-running random generators with altered seeds, or corrupting partially written git repositories.
* **Action**:
  1. Mandated a strict **READ-ONLY STATUS CHECK PROTOCOL**: after any timeout or disconnection, agents are prohibited from immediately re-executing writes.
  2. Agents must inspect disk state (`git status`, file existence, byte size, partial logs) to determine if the timed-out process completed asynchronously, failed cleanly, or left partial artifacts.
  3. Safe resumption: if partial artifacts exist, they are audited before clean resumption; if no changes occurred, the command is safely re-dispatched.
* **Outcome**: Zero instances of duplicate commits, corrupted JSON files, or lost experimental runs across hundreds of development hours.
* **Lesson Learned**: In autonomous multi-agent environments, asynchronous command idempotence and non-destructive status inspection are essential prerequisites for system reliability.

---

### Failure OP-003: Playwright Hydration Races and Locator Drift in Synthetic Journeys
* **Problem**: In PR #41 and PR #42, synthetic user journey tests failed intermittently because client-side React hydration had not completed when Playwright clicked form inputs, resulting in input values reverting to default empty states.
* **Detection**: Intermittent CI test failures in `test(e2e): synthetic user journey`.
* **Why it Mattered**: Flaky E2E tests erode confidence in the CI pipeline, tempting engineers to disable automated testing before major deadlines.
* **Action**:
  1. Synchronized pre-hydration DOM input values using React `key` bindings tied to active assessment IDs.
  2. Replaced fragile text locators with strict `data-testid` attributes.
  3. Added explicit network idle and URL navigation assertions (`waitForURL`) before initiating subsequent form steps.
* **Outcome**: Achieved 3 consecutive rounds of $100\%$ green CI runs across all viewports.
* **Lesson Learned**: Never rely on arbitrary `sleep()` calls in E2E automation; bind assertions directly to deterministic application state and DOM hydration events.

---

## Part 2: Scientific & Methodological Negative Results

### Negative Result SCI-001: The 24 vs. 22 Priority Shift Reconciliation
* **Problem**: Early project documentation claimed 24 priority shifts out of 30 scenarios, but the formal IEEE double-blind manuscript reported exactly 22 shifts ($73.33\%$).
* **Detection**: Cross-verification audit between continuous intermediate calculations and the official CVSS v4.0 discrete Environmental MacroVector lookup table.
* **Why it Mattered**: A discrepancy between early whitepapers and the academic article would constitute a severe integrity failure under IEEE peer review.
* **Root Cause**: Two boundary scenarios had continuous scores that shifted slightly (e.g., from 4.1 to 4.3), but because both scores mapped into the same discrete MacroVector severity bucket (Medium Priority), no discrete operational priority transition actually took place.
* **Action**:
  1. Rejected any continuous math tampering to force the two cases into shifting.
  2. Formally standardized the discrete operational priority definition: a shift occurs if and only if $P_{\text{env}} \neq P_{\text{base}}$.
  3. Audited and updated all historical tables and text to report the true, verifiable figure of **22 / 30 (73.33%)**.
* **Outcome**: Absolute alignment across code, CSV datasets, LaTeX manuscripts, and verifier assertions.
* **Lesson Learned**: In security metrics, always differentiate between continuous mathematical adjustments and discrete operational decisions.

---

### Negative Result SCI-002: Mutation Family F3 Complete Acceptance (0/16 Rejections)
* **Problem**: In the R3 randomized mutation campaign, Mutation Family F3 (attribute and subobject injection) achieved a $0\%$ detection rate: **16 out of 16 mutants were accepted by the verifier**.
* **Detection**: Canonical execution of the R3 randomized complement (`validation/article/r3_randomized_mutation_testing.json`).
* **Why it Mattered**: On its surface, a $0\%$ detection rate appears to be an embarrassing failure of the verifier, potentially undermining the entire validation narrative.
* **Root Cause**: The historical Schema v1 parser operated under standard **open-world JSON semantics**. It strictly verified that required fields were present and valid, but deliberately ignored unrecognized extraneous fields. When random subobjects were injected, the parser safely discarded them without error.
* **Action**:
  1. Strictly prohibited retroactively modifying the verifier or re-running the test with a different seed to artificially catch F3 mutants.
  2. Embraced the finding as a fundamental scientific discovery: open-world schemas cannot protect against attribute injection attacks.
  3. Documented the $0/16$ result directly in Section VII-A of the IEEE manuscript as empirical proof of the boundaries of open-world parsing.
  4. Formulated the **Schema v2 closed-world contract** as an independent hypothesis for Phase R6.
* **Outcome**: The honest disclosure of F3 became one of the most praised aspects of the R3 revision, transforming a potential embarrassment into a rigorous scientific contribution.
* **Lesson Learned**: Negative results that expose contract boundaries are often more scientifically valuable than superficial $100\%$ success claims.

---

### Negative Result SCI-003: 37 Accepted Perturbations in Randomized Mutation Testing
* **Problem**: Beyond F3, 21 additional randomized mutants were accepted by the verifier (19 in F5/F6 narrative string manipulations and 2 in F9 exposure flips), resulting in an overall rejection rate of $69.2\%$ ($83/120$).
* **Detection**: Case-by-case audit in `validation/article/r3_randomized_mutation_cases.csv`.
* **Why it Mattered**: Demonstrates that the verifier does not detect arbitrary noise injected into free-form text fields.
* **Root Cause**: Free-form evidence summaries and narrative deployment descriptions had no lexical or semantic grammar. Truncating a sentence like `"WAF enabled"` to `"WAF ena"` remained a syntactically valid JSON string.
* **Action**:
  1. Cataloged all 37 accepted mutants in the public artifact repository.
  2. Documented 34 explicit limitations in the manuscript, clarifying that machine-checkable structural verification checks syntax and arithmetic consistency, not natural language semantic truth.
* **Outcome**: Reviewers accepted the paper's claims because the limitations were clearly demarcated.
* **Lesson Learned**: Automated verifiers must clearly distinguish between structural syntax invariants and natural language semantic interpretation.

---

### Negative Result SCI-004: Experiment T2 30/30 Unclassified Outcomes and Incomplete Taxonomy
* **Problem**: In Phase R6-A1, when Experiment T2 was executed against the 30 canonical historical traces, **$100\%$ of the inputs (30/30) were marked as `UNCLASSIFIED_BY_FROZEN_COMPATIBILITY_MODEL`**.
* **Detection**: Automated execution output of `cmd_cvss_ieee_r6_a1_t2_execute_239`.
* **Why it Mattered**: The pre-registered experiment failed to classify a single input into any of its 4 designated categories.
* **Root Cause**: The pre-registered taxonomy assumed that historical traces would be `V1_VALID_V2_VALID`, and that the only reason a v1-valid trace would fail v2 would be undeclared fields (`V1_VALID_V2_INVALID_UNDECLARED_FIELD`). However, the Schema v2 closed-world contract also enforced strict typing on lists of objects (`compensating_controls`) and regex patterns on `cve_id`. The 30 historical traces failed v2 due to `INVALID_TYPE` (12 NVD) and `INVALID_ENUM` (18 Synthetic), leaving them unclassifiable under the frozen 4-category model.
* **Action**:
  1. Refused to alter historical data or rewrite code silently.
  2. Immediately halted execution and reported `R6_A1_T2_NEEDS_REVIEW`.
  3. Logged formal protocol deviation `R6-DEV-001` as a `POST_RESULT_CHANGE`.
  4. Engineered the **R6.1 Orthogonal State-Complete Taxonomy**, decoupling the primary 5-state category from the independent diagnostic error dimension.
  5. Kept the original T2 artifacts permanently immutable in `validation/article/r6_t2/`.
* **Outcome**: Demonstrated absolute adherence to pre-registration ethics and created a robust, future-proof taxonomic model.
* **Lesson Learned**: Pre-registered taxonomies must be mathematically state-complete across the full Boolean domain of their inputs rather than tailored to anticipated happy paths.
