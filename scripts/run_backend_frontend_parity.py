#!/usr/bin/env python3
"""Run backend (Python cvss 3.6) vs frontend (JS ae-cvss-calculator) parity evaluation.

Saves raw results to outputs/backend-frontend-parity-results.json.
"""
import json
import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.cvss40 import score

PARITY_VECTORS = [
    # 19 Core Parity Vectors
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H",
    "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/CR:H/IR:H/AR:H",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/MAV:A/MAC:H/MPR:H",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N/E:P",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P",
    "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:N/VI:N/VA:N/SC:L/SI:L/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N/E:P",
    # Additional Dataset B Vectors
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:N/VI:N/VA:N/SC:L/SI:L/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/MAV:A",
]

def main():
    print("=== EXECUTING BACKEND / FRONTEND PARITY SUITE ===")
    web_dir = ROOT / "web"
    results = []
    passed = 0
    total = len(PARITY_VECTORS)

    for idx, vec in enumerate(PARITY_VECTORS, start=1):
        py_res = score(vec)
        js_code = (
            f"const {{ fromVector }} = require('ae-cvss-calculator'); "
            f"const v = fromVector('{vec}'); "
            f"console.log(JSON.stringify({{ score: v.calculateOverallScore(), nomenclature: v.getNomenclature() }}));"
        )
        proc = subprocess.run(
            ["node", "-e", js_code],
            cwd=str(web_dir),
            capture_output=True,
            text=True,
            check=True,
        )
        js_res = json.loads(proc.stdout.strip())

        score_match = abs(py_res["score"] - js_res["score"]) < 0.05
        nom_match = py_res["nomenclature"] == js_res["nomenclature"]
        is_pass = score_match and nom_match

        if is_pass:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        results.append({
            "case_id": f"PARITY-{idx:03d}",
            "vector": vec,
            "python": {"score": py_res["score"], "nomenclature": py_res["nomenclature"], "severity": py_res["severity"]},
            "javascript": {"score": js_res["score"], "nomenclature": js_res["nomenclature"]},
            "delta": round(abs(py_res["score"] - js_res["score"]), 3),
            "status": status,
        })
        print(f"[{status}] PARITY-{idx:03d}: Py={py_res['score']} ({py_res['nomenclature']}) vs JS={js_res['score']} ({js_res['nomenclature']})")

    summary = {
        "suite": "Backend (Python cvss 3.6) vs Frontend (JS ae-cvss-calculator) Parity",
        "total_cases": total,
        "passed": passed,
        "failed": total - passed,
        "parity_rate": f"{(passed / total) * 100:.1f}%",
        "results": results,
    }

    out_file = ROOT / "outputs" / "backend-frontend-parity-results.json"
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nSaved raw results to {out_file}")
    print(f"Total: {total} | Passed: {passed} | Failed: {total - passed}")

    if total != passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
