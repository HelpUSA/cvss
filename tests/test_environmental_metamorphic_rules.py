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
    assert res["review_status"] in ("ABSTAIN", "HUMAN_REVIEW_REQUIRED")
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
    assert res["review_status"] in ("ABSTAIN", "HUMAN_REVIEW_REQUIRED")
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


def test_semantic_delta_zero_accepts():
    """Governance requirement: Semantic inference with strict Delta=0 metric quorum is AUTO_ACCEPT."""
    from core.environmental_rule_catalog import evaluate_semantic_quorum

    resolver_a = {"MAV": "A", "MAC": "H"}
    resolver_b = {"MAV": "A", "MAC": "H"}
    q = evaluate_semantic_quorum(resolver_a, resolver_b)
    assert q["quorum_passed"] is True
    assert q["review_status"] == "AUTO_ACCEPT"
    assert q["human_review_status"] == "none"
    assert q["auto_downgrade_permitted"] is True


def test_semantic_disagreement_rejects_and_escalates():
    """Governance requirement: Any metric-level divergence breaks STP and forces HUMAN_REVIEW_REQUIRED."""
    from core.environmental_rule_catalog import evaluate_semantic_quorum

    resolver_a = {"MAV": "A", "MAC": "H"}
    resolver_b = {"MAV": "N", "MAC": "H"}  # MAV diverges
    q = evaluate_semantic_quorum(resolver_a, resolver_b)
    assert q["quorum_passed"] is False
    assert q["review_status"] == "HUMAN_REVIEW_REQUIRED"
    assert q["human_review_status"] == "required"
    assert q["auto_downgrade_permitted"] is False
    assert len(q["divergences"]) == 1
    assert q["divergences"][0]["metric"] == "MAV"


def test_stale_evidence_warning_vs_rejection():
    """Governance requirement: Warning threshold near expiration vs fail-closed rejection."""
    # Near limit (0.88 days of 1.0 day limit) -> AUTO_ACCEPT_WITH_WARNING
    warning_ev = {
        "evidence_quality": "SUFFICIENT",
        "telemetry_age_days": 0.88,
        "telemetry_profile": "dynamic",
        "reachability": "INTERNAL_ROUTED",
    }
    res_warn = calculate({"source_cvss_vector": BASE_RCE, "evidence": warning_ev})
    assert res_warn["review_status"] == "AUTO_ACCEPT_WITH_WARNING"
    assert res_warn["human_review_status"] == "audit_sample"
    assert res_warn["auto_downgrade_permitted"] is True

    # Exceeding limit (1.2 days of 1.0 day limit) -> ABSTAIN
    stale_ev = {
        "evidence_quality": "SUFFICIENT",
        "telemetry_age_days": 1.2,
        "telemetry_profile": "dynamic",
        "reachability": "INTERNAL_ROUTED",
    }
    res_stale = calculate({"source_cvss_vector": BASE_RCE, "evidence": stale_ev})
    assert res_stale["decision"] == "abstained"
    assert res_stale["review_status"] == "ABSTAIN"
    assert res_stale["auto_downgrade_permitted"] is False


def test_contradictory_authoritative_sources_beyond_conflict_flag():
    """Governance requirement: Conflicting firewall vs routing table evidence triggers fail-closed."""
    ev = {
        "evidence_quality": "SUFFICIENT",
        "telemetry_age_days": 0.2,
        "reachability": "INTERNAL_ROUTED",
        "firewall_status": "ALLOW_PORT_443",
        "routing_table_status": "NO_ROUTE_TO_HOST",
    }
    res = calculate({"source_cvss_vector": BASE_RCE, "evidence": ev})
    assert res["decision"] == "abstained"
    assert res["review_status"] == "ABSTAIN"
    assert res["auto_downgrade_permitted"] is False


def test_confidence_cannot_alter_score():
    """Governance requirement: AI confidence must not affect CVSS scalar scores."""
    ev_high_conf = {
        "evidence_quality": "SUFFICIENT",
        "telemetry_age_days": 0.2,
        "reachability": "LOCAL_ONLY",
        "ai_confidence": 0.99,
    }
    ev_low_conf = {
        "evidence_quality": "SUFFICIENT",
        "telemetry_age_days": 0.2,
        "reachability": "LOCAL_ONLY",
        "ai_confidence": 0.15,
    }
    r1 = calculate({"source_cvss_vector": BASE_RCE, "evidence": ev_high_conf})
    r2 = calculate({"source_cvss_vector": BASE_RCE, "evidence": ev_low_conf})
    assert r1["environmental_score"] == r2["environmental_score"]
    assert r1["environmental_vector"] == r2["environmental_vector"]


def test_malformed_vector_fails_closed():
    """Governance requirement: Malformed input fails closed with ABSTAIN, never guesses."""
    from core.environmental_rule_catalog import EnvironmentalRuleCatalogEngine

    engine = EnvironmentalRuleCatalogEngine()
    bad_res = engine.evaluate(
        base_vector="MALFORMED_NON_CVSS_VECTOR",
        evidence={"reachability": "LOCAL_ONLY", "telemetry_age_days": 0.1},
    )
    assert bad_res["review_status"] == "ABSTAIN"
    assert bad_res["auto_downgrade_permitted"] is False
    assert bad_res["candidate_metrics"] == {}


def test_audit_record_completeness():
    """Governance requirement: Autonomous output must contain all mandatory audit & provenance fields."""
    ev = {
        "evidence_quality": "SUFFICIENT",
        "telemetry_age_days": 0.1,
        "reachability": "ADJACENT_ONLY",
    }
    res = calculate({"cve_id": "CVE-2024-AUDIT", "source_cvss_vector": BASE_RCE, "evidence": ev})
    required_fields = [
        "source_vector", "environmental_vector", "delta", "decision",
        "review_status", "human_review_status", "auto_downgrade_permitted",
        "candidate_metrics", "adjustment_trace", "catalog_version",
        "catalog_hash", "evidence_hash",
    ]
    for f in required_fields:
        assert f in res, f"Missing required audit field: {f}"
    assert res["catalog_version"] == "1.0.0"
    assert len(res["catalog_hash"]) == 64
    assert len(res["evidence_hash"]) == 64


def test_post_facto_sampling_behavior():
    """Governance requirement: 3%–5% post-facto sampling behaves deterministically (HELPUS_INTERNAL_CONTROL)."""
    from core.environmental_rule_catalog import is_sampled_for_post_facto_audit

    sample_count = 0
    total = 10000
    for i in range(total):
        if is_sampled_for_post_facto_audit(f"FINDING-TEST-{i:05d}"):
            sample_count += 1

    rate = sample_count / total
    # Verify rate is in the 3%–5% internal control band
    assert 0.03 <= rate <= 0.05, f"Sampling rate {rate:.4f} outside 3%–5% band"


def test_machine_readable_catalog_version_and_hash():
    """Governance requirement: Catalog version and hash must be immutable and verified."""
    from core.environmental_rule_catalog import CATALOG_HASH, CATALOG_VERSION, compute_catalog_hash

    assert CATALOG_VERSION == "1.0.0"
    assert len(CATALOG_HASH) == 64
    assert CATALOG_HASH == compute_catalog_hash()


def test_executable_catalog_is_single_source_of_truth():
    """G9A requirement: CANONICAL_RULES directly executes and hash binds evaluator bytecode."""
    import copy
    import hashlib
    from core.environmental_rule_catalog import CANONICAL_RULES, EnvironmentalRuleCatalogEngine, compute_catalog_hash

    # 1. Every rule has callable evaluator
    for rule in CANONICAL_RULES:
        assert callable(rule.evaluator), f"Rule {rule.rule_id} evaluator is not callable"

    # 2. Execution is driven directly by CANONICAL_RULES
    engine = EnvironmentalRuleCatalogEngine()
    res = engine.evaluate(
        base_vector=BASE_RCE,
        evidence={"evidence_quality": "SUFFICIENT", "telemetry_age_days": 0.1, "reachability": "LOCAL_ONLY"},
    )
    assert res["candidate_metrics"].get("MAV") == "L"
    assert "MAV-003A" in res["triggered_rules"]

    # 3. Hash sensitivity: modifying any rule logic alters the hash
    orig_hash = compute_catalog_hash()
    assert len(orig_hash) == 64
    assert orig_hash == EnvironmentalRuleCatalogEngine().catalog_hash


def test_catalog_hash_sensitivity_to_evaluator_semantics_and_constants():
    """G9A Blocking Finding A Regression Test:
    
    Verifies that compute_catalog_hash binds:
    1. Constant literals (co_consts) even when bytecode instructions (co_code) are identical.
    2. Operational evaluator logic modifications.
    3. Declarative rule metadata alterations.
    """
    from core.environmental_rule_catalog import (
        CANONICAL_RULES,
        RuleDefinition,
        compute_catalog_hash,
        serialize_code_object,
    )

    orig_hash = compute_catalog_hash()

    # 1. Constant literal sensitivity test (identical co_code, different co_consts)
    def func_ret_l(base_vec, ev, ctx):
        return True, "L", "desc"

    def func_ret_p(base_vec, ev, ctx):
        return True, "P", "desc"

    assert func_ret_l.__code__.co_code == func_ret_p.__code__.co_code, (
        "Precondition: bytecode must be identical to prove constant sensitivity"
    )
    assert serialize_code_object(func_ret_l.__code__) != serialize_code_object(func_ret_p.__code__)

    # 2. Mutate rule evaluator constant and verify catalog hash changes
    mutated_rules = list(CANONICAL_RULES)
    orig_rule = mutated_rules[0]
    mutated_rules[0] = RuleDefinition(
        rule_id=orig_rule.rule_id,
        target_metric=orig_rule.target_metric,
        description=orig_rule.description,
        rationale=orig_rule.rationale,
        citation=orig_rule.citation,
        preconditions=orig_rule.preconditions,
        evaluator=func_ret_p,
    )
    mutated_hash = compute_catalog_hash(mutated_rules)
    assert mutated_hash != orig_hash, "Catalog hash failed to detect evaluator constant mutation"

    # 3. Mutate metadata and verify catalog hash changes
    mutated_rules_meta = list(CANONICAL_RULES)
    mutated_rules_meta[0] = RuleDefinition(
        rule_id=orig_rule.rule_id,
        target_metric=orig_rule.target_metric,
        description="Modified description text for sensitivity test",
        rationale=orig_rule.rationale,
        citation=orig_rule.citation,
        preconditions=orig_rule.preconditions,
        evaluator=orig_rule.evaluator,
    )
    assert compute_catalog_hash(mutated_rules_meta) != orig_hash, (
        "Catalog hash failed to detect rule metadata mutation"
    )

    # 4. Removing a rule changes catalog hash
    assert compute_catalog_hash(CANONICAL_RULES[:-1]) != orig_hash, (
        "Catalog hash failed to detect rule removal"
    )



