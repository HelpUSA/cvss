import pytest

from core.ai_evidence_engine import AIEvidenceEngine
from core.cvss40 import compare

BASE_CRITICAL = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"


def test_ai_engine_segmented_internal_pci_asset():
    engine = AIEvidenceEngine()
    profile = {
        "internet_exposed": False,
        "network_segmented": True,
        "pci_in_scope": True,
        "business_criticality": "high",
        "data_sensitivity": "payment",
    }
    result = engine.analyze_finding("CVE-2024-TEST", BASE_CRITICAL, profile)

    assert result["candidate_metrics"]["MAV"] == "A"
    assert result["candidate_metrics"]["CR"] == "H"
    assert result["candidate_metrics"]["IR"] == "H"
    assert len(result["citations"]) > 0
    assert result["human_review_status"] == "required"

    comparison = compare(BASE_CRITICAL, result["candidate_metrics"])
    assert comparison["official_cvss"]["score"] == 9.3
    # Segmentation to Adjacent drops score to 8.7 in CVSS v4.0
    assert comparison["candidate_cvss"]["score"] == 8.7
    assert comparison["candidate_cvss"]["nomenclature"] == "CVSS-BE"


def test_ai_engine_isolated_redundant_asset():
    engine = AIEvidenceEngine()
    profile = {
        "internet_exposed": False,
        "network_segmented": False,
        "business_criticality": "low",
        "high_availability": True,
    }
    result = engine.analyze_finding("CVE-2024-LOW", BASE_CRITICAL, profile)

    assert result["candidate_metrics"]["MAV"] == "L"
    assert result["candidate_metrics"]["CR"] == "L"
    assert result["candidate_metrics"]["AR"] == "L"

    comparison = compare(BASE_CRITICAL, result["candidate_metrics"])
    assert comparison["candidate_cvss"]["score"] < 9.3
