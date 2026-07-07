import argparse
import importlib.util
import subprocess
from pathlib import Path

MODULE_PATH = Path.cwd() / "scripts" / "validate_real_pipeline.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_real_pipeline_for_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_build_steps_include_default_quality_gate():
    module = load_module()
    args = argparse.Namespace(
        run_scan=False,
        allow_findings=False,
        skip_refresh=False,
        skip_build=False,
    )
    steps = module.build_steps(args)
    assert steps[0][:3] == [module.sys.executable, "-m", "py_compile"]
    assert steps[1] == [module.sys.executable, "scripts/refresh_real_baseline.py"]
    assert [module.sys.executable, "-m", "pytest", "-q"] in steps
    assert [module.node_command(), "--check", "app.js"] in steps
    assert ["git", "diff", "--check"] in steps
    assert steps[-1] == [module.npm_command(), "run", "build", "--prefix", "web"]


def test_build_steps_support_scan_and_investigation_mode():
    module = load_module()
    args = argparse.Namespace(
        run_scan=True,
        allow_findings=True,
        skip_refresh=False,
        skip_build=True,
    )
    steps = module.build_steps(args)
    assert [
        module.sys.executable,
        "scripts/refresh_real_baseline.py",
        "--run-scan",
        "--allow-findings",
    ] in steps
    assert all("build" not in step for step in steps)


def test_build_steps_can_skip_refresh_execution():
    module = load_module()
    args = argparse.Namespace(
        run_scan=True,
        allow_findings=True,
        skip_refresh=True,
        skip_build=True,
    )
    steps = module.build_steps(args)
    refresh_exec_steps = [
        step
        for step in steps
        if step[:2] == [module.sys.executable, "scripts/refresh_real_baseline.py"]
    ]
    assert refresh_exec_steps == []


def test_run_steps_executes_with_repo_root(monkeypatch):
    module = load_module()
    calls = []

    def fake_run(cmd, *args, **kwargs):
        calls.append((cmd, args, kwargs))
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    module.run_steps([["first"], ["second", "arg"]])
    assert calls == [
        (["first"], (), {"cwd": module.ROOT, "check": True}),
        (["second", "arg"], (), {"cwd": module.ROOT, "check": True}),
    ]
