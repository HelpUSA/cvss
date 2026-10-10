"""Backend / Frontend CVSS v4.0 parity test.

Verifies that the Python scoring engine (core/cvss40.py) and the frontend
JavaScript engine (ae-cvss-calculator) produce identical scores and nomenclature.
"""
from pathlib import Path
import subprocess
import json
import pytest
from core.cvss40 import score

TEST_VECTORS = [
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
]


@pytest.mark.parametrize("vector", TEST_VECTORS)
def test_backend_frontend_cvss_score_parity(vector):
    web_dir = Path(__file__).resolve().parent.parent / "web"
    if not (web_dir / "node_modules" / "ae-cvss-calculator").exists():
        pytest.skip("ae-cvss-calculator not installed in web/node_modules in portable environment")
    py_res = score(vector)
    js_code = (
        f"const {{ fromVector }} = require('ae-cvss-calculator'); "
        f"const v = fromVector('{vector}'); "
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

    assert abs(py_res["score"] - js_res["score"]) < 0.05, (
        f"Score mismatch for {vector}: Python {py_res['score']} vs JS {js_res['score']}"
    )
    assert py_res["nomenclature"] == js_res["nomenclature"], (
        f"Nomenclature mismatch for {vector}: Python {py_res['nomenclature']} vs JS {js_res['nomenclature']}"
    )
