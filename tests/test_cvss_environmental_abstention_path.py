"""Regression test for the environmental-engine abstention path.

This specifically guards against the previously observed NameError caused by
calling score() without importing it in core.cvss_environmental_engine.
"""
from core.cvss_environmental_engine import calculate

BASE = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"


def test_calculate_abstention_path_returns_source_assessment_without_nameerror():
    result = calculate({
        "cve_id": "CVE-TEST-ABSTAIN",
        "source_cvss_vector": BASE,
        "evidence": {},
    })
    assert result["decision"] == "abstained"
    assert result["review_status"] in ("ABSTAIN", "HUMAN_REVIEW_REQUIRED")
    assert result["auto_downgrade_permitted"] is False
    assert result["environmental_vector"] is None
    assert result["source_vector"].startswith("CVSS:4.0/")
