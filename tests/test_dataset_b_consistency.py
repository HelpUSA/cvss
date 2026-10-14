"""Test consistency across all Dataset B representations."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_dataset_b_representations_are_identical():
    csv_path = ROOT / "data" / "dataset_b_source_assessments_normalized.csv"
    if not csv_path.exists():
        import pytest
        pytest.skip("dataset_b_source_assessments_normalized.csv not in portable profile")

    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 30, f"Expected 30 rows, got {len(rows)}"

    csv_cves = sorted([r["cve_id"] for r in rows if r["cve_id"]])
    assert len(csv_cves) == 12, "Expected exactly 12 real CVEs"

    # Check 03_DATASET_B_PROVENANCE_SUMMARY.md
    summary_path = ROOT / "03_DATASET_B_PROVENANCE_SUMMARY.md"
    assert summary_path.exists(), "Provenance summary must exist"
    summary_text = summary_path.read_text(encoding="utf-8")
    summary_cves = sorted(set(re.findall(r"CVE-\d{4}-\d+", summary_text)))
    assert csv_cves == summary_cves, f"CSV CVEs {csv_cves} must match summary CVEs {summary_cves}"

    # Check scenarios.json
    scenarios_path = ROOT / "data" / "dataset_b" / "scenarios.json"
    assert scenarios_path.exists(), "scenarios.json must exist"
    with scenarios_path.open(encoding="utf-8") as f:
        scenarios = json.load(f)
    assert len(scenarios) == 30

    # Check source_assessments.json
    assessments_path = ROOT / "data" / "dataset_b" / "source_assessments.json"
    assert assessments_path.exists(), "source_assessments.json must exist"
    with assessments_path.open(encoding="utf-8") as f:
        assessments = json.load(f)
    assert len(assessments) == 30

    # Verify origin flags
    for sc in scenarios:
        if sc["cve_id"]:
            assert sc["origin"] == "CNA_PUBLISHED"
        else:
            assert sc["origin"] == "SYNTHETIC"
