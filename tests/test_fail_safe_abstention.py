"""Tests for fail-safe abstention behavior in HelpUS AI Evidence Engine.

Ensures that incomplete, stale, or conflicting telemetry produces
HUMAN_REVIEW_REQUIRED and NEVER triggers an automatic score downgrade.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.ai_evidence_engine import AIEvidenceEngine

class TestFailSafeAbstention(unittest.TestCase):
    def setUp(self):
        self.engine = AIEvidenceEngine()

    def test_missing_telemetry_forces_abstention(self):
        """When telemetry is empty or missing, engine must abstain without downgrading."""
        base_vector = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
        sparse_evidence = {
            "reachability": "UNKNOWN",
            "firewall_rules": [],
            "evidence_quality": "INSUFFICIENT"
        }
        res = self.engine.analyze_scenario(base_vector=base_vector, evidence=sparse_evidence)
        self.assertEqual(res["review_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertFalse(res.get("auto_downgrade_permitted", False))

    def test_conflicting_acl_and_routes_forces_abstention(self):
        """Conflicting signals (e.g. firewall permits but routing shows unreachable) must trigger review."""
        base_vector = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
        conflicting_evidence = {
            "firewall_status": "ALLOW_PORT_80",
            "routing_table_status": "NO_ROUTE_TO_HOST",
            "conflict_flag": True
        }
        res = self.engine.analyze_scenario(base_vector=base_vector, evidence=conflicting_evidence)
        self.assertEqual(res["review_status"], "HUMAN_REVIEW_REQUIRED")

    def test_stale_telemetry_rejects_automatic_downgrade(self):
        """Telemetry older than freshness threshold must not allow automatic downgrade."""
        base_vector = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
        stale_evidence = {
            "telemetry_age_days": 45,
            "segmentation": "ISOLATED_VLAN"
        }
        res = self.engine.analyze_scenario(base_vector=base_vector, evidence=stale_evidence)
        self.assertEqual(res["review_status"], "HUMAN_REVIEW_REQUIRED")

if __name__ == "__main__":
    unittest.main()
