from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.cvss_environmental_engine import calculate


DEFAULT_SCENARIOS = ROOT / "scenarios"
DEFAULT_RUNS = ROOT / "outputs" / "runs"
DEFAULT_SUMMARY = (
    ROOT
    / "outputs"
    / "curated_run_summary.csv"
)

COMPARISON_FIELDS = [
    "case_id",
    "run_id",
    "finding_id",
    "asset_id",
    "cve",
    "vulnerability_type",
    "base_score",
    "base_severity",
    "base_vector",
    "environmental_score",
    "environmental_severity",
    "delta",
    "decision",
    "rationale",
    "trace_count",
    "trace_total_adjustment",
    "trace_json",
    "internet_exposed",
    "network_segmented",
    "pci_in_scope",
    "firewall_restricted",
    "compensating_controls",
    "business_criticality",
    "notes",
]

SUMMARY_FIELDS = [
    "case_id",
    "run_id",
    "findings",
    "assessments",
    "downgraded",
    "unchanged",
    "upgraded",
    "mean_delta",
    "source",
]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run all curated CVSS scenarios and generate "
            "comparison and summary CSV files."
        )
    )

    parser.add_argument(
        "--scenarios-dir",
        type=Path,
        default=DEFAULT_SCENARIOS,
        help="Directory containing curated scenario folders.",
    )

    parser.add_argument(
        "--runs-dir",
        type=Path,
        default=DEFAULT_RUNS,
        help="Directory receiving per-scenario run outputs.",
    )

    parser.add_argument(
        "--summary",
        type=Path,
        default=DEFAULT_SUMMARY,
        help="Summary CSV output path.",
    )

    return parser.parse_args()


def read_csv(
    path: Path,
) -> list[dict[str, str]]:
    if not path.exists():
        return []

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fields: list[str],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(rows)


def scenario_directories(
    scenarios_directory: Path,
) -> list[Path]:
    if not scenarios_directory.exists():
        return []

    return sorted(
        path
        for path in scenarios_directory.iterdir()
        if path.is_dir()
        and path.name != "templates"
    )


def process_scenario(
    scenario: Path,
    runs_directory: Path,
) -> dict[str, Any] | None:
    vulnerabilities = read_csv(
        scenario / "vulnerabilities.csv"
    )

    if not vulnerabilities:
        return None

    run_id = scenario.name
    output_directory = runs_directory / run_id

    comparison_rows: list[dict[str, Any]] = []

    for vulnerability in vulnerabilities:
        row: dict[str, Any] = dict(vulnerability)

        calculation = calculate(
            dict(vulnerability)
        )

        trace = calculation.pop(
            "adjustment_trace",
            [],
        )

        row.update(calculation)

        row["trace_json"] = json.dumps(
            trace,
            ensure_ascii=False,
        )

        row["case_id"] = scenario.name
        row["run_id"] = run_id

        comparison_rows.append(row)

    write_csv(
        output_directory
        / "before_after_comparison.csv",
        comparison_rows,
        COMPARISON_FIELDS,
    )

    downgraded = sum(
        1
        for row in comparison_rows
        if row.get("decision") == "downgraded"
    )

    upgraded = sum(
        1
        for row in comparison_rows
        if row.get("decision") == "upgraded"
    )

    unchanged = sum(
        1
        for row in comparison_rows
        if row.get("decision") == "unchanged"
    )

    mean_delta = round(
        sum(
            float(row.get("delta", 0))
            for row in comparison_rows
        )
        / len(comparison_rows),
        3,
    )

    return {
        "case_id": scenario.name,
        "run_id": run_id,
        "findings": len(comparison_rows),
        "assessments": len(comparison_rows),
        "downgraded": downgraded,
        "unchanged": unchanged,
        "upgraded": upgraded,
        "mean_delta": mean_delta,
        "source": "before_after_comparison.csv",
    }


def main() -> int:
    arguments = parse_arguments()

    summaries: list[dict[str, Any]] = []

    for scenario in scenario_directories(
        arguments.scenarios_dir
    ):
        result = process_scenario(
            scenario,
            arguments.runs_dir,
        )

        if result is not None:
            summaries.append(result)

    write_csv(
        arguments.summary,
        summaries,
        SUMMARY_FIELDS,
    )

    print(f"scenarios={len(summaries)}")
    print(f"wrote={arguments.summary.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
