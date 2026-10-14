import unittest
from core.ai_evidence_engine import AIEvidenceEngine

BASE = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"


class TestTopologyReachability(unittest.TestCase):
    def setUp(self):
        self.engine = AIEvidenceEngine()

    def good(self, reachability, **kwargs):
        e = {"evidence_quality": "SUFFICIENT", "telemetry_age_days": 0.1,
             "telemetry_profile": "dynamic", "reachability": reachability}
        e.update(kwargs)
        return e

    def test_public_routed_network(self):
        self.assertEqual(self.engine.analyze_scenario(BASE, self.good("PUBLIC_ROUTED"))["candidate_metrics"]["MAV"], "N")

    def test_internal_routed_network(self):
        self.assertEqual(self.engine.analyze_scenario(BASE, self.good("INTERNAL_ROUTED"))["candidate_metrics"]["MAV"], "N")

    def test_adjacent_only(self):
        self.assertEqual(self.engine.analyze_scenario(BASE, self.good("ADJACENT_ONLY"))["candidate_metrics"]["MAV"], "A")

    def test_local_only(self):
        self.assertEqual(self.engine.analyze_scenario(BASE, self.good("LOCAL_ONLY"))["candidate_metrics"]["MAV"], "L")

    def test_physical_only(self):
        self.assertEqual(self.engine.analyze_scenario(BASE, self.good("PHYSICAL_ONLY"))["candidate_metrics"]["MAV"], "P")

    def test_firewall_alone_does_not_set_mac(self):
        r = self.engine.analyze_scenario(BASE, self.good("PUBLIC_ROUTED", firewall_active=True))
        self.assertNotIn("MAC", r["candidate_metrics"])

    def test_exploit_specific_precondition_can_set_mac(self):
        r = self.engine.analyze_scenario(BASE, self.good("PUBLIC_ROUTED", evidenced_exploit_preconditions_elevated=True))
        self.assertEqual(r["candidate_metrics"].get("MAC"), "H")

    def test_conflicting_legacy_flags_abstain(self):
        r = self.engine.analyze_scenario(BASE, {
            "evidence_quality": "SUFFICIENT", "telemetry_age_days": 0,
            "routed_ip_access": True, "internet_exposed": False, "l2_broadcast_only": True,
        })
        self.assertIn(r["review_status"], ("ABSTAIN", "HUMAN_REVIEW_REQUIRED"))


if __name__ == "__main__":
    unittest.main()
