"""
Unit tests for the Independent Trace Verifier (tools/verify_trace_integrity.py).

Verifies that the verifier correctly validates structural integrity, algebraic
recomputation, cross-artifact consistency, and schema limitations across NVD
and synthetic scenario trace schemas.

Epistemological and Governance Boundary:
Uses self-contained test fixtures and the shared canonical policy module
(core.cvss40_environmental_policy) without accessing or unsealing confirmatory
gatekeeper datasets C1 or C2.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Dict

import pytest

import core.cvss40_environmental_policy as canonical_policy
from core.cvss40_environmental_policy import (
    CONTROL_WEIGHTS,
    CONTEXT_WEIGHTS,
    DEFAULT_CONTROL_WEIGHT,
    ENV_PROFILES,
    PRIORITY_ORDER,
    SEVERITY_TO_PRIORITY,
    adjust_priority,
    compute_delta_cat,
    lookup_nominal_weights,
    ordinal_to_priority,
    priority_to_ordinal,
    recompute_p_base,
    recompute_p_env_nominal,
)
import tools.verify_trace_integrity as trace_verifier_module
from tools.verify_trace_integrity import (
    CheckCategory,
    CheckStatus,
    TraceVerifier,
)


# ==============================================================================
# Canonical Fixtures (Unsealed Local Templates)
# ==============================================================================

VALID_NVD_FIXTURE: Dict[str, Any] = {
    "scenario_id": "SCN-NVD-002",
    "scenario_source": "nvd_cvss_v4_with_curated_environment",
    "cve_id": "CVE-2026-4252",
    "official_or_assigned_cvss_v4_vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X",
    "cvss_b_score": "8.9",
    "cvss_b_severity": "HIGH",
    "environmental_evidence": {
        "asset_class": "internal_admin_console",
        "deployment_context": "Internal administrative interface restricted to VPN and privileged operators.",
        "internet_exposure": "restricted",
        "privilege_context": "Administrative role required after VPN authentication.",
        "compensating_controls": "VPN, MFA, network segmentation, privileged access monitoring.",
        "evidence_links": "https://nvd.nist.gov/vuln/detail/CVE-2026-4252",
        "evidence_summary": "NVD CVE record with CVSS v4.0 metric plus curated local deployment profile: internal_admin_console.",
    },
    "candidate_environmental_assessment": {
        "confidentiality_requirement": "CR:M - confidentiality depends on administrative data visible through the console.",
        "integrity_requirement": "IR:H - integrity is high because admin actions may alter production configuration.",
        "availability_requirement": "AR:M - availability is medium due to operational dependency.",
        "candidate_modified_metrics": "Candidate Modified Base metrics should review restricted network path, MFA, privileges, and segmentation.",
        "watcher_recommendation": "Review candidate Environmental metric choices against curated deployment evidence before treating them as final.",
        "uncertainty_flags": "local_environment_curated; human_review_required; threat_context_not_authoritative",
        "human_review_status": "required",
    },
    "priority_comparison": {
        "base_priority": "high",
        "environmental_priority": "medium",
        "priority_delta": "-1",
    },
    "boundary": "This trace supports article workflow evaluation. It is not an autonomous official CVSS score.",
}

VALID_SYNTHETIC_FIXTURE: Dict[str, Any] = {
    "scenario_id": "SCN-SYN-013",
    "scenario_source": "curated_synthetic_no_cve",
    "cve_id": "",
    "official_or_assigned_cvss_v4_vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H",
    "cvss_b_score": "9.3",
    "cvss_b_severity": "CRITICAL",
    "environmental_evidence": {
        "asset_class": "developer_workstation",
        "deployment_context": "Developer endpoint with access to source code, build tools, and internal repositories.",
        "internet_exposure": "restricted",
        "privilege_context": "Standard developer user with access to internal repositories and CI credentials.",
        "compensating_controls": "EDR, device management, least privilege, repository access controls.",
        "evidence_links": "local://curated-scenario/SCN-SYN-013; docs/ARTICLE_DATASET_SCHEMA.md",
        "evidence_summary": "Curated local environment profile for developer_workstation; CVSS v4.0 vector assigned for controlled experiment, not an official CVE score.",
    },
    "candidate_environmental_assessment": {
        "confidentiality_requirement": "CR:M - confidentiality is medium due to source code and secrets exposure risk.",
        "integrity_requirement": "IR:H - integrity is high because code or pipeline changes may affect production.",
        "availability_requirement": "AR:L - availability impact is usually limited to one endpoint.",
        "candidate_modified_metrics": "Candidate Modified Base metrics should review endpoint controls, credentials, repository access, and user interaction.",
        "watcher_recommendation": "Use this row only as a curated scenario for workflow validation; final Environmental choices require human review.",
        "uncertainty_flags": "synthetic_scenario; assigned_vector_not_official_cve; human_review_required",
        "human_review_status": "required",
    },
    "priority_comparison": {
        "base_priority": "critical",
        "environmental_priority": "critical",
        "priority_delta": "0",
    },
    "boundary": "This trace supports article workflow evaluation. It is not an autonomous official CVSS score.",
}


# ==============================================================================
# 1. Canonical Policy Source and Parity Contract Tests
# ==============================================================================

def test_verifier_uses_canonical_policy_source():
    """Confirms verifier imports directly from core.cvss40_environmental_policy."""
    assert trace_verifier_module.PRIORITY_ORDER is canonical_policy.PRIORITY_ORDER
    assert trace_verifier_module.SEVERITY_TO_PRIORITY is canonical_policy.SEVERITY_TO_PRIORITY
    assert trace_verifier_module.CONTEXT_WEIGHTS is canonical_policy.CONTEXT_WEIGHTS
    assert trace_verifier_module.CONTROL_WEIGHTS is canonical_policy.CONTROL_WEIGHTS
    assert trace_verifier_module.priority_to_ordinal is canonical_policy.priority_to_ordinal
    assert trace_verifier_module.recompute_p_env_nominal is canonical_policy.recompute_p_env_nominal


def test_canonical_policy_profiles_parity():
    """Validates the canonical profile universe against Manuscript Eq. 8 contracts."""
    assert len(canonical_policy.ENV_PROFILES) == 8

    expected_assets = {
        "public_web_application",
        "internal_admin_console",
        "identity_provider",
        "database_server",
        "developer_workstation",
        "isolated_lab_system",
        "ot_monitoring_gateway",
        "public_api_gateway",
    }
    actual_assets = {p["asset_class"] for p in canonical_policy.ENV_PROFILES}
    assert actual_assets == expected_assets

    # Domain contracts from Manuscript Eq. 8
    valid_context_domain = {-2, 0, 1, 2, 3}
    valid_control_domain = {-1, 0}

    for p in canonical_policy.ENV_PROFILES:
        assert p["context_weight"] in valid_context_domain
        assert p["control_weight"] in valid_control_domain

    # Specific profile contracts
    assert canonical_policy.CONTEXT_WEIGHTS["public_api_gateway"] == 3
    assert canonical_policy.CONTEXT_WEIGHTS["isolated_lab_system"] == -2
    assert canonical_policy.CONTROL_WEIGHTS["ot_monitoring_gateway"] == 0
    assert canonical_policy.CONTROL_WEIGHTS["internal_admin_console"] == -1


# ==============================================================================
# 2. Happy Path Verification
# ==============================================================================

def test_happy_path_nvd_fixture():
    verifier = TraceVerifier()
    res = verifier.verify_scenario_trace(copy.deepcopy(VALID_NVD_FIXTURE))
    assert res.passed is True
    assert res.failure_count == 0
    assert res.source_type == "NVD"
    pass_names = [c.name for c in res.checks if c.status == CheckStatus.PASS]
    assert "structural_required_top_level_fields" in pass_names
    assert "structural_governance_authorization_state" in pass_names
    assert "recomputed_base_priority" in pass_names
    assert "recomputed_category_delta" in pass_names
    assert "recomputed_nvd_cvss_score" in pass_names
    assert "consistency_source_separation" in pass_names


def test_happy_path_synthetic_fixture():
    verifier = TraceVerifier()
    res = verifier.verify_scenario_trace(copy.deepcopy(VALID_SYNTHETIC_FIXTURE))
    assert res.passed is True
    assert res.failure_count == 0
    assert res.source_type == "SYNTHETIC"
    pass_names = [c.name for c in res.checks if c.status == CheckStatus.PASS]
    assert "structural_required_top_level_fields" in pass_names
    assert "consistency_synthetic_vector_syntax" in pass_names
    assert "consistency_synthetic_uncertainty_flags" in pass_names
    assert "recomputed_category_delta" in pass_names


# ==============================================================================
# 3. Structural Integrity: Missing Top-Level Fields
# ==============================================================================

def test_missing_required_top_level_field():
    verifier = TraceVerifier()
    bad_data = copy.deepcopy(VALID_NVD_FIXTURE)
    del bad_data["boundary"]

    res = verifier.verify_scenario_trace(bad_data)
    assert res.passed is False
    assert res.failure_count >= 1

    chk = next(c for c in res.checks if c.name == "structural_required_top_level_fields")
    assert chk.status == CheckStatus.FAIL
    assert "boundary" in chk.details["missing"]


# ==============================================================================
# 4. Structural Integrity: Missing Nested Fields
# ==============================================================================

def test_missing_nested_fields():
    verifier = TraceVerifier()
    bad_data = copy.deepcopy(VALID_SYNTHETIC_FIXTURE)
    del bad_data["candidate_environmental_assessment"]["human_review_status"]

    res = verifier.verify_scenario_trace(bad_data)
    assert res.passed is False

    chk = next(c for c in res.checks if c.name == "structural_nested_candidate_assessment")
    assert chk.status == CheckStatus.FAIL
    assert "human_review_status" in chk.details["missing"]


# ==============================================================================
# 5. Recomputed Algebraic Mismatch: Mismatched Delta_cat
# ==============================================================================

def test_mismatched_category_delta():
    verifier = TraceVerifier()
    bad_data = copy.deepcopy(VALID_NVD_FIXTURE)
    # Stored priorities: high (3) -> medium (2), algebraic delta is -1. Set stored delta to +1.
    bad_data["priority_comparison"]["priority_delta"] = "1"

    res = verifier.verify_scenario_trace(bad_data)
    assert res.passed is False

    chk = next(c for c in res.checks if c.name == "recomputed_category_delta")
    assert chk.status == CheckStatus.FAIL
    assert chk.details["recomputed_delta"] == -1
    assert chk.details["stored_delta"] == 1


# ==============================================================================
# 6. Consistency: Invalid Vector Syntax
# ==============================================================================

def test_invalid_vector_syntax():
    verifier = TraceVerifier()
    bad_data = copy.deepcopy(VALID_SYNTHETIC_FIXTURE)
    bad_data["official_or_assigned_cvss_v4_vector"] = "NOT_A_VALID_CVSS_VECTOR_STRING"

    res = verifier.verify_scenario_trace(bad_data)
    assert res.passed is False

    chk = next(c for c in res.checks if c.name == "consistency_synthetic_vector_syntax")
    assert chk.status == CheckStatus.FAIL


# ==============================================================================
# 7. Recomputed Official Conformance: NVD Score Mismatch
# ==============================================================================

def test_nvd_score_mismatch():
    verifier = TraceVerifier()
    bad_data = copy.deepcopy(VALID_NVD_FIXTURE)
    # The actual vector evaluates to 8.9; alter stored score to 3.5.
    bad_data["cvss_b_score"] = "3.5"

    res = verifier.verify_scenario_trace(bad_data)
    assert res.passed is False

    chk = next(c for c in res.checks if c.name == "recomputed_nvd_cvss_score")
    assert chk.status == CheckStatus.FAIL
    assert abs(chk.details["calculated"] - 8.9) < 1e-4
    assert chk.details["stored"] == 3.5


# ==============================================================================
# 8. Consistency: Synthetic Assigned Case Missing Required Uncertainty Flag
# ==============================================================================

def test_synthetic_missing_assigned_vector_flag():
    verifier = TraceVerifier()
    bad_data = copy.deepcopy(VALID_SYNTHETIC_FIXTURE)
    bad_data["candidate_environmental_assessment"]["uncertainty_flags"] = "synthetic_scenario; human_review_required"

    res = verifier.verify_scenario_trace(bad_data)
    assert res.passed is False

    chk = next(c for c in res.checks if c.name == "consistency_synthetic_uncertainty_flags")
    assert chk.status == CheckStatus.FAIL


# ==============================================================================
# 9. Structural Integrity: Missing Uncertainty Representation
# ==============================================================================

def test_missing_uncertainty_flags():
    verifier = TraceVerifier()
    bad_data = copy.deepcopy(VALID_NVD_FIXTURE)
    bad_data["candidate_environmental_assessment"]["uncertainty_flags"] = "   "

    res = verifier.verify_scenario_trace(bad_data)
    assert res.passed is False

    chk = next(c for c in res.checks if c.name == "structural_uncertainty_representation")
    assert chk.status == CheckStatus.FAIL


# ==============================================================================
# 10. Structural Governance: Invalid Review / Authorization State
# ==============================================================================

def test_invalid_governance_authorization_state():
    verifier = TraceVerifier()
    bad_data = copy.deepcopy(VALID_NVD_FIXTURE)
    # Any state other than "required" is an authorization boundary violation
    bad_data["candidate_environmental_assessment"]["human_review_status"] = "autonomous_approved"

    res = verifier.verify_scenario_trace(bad_data)
    assert res.passed is False

    chk = next(c for c in res.checks if c.name == "structural_governance_authorization_state")
    assert chk.status == CheckStatus.FAIL


# ==============================================================================
# 11. Schema Limitation Isolation: Not Treated as Failure nor Complete Pass
# ==============================================================================

def test_schema_limitation_reported_as_limitation():
    verifier = TraceVerifier()
    data = copy.deepcopy(VALID_SYNTHETIC_FIXTURE)

    res = verifier.verify_scenario_trace(data)
    assert res.passed is True  # Limitations do not cause scenario failure
    assert res.failure_count == 0
    assert res.limitation_count >= 1

    limitations = [c for c in res.checks if c.status == CheckStatus.LIMITATION]
    assert len(limitations) >= 1
    chk = next(c for c in limitations if c.name == "schema_limitation_metric_evidence_linkage")
    assert chk.category == CheckCategory.SCHEMA_LIMITATION
    assert "machine-addressable linkage between each candidate modified metric and its corresponding evidence item" in chk.message


# ==============================================================================
# 12. Epistemological Separation: NVD vs Synthetic
# ==============================================================================

def test_epistemological_separation_nvd_vs_synthetic():
    verifier = TraceVerifier()

    # 1. Synthetic vectors must NOT trigger official NVD scorer conformance check
    syn_data = copy.deepcopy(VALID_SYNTHETIC_FIXTURE)
    res_syn = verifier.verify_scenario_trace(syn_data)
    syn_check_names = [c.name for c in res_syn.checks]
    assert "recomputed_nvd_cvss_score" not in syn_check_names
    assert "consistency_synthetic_vector_syntax" in syn_check_names

    # 2. Synthetic scenarios must not carry a real CVE identifier
    bad_syn = copy.deepcopy(VALID_SYNTHETIC_FIXTURE)
    bad_syn["cve_id"] = "CVE-2026-9999"
    res_bad_syn = verifier.verify_scenario_trace(bad_syn)
    assert res_bad_syn.passed is False
    chk_sep = next(c for c in res_bad_syn.checks if c.name == "consistency_source_separation")
    assert chk_sep.status == CheckStatus.FAIL


# ==============================================================================
# 13. Helper Arithmetic and Seed Parity Consistency
# ==============================================================================

def test_ordinal_and_policy_helpers():
    assert priority_to_ordinal("defer") == 0
    assert priority_to_ordinal("critical") == 4
    assert ordinal_to_priority(0) == "defer"
    assert ordinal_to_priority(4) == "critical"
    # Clamp behavior
    assert ordinal_to_priority(-5) == "defer"
    assert ordinal_to_priority(99) == "critical"

    # Category delta Eq. 9
    assert compute_delta_cat("high", "defer") == -3
    assert compute_delta_cat("medium", "defer") == -2
    assert compute_delta_cat("low", "high") == 2
    assert compute_delta_cat("critical", "critical") == 0

    # Severity to priority mapping
    assert recompute_p_base("LOW") == "low"
    assert recompute_p_base("CRITICAL") == "critical"

    # Nominal policy recomputation
    env_p, delta = recompute_p_env_nominal("high", "isolated_lab_system")
    assert env_p == "defer"
    assert delta == -3

    # Seed generator adjustment logic parity
    profile = canonical_policy.ENV_PROFILES_BY_ASSET["isolated_lab_system"]
    assert adjust_priority("high", profile) == "defer"


# ==============================================================================
# 14. Canonical Discovery Scope from CSV
# ==============================================================================

def test_canonical_discovery_uses_csv_scope():
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"
    assert csv_path.exists(), f"Reference CSV missing at {csv_path}"

    verifier = TraceVerifier(dataset_csv_path=csv_path)
    canonical_ids = verifier.get_canonical_scenario_ids()

    # Must be strictly 30 canonical scenarios
    assert len(canonical_ids) == 30, f"Expected exactly 30 canonical scenarios, got {len(canonical_ids)}"

    expected_nvd = [f"SCN-NVD-{i:03d}" for i in range(1, 13)]
    expected_syn = [f"SCN-SYN-{i:03d}" for i in range(13, 31)]
    expected_all = expected_nvd + expected_syn

    assert canonical_ids == expected_all
    assert len([cid for cid in canonical_ids if cid.startswith("SCN-NVD-")]) == 12
    assert len([cid for cid in canonical_ids if cid.startswith("SCN-SYN-")]) == 18


# ==============================================================================
# 15. Extra Legacy Artifacts Are Out of Scope (Do Not Fail Canonical Run)
# ==============================================================================

def test_out_of_scope_legacy_does_not_fail_canonical_run(tmp_path):
    import json
    repo_root = Path(__file__).resolve().parent.parent
    real_traces_dir = repo_root / "validation" / "article" / "trace"
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"

    verifier = TraceVerifier(dataset_csv_path=csv_path)
    canonical_ids = verifier.get_canonical_scenario_ids()

    traces_tmp = tmp_path / "traces_scope"
    traces_tmp.mkdir()

    # Populate temporary directory with the 30 canonical traces
    for cid in canonical_ids:
        src = real_traces_dir / f"{cid}.json"
        dst = traces_tmp / f"{cid}.json"
        if src.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            template = copy.deepcopy(VALID_NVD_FIXTURE if cid.startswith("SCN-NVD-") else VALID_SYNTHETIC_FIXTURE)
            template["scenario_id"] = cid
            dst.write_text(json.dumps(template), encoding="utf-8")

    # Add an out-of-scope legacy file (e.g. SCN-SYN-001) not listed in the CSV
    extra_file = traces_tmp / "SCN-SYN-001.json"
    extra_file.write_text(json.dumps({"scenario_id": "SCN-SYN-001", "legacy_artifact": True}), encoding="utf-8")

    report = verifier.verify_all_traces(traces_tmp)

    # Extra file must be classified as OUT_OF_SCOPE
    out_of_scope_ids = [entry["scenario_id"] for entry in report.out_of_scope_files]
    assert "SCN-SYN-001" in out_of_scope_ids

    # Canonical evaluation must remain strictly 30/30 PASS
    assert report.total_scenarios == 30
    assert report.canonical_expected == 30
    assert report.canonical_found == 30
    assert report.failed_scenarios == 0
    assert report.passed_scenarios == 30
    assert report.overall_status == "PASS"


# ==============================================================================
# 16. Missing Canonical Trace Generates FAIL
# ==============================================================================

def test_missing_canonical_trace_fails(tmp_path):
    import json
    repo_root = Path(__file__).resolve().parent.parent
    real_traces_dir = repo_root / "validation" / "article" / "trace"
    csv_path = repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv"

    verifier = TraceVerifier(dataset_csv_path=csv_path)
    canonical_ids = verifier.get_canonical_scenario_ids()

    traces_tmp = tmp_path / "traces_missing"
    traces_tmp.mkdir()

    # Omit one canonical ID (SCN-NVD-001)
    omitted_id = "SCN-NVD-001"
    for cid in canonical_ids:
        if cid == omitted_id:
            continue
        src = real_traces_dir / f"{cid}.json"
        dst = traces_tmp / f"{cid}.json"
        if src.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            template = copy.deepcopy(VALID_NVD_FIXTURE if cid.startswith("SCN-NVD-") else VALID_SYNTHETIC_FIXTURE)
            template["scenario_id"] = cid
            dst.write_text(json.dumps(template), encoding="utf-8")

    report = verifier.verify_all_traces(traces_tmp)

    assert report.canonical_expected == 30
    assert report.canonical_found == 29
    assert report.failed_scenarios >= 1
    assert report.overall_status == "FAIL"

    missing_failures = [f for f in report.failures if f["check_name"] == "canonical_trace_missing"]
    assert len(missing_failures) >= 1
    assert missing_failures[0]["scenario_id"] == omitted_id
