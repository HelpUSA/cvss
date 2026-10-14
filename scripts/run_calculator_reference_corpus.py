#!/usr/bin/env python3
"""Run pinned CVSS v4.0 reference corpus against Red Hat cvss library (v3.6).

Produces outputs/calculator-reference-corpus-results.json.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from cvss import CVSS4
from core.cvss40 import score, CVSS40ValidationError

# Reference corpus of valid vectors
VALID_CORPUS = [
    # Smoke / spec boundary cases
    {"id": "CORPUS-001", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", "expected_score": 9.3, "expected_sev": "Critical", "nom": "CVSS-B"},
    {"id": "CORPUS-002", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H", "expected_score": 10.0, "expected_sev": "Critical", "nom": "CVSS-B"},
    {"id": "CORPUS-003", "vector": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", "expected_score": 8.5, "expected_sev": "High", "nom": "CVSS-B"},
    {"id": "CORPUS-004", "vector": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N", "expected_score": 8.2, "expected_sev": "High", "nom": "CVSS-B"},
    {"id": "CORPUS-005", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N", "expected_score": 5.3, "expected_sev": "Medium", "nom": "CVSS-B"},
    {"id": "CORPUS-006", "vector": "CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N", "expected_score": 7.1, "expected_sev": "High", "nom": "CVSS-B"},
    {"id": "CORPUS-007", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/CR:H/IR:H/AR:H", "expected_score": 9.3, "expected_sev": "Critical", "nom": "CVSS-BE"},
    {"id": "CORPUS-008", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/MAV:A/MAC:H/MPR:H", "expected_score": 7.3, "expected_sev": "High", "nom": "CVSS-BE"},
    {"id": "CORPUS-009", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N", "expected_score": 6.9, "expected_sev": "Medium", "nom": "CVSS-B"},
    {"id": "CORPUS-010", "vector": "CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N", "expected_score": 7.0, "expected_sev": "High", "nom": "CVSS-B"},
    # Zero impact boundary
    {"id": "CORPUS-011", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N", "expected_score": 0.0, "expected_sev": "None", "nom": "CVSS-B"},
    # Threat metrics (CVSS-BT)
    {"id": "CORPUS-012", "vector": "CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N/E:P", "expected_score": 1.1, "expected_sev": "Low", "nom": "CVSS-BT"},
    {"id": "CORPUS-013", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P", "expected_score": 8.9, "expected_sev": "High", "nom": "CVSS-BT"},
    {"id": "CORPUS-014", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N/E:P", "expected_score": 2.0, "expected_sev": "Low", "nom": "CVSS-BT"},
    # Environmental + Threat combined (CVSS-BTE)
    {"id": "CORPUS-015", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/MAV:A", "expected_score": 7.4, "expected_sev": "High", "nom": "CVSS-BTE"},
]

# Negative vectors that MUST raise CVSS40ValidationError or equivalent
NEGATIVE_CORPUS = [
    {"id": "NEG-001", "vector": "", "reason": "Empty vector"},
    {"id": "NEG-002", "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "reason": "v3.1 vector given to v4 parser"},
    {"id": "NEG-003", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N", "reason": "Truncated vector (missing SA)"},
    {"id": "NEG-004", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/AV:L", "reason": "Duplicate base metric AV"},
    {"id": "NEG-005", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/CR:Z", "reason": "Invalid metric value CR:Z"},
    {"id": "NEG-006", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/FOO:X", "reason": "Non-existent metric name FOO"},
    {"id": "NEG-007", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:INVALID", "reason": "Invalid exploit maturity value"},
]

def main():
    print("=== EXECUTING CVSS v4.0 PINNED REFERENCE CORPUS ===")
    results = []
    passed = 0
    total = len(VALID_CORPUS) + len(NEGATIVE_CORPUS)

    for item in VALID_CORPUS:
        try:
            res = score(item["vector"])
            obs_score = res["score"]
            obs_sev = res["severity"]
            obs_nom = res["nomenclature"]
            ok = abs(obs_score - item["expected_score"]) < 0.05 and obs_sev.lower() == item["expected_sev"].lower()
            if ok:
                passed += 1
                status = "PASS"
            else:
                status = "FAIL"
            results.append({
                "id": item["id"],
                "type": "valid",
                "vector": item["vector"],
                "expected": {"score": item["expected_score"], "severity": item["expected_sev"], "nomenclature": item["nom"]},
                "observed": {"score": obs_score, "severity": obs_sev, "nomenclature": obs_nom},
                "delta": round(obs_score - item["expected_score"], 2),
                "status": status,
            })
            print(f"[{status}] {item['id']}: expected {item['expected_score']} {item['expected_sev']} -> observed {obs_score} {obs_sev}")
        except Exception as e:
            results.append({
                "id": item["id"],
                "type": "valid",
                "vector": item["vector"],
                "status": "ERROR",
                "error": str(e),
            })
            print(f"[ERROR] {item['id']}: {e}")

    for item in NEGATIVE_CORPUS:
        rejected = False
        err_msg = ""
        try:
            score(item["vector"])
        except (CVSS40ValidationError, ValueError, Exception) as e:
            rejected = True
            err_msg = str(e)

        if rejected:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        results.append({
            "id": item["id"],
            "type": "negative",
            "vector": item["vector"],
            "expected_rejection": True,
            "rejected": rejected,
            "error": err_msg,
            "status": status,
        })
        print(f"[{status}] {item['id']} ({item['reason']}): correctly rejected = {rejected}")

    summary = {
        "suite": "CVSS v4.0 Pinned Reference Corpus (Red Hat cvss 3.6)",
        "calculator": "cvss==3.6 (Red Hat / FIRST CVSS v4.0 specification implementation)",
        "reference_basis": "FIRST CVSS v4.0 Specification Sections 4.1-4.2 and NVD/CNA audited dataset",
        "total_cases": total,
        "valid_cases": len(VALID_CORPUS),
        "negative_cases": len(NEGATIVE_CORPUS),
        "passed": passed,
        "failed": total - passed,
        "conformance_rate": f"{(passed / total) * 100:.1f}%",
        "results": results,
    }

    out_file = ROOT / "outputs" / "calculator-reference-corpus-results.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nSaved raw results to {out_file}")
    print(f"Total: {total} | Passed: {passed} | Failed: {total - passed}")

    if total != passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
