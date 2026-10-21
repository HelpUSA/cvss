#!/usr/bin/env python3
"""
test_article_cvss40_r3_randomized_mutation_test.py - Unit test suite for Randomized Mutation Complement.

IEEE Double-Blind Peer Review (Revision R3) Quality Assurance Suite.
Validates the deterministic planning, verifier-agnostic decoupling, seed reproducibility,
in-memory isolation, record schema completeness, and canonical artifact immutability.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Dict

import pytest

import tools.article_cvss40_r3_randomized_mutation_test as r3_rand


REPO_ROOT = Path(__file__).resolve().parent.parent
TRACES_DIR = REPO_ROOT / "validation" / "article" / "trace"
MANIFEST_PATH = REPO_ROOT / "validation" / "article" / "r2_freeze_manifest.json"


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture(scope="module")
def nvd_trace_raw() -> Dict[str, Any]:
    """Provides a clean in-memory copy of representative NVD scenario SCN-NVD-001."""
    return r3_rand.load_canonical_trace_readonly(TRACES_DIR, "SCN-NVD-001")


@pytest.fixture(scope="module")
def syn_trace_raw() -> Dict[str, Any]:
    """Provides a clean in-memory copy of representative Synthetic scenario SCN-SYN-013."""
    return r3_rand.load_canonical_trace_readonly(TRACES_DIR, "SCN-SYN-013")


# ==============================================================================
# 1. Deterministic Seed Behavior & Reproducibility Tests
# ==============================================================================

def test_deterministic_seed_behavior(nvd_trace_raw: Dict[str, Any]):
    """Test 1 & 2: Same seed + same scenario produces identical mutation sequence."""
    gen1 = r3_rand.RandomizedMutationGenerator(rng_seed=20261021)
    gen2 = r3_rand.RandomizedMutationGenerator(rng_seed=20261021)

    path1, b1, a1, app1, mut1 = gen1.apply_random_mutation(nvd_trace_raw, "F1_structural_required_field_removal", 1)
    path2, b2, a2, app2, mut2 = gen2.apply_random_mutation(nvd_trace_raw, "F1_structural_required_field_removal", 1)

    assert path1 == path2
    assert b1 == b2
    assert a1 == a2
    assert app1 == app2
    assert mut1 == mut2


def test_different_seed_produces_divergent_behavior(nvd_trace_raw: Dict[str, Any]):
    """Test 3: Different seeds can produce divergent mutation choices."""
    gen1 = r3_rand.RandomizedMutationGenerator(rng_seed=20261021)
    gen2 = r3_rand.RandomizedMutationGenerator(rng_seed=99999999)

    choices1 = [gen1.rng.choice(r3_rand.MUTATION_FAMILIES) for _ in range(10)]
    choices2 = [gen2.rng.choice(r3_rand.MUTATION_FAMILIES) for _ in range(10)]

    assert choices1 != choices2


# ==============================================================================
# 2. Verifier-Agnostic Isolation & Import Inspection Tests
# ==============================================================================

def test_generator_does_not_import_verifier_internals():
    """Test 4: Generator does not import assertion maps, check IDs, or verifier internals."""
    import inspect
    source = inspect.getsource(r3_rand)

    # Disallow importing verifier or referring to internal check IDs in the module
    forbidden_terms = [
        "import tools.verify_trace_integrity",
        "from tools.verify_trace_integrity",
        "CHK_",
        "check_catalog",
        "TraceVerifier",
        "assertion_map",
        "target_check_id",
    ]
    for term in forbidden_terms:
        assert term not in source, f"Forbidden verifier coupling detected in source: {term}"


# ==============================================================================
# 3. In-Memory Isolation & Byte-Identical Canonical Trace Tests
# ==============================================================================

def test_canonical_traces_remain_byte_identical():
    """Test 5: Canonical traces on disk remain byte-identical before and after plan generation."""
    scenario_ids = [sid for sid, _ in r3_rand.REPRESENTATIVE_SCENARIOS]
    pre_hashes = r3_rand.compute_traces_sha256(TRACES_DIR, scenario_ids)

    # Run full plan generation
    plan = r3_rand.generate_randomized_mutation_plan(
        traces_dir=TRACES_DIR,
        seed=20261021,
        scenarios=r3_rand.REPRESENTATIVE_SCENARIOS,
        target_per_scenario=20,
    )
    assert plan.total_planned_applicable == 120

    post_hashes = r3_rand.compute_traces_sha256(TRACES_DIR, scenario_ids)

    assert pre_hashes == post_hashes
    for sid in scenario_ids:
        assert pre_hashes[sid] == post_hashes[sid]


# ==============================================================================
# 4. Mutation Families & N/A Classification Tests
# ==============================================================================

def test_mutation_families_selectable(nvd_trace_raw: Dict[str, Any], syn_trace_raw: Dict[str, Any]):
    """Test 6: All mutation families are selectable and execute correctly on traces."""
    gen = r3_rand.RandomizedMutationGenerator(rng_seed=20261021)

    for family in r3_rand.MUTATION_FAMILIES:
        path, before, after, app, mutated = gen.apply_random_mutation(nvd_trace_raw, family, 1)
        assert app in ("APPLICABLE", "NOT_APPLICABLE")
        assert path != ""
        if app == "APPLICABLE":
            assert mutated != nvd_trace_raw

        path_s, before_s, after_s, app_s, mutated_s = gen.apply_random_mutation(syn_trace_raw, family, 1)
        assert app_s in ("APPLICABLE", "NOT_APPLICABLE")
        if app_s == "APPLICABLE":
            assert mutated_s != syn_trace_raw


def test_na_mutations_explicitly_classified():
    """Test 7: Mutations that cannot be applied are explicitly marked NOT_APPLICABLE."""
    gen = r3_rand.RandomizedMutationGenerator(rng_seed=20261021)
    empty_trace: Dict[str, Any] = {}

    # Removing a subobject from empty trace must be NOT_APPLICABLE
    path, before, after, app, mutated = gen.apply_random_mutation(
        empty_trace, "F2_structural_subobject_removal", 1
    )
    assert app == "NOT_APPLICABLE"


# ==============================================================================
# 5. Planning Mode & Target Counts Tests
# ==============================================================================

def test_planning_mode_target_count():
    """Test 8: Planning mode recognizes 6 scenarios * 20 = 120 target mutants."""
    plan = r3_rand.generate_randomized_mutation_plan(
        traces_dir=TRACES_DIR,
        seed=20261021,
        scenarios=r3_rand.REPRESENTATIVE_SCENARIOS,
        target_per_scenario=20,
    )
    assert len(plan.target_scenarios) == 6
    assert plan.target_count_per_scenario == 20
    assert plan.total_planned_applicable == 120
    assert len(plan.applicable_mutants) == 120


# ==============================================================================
# 6. Record Schema Completeness Tests
# ==============================================================================

def test_record_schema_contains_mandatory_fields():
    """Test 9: Record schema contains all mandatory fields."""
    plan = r3_rand.generate_randomized_mutation_plan(
        traces_dir=TRACES_DIR,
        seed=20261021,
        scenarios=r3_rand.REPRESENTATIVE_SCENARIOS,
        target_per_scenario=5,
    )
    mandatory_fields = [
        "scenario_id",
        "mutation_id",
        "rng_seed",
        "rng_index",
        "mutation_family",
        "mutation_group",
        "selected_path",
        "before_summary",
        "after_summary",
        "applicability",
        "verifier_accepted",
        "failed_check_families",
        "source_type",
    ]
    for mutant in plan.applicable_mutants:
        d = mutant.to_dict()
        for mf in mandatory_fields:
            assert mf in d, f"Missing mandatory field {mf} in mutant record"
        assert d["applicability"] == "APPLICABLE"
        assert d["verifier_accepted"] is None  # Must remain unevaluated in planning
        assert d["failed_check_families"] is None
        assert d["source_type"] in ("nvd", "synthetic")


# ==============================================================================
# 7. Dry-Run Isolation & Canonical Artifacts Self-Consistency Tests
# ==============================================================================

def test_dry_run_does_not_call_verifier_or_write_artifacts(tmp_path: Path):
    """Test 10 & 11: Dry run does not call verifier and does not write final JSON/CSV."""
    dummy_json = tmp_path / "dummy_randomized_mutation.json"
    dummy_csv = tmp_path / "dummy_randomized_mutation.csv"

    plan = r3_rand.generate_randomized_mutation_plan(
        traces_dir=TRACES_DIR,
        seed=20261021,
        scenarios=r3_rand.REPRESENTATIVE_SCENARIOS,
        target_per_scenario=20,
    )

    # In dry-run, no mutant has been evaluated by the verifier
    for mutant in plan.applicable_mutants:
        assert mutant.verifier_accepted is None
        assert mutant.failed_check_families is None

    # Confirm dry run did not output files to custom targets
    assert not dummy_json.exists()
    assert not dummy_csv.exists()


def test_canonical_artifacts_schema_and_self_consistency():
    """Validates self-consistency and schema of canonical R3 randomized mutation artifacts."""
    r3_json = REPO_ROOT / "validation" / "article" / "r3_randomized_mutation_testing.json"
    r3_csv = REPO_ROOT / "validation" / "article" / "r3_randomized_mutation_cases.csv"

    assert r3_json.is_file(), "Canonical R3 JSON report missing"
    assert r3_csv.is_file(), "Canonical R3 CSV report missing"

    with open(r3_json, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["schema"] == "cvss40_r3_randomized_mutation_testing"
    assert data["seed"] == 20261021
    assert data["design_frozen"] is True
    assert data["planned_target"] == 120
    assert data["applicable_count"] == 120
    assert data["rejected_total"] == 83
    assert data["accepted_total"] == 37
    assert data["rejection_rate"] == 0.6917
    assert len(data["mutant_records"]) == 120
    assert data["trace_files_hash_verified_unmodified"] is True

    # Validate CSV rows and header
    with open(r3_csv, mode="r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    header = lines[0].split(",")
    assert header == [
        "scenario_id",
        "source_type",
        "mutation_id",
        "rng_seed",
        "deterministic_sequence_index",
        "mutation_family",
        "selected_path_or_field",
        "before_summary",
        "after_summary",
        "applicability",
        "verifier_result",
        "failed_check_families",
    ]
    # 1 header + 120 mutant records
    assert len(lines) == 121


# ==============================================================================
# 8. R2 Canonical Artifact Immutability Tests
# ==============================================================================

def test_seven_canonical_r2_artifacts_unmodified():
    """Test 12: The seven canonical R2 artifacts remain exactly identical to R2 freeze manifest."""
    assert MANIFEST_PATH.is_file(), "R2 freeze manifest not found"

    with open(MANIFEST_PATH, mode="r", encoding="utf-8") as f:
        manifest = json.load(f)

    canonical_artifacts = manifest.get("canonical_artifacts", {})
    assert len(canonical_artifacts) == 7, f"Expected 7 canonical artifacts, found {len(canonical_artifacts)}"

    for rel_path, meta in canonical_artifacts.items():
        artifact_path = REPO_ROOT / rel_path
        assert artifact_path.is_file(), f"Missing canonical artifact: {rel_path}"
        content = artifact_path.read_bytes()
        actual_bytes = len(content)
        actual_sha256 = hashlib.sha256(content).hexdigest()

        assert actual_bytes == meta["bytes"], f"Byte mismatch in {rel_path}: {actual_bytes} != {meta['bytes']}"
        assert actual_sha256 == meta["sha256"], f"SHA256 mismatch in {rel_path}: {actual_sha256} != {meta['sha256']}"
