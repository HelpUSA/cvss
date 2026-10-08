import pytest

from core.cvss40 import (
    CVSS40ValidationError,
    apply_candidates,
    build_vector,
    compare,
    nomenclature,
    parse_vector,
    score,
)

# Externally published scores (NVD / CNA records used in the article dataset).
NVD_ORACLE = [
    ("CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N/E:P", 1.1, "Low", "CVSS-BT"),
    ("CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P", 8.9, "High", "CVSS-BT"),
    ("CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N", 6.8, "Medium", "CVSS-B"),
    ("CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N", 8.3, "High", "CVSS-B"),
    ("CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N", 8.2, "High", "CVSS-B"),
    ("CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:N/VI:N/VA:N/SC:L/SI:L/SA:N", 5.1, "Medium", "CVSS-B"),
    ("CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N", 5.1, "Medium", "CVSS-B"),
    ("CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N", 6.0, "Medium", "CVSS-B"),
    ("CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N/E:P", 2.0, "Low", "CVSS-BT"),
]

CRITICAL_BASE = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"


@pytest.mark.parametrize("vector,expected,severity,label", NVD_ORACLE)
def test_scores_match_published_nvd_values(vector, expected, severity, label):
    result = score(vector)
    assert result["score"] == expected
    assert result["severity"] == severity
    assert result["nomenclature"] == label


def test_reference_vectors():
    assert score(CRITICAL_BASE)["score"] == 9.3
    full = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"
    assert score(full)["score"] == 10.0
    none = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N"
    assert score(none)["score"] == 0.0
    assert score(none)["severity"] == "None"


def test_explicit_not_defined_values_are_equivalent_to_omission():
    padded = CRITICAL_BASE + "/E:X/CR:X/MAV:X/U:X"
    assert score(padded)["score"] == score(CRITICAL_BASE)["score"]
    assert score(padded)["vector"] == CRITICAL_BASE


@pytest.mark.parametrize(
    "vector",
    [
        "",
        "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N",  # missing SA
        CRITICAL_BASE + "/AV:L",  # duplicate
        CRITICAL_BASE + "/CR:Z",  # bad value
        CRITICAL_BASE + "/FOO:X",  # unknown metric
    ],
)
def test_invalid_vectors_are_rejected(vector):
    with pytest.raises(CVSS40ValidationError):
        parse_vector(vector)


def test_nomenclature():
    base = parse_vector(CRITICAL_BASE)
    assert nomenclature(base) == "CVSS-B"
    assert nomenclature({**base, "E": "A"}) == "CVSS-BT"
    assert nomenclature({**base, "CR": "H"}) == "CVSS-BE"
    assert nomenclature({**base, "E": "U", "MAV": "L"}) == "CVSS-BTE"
    assert nomenclature({**base, "S": "P"}) == "CVSS-B"  # supplemental never scores


def test_candidates_cannot_override_base_or_supplemental_metrics():
    with pytest.raises(CVSS40ValidationError):
        apply_candidates(CRITICAL_BASE, {"AV": "L"})
    with pytest.raises(CVSS40ValidationError):
        apply_candidates(CRITICAL_BASE, {"S": "P"})
    with pytest.raises(CVSS40ValidationError):
        apply_candidates(CRITICAL_BASE, {"MSI": "Q"})


def test_not_defined_candidates_leave_vector_unchanged():
    assert apply_candidates(CRITICAL_BASE, {"CR": "X", "MAV": None}) == CRITICAL_BASE


def test_restrictive_environment_lowers_score():
    result = compare(CRITICAL_BASE, {"CR": "L", "IR": "L", "AR": "L", "MAV": "L"})
    assert result["official_cvss"]["score"] == 9.3
    assert result["candidate_cvss"]["nomenclature"] == "CVSS-BE"
    assert result["candidate_cvss"]["score"] < 9.3
    assert result["delta"] < 0


def test_unreported_exploit_maturity_lowers_score():
    result = compare(CRITICAL_BASE, {"E": "U"})
    assert result["candidate_cvss"]["nomenclature"] == "CVSS-BT"
    assert result["candidate_cvss"]["score"] < result["official_cvss"]["score"]


def test_safety_impact_is_only_reachable_through_environmental_metrics():
    base = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:H"
    result = compare(base, {"MSI": "S", "MSA": "S"})
    assert result["candidate_cvss"]["score"] >= result["official_cvss"]["score"]


def test_build_vector_uses_canonical_order():
    shuffled = "CVSS:4.0/SA:N/SI:N/SC:N/VA:H/VI:H/VC:H/UI:N/PR:N/AT:N/AC:L/AV:N"
    assert build_vector(parse_vector(shuffled)) == CRITICAL_BASE
