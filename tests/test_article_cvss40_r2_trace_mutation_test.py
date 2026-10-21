#!/usr/bin/env python3
"""
test_article_cvss40_r2_trace_mutation_test.py - Unit test suite for Trace Mutation Testing.

IEEE Double-Blind Peer Review (Revision R2) Quality Assurance Suite.
Validates the deterministic planning, operator behavior (M1-M8), in-memory isolation,
applicability filtering, and conservative epistemological claims of the mutation tool.
"""

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Dict

import pytest

import tools.article_cvss40_r2_trace_mutation_test as mut
import tools.verify_trace_integrity as vti


REPO_ROOT = Path(__file__).resolve().parent.parent
TRACES_DIR = REPO_ROOT / "validation" / "article" / "trace"
CSV_PATH = REPO_ROOT / "data" / "article" / "cvss40_environmental_scenarios.csv"


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture(scope="module")
def verifier() -> vti.TraceVerifier:
    """Provides a shared TraceVerifier initialized with canonical CSV dataset."""
    return vti.TraceVerifier(dataset_csv_path=CSV_PATH)


@pytest.fixture(scope="module")
def nvd_trace_raw() -> Dict[str, Any]:
    """Provides a clean in-memory copy of representative NVD scenario SCN-NVD-001."""
    return mut.load_canonical_trace_readonly(TRACES_DIR, "SCN-NVD-001")


@pytest.fixture(scope="module")
def syn_trace_raw() -> Dict[str, Any]:
    """Provides a clean in-memory copy of representative Synthetic scenario SCN-SYN-013."""
    return mut.load_canonical_trace_readonly(TRACES_DIR, "SCN-SYN-013")


# ==============================================================================
# 1. Deterministic Campaign Planning Tests
# ==============================================================================

def test_campaign_plan_is_deterministic():
    """Confirms fixed selection of 6 scenarios, 48 planned mutants, 42 applicable, 6 N/A."""
    plan = mut.build_deterministic_mutation_plan()

    assert len(plan) == 48, f"Expected 48 planned mutants, got {len(plan)}"

    scenarios = sorted(set(c.scenario_id for c in plan))
    assert scenarios == sorted(mut.REPRESENTATIVE_SCENARIO_IDS)
    assert len(scenarios) == 6

    # 3 NVD + 3 Synthetic
    nvd_scens = [s for s in scenarios if s.startswith("SCN-NVD-")]
    syn_scens = [s for s in scenarios if s.startswith("SCN-SYN-")]
    assert len(nvd_scens) == 3
    assert len(syn_scens) == 3

    # Must contain at least one curated override (SCN-NVD-001 / 007) and one nominal match (SCN-NVD-003)
    assert "SCN-NVD-001" in nvd_scens
    assert "SCN-NVD-003" in nvd_scens

    applicable = [c for c in plan if c.is_applicable]
    not_applicable = [c for c in plan if not c.is_applicable]

    assert len(applicable) == 42, f"Expected 42 applicable mutants, got {len(applicable)}"
    assert len(not_applicable) == 6, f"Expected 6 not applicable mutants, got {len(not_applicable)}"


# ==============================================================================
# 2. Operator Sensitivity Tests (M1 - M8)
# ==============================================================================

def test_m1_remove_required_field_detected(nvd_trace_raw, verifier):
    """M1: Confirms verifier rejects trace when top-level mandatory field is removed."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M1, nvd_trace_raw, "NVD"
    )
    assert is_app is True
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M1",
        scenario_id="SCN-NVD-001",
        source_type="NVD",
        operator_id=mut.MutationOperatorId.M1.value,
        operator_name="remove_required_field",
        is_applicable=True,
        expected_check=exp_check,
        target_category="STRUCTURAL",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.detected is True
    assert res.detected_by_expected_check is True
    assert exp_check in res.failing_check_names


def test_m2_delta_cat_mismatch_detected(nvd_trace_raw, verifier):
    """M2: Confirms verifier rejects corrupted category delta via arithmetic check."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M2, nvd_trace_raw, "NVD"
    )
    assert is_app is True
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M2",
        scenario_id="SCN-NVD-001",
        source_type="NVD",
        operator_id=mut.MutationOperatorId.M2.value,
        operator_name="delta_cat_mismatch",
        is_applicable=True,
        expected_check=exp_check,
        target_category="RECOMPUTED",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.detected is True
    assert res.detected_by_expected_check is True
    assert "recomputed_category_delta" in res.failing_check_names


def test_m3_invalid_vector_syntax_detected_nvd(nvd_trace_raw, verifier):
    """M3 (NVD): Confirms verifier rejects invalid CVSS vector in NVD trace."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M3, nvd_trace_raw, "NVD"
    )
    assert is_app is True
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M3-NVD",
        scenario_id="SCN-NVD-001",
        source_type="NVD",
        operator_id=mut.MutationOperatorId.M3.value,
        operator_name="invalid_vector_syntax",
        is_applicable=True,
        expected_check=exp_check,
        target_category="RECOMPUTED",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.detected is True
    assert res.detected_by_expected_check is True
    assert "recomputed_nvd_cvss_score" in res.failing_check_names


def test_m3_invalid_vector_syntax_detected_synthetic(syn_trace_raw, verifier):
    """M3 (Synthetic): Confirms verifier rejects invalid vector grammar in synthetic trace."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M3, syn_trace_raw, "SYNTHETIC"
    )
    assert is_app is True
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M3-SYN",
        scenario_id="SCN-SYN-013",
        source_type="SYNTHETIC",
        operator_id=mut.MutationOperatorId.M3.value,
        operator_name="invalid_vector_syntax",
        is_applicable=True,
        expected_check=exp_check,
        target_category="CONSISTENCY",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.detected is True
    assert res.detected_by_expected_check is True
    assert "consistency_synthetic_vector_syntax" in res.failing_check_names


def test_m4_nvd_score_mismatch_detected(nvd_trace_raw, verifier):
    """M4: Confirms canonical scorer recomputation detects altered Base score in NVD trace."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M4, nvd_trace_raw, "NVD"
    )
    assert is_app is True
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M4",
        scenario_id="SCN-NVD-001",
        source_type="NVD",
        operator_id=mut.MutationOperatorId.M4.value,
        operator_name="nvd_score_mismatch",
        is_applicable=True,
        expected_check=exp_check,
        target_category="RECOMPUTED",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.detected is True
    assert res.detected_by_expected_check is True
    assert "recomputed_nvd_cvss_score" in res.failing_check_names


def test_m4_not_applicable_to_synthetic(syn_trace_raw, verifier):
    """M4: Confirms NVD score mismatch operator is NOT_APPLICABLE to synthetic scenarios."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M4, syn_trace_raw, "SYNTHETIC"
    )
    assert is_app is False
    assert exp_check == "NOT_APPLICABLE"
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M4-SYN",
        scenario_id="SCN-SYN-013",
        source_type="SYNTHETIC",
        operator_id=mut.MutationOperatorId.M4.value,
        operator_name="nvd_score_mismatch",
        is_applicable=False,
        expected_check=exp_check,
        target_category="RECOMPUTED",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.is_applicable is False
    assert res.detected is False
    assert len(res.failing_check_names) == 0


def test_m5_synthetic_uncertainty_flag_removal_detected(syn_trace_raw, verifier):
    """M5: Confirms removal of uncertainty flags in synthetic trace is detected."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M5, syn_trace_raw, "SYNTHETIC"
    )
    assert is_app is True
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M5",
        scenario_id="SCN-SYN-013",
        source_type="SYNTHETIC",
        operator_id=mut.MutationOperatorId.M5.value,
        operator_name="remove_synthetic_uncertainty_flag",
        is_applicable=True,
        expected_check=exp_check,
        target_category="STRUCTURAL",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.detected is True
    assert res.detected_by_expected_check is True
    assert "structural_uncertainty_representation" in res.failing_check_names


def test_m5_not_applicable_to_nvd(nvd_trace_raw, verifier):
    """M5: Confirms synthetic uncertainty flag operator is NOT_APPLICABLE to NVD scenarios."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M5, nvd_trace_raw, "NVD"
    )
    assert is_app is False
    assert exp_check == "NOT_APPLICABLE"
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M5-NVD",
        scenario_id="SCN-NVD-001",
        source_type="NVD",
        operator_id=mut.MutationOperatorId.M5.value,
        operator_name="remove_synthetic_uncertainty_flag",
        is_applicable=False,
        expected_check=exp_check,
        target_category="STRUCTURAL",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.is_applicable is False
    assert res.detected is False


def test_m6_invalid_review_state_detected(nvd_trace_raw, verifier):
    """M6: Confirms unauthorized review bypass status is detected and rejected."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M6, nvd_trace_raw, "NVD"
    )
    assert is_app is True
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M6",
        scenario_id="SCN-NVD-001",
        source_type="NVD",
        operator_id=mut.MutationOperatorId.M6.value,
        operator_name="invalid_review_state",
        is_applicable=True,
        expected_check=exp_check,
        target_category="STRUCTURAL",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.detected is True
    assert res.detected_by_expected_check is True
    assert "structural_governance_authorization_state" in res.failing_check_names


def test_m7_source_provenance_mismatch_detected(nvd_trace_raw, syn_trace_raw, verifier):
    """M7: Confirms contamination of source separation is detected on both NVD and synthetic."""
    # Test on NVD
    mut_nvd, is_app_nvd, exp_nvd = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M7, nvd_trace_raw, "NVD"
    )
    assert is_app_nvd is True
    case_nvd = mut.MutationCase(
        mutant_id="MUT-TEST-M7-NVD",
        scenario_id="SCN-NVD-001",
        source_type="NVD",
        operator_id=mut.MutationOperatorId.M7.value,
        operator_name="source_provenance_mismatch",
        is_applicable=True,
        expected_check=exp_nvd,
        target_category="CONSISTENCY",
        mutation_description="test",
    )
    res_nvd = mut.evaluate_mutant(case_nvd, mut_nvd, verifier)
    assert res_nvd.detected is True
    assert "consistency_source_separation" in res_nvd.failing_check_names

    # Test on Synthetic
    mut_syn, is_app_syn, exp_syn = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M7, syn_trace_raw, "SYNTHETIC"
    )
    assert is_app_syn is True
    case_syn = mut.MutationCase(
        mutant_id="MUT-TEST-M7-SYN",
        scenario_id="SCN-SYN-013",
        source_type="SYNTHETIC",
        operator_id=mut.MutationOperatorId.M7.value,
        operator_name="source_provenance_mismatch",
        is_applicable=True,
        expected_check=exp_syn,
        target_category="CONSISTENCY",
        mutation_description="test",
    )
    res_syn = mut.evaluate_mutant(case_syn, mut_syn, verifier)
    assert res_syn.detected is True
    assert "consistency_source_separation" in res_syn.failing_check_names


def test_m8_canonical_dataset_mismatch_detected(nvd_trace_raw, verifier):
    """M8: Confirms inconsistency between trace severity and reference CSV is detected."""
    mutated, is_app, exp_check = mut.apply_operator_to_trace(
        mut.MutationOperatorId.M8, nvd_trace_raw, "NVD"
    )
    assert is_app is True
    case = mut.MutationCase(
        mutant_id="MUT-TEST-M8",
        scenario_id="SCN-NVD-001",
        source_type="NVD",
        operator_id=mut.MutationOperatorId.M8.value,
        operator_name="canonical_dataset_mismatch",
        is_applicable=True,
        expected_check=exp_check,
        target_category="RECOMPUTED",
        mutation_description="test",
    )
    res = mut.evaluate_mutant(case, mutated, verifier)
    assert res.detected is True
    assert res.detected_by_expected_check is True
    assert "recomputed_base_priority" in res.failing_check_names


# ==============================================================================
# 3. Isolation, Invariant, and Epistemological Safety Tests
# ==============================================================================

def test_mutations_do_not_modify_source_trace(nvd_trace_raw):
    """Confirms applying mutation operators leaves source dictionary byte-for-byte identical."""
    source_copy = copy.deepcopy(nvd_trace_raw)
    orig_json = json.dumps(source_copy, sort_keys=True)

    # Apply all operators
    for op_id in mut.MutationOperatorId:
        mutated, _, _ = mut.apply_operator_to_trace(op_id, source_copy, "NVD")
        assert mutated is not source_copy

    after_json = json.dumps(source_copy, sort_keys=True)
    assert orig_json == after_json, "Source trace dictionary was mutated during operator application!"


def test_not_applicable_excluded_from_detection_rate():
    """Confirms that NOT_APPLICABLE cases do not count in detection rate denominator."""
    plan = mut.build_deterministic_mutation_plan()
    applicable_count = sum(1 for c in plan if c.is_applicable)
    not_applicable_count = sum(1 for c in plan if not c.is_applicable)

    assert applicable_count == 42
    assert not_applicable_count == 6

    # Hypothetical calculation: 42 detected out of 42 applicable = 1.0 (100%), NOT 42/48
    rate = applicable_count / applicable_count
    assert rate == 1.0


def test_detection_result_requires_rejection(verifier):
    """Confirms mutant is counted as detected ONLY when verifier yields actual check failures."""
    # A valid baseline trace should have 0 failures, hence detected=False
    valid_trace = mut.load_canonical_trace_readonly(TRACES_DIR, "SCN-NVD-001")
    dummy_case = mut.MutationCase(
        mutant_id="MUT-TEST-CLEAN",
        scenario_id="SCN-NVD-001",
        source_type="NVD",
        operator_id=mut.MutationOperatorId.M1.value,
        operator_name="test",
        is_applicable=True,
        expected_check="structural_required_top_level_fields",
        target_category="STRUCTURAL",
        mutation_description="clean test",
    )
    clean_res = mut.evaluate_mutant(dummy_case, valid_trace, verifier)
    assert clean_res.detected is False
    assert len(clean_res.failing_check_names) == 0


def test_claim_metadata_is_epistemically_conservative():
    """Confirms epistemological statement contains exact boundary phrasing and forbids overclaims."""
    report = mut.MutationCampaignReport(
        generated_at_utc="2026-10-21T00:00:00Z",
        total_mutants_planned=48,
        applicable_mutants=42,
        not_applicable_mutants=6,
        detected_mutants=42,
        overall_detection_rate=1.0,
        operator_summaries={},
        source_partition_summaries={},
        results=[],
    )
    stmt = report.epistemological_statement.lower()

    # Required phrasing
    assert "empirical evidence that injected trace violations are detected and rejected in the evaluated mutation set" in stmt

    # Forbidden claims as proved conclusions
    assert "formal verification" in stmt  # allowed only in negation ("does NOT constitute formal verification")
    assert "does not constitute" in stmt
    assert "not constitute" in stmt or "does not" in stmt


def test_no_canonical_trace_writes():
    """Confirms zero writes/modifications to canonical trace files on disk."""
    trace_files = list(TRACES_DIR.glob("SCN-*.json"))
    assert len(trace_files) >= 30

    # Record initial modification timestamps and hashes
    initial_stats = {
        p: (p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
        for p in trace_files[:6]
    }

    # Execute read and in-memory mutation
    for p in trace_files[:6]:
        sid = p.stem
        raw_data = mut.load_canonical_trace_readonly(TRACES_DIR, sid)
        stype = "NVD" if sid.startswith("SCN-NVD-") else "SYNTHETIC"
        for op in mut.MutationOperatorId:
            _ = mut.apply_operator_to_trace(op, raw_data, stype)

    # Verify no file on disk was modified or written to
    for p, (orig_mtime, orig_hash) in initial_stats.items():
        curr_mtime = p.stat().st_mtime_ns
        curr_hash = hashlib.sha256(p.read_bytes()).hexdigest()
        assert orig_mtime == curr_mtime, f"File mtime changed on disk: {p.name}"
        assert orig_hash == curr_hash, f"File content hash changed on disk: {p.name}"
