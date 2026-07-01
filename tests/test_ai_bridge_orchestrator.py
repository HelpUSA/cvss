from app.ai_bridge_orchestrator import (
    EnvironmentalScorer,
    _severity_from_score,
    build_assessment_rows,
)


def test_modified_attack_vector_parses_csv_booleans():
    assert EnvironmentalScorer.modified_attack_vector({"segmented": "false", "exposed_to_internet": "true"}) == "Network"
    assert EnvironmentalScorer.modified_attack_vector({"segmented": "true", "exposed_to_internet": "true"}) == "Adjacent"
    assert EnvironmentalScorer.modified_attack_vector({"segmented": "", "exposed_to_internet": ""}) == "Local"


def test_build_assessment_rows_exposes_official_and_contextual_layers():
    evidence = {
        "assets": [
            {
                "asset_id": "asset-web-01",
                "segmented": "false",
                "exposed_to_internet": "true",
                "cr": "High",
                "ir": "High",
                "ar": "Medium",
            }
        ],
        "vulnerabilities": [
            {
                "finding_id": "F-001",
                "asset_id": "asset-web-01",
                "cve": "CVE-2099-0001",
                "vulnerability_type": "Remote Code Execution",
                "state": "open",
                "base_score": "9.8",
                "matches_expected_requirements": "true",
            }
        ],
    }

    rows = build_assessment_rows(evidence)

    assert len(rows) == 1
    row = rows[0]
    assert row["base_score"] == 9.8
    assert row["environmental_score"] == 9.8
    assert row["environmental_metrics"] == {
        "CR": "High",
        "IR": "High",
        "AR": "Medium",
        "MAV": "Network",
    }
    assert row["official_cvss"] == {
        "base_score": 9.8,
        "base_severity": "Critical",
    }
    assert row["contextual_environmental"] == {
        "contextual_score": 9.8,
        "contextual_severity": "Critical",
        "decision": "unchanged",
        "delta_from_official_base": 0.0,
    }
    assert row["matches_expected_requirements"] is True
    assert row["evidence"]["finding"]["finding_id"] == "F-001"
    assert row["evidence"]["asset"]["asset_id"] == "asset-web-01"


def test_build_assessment_rows_preserves_lowered_contextual_decision():
    evidence = {
        "assets": [
            {
                "asset_id": "asset-internal-01",
                "segmented": "true",
                "exposed_to_internet": "false",
                "cr": "Medium",
                "ir": "Medium",
                "ar": "Medium",
            }
        ],
        "vulnerabilities": [
            {
                "finding_id": "F-002",
                "asset_id": "asset-internal-01",
                "cve": "CVE-2099-0002",
                "base_score": "7.5",
            }
        ],
    }

    rows = build_assessment_rows(evidence)

    assert rows[0]["environmental_score"] == 6.7
    assert rows[0]["contextual_environmental"]["decision"] == "lowered"
    assert rows[0]["contextual_environmental"]["delta_from_official_base"] == -0.8


def test_severity_from_score_boundaries():
    assert _severity_from_score(9.0) == "Critical"
    assert _severity_from_score(7.0) == "High"
    assert _severity_from_score(4.0) == "Medium"
    assert _severity_from_score(0.1) == "Low"
    assert _severity_from_score(0.0) == "None"
