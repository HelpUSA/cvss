from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WORKFLOW = Path(".github/workflows/real-pipeline.yml")


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_real_pipeline_workflow_exists():
    assert WORKFLOW.exists()


def test_real_pipeline_workflow_targets_real_world_branch():
    payload = workflow_text()
    assert "push:" in payload
    assert "pull_request:" in payload
    assert payload.count("- real-world-cvss") >= 2


def test_real_pipeline_workflow_installs_dependencies():
    payload = workflow_text()
    assert "python -m pip install --upgrade pip pytest" in payload
    assert "npm ci --prefix web" in payload


def test_real_pipeline_workflow_runs_consolidated_gate_without_fresh_scan():
    payload = workflow_text()
    assert "python scripts/validate_real_pipeline.py" in payload

    # CI should validate the committed baseline only. Fresh Trivy scans are local,
    # evidence-refresh actions before committing.
    assert "--run-scan" not in payload


def test_real_pipeline_workflow_uses_current_setup_actions():
    payload = workflow_text()
    assert "actions/checkout@v4" in payload
    assert "actions/setup-python@v5" in payload
    assert "actions/setup-node@v4" in payload

def test_ci_workflow_does_not_export_local_evidence_bundles():
    workflow = (ROOT  / ".github" / "workflows" / "real-pipeline.yml").read_text(encoding="utf-8")
    assert "--export-evidence" not in workflow
    assert "outputs/evidence" not in workflow
