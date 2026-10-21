#!/usr/bin/env python3
"""
HelpUS R6-T7 Held-Out Corpus Transfer Experiment Runner
Suite: TEST-SUITE-R6-T7-HELDOUT-TRANSFER (Label: R6-T7-HELDOUT)
Research Question: RQ-R6-1

FAIL-CLOSED GATE ENFORCEMENT:
By default, this runner operates in state QUARANTINED_LOCKED.
It unconditionally halts before opening any held-out data record unless
explicitly authorized by a dedicated supervisor order.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
HELDOUT_DIR = REPO_ROOT / "validation" / "article" / "r6_heldout"
T7_DIR = REPO_ROOT / "validation" / "article" / "r6_t7_heldout"
ACQUISITION_METADATA_PATH = HELDOUT_DIR / "acquisition_metadata.json"
ELIGIBLE_MANIFEST_PATH = HELDOUT_DIR / "eligible_corpus_manifest.json"
CONTRACT_PATH = T7_DIR / "r6_t7_measurement_contract.json"


def parse_args():
    parser = argparse.ArgumentParser(description="R6-T7 Held-Out Corpus Transfer Experiment Runner")
    parser.add_argument(
        "--authorize-held-out-access",
        action="store_true",
        default=False,
        help="Explicit supervisory authorization flag to unlock held-out data",
    )
    parser.add_argument(
        "--auth-token",
        type=str,
        default="",
        help="Cryptographic authorization token referencing T7 preregistration commit",
    )
    parser.add_argument(
        "--verify-structural-invariants-only",
        action="store_true",
        default=False,
        help="Verify pre-flight structural invariants and exit without opening records",
    )
    return parser.parse_args()


def verify_metadata_invariants() -> bool:
    """Verifies frozen acquisition metadata without accessing any individual records."""
    if not ACQUISITION_METADATA_PATH.exists():
        print(f"[ERROR] Acquisition metadata not found: {ACQUISITION_METADATA_PATH}", file=sys.stderr)
        return False

    with open(ACQUISITION_METADATA_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    if meta.get("eligible_natural_count") != 938:
        print(f"[ERROR] Unexpected eligible count: {meta.get('eligible_natural_count')}", file=sys.stderr)
        return False

    if meta.get("raw_candidate_count") != 947:
        print(f"[ERROR] Unexpected candidate count: {meta.get('raw_candidate_count')}", file=sys.stderr)
        return False

    if meta.get("r5_overlap_count") != 0:
        print(f"[ERROR] Unexpected R5 overlap count: {meta.get('r5_overlap_count')}", file=sys.stderr)
        return False

    if not CONTRACT_PATH.exists():
        print(f"[ERROR] Measurement contract not found: {CONTRACT_PATH}", file=sys.stderr)
        return False

    with open(CONTRACT_PATH, "r", encoding="utf-8") as f:
        contract = json.load(f)

    if contract.get("target_rate") is not None or contract.get("expected_rate") is not None:
        print("[ERROR] target_rate or expected_rate is not null in measurement contract", file=sys.stderr)
        return False

    if contract.get("held_out_accessed") is not False:
        print("[ERROR] held_out_accessed is not false in measurement contract", file=sys.stderr)
        return False

    return True


def main():
    args = parse_args()

    # Step 1: Pre-flight structural invariant check (always allowed, zero record access)
    if not verify_metadata_invariants():
        print("[FAIL-CLOSED] Structural metadata invariants check failed.", file=sys.stderr)
        sys.exit(1)

    if args.verify_structural_invariants_only:
        print("[SUCCESS] All structural invariants verified. Held-out records remain quarantined and untouched.")
        sys.exit(0)

    # Step 2: Fail-Closed Gate Enforcement
    if not args.authorize_held_out_access:
        print(
            "[FAIL-CLOSED] Execution blocked by First Held-Out Access Gate (state: QUARANTINED_LOCKED).\n"
            "Execution requires explicit --authorize-held-out-access flag and a valid --auth-token.",
            file=sys.stderr,
        )
        sys.exit(2)

    if not args.auth_token or len(args.auth_token.strip()) < 8:
        print(
            "[FAIL-CLOSED] Access denied: --auth-token is missing or invalid. "
            "Must provide valid commit/token authorized by supervisor.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Execution requires future order unlocking this branch
    print("[FAIL-CLOSED] Execution authorization acknowledged but runner awaiting complete pipeline activation.", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
