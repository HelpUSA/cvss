# Historical R5/R3 vs. Schema v2 Replay: Comparative Analysis

## 1. Executive Comparative Overview

This document presents a structured, family-by-family comparative analysis between the historical **R5/R3 Randomized Mutation Campaign** (evaluated under Schema v1 open-world conventions) and the **R6 Experiment T3 Replay** (evaluated under the frozen Schema v2 closed-world contract).

All 120 mutants were deterministically generated using the frozen seed `20261021` and evaluated against the frozen implementation commit `43664e58b4f7852d0a03c6b21ab043dec2529be9`.

---

## 2. Family-by-Family Comparative Breakdown

### Family F1: Structural Required Field Removal ($N = 16$)
* **Historical R5/R3 Outcome**: 16/16 rejected ($100.0\%$).
* **Schema v2 Replay Outcome**: 16/16 rejected ($100.0\%$).
* **Factual Delta**: $\Delta = 0$ ($0.0\%$ change).
* **Observed v2 Error Category**: `MISSING_REQUIRED_FIELD` (16/16).
* **Interpretation**: Both schema generations strictly enforce mandatory root fields. Structural required field removal is universally detected across open-world and closed-world regimes.

---

### Family F2: Structural Subobject Removal ($N = 12$)
* **Historical R5/R3 Outcome**: 12/12 rejected ($100.0\%$).
* **Schema v2 Replay Outcome**: 12/12 rejected ($100.0\%$).
* **Factual Delta**: $\Delta = 0$ ($0.0\%$ change).
* **Observed v2 Error Categories**: `MISSING_REQUIRED_FIELD` (3), `INVALID_TYPE` (4), `INVALID_ENUM` (5).
* **Interpretation**: Subobject removal is caught at the root structural layer or through downstream typing violations in both generations.

---

### Family F3: Structural Subobject & Attribute Injection ($N = 16$)
* **Historical R5/R3 Outcome**: 0/16 rejected ($0.0\%$), 16/16 accepted ($100.0\%$).
* **Schema v2 Replay Outcome**: 16/16 rejected ($100.0\%$), 0/16 accepted ($0.0\%$).
* **Factual Delta**: $\Delta = +16$ rejections ($+100.0\%$ increase in rejection rate).
* **Observed v2 Error Categories**: `UNKNOWN_FIELD` (6), `INVALID_TYPE` (3), `INVALID_ENUM` (7).
* **Interpretation**: This represents the defining empirical contrast between Schema v1 and Schema v2. Under Schema v1, open-world JSON parsing ignored unrecognized subobjects. Under Schema v2, closed-world enforcement actively rejects undeclared properties (`UNKNOWN_FIELD`) and strictly types sub-elements, eliminating the historical acceptance gap.

---

### Family F4: Structural Type Corruption ($N = 15$)
* **Historical R5/R3 Outcome**: 15/15 rejected ($100.0\%$).
* **Schema v2 Replay Outcome**: 15/15 rejected ($100.0\%$).
* **Factual Delta**: $\Delta = 0$ ($0.0\%$ change).
* **Observed v2 Error Category**: `INVALID_TYPE` (15/15).
* **Interpretation**: Replacing structured objects with mismatched primitive types (e.g., dict with integer) is caught with 100% concordance across both schema generations.

---

### Family F5: Field String Truncation ($N = 13$)
* **Historical R5/R3 Outcome**: 6/13 rejected ($46.2\%$), 7/13 accepted ($53.8\%$).
* **Schema v2 Replay Outcome**: 13/13 rejected ($100.0\%$), 0/13 accepted ($0.0\%$).
* **Factual Delta**: $\Delta = +7$ rejections ($+53.8\%$ increase).
* **Observed v2 Error Categories**: `INVALID_TYPE` (6), `INVALID_ENUM` (7).
* **Interpretation**: In R5, truncations in narrative text strings were accepted because Schema v1 lacked lexical constraints on free-form fields. Under Schema v2, the underlying scenarios fail closed-world typing and strict enum requirements, preventing truncated narratives from reaching scoring.

---

### Family F6: Field String Random Alteration ($N = 15$)
* **Historical R5/R3 Outcome**: 3/15 rejected ($20.0\%$), 12/15 accepted ($80.0\%$).
* **Schema v2 Replay Outcome**: 15/15 rejected ($100.0\%$), 0/15 accepted ($0.0\%$).
* **Factual Delta**: $\Delta = +12$ rejections ($+80.0\%$ increase).
* **Observed v2 Error Categories**: `INVALID_TYPE` (7), `INVALID_ENUM` (8).
* **Interpretation**: Identical to F5, random alterations inside text strings that passed Schema v1's permissive validation are rejected under Schema v2 prior to environmental scoring.

---

### Family F7: Field Numeric Perturbation ($N = 10$)
* **Historical R5/R3 Outcome**: 10/10 rejected ($100.0\%$).
* **Schema v2 Replay Outcome**: 10/10 rejected ($100.0\%$).
* **Factual Delta**: $\Delta = 0$ ($0.0\%$ change).
* **Observed v2 Error Categories**: `INVALID_TYPE` (6), `INVALID_ENUM` (4).
* **Interpretation**: Numeric perturbations (e.g., modifying CVSS Base score decimals) trigger recomputation or typing mismatches in both environments.

---

### Family F8: Field Numeric Swap or Domain Shift ($N = 11$)
* **Historical R5/R3 Outcome**: 11/11 rejected ($100.0\%$).
* **Schema v2 Replay Outcome**: 11/11 rejected ($100.0\%$).
* **Factual Delta**: $\Delta = 0$ ($0.0\%$ change).
* **Observed v2 Error Categories**: `INVALID_TYPE` (5), `INVALID_ENUM` (6).
* **Interpretation**: Swapping numeric fields or shifting domains triggers deterministic invariant violations across both contracts.

---

### Family F9: Field Valid Token Flip ($N = 12$)
* **Historical R5/R3 Outcome**: 10/12 rejected ($83.3\%$), 2/12 accepted ($16.7\%$).
* **Schema v2 Replay Outcome**: 12/12 rejected ($100.0\%$), 0/12 accepted ($0.0\%$).
* **Factual Delta**: $\Delta = +2$ rejections ($+16.7\%$ increase).
* **Observed v2 Error Categories**: `INVALID_TYPE` (7), `INVALID_ENUM` (5).
* **Interpretation**: In R5, two flips of `internet_exposure` between compatible tokens were accepted because the verifier lacked cross-field environmental invariants. Under Schema v2, the stricter structural rules reject the unnormalized traces.

---

## 3. Epistemological Demarcation: New Contract vs. Retroactive Correction

It is vital to state explicitly:
1. **The R5 Historical Results Remain Valid**: The 83 rejected / 37 accepted outcomes observed in R5 are an authentic, reproducible measurement of the **Schema v1 open-world contract**. They are not errors or retroactive mistakes.
2. **Schema v2 is an Alternative Hypothesis**: The shift to 120/120 rejections under Schema v2 reflects the adoption of a fundamentally different contract: a **closed-world structural schema** that rejects undeclared fields and enforces strict typing across all subobjects.
3. **No Claim of Formal Verification or Inferential Generalization**: These observations represent controlled empirical measurements on the 120 pre-registered mutant traces. They do not constitute mathematical formal verification or statistical proof that all arbitrary software bugs are detected.
