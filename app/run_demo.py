from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cvss_env_automation.case_loader import load_case
from cvss_env_automation.rule_engine import assess_case
from cvss_env_automation.reporting import write_outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AI Bridge CVSS Environmental demo case.")
    parser.add_argument("--case", required=True, help="Path to case directory.")
    parser.add_argument("--out", required=True, help="Output directory.")
    args = parser.parse_args()

    case = load_case(args.case)
    rows = assess_case(case)
    write_outputs(rows, args.out)

    print(f"Generated {len(rows)} assessments in {args.out}")
    print(f"- {Path(args.out) / 'report.md'}")
    print(f"- {Path(args.out) / 'summary.csv'}")
    print(f"- {Path(args.out) / 'assessments.json'}")
    print(f"- {Path(args.out) / 'audit_trace.jsonl'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
