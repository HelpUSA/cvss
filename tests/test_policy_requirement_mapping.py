import unittest
from core.ai_evidence_engine import AIEvidenceEngine

BASE = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"

class TestPolicyRequirementMapping(unittest.TestCase):
    def setUp(self):
        self.engine = AIEvidenceEngine()

    def base_evidence(self, **kwargs):
        e = {
            "evidence_quality": "SUFFICIENT",
            "telemetry_age_days": 0.1,
            "telemetry_profile": "dynamic",
            "reachability": "INTERNAL_ROUTED",
        }
        e.update(kwargs)
        return e

    def test_security_requirements_without_policy_abstain(self):
        r = self.engine.analyze_scenario(BASE, self.base_evidence(security_requirements={"CR": "H"}))
        self.assertEqual(r["review_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertFalse(r["auto_downgrade_permitted"])

    def test_versioned_policy_maps_requirements(self):
        r = self.engine.analyze_scenario(BASE, self.base_evidence(
            organization_policy_id="POL-001", policy_version="1.0",
            security_requirements={"CR": "H", "IR": "M", "AR": "H"},
        ))
        self.assertEqual(r["candidate_metrics"].get("CR"), "H")
        self.assertEqual(r["candidate_metrics"].get("IR"), "M")
        self.assertEqual(r["candidate_metrics"].get("AR"), "H")

    def test_high_availability_flag_does_not_force_ar_low(self):
        r = self.engine.analyze_scenario(BASE, self.base_evidence(high_availability=True))
        self.assertNotIn("AR", r["candidate_metrics"])

    def test_modified_availability_impact_requires_policy(self):
        r = self.engine.analyze_scenario(BASE, self.base_evidence(modified_impacts={"MVA": "L"}))
        self.assertEqual(r["review_status"], "HUMAN_REVIEW_REQUIRED")

if __name__ == "__main__":
    unittest.main()
