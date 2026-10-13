"""Metamorphic and adversarial test suite for HelpUS CVSS AI v4.0 environmental engine.

Validates the 4 core metamorphic relations (MR-1 to MR-4) and adversarial fail-safe
invariants defined in docs/NON_HUMAN_VALIDATION_PROTOCOL.md and CG-20261013-028.
"""
from __future__ import annotations

import copy
import random
from typing import Any, Dict

import pytest

from core.cvss40 import score
from core.cvss_environmental_engine import calculate

BASE_RCE = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
BASE_CHAIN = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"


def test_mr1_monotonicity_of_criticality():
    """MR-1: Increasing asset criticality must never decrease the score."""
    evidence_low = {
        "evidence_quality": "HIGH",
        "telemetry_age_days": 0.1,
        "conflict_flag": False,
        "reachability": "PUBLIC_ROUTED",
        "security_requirements": {"CR": "L", "IR": "L", "AR": "L"},
        "organization_policy_id": "POL-TEST-001",
        "policy_version": "1.0",
    }
    evidence_high = copy.deepcopy(evidence_low)
    evidence_high["security_requirements"] = {"CR": "H", "IR": "H", "AR": "H"}

    res_low = calculate({"source_cvss_vector": BASE_RCE, "evidence": evidence_low})
    res_high = calculate({"source_cvss_vector": BASE_RCE, "evidence": evidence_high})

    assert res_low["decision"] in ("downgraded", "upgraded", "unchanged")
    assert res_high["decision"] in ("downgraded", "upgraded", "unchanged")
    assert res_high["environmental_score"] >= res_low["environmental_score"]


def test_mr2_defense_removal_monotonicity():
    """MR-2: Removing an effective defense must never decrease the score."""
    evidence_defended = {
        "evidence_quality": "HIGH",
        "telemetry_age_days": 0.1,
        "conflict_flag": False,
        "reachability": "ADJACENT_ONLY",
        "organization_policy_id": "POL-TEST-002",
        "policy_version": "1.0",
        "security_requirements": {"CR": "M", "IR": "M", "AR": "M"},
    }
    # Undefended: exposed to public routed Internet
    evidence_undefended = copy.deepcopy(evidence_defended)
    evidence_undefended["reachability"] = "PUBLIC_ROUTED"

    res_defended = calculate({"source_cvss_vector": BASE_RCE, "evidence": evidence_defended})
    res_undefended = calculate({"source_cvss_vector": BASE_RCE, "evidence": evidence_undefended})

    assert res_defended["decision"] in ("downgraded", "upgraded", "unchanged")
    assert res_undefended["decision"] in ("downgraded", "upgraded", "unchanged")
    # Defended has MAV:A; undefended retains MAV:N (Base AV)
    assert res_undefended["environmental_score"] >= res_defended["environmental_score"]


def test_mr3_context_permutation_invariance():
    """MR-3: Permuting the order of input keys/evidence must yield identical results."""
    keys = [
        ("evidence_quality", "HIGH"),
        ("telemetry_age_days", 0.2),
        ("conflict_flag", False),
        ("reachability", "ADJACENT_ONLY"),
        ("organization_policy_id", "POL-TEST-003"),
        ("policy_version", "1.0"),
        ("security_requirements", {"CR": "H", "IR": "H", "AR": "M"}),
    ]

    results = []
    for seed in range(5):
        shuffled = copy.deepcopy(keys)
        random.seed(seed)
        random.shuffle(shuffled)
        evidence_dict = dict(shuffled)

        res = calculate({
            "source_cvss_vector": BASE_RCE,
            "evidence": evidence_dict,
        })
        results.append(res)

    for i in range(1, len(results)):
        assert results[i]["environmental_vector"] == results[0]["environmental_vector"]
        assert results[i]["environmental_score"] == results[0]["environmental_score"]
        assert results[i]["decision"] == results[0]["decision"]


def test_mr4_irrelevant_control_invariance():
    """MR-4: Adding an irrelevant tag/control must not alter calculated metrics."""
    base_evidence = {
        "evidence_quality": "HIGH",
        "telemetry_age_days": 0.1,
        "conflict_flag": False,
        "reachability": "PUBLIC_ROUTED",
        "organization_policy_id": "POL-TEST-004",
        "policy_version": "1.0",
        "security_requirements": {"CR": "H", "IR": "M", "AR": "L"},
    }
    evidence_with_irrelevant = copy.deepcopy(base_evidence)
    evidence_with_irrelevant["unrelated_printer_installed"] = True
    evidence_with_irrelevant["office_location_floor"] = 4
    evidence_with_irrelevant["legacy_backup_software_unrelated"] = "v2.1"

    res_base = calculate({"source_cvss_vector": BASE_RCE, "evidence": base_evidence})
    res_irrelevant = calculate({"source_cvss_vector": BASE_RCE, "evidence": evidence_with_irrelevant})

    assert res_base["environmental_vector"] == res_irrelevant["environmental_vector"]
    assert res_base["environmental_score"] == res_irrelevant["environmental_score"]


def test_adversarial_stale_telemetry_abstains():
    """Adversarial test: Telemetry older than allowed threshold forces abstention."""
    evidence_stale = {
        "evidence_quality": "HIGH",
        "telemetry_age_days": 15.0,  # Stale: > dynamic max age
        "conflict_flag": False,
        "reachability": "l2_broadcast_only",
        "l2_broadcast_only": True,
        "internet_exposed": False,
    }
    res = calculate({"source_cvss_vector": BASE_RCE, "evidence": evidence_stale})
    assert res["decision"] == "abstained"
    assert res["review_status"] == "HUMAN_REVIEW_REQUIRED"
    assert res["auto_downgrade_permitted"] is False
    assert res["environmental_vector"] is None


def test_adversarial_conflict_flag_abstains():
    """Adversarial test: Conflicting reachability evidence forces abstention."""
    evidence_conflict = {
        "evidence_quality": "HIGH",
        "telemetry_age_days": 0.1,
        "conflict_flag": True,  # Telemetry sources conflict
        "reachability": "l2_broadcast_only",
        "l2_broadcast_only": True,
        "internet_exposed": False,
    }
    res = calculate({"source_cvss_vector": BASE_RCE, "evidence": evidence_conflict})
    assert res["decision"] == "abstained"
    assert res["review_status"] == "HUMAN_REVIEW_REQUIRED"
    assert res["auto_downgrade_permitted"] is False


def test_control_present_is_not_metric_change():
    """Formal Invariant: CONTROL_PRESENT != CVSS_MODIFIED_METRIC. WAF presence alone does not imply MAC:H."""
    evidence = {
        "evidence_quality": "HIGH",
        "telemetry_age_days": 0.1,
        "conflict_flag": False,
        "firewall_status": "active",
        "waf_present": True,  # WAF is present but no verified mitigation rule for this CVE
    }
    res = calculate({"source_cvss_vector": BASE_RCE, "evidence": evidence})
    # Must not assert MAC:H simply because WAF is present
    if res["candidate_metrics"]:
        assert res["candidate_metrics"].get("MAC") != "H"
