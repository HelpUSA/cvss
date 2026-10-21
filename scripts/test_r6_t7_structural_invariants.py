#!/usr/bin/env python3
"""
Test Suite: Structural Invariants for R6-T7 Preregistration
Tests execution gates, metadata contracts, and firewall invariants WITHOUT reading held-out records.
"""

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
T7_DIR = REPO_ROOT / "validation" / "article" / "r6_t7_heldout"
HELDOUT_DIR = REPO_ROOT / "validation" / "article" / "r6_heldout"
RUNNER_PATH = REPO_ROOT / "scripts" / "run_r6_t7_heldout_experiment.py"


class TestR6T7StructuralInvariants(unittest.TestCase):
    def setUp(self):
        self.contract_path = T7_DIR / "r6_t7_measurement_contract.json"
        self.prereg_path = T7_DIR / "r6_t7_preregistration.md"
        self.change_manifest_path = T7_DIR / "r6_t7_change_manifest.json"
        self.runner_contract_path = T7_DIR / "r6_t7_runner_contract.json"
        self.gate_spec_path = T7_DIR / "r6_t7_authorization_gate_specification.md"
        self.acq_meta_path = HELDOUT_DIR / "acquisition_metadata.json"

    def test_artifacts_existence(self):
        """All mandatory T7 preregistration artifacts must exist."""
        self.assertTrue(self.contract_path.exists(), "Measurement contract must exist")
        self.assertTrue(self.prereg_path.exists(), "Preregistration markdown must exist")
        self.assertTrue(self.change_manifest_path.exists(), "Change manifest must exist")
        self.assertTrue(self.runner_contract_path.exists(), "Runner contract must exist")
        self.assertTrue(self.gate_spec_path.exists(), "Gate specification must exist")
        self.assertTrue(RUNNER_PATH.exists(), "Runner skeleton must exist")

    def test_runner_gate_locked_by_default(self):
        """Runner must exit with code 2 when invoked without authorization."""
        res = subprocess.run(
            [sys.executable, str(RUNNER_PATH)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 2, f"Runner did not exit with code 2 when locked: {res.stderr}")
        self.assertIn("QUARANTINED_LOCKED", res.stderr)

    def test_runner_structural_invariants_flag(self):
        """Runner passes pre-flight checks under structural verify flag."""
        res = subprocess.run(
            [sys.executable, str(RUNNER_PATH), "--verify-structural-invariants-only"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"Pre-flight failed: {res.stderr}")
        self.assertIn("All structural invariants verified", res.stdout)

    def test_measurement_contract_invariants(self):
        """Contract must maintain strict methodological invariants."""
        with open(self.contract_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["experiment_id"], "TEST-SUITE-R6-T7-HELDOUT-TRANSFER")
        self.assertEqual(data["label"], "R6-T7-HELDOUT")
        self.assertEqual(data["rq_id"], "RQ-R6-1")
        self.assertEqual(data["eligible_denominator"], 938)
        self.assertIsNone(data["target_rate"], "target_rate must be null")
        self.assertIsNone(data["expected_rate"], "expected_rate must be null")
        self.assertFalse(data["held_out_accessed"], "held_out_accessed must be false")
        self.assertFalse(data["human_adjudication_completed"], "human_adjudication_completed must be false")
        self.assertFalse(data["eq8_modified"], "eq8_modified must be false")
        self.assertTrue(data["governance_override_downstream"], "governance override must be downstream")
        self.assertFalse(data["information_invention_allowed"], "information invention must be forbidden")
        self.assertIsNone(data["statistical_inference_default"], "statistical inference default must be null")
        self.assertTrue(data["two_pass_determinism_required"], "two pass determinism required")
        self.assertEqual(data["execution_gate"], "QUARANTINED_LOCKED")

    def test_frozen_metadata_consistency(self):
        """Metadata hashes must match pre-registered constants without opening raw records."""
        with open(self.acq_meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.assertEqual(meta["eligible_natural_count"], 938)
        self.assertEqual(meta["raw_candidate_count"], 947)
        self.assertEqual(meta["total_exclusions"], 9)
        self.assertEqual(meta["r5_overlap_count"], 0)
        self.assertTrue(meta["corpus_locked"])
        self.assertFalse(meta["results_available"])

    def test_outcome_taxonomy_completeness(self):
        """Taxonomy must contain all distinct required outcome categories."""
        with open(self.contract_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        taxonomy = set(data["outcome_taxonomy"])
        required = {
            "SCHEMA_V2_VALID_NOMINAL_CALCULABLE",
            "SCHEMA_V2_VALID_GOVERNANCE_OVERRIDE_DOCUMENTED",
            "SCHEMA_V2_STRUCTURAL_INVALIDITY_REJECTED",
            "MISSING_MANDATORY_EVIDENCE_REJECTED",
            "INSUFFICIENT_INFORMATION_UNRESOLVED",
            "EXECUTION_OR_ENVIRONMENT_ERROR",
        }
        self.assertTrue(required.issubset(taxonomy), f"Missing categories: {required - taxonomy}")


if __name__ == "__main__":
    unittest.main()
