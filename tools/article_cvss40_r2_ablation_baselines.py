#!/usr/bin/env python3
"""
Ablation and Baseline Analysis (B0-B4) for CVSS v4.0 Environmental Metric Normalization.

This tool operationalizes systematic ablation analysis across five baseline configurations (B0-B4)
evaluated over the 30 canonical scenarios (data/article/cvss40_environmental_scenarios.csv):

  B0 — Base Severity Only:
       P_B0 = severity(S_base) mapped to categorical priority.
       Evaluates prioritization using only intrinsic vulnerability severity without context.

  B1 — Environmental Score Only:
       P_B1 = severity(S_env) derived from CVSS-BE score via official CVSS v4.0 scoring grammar.
       Evaluates standard CVSS v4.0 Environmental vector adjustment without categorical policy layer.

  B2 — Context-Only Policy:
       P_B2 derived by applying only nominal context weight w_context with w_control = 0.
       Evaluates asset criticality and exposure impact in isolation.

  B3 — Controls-Only Policy:
       P_B3 derived by applying only compensating control weight w_control with w_context = 0.
       Evaluates defensive mitigating controls in isolation.

  B4 — Full Policy:
       Integrates context and control weights:
       - B4_nominal: Recomputed deterministically from structured policy weights.
       - B4_observed: Stored operational priority recorded in canonical benchmark traces.
       Distinguishes nominal recomputation from curated narrative adjustments (SCN-NVD-001, 006, 007, 008).

Epistemological Boundaries:
Deterministic descriptive benchmark evaluation across N=30 scenarios.
No inferential population claims, no IID assumptions, and no assertion of formal proof.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

# Reusable canonical scorers and policy
try:
    import core.cvss40 as cvss40
    import core.cvss40_environmental_policy as policy
except ImportError:
    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    import core.cvss40 as cvss40
    import core.cvss40_environmental_policy as policy


# ==============================================================================
# Data Structures
# ==============================================================================

@dataclass
class ScenarioAblationResult:
    scenario_id: str
    source_type: str  # "NVD" or "SYNTHETIC"
    cve_id: str
    s_base: float
    p_base: str
    s_env: float
    p_b1: str
    environment_profile: str
    w_context: int
    w_control: int
    b0: str
    b1: str
    b2: str
    b3: str
    b4_nominal: str
    b4_observed: str
    curated_override: bool
    ordinal_differences_vs_observed: Dict[str, int] = field(default_factory=dict)
    category_shifts_vs_b0: Dict[str, int] = field(default_factory=dict)


@dataclass
class BaselineMetricGroup:
    exact_matches_vs_observed: int
    match_rate_vs_observed: float
    mean_signed_ordinal_diff: float
    mean_absolute_ordinal_diff: float
    ordinal_diff_distribution: Dict[int, int]
    category_shift_count_vs_b0: int
    shift_rate_vs_b0: float


@dataclass
class BaselineSummary:
    baseline_name: str
    total: BaselineMetricGroup
    nvd: BaselineMetricGroup
    synthetic: BaselineMetricGroup


@dataclass
class AblationExperimentReport:
    generated_at_utc: str
    canonical_expected: int
    canonical_found: int
    total_scenarios: int
    nvd_scenarios: int
    synthetic_scenarios: int
    nominal_vs_observed_divergence_count: int
    nominal_vs_observed_divergent_ids: List[str]
    baseline_summaries: Dict[str, Dict[str, Any]]
    scenario_results: List[Dict[str, Any]]
    methodological_note: str = (
        "All metrics are deterministic descriptive statistics computed over the N=30 canonical "
        "benchmark corpus. No inferential population claims, p-values, confidence intervals, "
        "or IID assumptions are asserted."
    )


# ==============================================================================
# Pure Functions: Extraction and Computation
# ==============================================================================

def extract_candidate_requirements(cr_text: str, ir_text: str, ar_text: str) -> Dict[str, str]:
    """Extracts candidate metric ratings (H, M, L, or X) from requirement strings."""
    candidates = {}
    for prefix, raw_val in [("CR", cr_text), ("IR", ir_text), ("AR", ar_text)]:
        s = str(raw_val or "").strip()
        m = re.search(rf"\b{prefix}:([HMLX])\b", s, re.IGNORECASE)
        if m:
            candidates[prefix] = m.group(1).upper()
        else:
            candidates[prefix] = "X"
    return candidates


def compute_b1_environmental_score(
    base_vector: str,
    candidates: Mapping[str, str],
) -> Tuple[float, str, str]:
    """
    Computes CVSS-BE Environmental score and mapped priority category.
    Returns (score_env, severity_env, priority_b1).
    """
    try:
        env_vector = cvss40.apply_candidates(base_vector, candidates)
        res = cvss40.score(env_vector)
        score_val = float(res.get("score", 0.0))
        sev_val = str(res.get("severity", "None")).strip().upper()
        p_b1 = policy.recompute_p_base(sev_val)
        return score_val, sev_val, p_b1
    except Exception:
        # Fallback to zero score if parsing fails
        return 0.0, "NONE", "defer"


def evaluate_scenario_ablation(row: Dict[str, str]) -> ScenarioAblationResult:
    """Evaluates all baselines B0-B4 for a single scenario row."""
    sid = row.get("scenario_id", "").strip()
    cve_id = row.get("cve_id", "").strip()
    source_type = "NVD" if sid.startswith("SCN-NVD-") else "SYNTHETIC"

    raw_base_score = float(row.get("cvss_b_score", "0.0"))
    b_sev = str(row.get("cvss_b_severity", "NONE")).strip().upper()
    p_base = policy.recompute_p_base(b_sev)

    # Asset class & nominal weights
    asset_class = row.get("asset_class", "").strip()
    w_ctx, w_ctrl = policy.lookup_nominal_weights(asset_class)

    # B0: Base Severity Only
    b0 = p_base

    # B1: Environmental Score Only (CVSS-BE)
    candidates = extract_candidate_requirements(
        row.get("confidentiality_requirement", ""),
        row.get("integrity_requirement", ""),
        row.get("availability_requirement", ""),
    )
    vec = row.get("official_cvss_v4_vector", "")
    s_env, sev_env, b1 = compute_b1_environmental_score(vec, candidates)

    # B2: Context-Only Policy (w_control = 0)
    ord_base = policy.priority_to_ordinal(p_base)
    ord_b2 = max(0, min(4, ord_base + w_ctx))
    b2 = policy.ordinal_to_priority(ord_b2)

    # B3: Controls-Only Policy (w_context = 0)
    ord_b3 = max(0, min(4, ord_base + w_ctrl))
    b3 = policy.ordinal_to_priority(ord_b3)

    # B4_nominal: Full Nominal Policy
    b4_nominal, _ = policy.recompute_p_env_nominal(p_base, asset_class)

    # B4_observed: Stored Operational Priority in benchmark
    b4_observed = row.get("environmental_priority", "").strip().lower()

    # Detect divergence / curated override
    curated_override = (b4_nominal != b4_observed)

    # Differences vs B4_observed
    ord_observed = policy.priority_to_ordinal(b4_observed)
    diffs_vs_observed = {
        "B0": policy.priority_to_ordinal(b0) - ord_observed,
        "B1": policy.priority_to_ordinal(b1) - ord_observed,
        "B2": ord_b2 - ord_observed,
        "B3": ord_b3 - ord_observed,
        "B4_nominal": policy.priority_to_ordinal(b4_nominal) - ord_observed,
        "B4_observed": 0,
    }

    # Shifts vs B0
    shifts_vs_b0 = {
        "B1": policy.priority_to_ordinal(b1) - ord_base,
        "B2": ord_b2 - ord_base,
        "B3": ord_b3 - ord_base,
        "B4_nominal": policy.priority_to_ordinal(b4_nominal) - ord_base,
        "B4_observed": ord_observed - ord_base,
    }

    return ScenarioAblationResult(
        scenario_id=sid,
        source_type=source_type,
        cve_id=cve_id,
        s_base=raw_base_score,
        p_base=p_base,
        s_env=s_env,
        p_b1=b1,
        environment_profile=asset_class,
        w_context=w_ctx,
        w_control=w_ctrl,
        b0=b0,
        b1=b1,
        b2=b2,
        b3=b3,
        b4_nominal=b4_nominal,
        b4_observed=b4_observed,
        curated_override=curated_override,
        ordinal_differences_vs_observed=diffs_vs_observed,
        category_shifts_vs_b0=shifts_vs_b0,
    )


def load_canonical_scenarios(csv_path: Path) -> List[Dict[str, str]]:
    """Loads authoritative scenarios from canonical reference CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Canonical scenarios CSV not found: {csv_path}")

    rows: List[Dict[str, str]] = []
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row.get("scenario_id", "").strip()
            if sid:
                rows.append(row)
    return rows


def compute_metric_group(
    results: List[ScenarioAblationResult],
    baseline_key: str,
) -> BaselineMetricGroup:
    """Computes descriptive summary statistics for a given baseline over a scenario subset."""
    n = len(results)
    if n == 0:
        return BaselineMetricGroup(
            exact_matches_vs_observed=0,
            match_rate_vs_observed=0.0,
            mean_signed_ordinal_diff=0.0,
            mean_absolute_ordinal_diff=0.0,
            ordinal_diff_distribution={},
            category_shift_count_vs_b0=0,
            shift_rate_vs_b0=0.0,
        )

    matches = 0
    signed_diffs: List[int] = []
    abs_diffs: List[int] = []
    dist: Dict[int, int] = {}
    shift_count = 0

    for r in results:
        # Match vs observed
        diff = r.ordinal_differences_vs_observed.get(baseline_key, 0)
        signed_diffs.append(diff)
        abs_diffs.append(abs(diff))
        dist[diff] = dist.get(diff, 0) + 1

        if diff == 0:
            matches += 1

        # Shift vs B0
        shift = r.category_shifts_vs_b0.get(baseline_key, 0)
        if shift != 0:
            shift_count += 1

    return BaselineMetricGroup(
        exact_matches_vs_observed=matches,
        match_rate_vs_observed=round(matches / n, 4),
        mean_signed_ordinal_diff=round(sum(signed_diffs) / n, 4),
        mean_absolute_ordinal_diff=round(sum(abs_diffs) / n, 4),
        ordinal_diff_distribution={k: dist[k] for k in sorted(dist.keys())},
        category_shift_count_vs_b0=shift_count,
        shift_rate_vs_b0=round(shift_count / n, 4),
    )


def aggregate_ablation_metrics(
    results: List[ScenarioAblationResult],
    canonical_expected: int = 30,
) -> AblationExperimentReport:
    """Aggregates all baseline metrics across total, NVD, and synthetic partitions."""
    nvd_results = [r for r in results if r.source_type == "NVD"]
    syn_results = [r for r in results if r.source_type == "SYNTHETIC"]

    divergent = [r.scenario_id for r in results if r.curated_override]

    baselines = ["B0", "B1", "B2", "B3", "B4_nominal", "B4_observed"]
    summaries: Dict[str, Dict[str, Any]] = {}

    for b in baselines:
        summary_obj = BaselineSummary(
            baseline_name=b,
            total=compute_metric_group(results, b),
            nvd=compute_metric_group(nvd_results, b),
            synthetic=compute_metric_group(syn_results, b),
        )
        summaries[b] = asdict(summary_obj)

    return AblationExperimentReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        canonical_expected=canonical_expected,
        canonical_found=len(results),
        total_scenarios=len(results),
        nvd_scenarios=len(nvd_results),
        synthetic_scenarios=len(syn_results),
        nominal_vs_observed_divergence_count=len(divergent),
        nominal_vs_observed_divergent_ids=sorted(divergent),
        baseline_summaries=summaries,
        scenario_results=[asdict(r) for r in results],
    )


def run_ablation_study(
    csv_path: Optional[Path] = None,
) -> AblationExperimentReport:
    """Executes the full deterministic ablation study over canonical scenarios."""
    if csv_path is None:
        repo_root = Path(__file__).resolve().parent.parent
        csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"

    rows = load_canonical_scenarios(csv_path)
    results = [evaluate_scenario_ablation(row) for row in rows]
    return aggregate_ablation_metrics(results, canonical_expected=len(rows))


def export_scenarios_csv(
    report: AblationExperimentReport,
    output_path: Path,
) -> None:
    """Exports per-scenario ablation results to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "scenario_id",
        "source_type",
        "cve_id",
        "s_base",
        "p_base",
        "s_env",
        "p_b1",
        "environment_profile",
        "w_context",
        "w_control",
        "b0",
        "b1",
        "b2",
        "b3",
        "b4_nominal",
        "b4_observed",
        "curated_override",
        "diff_b0_vs_observed",
        "diff_b1_vs_observed",
        "diff_b2_vs_observed",
        "diff_b3_vs_observed",
        "diff_b4_nominal_vs_observed",
        "shift_b1_vs_b0",
        "shift_b2_vs_b0",
        "shift_b3_vs_b0",
        "shift_b4_nominal_vs_b0",
        "shift_b4_observed_vs_b0",
    ]
    with open(output_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in report.scenario_results:
            diffs = s.get("ordinal_differences_vs_observed", {})
            shifts = s.get("category_shifts_vs_b0", {})
            row = {
                "scenario_id": s.get("scenario_id"),
                "source_type": s.get("source_type"),
                "cve_id": s.get("cve_id"),
                "s_base": s.get("s_base"),
                "p_base": s.get("p_base"),
                "s_env": s.get("s_env"),
                "p_b1": s.get("p_b1"),
                "environment_profile": s.get("environment_profile"),
                "w_context": s.get("w_context"),
                "w_control": s.get("w_control"),
                "b0": s.get("b0"),
                "b1": s.get("b1"),
                "b2": s.get("b2"),
                "b3": s.get("b3"),
                "b4_nominal": s.get("b4_nominal"),
                "b4_observed": s.get("b4_observed"),
                "curated_override": s.get("curated_override"),
                "diff_b0_vs_observed": diffs.get("B0", 0),
                "diff_b1_vs_observed": diffs.get("B1", 0),
                "diff_b2_vs_observed": diffs.get("B2", 0),
                "diff_b3_vs_observed": diffs.get("B3", 0),
                "diff_b4_nominal_vs_observed": diffs.get("B4_nominal", 0),
                "shift_b1_vs_b0": shifts.get("B1", 0),
                "shift_b2_vs_b0": shifts.get("B2", 0),
                "shift_b3_vs_b0": shifts.get("B3", 0),
                "shift_b4_nominal_vs_b0": shifts.get("B4_nominal", 0),
                "shift_b4_observed_vs_b0": shifts.get("B4_observed", 0),
            }
            writer.writerow(row)
    print(f"Wrote scenario CSV to {output_path}")


def format_human_ablation_summary(report: AblationExperimentReport) -> str:
    """Formats ablation summary report into console-readable representation."""
    lines = [
        "=" * 78,
        "CVSS v4.0 ABLATION AND BASELINE EXPERIMENT (B0-B4 EVALUATION)",
        "=" * 78,
        f"Generated at UTC   : {report.generated_at_utc}",
        f"Canonical Scope    : {report.canonical_found} / {report.canonical_expected} scenarios evaluated",
        f"Partitions         : Total={report.total_scenarios}, NVD={report.nvd_scenarios}, Synthetic={report.synthetic_scenarios}",
        f"Divergence Count   : {report.nominal_vs_observed_divergence_count} curated overrides ({', '.join(report.nominal_vs_observed_divergent_ids)})",
        "-" * 78,
        f"{'Baseline':<14} {'Exact Match (Tot)':<18} {'Mean |Diff|':<14} {'Shift vs B0':<14}",
        "-" * 78,
    ]
    for b_name, summ in report.baseline_summaries.items():
        tot = summ["total"]
        match_str = f"{tot['exact_matches_vs_observed']}/{report.total_scenarios} ({tot['match_rate_vs_observed']*100:.1f}%)"
        diff_str = f"{tot['mean_absolute_ordinal_diff']:.3f}"
        shift_str = f"{tot['category_shift_count_vs_b0']}/{report.total_scenarios} ({tot['shift_rate_vs_b0']*100:.1f}%)"
        lines.append(f"{b_name:<14} {match_str:<18} {diff_str:<14} {shift_str:<14}")
    lines.append("=" * 78)
    return "\n".join(lines)


# ==============================================================================
# CLI Entrypoint (Import Safe)
# ==============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run CVSS v4.0 environmental ablation study across baselines B0-B4."
    )
    repo_root = Path(__file__).resolve().parent.parent
    parser.add_argument(
        "--dataset-csv",
        type=Path,
        default=repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv",
        help="Path to canonical reference CSV",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Optional path to output structured JSON report",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=None,
        help="Optional path to output per-scenario CSV report",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress human-readable stdout summary",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_ablation_study(args.dataset_csv)

    if not args.quiet:
        print(format_human_ablation_summary(report))

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_json, mode="w", encoding="utf-8") as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        print(f"Wrote ablation report to {args.output_json}")

    if args.output_csv:
        export_scenarios_csv(report, args.output_csv)

    return 0


if __name__ == "__main__":
    sys.exit(main())
