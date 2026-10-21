"""
Unit tests for Ablation and Baseline Infrastructure (tools/article_cvss40_r2_ablation_baselines.py).

Verifies the mathematical, policy, and architectural isolation of Baselines B0-B4:
  B0: Base Severity Only
  B1: Environmental Score Only (CVSS-BE)
  B2: Context-Only Policy (w_context only)
  B3: Controls-Only Policy (w_control only)
  B4: Full Policy (B4_nominal vs B4_observed)

Epistemological Boundaries:
Self-contained unsealed test fixtures and canonical dataset contract assertions.
No access to confirmatory datasets C1/C2; strictly descriptive benchmark evaluation.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Dict

import pytest

import core.cvss40 as canonical_cvss40
import core.cvss40_environmental_policy as canonical_policy
import tools.article_cvss40_r2_ablation_baselines as ablation_tool
from tools.article_cvss40_r2_ablation_baselines import (
    AblationExperimentReport,
    BaselineMetricGroup,
    ScenarioAblationResult,
    aggregate_ablation_metrics,
    compute_b1_environmental_score,
    compute_metric_group,
    evaluate_scenario_ablation,
    extract_candidate_requirements,
    load_canonical_scenarios,
)


# ==============================================================================
# Isolated Unsealed Fixtures
# ==============================================================================

MOCK_ROW_PUBLIC_WEB: Dict[str, str] = {
    "scenario_id": "MOCK-NVD-001",
    "cve_id": "CVE-2026-0001",
    "cvss_b_score": "1.1",
    "cvss_b_severity": "LOW",
    "asset_class": "public_web_application",
    "confidentiality_requirement": "CR:H - high confidentiality",
    "integrity_requirement": "IR:H - high integrity",
    "availability_requirement": "AR:M - medium availability",
    "official_cvss_v4_vector": "CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N",
    "environmental_priority": "low",
}

MOCK_ROW_LAB: Dict[str, str] = {
    "scenario_id": "MOCK-SYN-013",
    "cve_id": "",
    "cvss_b_score": "6.8",
    "cvss_b_severity": "MEDIUM",
    "asset_class": "isolated_lab_system",
    "confidentiality_requirement": "CR:L - low",
    "integrity_requirement": "IR:L - low",
    "availability_requirement": "AR:L - low",
    "official_cvss_v4_vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N",
    "environmental_priority": "defer",
}


# ==============================================================================
# 1. B0 — Base Severity Only
# ==============================================================================

def test_b0_uses_base_severity_only():
    """Confirms that B0 strictly reflects Base severity via policy mapping, independent of context."""
    res = evaluate_scenario_ablation(MOCK_ROW_PUBLIC_WEB)
    assert res.b0 == "low"
    assert res.b0 == canonical_policy.recompute_p_base(MOCK_ROW_PUBLIC_WEB["cvss_b_severity"])

    # Modifying context weights must have zero impact on B0
    tampered_row = copy.deepcopy(MOCK_ROW_PUBLIC_WEB)
    tampered_row["asset_class"] = "public_api_gateway"  # w_context = +3
    res_tampered = evaluate_scenario_ablation(tampered_row)
    assert res_tampered.b0 == "low"


# ==============================================================================
# 2. B1 — Environmental Score Only
# ==============================================================================

def test_b1_uses_environmental_score_only():
    """Confirms that B1 derives from CVSS-BE score without categorical policy layer."""
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"
    rows = load_canonical_scenarios(csv_path)

    # In SCN-SYN-016: Base=6.8 (medium) -> Env=8.4 (High) -> P_B1=high != P_B0 (medium)
    row_scn16 = next(r for r in rows if r["scenario_id"] == "SCN-SYN-016")
    res_16 = evaluate_scenario_ablation(row_scn16)

    assert res_16.b0 == "medium"
    assert res_16.s_env == 8.4
    assert res_16.p_b1 == "high"
    assert res_16.b1 == "high"
    assert res_16.b1 != res_16.b0


# ==============================================================================
# 3. B2 — Context-Only Policy
# ==============================================================================

def test_b2_context_only():
    """Confirms that B2 applies only w_context while w_control is held at 0."""
    # public_web_application has w_context = +2, w_control = -1
    # P_base = low (ordinal 1)
    # B2 should be: clamp(1 + 2) = 3 -> "high"
    res = evaluate_scenario_ablation(MOCK_ROW_PUBLIC_WEB)
    assert res.w_context == 2
    assert res.w_control == -1
    assert res.b2 == "high"
    assert canonical_policy.priority_to_ordinal(res.b2) == 3


# ==============================================================================
# 4. B3 — Control-Only Policy
# ==============================================================================

def test_b3_control_only():
    """Confirms that B3 applies only w_control while w_context is held at 0."""
    # public_web_application has w_context = +2, w_control = -1
    # P_base = low (ordinal 1)
    # B3 should be: clamp(1 - 1) = 0 -> "defer"
    res = evaluate_scenario_ablation(MOCK_ROW_PUBLIC_WEB)
    assert res.b3 == "defer"
    assert canonical_policy.priority_to_ordinal(res.b3) == 0


# ==============================================================================
# 5. B4 — Nominal Full Policy
# ==============================================================================

def test_b4_nominal_full_policy():
    """Confirms that B4_nominal applies w_context + w_control with ordinal clamp."""
    # public_web_application: P_base=low (1), w_context=+2, w_control=-1
    # B4_nominal = clamp(1 + 2 - 1) = 2 -> "medium"
    res = evaluate_scenario_ablation(MOCK_ROW_PUBLIC_WEB)
    assert res.b4_nominal == "medium"
    assert canonical_policy.priority_to_ordinal(res.b4_nominal) == 2


# ==============================================================================
# 6. Ordinal Clamp Bounds
# ==============================================================================

def test_clamp_bounds():
    """Confirms that ordinal bounds are strictly preserved within [0, 4]."""
    # Lower clamp bound test: P_base = low (1), asset = isolated_lab_system (w_context = -2, w_control = -1)
    # Net delta = -3. 1 - 3 = -2 -> clamped to 0 ("defer")
    clamp_low_row = copy.deepcopy(MOCK_ROW_LAB)
    clamp_low_row["cvss_b_severity"] = "LOW"
    res_low = evaluate_scenario_ablation(clamp_low_row)
    assert res_low.b4_nominal == "defer"
    assert canonical_policy.priority_to_ordinal(res_low.b4_nominal) == 0

    # Upper clamp bound test: P_base = critical (4), asset = public_api_gateway (w_context = +3, w_control = -1)
    # B2 alone would be 4 + 3 = 7 -> clamped to 4 ("critical")
    clamp_high_row = copy.deepcopy(MOCK_ROW_PUBLIC_WEB)
    clamp_high_row["cvss_b_severity"] = "CRITICAL"
    clamp_high_row["asset_class"] = "public_api_gateway"
    res_high = evaluate_scenario_ablation(clamp_high_row)
    assert res_high.b2 == "critical"
    assert canonical_policy.priority_to_ordinal(res_high.b2) == 4


# ==============================================================================
# 7. Policy Source Integrity
# ==============================================================================

def test_policy_source_is_canonical():
    """Confirms that the tool reuses core.cvss40_environmental_policy without duplication."""
    assert ablation_tool.policy is canonical_policy
    assert ablation_tool.policy.PRIORITY_ORDER == canonical_policy.PRIORITY_ORDER
    assert ablation_tool.policy.ENV_PROFILES_BY_ASSET == canonical_policy.ENV_PROFILES_BY_ASSET


# ==============================================================================
# 8. Scope Derived Exclusively from Reference CSV
# ==============================================================================

def test_scope_is_exactly_canonical_csv():
    """Confirms that the scenario list is strictly derived from reference CSV (30 items)."""
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"
    scenarios = load_canonical_scenarios(csv_path)

    assert len(scenarios) == 30
    sids = [s["scenario_id"] for s in scenarios]

    expected_nvd = [f"SCN-NVD-{i:03d}" for i in range(1, 13)]
    expected_syn = [f"SCN-SYN-{i:03d}" for i in range(13, 31)]
    assert sids == expected_nvd + expected_syn

    # Legacy artifacts must never enter the canonical ablation scope
    for i in range(1, 13):
        assert f"SCN-SYN-{i:03d}" not in sids


# ==============================================================================
# 9. Curated Override Detection Contract
# ==============================================================================

def test_curated_override_detection_matches_current_benchmark():
    """
    Contract assertion: confirms that the divergence between B4_nominal and B4_observed
    occurs in exactly the four curated NVD scenarios documented in the benchmark.
    """
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"
    rows = load_canonical_scenarios(csv_path)

    results = [evaluate_scenario_ablation(r) for r in rows]
    divergent_ids = {r.scenario_id for r in results if r.curated_override}

    expected_divergent = {"SCN-NVD-001", "SCN-NVD-006", "SCN-NVD-007", "SCN-NVD-008"}
    assert divergent_ids == expected_divergent

    # All remaining 26 scenarios must exhibit exact match between nominal and observed
    for r in results:
        if r.scenario_id not in expected_divergent:
            assert r.b4_nominal == r.b4_observed
            assert r.curated_override is False


# ==============================================================================
# 10. Curated Override Not Treated as Arithmetic Error
# ==============================================================================

def test_curated_override_not_treated_as_arithmetic_error():
    """Confirms that curated overrides are preserved as structured divergence, not calculation failures."""
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"
    rows = load_canonical_scenarios(csv_path)

    results = [evaluate_scenario_ablation(r) for r in rows]
    divergent_results = [r for r in results if r.curated_override]

    for r in divergent_results:
        # Nominal computation must still be completely valid
        assert r.b4_nominal in canonical_policy.PRIORITY_ORDER
        assert r.b4_observed in canonical_policy.PRIORITY_ORDER
        assert r.b4_nominal != r.b4_observed
        # Internal delta between observed and base priority is mathematically sound
        delta = canonical_policy.compute_delta_cat(r.p_base, r.b4_observed)
        assert -4 <= delta <= 4


# ==============================================================================
# 11. Aggregate Metrics Partitioning
# ==============================================================================

def test_aggregate_metrics_partitioning():
    """Confirms that aggregation correctly partitions Total (N=30), NVD (N=12), and Synthetic (N=18)."""
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"
    rows = load_canonical_scenarios(csv_path)

    results = [evaluate_scenario_ablation(r) for r in rows]
    report = aggregate_ablation_metrics(results, canonical_expected=30)

    assert report.total_scenarios == 30
    assert report.nvd_scenarios == 12
    assert report.synthetic_scenarios == 18
    assert report.canonical_expected == 30
    assert report.canonical_found == 30

    for b in ["B0", "B1", "B2", "B3", "B4_nominal", "B4_observed"]:
        assert b in report.baseline_summaries
        summ = report.baseline_summaries[b]
        assert "total" in summ
        assert "nvd" in summ
        assert "synthetic" in summ


# ==============================================================================
# 12. Aggregate Metrics Are Descriptive Only
# ==============================================================================

def test_aggregate_metrics_are_descriptive_only():
    """Confirms absence of inferential CI, p-value, or IID claims in serialized output."""
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"
    rows = load_canonical_scenarios(csv_path)

    results = [evaluate_scenario_ablation(r) for r in rows]
    report = aggregate_ablation_metrics(results, canonical_expected=30)

    import dataclasses
    report_dict = dataclasses.asdict(report)
    serialized = str(report_dict).lower()

    forbidden_statistical_terms = [
        "confidence_interval",
        "ci_lower",
        "ci_upper",
        "p_value",
        "pvalue",
        "t_test",
        "anova",
        "iid_assumption",
    ]
    for term in forbidden_statistical_terms:
        assert term not in serialized


# ==============================================================================
# 13. B4 Nominal Divergence Count Is Four
# ==============================================================================

def test_b4_nominal_divergence_count_is_four():
    """Confirms that aggregate report records exactly 4 curated divergences."""
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"
    rows = load_canonical_scenarios(csv_path)

    results = [evaluate_scenario_ablation(r) for r in rows]
    report = aggregate_ablation_metrics(results, canonical_expected=30)

    assert report.nominal_vs_observed_divergence_count == 4
    assert report.nominal_vs_observed_divergent_ids == [
        "SCN-NVD-001",
        "SCN-NVD-006",
        "SCN-NVD-007",
        "SCN-NVD-008",
    ]


# ==============================================================================
# 14. Difference Metrics Mathematical Consistency
# ==============================================================================

def test_difference_metrics_consistency():
    """Confirms internal arithmetic consistency of exact matches, signed/abs diffs, and distribution."""
    # Create controlled fixture of 3 results
    r1 = copy.deepcopy(MOCK_ROW_PUBLIC_WEB)
    r2 = copy.deepcopy(MOCK_ROW_LAB)
    res_list = [evaluate_scenario_ablation(r1), evaluate_scenario_ablation(r2)]

    mg = compute_metric_group(res_list, "B0")

    # Sum of counts in ordinal_diff_distribution must equal total N
    assert sum(mg.ordinal_diff_distribution.values()) == 2
    # Match count must match entries where diff == 0
    zero_diffs = mg.ordinal_diff_distribution.get(0, 0)
    assert mg.exact_matches_vs_observed == zero_diffs
    assert mg.match_rate_vs_observed == round(zero_diffs / 2, 4)
    assert mg.mean_absolute_ordinal_diff >= 0.0
