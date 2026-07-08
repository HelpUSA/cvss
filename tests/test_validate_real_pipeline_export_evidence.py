import argparse
import importlib.util
from pathlib import Path


MODULE_PATH = Path.cwd() / "scripts" / "validate_real_pipeline.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_real_pipeline_for_export_test", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_export_evidence_option_is_available():
    module = load_module()
    args = module.parse_args(["--export-evidence"])
    assert args.export_evidence is True


def test_build_steps_include_export_after_validation_when_requested():
    module = load_module()
    args = argparse.Namespace(
        run_scan=False,
        allow_findings=False,
        skip_refresh=True,
        skip_build=True,
        export_evidence=True,
    )
    steps = module.build_steps(args)
    assert [module.sys.executable, "scripts/export_real_evidence.py"] in steps


def test_build_steps_pass_allow_findings_to_export():
    module = load_module()
    args = argparse.Namespace(
        run_scan=False,
        allow_findings=True,
        skip_refresh=True,
        skip_build=True,
        export_evidence=True,
    )
    steps = module.build_steps(args)
    assert [
        module.sys.executable,
        "scripts/export_real_evidence.py",
        "--allow-findings",
    ] in steps

def test_build_steps_do_not_export_evidence_by_default():
    module = load_module()
    args = argparse.Namespace(
        run_scan=False,
        allow_findings=False,
        skip_refresh=True,
        skip_build=True,
        export_evidence=False,
    )
    steps = module.build_steps(args)
    assert [module.sys.executable, "scripts/export_real_evidence.py"] not in steps
    assert [
        module.sys.executable,
        "scripts/export_real_evidence.py",
        "--allow-findings",
    ] not in steps

def test_export_evidence_step_runs_after_build_when_build_is_enabled():
    module = load_module()
    args = argparse.Namespace(
        run_scan=False,
        allow_findings=False,
        skip_refresh=True,
        skip_build=False,
        export_evidence=True,
    )
    steps = module.build_steps(args)
    build_step = [module.npm_command(), "run", "build", "--prefix", "web"]
    export_step = [module.sys.executable, "scripts/export_real_evidence.py"]
    assert build_step in steps
    assert export_step in steps
    assert steps.index(build_step) < steps.index(export_step)
    assert steps[-1] == export_step

def test_export_evidence_skip_build_gate_exports_after_static_checks():
    import argparse
    import importlib.util
    from pathlib import Path

    module_path = Path.cwd() / "scripts" / "validate_real_pipeline.py"
    spec = importlib.util.spec_from_file_location("validate_real_pipeline_gate_smoke", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    args = argparse.Namespace(
        run_scan=False,
        allow_findings=False,
        skip_refresh=False,
        skip_build=True,
        export_evidence=True,
    )

    steps = [tuple(str(part) for part in step) for step in module.build_steps(args)]

    assert steps[-1][-1].replace("\\", "/").endswith("scripts/export_real_evidence.py")
    assert any(step[:2] == ("git", "diff") and "--check" in step for step in steps)
    assert not any(step and step[0] == "npm" and "build" in step for step in steps)
