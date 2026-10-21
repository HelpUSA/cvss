# HelpUS CVSS AI v4.0 — Scientific Decision Log

This log documents the epistemological, methodological, and scientific boundary decisions governing the HelpUS CVSS AI research program. It establishes what the project claims, what it explicitly refrains from claiming, and how threats to scientific validity were neutralized.

---

### Scientific Decision 1: Controlled Curated Corpus vs. Statistical Random Sample
* **Scientific Principle**: Epistemological modesty regarding statistical generalization.
* **Context**: The core empirical study evaluates 30 canonical scenarios (12 NVD CVEs + 18 synthetic edge-cases).
* **The Decision**: The 30 scenarios must be described exclusively as a **controlled, curated benchmark corpus**, never as a "statistically representative random sample of the vulnerability universe".
* **Methodological Rationale**:
  - Statistical significance testing (e.g., p-values, confidence intervals) on a 30-scenario curated set would constitute pseudo-rigor, as the sample is purposive rather than randomized.
  - The corpus was designed to test boundary behaviors across 8 distinct deployment topologies (public web apps, internal databases, DMZ gateways, restricted workstations), not to estimate global CVE population distributions.
* **Enforced Guardrail**: Prohibited any phrasing suggesting that the $73.33\%$ shift rate applies globally to all existing CVEs.

---

### Scientific Decision 2: Demarcation of Human Expert Adjudication Status
* **Scientific Principle**: Absolute transparency regarding experimental completion state.
* **Context**: Academic reviewers inquired about the degree of human expert consensus supporting the priority adjustments.
* **The Decision**: Explicitly classify the independent expert adjudication as **PENDING / PROTOCOL SPECIFIED**, rather than simulating or claiming human validation.
* **Methodological Rationale**:
  - Human validation requires an institutional IRB/CEP protocol, multi-evaluator blinded scoring, and inter-rater reliability calculation (Fleiss' Kappa / Krippendorff's Alpha).
  - Attempting to substitute AI evaluations (e.g., using ChatGPT or Gemini as "human experts") without formal multi-agent protocol boundaries would compromise scientific integrity.
* **Enforced Guardrail**: Reframed Section X of the IEEE manuscript as a **Standardized Adjudication Protocol Specification**, an architectural deliverable establishing how organizations can conduct blinded human reviews, rather than presenting incomplete preliminary human data.

---

### Scientific Decision 3: "Independent Machine-Checkable Verification" vs. "Formal Verification"
* **Scientific Principle**: Precision in computer science terminology.
* **Context**: Developing automated trace verification tools (`verify_trace_integrity.py`).
* **The Decision**: Ban the term "Formal Verification" and adopt strictly **"Independent Machine-Checkable Verification"** or **"Machine-Checkable Structural Contract Verification"**.
* **Methodological Rationale**:
  - "Formal Verification" in computer science denotes deductive mathematical proof of program correctness with respect to a formal logic specification (e.g., via Coq, Isabelle/HOL, TLA+, or Z3 SMT solvers).
  - The Python verifier performs comprehensive structural validation, syntax checking, and deterministic formula recomputation across 464 assertions. While rigorous, this is runtime assertion verification, not mathematical formal proof.
* **Enforced Guardrail**: Cataloged 34 explicit verifier limitations directly in the manuscript to ensure reviewers understand the exact scope of the automated checks.

---

### Scientific Decision 4: Honest Disclosure of Accepted Randomized Mutants (R3)
* **Scientific Principle**: Negative results and boundary conditions are primary scientific contributions.
* **Context**: In the R3 randomized mutation campaign ($N = 120$ mutants), the verifier rejected 83 mutants ($69.2\%$) and accepted 37 mutants ($30.8\%$).
* **The Decision**: Publish the full $69.2\% / 30.8\%$ split transparently without attempting to re-tune operators, add ad-hoc verifier checks, or re-run the seed to achieve an artificial "$100\%$ detection rate".
* **Methodological Rationale**:
  - The 37 accepted mutants revealed critical properties of the system's contract boundaries:
    1. 16 F3 mutants passed because open-world JSON parsing legitimately ignores unrecognized keys.
    2. 19 F5/F6 mutants passed because free-form narrative fields had no formal grammar.
    3. 2 F9 mutants passed because exposure transitions lacked cross-field invariants.
  - Presenting these findings transparently demonstrates the true, objective boundaries of automated verification and establishes the scientific motivation for closed-world contracts.
* **Enforced Guardrail**: Published the complete case-by-case audit in `validation/article/r3_randomized_mutation_testing.json` and `r3_randomized_mutation_cases.csv`.

---

### Scientific Decision 5: F3 Mutation Invariance as an Open-World Property, Not a Defect
* **Scientific Principle**: Historical baseline immutability.
* **Context**: Mutation Family F3 yielded $0 / 16$ rejections under Schema v1.
* **The Decision**: Declare that F3's historical result is an accurate empirical measurement of the **Schema v1 open-world contract**, not an operational bug to be erased or retroactively corrected.
* **Methodological Rationale**:
  - In open-world systems, ignoring unexpected fields is standard behavior. Treating this as a defect that invalidates previous publications would misrepresent the engineering history.
  - Schema v2 was formulated as an independent, alternative hypothesis (closed-world contract) to be tested comparatively, rather than an admission of retroactive flaw in Schema v1.
* **Enforced Guardrail**: Schema v1 and Schema v2 are evaluated as distinct experimental conditions in Phase R6.

---

### Scientific Decision 6: Preservation of Nominal Equation 8 and Rejection of Delta Audit
* **Scientific Principle**: Invariance of the core physical model under operational adaptation.
* **Context**: Designing governance override mechanisms for operational exceptions.
* **The Decision**: Strictly prohibit adding a heuristic adjustment parameter ($\delta_{\text{audit}}$) into Equation 8.
* **Methodological Rationale**:
  - Equation 8 defines the mathematical relationship between contextual weights and priority transitions. Altering its formula to absorb operational deviations destroys its closed-form reproducibility and breaks FIRST calculator conformance.
  - Operational overrides must be modeled as a distinct, decoupled layer ($OVR$) that wraps the nominal score, preserving mathematical auditability.
* **Enforced Guardrail**: Verified `Eq8_modified = false` in all CI and governance gates.

---

### Scientific Decision 7: Strict Cryptographic Firewall on External Held-Out Corpus
* **Scientific Principle**: Prevention of data snooping and pre-test overfitting.
* **Context**: Acquiring 938 eligible CVSS v4.0 advisories from GitHub Advisory Database for Phase R6.
* **The Decision**: Lock the held-out corpus behind an absolute cryptographic firewall (`held_out_accessed = false`) prior to experimental execution.
* **Methodological Rationale**:
  - In top-tier security research (IEEE S&P, USENIX), inspecting test data during model/schema design introduces subtle cognitive biases, leading researchers to write rules that subconsciously accommodate known outliers.
  - True generalizability requires that the schema and validator be designed, implemented, and frozen **without ever seeing the held-out records**.
* **Enforced Guardrail**: Logged `held_out_accessed = false` in the experiment registry; zero reading of advisory text during R6-1/R6-2 design.

---

### Scientific Decision 8: Schema v2 as an Independent Hypothesis (Not Retroactive Patch)
* **Scientific Principle**: Separation of pre-registered hypotheses from historical baselines.
* **Context**: Implementing closed-world validation in Phase R6.
* **The Decision**: Schema v2 is treated as a new experimental treatment for Phase R6, while Schema v1 remains the historical baseline.
* **Methodological Rationale**:
  - Retroactively modifying historical traces to satisfy Schema v2 would destroy the reproducibility of the R2–R5 experimental campaigns.
  - Scientific progress requires comparing Treatment B against Baseline A, not overwriting Baseline A to look like Treatment B.
* **Enforced Guardrail**: Maintained separate validators (`validate_trace_v1` and `validate_trace_v2`) and preserved historical files byte-identical.

---

### Scientific Decision 9: Formal Classification of Protocol Deviation R6-DEV-001 as POST_RESULT_CHANGE
* **Scientific Principle**: Strict pre-registration governance and anti-retuning discipline.
* **Context**: In Experiment T2, all 30 historical traces fell outside the frozen 4-category taxonomy, resulting in 30/30 unclassified outcomes.
* **The Decision**: Refuse to silently adjust the taxonomy before logging the results; formally record `R6-DEV-001` as a `POST_RESULT_CHANGE` and lock the R6.1 taxonomy prior to any rerun.
* **Methodological Rationale**:
  - Modifying a pre-registered evaluation model after observing empirical data is the definition of a post-hoc change. Attempting to disguise it as an initial design would violate academic ethics.
  - By publicly disclosing that the initial model had a taxonomy gap, keeping the original unclassified results permanently archived, and defining R6.1 as a documented iteration, the project upholds the highest standards of reproducible science.
* **Enforced Guardrail**: Created `validation/article/r6_1_t2_compatibility_taxonomy.md` and locked commit `bfaece2` before scheduling rerun R6.1-T2R.
