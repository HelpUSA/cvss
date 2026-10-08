# Test Report - Local HelpUS Pre-Freeze Test Execution

**Execution Timestamp:** 2026-10-08T21:35:00Z  
**Environment:** Windows Server / Node.js v24.18.0 / Python 3.14.0 (.venv) / Next.js 15.5.18  
**Scoring Implementation:** Red Hat Product Security `cvss` v3.6 (Python) & `ae-cvss-calculator` v1.0.13 (Node.js)

---

## 1. Summary of Test Execution

| Test Suite / Target | Tests Collected | Passed | Failed | Status |
| :--- | :--- | :--- | :--- | :--- |
| Core Repository Pytest (`tests/`) | 100 | 100 | 0 | **PASS** |
| Backend/Frontend CVSS Parity (`tests/test_backend_frontend_parity.py`) | 19 | 19 | 0 | **PASS** |
| Smoke Suite (`tests/cvss_v4_conformance/test_cvss40_conformance.py`) | 10 | 10 | 0 | **PASS** |
| Dataset B Structural Validation (`scripts/validate_dataset_b.py`) | 30 scenarios | 30 | 0 | **PASS** |
| Historical Fisher 2x2 Reproducibility (`scripts/reproduce_historical_fisher.py`) | 4 statistics | 4 | 0 | **PASS** |
| Web Application Production Build (`npm run build`) | 10 routes | 10 | 0 | **PASS** |
| Web Route Automated Integration (`web/scripts/test_analyze_route.ts`) | 2 live cases | 2 | 0 | **PASS** |
| **Total Comprehensive Test Suite** | **119** | **119** | **0** | **PASS** |

---

## 2. Targeted Engine Invariants Verified

Command:
```bash
python -m pytest tests/test_fail_safe_abstention.py tests/test_topology_reachability.py tests/test_policy_requirement_mapping.py tests/test_real_world_wrapper.py
```
- Missing/unknown telemetry age $\implies$ `HUMAN_REVIEW_REQUIRED`, `auto_downgrade_permitted = False`.
- Stale telemetry (> 1.0 day dynamic, > 7.0 days static) $\implies$ `HUMAN_REVIEW_REQUIRED`.
- Conflicting firewall/routing table $\implies$ `HUMAN_REVIEW_REQUIRED`.
- `PUBLIC_ROUTED` and `INTERNAL_ROUTED` $\implies$ `MAV:N` (strictly prevents `internal-only => MAV:A` error).
- `ADJACENT_ONLY` $\implies$ `MAV:A` (requires explicit L2 adjacency evidence).
- `LOCAL_ONLY` $\implies$ `MAV:L`; `PHYSICAL_ONLY` $\implies$ `MAV:P`.
- Firewall/WAF presence alone $\implies$ does NOT set `MAC:H`.
- High availability $\implies$ does NOT set `AR:L`.
- Security Requirements (`CR`, `IR`, `AR`) require explicit `organization_policy_id` and `policy_version`.

---

## 3. Cross-Implementation Backend / Frontend Parity

Command:
```bash
python -m pytest tests/test_backend_frontend_parity.py
```
**Result:** 19/19 passed (100% score and nomenclature equivalence between Python `cvss` v3.6 and frontend Node.js `ae-cvss-calculator` v1.0.13). Maximum score deviation observed: `0.00`.

---

## 4. Dataset B Structural Invariants

Command:
```bash
python scripts/validate_dataset_b.py
```
**Result:** `rows=30 errors=0`.
- All 12 real CVEs preserve explicit nomenclature (`CVSS-B` vs `CVSS-BT`).
- All 18 synthetic scenarios are marked as `SYNTHETIC` and `INVESTIGATOR_ASSIGNED`.
- Operational dispositions adhere strictly to `P0_IMMEDIATE` through `P4_DEFER_RECOMMENDED`.

---

## 5. Historical Fisher Exact Test Reproducibility

Command:
```bash
python scripts/reproduce_historical_fisher.py
```
**Statistical outputs generated via SciPy 1.18.1:**
- Two-sided Fisher exact p-value: `4.223475753262034e-06`
- Sample cross-product odds ratio: `3.388235294117647`
- Conditional maximum-likelihood odds ratio: `3.3770294841208597`
- Conditional exact 95% confidence interval: `[1.9131109781442286, 6.184139076556205]`

Persisted to `generated/historical_fisher.json` and `generated/historical_fisher_macros.tex`.

---

## 6. Web Application Synchronization & Production Build

Command:
```bash
cd web && npm run build
```
- TypeScript compilation: 0 errors (`npx tsc --noEmit`).
- Static routes generated: 10/10.
- Dynamic route `/api/analyze-environment` verified with 5 auditable layers, fail-safe abstention on stale telemetry, and RFC 8785 canonical SHA-256 receipt generation.
