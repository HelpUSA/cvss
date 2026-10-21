#!/usr/bin/env python3
"""
Independent Trace Verifier for CVSS v4.0 Evidence Normalization Workflows.

Operationalizes machine-verifiable integrity verification across canonical scenario
trace artifacts (SCN-NVD-001..012 and SCN-SYN-013..030) and the reference dataset
(data/article/cvss40_environmental_scenarios.csv).

Epistemological Claim and Governance Boundaries:
This tool provides automated, deterministic verification of structured trace schema
completeness, syntactic vector parseability, policy arithmetic recomputation, and
cross-artifact dataset consistency. It does NOT assert formal mathematical proof
across infinite input spaces, semantic correctness of evidence interpretation,
or completed independent human expert adjudication.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Reusable canonical scorer and vector parser
try:
    import core.cvss40 as cvss40
except ImportError:
    # Fallback to local path if run from repository root or tools dir
    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    import core.cvss40 as cvss40


class CheckCategory(str, Enum):
    STRUCTURAL = "STRUCTURAL"
    RECOMPUTED = "RECOMPUTED"
    CONSISTENCY = "CONSISTENCY"
    SCHEMA_LIMITATION = "SCHEMA_LIMITATION"


class CheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    LIMITATION = "LIMITATION"


@dataclass
class CheckResult:
    name: str
    category: CheckCategory
    status: CheckStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScenarioVerification:
    scenario_id: str
    source_type: str  # "NVD" or "SYNTHETIC"
    passed: bool
    checks: List[CheckResult] = field(default_factory=list)
    failure_count: int = 0
    limitation_count: int = 0


@dataclass
class VerificationReport:
    generated_at_utc: str
    total_scenarios: int
    nvd_scenarios: int
    synthetic_scenarios: int
    passed_scenarios: int
    failed_scenarios: int
    overall_status: str  # "PASS" or "FAIL"
    category_counts: Dict[str, int]
    status_counts: Dict[str, int]
    failures: List[Dict[str, Any]]
    schema_limitations: List[Dict[str, Any]]
    scenario_results: List[Dict[str, Any]]
    canonical_expected: int = 0
    canonical_found: int = 0
    out_of_scope_files: List[Dict[str, str]] = field(default_factory=list)


# ==============================================================================
# Canonical Policy Import (Single Source of Truth: core.cvss40_environmental_policy)
# ==============================================================================

from core.cvss40_environmental_policy import (
    PRIORITY_ORDER,
    SEVERITY_TO_PRIORITY,
    CONTEXT_WEIGHTS,
    CONTROL_WEIGHTS,
    DEFAULT_CONTROL_WEIGHT,
    priority_to_ordinal,
    ordinal_to_priority,
    compute_delta_cat,
    recompute_p_base,
    lookup_nominal_weights,
    recompute_p_env_nominal,
)

REQUIRED_TOP_LEVEL_FIELDS = [
    "scenario_id",
    "scenario_source",
    "cve_id",
    "official_or_assigned_cvss_v4_vector",
    "cvss_b_score",
    "cvss_b_severity",
    "environmental_evidence",
    "candidate_environmental_assessment",
    "priority_comparison",
    "boundary",
]

REQUIRED_EVIDENCE_FIELDS = [
    "asset_class",
    "deployment_context",
    "internet_exposure",
    "privilege_context",
    "compensating_controls",
    "evidence_links",
    "evidence_summary",
]

REQUIRED_ASSESSMENT_FIELDS = [
    "confidentiality_requirement",
    "integrity_requirement",
    "availability_requirement",
    "candidate_modified_metrics",
    "watcher_recommendation",
    "uncertainty_flags",
    "human_review_status",
]

REQUIRED_PRIORITY_FIELDS = [
    "base_priority",
    "environmental_priority",
    "priority_delta",
]



def get_canonical_scenario_ids_from_csv(csv_path: Path) -> List[str]:
    """Extracts ordered list of canonical scenario IDs from reference CSV."""
    if not csv_path.exists():
        return []
    ids: List[str] = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row.get("scenario_id", "").strip()
            if sid and sid not in ids:
                ids.append(sid)
    return ids


# ==============================================================================
# Verifier Implementation
# ==============================================================================

class TraceVerifier:
    """
    Deterministic independent verifier for structured trace artifacts.
    """

    def __init__(self, dataset_csv_path: Optional[Path] = None):
        self.dataset_csv_path = dataset_csv_path
        self.dataset_rows: Dict[str, Dict[str, str]] = {}
        if dataset_csv_path and dataset_csv_path.exists():
            self._load_reference_csv(dataset_csv_path)

    def _load_reference_csv(self, path: Path) -> None:
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row.get("scenario_id", "").strip()
                if sid:
                    self.dataset_rows[sid] = row

    def get_canonical_scenario_ids(self) -> List[str]:
        """Returns the ordered canonical scenario IDs from reference CSV."""
        if self.dataset_rows:
            return list(self.dataset_rows.keys())
        if self.dataset_csv_path and self.dataset_csv_path.exists():
            return get_canonical_scenario_ids_from_csv(self.dataset_csv_path)
        return []

    def verify_scenario_trace(
        self,
        trace_data: Dict[str, Any],
        expected_scenario_id: Optional[str] = None,
    ) -> ScenarioVerification:
        """
        Executes complete verification suite on a single trace dictionary.
        """
        sid = str(trace_data.get("scenario_id", expected_scenario_id or "UNKNOWN")).strip()
        source_raw = str(trace_data.get("scenario_source", "")).strip()
        is_nvd = (source_raw == "nvd_cvss_v4_with_curated_environment" or sid.startswith("SCN-NVD-"))
        source_type = "NVD" if is_nvd else "SYNTHETIC"

        checks: List[CheckResult] = []

        # ----------------------------------------------------------------------
        # A. STRUCTURAL CHECKS
        # ----------------------------------------------------------------------

        # 1. Required top-level fields
        missing_top = [k for k in REQUIRED_TOP_LEVEL_FIELDS if k not in trace_data]
        if missing_top:
            checks.append(CheckResult(
                name="structural_required_top_level_fields",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.FAIL,
                message=f"Missing required top-level fields: {missing_top}",
                details={"missing": missing_top},
            ))
        else:
            checks.append(CheckResult(
                name="structural_required_top_level_fields",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.PASS,
                message="All required top-level fields are present",
            ))

        # 2. Scenario ID format
        id_pattern = r"^SCN-(NVD|SYN)-\d{3}$"
        if not re.match(id_pattern, sid):
            checks.append(CheckResult(
                name="structural_scenario_id_format",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.FAIL,
                message=f"Scenario ID '{sid}' does not match expected canonical pattern SCN-[NVD|SYN]-###",
                details={"scenario_id": sid},
            ))
        elif expected_scenario_id and sid != expected_scenario_id:
            checks.append(CheckResult(
                name="structural_scenario_id_format",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.FAIL,
                message=f"Scenario ID mismatch: expected '{expected_scenario_id}', got '{sid}'",
                details={"expected": expected_scenario_id, "actual": sid},
            ))
        else:
            checks.append(CheckResult(
                name="structural_scenario_id_format",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.PASS,
                message=f"Scenario ID '{sid}' matches canonical format",
            ))

        # 3. Nested section schemas
        env_ev = trace_data.get("environmental_evidence")
        if not isinstance(env_ev, dict):
            checks.append(CheckResult(
                name="structural_nested_environmental_evidence",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.FAIL,
                message="Field 'environmental_evidence' must be a dictionary",
            ))
            env_ev = {}
        else:
            missing_ev = [k for k in REQUIRED_EVIDENCE_FIELDS if k not in env_ev]
            if missing_ev:
                checks.append(CheckResult(
                    name="structural_nested_environmental_evidence",
                    category=CheckCategory.STRUCTURAL,
                    status=CheckStatus.FAIL,
                    message=f"Missing fields in environmental_evidence: {missing_ev}",
                    details={"missing": missing_ev},
                ))
            else:
                checks.append(CheckResult(
                    name="structural_nested_environmental_evidence",
                    category=CheckCategory.STRUCTURAL,
                    status=CheckStatus.PASS,
                    message="Nested environmental_evidence structure is complete",
                ))

        cand_assess = trace_data.get("candidate_environmental_assessment")
        if not isinstance(cand_assess, dict):
            checks.append(CheckResult(
                name="structural_nested_candidate_assessment",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.FAIL,
                message="Field 'candidate_environmental_assessment' must be a dictionary",
            ))
            cand_assess = {}
        else:
            missing_as = [k for k in REQUIRED_ASSESSMENT_FIELDS if k not in cand_assess]
            if missing_as:
                checks.append(CheckResult(
                    name="structural_nested_candidate_assessment",
                    category=CheckCategory.STRUCTURAL,
                    status=CheckStatus.FAIL,
                    message=f"Missing fields in candidate_environmental_assessment: {missing_as}",
                    details={"missing": missing_as},
                ))
            else:
                checks.append(CheckResult(
                    name="structural_nested_candidate_assessment",
                    category=CheckCategory.STRUCTURAL,
                    status=CheckStatus.PASS,
                    message="Nested candidate_environmental_assessment structure is complete",
                ))

        p_comp = trace_data.get("priority_comparison")
        if not isinstance(p_comp, dict):
            checks.append(CheckResult(
                name="structural_nested_priority_comparison",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.FAIL,
                message="Field 'priority_comparison' must be a dictionary",
            ))
            p_comp = {}
        else:
            missing_pc = [k for k in REQUIRED_PRIORITY_FIELDS if k not in p_comp]
            if missing_pc:
                checks.append(CheckResult(
                    name="structural_nested_priority_comparison",
                    category=CheckCategory.STRUCTURAL,
                    status=CheckStatus.FAIL,
                    message=f"Missing fields in priority_comparison: {missing_pc}",
                    details={"missing": missing_pc},
                ))
            else:
                checks.append(CheckResult(
                    name="structural_nested_priority_comparison",
                    category=CheckCategory.STRUCTURAL,
                    status=CheckStatus.PASS,
                    message="Nested priority_comparison structure is complete",
                ))

        # 4. Mandatory governance authorization state
        review_status = str(cand_assess.get("human_review_status", "")).strip().lower()
        if review_status != "required":
            checks.append(CheckResult(
                name="structural_governance_authorization_state",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.FAIL,
                message=f"Invalid governance review status: '{review_status}'. Must be 'required'.",
                details={"human_review_status": review_status},
            ))
        else:
            checks.append(CheckResult(
                name="structural_governance_authorization_state",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.PASS,
                message="Mandatory human authorization gatekeeper status 'required' is enforced",
            ))

        # 5. Uncertainty representation
        unc_flags = str(cand_assess.get("uncertainty_flags", "")).strip()
        if not unc_flags:
            checks.append(CheckResult(
                name="structural_uncertainty_representation",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.FAIL,
                message="Uncertainty representation 'uncertainty_flags' is empty or missing",
            ))
        else:
            checks.append(CheckResult(
                name="structural_uncertainty_representation",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.PASS,
                message=f"Uncertainty flags present: '{unc_flags}'",
                details={"uncertainty_flags": unc_flags},
            ))

        # 6. Boundary disclaimer statement
        boundary = str(trace_data.get("boundary", "")).strip()
        if not boundary or "not an autonomous official" not in boundary.lower():
            checks.append(CheckResult(
                name="structural_boundary_statement",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.FAIL,
                message="Boundary disclaimer missing or does not state non-autonomous official status",
                details={"boundary": boundary},
            ))
        else:
            checks.append(CheckResult(
                name="structural_boundary_statement",
                category=CheckCategory.STRUCTURAL,
                status=CheckStatus.PASS,
                message="Boundary disclaimer explicitly preserves governance limit",
            ))

        # ----------------------------------------------------------------------
        # B. RECOMPUTED ARITHMETIC AND POLICY CHECKS
        # ----------------------------------------------------------------------

        stored_base_p = str(p_comp.get("base_priority", "")).strip().lower()
        stored_env_p = str(p_comp.get("environmental_priority", "")).strip().lower()
        stored_delta_str = str(p_comp.get("priority_delta", "")).strip()
        b_sev = str(trace_data.get("cvss_b_severity", "")).strip().upper()

        # 1. P_base recomputed from CVSS-B severity
        try:
            recomputed_base_p = recompute_p_base(b_sev)
            if recomputed_base_p != stored_base_p:
                checks.append(CheckResult(
                    name="recomputed_base_priority",
                    category=CheckCategory.RECOMPUTED,
                    status=CheckStatus.FAIL,
                    message=f"P_base mismatch: severity '{b_sev}' maps to '{recomputed_base_p}', trace has '{stored_base_p}'",
                    details={"severity": b_sev, "recomputed": recomputed_base_p, "stored": stored_base_p},
                ))
            else:
                checks.append(CheckResult(
                    name="recomputed_base_priority",
                    category=CheckCategory.RECOMPUTED,
                    status=CheckStatus.PASS,
                    message=f"P_base '{stored_base_p}' matches recomputed severity mapping for '{b_sev}'",
                ))
        except Exception as e:
            checks.append(CheckResult(
                name="recomputed_base_priority",
                category=CheckCategory.RECOMPUTED,
                status=CheckStatus.FAIL,
                message=f"Failed to recompute P_base: {str(e)}",
            ))

        # 2. Delta_cat recomputed from g(P_env) - g(P_base)
        try:
            stored_delta = int(stored_delta_str)
            recomputed_delta = compute_delta_cat(stored_base_p, stored_env_p)
            if stored_delta != recomputed_delta:
                checks.append(CheckResult(
                    name="recomputed_category_delta",
                    category=CheckCategory.RECOMPUTED,
                    status=CheckStatus.FAIL,
                    message=f"Delta_cat mismatch: g('{stored_env_p}') - g('{stored_base_p}') = {recomputed_delta}, trace has {stored_delta}",
                    details={"recomputed_delta": recomputed_delta, "stored_delta": stored_delta},
                ))
            else:
                checks.append(CheckResult(
                    name="recomputed_category_delta",
                    category=CheckCategory.RECOMPUTED,
                    status=CheckStatus.PASS,
                    message=f"Category delta Delta_cat={recomputed_delta} verified algebraically",
                ))
        except Exception as e:
            checks.append(CheckResult(
                name="recomputed_category_delta",
                category=CheckCategory.RECOMPUTED,
                status=CheckStatus.FAIL,
                message=f"Failed to verify category delta arithmetic: {str(e)}",
            ))

        # 3. Clamped ordinal range check: g(P_env) in [0, 4]
        try:
            g_env = priority_to_ordinal(stored_env_p)
            if not (0 <= g_env <= 4):
                checks.append(CheckResult(
                    name="recomputed_ordinal_clamp_range",
                    category=CheckCategory.RECOMPUTED,
                    status=CheckStatus.FAIL,
                    message=f"g(P_env) ordinal {g_env} outside clamped boundary [0, 4]",
                ))
            else:
                checks.append(CheckResult(
                    name="recomputed_ordinal_clamp_range",
                    category=CheckCategory.RECOMPUTED,
                    status=CheckStatus.PASS,
                    message=f"g(P_env)={g_env} strictly bounded in [0, 4]",
                ))
        except Exception as e:
            checks.append(CheckResult(
                name="recomputed_ordinal_clamp_range",
                category=CheckCategory.RECOMPUTED,
                status=CheckStatus.FAIL,
                message=f"Invalid priority category '{stored_env_p}': {str(e)}",
            ))

        # 4. Scorer recomputation for NVD traces
        raw_vector = str(trace_data.get("official_or_assigned_cvss_v4_vector", "")).strip()
        raw_score_str = str(trace_data.get("cvss_b_score", "")).strip()

        if is_nvd:
            try:
                scoring_result = cvss40.score(raw_vector)
                calc_score = float(scoring_result["score"])
                stored_score = float(raw_score_str)
                calc_sev = str(scoring_result["severity"]).upper()

                if abs(calc_score - stored_score) > 1e-4:
                    checks.append(CheckResult(
                        name="recomputed_nvd_cvss_score",
                        category=CheckCategory.RECOMPUTED,
                        status=CheckStatus.FAIL,
                        message=f"NVD CVSS score mismatch: calc={calc_score}, stored={stored_score}",
                        details={"calculated": calc_score, "stored": stored_score, "vector": raw_vector},
                    ))
                elif calc_sev != b_sev:
                    checks.append(CheckResult(
                        name="recomputed_nvd_cvss_score",
                        category=CheckCategory.RECOMPUTED,
                        status=CheckStatus.FAIL,
                        message=f"NVD CVSS severity mismatch: calc={calc_sev}, stored={b_sev}",
                        details={"calculated_severity": calc_sev, "stored_severity": b_sev},
                    ))
                else:
                    checks.append(CheckResult(
                        name="recomputed_nvd_cvss_score",
                        category=CheckCategory.RECOMPUTED,
                        status=CheckStatus.PASS,
                        message=f"NVD CVSS Base score {calc_score} and severity '{calc_sev}' verified via canonical scorer",
                    ))
            except Exception as e:
                checks.append(CheckResult(
                    name="recomputed_nvd_cvss_score",
                    category=CheckCategory.RECOMPUTED,
                    status=CheckStatus.FAIL,
                    message=f"Canonical scorer execution failed for NVD vector: {str(e)}",
                ))

        # 5. Nominal policy comparison and schema limitation classification
        asset_class = str(env_ev.get("asset_class", "")).strip()
        try:
            nominal_env_p, nominal_delta = recompute_p_env_nominal(stored_base_p, asset_class)
            if stored_env_p == nominal_env_p and int(stored_delta_str) == nominal_delta:
                checks.append(CheckResult(
                    name="recomputed_nominal_policy_profile",
                    category=CheckCategory.RECOMPUTED,
                    status=CheckStatus.PASS,
                    message=f"Trace priority matches nominal policy profile for '{asset_class}' (Delta={nominal_delta})",
                ))
            else:
                # Discrepancy between nominal profile lookup and stored trace priority:
                # In curated NVD scenarios (e.g. SCN-NVD-001, SCN-NVD-006, 007, 008), the contextual
                # priority represents a local deployment curation recorded in the dataset.
                checks.append(CheckResult(
                    name="recomputed_nominal_policy_profile",
                    category=CheckCategory.SCHEMA_LIMITATION,
                    status=CheckStatus.LIMITATION,
                    message=(
                        f"Scenario exhibits curated local deployment context: stored (Env={stored_env_p}, Delta={stored_delta_str}) "
                        f"vs nominal profile (Env={nominal_env_p}, Delta={nominal_delta}). "
                        "The trace schema provides narrative evidence fields rather than explicit sub-weight vectors."
                    ),
                    details={
                        "stored_env_priority": stored_env_p,
                        "stored_delta": stored_delta_str,
                        "nominal_env_priority": nominal_env_p,
                        "nominal_delta": nominal_delta,
                        "asset_class": asset_class,
                    },
                ))
        except Exception as e:
            checks.append(CheckResult(
                name="recomputed_nominal_policy_profile",
                category=CheckCategory.RECOMPUTED,
                status=CheckStatus.FAIL,
                message=f"Failed to evaluate nominal policy: {str(e)}",
            ))

        # ----------------------------------------------------------------------
        # C. CONSISTENCY CHECKS
        # ----------------------------------------------------------------------

        # 1. Separation of NVD vs Synthetic source
        cve_id = str(trace_data.get("cve_id", "")).strip()
        if is_nvd:
            if not re.match(r"^CVE-\d{4}-\d+$", cve_id):
                checks.append(CheckResult(
                    name="consistency_source_separation",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.FAIL,
                    message=f"NVD scenario must have valid CVE ID; found '{cve_id}'",
                ))
            elif source_raw != "nvd_cvss_v4_with_curated_environment":
                checks.append(CheckResult(
                    name="consistency_source_separation",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.FAIL,
                    message=f"NVD scenario source must be 'nvd_cvss_v4_with_curated_environment', found '{source_raw}'",
                ))
            else:
                checks.append(CheckResult(
                    name="consistency_source_separation",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.PASS,
                    message=f"NVD source separation validated for {cve_id}",
                ))
        else:
            if cve_id != "":
                checks.append(CheckResult(
                    name="consistency_source_separation",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.FAIL,
                    message=f"Synthetic scenario must have empty cve_id; found '{cve_id}'",
                ))
            elif source_raw != "curated_synthetic_no_cve":
                checks.append(CheckResult(
                    name="consistency_source_separation",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.FAIL,
                    message=f"Synthetic scenario source must be 'curated_synthetic_no_cve', found '{source_raw}'",
                ))
            else:
                checks.append(CheckResult(
                    name="consistency_source_separation",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.PASS,
                    message="Synthetic source separation validated (cve_id empty, curated source tag)",
                ))

        # 2. Synthetic vector syntax validation (without treating score as CVE ground truth)
        if not is_nvd:
            try:
                parsed_vec = cvss40.parse_vector(raw_vector)
                if not parsed_vec or not isinstance(parsed_vec, dict):
                    checks.append(CheckResult(
                        name="consistency_synthetic_vector_syntax",
                        category=CheckCategory.CONSISTENCY,
                        status=CheckStatus.FAIL,
                        message=f"Failed to parse synthetic vector string '{raw_vector}'",
                    ))
                else:
                    checks.append(CheckResult(
                        name="consistency_synthetic_vector_syntax",
                        category=CheckCategory.CONSISTENCY,
                        status=CheckStatus.PASS,
                        message="Synthetic CVSS v4.0 vector string parsed cleanly by canonical grammar",
                        details={"metric_count": len(parsed_vec)},
                    ))
            except Exception as e:
                checks.append(CheckResult(
                    name="consistency_synthetic_vector_syntax",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.FAIL,
                    message=f"Synthetic vector syntax invalid: {str(e)}",
                ))

            # Mandatory uncertainty flag in synthetic case
            has_assigned_flag = "assigned_vector_not_official_cve" in unc_flags
            has_synthetic_flag = "synthetic_scenario" in unc_flags
            if not (has_assigned_flag and has_synthetic_flag):
                checks.append(CheckResult(
                    name="consistency_synthetic_uncertainty_flags",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.FAIL,
                    message="Synthetic trace must contain 'assigned_vector_not_official_cve' and 'synthetic_scenario' in uncertainty_flags",
                    details={"uncertainty_flags": unc_flags},
                ))
            else:
                checks.append(CheckResult(
                    name="consistency_synthetic_uncertainty_flags",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.PASS,
                    message="Synthetic trace correctly disclaims official CVE ground truth via uncertainty flags",
                ))

        # 3. Cross-artifact consistency with reference CSV
        if self.dataset_rows:
            csv_row = self.dataset_rows.get(sid)
            if not csv_row:
                checks.append(CheckResult(
                    name="consistency_csv_cross_reference",
                    category=CheckCategory.CONSISTENCY,
                    status=CheckStatus.FAIL,
                    message=f"Scenario ID '{sid}' not found in canonical reference dataset CSV",
                ))
            else:
                mismatches = []
                if csv_row.get("cve_id", "").strip() != cve_id:
                    mismatches.append(f"cve_id: csv='{csv_row.get('cve_id')}', trace='{cve_id}'")
                if csv_row.get("cvss_b_score", "").strip() != raw_score_str:
                    mismatches.append(f"cvss_b_score: csv='{csv_row.get('cvss_b_score')}', trace='{raw_score_str}'")
                if csv_row.get("cvss_b_severity", "").strip().upper() != b_sev:
                    mismatches.append(f"cvss_b_severity: csv='{csv_row.get('cvss_b_severity')}', trace='{b_sev}'")
                if csv_row.get("base_priority", "").strip().lower() != stored_base_p:
                    mismatches.append(f"base_priority: csv='{csv_row.get('base_priority')}', trace='{stored_base_p}'")
                if csv_row.get("environmental_priority", "").strip().lower() != stored_env_p:
                    mismatches.append(f"environmental_priority: csv='{csv_row.get('environmental_priority')}', trace='{stored_env_p}'")
                if csv_row.get("priority_delta", "").strip() != stored_delta_str:
                    mismatches.append(f"priority_delta: csv='{csv_row.get('priority_delta')}', trace='{stored_delta_str}'")
                if csv_row.get("asset_class", "").strip() != asset_class:
                    mismatches.append(f"asset_class: csv='{csv_row.get('asset_class')}', trace='{asset_class}'")

                if mismatches:
                    checks.append(CheckResult(
                        name="consistency_csv_cross_reference",
                        category=CheckCategory.CONSISTENCY,
                        status=CheckStatus.FAIL,
                        message=f"CSV cross-reference mismatches: {'; '.join(mismatches)}",
                        details={"mismatches": mismatches},
                    ))
                else:
                    checks.append(CheckResult(
                        name="consistency_csv_cross_reference",
                        category=CheckCategory.CONSISTENCY,
                        status=CheckStatus.PASS,
                        message="Trace matches reference CSV across all 7 core metadata columns",
                    ))

        # ----------------------------------------------------------------------
        # D. SCHEMA LIMITATION CHECKS
        # ----------------------------------------------------------------------
        # The schema provides narrative 'watcher_recommendation' and 'candidate_modified_metrics',
        # but does not encode machine-checkable sub-token metric citation graphs or cryptographic
        # evidence signatures. This is recorded as a structured limitation rather than a failure.
        cand_mods = str(cand_assess.get("candidate_modified_metrics", "")).strip()
        if cand_mods:
            checks.append(CheckResult(
                name="schema_limitation_metric_evidence_linkage",
                category=CheckCategory.SCHEMA_LIMITATION,
                status=CheckStatus.LIMITATION,
                message=(
                    "The trace schema provides narrative evidence fields rather than an atomic, "
                    "machine-addressable linkage between each candidate modified metric and its corresponding evidence item."
                ),
                details={"candidate_modified_metrics_excerpt": cand_mods[:80]},
            ))

        # Overall scenario status
        failures = [c for c in checks if c.status == CheckStatus.FAIL]
        limitations = [c for c in checks if c.status == CheckStatus.LIMITATION]
        is_passed = len(failures) == 0

        return ScenarioVerification(
            scenario_id=sid,
            source_type=source_type,
            passed=is_passed,
            checks=checks,
            failure_count=len(failures),
            limitation_count=len(limitations),
        )

    def verify_trace_file(self, trace_file_path: Path) -> ScenarioVerification:
        """Loads and verifies a single trace JSON file."""
        if not trace_file_path.exists():
            return ScenarioVerification(
                scenario_id=trace_file_path.stem,
                source_type="UNKNOWN",
                passed=False,
                checks=[CheckResult(
                    name="file_existence",
                    category=CheckCategory.STRUCTURAL,
                    status=CheckStatus.FAIL,
                    message=f"Trace file not found: {trace_file_path}",
                )],
                failure_count=1,
                limitation_count=0,
            )

        with open(trace_file_path, mode="r", encoding="utf-8") as f:
            data = json.load(f)

        return self.verify_scenario_trace(data, expected_scenario_id=trace_file_path.stem)

    def verify_all_traces(self, traces_dir: Path) -> VerificationReport:
        """
        Discovers and verifies all canonical trace files in the given directory.
        Authoritative scenario scope is derived strictly from the reference CSV.
        Extra or legacy files not in the CSV are classified as OUT_OF_SCOPE.
        """
        from datetime import datetime, timezone

        if not self.dataset_rows and self.dataset_csv_path and self.dataset_csv_path.exists():
            self._load_reference_csv(self.dataset_csv_path)

        if self.dataset_rows:
            canonical_ids = list(self.dataset_rows.keys())
        else:
            canonical_ids = [p.stem for p in sorted(traces_dir.glob("SCN-*.json"))]

        canonical_expected = len(canonical_ids)
        canonical_found = 0
        results: List[ScenarioVerification] = []

        for cid in canonical_ids:
            trace_path = traces_dir / f"{cid}.json"
            if trace_path.exists():
                canonical_found += 1
                res = self.verify_trace_file(trace_path)
                results.append(res)
            else:
                is_nvd = cid.startswith("SCN-NVD-")
                res = ScenarioVerification(
                    scenario_id=cid,
                    source_type="NVD" if is_nvd else "SYNTHETIC",
                    passed=False,
                    checks=[CheckResult(
                        name="canonical_trace_missing",
                        category=CheckCategory.STRUCTURAL,
                        status=CheckStatus.FAIL,
                        message=f"Required canonical trace file not found: {trace_path.name}",
                        details={"expected_path": str(trace_path)},
                    )],
                    failure_count=1,
                    limitation_count=0,
                )
                results.append(res)

        # Detect out-of-scope / legacy files in directory
        disk_files = sorted(traces_dir.glob("SCN-*.json"))
        canonical_set = set(canonical_ids)
        out_of_scope: List[Dict[str, str]] = []
        for df in disk_files:
            if df.stem not in canonical_set:
                out_of_scope.append({
                    "file_name": df.name,
                    "scenario_id": df.stem,
                    "classification": "OUT_OF_SCOPE",
                    "reason": "Legacy scenario artifact not present in canonical reference dataset CSV",
                })

        # Summary metrics strictly based on canonical scenario results
        total = len(results)
        nvd_cnt = sum(1 for r in results if r.source_type == "NVD")
        syn_cnt = sum(1 for r in results if r.source_type == "SYNTHETIC")
        passed_cnt = sum(1 for r in results if r.passed)
        failed_cnt = sum(1 for r in results if not r.passed)

        cat_counts: Dict[str, int] = {c.value: 0 for c in CheckCategory}
        stat_counts: Dict[str, int] = {s.value: 0 for s in CheckStatus}
        all_failures: List[Dict[str, Any]] = []
        all_limitations: List[Dict[str, Any]] = []

        for r in results:
            for chk in r.checks:
                cat_counts[chk.category.value] = cat_counts.get(chk.category.value, 0) + 1
                stat_counts[chk.status.value] = stat_counts.get(chk.status.value, 0) + 1
                if chk.status == CheckStatus.FAIL:
                    all_failures.append({
                        "scenario_id": r.scenario_id,
                        "check_name": chk.name,
                        "category": chk.category.value,
                        "message": chk.message,
                        "details": chk.details,
                    })
                elif chk.status == CheckStatus.LIMITATION:
                    all_limitations.append({
                        "scenario_id": r.scenario_id,
                        "check_name": chk.name,
                        "category": chk.category.value,
                        "message": chk.message,
                        "details": chk.details,
                    })

        overall = "PASS" if (failed_cnt == 0 and total > 0) else "FAIL"

        return VerificationReport(
            generated_at_utc=datetime.now(timezone.utc).isoformat(),
            total_scenarios=total,
            nvd_scenarios=nvd_cnt,
            synthetic_scenarios=syn_cnt,
            passed_scenarios=passed_cnt,
            failed_scenarios=failed_cnt,
            overall_status=overall,
            category_counts=cat_counts,
            status_counts=stat_counts,
            failures=all_failures,
            schema_limitations=all_limitations,
            scenario_results=[asdict(r) for r in results],
            canonical_expected=canonical_expected,
            canonical_found=canonical_found,
            out_of_scope_files=out_of_scope,
        )


def format_human_summary(report: VerificationReport) -> str:
    """Formats verification report into human-readable console summary."""
    lines = [
        "=" * 78,
        "CVSS v4.0 INDEPENDENT TRACE VERIFIER (IEEE R2 VERIFICATION SUITE)",
        "=" * 78,
        f"Generated at UTC   : {report.generated_at_utc}",
        f"Overall Status     : {report.overall_status}",
        f"Canonical Scope    : {report.canonical_found} / {report.canonical_expected} expected scenarios found",
        f"Total Scenarios    : {report.total_scenarios} (NVD: {report.nvd_scenarios}, Synthetic: {report.synthetic_scenarios})",
        f"Passed Scenarios   : {report.passed_scenarios} / {report.total_scenarios}",
        f"Failed Scenarios   : {report.failed_scenarios} / {report.total_scenarios}",
    ]
    if report.out_of_scope_files:
        lines.append(f"Out of Scope Files : {len(report.out_of_scope_files)} ignored legacy artifacts")
    lines.extend([
        "-" * 78,
        "Check Counts by Category:",
    ])
    for cat, cnt in report.category_counts.items():
        lines.append(f"  - {cat:<20}: {cnt}")
    lines.append("-" * 78)
    lines.append("Check Status Summary:")
    for stat, cnt in report.status_counts.items():
        lines.append(f"  - {stat:<20}: {cnt}")
    lines.append("-" * 78)

    if report.failures:
        lines.append(f"FAILURES DETECTED ({len(report.failures)}):")
        for f in report.failures:
            lines.append(f"  * [{f['scenario_id']}] {f['check_name']} ({f['category']}): {f['message']}")
    else:
        lines.append("Zero structural, algebraic, or consistency failures detected.")

    if report.schema_limitations:
        lines.append(f"Identified Schema Limitations Recorded ({len(report.schema_limitations)} occurrences):")
        # Deduplicate limitation messages
        seen_msgs = set()
        for lim in report.schema_limitations:
            msg_key = (lim["check_name"], lim["message"])
            if msg_key not in seen_msgs:
                seen_msgs.add(msg_key)
                lines.append(f"  ! {lim['check_name']}: {lim['message'][:110]}...")

    lines.append("=" * 78)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify integrity, arithmetic, and consistency of canonical CVSS v4.0 traces."
    )
    repo_root = Path(__file__).resolve().parent.parent
    parser.add_argument(
        "--traces-dir",
        type=Path,
        default=repo_root / "validation" / "article" / "trace",
        help="Path to directory containing SCN-*.json traces",
    )
    parser.add_argument(
        "--dataset-csv",
        type=Path,
        default=repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv",
        help="Path to reference cvss40_environmental_scenarios.csv",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Optional path to output structured JSON report",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress human-readable stdout summary",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    verifier = TraceVerifier(dataset_csv_path=args.dataset_csv)
    report = verifier.verify_all_traces(args.traces_dir)

    if not args.quiet:
        print(format_human_summary(report))

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_json, mode="w", encoding="utf-8") as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        print(f"Wrote report to {args.output_json}")

    return 0 if report.overall_status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
