import unittest
from core.ai_evidence_engine import AIEvidenceEngine

BASE = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"


class TestAIEvidenceEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AIEvidenceEngine()

    def good(self, **kwargs):
        e = {
            "evidence_quality": "SUFFICIENT",
            "telemetry_age_days": 0.2,
            "telemetry_profile": "dynamic",
            "reachability": "INTERNAL_ROUTED",
        }
        e.update(kwargs)
        return e

    def test_internal_routed_is_network(self):
        r = self.engine.analyze_scenario(BASE, self.good())
        self.assertEqual(r["candidate_metrics"]["MAV"], "N")
        self.assertEqual(r["review_status"], "AUTO_ACCEPT")
        self.assertTrue(r["auto_downgrade_permitted"])
        self.assertEqual(r["human_review_status"], "none")

    def test_pci_flag_alone_does_not_set_requirements(self):
        r = self.engine.analyze_scenario(BASE, self.good(pci_in_scope=True))
        self.assertNotIn("CR", r["candidate_metrics"])
        self.assertNotIn("IR", r["candidate_metrics"])
        self.assertNotIn("AR", r["candidate_metrics"])

    def test_versioned_policy_can_set_requirements(self):
        r = self.engine.analyze_scenario(
            BASE,
            self.good(
                organization_policy_id="POL-001",
                policy_version="1.0",
                security_requirements={"CR": "H", "IR": "H", "AR": "M"},
            ),
        )
        self.assertEqual(r["candidate_metrics"]["CR"], "H")
        self.assertEqual(r["candidate_metrics"]["IR"], "H")
        self.assertEqual(r["candidate_metrics"]["AR"], "M")

    def test_high_availability_does_not_mean_ar_low(self):
        r = self.engine.analyze_scenario(BASE, self.good(high_availability=True))
        self.assertNotIn("AR", r["candidate_metrics"])

    def test_explicit_modified_availability_impact(self):
        r = self.engine.analyze_scenario(
            BASE,
            self.good(
                organization_policy_id="POL-001",
                policy_version="1.0",
                modified_impacts={"MVA": "L"},
            ),
        )
        self.assertEqual(r["candidate_metrics"]["MVA"], "L")


if __name__ == "__main__":
    unittest.main()
