#!/usr/bin/env python3
"""
tests/test_r6_schema_v2_contract.py - T1 Schema Unit Contract Tests for R6-A1.

Derives exclusively from:
- validation/article/r6_schema_v2_specification.md
- validation/article/r6_schema_v2_contract.json

Evaluates:
- Closed-world rejection of undeclared properties across root and nested objects.
- Correct error categories (UNKNOWN_FIELD, MISSING_REQUIRED_FIELD, INVALID_TYPE, etc.).
- Explicit extension point vendor namespacing.
- Prohibited reserved keyword enforcement (delta_audit, etc.).
- Strict decoupling: Schema v1 historical open-world path remains accessible and distinct.
"""

from __future__ import annotations

import copy
from typing import Any, Dict

import pytest

from core.r6_schema_v2_validator import (
    SchemaErrorCategory,
    SchemaV1Validator,
    SchemaV2Validator,
    validate_trace,
    validate_trace_v1,
    validate_trace_v2,
)


@pytest.fixture
def valid_v2_trace() -> Dict[str, Any]:
    """Provides a minimal canonical synthetic trace strictly conforming to Schema v2."""
    return {
        "scenario_id": "SCN-SYN-001",
        "scenario_source": "synthetic_expert_scenario",
        "official_or_assigned_cvss_v4_vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        "cvss_b_score": 9.3,
        "cvss_b_severity": "CRITICAL",
        "environmental_evidence": {
            "asset_class": "public_web_application",
            "deployment_context": "Production Kubernetes Cluster",
            "internet_exposure": "public",
            "privilege_context": "unprivileged",
            "compensating_controls": [
                {
                    "control_id": "CTRL-WAF-01",
                    "control_type": "waf",
                    "status": "enforced",
                    "description": "Cloudflare WAF with OWASP CRS",
                }
            ],
            "evidence_links": [
                {
                    "link_id": "LINK-01",
                    "uri_or_reference": "https://internal.sec/evidence/01",
                    "confidence": "high",
                }
            ],
            "evidence_summary": "Public facing web app protected by WAF",
        },
        "candidate_environmental_assessment": {
            "confidentiality_requirement": "H",
            "integrity_requirement": "H",
            "availability_requirement": "H",
            "candidate_modified_metrics": {
                "MAV": "N",
                "MAC": "L",
            },
            "watcher_recommendation": "Maintain critical rating",
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


# ==============================================================================
# T1 Test Suite: Cases 1 through 15
# ==============================================================================

def test_t1_01_valid_declared_core_object_accepted(valid_v2_trace):
    """T1.1: Valid declared core object strictly adheres to Schema v2 and is accepted."""
    result = validate_trace_v2(valid_v2_trace)
    assert result.valid is True
    assert len(result.errors) == 0
    assert result.schema_version == "v2"


def test_t1_02_unknown_core_field_rejected(valid_v2_trace):
    """T1.2: Undeclared property in root object is rejected with UNKNOWN_FIELD."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["spurious_attribute"] = "malicious_payload"

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.UNKNOWN_FIELD.value
    assert "spurious_attribute" in result.error_message


def test_t1_03_unknown_nested_core_field_rejected(valid_v2_trace):
    """T1.3: Undeclared property inside nested core object is rejected with UNKNOWN_FIELD."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["environmental_evidence"]["spurious_metadata"] = 12345

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.UNKNOWN_FIELD.value
    assert "spurious_metadata" in result.error_message


def test_t1_04_valid_permitted_extension_namespace_accepted(valid_v2_trace):
    """T1.4: Well-formed vendor-namespaced extension inside extensions: {} is accepted."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["extensions"] = {
        "helpus:audit_telemetry": {"stage": "pre_scoring", "id": 101},
        "acme_corp:risk_rating": "Tier1",
    }

    result = validate_trace_v2(mutant)
    assert result.valid is True
    assert len(result.errors) == 0


def test_t1_05_malformed_extension_namespace_rejected(valid_v2_trace):
    """T1.5: Extension attribute lacking required vendor prefix is rejected with INVALID_EXTENSION_NAMESPACE."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["extensions"] = {
        "unnamespaced_key": "arbitrary_value",
    }

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.INVALID_EXTENSION_NAMESPACE.value


def test_t1_06_missing_required_field_rejected(valid_v2_trace):
    """T1.6: Omitting a required attribute raises MISSING_REQUIRED_FIELD."""
    mutant = copy.deepcopy(valid_v2_trace)
    del mutant["scenario_id"]

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.MISSING_REQUIRED_FIELD.value


def test_t1_07_invalid_type_rejected(valid_v2_trace):
    """T1.7: Supplying wrong primitive type raises INVALID_TYPE."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["scenario_id"] = 123456  # Expected str

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.INVALID_TYPE.value


def test_t1_08_invalid_enum_rejected(valid_v2_trace):
    """T1.8: Supplying an unauthorized token raises INVALID_ENUM."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["environmental_evidence"]["internet_exposure"] = "unrestricted_worldwide"

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.INVALID_ENUM.value


def test_t1_09_invalid_range_or_format_rejected(valid_v2_trace):
    """T1.9: Supplying malformed ID pattern raises INVALID_ENUM or INVALID_RANGE."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["scenario_id"] = "INVALID-FORMAT-999"

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.INVALID_ENUM.value


def test_t1_10_null_handling_rejected(valid_v2_trace):
    """T1.10: Null in non-nullable scalar field raises INVALID_TYPE."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["environmental_evidence"]["asset_class"] = None

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.INVALID_TYPE.value


def test_t1_11_reserved_field_rejected(valid_v2_trace):
    """T1.11: Prohibited keyword 'delta_audit' produces RESERVED_FIELD."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["delta_audit"] = {"e": 0.5}

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.RESERVED_FIELD.value


def test_t1_12_no_silent_v1_fallback(valid_v2_trace):
    """T1.12: When validating under v2, an unknown field fails closed and does not fallback to v1."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["undeclared_v1_tolerated_field"] = "foo"

    result = validate_trace(mutant, schema_version="v2")
    assert result.valid is False
    assert result.schema_version == "v2"


def test_t1_13_closed_world_nested_behavior(valid_v2_trace):
    """T1.13: Nested list items (EvidenceLinkItem) strictly reject extra properties."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["environmental_evidence"]["evidence_links"][0]["extra_link_attr"] = "unauthorized"

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.UNKNOWN_FIELD.value


def test_t1_14_normalization_boundary_does_not_coerce_invalid(valid_v2_trace):
    """T1.14: Structural validity is separate; invalid structure cannot pass validator."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["priority_comparison"]["base_priority"] = "SUPER_CRITICAL"

    result = validate_trace_v2(mutant)
    assert result.valid is False
    assert result.error_category == SchemaErrorCategory.INVALID_ENUM.value


def test_t1_15_schema_v1_historical_path_remains_distinct(valid_v2_trace):
    """T1.15: Schema v1 baseline tolerates extraneous properties (open-world historical fidelity)."""
    mutant = copy.deepcopy(valid_v2_trace)
    mutant["spurious_open_world_attribute"] = "accepted_in_v1"

    # Schema v2 must reject
    res_v2 = validate_trace_v2(mutant)
    assert res_v2.valid is False

    # Schema v1 must accept (historical open-world baseline)
    res_v1 = validate_trace_v1(mutant)
    assert res_v1.valid is True
    assert res_v1.schema_version == "v1"
