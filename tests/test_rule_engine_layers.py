
from app.cvss_env_automation.rule_engine import assess_case


def test_assess_case_emits_official_and_contextual_layers():
    case = {
        "assets": [{
            "asset_id": "asset-1",
            "pci_scope_before": "in_scope",
            "pci_scope_after": "out_of_scope",
            "external_exposure_before": "internet",
            "external_exposure_after": "none",
            "role": "web",
        }],
        "business_impact": {"assets": {}},
        "expected": {"expected_labels": {}},
        "vulnerabilities": [{
            "finding_id": "F-1",
            "asset_id": "asset-1",
            "cve": "CVE-2099-0001",
            "vulnerability_type": "RCE",
            "base_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        }],
    }

    rows = assess_case(case)
    assert len(rows) == 2

    for row in rows:
        assert row["official_cvss"]["base_vector"] == row["base_vector"]
        assert row["official_cvss"]["base_score"] == row["base_score"]
        assert row["official_cvss"]["base_severity"] == "Critical"
        assert row["contextual_environmental"]["contextual_vector"] == row["environmental_vector"]
        assert row["contextual_environmental"]["contextual_score"] == row["environmental_score"]
        assert row["contextual_environmental"]["contextual_severity"] in {"None", "Low", "Medium", "High", "Critical"}
        assert row["contextual_environmental"]["decision"] in {"upgraded", "lowered", "unchanged"}
        assert row["contextual_environmental"]["delta_from_official_base"] == round(row["environmental_score"] - row["base_score"], 1)

    assert rows[0]["environmental_metrics"]["MAV"] == "N"
    assert rows[1]["environmental_metrics"]["MAV"] == "A"
    assert rows[1]["contextual_environmental"]["decision"] == "lowered"
