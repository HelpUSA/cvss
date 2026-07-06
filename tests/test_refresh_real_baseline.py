import importlib.util
import json
import tempfile
from pathlib import Path

MODULE_PATH = Path.cwd() / "scripts" / "refresh_real_baseline.py"


def load_module():
    spec = importlib.util.spec_from_file_location("refresh_real_baseline_for_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_payload(path, count):
    payload = {
        "schema": "helpus.cvss.real_assessment",
        "schema_version": 1,
        "summary": {
            "finding_count": count,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return payload


def test_copy_baseline_writes_dashboard_json():
    module = load_module()
    with tempfile.TemporaryDirectory() as dirname:
        root = Path(dirname)
        src = root / "latest_assessment.json"
        dst = root / "web" / "data" / "real_assessment.json"
        write_payload(src, 0)
        result = module.copy_baseline(src, dst)
        assert result["summary"]["finding_count"] == 0
        assert json.loads(dst.read_text(encoding="utf-8"))["schema"] == "helpus.cvss.real_assessment"


def test_copy_baseline_refuses_non_zero_findings_by_default():
    module = load_module()
    with tempfile.TemporaryDirectory() as dirname:
        root = Path(dirname)
        src = root / "latest_assessment.json"
        dst = root / "web" / "data" / "real_assessment.json"
        write_payload(src, 1)
        try:
            module.copy_baseline(src, dst)
        except SystemExit as exc:
            assert "finding_count=1" in str(exc)
        else:
            raise AssertionError("copy_baseline should reject non-zero findings")


def test_copy_baseline_can_allow_findings_for_investigation():
    module = load_module()
    with tempfile.TemporaryDirectory() as dirname:
        root = Path(dirname)
        src = root / "latest_assessment.json"
        dst = root / "web" / "data" / "real_assessment.json"
        write_payload(src, 1)
        result = module.copy_baseline(src, dst, allow_findings=True)
        assert result["summary"]["finding_count"] == 1
        assert dst.exists()