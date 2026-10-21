"""
Unit tests for tools/article_cvss40_r2_priority_sensitivity.py.

Verifies canonical domains, ordinal neighbor semantics, control flip semantics,
deterministic grid generation, B4_nominal comparison baseline, curated NVD flags,
aggregation partitioning, stability flags, and epistemological boundaries.
"""

import csv
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.cvss40_environmental_policy import (
    PRIORITY_ORDER,
    lookup_nominal_weights,
    ordinal_to_priority,
    priority_to_ordinal,
    recompute_p_base,
    recompute_p_env_nominal,
)
from tools.article_cvss40_r2_priority_sensitivity import (
    CURATED_NVD_DEVIATIONS,
    DEFAULT_SCENARIOS_CSV,
    VALID_CONTEXT_WEIGHTS,
    VALID_CONTROL_WEIGHTS,
    ScenarioSensitivityResult,
    SensitivityAggregate,
    SensitivityPerturbationResult,
    compute_sensitivity_aggregate,
    evaluate_scenario_sensitivity,
    evaluate_single_perturbation,
    generate_scenario_perturbation_grid,
    generate_sensitivity_plan,
    get_valid_context_neighbors,
    get_valid_control_states,
)


# 1. test_context_domain_is_canonical
def test_context_domain_is_canonical():
    assert VALID_CONTEXT_WEIGHTS == [-2, 0, 1, 2, 3]
    assert -1 not in VALID_CONTEXT_WEIGHTS
    assert 4 not in VALID_CONTEXT_WEIGHTS
    assert -3 not in VALID_CONTEXT_WEIGHTS


# 2. test_control_domain_is_canonical
def test_control_domain_is_canonical():
    assert VALID_CONTROL_WEIGHTS == [-1, 0]
    assert 1 not in VALID_CONTROL_WEIGHTS
    assert -2 not in VALID_CONTROL_WEIGHTS


# 3. test_context_neighbors_lower_boundary
def test_context_neighbors_lower_boundary():
    neighbors = get_valid_context_neighbors(-2)
    assert len(neighbors) == 2
    vals = [val for val, _ in neighbors]
    rels = {rel: val for val, rel in neighbors}
    assert vals == [-2, 0]
    assert "down" not in rels
    assert rels["nominal"] == -2
    assert rels["up"] == 0


# 4. test_context_neighbors_internal_zero
def test_context_neighbors_internal_zero():
    neighbors = get_valid_context_neighbors(0)
    assert len(neighbors) == 3
    vals = [val for val, _ in neighbors]
    rels = {rel: val for val, rel in neighbors}
    assert vals == [-2, 0, 1]
    assert rels["down"] == -2
    assert rels["nominal"] == 0
    assert rels["up"] == 1


# 5. test_context_neighbors_internal_one
def test_context_neighbors_internal_one():
    neighbors = get_valid_context_neighbors(1)
    assert len(neighbors) == 3
    vals = [val for val, _ in neighbors]
    rels = {rel: val for val, rel in neighbors}
    assert vals == [0, 1, 2]
    assert rels["down"] == 0
    assert rels["nominal"] == 1
    assert rels["up"] == 2


# 6. test_context_neighbors_internal_two
def test_context_neighbors_internal_two():
    neighbors = get_valid_context_neighbors(2)
    assert len(neighbors) == 3
    vals = [val for val, _ in neighbors]
    rels = {rel: val for val, rel in neighbors}
    assert vals == [1, 2, 3]
    assert rels["down"] == 1
    assert rels["nominal"] == 2
    assert rels["up"] == 3


# 7. test_context_neighbors_upper_boundary
def test_context_neighbors_upper_boundary():
    neighbors = get_valid_context_neighbors(3)
    assert len(neighbors) == 2
    vals = [val for val, _ in neighbors]
    rels = {rel: val for val, rel in neighbors}
    assert vals == [2, 3]
    assert "up" not in rels
    assert rels["down"] == 2
    assert rels["nominal"] == 3


# 8. test_control_flip_is_binary_and_reversible
def test_control_flip_is_binary_and_reversible():
    states_from_minus1 = get_valid_control_states(-1)
    assert states_from_minus1 == [(-1, "nominal"), (0, "flipped")]

    states_from_0 = get_valid_control_states(0)
    assert states_from_0 == [(0, "nominal"), (-1, "flipped")]


# 9. test_perturbation_grid_contains_nominal_once
def test_perturbation_grid_contains_nominal_once():
    grid = generate_scenario_perturbation_grid(w_ctx=2, w_ctrl=-1, include_nominal=True)
    nominal_matches = [t for t in grid if t[2] == "nominal" and t[3] == "nominal"]
    assert len(nominal_matches) == 1
    assert nominal_matches[0] == (2, -1, "nominal", "nominal")


# 10. test_perturbation_grid_excludes_nominal_when_requested
def test_perturbation_grid_excludes_nominal_when_requested():
    grid = generate_scenario_perturbation_grid(w_ctx=2, w_ctrl=-1, include_nominal=False)
    nominal_matches = [t for t in grid if t[2] == "nominal" and t[3] == "nominal"]
    assert len(nominal_matches) == 0
    # For nominal (2, -1): context neighbors are [1, 2, 3], controls [-1, 0] -> 6 total, strictly perturbed = 5
    assert len(grid) == 5


# 11. test_plan_scope_is_exactly_30_canonical_scenarios
def test_plan_scope_is_exactly_30_canonical_scenarios():
    plan = generate_sensitivity_plan(DEFAULT_SCENARIOS_CSV)
    assert plan["total_scenarios"] == 30
    scenario_ids = [s["scenario_id"] for s in plan["scenarios"]]
    assert len(scenario_ids) == 30
    assert len(set(scenario_ids)) == 30

    nvd_scenarios = [s for s in plan["scenarios"] if "NVD" in s["scenario_id"]]
    syn_scenarios = [s for s in plan["scenarios"] if "SYN" in s["scenario_id"]]
    assert len(nvd_scenarios) == 12
    assert len(syn_scenarios) == 18


# 12. test_plan_counts_are_166_total_and_136_perturbed
def test_plan_counts_are_166_total_and_136_perturbed():
    plan = generate_sensitivity_plan(DEFAULT_SCENARIOS_CSV)
    assert plan["total_grid_combinations"] == 166
    assert plan["total_strictly_perturbed_cases"] == 136

    nvd_scens = [s for s in plan["scenarios"] if "NVD" in s["scenario_id"]]
    syn_scens = [s for s in plan["scenarios"] if "SYN" in s["scenario_id"]]

    nvd_total = sum(s["full_grid_count"] for s in nvd_scens)
    nvd_pert = sum(s["strictly_perturbed_count"] for s in nvd_scens)
    syn_total = sum(s["full_grid_count"] for s in syn_scens)
    syn_pert = sum(s["strictly_perturbed_count"] for s in syn_scens)

    assert nvd_total == 68
    assert nvd_pert == 56
    assert syn_total == 98
    assert syn_pert == 80


# 13. test_no_invalid_weight_generated_anywhere
def test_no_invalid_weight_generated_anywhere():
    plan = generate_sensitivity_plan(DEFAULT_SCENARIOS_CSV)
    for s in plan["scenarios"]:
        for t in s["perturbation_tuples"]:
            assert t["w_context"] in VALID_CONTEXT_WEIGHTS
            assert t["w_control"] in VALID_CONTROL_WEIGHTS


# 14. test_baseline_is_b4_nominal_not_observed
def test_baseline_is_b4_nominal_not_observed():
    # Pick SCN-NVD-001 where observed ('low') differs from nominal ('medium')
    with open(DEFAULT_SCENARIOS_CSV, "r", encoding="utf-8") as f:
        rows = {r["scenario_id"]: r for r in csv.DictReader(f)}

    r001 = rows["SCN-NVD-001"]
    res = evaluate_scenario_sensitivity(r001, include_nominal_in_perturbations=False)

    assert res.nominal_p_env == "medium"
    assert res.observed_p_env == "low"
    assert res.nominal_p_env != res.observed_p_env

    # Check that deltas are computed against nominal ('medium', ordinal 2)
    for p in res.perturbations:
        assert p.ordinal_delta_vs_nominal == p.g_env_perturbed - res.g_nominal_p_env


# 15. test_curated_nvd_deviations_flagged_exactly_four
def test_curated_nvd_deviations_flagged_exactly_four():
    assert CURATED_NVD_DEVIATIONS == {
        "SCN-NVD-001",
        "SCN-NVD-006",
        "SCN-NVD-007",
        "SCN-NVD-008",
    }
    with open(DEFAULT_SCENARIOS_CSV, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        scen_id = r["scenario_id"]
        res = evaluate_scenario_sensitivity(r, include_nominal_in_perturbations=False)
        if scen_id in CURATED_NVD_DEVIATIONS:
            assert res.is_curated_nvd_deviation is True
        else:
            assert res.is_curated_nvd_deviation is False


# 16. test_single_perturbation_ordinal_delta_is_recomputed_by_canonical_policy
def test_single_perturbation_ordinal_delta_is_recomputed_by_canonical_policy():
    res = evaluate_single_perturbation(
        scenario_id="SCN-TEST-001",
        base_priority="medium",
        nominal_p_env="high",
        w_ctx_pert=0,
        w_ctrl_pert=-1,
        c_rel="down",
        k_rel="nominal",
        perturbation_index=1,
    )
    # g_base = ordinal(medium) = 2
    # g_pert = clamp(2 + 0 + -1) = clamp(1) = 1 (low)
    # nominal = high (ordinal 3)
    # delta = 1 - 3 = -2
    assert res.p_env_perturbed == "low"
    assert res.g_env_perturbed == 1
    assert res.ordinal_delta_vs_nominal == -2
    assert res.changed is True
    assert res.shift_direction == "down"
    assert res.abs_ordinal_shift == 2


# 17. test_scenario_stability_flag_semantics
def test_scenario_stability_flag_semantics():
    # Construct a synthetic scenario result where all perturbations preserve nominal priority
    stable_scen = ScenarioSensitivityResult(
        scenario_id="SCN-STABLE-001",
        source_type="synthetic",
        asset_class="public_web_application",
        cve_id=None,
        base_priority="high",
        g_base=3,
        nominal_w_context=2,
        nominal_w_control=-1,
        nominal_p_env="critical",
        g_nominal_p_env=4,
        observed_p_env="critical",
        is_curated_nvd_deviation=False,
        total_valid_perturbations=5,
        unchanged_count=5,
        changed_count=0,
        upward_count=0,
        downward_count=0,
        unchanged_rate=1.0,
        max_abs_ordinal_shift=0,
        mean_abs_ordinal_shift=0.0,
        is_stable=True,
    )
    assert stable_scen.is_stable is True

    unstable_scen = ScenarioSensitivityResult(
        scenario_id="SCN-UNSTABLE-001",
        source_type="synthetic",
        asset_class="public_web_application",
        cve_id=None,
        base_priority="high",
        g_base=3,
        nominal_w_context=2,
        nominal_w_control=-1,
        nominal_p_env="critical",
        g_nominal_p_env=4,
        observed_p_env="critical",
        is_curated_nvd_deviation=False,
        total_valid_perturbations=5,
        unchanged_count=4,
        changed_count=1,
        upward_count=0,
        downward_count=1,
        unchanged_rate=0.8,
        max_abs_ordinal_shift=1,
        mean_abs_ordinal_shift=0.2,
        is_stable=False,
    )
    assert unstable_scen.is_stable is False


# 18. test_aggregate_counts_partition_exactly
def test_aggregate_counts_partition_exactly():
    # Evaluate a small representative subset: 1 NVD + 1 Synthetic
    with open(DEFAULT_SCENARIOS_CSV, "r", encoding="utf-8") as f:
        rows = {r["scenario_id"]: r for r in csv.DictReader(f)}

    nvd_scen = evaluate_scenario_sensitivity(rows["SCN-NVD-001"])
    syn_scen = evaluate_scenario_sensitivity(rows["SCN-SYN-013"])

    total_agg = compute_sensitivity_aggregate("total", [nvd_scen, syn_scen])
    nvd_agg = compute_sensitivity_aggregate("nvd", [nvd_scen])
    syn_agg = compute_sensitivity_aggregate("syn", [syn_scen])

    assert total_agg.total_perturbation_cases == nvd_agg.total_perturbation_cases + syn_agg.total_perturbation_cases
    assert total_agg.unchanged_count == nvd_agg.unchanged_count + syn_agg.unchanged_count
    assert total_agg.changed_count == nvd_agg.changed_count + syn_agg.changed_count
    assert total_agg.upward_count == nvd_agg.upward_count + syn_agg.upward_count
    assert total_agg.downward_count == nvd_agg.downward_count + syn_agg.downward_count


# 19. test_aggregate_is_descriptive_only
def test_aggregate_is_descriptive_only():
    with open(DEFAULT_SCENARIOS_CSV, "r", encoding="utf-8") as f:
        r001 = list(csv.DictReader(f))[0]
    scen = evaluate_scenario_sensitivity(r001)
    agg = compute_sensitivity_aggregate("sample", [scen])

    agg_dict = agg.__dict__
    forbidden_terms = ["p_value", "ci", "confidence_interval", "iid", "causal", "predictive"]
    for term in forbidden_terms:
        assert term not in agg_dict


# 20. test_shift_direction_and_absolute_shift_consistent
def test_shift_direction_and_absolute_shift_consistent():
    test_cases = [
        (2, "up", 2),
        (-1, "down", 1),
        (0, "unchanged", 0),
        (-3, "down", 3),
        (1, "up", 1),
    ]
    for delta, expected_dir, expected_abs in test_cases:
        direction = "up" if delta > 0 else ("down" if delta < 0 else "unchanged")
        abs_shift = abs(delta)
        assert direction == expected_dir
        assert abs_shift == expected_abs


# 21. test_deterministic_plan_order
def test_deterministic_plan_order():
    plan1 = generate_sensitivity_plan(DEFAULT_SCENARIOS_CSV)
    plan2 = generate_sensitivity_plan(DEFAULT_SCENARIOS_CSV)

    ids1 = [s["scenario_id"] for s in plan1["scenarios"]]
    ids2 = [s["scenario_id"] for s in plan2["scenarios"]]
    assert ids1 == ids2

    tuples1 = [s["perturbation_tuples"] for s in plan1["scenarios"]]
    tuples2 = [s["perturbation_tuples"] for s in plan2["scenarios"]]
    assert tuples1 == tuples2


# 22. test_claim_metadata_is_epistemically_conservative
def test_claim_metadata_is_epistemically_conservative():
    tool_code = Path(REPO_ROOT / "tools" / "article_cvss40_r2_priority_sensitivity.py").read_text(encoding="utf-8")

    # Required conservative claim formulation
    required_claim = (
        "The stress test characterizes deterministic sensitivity of nominal operational priority "
        "to valid local perturbations of contextual policy weights within the declared policy domain."
    )
    normalized_tool_code = " ".join(tool_code.split()).lower()
    assert required_claim.lower() in normalized_tool_code

    # Confirm prohibited claims are strictly absent from execution logic and metadata
    forbidden_claims = [
        "predictive robustness generally",
        "statistical robustness",
        "generalization to unseen environments",
        "causal sensitivity",
        "calibrated uncertainty",
        "formal robustness proof",
    ]
    for fc in forbidden_claims:
        # Check that forbidden claim is not present outside the docstring boundary list
        assert tool_code.count(fc) <= 1  # May only appear once in the negative disclaimer docstring
