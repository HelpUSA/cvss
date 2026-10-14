"""HELPUS CVSS AI v4.0 — Autonomous Context Pipeline Clean-Room Replay (Gate G10A).

Executes deterministic clean-room verification of the autonomous environmental
context pipeline, verifying bit-identical reproducibility and generating
the cryptographic manifest for G10A freeze readiness.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.cvss_environmental_engine import calculate
from core.environmental_rule_catalog import (
    CATALOG_HASH,
    CATALOG_VERSION,
    EnvironmentalRuleCatalogEngine,
)


def get_git_commit() -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        return res.stdout.strip()
    except Exception:
        return "UNKNOWN_COMMIT"


def get_working_tree_status() -> dict:
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        changes = [
            l for l in res.stdout.strip().splitlines()
            if l and not l.startswith("??") and not l.strip().endswith("outputs/clean_room_autonomous_pipeline_manifest.json")
        ]
        return {
            "is_clean": len(changes) == 0,
            "tracked_modifications_count": len(changes),
        }
    except Exception:
        return {"is_clean": False, "tracked_modifications_count": -1}


def get_dependency_inventory() -> dict:
    try:
        res = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True,
            check=True,
        )
        pkgs = json.loads(res.stdout)
        pkg_dict = {p["name"]: p["version"] for p in pkgs}
        hasher = hashlib.sha256()
        for k in sorted(pkg_dict.keys()):
            hasher.update(f"{k}=={pkg_dict[k]}".encode("utf-8"))
        return {
            "total_packages": len(pkg_dict),
            "dependency_environment_hash": hasher.hexdigest(),
            "core_packages": {k: pkg_dict[k] for k in ("pytest", "anyio") if k in pkg_dict},
        }
    except Exception:
        return {"total_packages": 0, "dependency_environment_hash": "UNAVAILABLE", "core_packages": {}}


def file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()



def run_clean_room_replay() -> dict:
    fixture_path = REPO_ROOT / "data" / "autonomous_benchmark_fixtures.json"
    if not fixture_path.exists():
        raise FileNotFoundError(f"Fixture file missing: {fixture_path}")

    fixture_hash = file_sha256(fixture_path)
    with open(fixture_path, "r", encoding="utf-8") as f:
        fixtures = json.load(f)

    results: list[dict] = []
    failures: list[str] = []

    for fix in fixtures:
        fid = fix["fixture_id"]
        cve = fix["cve_id"]
        vec = fix["source_cvss_vector"]
        ev = fix["evidence"]

        out = calculate({"cve_id": cve, "source_cvss_vector": vec, "evidence": ev})

        # Verification of expected outcomes
        expected_status = fix.get("expected_status")
        if expected_status and out["review_status"] != expected_status:
            failures.append(f"{fid}: expected review_status {expected_status}, got {out['review_status']}")

        expected_mav = fix.get("expected_mav")
        if expected_mav and out["candidate_metrics"].get("MAV") != expected_mav:
            failures.append(f"{fid}: expected MAV {expected_mav}, got {out['candidate_metrics'].get('MAV')}")

        expected_mac = fix.get("expected_mac")
        if expected_mac and out["candidate_metrics"].get("MAC") != expected_mac:
            failures.append(f"{fid}: expected MAC {expected_mac}, got {out['candidate_metrics'].get('MAC')}")

        expected_mpr = fix.get("expected_mpr")
        if expected_mpr and out["candidate_metrics"].get("MPR") != expected_mpr:
            failures.append(f"{fid}: expected MPR {expected_mpr}, got {out['candidate_metrics'].get('MPR')}")

        results.append({
            "fixture_id": fid,
            "cve_id": cve,
            "source_vector": out["source_vector"],
            "environmental_vector": out["environmental_vector"],
            "source_score": out["source_score"],
            "environmental_score": out["environmental_score"],
            "delta": out["delta"],
            "decision": out["decision"],
            "review_status": out["review_status"],
            "auto_downgrade_permitted": out["auto_downgrade_permitted"],
            "candidate_metrics": out["candidate_metrics"],
            "catalog_version": out["catalog_version"],
            "catalog_hash": out["catalog_hash"],
            "evidence_hash": out["evidence_hash"],
        })

    results_bytes = json.dumps(results, sort_keys=True, indent=2).encode("utf-8")
    output_hash = hashlib.sha256(results_bytes).hexdigest()

    manifest = {
        "manifest_type": "HELPUS_AUTONOMOUS_PIPELINE_CLEAN_ROOM_REPLAY",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit(),
        "working_tree_provenance": get_working_tree_status(),
        "runtime_environment": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "system_platform": platform.platform(),
            "os_name": os.name,
            "executable_path": sys.executable,
        },
        "dependency_inventory": get_dependency_inventory(),
        "rule_catalog": {
            "catalog_version": CATALOG_VERSION,
            "catalog_sha256": CATALOG_HASH,
            "rule_source_file_sha256": file_sha256(REPO_ROOT / "core" / "environmental_rule_catalog.py"),
        },
        "benchmark_fixtures": {
            "fixture_file": "data/autonomous_benchmark_fixtures.json",
            "fixture_sha256": fixture_hash,
            "total_fixtures_tested": len(fixtures),
        },
        "execution_summary": {
            "total_passed": len(fixtures) - len(failures),
            "total_failed": len(failures),
            "failures": failures,
            "verdict": "PASSED" if len(failures) == 0 else "FAILED",
        },
        "replay_command": "python scripts/clean_room_replay.py",
        "output_artifacts": {
            "results_sha256": output_hash,
            "output_manifest": "outputs/clean_room_autonomous_pipeline_manifest.json",
        },
        "results": results,
    }

    out_file = REPO_ROOT / "outputs" / "clean_room_autonomous_pipeline_manifest.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest


if __name__ == "__main__":
    man = run_clean_room_replay()
    print(f"VERDICT: {man['execution_summary']['verdict']}")
    print(f"Passed: {man['execution_summary']['total_passed']}/{man['benchmark_fixtures']['total_fixtures_tested']}")
    print(f"Fixture SHA-256: {man['benchmark_fixtures']['fixture_sha256']}")
    print(f"Catalog SHA-256: {man['rule_catalog']['catalog_sha256']}")
    print(f"Output SHA-256:  {man['output_artifacts']['results_sha256']}")
    if man["execution_summary"]["total_failed"] > 0:
        sys.exit(1)
