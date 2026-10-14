#!/usr/bin/env python3
"""Fail-closed gatekeeper for HelpUS G10B confirmatory execution.

This module does NOT implement the C1/C2 scorer and does not inspect benchmark
semantics. It only enforces authorization/integrity prerequisites before an
external confirmatory executor may be launched.

C1/C2 must remain sealed until a Master SuperAdmin authorization record and
pre-existing custody seal hashes are present.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

PROTOCOL_ID = "HELPUS-G10B-CONFIRMATORY-RUN-v1.0"
FROZEN_BASELINE = "007fe79a6cd0e843fe6a9f837444720e23a4bcad"
REQUIRED_ACK = (
    "I authorize the one-time blind confirmatory execution of C1 and C2 "
    "under NO_RETUNING_PERMITTED."
)


class GateError(RuntimeError):
    """Raised when a confirmatory-run prerequisite is not satisfied."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GateError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise GateError(f"JSON object required: {path}")
    return data


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_seal_manifest(seal: dict[str, Any]) -> None:
    if seal.get("protocol_id") != PROTOCOL_ID:
        raise GateError("Seal manifest protocol_id mismatch")
    if seal.get("frozen_baseline_commit") != FROZEN_BASELINE:
        raise GateError("Seal manifest frozen baseline mismatch")

    datasets = seal.get("datasets")
    if not isinstance(datasets, dict):
        raise GateError("Seal manifest datasets object missing")

    for name in ("C1", "C2"):
        entry = datasets.get(name)
        if not isinstance(entry, dict):
            raise GateError(f"Seal manifest missing {name}")
        if entry.get("state") != "SEALED":
            raise GateError(f"{name} must be SEALED before authorization")
        expected = str(entry.get("expected_sha256") or "")
        if len(expected) != 64 or any(c not in "0123456789abcdefABCDEF" for c in expected):
            raise GateError(f"{name} expected_sha256 must be a 64-char SHA-256")
        if not entry.get("path"):
            raise GateError(f"{name} path missing")
        size = entry.get("expected_size_bytes")
        if not isinstance(size, int) or size < 0:
            raise GateError(f"{name} expected_size_bytes missing/invalid")


def validate_authorization(
    auth: dict[str, Any],
    seal: dict[str, Any],
    *,
    protocol_sha256: str,
    executor_sha256: str,
    dependency_lock_sha256: str,
) -> None:
    if auth.get("CONFIRMATORY_RUN_AUTHORIZED") is not True:
        raise GateError("CONFIRMATORY_RUN_AUTHORIZED must be true")
    if auth.get("authorized_by") != "wmsjp":
        raise GateError("Authorization must be issued by wmsjp")
    if auth.get("protocol_id") != PROTOCOL_ID:
        raise GateError("Authorization protocol_id mismatch")
    if auth.get("frozen_baseline_commit") != FROZEN_BASELINE:
        raise GateError("Authorization frozen baseline mismatch")
    if auth.get("acknowledgement") != REQUIRED_ACK:
        raise GateError("Authorization acknowledgement mismatch")

    expected_bindings = {
        "protocol_sha256": protocol_sha256,
        "executor_sha256": executor_sha256,
        "dependency_lock_sha256": dependency_lock_sha256,
        "c1_expected_sha256": seal["datasets"]["C1"]["expected_sha256"],
        "c2_expected_sha256": seal["datasets"]["C2"]["expected_sha256"],
    }
    for key, expected in expected_bindings.items():
        if auth.get(key) != expected:
            raise GateError(f"Authorization binding mismatch: {key}")

    if not auth.get("authorized_at_utc"):
        raise GateError("authorized_at_utc is required")


def verify_dataset_integrity(seal: dict[str, Any], repo_root: Path) -> dict[str, dict[str, Any]]:
    """Read bytes only after authorization validation and compare to custody hashes."""
    observed: dict[str, dict[str, Any]] = {}
    for name in ("C1", "C2"):
        entry = seal["datasets"][name]
        path = (repo_root / entry["path"]).resolve()
        try:
            path.relative_to(repo_root.resolve())
        except ValueError as exc:
            raise GateError(f"{name} path escapes repository root") from exc
        if not path.is_file():
            raise GateError(f"{name} dataset file not found")
        size = path.stat().st_size
        if size != entry["expected_size_bytes"]:
            raise GateError(f"{name} byte-size mismatch before parsing")
        digest = sha256_file(path)
        if digest.lower() != entry["expected_sha256"].lower():
            raise GateError(f"{name} SHA-256 mismatch before parsing")
        observed[name] = {"path": str(path), "sha256": digest, "size_bytes": size}
    return observed


def build_preflight_record(
    *,
    auth_path: Path,
    seal_path: Path,
    protocol_path: Path,
    executor_path: Path,
    dependency_lock_path: Path,
    repo_root: Path,
    verify_datasets: bool,
) -> dict[str, Any]:
    seal = _load_json(seal_path)
    validate_seal_manifest(seal)

    protocol_sha = sha256_file(protocol_path)
    executor_sha = sha256_file(executor_path)
    dependency_sha = sha256_file(dependency_lock_path)

    auth = _load_json(auth_path)
    validate_authorization(
        auth,
        seal,
        protocol_sha256=protocol_sha,
        executor_sha256=executor_sha,
        dependency_lock_sha256=dependency_sha,
    )

    record: dict[str, Any] = {
        "protocol_id": PROTOCOL_ID,
        "frozen_baseline_commit": FROZEN_BASELINE,
        "authorization_valid": True,
        "protocol_sha256": protocol_sha,
        "executor_sha256": executor_sha,
        "dependency_lock_sha256": dependency_sha,
        "dataset_integrity_verified": False,
        "datasets": {},
    }

    if verify_datasets:
        record["datasets"] = verify_dataset_integrity(seal, repo_root)
        record["dataset_integrity_verified"] = True

    return record


def main() -> int:
    parser = argparse.ArgumentParser(description="HelpUS G10B confirmatory gatekeeper")
    parser.add_argument("--authorization", type=Path, required=True)
    parser.add_argument("--seal-manifest", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--executor", type=Path, required=True)
    parser.add_argument("--dependency-lock", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--verify-datasets",
        action="store_true",
        help="After valid authorization, read C1/C2 only to verify size/SHA-256.",
    )
    parser.add_argument(
        "--launch",
        action="store_true",
        help="Launch the already-frozen executor after authorized dataset verification.",
    )
    parser.add_argument(
        "executor_args",
        nargs=argparse.REMAINDER,
        help="Arguments passed to the frozen executor after '--'.",
    )
    args = parser.parse_args()

    if args.launch and not args.verify_datasets:
        raise GateError("--launch requires --verify-datasets")

    record = build_preflight_record(
        auth_path=args.authorization,
        seal_path=args.seal_manifest,
        protocol_path=args.protocol,
        executor_path=args.executor,
        dependency_lock_path=args.dependency_lock,
        repo_root=args.repo_root.resolve(),
        verify_datasets=args.verify_datasets,
    )

    print(json.dumps(record, indent=2, sort_keys=True))

    if not args.launch:
        return 0

    if os.environ.get("HELPUS_G10B_NETWORK_ISOLATED") != "1":
        raise GateError(
            "Refusing launch: HELPUS_G10B_NETWORK_ISOLATED=1 attestation missing. "
            "OS/container network isolation must be established externally."
        )
    if os.environ.get("HELPUS_HCAL_DISABLED") != "1":
        raise GateError("Refusing launch: HELPUS_HCAL_DISABLED=1 attestation missing")

    cmd = [sys.executable, str(args.executor)] + list(args.executor_args)
    completed = subprocess.run(cmd, cwd=args.repo_root.resolve(), check=False)
    return int(completed.returncode)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateError as exc:
        print(f"G10B_GATE_REFUSAL: {exc}", file=sys.stderr)
        raise SystemExit(2)
