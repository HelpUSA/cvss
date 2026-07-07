#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]


def npm_command() -> str:
    return "npm.cmd" if sys.platform.startswith("win") else "npm"


def node_command() -> str:
    return "node.exe" if sys.platform.startswith("win") else "node"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local validation gate for the real CVSS pipeline."
    )
    parser.add_argument(
        "--run-scan",
        action="store_true",
        help="Run a fresh Trivy assessment before refreshing the dashboard baseline.",
    )
    parser.add_argument(
        "--allow-findings",
        action="store_true",
        help="Allow publishing a non-zero finding baseline for investigation.",
    )
    parser.add_argument(
        "--skip-refresh",
        action="store_true",
        help="Skip refreshing web/data/real_assessment.json.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the Next.js production build.",
    )
    return parser.parse_args(argv)


def build_steps(args: argparse.Namespace) -> list[list[str]]:
    steps: list[list[str]] = [
        [
            sys.executable,
            "-m",
            "py_compile",
            "tools/run_real_assessment.py",
            "scripts/refresh_real_baseline.py",
            "scripts/validate_real_pipeline.py",
        ]
    ]

    if not args.skip_refresh:
        refresh = [sys.executable, "scripts/refresh_real_baseline.py"]
        if args.run_scan:
            refresh.append("--run-scan")
        if args.allow_findings:
            refresh.append("--allow-findings")
        steps.append(refresh)

    steps.extend(
        [
            [sys.executable, "-m", "pytest", "-q"],
            [node_command(), "--check", "app.js"],
            ["git", "diff", "--check"],
        ]
    )

    if not args.skip_build:
        steps.append([npm_command(), "run", "build", "--prefix", "web"])

    return steps


def run_steps(steps: Sequence[Sequence[str]]) -> None:
    for step in steps:
        print("VALIDATE_REAL_PIPELINE_STEP", " ".join(step), flush=True)
        subprocess.run(list(step), cwd=ROOT, check=True)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    run_steps(build_steps(args))
    print("REAL_PIPELINE_VALIDATION_OK")


if __name__ == "__main__":
    main()
