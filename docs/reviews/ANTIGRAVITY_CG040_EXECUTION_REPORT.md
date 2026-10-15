# Antigravity CG-040 Execution Report

- **Date:** 2026-10-15
- **Repository:** HelpUSA/cvss
- **PR:** #30 — CG-040: validate Gemini audit and add FIRST/sensitivity safeguards
- **Base Branch:** scientific-validation
- **PR Branch:** chatgpt/cg040-gemini-audit-validation
- **Tested HEAD SHA:** `b894d0ef05cb6bf83e692cea737d8b965c2622b2`

---

## 1. Environment & Dependencies

- **Python Version:** 3.14.0
- **cvss Library Version:** 3.6 (`cvss==3.6` confirmed via `pip show cvss`)
- **Node.js / npm:** v22 / npm 11.6.2
- **Prisma Version:** 6.19.0
- **Next.js Version:** 15.5.18
- **FIRST Fixtures Commit:** `d766d0c8ab4368b67bf27dd0e411eb481f05fdbb`

---

## 2. Test Execution & Conformance Results

### 2.1 FIRST Reference Corpus Round 4 (Strict Gate)
- **Script:** `python scripts/run_first_reference_corpus_round4.py`
- **Criterion:** Exact score equality (`observed_score == expected_score`, 0 delta tolerance)
- **Total Evaluated:** 486,472 cases
- **Total Passed:** 486,472 cases
- **Failed:** 0
- **Score Mismatches:** 0
- **Severity Mismatches:** 0
- **Execution Time:** 39.198s
- **Verdict:** `PASS` (G1 gate passed)

### 2.2 Metamorphic Campaign (Gate G9B)
- **Script:** `python scripts/run_metamorphic_campaign.py`
- **Total Cases Evaluated:** 10,000 cases (Seed: 20261013)
  - MR-1 (Monotonicity of Criticality): 2,500 / 2,500 passed (0 violations)
  - MR-2 (Defense Removal Monotonicity): 2,500 / 2,500 passed (0 violations)
  - MR-3 (Context Permutation Invariance): 2,500 / 2,500 passed (0 violations)
  - MR-4 (Irrelevant Control Invariance): 2,500 / 2,500 passed (0 violations)
- **Total Violations:** 0
- **Execution Time:** 61.112s
- **Verdict:** `PASSED`

### 2.3 EQ3/EQ6 Regression & Sensitivity Pytest Suite
- **Mandatory Targeted Suites:**
  - `tests/test_cvss_sensitivity.py`: 5 passed
  - `tests/test_cvss_eq3_eq6_regression.py`: 2 passed
  - `tests/test_environmental_metamorphic_rules.py`: 18 passed
  - `tests/test_fail_safe_abstention.py`: 7 passed
  - `tests/test_first_reference_gate_contract.py`: 1 passed
- **Full Pytest Suite:**
  - Total items: 166
  - Passed: 166
  - Failed: 0
  - Skipped: 0
  - Time: 3.25s
- **Verdict:** `PASS`

---

## 3. Empirical Proof: Gemini AR / VA:N / SA:N Hypothesis

- **Hypothesis Tested:** "Quando VA:N e SA:N, AR seria sempre irrelevante para o score final".
- **Script:** `scripts/test_gemini_ar_hypothesis.py`
- **Grid Evaluated:** 2,560 synthetic/reference combinations with `VA:N` and `SA:N`.
- **Finding:** 1,158 vectors exhibited non-invariance (45.2% of tested vectors).
- **Representative Counterexamples:**
  1. `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:N/SA:N`:
     - Varying `AR` in `{"L", "M", "H"}` produces `[9.8, 9.9]`.
  2. `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:L/SI:L/SA:N`:
     - Varying `AR` in `{"L", "M", "H"}` produces `[8.7, 8.8]`.
- **Mathematical Root Cause:** In FIRST CVSS v4.0, joint EQ3/EQ6 macrovector classification and distance interpolation interact with Modified / Subsequent system dimensions. Availability Requirement (`AR`) adjusts macro-level weights, shifting final rounded scores even when local and subsequent availability impacts are None.
- **Verdict:** **REFUTED**. Short-circuiting AR when VA:N and SA:N without checking the joint macrovector would introduce score corruption.

---

## 4. Web Engine & JCS Conformance

- **Prisma Schema Validation:** `npx prisma validate` -> `PASS`
- **Prisma Client Generation:** `npx prisma generate` -> `PASS`
- **TypeScript Typecheck:** `npm run typecheck` -> `PASS` (0 errors)
- **SaaS Unit Tests:** `npm run test:saas:unit` -> `PASS` (16/16 passed)
  - `JCS preserves Unicode as-is and does not silently normalize NFC` -> `PASS`
  - `JCS canonicalization remains key-order invariant` -> `PASS`
  - `tenant scope binds assessment to organization/project/environment hierarchy` -> `PASS`
- **JCS Conformance Suite:** `npx tsx scripts/test_jcs_conformance.ts` -> `PASS` (15/15 passed)
- **RFC 8785 Published Example:** `npx tsx scripts/test_jcs_rfc8785_examples.ts` -> `PASS`
- **Next.js Production Build:** `npm run build` -> `PASS` (All 45 routes compiled successfully)

---

## 5. Production & Deployment Verification

- **Domain:** `https://cvss.helpusbr.com`
- **Vercel Project:** `cvss` (`prj_RDSltmCDT9qQJYzLZJ1xHSEkS8ZT`)
- **HTTP Status:** 200 OK
- **Legacy Expert/HITL Language Scan:** 0 occurrences on landing page, `/demo`, `/login`, or `/app`.
- **Active Operational Flow:** Reviewer role is optional; no mandatory human-in-the-loop gate or blocking expert portal in active SaaS paths.

---

## 6. Recommendation

**MERGE**. All criteria for PR #30 are satisfied with zero regressions, zero mismatches, 100% green suites, and mathematical proof of sensitivity boundaries.
