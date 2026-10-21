"""
Deterministic Contextual Priority Sensitivity Stress Test for CVSS v4.0.

Authoritative tool for evaluating local stability and sensitivity of nominal
operational priority (B4_nominal) under valid ordinal perturbations of contextual
policy weights within declared specification boundaries:
  w_context in {-2, 0, 1, 2, 3}
  w_control in {-1, 0}

Scientific framing:
The stress test characterizes deterministic sensitivity of nominal operational
priority to valid local perturbations of contextual policy weights within the declared
policy domain. It is a descriptive stability stress test, NOT a predictive generalization
test, cross-validation, probabilistic uncertainty quantification, or causal inference.

Reuses core/cvss40_environmental_policy.py exclusively without duplication.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.cvss40_environmental_policy import (
    PRIORITY_ORDER,
    SEVERITY_TO_PRIORITY,
    lookup_nominal_weights,
    ordinal_to_priority,
    priority_to_ordinal,
    recompute_p_base,
    recompute_p_env_nominal,
)

# ==============================================================================
# Declared Domain Constants
# ==============================================================================

VALID_CONTEXT_WEIGHTS: List[int] = [-2, 0, 1, 2, 3]
VALID_CONTROL_WEIGHTS: List[int] = [-1, 0]

CURATED_NVD_DEVIATIONS: set[str] = {
    "SCN-NVD-001",
    "SCN-NVD-006",
    "SCN-NVD-007",
    "SCN-NVD-008",
}

DEFAULT_SCENARIOS_CSV = REPO_ROOT / "data" / "article" / "cvss40_environmental_scenarios.csv"


# ==============================================================================
# Dataclasses
# ==============================================================================

@dataclass
class SensitivityPerturbationResult:
    """Individual perturbation outcome for a single scenario."""
    perturbation_id: str
    scenario_id: str
    w_context: int
    w_control: int
    context_relation: str  # "nominal", "down", "up"
    control_relation: str  # "nominal", "flipped"
    p_env_perturbed: str
    g_env_perturbed: int
    ordinal_delta_vs_nominal: int
    changed: bool
    shift_direction: str  # "unchanged", "up", "down"
    abs_ordinal_shift: int


@dataclass
class ScenarioSensitivityResult:
    """Consolidated sensitivity assessment for a single scenario across valid perturbations."""
    scenario_id: str
    source_type: str
    asset_class: str
    cve_id: Optional[str]
    base_priority: str
    g_base: int
    nominal_w_context: int
    nominal_w_control: int
    nominal_p_env: str
    g_nominal_p_env: int
    observed_p_env: str
    is_curated_nvd_deviation: bool
    total_valid_perturbations: int
    unchanged_count: int
    changed_count: int
    upward_count: int
    downward_count: int
    unchanged_rate: float
    max_abs_ordinal_shift: int
    mean_abs_ordinal_shift: float
    is_stable: bool
    perturbations: List[SensitivityPerturbationResult] = field(default_factory=list)


@dataclass
class SensitivityAggregate:
    """Descriptive aggregate metrics for a scenario subset."""
    subset_name: str
    scenario_count: int
    total_perturbation_cases: int
    unchanged_count: int
    unchanged_rate: float
    changed_count: int
    changed_rate: float
    upward_count: int
    downward_count: int
    mean_signed_shift: float
    mean_abs_shift: float
    max_abs_shift: int
    stable_scenarios_count: int
    sensitive_scenarios_count: int
    shift_magnitude_distribution: Dict[str, int] = field(default_factory=dict)


@dataclass
class PrioritySensitivityReport:
    """Root artifact representing the complete sensitivity stress test results."""
    generated_at_utc: str
    schema_version: str
    methodological_statement: str
    canonical_scope: str
    domains: Dict[str, List[int]]
    nominal_baseline_definition: str
    curated_deviation_ids: List[str]
    total_scenarios: int
    total_grid_combinations: int
    total_strictly_perturbed_cases: int
    total_aggregate: SensitivityAggregate
    nvd_aggregate: SensitivityAggregate
    synthetic_aggregate: SensitivityAggregate
    profile_aggregates: Dict[str, SensitivityAggregate]
    scenarios: List[ScenarioSensitivityResult] = field(default_factory=list)


# ==============================================================================
# Pure Helper Functions
# ==============================================================================

def get_valid_context_neighbors(w_ctx: int) -> List[Tuple[int, str]]:
    """
    Returns ordered valid context candidates:
    - context_down: nearest valid lower neighbor in [-2, 0, 1, 2, 3], if exists
    - context_nominal: w_ctx
    - context_up: nearest valid upper neighbor in [-2, 0, 1, 2, 3], if exists
    """
    if w_ctx not in VALID_CONTEXT_WEIGHTS:
        raise ValueError(f"Context weight {w_ctx} outside valid domain {VALID_CONTEXT_WEIGHTS}")

    idx = VALID_CONTEXT_WEIGHTS.index(w_ctx)
    candidates: List[Tuple[int, str]] = []

    if idx > 0:
        candidates.append((VALID_CONTEXT_WEIGHTS[idx - 1], "down"))

    candidates.append((w_ctx, "nominal"))

    if idx < len(VALID_CONTEXT_WEIGHTS) - 1:
        candidates.append((VALID_CONTEXT_WEIGHTS[idx + 1], "up"))

    return candidates


def get_valid_control_states(w_ctrl: int) -> List[Tuple[int, str]]:
    """
    Returns valid control candidates in {-1, 0}:
    - control_nominal: w_ctrl
    - control_flipped: flipped state (-1 <-> 0)
    """
    if w_ctrl not in VALID_CONTROL_WEIGHTS:
        raise ValueError(f"Control weight {w_ctrl} outside valid domain {VALID_CONTROL_WEIGHTS}")

    flipped = 0 if w_ctrl == -1 else -1
    return [(w_ctrl, "nominal"), (flipped, "flipped")]


def generate_scenario_perturbation_grid(
    w_ctx: int,
    w_ctrl: int,
    include_nominal: bool = False,
) -> List[Tuple[int, int, str, str]]:
    """
    Generates all valid combinations of context neighbors and control states.
    Returns list of (w_context, w_control, context_relation, control_relation).
    """
    ctx_candidates = get_valid_context_neighbors(w_ctx)
    ctrl_candidates = get_valid_control_states(w_ctrl)

    grid: List[Tuple[int, int, str, str]] = []
    for c_val, c_rel in ctx_candidates:
        for k_val, k_rel in ctrl_candidates:
            if not include_nominal and c_rel == "nominal" and k_rel == "nominal":
                continue
            grid.append((c_val, k_val, c_rel, k_rel))
    return grid


def evaluate_single_perturbation(
    scenario_id: str,
    base_priority: str,
    nominal_p_env: str,
    w_ctx_pert: int,
    w_ctrl_pert: int,
    c_rel: str,
    k_rel: str,
    perturbation_index: int,
) -> SensitivityPerturbationResult:
    """Evaluates one perturbed policy tuple on a scenario."""
    g_base = priority_to_ordinal(base_priority)
    g_nom = priority_to_ordinal(nominal_p_env)

    # Recompute priority using canonical clamped specification
    g_pert = max(0, min(len(PRIORITY_ORDER) - 1, g_base + w_ctx_pert + w_ctrl_pert))
    p_env_pert = ordinal_to_priority(g_pert)

    delta = g_pert - g_nom
    changed = (delta != 0)
    shift_dir = "up" if delta > 0 else ("down" if delta < 0 else "unchanged")
    abs_shift = abs(delta)

    pert_id = f"{scenario_id}-PERT-{perturbation_index:02d}"
    return SensitivityPerturbationResult(
        perturbation_id=pert_id,
        scenario_id=scenario_id,
        w_context=w_ctx_pert,
        w_control=w_ctrl_pert,
        context_relation=c_rel,
        control_relation=k_rel,
        p_env_perturbed=p_env_pert,
        g_env_perturbed=g_pert,
        ordinal_delta_vs_nominal=delta,
        changed=changed,
        shift_direction=shift_dir,
        abs_ordinal_shift=abs_shift,
    )


def evaluate_scenario_sensitivity(
    scenario_row: Dict[str, str],
    include_nominal_in_perturbations: bool = False,
) -> ScenarioSensitivityResult:
    """Evaluates complete perturbation grid for a single scenario row."""
    scenario_id = scenario_row["scenario_id"]
    asset_class = scenario_row["asset_class"]
    cve_id = scenario_row.get("cve_id") or None
    source_type = "nvd" if (cve_id and cve_id.strip()) else "synthetic"

    base_priority = scenario_row["base_priority"]
    g_base = priority_to_ordinal(base_priority)

    nom_w_ctx, nom_w_ctrl = lookup_nominal_weights(asset_class)
    nom_p_env, _ = recompute_p_env_nominal(base_priority, asset_class)
    g_nom = priority_to_ordinal(nom_p_env)

    observed_p_env = scenario_row["environmental_priority"]
    is_dev = scenario_id in CURATED_NVD_DEVIATIONS

    grid = generate_scenario_perturbation_grid(
        nom_w_ctx, nom_w_ctrl, include_nominal=include_nominal_in_perturbations
    )

    perturbations: List[SensitivityPerturbationResult] = []
    for idx, (c_val, k_val, c_rel, k_rel) in enumerate(grid, start=1):
        res = evaluate_single_perturbation(
            scenario_id=scenario_id,
            base_priority=base_priority,
            nominal_p_env=nom_p_env,
            w_ctx_pert=c_val,
            w_ctrl_pert=k_val,
            c_rel=c_rel,
            k_rel=k_rel,
            perturbation_index=idx,
        )
        perturbations.append(res)

    total_pert = len(perturbations)
    unchanged = sum(1 for p in perturbations if not p.changed)
    changed = sum(1 for p in perturbations if p.changed)
    upward = sum(1 for p in perturbations if p.shift_direction == "up")
    downward = sum(1 for p in perturbations if p.shift_direction == "down")

    unchanged_rate = unchanged / total_pert if total_pert > 0 else 1.0
    abs_shifts = [p.abs_ordinal_shift for p in perturbations]
    max_shift = max(abs_shifts) if abs_shifts else 0
    mean_shift = sum(abs_shifts) / total_pert if total_pert > 0 else 0.0
    is_stable = (changed == 0)

    return ScenarioSensitivityResult(
        scenario_id=scenario_id,
        source_type=source_type,
        asset_class=asset_class,
        cve_id=cve_id,
        base_priority=base_priority,
        g_base=g_base,
        nominal_w_context=nom_w_ctx,
        nominal_w_control=nom_w_ctrl,
        nominal_p_env=nom_p_env,
        g_nominal_p_env=g_nom,
        observed_p_env=observed_p_env,
        is_curated_nvd_deviation=is_dev,
        total_valid_perturbations=total_pert,
        unchanged_count=unchanged,
        changed_count=changed,
        upward_count=upward,
        downward_count=downward,
        unchanged_rate=round(unchanged_rate, 4),
        max_abs_ordinal_shift=max_shift,
        mean_abs_ordinal_shift=round(mean_shift, 4),
        is_stable=is_stable,
        perturbations=perturbations,
    )


def compute_sensitivity_aggregate(
    subset_name: str,
    scenario_results: List[ScenarioSensitivityResult],
) -> SensitivityAggregate:
    """Computes aggregate descriptive statistics across a list of evaluated scenarios."""
    scen_count = len(scenario_results)
    if scen_count == 0:
        return SensitivityAggregate(
            subset_name=subset_name,
            scenario_count=0,
            total_perturbation_cases=0,
            unchanged_count=0,
            unchanged_rate=0.0,
            changed_count=0,
            changed_rate=0.0,
            upward_count=0,
            downward_count=0,
            mean_signed_shift=0.0,
            mean_abs_shift=0.0,
            max_abs_shift=0,
            stable_scenarios_count=0,
            sensitive_scenarios_count=0,
            shift_magnitude_distribution={},
        )

    all_perturbations: List[SensitivityPerturbationResult] = []
    for s in scenario_results:
        all_perturbations.extend(s.perturbations)

    tot_cases = len(all_perturbations)
    unchanged = sum(1 for p in all_perturbations if not p.changed)
    changed = sum(1 for p in all_perturbations if p.changed)
    upward = sum(1 for p in all_perturbations if p.shift_direction == "up")
    downward = sum(1 for p in all_perturbations if p.shift_direction == "down")

    unchanged_rate = unchanged / tot_cases if tot_cases > 0 else 0.0
    changed_rate = changed / tot_cases if tot_cases > 0 else 0.0

    signed_shifts = [p.ordinal_delta_vs_nominal for p in all_perturbations]
    abs_shifts = [p.abs_ordinal_shift for p in all_perturbations]

    mean_signed = sum(signed_shifts) / tot_cases if tot_cases > 0 else 0.0
    mean_abs = sum(abs_shifts) / tot_cases if tot_cases > 0 else 0.0
    max_abs = max(abs_shifts) if abs_shifts else 0

    stable_count = sum(1 for s in scenario_results if s.is_stable)
    sensitive_count = scen_count - stable_count

    mag_dist: Dict[str, int] = {}
    for d in sorted(set(abs_shifts)):
        mag_dist[str(d)] = sum(1 for a in abs_shifts if a == d)

    return SensitivityAggregate(
        subset_name=subset_name,
        scenario_count=scen_count,
        total_perturbation_cases=tot_cases,
        unchanged_count=unchanged,
        unchanged_rate=round(unchanged_rate, 4),
        changed_count=changed,
        changed_rate=round(changed_rate, 4),
        upward_count=upward,
        downward_count=downward,
        mean_signed_shift=round(mean_signed, 4),
        mean_abs_shift=round(mean_abs, 4),
        max_abs_shift=max_abs,
        stable_scenarios_count=stable_count,
        sensitive_scenarios_count=sensitive_count,
        shift_magnitude_distribution=mag_dist,
    )


# ==============================================================================
# Plan & Execution
# ==============================================================================

def generate_sensitivity_plan(scenarios_csv: Path = DEFAULT_SCENARIOS_CSV) -> Dict[str, Any]:
    """Generates a deterministic plan of the sensitivity stress test without executing evaluation."""
    if not scenarios_csv.exists():
        raise FileNotFoundError(f"Scenarios CSV not found at {scenarios_csv}")

    with open(scenarios_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    rows_sorted = sorted(rows, key=lambda r: r["scenario_id"])

    plan_scenarios = []
    total_grid = 0
    total_strictly_perturbed = 0

    for r in rows_sorted:
        scen_id = r["scenario_id"]
        asset_class = r["asset_class"]
        nom_w_ctx, nom_w_ctrl = lookup_nominal_weights(asset_class)
        grid_strictly_perturbed = generate_scenario_perturbation_grid(nom_w_ctx, nom_w_ctrl, include_nominal=False)
        grid_full = generate_scenario_perturbation_grid(nom_w_ctx, nom_w_ctrl, include_nominal=True)

        total_grid += len(grid_full)
        total_strictly_perturbed += len(grid_strictly_perturbed)

        plan_scenarios.append({
            "scenario_id": scen_id,
            "asset_class": asset_class,
            "nominal_w_context": nom_w_ctx,
            "nominal_w_control": nom_w_ctrl,
            "strictly_perturbed_count": len(grid_strictly_perturbed),
            "full_grid_count": len(grid_full),
            "perturbation_tuples": [
                {"w_context": c, "w_control": k, "ctx_rel": cr, "ctrl_rel": kr}
                for c, k, cr, kr in grid_strictly_perturbed
            ],
        })

    return {
        "scenarios_csv": str(scenarios_csv),
        "total_scenarios": len(rows_sorted),
        "total_grid_combinations": total_grid,
        "total_strictly_perturbed_cases": total_strictly_perturbed,
        "valid_context_weights": VALID_CONTEXT_WEIGHTS,
        "valid_control_weights": VALID_CONTROL_WEIGHTS,
        "curated_nvd_deviations_tracked": sorted(list(CURATED_NVD_DEVIATIONS)),
        "scenarios": plan_scenarios,
    }


def run_priority_sensitivity_stress_test(
    scenarios_csv: Path = DEFAULT_SCENARIOS_CSV,
    include_nominal_baseline: bool = False,
) -> PrioritySensitivityReport:
    """Executes the full deterministic sensitivity stress test across canonical scenarios."""
    if not scenarios_csv.exists():
        raise FileNotFoundError(f"Scenarios CSV not found at {scenarios_csv}")

    with open(scenarios_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    rows_sorted = sorted(rows, key=lambda r: r["scenario_id"])

    scenario_results: List[ScenarioSensitivityResult] = []
    for r in rows_sorted:
        res = evaluate_scenario_sensitivity(r, include_nominal_in_perturbations=include_nominal_baseline)
        scenario_results.append(res)

    total_agg = compute_sensitivity_aggregate("total_corpus", scenario_results)

    nvd_results = [s for s in scenario_results if s.source_type == "nvd"]
    syn_results = [s for s in scenario_results if s.source_type == "synthetic"]

    nvd_agg = compute_sensitivity_aggregate("nvd_curated", nvd_results)
    syn_agg = compute_sensitivity_aggregate("synthetic_curated", syn_results)

    # Profile aggregates
    profile_aggregates: Dict[str, SensitivityAggregate] = {}
    profiles = sorted(set(s.asset_class for s in scenario_results))
    for prof in profiles:
        prof_res = [s for s in scenario_results if s.asset_class == prof]
        profile_aggregates[prof] = compute_sensitivity_aggregate(f"profile_{prof}", prof_res)

    tot_grid = sum(s.total_valid_perturbations + (0 if include_nominal_baseline else 1) for s in scenario_results)
    tot_strictly_pert = sum(s.total_valid_perturbations for s in scenario_results)

    return PrioritySensitivityReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        schema_version="1.0.0-r2-sensitivity",
        methodological_statement="The stress test characterizes deterministic sensitivity of nominal operational priority to valid local perturbations of contextual policy weights within the declared policy domain.",
        canonical_scope="30 canonical scenarios (12 NVD, 18 Synthetic)",
        domains={
            "w_context": VALID_CONTEXT_WEIGHTS,
            "w_control": VALID_CONTROL_WEIGHTS,
        },
        nominal_baseline_definition="B4_nominal evaluated via core.cvss40_environmental_policy.recompute_p_env_nominal",
        curated_deviation_ids=sorted(list(CURATED_NVD_DEVIATIONS)),
        total_scenarios=len(scenario_results),
        total_grid_combinations=tot_grid,
        total_strictly_perturbed_cases=tot_strictly_pert,
        total_aggregate=total_agg,
        nvd_aggregate=nvd_agg,
        synthetic_aggregate=syn_agg,
        profile_aggregates=profile_aggregates,
        scenarios=scenario_results,
    )


# ==============================================================================
# CLI
# ==============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic Contextual Priority Sensitivity Stress Test for CVSS v4.0"
    )
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print deterministic evaluation plan without running the full test",
    )
    parser.add_argument(
        "--scenarios-csv",
        type=Path,
        default=DEFAULT_SCENARIOS_CSV,
        help="Path to scenarios CSV (default: data/article/cvss40_environmental_scenarios.csv)",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Output path for JSON report",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=None,
        help="Output path for tabular case-level CSV",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose stdout reporting",
    )
    args = parser.parse_args()

    if args.plan_only:
        plan = generate_sensitivity_plan(args.scenarios_csv)
        if not args.quiet:
            print("=================================================================")
            print("DETERMINISTIC CONTEXTUAL PRIORITY SENSITIVITY STRESS TEST PLAN")
            print("=================================================================")
            print(f"Scenarios CSV:                 {plan['scenarios_csv']}")
            print(f"Total Scenarios:               {plan['total_scenarios']}")
            print(f"Total Full Grid Combinations:  {plan['total_grid_combinations']}")
            print(f"Total Strictly Perturbed Cases:{plan['total_strictly_perturbed_cases']}")
            print(f"Valid Context Weights:         {plan['valid_context_weights']}")
            print(f"Valid Control Weights:         {plan['valid_control_weights']}")
            print(f"Curated NVD Deviations:        {plan['curated_nvd_deviations_tracked']}")
            print("-----------------------------------------------------------------")
            print("PLAN_STATUS: READY_TO_RUN")
        return 0

    # If full run is requested in future orders:
    report = run_priority_sensitivity_stress_test(args.scenarios_csv)

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
        if not args.quiet:
            print(f"Saved sensitivity JSON report to {args.output_json}")

    if args.output_csv:
        args.output_csv.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "scenario_id",
            "source_type",
            "asset_class",
            "nominal_w_context",
            "nominal_w_control",
            "perturbed_w_context",
            "perturbed_w_control",
            "nominal_priority",
            "perturbed_priority",
            "ordinal_delta",
            "abs_shift",
            "shift_direction",
            "changed",
            "curated_nvd_deviation",
            "perturbation_id",
            "base_priority",
            "context_relation",
            "control_relation",
        ]
        with open(args.output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in report.scenarios:
                for p in s.perturbations:
                    writer.writerow({
                        "scenario_id": s.scenario_id,
                        "source_type": s.source_type,
                        "asset_class": s.asset_class,
                        "nominal_w_context": s.nominal_w_context,
                        "nominal_w_control": s.nominal_w_control,
                        "perturbed_w_context": p.w_context,
                        "perturbed_w_control": p.w_control,
                        "nominal_priority": s.nominal_p_env,
                        "perturbed_priority": p.p_env_perturbed,
                        "ordinal_delta": p.ordinal_delta_vs_nominal,
                        "abs_shift": p.abs_ordinal_shift,
                        "shift_direction": p.shift_direction,
                        "changed": p.changed,
                        "curated_nvd_deviation": s.is_curated_nvd_deviation,
                        "perturbation_id": p.perturbation_id,
                        "base_priority": s.base_priority,
                        "context_relation": p.context_relation,
                        "control_relation": p.control_relation,
                    })
        if not args.quiet:
            print(f"Saved sensitivity CSV cases to {args.output_csv}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
