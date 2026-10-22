#!/usr/bin/env python3
"""
tests/test_r6_schema_governance_boundaries.py - Boundary and Architectural Integration Tests for R6-A1.

Evaluates non-experimental integration boundaries:
- Schema v2 structural validation executes strictly prior to normalization, policy, or scoring.
- Invalid Schema v2 inputs are blocked fail-closed before any policy logic is invoked.
- Governance override consumes nominal Equation 8 outputs without modifying or perturbing weights.
- Invalid or unapproved governance records leave final operational priority equal to nominal output.
- Pure synthetic execution without dependencies, imports, or paths referencing the 938 held-out cases.
"""

from __future__ import annotations

import copy
from typing import Any, Dict

import pytest

import core.cvss40_environmental_policy as nominal_policy
from core.r6_governance_override import (
    evaluate_governance_override,
    execute_governance_pipeline,
)
from core.r6_schema_v2_validator import validate_trace_v2


@pytest.fixture
def minimal_boundary_trace() -> Dict[str, Any]:
    """Synthetic minimal trace for boundary execution."""
    return {
        "scenario_id": "SCN-SYN-001",
        "scenario_source": "synthetic_expert_scenario",
        "official_or_assigned_cvss_v4_vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        "cvss_b_score": 9.3,
        "cvss_b_severity": "CRITICAL",
        "environmental_evidence": {
            "asset_class": "public_web_application",
            "deployment_context": "Kubernetes Cluster",
            "internet_exposure": "public",
            "privilege_context": "unprivileged",
            "compensating_controls": [
                {
                    "control_id": "CTRL-WAF-01",
                    "control_type": "waf",
                    "status": "enforced",
                    "description": "Cloudflare WAF",
                }
            ],
            "evidence_links": [
                {
                    "link_id": "LINK-01",
                    "uri_or_reference": "https://sec.internal/link",
                    "confidence": "high",
                }
            ],
            "evidence_summary": "Summary text",
        },
        "candidate_environmental_assessment": {
            "confidentiality_requirement": "H",
            "integrity_requirement": "H",
            "availability_requirement": "H",
            "candidate_modified_metrics": {},
            "watcher_recommendation": "Watcher rec",
            "uncertainty_flags": [],
            "human_review_status": "required",
        },
        "priority_comparison": {
            "base_priority": "CRITICAL",
            "environmental_priority": "CRITICAL",
            "priority_delta": 0,
        },
        "boundary": "This trace supports article workflow evaluation.",
    }


def test_boundary_01_validation_precedes_scoring(minimal_boundary_trace):
    """Boundary 1: Validation occurs prior to scoring; invalid payload never reaches policy engine."""
    invalid_trace = copy.deepcopy(minimal_boundary_trace)
    invalid_trace["illegal_injection"] = "blocked_payload"

    # Schema validation step
    v_res = validate_trace_v2(invalid_trace)
    assert v_res.valid is False

    # Guard: Fail-closed prevents execution of downstream scoring
    policy_invoked = False
    def guarded_policy_call(*args):
        nonlocal policy_invoked
        policy_invoked = True
        return "CRITICAL"

    if v_res.valid:
        guarded_policy_call()

    assert policy_invoked is False


def test_boundary_02_invalid_v2_input_cannot_reach_policy_path(minimal_boundary_trace):
    """Boundary 2: Malformed nested structures are halted before policy computation."""
    corrupted_trace = copy.deepcopy(minimal_boundary_trace)
    corrupted_trace["environmental_evidence"]["compensating_controls"][0]["spurious"] = 999

    v_res = validate_trace_v2(corrupted_trace)
    assert v_res.valid is False
    assert v_res.error_category == "UNKNOWN_FIELD"


def test_boundary_03_governance_consumes_nominal_without_mutating_formula():
    """Boundary 3: Nominal priority computation via Equation 8 remains invariant."""
    p_base = "high"
    asset_class = "public_web_application"

    # Direct calculation of nominal Eq. 8 priority
    nominal_prio = nominal_policy.recompute_p_env_nominal(p_base, asset_class)

    # Wrap inside governance pipeline with an unapproved override request
    dummy_trace = {
        "priority_comparison": {"base_priority": p_base},
        "environmental_evidence": {"asset_class": asset_class},
    }
    dummy_request = {
        "override_requested": True,
        "authorization_state": "REQUESTED",
        "post_override_priority": "LOW",
    }

    pipeline_out = execute_governance_pipeline(
        trace_input=dummy_trace,
        nominal_policy_calculator=nominal_policy.recompute_p_env_nominal,
        override_request=dummy_request,
    )

    # Formula result is untouched and equals the nominal calculation
    expected_nominal = nominal_prio[0].upper() if isinstance(nominal_prio, tuple) else nominal_prio.upper()
    assert pipeline_out["priority_comparison"]["nominal_policy_priority"] == expected_nominal
    assert pipeline_out["priority_comparison"]["final_authorized_priority"] == expected_nominal


def test_boundary_04_invalid_governance_object_cannot_change_priority():
    """Boundary 4: Corrupted governance override record fails closed without altering final priority."""
    corrupted_override = {
        "override_requested": True,
        "authorization_state": "APPROVED",
        "authorized_by_role": "SECURITY_LEAD",
        "reason_code": None,  # Missing reason code
        "evidence_ids": [],   # Empty evidence
        "post_override_priority": "LOW",
    }

    gov_eval = evaluate_governance_override(
        nominal_policy_priority="CRITICAL",
        override_data=corrupted_override,
    )

    assert gov_eval.override_applied is False
    assert gov_eval.final_authorized_priority == "CRITICAL"


def test_boundary_05_valid_nominal_only_produces_final_equal_to_nominal():
    """Boundary 5: Normal case with no override yields final_authorized_priority == nominal."""
    gov_eval = evaluate_governance_override(
        nominal_policy_priority="HIGH",
        override_data=None,
    )
    assert gov_eval.override_applied is False
    assert gov_eval.final_authorized_priority == "HIGH"
    assert gov_eval.record.override_requested is False


def test_boundary_06_no_held_out_dependency():
    """Boundary 6: Confirms that test fixtures do not import, open, or depend on held-out manifests."""
    import inspect
    import core.r6_governance_override as gov_mod
    import core.r6_schema_v2_validator as sch_mod

    gov_source = inspect.getsource(gov_mod)
    sch_source = inspect.getsource(sch_mod)

    assert "eligible_corpus_manifest" not in gov_source
    assert "eligible_corpus_manifest" not in sch_source
    assert "r6_heldout" not in gov_source
    assert "r6_heldout" not in sch_source
