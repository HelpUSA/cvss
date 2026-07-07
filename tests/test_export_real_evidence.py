import importlib.util
import json
import tempfile
from pathlib import Path

import pytest


MODULE_PATH = Path.cwd() / "scripts" / "export_real_evidence.py"


def load_module():
    spec = importlib.util.spec_from_file_location("export_real_evidence_for_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")


def test_export_evidence_copies_files_and_writes_manifest():
    module = load_module()
    with tempfile.TemporaryDirectory() as temp:
        temp_path = Path(temp)
        scan = temp_path / "trivy_latest.json"
        assessment = temp_path / "latest_assessment.json"
        dashboard = temp_path / "real_assessment.json"
        report = temp_path / "latest_assessment_report.md"
        out = temp_path / "bundle"

        write_json(scan, {"Metadata": {"ImageID": "local"}})
        write_json(assessment, {"summary": {"finding_count": 0}})
        write_json(dashboard, {"summary": {"finding_count": 0}})
        report.write_text("# Report\n", encoding="utf-8")

        manifest_path = module.export_evidence(out, scan, assessment, dashboard, report)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        assert manifest["schema"] == "helpus.cvss.real_evidence_export"
        assert manifest["finding_count"] == 0
        assert (out / manifest["files"]["scan"]).exists()
        assert (out / manifest["files"]["assessment"]).exists()
        assert (out / manifest["files"]["dashboard_baseline"]).exists()
        assert (out / manifest["files"]["assessment_report"]).exists()


def test_export_evidence_refuses_non_zero_findings_by_default():
    module = load_module()
    with tempfile.TemporaryDirectory() as temp:
        temp_path = Path(temp)
        scan = temp_path / "scan.json"
        assessment = temp_path / "assessment.json"
        dashboard = temp_path / "dashboard.json"
        out = temp_path / "bundle"

        write_json(scan, {})
        write_json(assessment, {"summary": {"finding_count": 1}})
        write_json(dashboard, {"summary": {"finding_count": 1}})

        with pytest.raises(SystemExit, match="non-zero finding"):
            module.export_evidence(out, scan, assessment, dashboard)


def test_export_evidence_allows_non_zero_findings_for_investigation():
    module = load_module()
    with tempfile.TemporaryDirectory() as temp:
        temp_path = Path(temp)
        scan = temp_path / "scan.json"
        assessment = temp_path / "assessment.json"
        dashboard = temp_path / "dashboard.json"
        out = temp_path / "bundle"

        write_json(scan, {})
        write_json(assessment, {"summary": {"finding_count": 2}})
        write_json(dashboard, {"summary": {"finding_count": 2}})

        manifest_path = module.export_evidence(
            out, scan, assessment, dashboard, allow_findings=True
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        assert manifest["finding_count"] == 2


def test_export_evidence_refuses_mismatched_dashboard_count():
    module = load_module()
    with tempfile.TemporaryDirectory() as temp:
        temp_path = Path(temp)
        scan = temp_path / "scan.json"
        assessment = temp_path / "assessment.json"
        dashboard = temp_path / "dashboard.json"
        out = temp_path / "bundle"

        write_json(scan, {})
        write_json(assessment, {"summary": {"finding_count": 0}})
        write_json(dashboard, {"summary": {"finding_count": 1}})

        with pytest.raises(SystemExit, match="finding counts differ"):
            module.export_evidence(out, scan, assessment, dashboard)

def test_export_evidence_refuses_mismatched_assessment_and_dashboard_counts(tmp_path):
    module = load_module()
    scan = tmp_path / "trivy.json"
    assessment = tmp_path / "assessment.json"
    dashboard = tmp_path / "dashboard.json"
    out = tmp_path / "out"

    write_json(scan, {"Results": []})
    write_json(assessment, {"summary": {"finding_count": 0}})
    write_json(dashboard, {"summary": {"finding_count": 1}})

    try:
        module.export_evidence(out, scan, assessment, dashboard)
    except SystemExit as exc:
        assert "finding counts differ" in str(exc)
    else:
        raise AssertionError("expected mismatched finding counts to stop export")

    assert not (out / "manifest.json").exists()


def test_export_evidence_skips_missing_optional_report(tmp_path):
    module = load_module()
    scan = tmp_path / "trivy.json"
    assessment = tmp_path / "assessment.json"
    dashboard = tmp_path / "dashboard.json"
    report = tmp_path / "missing-report.md"
    out = tmp_path / "out"

    write_json(scan, {"Results": []})
    write_json(assessment, {"summary": {"finding_count": 0}})
    write_json(dashboard, {"summary": {"finding_count": 0}})

    manifest_path = module.export_evidence(out, scan, assessment, dashboard, report)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert "assessment_report" not in manifest["files"]
    assert not (out / report.name).exists()

def test_load_json_rejects_non_object_payload(tmp_path):
    module = load_module()
    payload = tmp_path / "payload.json"
    payload.write_text("[]\n", encoding="utf-8")

    try:
        module.load_json(payload)
    except SystemExit as exc:
        assert "expected JSON object" in str(exc)
    else:
        raise AssertionError("expected non-object JSON payload to stop export")


def test_finding_count_requires_integer_value():
    module = load_module()

    try:
        module.finding_count({"summary": {"finding_count": "0"}})
    except SystemExit as exc:
        assert "finding_count must be an integer" in str(exc)
    else:
        raise AssertionError("expected non-integer finding_count to stop export")
