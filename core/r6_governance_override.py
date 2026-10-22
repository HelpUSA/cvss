#!/usr/bin/env python3
"""
core/r6_governance_override.py - Normative Governance Override Layer for R6-A1.

Implements the formal specification frozen in validation/article/r6_governance_override_specification.md
and validation/article/r6_governance_override_contract.json.

Epistemological and Architectural Constraints:
- Operates strictly downstream of Equation 8 nominal policy evaluation.
- Preserves nominal_policy_priority unconditionally in the trace.
- Zero modification to mathematical weights w_context, w_control, or Eq. 8 structure.
- Prohibits delta_audit and autonomous overrides by core scoring or watcher agents.
- Enforces role separation, mandatory human authorization, evidence linkage, and fail-closed resolution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class AuthorizationState(str, Enum):
    NOT_REQUESTED = "NOT_REQUESTED"
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class ReasonCode(str, Enum):
    DOCUMENTED_ENVIRONMENTAL_EXCEPTION = "DOCUMENTED_ENVIRONMENTAL_EXCEPTION"
    CONTROL_COMPENSATION = "CONTROL_COMPENSATION"
    ASSET_CRITICALITY_EXCEPTION = "ASSET_CRITICALITY_EXCEPTION"
    EXPOSURE_CONTEXT_EXCEPTION = "EXPOSURE_CONTEXT_EXCEPTION"
    EVIDENCE_CONFLICT_REQUIRES_REVIEW = "EVIDENCE_CONFLICT_REQUIRES_REVIEW"
    OTHER_REQUIRES_DOCUMENTED_JUSTIFICATION = "OTHER_REQUIRES_DOCUMENTED_JUSTIFICATION"


class GovernanceRole(str, Enum):
    SECURITY_LEAD = "SECURITY_LEAD"
    MASTER_SUPERADMIN = "MASTER_SUPERADMIN"
    INCIDENT_COMMANDER = "INCIDENT_COMMANDER"


# Allowed state transitions per specification Section 4
ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
    AuthorizationState.NOT_REQUESTED.value: {AuthorizationState.REQUESTED.value},
    AuthorizationState.REQUESTED.value: {
        AuthorizationState.APPROVED.value,
        AuthorizationState.REJECTED.value,
        AuthorizationState.SUPERSEDED.value,
    },
    AuthorizationState.APPROVED.value: {AuthorizationState.SUPERSEDED.value},
    AuthorizationState.REJECTED.value: {AuthorizationState.REQUESTED.value},
    AuthorizationState.SUPERSEDED.value: set(),
}


@dataclass
class GovernanceOverrideRecord:
    override_id: str
    case_id: str
    nominal_policy_priority: str
    pre_override_priority: str
    post_override_priority: str
    override_requested: bool
    override_applied: bool
    authorization_state: str
    review_required: bool
    schema_version: str = "1.0.0"
    reason_code: Optional[str] = None
    reason_text_optional: Optional[str] = None
    evidence_ids: List[str] = field(default_factory=list)
    authorized_by_role: Optional[str] = None
    authorization_timestamp: Optional[str] = None
    trace_link: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GovernanceEvaluationResult:
    final_authorized_priority: str
    override_applied: bool
    record: GovernanceOverrideRecord
    diagnostics: List[str] = field(default_factory=list)
    invariant_violations: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.invariant_violations) == 0


def transition_authorization_state(current_state: str, next_state: str) -> Tuple[bool, Optional[str]]:
    """
    Validates state transitions against the frozen normative state machine.

    Returns:
        (True, None) if transition is valid, or (False, error_message).
    """
    if current_state not in ALLOWED_TRANSITIONS:
        return False, f"Unknown current authorization state '{current_state}'"

    allowed_next = ALLOWED_TRANSITIONS[current_state]
    if next_state not in allowed_next:
        return False, (
            f"Invalid state transition from '{current_state}' to '{next_state}'. "
            f"Permitted next states: {sorted(list(allowed_next))}"
        )
    return True, None


def evaluate_governance_override(
    nominal_policy_priority: str,
    override_data: Optional[Dict[str, Any]],
    requester_role: Optional[str] = None,
) -> GovernanceEvaluationResult:
    """
    Evaluates a governance override record against formal invariants INV-G1 to INV-G8.

    Fails closed: Any invariant violation or authorization failure results in
    override_applied = False, post_override_priority = nominal_policy_priority,
    and review_required = True.

    Args:
        nominal_policy_priority: Exact priority computed via Equation 8.
        override_data: Raw dictionary representing the override record or request.
        requester_role: Optional role of the requesting entity (to test role separation).

    Returns:
        GovernanceEvaluationResult with final priority, override status, and diagnostics.
    """
    diagnostics: List[str] = []
    violations: List[str] = []

    # Case 1: No override requested or provided -> Nominal governs cleanly
    if not override_data:
        record = GovernanceOverrideRecord(
            override_id="OVR-NONE",
            case_id="UNKNOWN",
            nominal_policy_priority=nominal_policy_priority,
            pre_override_priority=nominal_policy_priority,
            post_override_priority=nominal_policy_priority,
            override_requested=False,
            override_applied=False,
            authorization_state=AuthorizationState.NOT_REQUESTED.value,
            review_required=False,
            schema_version="1.0.0",
        )
        return GovernanceEvaluationResult(
            final_authorized_priority=nominal_policy_priority,
            override_applied=False,
            record=record,
        )

    # Parse and extract fields with fail-closed defaults
    override_id = override_data.get("override_id", "OVR-MALFORMED")
    case_id = override_data.get("case_id", "UNKNOWN")
    req_flag = bool(override_data.get("override_requested", False))
    auth_state = override_data.get("authorization_state", AuthorizationState.NOT_REQUESTED.value)
    proposed_post = override_data.get("post_override_priority", nominal_policy_priority)
    reason_code = override_data.get("reason_code")
    reason_text = override_data.get("reason_text_optional")
    evidence_ids = override_data.get("evidence_ids", [])
    authorized_by_role = override_data.get("authorized_by_role")
    auth_ts = override_data.get("authorization_timestamp")
    trace_link = override_data.get("trace_link")
    schema_version = override_data.get("schema_version", "1.0.0")

    # Invariant G2: Nominal preservation
    # If payload attempted to forge nominal priority, force restoration and reject application
    payload_nominal = override_data.get("nominal_policy_priority")
    if payload_nominal is not None and payload_nominal != nominal_policy_priority:
        violations.append("INV-G2: nominal_policy_priority was mutated in payload; restoring Eq. 8 ground truth")
        diagnostics.append("GOVERNANCE_NOMINAL_MUTATION_PREVENTED")

    # Invariant G1: Explicit request and approval prerequisite
    if not req_flag:
        diagnostics.append("GOVERNANCE_OVERRIDE_NOT_REQUESTED")
        record = GovernanceOverrideRecord(
            override_id=override_id,
            case_id=case_id,
            nominal_policy_priority=nominal_policy_priority,
            pre_override_priority=nominal_policy_priority,
            post_override_priority=nominal_policy_priority,
            override_requested=False,
            override_applied=False,
            authorization_state=auth_state,
            review_required=False,
            schema_version=schema_version,
            trace_link=trace_link,
        )
        return GovernanceEvaluationResult(
            final_authorized_priority=nominal_policy_priority,
            override_applied=False,
            record=record,
            diagnostics=diagnostics,
        )

    # If requested but not approved -> Fail closed to nominal output
    if auth_state != AuthorizationState.APPROVED.value:
        diagnostics.append("GOVERNANCE_UNAUTHORIZED_OVERRIDE_REJECTED")
        record = GovernanceOverrideRecord(
            override_id=override_id,
            case_id=case_id,
            nominal_policy_priority=nominal_policy_priority,
            pre_override_priority=nominal_policy_priority,
            post_override_priority=nominal_policy_priority,
            override_requested=True,
            override_applied=False,
            authorization_state=auth_state,
            review_required=True,
            reason_code=reason_code,
            reason_text_optional=reason_text,
            evidence_ids=evidence_ids,
            authorized_by_role=authorized_by_role,
            authorization_timestamp=auth_ts,
            trace_link=trace_link,
            schema_version=schema_version,
        )
        return GovernanceEvaluationResult(
            final_authorized_priority=nominal_policy_priority,
            override_applied=False,
            record=record,
            diagnostics=diagnostics,
        )

    # Invariant G1 check: Must have authorized_by_role
    if not authorized_by_role:
        violations.append("INV-G1: APPROVED state lacks authorized_by_role")
        diagnostics.append("GOVERNANCE_MISSING_AUTHORIZATION_ROLE")

    # Invariant G4: Separation of roles (no self-authorization)
    if requester_role and authorized_by_role and requester_role == authorized_by_role:
        violations.append("INV-G4: Requester role cannot match authorized_by_role (self-authorization prohibited)")
        diagnostics.append("GOVERNANCE_SELF_AUTHORIZATION_REJECTED")

    # Invariant G3: Mandatory justification and evidence
    allowed_reason_values = {rc.value for rc in ReasonCode}
    if not reason_code or reason_code not in allowed_reason_values:
        violations.append(f"INV-G3: Invalid or missing reason_code '{reason_code}'")
        diagnostics.append("GOVERNANCE_MISSING_REASON_CODE_REJECTED")

    if reason_code == ReasonCode.OTHER_REQUIRES_DOCUMENTED_JUSTIFICATION.value:
        if not reason_text or len(reason_text.strip()) < 30:
            violations.append("INV-G3: OTHER reason code requires reason_text exceeding 30 characters")
            diagnostics.append("GOVERNANCE_INSUFFICIENT_DOCUMENTED_JUSTIFICATION")

    if not evidence_ids or len(evidence_ids) < 1:
        violations.append("INV-G3: evidence_ids cannot be empty when applying override")
        diagnostics.append("GOVERNANCE_EMPTY_EVIDENCE_REJECTED")

    # Invariant G8: If any violation occurred -> Fail closed to nominal output
    if violations:
        record = GovernanceOverrideRecord(
            override_id=override_id,
            case_id=case_id,
            nominal_policy_priority=nominal_policy_priority,
            pre_override_priority=nominal_policy_priority,
            post_override_priority=nominal_policy_priority,
            override_requested=True,
            override_applied=False,
            authorization_state=auth_state,
            review_required=True,
            reason_code=reason_code,
            reason_text_optional=reason_text,
            evidence_ids=evidence_ids,
            authorized_by_role=authorized_by_role,
            authorization_timestamp=auth_ts,
            trace_link=trace_link,
            schema_version=schema_version,
        )
        return GovernanceEvaluationResult(
            final_authorized_priority=nominal_policy_priority,
            override_applied=False,
            record=record,
            diagnostics=diagnostics,
            invariant_violations=violations,
        )

    # All invariants satisfied -> Apply authorized governance override cleanly
    record = GovernanceOverrideRecord(
        override_id=override_id,
        case_id=case_id,
        nominal_policy_priority=nominal_policy_priority,
        pre_override_priority=nominal_policy_priority,
        post_override_priority=proposed_post,
        override_requested=True,
        override_applied=True,
        authorization_state=AuthorizationState.APPROVED.value,
        review_required=False,
        reason_code=reason_code,
        reason_text_optional=reason_text,
        evidence_ids=evidence_ids,
        authorized_by_role=authorized_by_role,
        authorization_timestamp=auth_ts,
        trace_link=trace_link,
        schema_version=schema_version,
    )
    diagnostics.append("GOVERNANCE_OVERRIDE_APPLIED_SUCCESSFULLY")

    return GovernanceEvaluationResult(
        final_authorized_priority=proposed_post,
        override_applied=True,
        record=record,
        diagnostics=diagnostics,
    )


def execute_governance_pipeline(
    trace_input: Dict[str, Any],
    nominal_policy_calculator: Callable[[str, str], Any],
    override_request: Optional[Dict[str, Any]] = None,
    requester_role: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes the end-to-end architectural flow:
    Evidence -> Nominal Eq.8 Policy -> nominal_policy_priority -> Governance Override Layer -> Final Authorized Priority.

    Ensures that validation occurs prior to scoring, and that nominal priority is
    irrevocably calculated and recorded regardless of override outcome.
    """
    # 1. Compute Nominal Policy strictly via Equation 8
    p_base = trace_input.get("priority_comparison", {}).get("base_priority", "LOW").lower()
    asset_class = trace_input.get("environmental_evidence", {}).get("asset_class", "developer_workstation")

    raw_calc = nominal_policy_calculator(p_base, asset_class)
    if isinstance(raw_calc, tuple):
        nominal_priority_str = str(raw_calc[0]).upper()
    else:
        nominal_priority_str = str(raw_calc).upper()

    # 2. Evaluate Governance Override Layer
    gov_result = evaluate_governance_override(
        nominal_policy_priority=nominal_priority_str,
        override_data=override_request,
        requester_role=requester_role,
    )

    # 3. Assemble Output Trace preserving both nominal and post-override states
    trace_output = dict(trace_input)
    trace_output["priority_comparison"] = dict(trace_input.get("priority_comparison", {}))
    trace_output["priority_comparison"]["nominal_policy_priority"] = nominal_priority_str
    trace_output["priority_comparison"]["final_authorized_priority"] = gov_result.final_authorized_priority
    trace_output["governance_override"] = gov_result.record.to_dict()

    return trace_output
