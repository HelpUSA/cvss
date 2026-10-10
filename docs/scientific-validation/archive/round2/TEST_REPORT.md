# Test Execution & Verification Report - Round 2

Generated: 2026-10-09T16:24:17.386300+00:00
Python Toolchain: Python 3.14.0 (Windows), cvss==3.6, scipy==1.18.1, pytest==9.1.1
Node Toolchain: Node v24.18.0, npm 11.6.2, Next.js 15.5.18, ae-cvss-calculator 1.0.13

## 1. Full Pytest Suite Collection
- **Total Tests Collected & Passed:** 121
- **Failed / Errors:** 0
- **Execution Time:** ~2.1 seconds

### Overlapping Subsets Included in the 121 Total:
- **Backend / Frontend Parity:** 19 tests (`test_backend_frontend_parity.py`)
- **Official Specification / Boundary Vectors:** 17 tests (`test_cvss40_official.py`)
- **CVSS v4.0 Conformance Smoke:** 10 tests (`test_cvss40_conformance.py`)
- **Abstention & Fail-Safe Invariants:** 8 tests (`test_fail_safe_abstention.py`, `test_cvss_environmental_abstention_path.py`)
- **Topology Reachability Mappings:** 8 tests (`test_topology_reachability.py`)
- **Policy Requirements & Mappings:** 4 tests (`test_policy_requirement_mapping.py`)
- **Dataset B Consistency:** 1 test (`test_dataset_b_consistency.py`)
- **Reporting & Pipeline Contracts:** 54 tests

## 2. Additional Independent Verification Suites
- **CVSS v4.0 Pinned Reference Corpus:** 22/22 passed (15 valid vectors + 7 negative rejection tests; 100% agreement).
- **RFC 8785 / JCS Canonicalization Suite:** 12/12 passed (key ordering, nested arrays, Unicode, numbers, NaN/Infinity rejection, SHA-256 structural invariance).
- **Web API Security & Fail-Safe Contract:** 5/5 passed (missing evidence rejected HTTP 400, stale/conflicting evidence abstains, policy requirements verified).
- **Backend / Frontend Extended Parity:** 23/23 passed (zero delta between Python and JS scoring engines).

## 3. Raw Log Artifacts
- `outputs/pytest-full.log`
- `outputs/jcs-conformance.log`
- `outputs/web-api-tests.log`
- `outputs/typescript-check.log`
- `outputs/web-build.log`
- `outputs/latex-build.log`
- `outputs/calculator-reference-corpus-results.json`
- `outputs/backend-frontend-parity-results.json`
- `outputs/jcs_conformance_results.json`
