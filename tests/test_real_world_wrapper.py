from core.cvss_real_world import assess_finding

NETWORK_CRITICAL_VECTOR = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"


def test_assess_finding_returns_official_contextual_and_evidence_layers():
    row = {
        "cvss_vector": NETWORK_CRITICAL_VECTOR,
        "cve": "CVE-2099-0001",
        "asset_id": "asset-web-01",
        "source_url": "https://example.test/finding/CVE-2099-0001",
        "environment": "production",
        "business_criticality": "high",
        "internet_exposed": True,
        "pci_in_scope": True,
    }

    result = assess_finding(row)

    assert set(result) == {
        "official_cvss",
        "contextual_environmental",
        "evidence",
    }

    official = result["official_cvss"]
    contextual = result["contextual_environmental"]
    evidence = result["evidence"]

    assert official["base_score"] == 9.8
    assert official["base_severity"] == "Critical"

    assert contextual["contextual_score"] == 10.0
    assert contextual["contextual_severity"] == "Critical"
    assert contextual["decision"] == "upgraded"
    assert round(contextual["delta_from_official_base"], 1) == 0.2
    assert isinstance(contextual["trace"], list)
    assert contextual["trace"]

    assert evidence == {
        "cve": "CVE-2099-0001",
        "asset_id": "asset-web-01",
        "source_url": "https://example.test/finding/CVE-2099-0001",
        "environment": "production",
        "business_criticality": "high",
        "pci_in_scope": True,
    }


def test_assess_finding_accepts_vector_alias_for_official_cvss_input():
    result = assess_finding({"vector": NETWORK_CRITICAL_VECTOR})

    assert result["official_cvss"]["base_score"] == 9.8
    assert "contextual_score" in result["contextual_environmental"]


def test_assess_finding_requires_cvss_vector_or_vector_alias():
    try:
        assess_finding({})
    except ValueError as exc:
        assert str(exc) == "cvss_vector is required for real-world assessment"
    else:
        raise AssertionError("assess_finding should require cvss_vector or vector")


if __name__ == "__main__":
    test_assess_finding_returns_official_contextual_and_evidence_layers()
    test_assess_finding_accepts_vector_alias_for_official_cvss_input()
    test_assess_finding_requires_cvss_vector_or_vector_alias()
