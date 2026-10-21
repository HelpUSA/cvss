#!/usr/bin/env python3
"""
tests/test_r6_governance_override_contract.py - T5 Governance Contract Tests for R6-A1.

Derives exclusively from:
- validation/article/r6_governance_override_specification.md
- validation/article/r6_governance_override_contract.json

Evaluates:
- Lifecycle state transitions and fail-closed resolution.
- Invariants INV-G1 through INV-G8.
- Separation of watcher / requester from authorizing authority.
- Preservation of Equation 8 nominal policy priority under all outcomes.
- Complete reconstruction of governance audit trail in trace output.
"""

from __future__ import annotations

import copy
from typing import Any, Dict

import pytest

from core.r6_governance_override import (
    AuthorizationState,
    GovernanceRole,
    ReasonCode,
    evaluate_governance_override,
    execute_governance_pipeline,
    transition_authorization_state,
)


@pytest.fixture
def valid_approved_override() -> Dict[str, Any]:
    """Provides a valid, role-authorized governance override payload."""
    return {
        "override_id": "OVR-2026-0001",
        "case_id": "SCN-SYN-001",
        "nominal_policy_priority": "CRITICAL",
        "pre_override_priority": "CRITICAL",
        "post_override_priority": "MEDIUM",
        "override_requested": True,
        "override_applied": True,
        "authorization_state": "APPROVED",
        "reason_code": "CONTROL_COMPENSATION",
        "reason_text_optional": "Dedicated hardware firewall and strict mTLS enforce isolation.",
        "evidence_ids": ["CTRL-WAF-01", "LINK-01"],
        "authorized_by_role": "SECURITY_LEAD",
        "authorization_timestamp": "2026-10-21T12:00:00Z",
        "review_required": False,
        "trace_link": "validation/article/trace/SCN-SYN-001.json",
        "schema_version": "1.0.0",
    }


# ==============================================================================
# T5 Test Suite: Cases 1 through 18
# ==============================================================================

def test_t5_01_not_requested_cannot_apply():
    """T5.1: If override_requested is False, override cannot be applied; nominal governs."""
    payload = {
        "override_id": "OVR-2026-0002",
        "case_id": "SCN-SYN-001",
        "override_requested": False,
        "authorization_state": "NOT_REQUESTED",
        "post_override_priority": "LOW",
    }
    result = evaluate_governance_override(
        nominal_policy_priority="HIGH",
        override_data=payload,
    )
    assert result.override_applied is False
    assert result.final_authorized_priority == "HIGH"
    assert "GOVERNANCE_OVERRIDE_NOT_REQUESTED" in result.diagnostics


def test_t5_02_requested_without_approved_cannot_apply(valid_approved_override):
    """T5.2: State REQUESTED or REJECTED fails closed to nominal priority."""
    payload = copy.deepcopy(valid_approved_override)
    payload["authorization_state"] = "REQUESTED"

    result = evaluate_governance_override("CRITICAL", payload)
    assert result.override_applied is False
    assert result.final_authorized_priority == "CRITICAL"
    assert result.record.review_required is True
    assert "GOVERNANCE_UNAUTHORIZED_OVERRIDE_REJECTED" in result.diagnostics


def test_t5_03_approved_valid_override_applied(valid_approved_override):
    """T5.3: Formally approved, valid override transitions priority to post_override_priority."""
    result = evaluate_governance_override(
        nominal_policy_priority="CRITICAL",
        override_data=valid_approved_override,
        requester_role="INCIDENT_COMMANDER",  # Distinct from authorized_by_role
    )
    assert result.override_applied is True
    assert result.final_authorized_priority == "MEDIUM"
    assert result.record.post_override_priority == "MEDIUM"
    assert result.record.review_required is False
    assert result.is_valid is True


def test_t5_04_missing_reason_code_fails_closed(valid_approved_override):
    """T5.4: Missing or invalid reason code fails closed to nominal output."""
    payload = copy.deepcopy(valid_approved_override)
    payload["reason_code"] = None

    result = evaluate_governance_override("CRITICAL", payload)
    assert result.override_applied is False
    assert result.final_authorized_priority == "CRITICAL"
    assert result.record.review_required is True
    assert any("INV-G3" in v for v in result.invariant_violations)


def test_t5_05_empty_evidence_ids_fails_closed(valid_approved_override):
    """T5.5: Empty evidence_ids array fails closed to nominal output."""
    payload = copy.deepcopy(valid_approved_override)
    payload["evidence_ids"] = []

    result = evaluate_governance_override("CRITICAL", payload)
    assert result.override_applied is False
    assert result.final_authorized_priority == "CRITICAL"
    assert result.record.review_required is True
    assert any("INV-G3" in v for v in result.invariant_violations)


def test_t5_06_self_authorization_rejected(valid_approved_override):
    """T5.6: Requester role matching authorized_by_role is rejected (no self-authorization)."""
    payload = copy.deepcopy(valid_approved_override)
    payload["authorized_by_role"] = "SECURITY_LEAD"

    result = evaluate_governance_override(
        nominal_policy_priority="CRITICAL",
        override_data=payload,
        requester_role="SECURITY_LEAD",  # Same role -> Self-authorization violation
    )
    assert result.override_applied is False
    assert result.final_authorized_priority == "CRITICAL"
    assert any("INV-G4" in v for v in result.invariant_violations)


def test_t5_07_invalid_authorization_transition_rejected():
    """T5.7: Invalid state jump (NOT_REQUESTED -> APPROVED) is rejected by state machine."""
    valid, err = transition_authorization_state(
        current_state=AuthorizationState.NOT_REQUESTED.value,
        next_state=AuthorizationState.APPROVED.value,
    )
    assert valid is False
    assert "Invalid state transition" in err


def test_t5_08_nominal_policy_priority_always_preserved(valid_approved_override):
    """T5.8: Equation 8 nominal priority is strictly preserved in trace record."""
    payload = copy.deepcopy(valid_approved_override)
    payload["nominal_policy_priority"] = "FORGED_PRIORITY"

    result = evaluate_governance_override(
        nominal_policy_priority="CRITICAL",
        override_data=payload,
    )
    assert result.record.nominal_policy_priority == "CRITICAL"
    assert any("INV-G2" in v for v in result.invariant_violations)


def test_t5_09_pre_override_priority_preserved(valid_approved_override):
    """T5.9: pre_override_priority is explicitly recorded and matches nominal state."""
    result = evaluate_governance_override("HIGH", valid_approved_override)
    assert result.record.pre_override_priority == "HIGH"


def test_t5_10_post_override_priority_traceable(valid_approved_override):
    """T5.10: post_override_priority is explicitly traceable in the output record."""
    result = evaluate_governance_override(
        nominal_policy_priority="CRITICAL",
        override_data=valid_approved_override,
    )
    assert result.record.post_override_priority == "MEDIUM"


def test_t5_11_unauthorized_override_returns_nominal(valid_approved_override):
    """T5.11: An unauthorized or rejected override preserves nominal priority in final output."""
    payload = copy.deepcopy(valid_approved_override)
    payload["authorization_state"] = "REJECTED"

    result = evaluate_governance_override("CRITICAL", payload)
    assert result.final_authorized_priority == "CRITICAL"


def test_t5_12_malformed_override_returns_nominal_plus_review(valid_approved_override):
    """T5.12: Malformed payload missing authorized_by_role leaves nominal intact and sets review_required."""
    payload = copy.deepcopy(valid_approved_override)
    payload["authorized_by_role"] = None

    result = evaluate_governance_override("CRITICAL", payload)
    assert result.final_authorized_priority == "CRITICAL"
    assert result.record.review_required is True


def test_t5_13_watcher_cannot_authorize_itself(valid_approved_override):
    """T5.13: Autonomous watcher or requester role attempting self-authorization is prohibited."""
    payload = copy.deepcopy(valid_approved_override)
    payload["authorized_by_role"] = "SECURITY_LEAD"

    result = evaluate_governance_override(
        nominal_policy_priority="CRITICAL",
        override_data=payload,
        requester_role="SECURITY_LEAD",  # Self-authorization attempt
    )
    assert result.override_applied is False
    assert result.final_authorized_priority == "CRITICAL"
    assert any("INV-G4" in v for v in result.invariant_violations)


def test_t5_14_no_auto_override_path():
    """T5.14: Without explicit override request, no priority deviation occurs."""
    result = evaluate_governance_override("LOW", None)
    assert result.override_applied is False
    assert result.final_authorized_priority == "LOW"


def test_t5_15_reason_codes_match_frozen_spec():
    """T5.15: Reason codes in module match the 6 frozen specification enums exactly."""
    expected_codes = {
        "DOCUMENTED_ENVIRONMENTAL_EXCEPTION",
        "CONTROL_COMPENSATION",
        "ASSET_CRITICALITY_EXCEPTION",
        "EXPOSURE_CONTEXT_EXCEPTION",
        "EVIDENCE_CONFLICT_REQUIRES_REVIEW",
        "OTHER_REQUIRES_DOCUMENTED_JUSTIFICATION",
    }
    actual_codes = {rc.value for rc in ReasonCode}
    assert actual_codes == expected_codes


def test_t5_16_authorization_states_match_frozen_spec():
    """T5.16: Authorization states in module match the 5 frozen specification enums exactly."""
    expected_states = {
        "NOT_REQUESTED",
        "REQUESTED",
        "APPROVED",
        "REJECTED",
        "SUPERSEDED",
    }
    actual_states = {st.value for st in AuthorizationState}
    assert actual_states == expected_states


def test_t5_17_eq8_formula_untouched_by_governance():
    """T5.17: Governance module operates as a pure post-scoring consumer without modifying Eq. 8."""
    dummy_nominal_calc = lambda p_base, asset: "HIGH"
    dummy_trace = {
        "priority_comparison": {"base_priority": "MEDIUM"},
        "environmental_evidence": {"asset_class": "public_web_application"},
    }

    output = execute_governance_pipeline(
        trace_input=dummy_trace,
        nominal_policy_calculator=dummy_nominal_calc,
        override_request=None,
    )
    assert output["priority_comparison"]["nominal_policy_priority"] == "HIGH"
    assert output["priority_comparison"]["final_authorized_priority"] == "HIGH"
    assert output["governance_override"]["override_applied"] is False


def test_t5_18_trace_reconstructs_full_audit_lifecycle(valid_approved_override):
    """T5.18: Pipeline output reconstructs nominal -> request -> reason/evidence -> authorization -> final."""
    dummy_nominal_calc = lambda p_base, asset: "CRITICAL"
    dummy_trace = {
        "priority_comparison": {"base_priority": "HIGH"},
        "environmental_evidence": {"asset_class": "developer_workstation"},
    }

    output = execute_governance_pipeline(
        trace_input=dummy_trace,
        nominal_policy_calculator=dummy_nominal_calc,
        override_request=valid_approved_override,
        requester_role="INCIDENT_COMMANDER",
    )

    prio = output["priority_comparison"]
    gov = output["governance_override"]

    assert prio["nominal_policy_priority"] == "CRITICAL"
    assert prio["final_authorized_priority"] == "MEDIUM"
    assert gov["override_applied"] is True
    assert gov["reason_code"] == "CONTROL_COMPENSATION"
    assert gov["evidence_ids"] == ["CTRL-WAF-01", "LINK-01"]
    assert gov["authorized_by_role"] == "SECURITY_LEAD"
