#!/usr/bin/env python3
"""
article_cvss40_r2_trace_mutation_test.py - Empirical Mutation Testing for Trace Verifier.

IEEE Double-Blind Peer Review (Revision R2) Empirical Sensitivity Suite.
Evaluates the error detection sensitivity of tools.verify_trace_integrity.TraceVerifier
against controlled, deterministic mutation injections (M1-M8).

Epistemological Boundary:
Empirical mutation testing provides descriptive evidence that injected trace violations
are detected and rejected within the evaluated mutation set. It does NOT constitute
formal verification, proof of completeness, semantic correctness, or exhaustive coverage.
All mutations are strictly generated in-memory on deep copies. Canonical trace files on disk
are NEVER modified or overwritten.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

# Reusable canonical verifier and policy
try:
    import tools.verify_trace_integrity as vti
except ImportError:
    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    import tools.verify_trace_integrity as vti


# ==============================================================================
# Mutation Operator Definitions and Metadata
# ==============================================================================

class MutationOperatorId(str, Enum):
    M1 = "M1_remove_required_field"
    M2 = "M2_delta_cat_mismatch"
    M3 = "M3_invalid_vector_syntax"
    M4 = "M4_nvd_score_mismatch"
    M5 = "M5_remove_synthetic_uncertainty_flag"
    M6 = "M6_invalid_review_state"
    M7 = "M7_source_provenance_mismatch"
    M8 = "M8_canonical_dataset_mismatch"


@dataclass(frozen=True)
class MutationOperatorDef:
    operator_id: MutationOperatorId
    name: str
    description: str
    applicable_sources: Tuple[str, ...]  # ("NVD", "SYNTHETIC") or subset
    expected_check_name: str
    target_category: str


MUTATION_OPERATOR_REGISTRY: Dict[MutationOperatorId, MutationOperatorDef] = {
    MutationOperatorId.M1: MutationOperatorDef(
        operator_id=MutationOperatorId.M1,
        name="remove_required_field",
        description="Removes a mandatory top-level structural field (boundary) from the trace.",
        applicable_sources=("NVD", "SYNTHETIC"),
        expected_check_name="structural_required_top_level_fields",
        target_category="STRUCTURAL",
    ),
    MutationOperatorId.M2: MutationOperatorDef(
        operator_id=MutationOperatorId.M2,
        name="delta_cat_mismatch",
        description="Corrupts stored category_delta to an algebraically invalid value (+4).",
        applicable_sources=("NVD", "SYNTHETIC"),
        expected_check_name="recomputed_category_delta",
        target_category="RECOMPUTED",
    ),
    MutationOperatorId.M3: MutationOperatorDef(
        operator_id=MutationOperatorId.M3,
        name="invalid_vector_syntax",
        description="Corrupts CVSS v4.0 vector string with invalid metric value (AV:INVALID).",
        applicable_sources=("NVD", "SYNTHETIC"),
        expected_check_name="recomputed_nvd_cvss_score",  # for NVD; consistency_synthetic_vector_syntax for SYN
        target_category="RECOMPUTED_OR_CONSISTENCY",
    ),
    MutationOperatorId.M4: MutationOperatorDef(
        operator_id=MutationOperatorId.M4,
        name="nvd_score_mismatch",
        description="Alters stored Base score in NVD trace (9.9) while keeping vector intact.",
        applicable_sources=("NVD",),
        expected_check_name="recomputed_nvd_cvss_score",
        target_category="RECOMPUTED",
    ),
    MutationOperatorId.M5: MutationOperatorDef(
        operator_id=MutationOperatorId.M5,
        name="remove_synthetic_uncertainty_flag",
        description="Clears uncertainty_flags representation from candidate environmental assessment.",
        applicable_sources=("SYNTHETIC",),
        expected_check_name="structural_uncertainty_representation",
        target_category="STRUCTURAL",
    ),
    MutationOperatorId.M6: MutationOperatorDef(
        operator_id=MutationOperatorId.M6,
        name="invalid_review_state",
        description="Alters human_review_status from 'required' to forbidden bypass state 'bypassed'.",
        applicable_sources=("NVD", "SYNTHETIC"),
        expected_check_name="structural_governance_authorization_state",
        target_category="STRUCTURAL",
    ),
    MutationOperatorId.M7: MutationOperatorDef(
        operator_id=MutationOperatorId.M7,
        name="source_provenance_mismatch",
        description="Contaminates source separation (assigns CVE ID to synthetic scenario or invalid source tag to NVD).",
        applicable_sources=("NVD", "SYNTHETIC"),
        expected_check_name="consistency_source_separation",
        target_category="CONSISTENCY",
    ),
    MutationOperatorId.M8: MutationOperatorDef(
        operator_id=MutationOperatorId.M8,
        name="canonical_dataset_mismatch",
        description="Alters trace metadata (cvss_b_severity) so it disagrees with the reference CSV row.",
        applicable_sources=("NVD", "SYNTHETIC"),
        expected_check_name="recomputed_base_priority",
        target_category="RECOMPUTED",
    ),
}


# ==============================================================================
# Representative Scenario Selection for Focused Mutation Campaign
# ==============================================================================

# Deterministic selection: 3 NVD (including curated override & nominal match) + 3 Synthetic
REPRESENTATIVE_SCENARIO_IDS: Tuple[str, ...] = (
    "SCN-NVD-001",  # NVD: Curated override (nominal medium vs observed low)
    "SCN-NVD-003",  # NVD: Nominal match (medium -> high)
    "SCN-NVD-007",  # NVD: Curated override (nominal critical vs observed medium)
    "SCN-SYN-013",  # Synthetic: Nominal match (high -> high)
    "SCN-SYN-020",  # Synthetic: Nominal match (medium -> medium)
    "SCN-SYN-028",  # Synthetic: Nominal match (critical -> critical)
)


# ==============================================================================
# Data Structures
# ==============================================================================

@dataclass
class MutationCase:
    mutant_id: str
    scenario_id: str
    source_type: str  # "NVD" or "SYNTHETIC"
    operator_id: str
    operator_name: str
    is_applicable: bool
    expected_check: str
    target_category: str
    mutation_description: str


@dataclass
class MutationResult:
    mutant_id: str
    scenario_id: str
    source_type: str
    operator_id: str
    is_applicable: bool
    detected: bool
    detected_by_expected_check: bool
    failing_check_names: List[str] = field(default_factory=list)
    failure_messages: List[str] = field(default_factory=list)
    execution_notes: str = ""


@dataclass
class MutationOperatorSummary:
    operator_id: str
    name: str
    total_cases: int
    applicable_cases: int
    not_applicable_cases: int
    detected_count: int
    detection_rate_applicable: float
    expected_check_match_count: int


@dataclass
class MutationCaseRecord:
    mutant_id: str
    scenario_id: str
    source_type: str
    operator_id: str
    operator_name: str
    is_applicable: bool
    expected_check: str
    target_category: str
    status: str  # "DETECTED", "MISSED", "UNEXPECTED", "NOT_APPLICABLE"
    detected: bool
    detected_by_expected_check: bool
    failing_checks: List[str] = field(default_factory=list)
    failure_messages: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class MutationCampaignReport:
    generated_at_utc: str
    total_mutants_planned: int
    applicable_mutants: int
    not_applicable_mutants: int
    detected_mutants: int
    overall_detection_rate: float
    operator_summaries: Dict[str, Dict[str, Any]]
    source_partition_summaries: Dict[str, Dict[str, Any]]
    results: List[Dict[str, Any]]
    campaign_integrity_status: str = "PASS"
    canonical_scenarios_selected: List[str] = field(default_factory=list)
    original_controls: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    all_original_controls_passed: bool = True
    trace_files_hash_verified_unmodified: bool = True
    missed_mutants: int = 0
    unexpected_mutants: int = 0
    epistemological_statement: str = (
        "Empirical mutation testing provides empirical evidence that injected trace violations "
        "are detected and rejected in the evaluated mutation set. "
        "It provides empirical sensitivity evidence and does NOT constitute formal verification, "
        "proof of semantic correctness, completeness guarantee, or exhaustive coverage."
    )


# ==============================================================================
# Pure Mutation Functions (Operate Strictly on In-Memory Dictionaries)
# ==============================================================================

def mutate_m1_remove_required_field(trace_dict: Dict[str, Any]) -> Dict[str, Any]:
    """M1: Removes top-level mandatory field 'boundary'."""
    mutant = copy.deepcopy(trace_dict)
    mutant.pop("boundary", None)
    return mutant


def mutate_m2_delta_cat_mismatch(trace_dict: Dict[str, Any]) -> Dict[str, Any]:
    """M2: Injects an inconsistent category delta into priority_comparison."""
    mutant = copy.deepcopy(trace_dict)
    p_comp = mutant.get("priority_comparison", {})
    if isinstance(p_comp, dict):
        p_comp = copy.deepcopy(p_comp)
        current_delta = int(p_comp.get("priority_delta", 0))
        # Alter delta by +3 or set to 4 (incompatible with any valid delta)
        p_comp["priority_delta"] = 4 if current_delta != 4 else -4
        mutant["priority_comparison"] = p_comp
    return mutant


def mutate_m3_invalid_vector_syntax(trace_dict: Dict[str, Any]) -> Dict[str, Any]:
    """M3: Corrupts the CVSS vector string syntax."""
    mutant = copy.deepcopy(trace_dict)
    raw_vec = str(mutant.get("official_or_assigned_cvss_v4_vector", "CVSS:4.0/AV:N/AC:L"))
    mutant["official_or_assigned_cvss_v4_vector"] = raw_vec.replace("AV:N", "AV:INVALID_VAL").replace("AV:A", "AV:INVALID_VAL").replace("AV:L", "AV:INVALID_VAL")
    if mutant["official_or_assigned_cvss_v4_vector"] == raw_vec:
        mutant["official_or_assigned_cvss_v4_vector"] = raw_vec + "/INVALID_METRIC:CORRUPT"
    return mutant


def mutate_m4_nvd_score_mismatch(trace_dict: Dict[str, Any]) -> Dict[str, Any]:
    """M4: Alters CVSS Base score in NVD trace without changing the vector."""
    mutant = copy.deepcopy(trace_dict)
    stored_score = float(mutant.get("cvss_b_score", 5.0))
    mutant["cvss_b_score"] = 9.9 if stored_score != 9.9 else 1.0
    return mutant


def mutate_m5_remove_synthetic_uncertainty_flag(trace_dict: Dict[str, Any]) -> Dict[str, Any]:
    """M5: Removes or blanks out uncertainty flags in candidate assessment."""
    mutant = copy.deepcopy(trace_dict)
    cand = mutant.get("candidate_environmental_assessment", {})
    if isinstance(cand, dict):
        cand = copy.deepcopy(cand)
        cand["uncertainty_flags"] = ""
        mutant["candidate_environmental_assessment"] = cand
    return mutant


def mutate_m6_invalid_review_state(trace_dict: Dict[str, Any]) -> Dict[str, Any]:
    """M6: Sets human_review_status to forbidden bypass value."""
    mutant = copy.deepcopy(trace_dict)
    cand = mutant.get("candidate_environmental_assessment", {})
    if isinstance(cand, dict):
        cand = copy.deepcopy(cand)
        cand["human_review_status"] = "bypassed_auto_approved"
        mutant["candidate_environmental_assessment"] = cand
    return mutant


def mutate_m7_source_provenance_mismatch(trace_dict: Dict[str, Any], is_nvd: bool) -> Dict[str, Any]:
    """M7: Contaminates source separation (adds CVE to synthetic, or corrupts NVD source tag)."""
    mutant = copy.deepcopy(trace_dict)
    if is_nvd:
        mutant["scenario_source"] = "corrupted_source_provenance"
    else:
        mutant["cve_id"] = "CVE-2026-99999"
    return mutant


def mutate_m8_canonical_dataset_mismatch(trace_dict: Dict[str, Any]) -> Dict[str, Any]:
    """M8: Inverts CVSS severity to create internal mismatch with Base priority."""
    mutant = copy.deepcopy(trace_dict)
    current_sev = str(mutant.get("cvss_b_severity", "")).upper()
    mutant["cvss_b_severity"] = "LOW" if current_sev != "LOW" else "CRITICAL"
    return mutant


# ==============================================================================
# Campaign Planning and Mutant Generator
# ==============================================================================

def apply_operator_to_trace(
    op_id: MutationOperatorId,
    trace_dict: Dict[str, Any],
    source_type: str,
) -> Tuple[Dict[str, Any], bool, str]:
    """
    Applies the mutation operator to an in-memory deep copy of trace_dict.
    Returns (mutated_trace_dict, is_applicable, expected_check_name).
    """
    op_def = MUTATION_OPERATOR_REGISTRY[op_id]
    if source_type not in op_def.applicable_sources:
        return copy.deepcopy(trace_dict), False, "NOT_APPLICABLE"

    expected_check = op_def.expected_check_name
    # Specific adjustment for M3 on synthetic scenarios
    if op_id == MutationOperatorId.M3 and source_type == "SYNTHETIC":
        expected_check = "consistency_synthetic_vector_syntax"

    if op_id == MutationOperatorId.M1:
        return mutate_m1_remove_required_field(trace_dict), True, expected_check
    elif op_id == MutationOperatorId.M2:
        return mutate_m2_delta_cat_mismatch(trace_dict), True, expected_check
    elif op_id == MutationOperatorId.M3:
        return mutate_m3_invalid_vector_syntax(trace_dict), True, expected_check
    elif op_id == MutationOperatorId.M4:
        return mutate_m4_nvd_score_mismatch(trace_dict), True, expected_check
    elif op_id == MutationOperatorId.M5:
        return mutate_m5_remove_synthetic_uncertainty_flag(trace_dict), True, expected_check
    elif op_id == MutationOperatorId.M6:
        return mutate_m6_invalid_review_state(trace_dict), True, expected_check
    elif op_id == MutationOperatorId.M7:
        is_nvd = (source_type == "NVD")
        return mutate_m7_source_provenance_mismatch(trace_dict, is_nvd), True, expected_check
    elif op_id == MutationOperatorId.M8:
        return mutate_m8_canonical_dataset_mismatch(trace_dict), True, expected_check
    else:
        raise ValueError(f"Unknown operator ID: {op_id}")


def build_deterministic_mutation_plan(
    scenario_ids: Sequence[str] = REPRESENTATIVE_SCENARIO_IDS,
) -> List[MutationCase]:
    """
    Constructs the deterministic plan of mutation test cases.
    For each selected scenario and each operator M1-M8, determines applicability
    and registers expected behavior without executing the verifier.
    """
    plan: List[MutationCase] = []

    for sid in scenario_ids:
        is_nvd = sid.startswith("SCN-NVD-")
        source_type = "NVD" if is_nvd else "SYNTHETIC"

        for op_id in MutationOperatorId:
            op_def = MUTATION_OPERATOR_REGISTRY[op_id]
            is_app = source_type in op_def.applicable_sources

            expected_check = op_def.expected_check_name
            if op_id == MutationOperatorId.M3 and not is_nvd:
                expected_check = "consistency_synthetic_vector_syntax"
            elif not is_app:
                expected_check = "NOT_APPLICABLE"

            mutant_id = f"MUT-{sid}-{op_id.name}"
            plan.append(MutationCase(
                mutant_id=mutant_id,
                scenario_id=sid,
                source_type=source_type,
                operator_id=op_id.value,
                operator_name=op_def.name,
                is_applicable=is_app,
                expected_check=expected_check,
                target_category=op_def.target_category,
                mutation_description=op_def.description,
            ))

    return plan


# ==============================================================================
# Read-Only Trace Loader (Zero-Write Guarantee)
# ==============================================================================

def load_canonical_trace_readonly(traces_dir: Path, scenario_id: str) -> Dict[str, Any]:
    """
    Reads a canonical trace file strictly in read-only mode from disk.
    Never modifies, writes, or unlinks any trace file.
    """
    trace_path = traces_dir / f"{scenario_id}.json"
    if not trace_path.exists():
        raise FileNotFoundError(f"Canonical trace artifact not found: {trace_path}")

    # Read strictly
    with open(trace_path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    # Return deepcopy to ensure caller cannot affect cached buffers
    return copy.deepcopy(data)


# ==============================================================================
# Verifier Evaluation Runner (Pure In-Memory Execution)
# ==============================================================================

def evaluate_mutant(
    mutant_case: MutationCase,
    mutated_trace: Dict[str, Any],
    verifier: vti.TraceVerifier,
) -> MutationResult:
    """
    Evaluates a single mutated trace using the in-memory TraceVerifier API.
    Does NOT write the mutated trace to disk.
    """
    if not mutant_case.is_applicable:
        return MutationResult(
            mutant_id=mutant_case.mutant_id,
            scenario_id=mutant_case.scenario_id,
            source_type=mutant_case.source_type,
            operator_id=mutant_case.operator_id,
            is_applicable=False,
            detected=False,
            detected_by_expected_check=False,
            execution_notes="Operator not applicable to this scenario source type.",
        )

    # Execute in-memory verification
    res: vti.ScenarioVerification = verifier.verify_scenario_trace(
        trace_data=mutated_trace,
        expected_scenario_id=mutant_case.scenario_id,
    )

    failing_checks = [c.name for c in res.checks if c.status == vti.CheckStatus.FAIL]
    failure_messages = [c.message for c in res.checks if c.status == vti.CheckStatus.FAIL]

    detected = (len(failing_checks) > 0)
    detected_by_expected = (mutant_case.expected_check in failing_checks)

    return MutationResult(
        mutant_id=mutant_case.mutant_id,
        scenario_id=mutant_case.scenario_id,
        source_type=mutant_case.source_type,
        operator_id=mutant_case.operator_id,
        is_applicable=True,
        detected=detected,
        detected_by_expected_check=detected_by_expected,
        failing_check_names=failing_checks,
        failure_messages=failure_messages,
        execution_notes="Detected" if detected else "UNEXPECTED_PASS_MUTANT_MISSED",
    )


# ==============================================================================
# Full Deterministic Campaign Runner
# ==============================================================================

def run_mutation_campaign(
    traces_dir: Path,
    dataset_csv_path: Path,
    scenario_ids: Sequence[str] = REPRESENTATIVE_SCENARIO_IDS,
) -> MutationCampaignReport:
    """
    Executes the deterministic mutation campaign over representative scenarios.
    Performs original-control pre-flight checks, in-memory mutation evaluation,
    and post-run canonical hash integrity verification.
    """
    verifier = vti.TraceVerifier(dataset_csv_path=dataset_csv_path)

    # 1. Pre-flight original control checks
    original_controls: Dict[str, Dict[str, Any]] = {}
    hashes_before: Dict[str, str] = {}
    for sid in scenario_ids:
        trace_file = traces_dir / f"{sid}.json"
        hashes_before[sid] = hashlib.sha256(trace_file.read_bytes()).hexdigest()
        orig_data = load_canonical_trace_readonly(traces_dir, sid)
        ctrl_res = verifier.verify_scenario_trace(orig_data, sid)
        original_controls[sid] = {
            "passed": ctrl_res.passed,
            "failure_count": ctrl_res.failure_count,
            "limitation_count": ctrl_res.limitation_count,
            "status": "PASS" if ctrl_res.passed else "FAIL",
            "initial_sha256": hashes_before[sid],
        }

    all_passed = all(c["passed"] for c in original_controls.values())
    campaign_integrity = "PASS" if all_passed else "FAIL"

    # 2. Build deterministic plan
    plan = build_deterministic_mutation_plan(scenario_ids)

    # 3. Execute mutants
    records: List[MutationCaseRecord] = []
    for case in plan:
        orig_data = load_canonical_trace_readonly(traces_dir, case.scenario_id)
        mutated, is_app, exp_check = apply_operator_to_trace(
            MutationOperatorId(case.operator_id), orig_data, case.source_type
        )
        res = evaluate_mutant(case, mutated, verifier)

        if not case.is_applicable:
            status = "NOT_APPLICABLE"
        elif res.detected and res.detected_by_expected_check:
            status = "DETECTED"
        elif res.detected:
            status = "UNEXPECTED"
        else:
            status = "MISSED"

        records.append(MutationCaseRecord(
            mutant_id=case.mutant_id,
            scenario_id=case.scenario_id,
            source_type=case.source_type,
            operator_id=case.operator_id,
            operator_name=case.operator_name,
            is_applicable=case.is_applicable,
            expected_check=case.expected_check,
            target_category=case.target_category,
            status=status,
            detected=res.detected,
            detected_by_expected_check=res.detected_by_expected_check,
            failing_checks=res.failing_check_names,
            failure_messages=res.failure_messages,
            notes=res.execution_notes,
        ))

    # 4. Post-run hash verification
    hashes_after = {
        sid: hashlib.sha256((traces_dir / f"{sid}.json").read_bytes()).hexdigest()
        for sid in scenario_ids
    }
    for sid in scenario_ids:
        original_controls[sid]["post_campaign_sha256"] = hashes_after[sid]
        original_controls[sid]["hash_unmodified"] = (hashes_before[sid] == hashes_after[sid])

    hashes_verified = (hashes_before == hashes_after)

    # 5. Compute aggregates
    total_planned = len(records)
    applicable_cases = [r for r in records if r.is_applicable]
    not_app_cases = [r for r in records if not r.is_applicable]
    detected_cases = [r for r in applicable_cases if r.status == "DETECTED"]
    missed_cases = [r for r in applicable_cases if r.status == "MISSED"]
    unexpected_cases = [r for r in applicable_cases if r.status == "UNEXPECTED"]

    app_count = len(applicable_cases)
    det_count = len(detected_cases)
    overall_rate = round(det_count / app_count, 4) if app_count > 0 else 0.0

    # Aggregates by operator
    op_summaries: Dict[str, Dict[str, Any]] = {}
    for op_id in MutationOperatorId:
        op_recs = [r for r in records if r.operator_id == op_id.value]
        op_app = [r for r in op_recs if r.is_applicable]
        op_det = [r for r in op_app if r.status == "DETECTED"]
        op_mis = [r for r in op_app if r.status == "MISSED"]
        op_unexp = [r for r in op_app if r.status == "UNEXPECTED"]
        op_not_app = [r for r in op_recs if not r.is_applicable]
        rate = round(len(op_det) / len(op_app), 4) if len(op_app) > 0 else 0.0
        op_summaries[op_id.value] = {
            "operator_id": op_id.value,
            "operator_name": MUTATION_OPERATOR_REGISTRY[op_id].name,
            "total_cases": len(op_recs),
            "applicable_cases": len(op_app),
            "not_applicable_cases": len(op_not_app),
            "detected_count": len(op_det),
            "missed_count": len(op_mis),
            "unexpected_count": len(op_unexp),
            "detection_rate": rate,
        }

    # Aggregates by source partition
    partition_summaries: Dict[str, Dict[str, Any]] = {}
    for stype in ["NVD", "SYNTHETIC"]:
        st_recs = [r for r in records if r.source_type == stype]
        st_app = [r for r in st_recs if r.is_applicable]
        st_det = [r for r in st_app if r.status == "DETECTED"]
        st_mis = [r for r in st_app if r.status == "MISSED"]
        st_unexp = [r for r in st_app if r.status == "UNEXPECTED"]
        st_not_app = [r for r in st_recs if not r.is_applicable]
        rate = round(len(st_det) / len(st_app), 4) if len(st_app) > 0 else 0.0
        partition_summaries[stype] = {
            "source_type": stype,
            "total_cases": len(st_recs),
            "applicable_cases": len(st_app),
            "not_applicable_cases": len(st_not_app),
            "detected_count": len(st_det),
            "missed_count": len(st_mis),
            "unexpected_count": len(st_unexp),
            "detection_rate": rate,
        }

    return MutationCampaignReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        campaign_integrity_status=campaign_integrity,
        canonical_scenarios_selected=list(scenario_ids),
        original_controls=original_controls,
        all_original_controls_passed=all_passed,
        trace_files_hash_verified_unmodified=hashes_verified,
        total_mutants_planned=total_planned,
        applicable_mutants=app_count,
        not_applicable_mutants=len(not_app_cases),
        detected_mutants=det_count,
        missed_mutants=len(missed_cases),
        unexpected_mutants=len(unexpected_cases),
        overall_detection_rate=overall_rate,
        operator_summaries=op_summaries,
        source_partition_summaries=partition_summaries,
        results=[asdict(r) for r in records],
    )


def export_mutation_report_json(report: MutationCampaignReport, output_path: Path) -> None:
    """Serializes the full mutation campaign report to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, mode="w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2, ensure_ascii=False)
    print(f"Wrote mutation campaign JSON report to {output_path}")


def export_mutation_cases_csv(report: MutationCampaignReport, output_path: Path) -> None:
    """Serializes all individual mutation cases to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "mutant_id",
        "scenario_id",
        "source_type",
        "operator_id",
        "operator_name",
        "is_applicable",
        "expected_check",
        "target_category",
        "status",
        "detected",
        "detected_by_expected_check",
        "failing_checks",
        "failure_messages",
        "notes",
    ]
    with open(output_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in report.results:
            row = {
                "mutant_id": r.get("mutant_id"),
                "scenario_id": r.get("scenario_id"),
                "source_type": r.get("source_type"),
                "operator_id": r.get("operator_id"),
                "operator_name": r.get("operator_name"),
                "is_applicable": r.get("is_applicable"),
                "expected_check": r.get("expected_check"),
                "target_category": r.get("target_category"),
                "status": r.get("status"),
                "detected": r.get("detected"),
                "detected_by_expected_check": r.get("detected_by_expected_check"),
                "failing_checks": "; ".join(r.get("failing_checks", [])),
                "failure_messages": "; ".join(r.get("failure_messages", [])),
                "notes": r.get("notes"),
            }
            writer.writerow(row)
    print(f"Wrote mutation cases CSV to {output_path}")


def format_campaign_summary(report: MutationCampaignReport) -> str:
    """Formats campaign report into console-readable summary."""
    lines = [
        "=" * 78,
        "CVSS v4.0 INDEPENDENT TRACE VERIFIER - EMPIRICAL MUTATION CAMPAIGN RESULTS",
        "=" * 78,
        f"Generated at UTC          : {report.generated_at_utc}",
        f"Campaign Integrity Status : {report.campaign_integrity_status}",
        f"Original Controls         : {sum(1 for c in report.original_controls.values() if c['passed'])}/{len(report.original_controls)} PASS",
        f"Canonical Files Unmodified: {report.trace_files_hash_verified_unmodified}",
        f"Representative Scenarios  : {len(report.canonical_scenarios_selected)} ({', '.join(report.canonical_scenarios_selected)})",
        f"Planned Total Mutants     : {report.total_mutants_planned}",
        f"Applicable Mutants        : {report.applicable_mutants}",
        f"NOT_APPLICABLE Mutants    : {report.not_applicable_mutants}",
        f"Detected Mutants          : {report.detected_mutants}",
        f"Missed Mutants            : {report.missed_mutants}",
        f"Unexpected Mutants        : {report.unexpected_mutants}",
        f"Overall Detection Rate    : {report.overall_detection_rate * 100:.1f}% ({report.detected_mutants}/{report.applicable_mutants})",
        "-" * 78,
        f"{'Operator':<32} {'Applicable':<12} {'Detected':<10} {'Missed':<8} {'Rate':<10}",
        "-" * 78,
    ]
    for op_id, summ in report.operator_summaries.items():
        name = summ["operator_name"]
        app = summ["applicable_cases"]
        det = summ["detected_count"]
        mis = summ["missed_count"]
        rate_str = f"{summ['detection_rate']*100:.1f}%" if app > 0 else "N/A"
        lines.append(f"{name:<32} {app:<12} {det:<10} {mis:<8} {rate_str:<10}")

    lines.append("-" * 78)
    lines.append("PARTITION SUMMARY (NVD vs SYNTHETIC):")
    for stype, summ in report.source_partition_summaries.items():
        app = summ["applicable_cases"]
        det = summ["detected_count"]
        mis = summ["missed_count"]
        rate_str = f"{summ['detection_rate']*100:.1f}%" if app > 0 else "N/A"
        lines.append(f"  {stype:<12}: {det}/{app} detected ({rate_str}), {mis} missed, {summ['not_applicable_cases']} N/A")

    lines.append("=" * 78)
    lines.append(f"Epistemological Boundary Statement:\n{report.epistemological_statement}")
    lines.append("=" * 78)
    return "\n".join(lines)


# ==============================================================================
# CLI and Reporting Interface
# ==============================================================================

def format_plan_summary(plan: List[MutationCase]) -> str:
    """Formats the planned mutation cases into a clear console summary."""
    total = len(plan)
    applicable = sum(1 for c in plan if c.is_applicable)
    not_app = total - applicable
    scenarios = sorted(set(c.scenario_id for c in plan))
    nvd_scens = [s for s in scenarios if s.startswith("SCN-NVD-")]
    syn_scens = [s for s in scenarios if s.startswith("SCN-SYN-")]

    lines = [
        "=" * 78,
        "CVSS v4.0 INDEPENDENT TRACE VERIFIER - EMPIRICAL MUTATION TESTING SUITE",
        "=" * 78,
        f"Target System Under Test : tools.verify_trace_integrity.TraceVerifier",
        f"Planned Representative Scenarios: {len(scenarios)} total (NVD={len(nvd_scens)}, Synthetic={len(syn_scens)})",
        f"Selected Scenario IDs   : {', '.join(scenarios)}",
        f"Total Mutants Planned    : {total} ({applicable} applicable, {not_app} not applicable)",
        "-" * 78,
        f"{'Operator':<32} {'Applicable Sources':<20} {'Target Category':<22}",
        "-" * 78,
    ]
    for op_id, op_def in MUTATION_OPERATOR_REGISTRY.items():
        sources_str = "/".join(op_def.applicable_sources)
        lines.append(f"{op_def.name:<32} {sources_str:<20} {op_def.target_category:<22}")
    lines.append("=" * 78)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Empirical mutation test suite for Independent Trace Verifier."
    )
    repo_root = Path(__file__).resolve().parent.parent
    parser.add_argument(
        "--traces-dir",
        type=Path,
        default=repo_root / "validation" / "article" / "trace",
        help="Path to canonical trace directory (read-only)",
    )
    parser.add_argument(
        "--dataset-csv",
        type=Path,
        default=repo_root / "data" / "article" / "cvss40_environmental_scenarios.csv",
        help="Path to reference scenarios CSV (read-only)",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Optional path to output structured JSON report",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=None,
        help="Optional path to output per-mutant CSV report",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress human-readable stdout summary",
    )
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print deterministic mutation plan and exit without running campaign",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.plan_only:
        plan = build_deterministic_mutation_plan()
        print(format_plan_summary(plan))
        print("\nPlan-only mode complete. No mutation campaign executed.")
        return 0

    report = run_mutation_campaign(
        traces_dir=args.traces_dir,
        dataset_csv_path=args.dataset_csv,
    )

    if not args.quiet:
        print(format_campaign_summary(report))

    if args.output_json:
        export_mutation_report_json(report, args.output_json)

    if args.output_csv:
        export_mutation_cases_csv(report, args.output_csv)

    return 0 if report.all_original_controls_passed else 1


if __name__ == "__main__":
    sys.exit(main())
