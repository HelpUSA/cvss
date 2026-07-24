from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


FIELDS = [
    "finding_id",
    "asset_id",
    "cve",
    "vulnerability_type",
    "base_score",
    "base_severity",
    "base_vector",
    "internet_exposed",
    "network_segmented",
    "pci_in_scope",
    "firewall_restricted",
    "compensating_controls",
    "business_criticality",
    "notes",
]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert an interactive CVSS export into "
            "the curated scenario directory format."
        )
    )

    parser.add_argument(
        "input_json",
        type=Path,
        help="Interactive export JSON file.",
    )

    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("scenarios/from_interactive"),
        help="Destination directory for converted scenarios.",
    )

    return parser.parse_args()


def load_export(path: Path) -> dict[str, Any]:
    payload = json.loads(
        path.read_text(encoding="utf-8")
    )

    if not isinstance(payload, dict):
        raise ValueError(
            "The interactive export must contain a JSON object."
        )

    return payload


def scenario_name_from_export(
    payload: dict[str, Any],
) -> str:
    case_description = payload.get("case_description")

    if not isinstance(case_description, dict):
        case_description = {}

    result = payload.get("result")

    if not isinstance(result, dict):
        result = {}

    scenario = (
        case_description.get("scenario")
        or result.get("scenario")
        or "interactive_scenario"
    )

    return str(scenario).strip() or "interactive_scenario"


def safe_directory_name(value: str) -> str:
    normalized = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        value.strip(),
    )

    normalized = normalized.strip("._")

    return normalized or "interactive_scenario"


def write_case_description(
    path: Path,
    scenario_name: str,
) -> None:
    content = (
        f"# {scenario_name}\n\n"
        "Generated from interactive static MVP export.\n"
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        handle.write(content)


def vulnerability_rows(
    payload: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = payload.get("vulnerabilities") or []

    if not isinstance(rows, list):
        raise ValueError(
            "The vulnerabilities field must contain a JSON array."
        )

    normalized_rows: list[dict[str, Any]] = []

    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(
                "Each vulnerability must be a JSON object. "
                f"Invalid item at position {index}."
            )

        normalized_rows.append(row)

    return normalized_rows


def write_vulnerabilities(
    path: Path,
    rows: list[dict[str, Any]],
) -> None:
    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDS,
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    field: row.get(field, "")
                    for field in FIELDS
                }
            )


def main() -> int:
    arguments = parse_arguments()
    payload = load_export(arguments.input_json)

    scenario_name = scenario_name_from_export(payload)

    output_directory = (
        arguments.out_dir
        / safe_directory_name(scenario_name)
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    write_case_description(
        output_directory / "case_description.md",
        scenario_name,
    )

    write_vulnerabilities(
        output_directory / "vulnerabilities.csv",
        vulnerability_rows(payload),
    )

    print(output_directory.resolve())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
