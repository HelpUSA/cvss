from core.cvss_sensitivity import (
    SensitivityAnalysisError,
    envelope_is_non_expanding,
    score_envelope,
)

BASE = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"


def test_score_envelope_enumerates_only_canonical_scorer_outputs():
    env = score_envelope(
        BASE,
        {
            "CR": ["L", "M", "H"],
            "IR": ["L", "M", "H"],
            "AR": ["L", "M", "H"],
        },
    )
    assert env["combinations_evaluated"] == 27
    assert env["min_score"] <= env["max_score"]
    assert env["unique_scores"] == sorted(set(env["unique_scores"]))
    assert env["invariant"] is (len(env["unique_scores"]) == 1)


def test_mr6_narrower_admissible_domain_cannot_widen_score_envelope():
    broad = score_envelope(BASE, {"CR": ["L", "M", "H"]})
    narrowed = score_envelope(BASE, {"CR": ["M", "H"]})
    assert envelope_is_non_expanding(broad, narrowed)


def test_singleton_domain_is_score_invariant_by_construction():
    env = score_envelope(BASE, {"CR": ["H"]})
    assert env["invariant"] is True
    assert env["min_score"] == env["max_score"]


def test_sensitivity_rejects_base_metrics():
    try:
        score_envelope(BASE, {"AV": ["N", "A"]})
    except SensitivityAnalysisError:
        pass
    else:
        raise AssertionError("Base metrics must not be altered by sensitivity analysis")


def test_sensitivity_guard_prevents_unbounded_cartesian_expansion():
    try:
        score_envelope(
            BASE,
            {"CR": ["L", "M", "H"], "IR": ["L", "M", "H"]},
            max_combinations=4,
        )
    except SensitivityAnalysisError:
        pass
    else:
        raise AssertionError("Expected max_combinations guard to reject expansion")
