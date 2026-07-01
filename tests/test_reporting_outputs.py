import csv
import json
from pathlib import Path

from tempfile import TemporaryDirectory

from app.cvss_env_automation.reporting import write_outputs


def _tmp_path():
    manager = TemporaryDirectory()
    return manager, Path(manager.name)


def test_write_outputs_exports_official_and_contextual_layers():
    manager, out_dir = _tmp_path()
    try:
        rows = [
            {
                "finding_id": "F-001",
                "asset_id": "asset-web-01",
                "cve": "CVE-2099-0001",
                "vulnerability_type": "Remote Code Execution",
                "state": "open",
                "base_score": 9.8,
                "environmental_score": 10.0,
                "environmental_metrics": {"CR": "H", "IR": "H", "AR": "H", "MAV": "N"},
                "matches_expected_requirements": True,
                "official_cvss": {
                    "base_score": 9.8,
                    "base_severity": "Critical",
                },
                "contextual_environmental": {
                    "contextual_score": 10.0,
                    "contextual_severity": "Critical",
                    "decision": "upgraded",
                    "delta_from_official_base": 0.2,
                },
                "evidence": {
                    "source_url": "https://example.test/finding/CVE-2099-0001",
                    "pci_in_scope": True,
                },
            }
        ]

        write_outputs(rows, out_dir)

        assessments = json.loads((out_dir / "assessments.json").read_text(encoding="utf-8"))
        assert assessments[0]["official_cvss"]["base_score"] == 9.8
        assert assessments[0]["contextual_environmental"]["contextual_score"] == 10.0

        summary_rows = list(csv.DictReader((out_dir / "summary.csv").open(encoding="utf-8")))
        summary = summary_rows[0]
        assert summary["official_cvss_base_score"] == "9.8"
        assert summary["official_cvss_base_severity"] == "Critical"
        assert summary["contextual_score"] == "10.0"
        assert summary["contextual_severity"] == "Critical"
        assert summary["contextual_decision"] == "upgraded"
        assert summary["contextual_delta_from_official_base"] == "0.2"

        audit = json.loads((out_dir / "audit_trace.jsonl").read_text(encoding="utf-8").splitlines()[0])
        assert audit["source_url"] == "https://example.test/finding/CVE-2099-0001"
        assert audit["pci_in_scope"] is True

        report = (out_dir / "report.md").read_text(encoding="utf-8")
        assert "Official CVSS Base" in report
        assert "Contextual Score" in report
        assert "must not be labeled as official CVSS" in report
    finally:
        manager.cleanup()


def test_write_outputs_keeps_legacy_rows_compatible():
    manager, out_dir = _tmp_path()
    try:
        rows = [
            {
                "finding_id": "F-legacy",
                "asset_id": "asset-legacy",
                "cve": "CVE-2099-0002",
                "vulnerability_type": "Legacy",
                "state": "open",
                "base_score": 7.5,
                "base_severity": "High",
                "environmental_score": 6.5,
                "environmental_severity": "Medium",
                "environmental_metrics": {},
                "matches_expected_requirements": False,
                "evidence": [],
            }
        ]

        write_outputs(rows, out_dir)

        summary_rows = list(csv.DictReader((out_dir / "summary.csv").open(encoding="utf-8")))
        summary = summary_rows[0]
        assert summary["official_cvss_base_score"] == "7.5"
        assert summary["official_cvss_base_severity"] == "High"
        assert summary["contextual_score"] == "6.5"
        assert summary["contextual_severity"] == "Medium"
    finally:
        manager.cleanup()
