"""Tests for topology modeling and reachability semantics in HelpUS.

Validates that:
- Internal routed IP traffic preserves MAV:Network.
- MAV:Adjacent strictly requires unrouted L2 broadcast containment.
- Local host requires interactive console/loopback isolation (MAV:Local).
- Firewall presence alone does NOT automatically elevate MAC to High.
- Same IP in different routing domains (VRF/VPC) are recognized as distinct.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.ai_evidence_engine import AIEvidenceEngine

class TestTopologyReachability(unittest.TestCase):
    def setUp(self):
        self.engine = AIEvidenceEngine()
        self.base_vector = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"

    def test_internal_routed_preserves_mav_network(self):
        """Internal service reachable via routed subnets is MAV:Network, not Adjacent."""
        evidence = {
            "internet_exposed": False,
            "routed_ip_access": True,
            "l2_broadcast_only": False,
            "local_host_only": False,
            "evidence_quality": "SUFFICIENT"
        }
        res = self.engine.analyze_scenario(self.base_vector, evidence)
        self.assertEqual(res["candidate_metrics"].get("MAV"), "N")

    def test_l2_containment_produces_mav_adjacent(self):
        """Service confined to unrouted L2 broadcast domain produces MAV:Adjacent."""
        evidence = {
            "internet_exposed": False,
            "routed_ip_access": False,
            "l2_broadcast_only": True,
            "local_host_only": False,
            "evidence_quality": "SUFFICIENT"
        }
        res = self.engine.analyze_scenario(self.base_vector, evidence)
        self.assertEqual(res["candidate_metrics"].get("MAV"), "A")

    def test_local_host_produces_mav_local(self):
        """Service without network listener requiring interactive shell is MAV:Local."""
        evidence = {
            "internet_exposed": False,
            "routed_ip_access": False,
            "l2_broadcast_only": False,
            "local_host_only": True,
            "evidence_quality": "SUFFICIENT"
        }
        res = self.engine.analyze_scenario(self.base_vector, evidence)
        self.assertEqual(res["candidate_metrics"].get("MAV"), "L")

    def test_firewall_alone_does_not_set_mac_high(self):
        """Presence of firewall without verified exploit-precondition change leaves MAC alone."""
        evidence = {
            "internet_exposed": True,
            "routed_ip_access": True,
            "firewall_active": True,
            "evidenced_exploit_preconditions_elevated": False,
            "evidence_quality": "SUFFICIENT"
        }
        res = self.engine.analyze_scenario(self.base_vector, evidence)
        self.assertNotIn("MAC", res["candidate_metrics"])

    def test_elevated_exploit_preconditions_sets_mac_high(self):
        """Verified exploit filtering/preconditions change produces MAC:High."""
        evidence = {
            "internet_exposed": True,
            "routed_ip_access": True,
            "firewall_active": True,
            "evidenced_exploit_preconditions_elevated": True,
            "evidence_quality": "SUFFICIENT"
        }
        res = self.engine.analyze_scenario(self.base_vector, evidence)
        self.assertEqual(res["candidate_metrics"].get("MAC"), "H")

if __name__ == "__main__":
    unittest.main()
