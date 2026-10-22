#!/usr/bin/env python3
"""
core/r6_schema_v2_validator.py - Normative Closed-World Schema Validator for R6-A1.

Implements the formal specification frozen in validation/article/r6_schema_v2_specification.md
and validation/article/r6_schema_v2_contract.json.

Epistemological and Architectural Constraints:
- Pure module with zero network calls, zero I/O side effects, and fail-closed validation.
- Validates structural conformance prior to evidence normalization, policy computation, or scoring.
- Strictly separates Schema v1 (historical open-world baseline) from Schema v2 (closed-world candidate).
- Rejects undeclared fields on all objects classified as CLOSED_WORLD_REQUIRED.
- Enforces vendor namespacing on OPEN_EXTENSION_POINT_ALLOWED (TraceRoot.extensions).
- Rejects reserved architectural keywords (RESERVED_FOR_FUTURE_VERSION).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class SchemaErrorCategory(str, Enum):
    UNKNOWN_FIELD = "UNKNOWN_FIELD"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_TYPE = "INVALID_TYPE"
    INVALID_ENUM = "INVALID_ENUM"
    INVALID_RANGE = "INVALID_RANGE"
    INVALID_NESTED_OBJECT = "INVALID_NESTED_OBJECT"
    RESERVED_FIELD = "RESERVED_FIELD"
    INVALID_EXTENSION_NAMESPACE = "INVALID_EXTENSION_NAMESPACE"


@dataclass(frozen=True)
class SchemaValidationError:
    category: SchemaErrorCategory
    message: str
    path: str
    actual_value: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.value,
            "message": self.message,
            "path": self.path,
            "actual_value": str(self.actual_value) if self.actual_value is not None else None,
        }


@dataclass
class SchemaValidationResult:
    valid: bool
    schema_version: str
    errors: List[SchemaValidationError] = field(default_factory=list)

    @property
    def primary_error(self) -> Optional[SchemaValidationError]:
        return self.errors[0] if self.errors else None

    @property
    def error_category(self) -> Optional[str]:
        return self.errors[0].category.value if self.errors else None

    @property
    def error_message(self) -> Optional[str]:
        return self.errors[0].message if self.errors else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "schema_version": self.schema_version,
            "error_count": len(self.errors),
            "errors": [e.to_dict() for e in self.errors],
        }


# ==============================================================================
# Frozen Normative Constants & RegEx Patterns
# ==============================================================================

RESERVED_KEYWORDS: Set[str] = {
    "delta_audit",
    "formula_override",
    "dynamic_weights",
    "runtime_bypass",
}

EXTENSION_NAMESPACE_REGEX = re.compile(r"^[a-z0-9_]{3,30}:[a-z0-9_]{2,50}$")

SCENARIO_ID_REGEX = re.compile(
    r"^(SCN-(NVD|SYN)-\d{3}|GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4})$"
)

CVE_ID_REGEX = re.compile(r"^CVE-\d{4}-\d{4,}$")
OVERRIDE_ID_REGEX = re.compile(r"^OVR-\d{4}-\d{4,}$")

ALLOWED_SEVERITIES: Set[str] = {"NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
ALLOWED_PRIORITIES: Set[str] = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
ALLOWED_INTERNET_EXPOSURE: Set[str] = {"public", "dmz", "internal", "isolated"}
ALLOWED_CONTROL_TYPES: Set[str] = {
    "network_firewall",
    "waf",
    "edr",
    "segmentation",
    "mfa",
    "least_privilege",
    "rate_limiting",
    "custom_compensating_control",
}
ALLOWED_CONTROL_STATUSES: Set[str] = {"enforced", "planned", "inactive", "partial"}
ALLOWED_LINK_CONFIDENCES: Set[str] = {"high", "medium", "low", "unverified"}
ALLOWED_REQUIREMENTS: Set[str] = {"H", "M", "L", "X"}
ALLOWED_HUMAN_REVIEW_STATUSES: Set[str] = {"required", "completed", "waived", "pending_review"}
ALLOWED_AUTHORIZATION_STATES: Set[str] = {
    "NOT_REQUESTED",
    "REQUESTED",
    "APPROVED",
    "REJECTED",
    "SUPERSEDED",
}
ALLOWED_REASON_CODES: Set[str] = {
    "DOCUMENTED_ENVIRONMENTAL_EXCEPTION",
    "CONTROL_COMPENSATION",
    "ASSET_CRITICALITY_EXCEPTION",
    "EXPOSURE_CONTEXT_EXCEPTION",
    "EVIDENCE_CONFLICT_REQUIRES_REVIEW",
    "OTHER_REQUIRES_DOCUMENTED_JUSTIFICATION",
}
ALLOWED_GOVERNANCE_ROLES: Set[str] = {
    "SECURITY_LEAD",
    "MASTER_SUPERADMIN",
    "INCIDENT_COMMANDER",
}


# ==============================================================================
# Object Policy Definitions
# ==============================================================================

OBJECT_SPECS: Dict[str, Dict[str, Any]] = {
    "TraceRoot": {
        "required": {
            "scenario_id": str,
            "scenario_source": str,
            "official_or_assigned_cvss_v4_vector": str,
            "cvss_b_score": (str, int, float),
            "cvss_b_severity": str,
            "environmental_evidence": dict,
            "candidate_environmental_assessment": dict,
            "priority_comparison": dict,
            "boundary": str,
        },
        "optional": {
            "cve_id": (str, type(None)),
            "governance_override": (dict, type(None)),
            "extensions": dict,
        },
    },
    "EnvironmentalEvidence": {
        "required": {
            "asset_class": str,
            "deployment_context": str,
            "internet_exposure": str,
            "privilege_context": str,
            "compensating_controls": list,
            "evidence_links": list,
            "evidence_summary": str,
        },
        "optional": {},
    },
    "CompensatingControlItem": {
        "required": {
            "control_id": str,
            "control_type": str,
            "status": str,
        },
        "optional": {
            "description": str,
        },
    },
    "EvidenceLinkItem": {
        "required": {
            "link_id": str,
            "uri_or_reference": str,
            "confidence": str,
        },
        "optional": {},
    },
    "CandidateEnvironmentalAssessment": {
        "required": {
            "confidentiality_requirement": str,
            "integrity_requirement": str,
            "availability_requirement": str,
            "candidate_modified_metrics": dict,
            "watcher_recommendation": str,
            "uncertainty_flags": list,
            "human_review_status": str,
        },
        "optional": {},
    },
    "CandidateModifiedMetrics": {
        "required": {},
        "optional": {
            "MAV": str, "MAC": str, "MAT": str, "MPR": str, "MUI": str,
            "MVC": str, "MVI": str, "MVA": str,
            "MSC": str, "MSI": str, "MSA": str,
            "CR": str, "IR": str, "AR": str,
        },
    },
    "PriorityComparison": {
        "required": {
            "base_priority": str,
            "environmental_priority": str,
            "priority_delta": (str, int, float),
        },
        "optional": {},
    },
    "GovernanceOverrideRecord": {
        "required": {
            "override_id": str,
            "case_id": str,
            "nominal_policy_priority": str,
            "pre_override_priority": str,
            "post_override_priority": str,
            "override_requested": bool,
            "override_applied": bool,
            "authorization_state": str,
            "review_required": bool,
            "schema_version": str,
        },
        "optional": {
            "reason_code": (str, type(None)),
            "reason_text_optional": (str, type(None)),
            "evidence_ids": list,
            "authorized_by_role": (str, type(None)),
            "authorization_timestamp": (str, type(None)),
            "trace_link": (str, type(None)),
        },
    },
}


# ==============================================================================
# Closed-World Validator Implementation (Schema v2)
# ==============================================================================

class SchemaV2Validator:
    """Normative Closed-World Schema Validator for CVSS v4.0 Evidence Traces."""

    def __init__(self, fail_fast: bool = True):
        self.fail_fast = fail_fast

    def validate(self, trace_data: Any) -> SchemaValidationResult:
        errors: List[SchemaValidationError] = []

        if not isinstance(trace_data, dict):
            errors.append(
                SchemaValidationError(
                    category=SchemaErrorCategory.INVALID_TYPE,
                    message=f"Root trace payload must be a JSON object, got {type(trace_data).__name__}",
                    path="root",
                    actual_value=type(trace_data).__name__,
                )
            )
            return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        # 1. Validate Root Object closed-world structure
        self._validate_object(
            obj=trace_data,
            spec_name="TraceRoot",
            path="root",
            errors=errors,
        )
        if errors and self.fail_fast:
            return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        # 2. Specific Root Field Content Validations
        if "scenario_id" in trace_data and isinstance(trace_data["scenario_id"], str):
            if not SCENARIO_ID_REGEX.match(trace_data["scenario_id"]):
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.INVALID_ENUM,
                        message=f"Invalid scenario_id format: '{trace_data['scenario_id']}'",
                        path="root.scenario_id",
                        actual_value=trace_data["scenario_id"],
                    )
                )
                if self.fail_fast:
                    return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        if "cve_id" in trace_data and trace_data["cve_id"] is not None:
            if not isinstance(trace_data["cve_id"], str) or not CVE_ID_REGEX.match(trace_data["cve_id"]):
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.INVALID_ENUM,
                        message=f"Invalid cve_id format: '{trace_data['cve_id']}'",
                        path="root.cve_id",
                        actual_value=trace_data["cve_id"],
                    )
                )
                if self.fail_fast:
                    return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        if "cvss_b_severity" in trace_data and trace_data["cvss_b_severity"] not in ALLOWED_SEVERITIES:
            errors.append(
                SchemaValidationError(
                    category=SchemaErrorCategory.INVALID_ENUM,
                    message=f"Invalid cvss_b_severity: '{trace_data['cvss_b_severity']}'",
                    path="root.cvss_b_severity",
                    actual_value=trace_data["cvss_b_severity"],
                )
            )
            if self.fail_fast:
                return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        # 3. Validate EnvironmentalEvidence subobject
        env_ev = trace_data.get("environmental_evidence")
        if isinstance(env_ev, dict):
            self._validate_object(env_ev, "EnvironmentalEvidence", "root.environmental_evidence", errors)
            if errors and self.fail_fast:
                return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

            # Enum: internet_exposure
            ie = env_ev.get("internet_exposure")
            if ie and ie not in ALLOWED_INTERNET_EXPOSURE:
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.INVALID_ENUM,
                        message=f"Invalid internet_exposure: '{ie}'",
                        path="root.environmental_evidence.internet_exposure",
                        actual_value=ie,
                    )
                )
                if self.fail_fast:
                    return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

            # Array: compensating_controls
            controls = env_ev.get("compensating_controls", [])
            if isinstance(controls, list):
                for idx, ctrl in enumerate(controls):
                    ctrl_path = f"root.environmental_evidence.compensating_controls[{idx}]"
                    if not isinstance(ctrl, dict):
                        errors.append(
                            SchemaValidationError(
                                category=SchemaErrorCategory.INVALID_NESTED_OBJECT,
                                message="Compensating control item must be an object",
                                path=ctrl_path,
                            )
                        )
                    else:
                        self._validate_object(ctrl, "CompensatingControlItem", ctrl_path, errors)
                        if ctrl.get("control_type") not in ALLOWED_CONTROL_TYPES:
                            errors.append(
                                SchemaValidationError(
                                    category=SchemaErrorCategory.INVALID_ENUM,
                                    message=f"Invalid control_type: '{ctrl.get('control_type')}'",
                                    path=f"{ctrl_path}.control_type",
                                    actual_value=ctrl.get("control_type"),
                                )
                            )
                        if ctrl.get("status") not in ALLOWED_CONTROL_STATUSES:
                            errors.append(
                                SchemaValidationError(
                                    category=SchemaErrorCategory.INVALID_ENUM,
                                    message=f"Invalid control status: '{ctrl.get('status')}'",
                                    path=f"{ctrl_path}.status",
                                    actual_value=ctrl.get("status"),
                                )
                            )
                    if errors and self.fail_fast:
                        return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

            # Array: evidence_links
            links = env_ev.get("evidence_links", [])
            if isinstance(links, list):
                for idx, lnk in enumerate(links):
                    lnk_path = f"root.environmental_evidence.evidence_links[{idx}]"
                    if not isinstance(lnk, dict):
                        errors.append(
                            SchemaValidationError(
                                category=SchemaErrorCategory.INVALID_NESTED_OBJECT,
                                message="Evidence link item must be an object",
                                path=lnk_path,
                            )
                        )
                    else:
                        self._validate_object(lnk, "EvidenceLinkItem", lnk_path, errors)
                        if lnk.get("confidence") not in ALLOWED_LINK_CONFIDENCES:
                            errors.append(
                                SchemaValidationError(
                                    category=SchemaErrorCategory.INVALID_ENUM,
                                    message=f"Invalid link confidence: '{lnk.get('confidence')}'",
                                    path=f"{lnk_path}.confidence",
                                    actual_value=lnk.get("confidence"),
                                )
                            )
                    if errors and self.fail_fast:
                        return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        # 4. Validate CandidateEnvironmentalAssessment subobject
        cand = trace_data.get("candidate_environmental_assessment")
        if isinstance(cand, dict):
            self._validate_object(cand, "CandidateEnvironmentalAssessment", "root.candidate_environmental_assessment", errors)
            if errors and self.fail_fast:
                return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

            for req_metric in ["confidentiality_requirement", "integrity_requirement", "availability_requirement"]:
                val = cand.get(req_metric)
                if val and val not in ALLOWED_REQUIREMENTS:
                    errors.append(
                        SchemaValidationError(
                            category=SchemaErrorCategory.INVALID_ENUM,
                            message=f"Invalid metric requirement value '{val}' for {req_metric}",
                            path=f"root.candidate_environmental_assessment.{req_metric}",
                            actual_value=val,
                        )
                    )
            if cand.get("human_review_status") not in ALLOWED_HUMAN_REVIEW_STATUSES:
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.INVALID_ENUM,
                        message=f"Invalid human_review_status: '{cand.get('human_review_status')}'",
                        path="root.candidate_environmental_assessment.human_review_status",
                        actual_value=cand.get("human_review_status"),
                    )
                )

            # Nested: candidate_modified_metrics
            cmm = cand.get("candidate_modified_metrics")
            if isinstance(cmm, dict):
                self._validate_object(cmm, "CandidateModifiedMetrics", "root.candidate_environmental_assessment.candidate_modified_metrics", errors)

            if errors and self.fail_fast:
                return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        # 5. Validate PriorityComparison subobject
        prio = trace_data.get("priority_comparison")
        if isinstance(prio, dict):
            self._validate_object(prio, "PriorityComparison", "root.priority_comparison", errors)
            if errors and self.fail_fast:
                return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

            for p_field in ["base_priority", "environmental_priority"]:
                pval = prio.get(p_field)
                if pval and pval not in ALLOWED_PRIORITIES:
                    errors.append(
                        SchemaValidationError(
                            category=SchemaErrorCategory.INVALID_ENUM,
                            message=f"Invalid priority '{pval}' for {p_field}",
                            path=f"root.priority_comparison.{p_field}",
                            actual_value=pval,
                        )
                    )
            if errors and self.fail_fast:
                return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        # 6. Validate GovernanceOverrideRecord (if present)
        gov = trace_data.get("governance_override")
        if gov is not None:
            if not isinstance(gov, dict):
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.INVALID_TYPE,
                        message="governance_override must be an object if present",
                        path="root.governance_override",
                    )
                )
            else:
                self._validate_object(gov, "GovernanceOverrideRecord", "root.governance_override", errors)
                ovr_id = gov.get("override_id")
                if ovr_id and not OVERRIDE_ID_REGEX.match(ovr_id):
                    errors.append(
                        SchemaValidationError(
                            category=SchemaErrorCategory.INVALID_ENUM,
                            message=f"Invalid override_id format '{ovr_id}'",
                            path="root.governance_override.override_id",
                            actual_value=ovr_id,
                        )
                    )
                state = gov.get("authorization_state")
                if state and state not in ALLOWED_AUTHORIZATION_STATES:
                    errors.append(
                        SchemaValidationError(
                            category=SchemaErrorCategory.INVALID_ENUM,
                            message=f"Invalid authorization_state '{state}'",
                            path="root.governance_override.authorization_state",
                            actual_value=state,
                        )
                    )
                rc = gov.get("reason_code")
                if rc is not None and rc not in ALLOWED_REASON_CODES:
                    errors.append(
                        SchemaValidationError(
                            category=SchemaErrorCategory.INVALID_ENUM,
                            message=f"Invalid reason_code '{rc}'",
                            path="root.governance_override.reason_code",
                            actual_value=rc,
                        )
                    )
                role = gov.get("authorized_by_role")
                if role is not None and role not in ALLOWED_GOVERNANCE_ROLES:
                    errors.append(
                        SchemaValidationError(
                            category=SchemaErrorCategory.INVALID_ENUM,
                            message=f"Invalid authorized_by_role '{role}'",
                            path="root.governance_override.authorized_by_role",
                            actual_value=role,
                        )
                    )
            if errors and self.fail_fast:
                return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        # 7. Validate Extensions Namespace Point
        extensions = trace_data.get("extensions")
        if extensions is not None:
            if not isinstance(extensions, dict):
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.INVALID_TYPE,
                        message="extensions must be a JSON object",
                        path="root.extensions",
                    )
                )
            else:
                for ext_key in extensions.keys():
                    # Check reserved keywords
                    if ext_key in RESERVED_KEYWORDS:
                        errors.append(
                            SchemaValidationError(
                                category=SchemaErrorCategory.RESERVED_FIELD,
                                message=f"Use of reserved keyword '{ext_key}' in extensions is prohibited",
                                path=f"root.extensions.{ext_key}",
                                actual_value=ext_key,
                            )
                        )
                    elif not EXTENSION_NAMESPACE_REGEX.match(ext_key):
                        errors.append(
                            SchemaValidationError(
                                category=SchemaErrorCategory.INVALID_EXTENSION_NAMESPACE,
                                message=f"Extension key '{ext_key}' does not match required vendor namespace pattern",
                                path=f"root.extensions.{ext_key}",
                                actual_value=ext_key,
                            )
                        )
                    if errors and self.fail_fast:
                        return SchemaValidationResult(valid=False, schema_version="v2", errors=errors)

        return SchemaValidationResult(
            valid=(len(errors) == 0),
            schema_version="v2",
            errors=errors,
        )

    def _validate_object(
        self,
        obj: Dict[str, Any],
        spec_name: str,
        path: str,
        errors: List[SchemaValidationError],
    ) -> None:
        """Enforces closed-world property adherence and types on a dictionary."""
        spec = OBJECT_SPECS[spec_name]
        required_fields = spec["required"]
        optional_fields = spec["optional"]
        allowed_fields = set(required_fields.keys()).union(set(optional_fields.keys()))

        # A. Check for unknown fields and reserved keywords (Closed-World Enforcement)
        for field_name, value in obj.items():
            if field_name in RESERVED_KEYWORDS:
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.RESERVED_FIELD,
                        message=f"Encountered prohibited reserved keyword '{field_name}'",
                        path=f"{path}.{field_name}",
                        actual_value=value,
                    )
                )
                if self.fail_fast:
                    return
            elif field_name not in allowed_fields:
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.UNKNOWN_FIELD,
                        message=f"Undeclared property '{field_name}' in closed-world object {spec_name}",
                        path=f"{path}.{field_name}",
                        actual_value=value,
                    )
                )
                if self.fail_fast:
                    return

        # B. Check for missing required fields
        for req_field, expected_type in required_fields.items():
            if req_field not in obj:
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.MISSING_REQUIRED_FIELD,
                        message=f"Missing required field '{req_field}' in {spec_name}",
                        path=f"{path}.{req_field}",
                    )
                )
                if self.fail_fast:
                    return
            else:
                val = obj[req_field]
                if not isinstance(val, expected_type):
                    errors.append(
                        SchemaValidationError(
                            category=SchemaErrorCategory.INVALID_TYPE,
                            message=f"Field '{req_field}' expects type {expected_type}, got {type(val).__name__}",
                            path=f"{path}.{req_field}",
                            actual_value=val,
                        )
                    )
                    if self.fail_fast:
                        return

        # C. Check optional field types if present
        for opt_field, expected_type in optional_fields.items():
            if opt_field in obj:
                val = obj[opt_field]
                if not isinstance(val, expected_type):
                    errors.append(
                        SchemaValidationError(
                            category=SchemaErrorCategory.INVALID_TYPE,
                            message=f"Optional field '{opt_field}' expects type {expected_type}, got {type(val).__name__}",
                            path=f"{path}.{opt_field}",
                            actual_value=val,
                        )
                    )
                    if self.fail_fast:
                        return


# ==============================================================================
# Historical Open-World Validator Implementation (Schema v1 Baseline)
# ==============================================================================

class SchemaV1Validator:
    """Historical Open-World Baseline Validator preserving R2-R5 semantics."""

    REQUIRED_ROOT_FIELDS: Set[str] = {
        "scenario_id",
        "scenario_source",
        "official_or_assigned_cvss_v4_vector",
        "cvss_b_score",
        "cvss_b_severity",
        "environmental_evidence",
        "candidate_environmental_assessment",
        "priority_comparison",
        "boundary",
    }

    def validate(self, trace_data: Any) -> SchemaValidationResult:
        errors: List[SchemaValidationError] = []

        if not isinstance(trace_data, dict):
            errors.append(
                SchemaValidationError(
                    category=SchemaErrorCategory.INVALID_TYPE,
                    message="Payload must be a JSON object",
                    path="root",
                )
            )
            return SchemaValidationResult(valid=False, schema_version="v1", errors=errors)

        # Open-World Check: Only mandatory fields are enforced; extra attributes are tolerated.
        for rf in self.REQUIRED_ROOT_FIELDS:
            if rf not in trace_data:
                errors.append(
                    SchemaValidationError(
                        category=SchemaErrorCategory.MISSING_REQUIRED_FIELD,
                        message=f"Missing required field '{rf}' under v1 open-world contract",
                        path=f"root.{rf}",
                    )
                )

        return SchemaValidationResult(
            valid=(len(errors) == 0),
            schema_version="v1",
            errors=errors,
        )


# ==============================================================================
# Unified Public API
# ==============================================================================

def validate_trace(trace_data: Any, schema_version: str = "v2") -> SchemaValidationResult:
    """
    Validates a trace dictionary against the specified schema contract.

    Args:
        trace_data: In-memory dictionary representing the vulnerability evidence trace.
        schema_version: 'v1' for historical open-world baseline, 'v2' for closed-world candidate.

    Returns:
        SchemaValidationResult containing boolean validity and error diagnostics.
    """
    if schema_version == "v1":
        validator = SchemaV1Validator()
        return validator.validate(trace_data)
    elif schema_version == "v2":
        validator = SchemaV2Validator()
        return validator.validate(trace_data)
    else:
        raise ValueError(f"Unknown schema_version '{schema_version}'. Supported: 'v1', 'v2'.")


def validate_trace_v1(trace_data: Any) -> SchemaValidationResult:
    """Convenience wrapper for historical Schema v1 open-world validation."""
    return validate_trace(trace_data, schema_version="v1")


def validate_trace_v2(trace_data: Any) -> SchemaValidationResult:
    """Convenience wrapper for Schema v2 closed-world validation."""
    return validate_trace(trace_data, schema_version="v2")
