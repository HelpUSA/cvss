import unittest
from core.ai_evidence_engine import AIEvidenceEngine

BASE = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"


class TestFailSafeAbstention(unittest.TestCase):
    def setUp(self):
        self.engine = AIEvidenceEngine()

    def assert_abstains(self, evidence):
        r = self.engine.analyze_scenario(BASE, evidence)
        self.assertIn(r["review_status"], ("ABSTAIN", "HUMAN_REVIEW_REQUIRED"))
        self.assertFalse(r["auto_downgrade_permitted"])
        self.assertEqual(r["candidate_metrics"], {})

    def test_empty_evidence_abstains(self):
        self.assert_abstains({})

    def test_explicit_insufficient_abstains(self):
        self.assert_abstains({"evidence_quality": "INSUFFICIENT", "telemetry_age_days": 0})

    def test_explicit_conflicting_abstains(self):
        self.assert_abstains({
            "evidence_quality": "CONFLICTING",
            "telemetry_age_days": 0,
            "reachability": "INTERNAL_ROUTED",
        })

    def test_missing_age_abstains(self):
        self.assert_abstains({"evidence_quality": "SUFFICIENT", "reachability": "INTERNAL_ROUTED"})

    def test_dynamic_older_than_one_day_abstains(self):
        self.assert_abstains({
            "evidence_quality": "SUFFICIENT", "reachability": "INTERNAL_ROUTED",
            "telemetry_profile": "dynamic", "telemetry_age_days": 1.1,
        })

    def test_static_older_than_seven_days_abstains(self):
        self.assert_abstains({
            "evidence_quality": "SUFFICIENT", "reachability": "INTERNAL_ROUTED",
            "telemetry_profile": "static", "telemetry_age_days": 7.1,
        })

    def test_conflicting_acl_routes_abstains(self):
        self.assert_abstains({
            "evidence_quality": "SUFFICIENT", "telemetry_age_days": 0,
            "reachability": "INTERNAL_ROUTED", "firewall_status": "ALLOW_PORT_80",
            "routing_table_status": "NO_ROUTE_TO_HOST",
        })


if __name__ == "__main__":
    unittest.main()
