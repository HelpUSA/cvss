#!/usr/bin/env python3
"""Read-only audit: recompute the article dataset's CVSS v4.0 scores.

Compares the score/severity stored in data/article/cvss40_environmental_scenarios.csv
with the official CVSS v4.0 score computed from each row's vector.
The dataset itself is never modified.

Usage:
    python tools/audit_cvss40_dataset_scores.py [--out DIR]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.cvss40 import score  # noqa: E402

DATASET = ROOT / "data" / "article" / "cvss40_environmental_scenarios.csv"


def audit(dataset: Path = DATASET) -> list[dict]:
    rows = []
    with dataset.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            computed = score(row["official_cvss_v4_vector"])
            stored_score = float(row["cvss_b_score"])
            stored_sev = row["cvss_b_severity"].strip().title()
            rows.append({
                "scenario_id": row["scenario_id"],
                "scenario_source": row["scenario_source"],
                "vector": computed["vector"],
                "nomenclature": computed["nomenclature"],
                "stored_score": stored_score,
                "computed_score": computed["score"],
                "stored_severity": stored_sev,
                "computed_severity": computed["severity"],
                "score_matches": stored_score == computed["score"],
                "severity_matches": stored_sev == computed["severity"],
            })
    return rows


def render_markdown(rows: list[dict]) -> str:
    mismatched = [r for r in rows if not r["score_matches"]]
    sev_changed = [r for r in rows if not r["severity_matches"]]
    lines = [
        "# CVSS v4.0 dataset score audit",
        "",
        f"- Dataset: `{DATASET.relative_to(ROOT).as_posix()}` (read-only)",
        f"- Scenarios: {len(rows)}",
        f"- Stored score differs from computed score: {len(mismatched)}",
        f"- Stored severity differs from computed severity: {len(sev_changed)}",
        "",
        "| Scenario | Source | Label | Stored | Computed | Stored sev. | Computed sev. |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        flag = "" if r["score_matches"] else " ⚠"
        lines.append(
            f"| {r['scenario_id']}{flag} | {r['scenario_source']} | {r['nomenclature']} | "
            f"{r['stored_score']} | {r['computed_score']} | {r['stored_severity']} | "
            f"{r['computed_severity']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "outputs" / "cvss40_dataset_audit")
    args = parser.parse_args()

    rows = audit()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "audit.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    (args.out / "audit.md").write_text(render_markdown(rows), encoding="utf-8")

    mismatched = sum(not r["score_matches"] for r in rows)
    print(f"{len(rows)} scenarios audited; {mismatched} stored scores differ from CVSS v4.0.")
    print(f"Report: {args.out / 'audit.md'}")
    return 1 if mismatched else 0


if __name__ == "__main__":
    raise SystemExit(main())
