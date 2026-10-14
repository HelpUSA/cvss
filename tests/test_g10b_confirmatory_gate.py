from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "g10b_confirmatory_gate.py"
SPEC = importlib.util.spec_from_file_location("g10b_confirmatory_gate", MODULE_PATH)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _fixture_bundle(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    data_dir = repo / "data"
    data_dir.mkdir()

    # Synthetic non-confirmatory fixtures only.
    c1 = data_dir / "synthetic_c1.json"
    c2 = data_dir / "synthetic_c2.json"
    c1.write_text('{"synthetic": "c1"}\n', encoding="utf-8")
    c2.write_text('{"synthetic": "c2"}\n', encoding="utf-8")

    protocol = repo / "protocol.md"
    executor = repo / "executor.py"
    lock = repo / "requirements.lock"
    protocol.write_text("synthetic protocol\n", encoding="utf-8")
    executor.write_text("print('synthetic executor')\n", encoding="utf-8")
    lock.write_text("pytest==9.0.3\n", encoding="utf-8")

    seal = {
        "protocol_id": gate.PROTOCOL_ID,
        "frozen_baseline_commit": gate.FROZEN_BASELINE,
        "datasets": {
            "C1": {
                "path": "data/synthetic_c1.json",
                "state": "SEALED",
                "expected_sha256": _sha(c1),
                "expected_size_bytes": c1.stat().st_size,
            },
            "C2": {
                "path": "data/synthetic_c2.json",
                "state": "SEALED",
                "expected_sha256": _sha(c2),
                "expected_size_bytes": c2.stat().st_size,
            },
        },
    }
    seal_path = repo / "seal.json"
    _write_json(seal_path, seal)

    auth = {
        "CONFIRMATORY_RUN_AUTHORIZED": True,
        "authorized_by": "wmsjp",
        "authorized_at_utc": "2026-10-14T16:00:00Z",
        "protocol_id": gate.PROTOCOL_ID,
        "frozen_baseline_commit": gate.FROZEN_BASELINE,
        "protocol_sha256": _sha(protocol),
        "executor_sha256": _sha(executor),
        "dependency_lock_sha256": _sha(lock),
        "c1_expected_sha256": _sha(c1),
        "c2_expected_sha256": _sha(c2),
        "acknowledgement": gate.REQUIRED_ACK,
    }
    auth_path = repo / "authorization.json"
    _write_json(auth_path, auth)

    return repo, c1, c2, protocol, executor, lock, seal_path, auth_path


def test_gate_rejects_non_authorized_record_before_dataset_verification(tmp_path: Path):
    repo, _, _, protocol, executor, lock, seal_path, auth_path = _fixture_bundle(tmp_path)
    auth = json.loads(auth_path.read_text(encoding="utf-8"))
    auth["CONFIRMATORY_RUN_AUTHORIZED"] = False
    _write_json(auth_path, auth)

    with pytest.raises(gate.GateError, match="CONFIRMATORY_RUN_AUTHORIZED"):
        gate.build_preflight_record(
            auth_path=auth_path,
            seal_path=seal_path,
            protocol_path=protocol,
            executor_path=executor,
            dependency_lock_path=lock,
            repo_root=repo,
            verify_datasets=False,
        )


def test_gate_rejects_authorization_binding_mismatch(tmp_path: Path):
    repo, _, _, protocol, executor, lock, seal_path, auth_path = _fixture_bundle(tmp_path)
    auth = json.loads(auth_path.read_text(encoding="utf-8"))
    auth["executor_sha256"] = "0" * 64
    _write_json(auth_path, auth)

    with pytest.raises(gate.GateError, match="executor_sha256"):
        gate.build_preflight_record(
            auth_path=auth_path,
            seal_path=seal_path,
            protocol_path=protocol,
            executor_path=executor,
            dependency_lock_path=lock,
            repo_root=repo,
            verify_datasets=False,
        )


def test_gate_verifies_synthetic_dataset_hashes_only_after_valid_authorization(tmp_path: Path):
    repo, _, _, protocol, executor, lock, seal_path, auth_path = _fixture_bundle(tmp_path)

    record = gate.build_preflight_record(
        auth_path=auth_path,
        seal_path=seal_path,
        protocol_path=protocol,
        executor_path=executor,
        dependency_lock_path=lock,
        repo_root=repo,
        verify_datasets=True,
    )

    assert record["authorization_valid"] is True
    assert record["dataset_integrity_verified"] is True
    assert record["datasets"]["C1"]["sha256"]
    assert record["datasets"]["C2"]["sha256"]


def test_gate_detects_synthetic_dataset_tampering(tmp_path: Path):
    repo, c1, _, protocol, executor, lock, seal_path, auth_path = _fixture_bundle(tmp_path)
    c1.write_text('{"synthetic": "tampered"}\n', encoding="utf-8")

    with pytest.raises(gate.GateError, match="C1 byte-size mismatch|C1 SHA-256 mismatch"):
        gate.build_preflight_record(
            auth_path=auth_path,
            seal_path=seal_path,
            protocol_path=protocol,
            executor_path=executor,
            dependency_lock_path=lock,
            repo_root=repo,
            verify_datasets=True,
        )


def test_seal_manifest_requires_both_registered_hashes(tmp_path: Path):
    repo, _, _, protocol, executor, lock, seal_path, auth_path = _fixture_bundle(tmp_path)
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    seal["datasets"]["C2"]["expected_sha256"] = None
    _write_json(seal_path, seal)

    with pytest.raises(gate.GateError, match="C2 expected_sha256"):
        gate.build_preflight_record(
            auth_path=auth_path,
            seal_path=seal_path,
            protocol_path=protocol,
            executor_path=executor,
            dependency_lock_path=lock,
            repo_root=repo,
            verify_datasets=False,
        )
