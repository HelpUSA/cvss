#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "assessments" / "latest_assessment.json"
DEFAULT_OUTPUT = ROOT / "web" / "data" / "real_assessment.json"
RUNNER = ROOT / "tools" / "run_real_assessment.py"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing assessment file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise SystemExit(f"assessment payload must be an object: {path}")
    return payload


def finding_count(payload: dict[str, Any]) -> int:
    summary = payload.get("summary") or {}
    try:
        return int(summary.get("finding_count") or 0)
    except (TypeError, ValueError) as exc:
        raise SystemExit("summary.finding_count must be numeric") from exc


def validate_baseline(payload: dict[str, Any], allow_findings: bool = False) -> None:
    count = finding_count(payload)
    if count and not allow_findings:
        raise SystemExit(f"refusing to publish non-zero baseline: finding_count={count}")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_baseline(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_OUTPUT, allow_findings: bool = False) -> dict[str, Any]:
    payload = load_json(input_path)
    validate_baseline(payload, allow_findings=allow_findings)
    write_json(output_path, payload)
    return payload


def run_scan(args: argparse.Namespace) -> None:
    cmd = [
        sys.executable,
        str(RUNNER),
        "--scanner",
        "trivy",
        "--target",
        ".",
        "--raw-output",
        str(ROOT / "outputs" / "scans" / "trivy_latest.json"),
        "--output",
        str(DEFAULT_INPUT),
        "--environment",
        args.environment,
        "--internet-exposed",
        args.internet_exposed,
        "--business-criticality",
        args.business_criticality,
        "--data-sensitivity",
        args.data_sensitivity,
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh the web dashboard copy of the latest real Trivy baseline.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--allow-findings", action="store_true")
    parser.add_argument("--run-scan", action="store_true")
    parser.add_argument("--environment", default="development")
    parser.add_argument("--internet-exposed", default="false")
    parser.add_argument("--business-criticality", default="medium")
    parser.add_argument("--data-sensitivity", default="internal")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.run_scan:
        run_scan(args)
    payload = copy_baseline(args.input, args.output, allow_findings=args.allow_findings)
    print(f"REFRESHED_REAL_BASELINE output={args.output} finding_count={finding_count(payload)}")


if __name__ == "__main__":
    main()