"""Tests for current-world HelpUS assessment wrapper (CVSS v4.0)."""
import pytest
from core.cvss_real_world import assess_finding

CVSS4_VECTOR = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"


def test_assess_finding_returns_official_contextual_and_evidence_layers():
    row = {
        "source_cvss_vector": CVSS4_VECTOR,
        "cve": "CVE-2024-0001",
        "asset_id": "asset-web-01",
        "source_url": "https://example.test/finding/CVE-2024-0001",
        "environment": "production",
        "business_criticality": "high",
        "evidence_quality": "SUFFICIENT",
        "reachability": "PUBLIC_ROUTED",
        "telemetry_age_days": 0.5,
    }

    result = assess_finding(row)

    assert "source_cvss" in result
    assert "official_cvss" in result  # compatibility alias
    assert "contextual_environmental" in result
    assert "evidence" in result

    source = result["source_cvss"]
    assert source["score"] == 9.3
    assert source["severity"] == "Critical"
    assert source["nomenclature"] == "CVSS-B"

    ctx = result["contextual_environmental"]
    assert ctx["score"] == 9.3
    assert ctx["decision"] == "unchanged"
    assert ctx["auto_downgrade_permitted"] is False

    evidence = result["evidence"]
    assert evidence["cve"] == "CVE-2024-0001"
    assert evidence["asset_id"] == "asset-web-01"


def test_assess_finding_accepts_vector_alias_for_source_vector():
    result = assess_finding({
        "vector": CVSS4_VECTOR,
        "evidence_quality": "SUFFICIENT",
        "reachability": "PUBLIC_ROUTED",
        "telemetry_age_days": 0.5,
    })

    assert result["source_cvss"]["score"] == 9.3
    assert "score" in result["contextual_environmental"]


def test_assess_finding_requires_cvss_vector_or_vector_alias():
    with pytest.raises(ValueError, match="source_cvss_vector/cvss_vector/vector is required"):
        assess_finding({})


def test_assess_finding_rejects_non_v4_vector():
    with pytest.raises(ValueError, match="Current HelpUS environmental assessment requires a CVSS v4.0 source vector"):
        assess_finding({"vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"})
