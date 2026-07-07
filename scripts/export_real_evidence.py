#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"required evidence file not found: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return value


def finding_count(assessment: dict[str, Any]) -> int:
    summary = assessment.get("summary")
    if not isinstance(summary, dict):
        raise SystemExit("assessment summary is missing or invalid")
    value = summary.get("finding_count", 0)
    if not isinstance(value, int):
        raise SystemExit("assessment summary.finding_count must be an integer")
    return value


def copy_required(source: Path, destination_dir: Path) -> str:
    if not source.exists():
        raise SystemExit(f"required evidence file not found: {source}")
    destination = destination_dir / source.name
    shutil.copy2(source, destination)
    return destination.name


def relative_or_absolute(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def export_evidence(
    output_dir: Path,
    scan_path: Path,
    assessment_path: Path,
    dashboard_path: Path,
    report_path: Path | None = None,
    allow_findings: bool = False,
) -> Path:
    scan_path = scan_path.resolve()
    assessment_path = assessment_path.resolve()
    dashboard_path = dashboard_path.resolve()
    output_dir = output_dir.resolve()

    scan = load_json(scan_path)
    assessment = load_json(assessment_path)
    dashboard = load_json(dashboard_path)

    assessment_count = finding_count(assessment)
    dashboard_count = finding_count(dashboard)

    if assessment_count != dashboard_count:
        raise SystemExit(
            "assessment and dashboard baseline finding counts differ: "
            f"{assessment_count} != {dashboard_count}"
        )

    if assessment_count != 0 and not allow_findings:
        raise SystemExit(
            "refusing to export non-zero finding evidence without --allow-findings"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    files: dict[str, str] = {
        "scan": copy_required(scan_path, output_dir),
        "assessment": copy_required(assessment_path, output_dir),
        "dashboard_baseline": copy_required(dashboard_path, output_dir),
    }

    if report_path is not None and report_path.exists():
        files["assessment_report"] = copy_required(report_path.resolve(), output_dir)

    manifest = {
        "schema": "helpus.cvss.real_evidence_export",
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "finding_count": assessment_count,
        "files": files,
        "source_paths": {
            "scan": relative_or_absolute(scan_path),
            "assessment": relative_or_absolute(assessment_path),
            "dashboard_baseline": relative_or_absolute(dashboard_path),
        },
        "scan_summary": scan.get("Metadata", {}),
        "assessment_summary": assessment.get("summary", {}),
    }

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a reviewable evidence bundle for the real CVSS pipeline."
    )
    parser.add_argument("--output-dir", default="outputs/evidence/latest")
    parser.add_argument("--scan", default="outputs/scans/trivy_latest.json")
    parser.add_argument("--assessment", default="outputs/assessments/latest_assessment.json")
    parser.add_argument("--dashboard", default="web/data/real_assessment.json")
    parser.add_argument("--report", default="outputs/assessments/latest_assessment_report.md")
    parser.add_argument(
        "--allow-findings",
        action="store_true",
        help="Allow exporting non-zero finding evidence for investigation branches.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    manifest = export_evidence(
        output_dir=Path(args.output_dir),
        scan_path=Path(args.scan),
        assessment_path=Path(args.assessment),
        dashboard_path=Path(args.dashboard),
        report_path=Path(args.report),
        allow_findings=args.allow_findings,
    )
    print(f"EXPORTED_REAL_EVIDENCE manifest={manifest}")


if __name__ == "__main__":
    main()
