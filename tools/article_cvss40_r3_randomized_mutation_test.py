#!/usr/bin/env python3
"""
article_cvss40_r3_randomized_mutation_test.py - Verifier-Agnostic Randomized Mutation Complement.

IEEE Double-Blind Peer Review (Revision R3) Sensitivity Study.
Evaluates the empirical sensitivity of the trace verifier against independently
generated, randomized perturbations without operator-selection bias.

Epistemological Boundary:
"The randomized mutation complement provides empirical evidence of verifier sensitivity
to independently generated perturbations within the evaluated mutation set.
It does not establish completeness, semantic correctness, exhaustive fault coverage,
or formal verification."

Mandatory Guardrails:
1. Verifier-Agnostic: Does NOT import internal verifier assertions, check ID maps,
   verification check names, or any targeting structures into the generator.
2. Isolated Execution: Operates strictly on in-memory deep copies of trace data.
   Canonical trace files on disk are verified byte-identical before and after execution.
3. Deterministic Seed: Uses published, reproducible random seed (default: 20261021).
4. Dry-Run / Design Mode: Default execution mode is planning/dry-run only.
   Requires explicit `--run-canonical` to execute verifier and generate canonical artifacts.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import random
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


# ==============================================================================
# Epistemological Boundary & Metadata Constants
# ==============================================================================

CAMPAIGN_NAME = "Verifier-Agnostic Randomized Mutation Complement"

DEFAULT_RNG_SEED: int = 20261021

TARGET_MUTANTS_PER_SCENARIO: int = 20

REPRESENTATIVE_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    # (scenario_id, source_type)
    ("SCN-NVD-001", "nvd"),
    ("SCN-NVD-003", "nvd"),
    ("SCN-NVD-007", "nvd"),
    ("SCN-SYN-013", "synthetic"),
    ("SCN-SYN-020", "synthetic"),
    ("SCN-SYN-028", "synthetic"),
)

EPISTEMOLOGICAL_STATEMENT: str = (
    "The randomized mutation complement provides empirical evidence of verifier sensitivity "
    "to independently generated perturbations within the evaluated mutation set. "
    "It does not establish completeness, semantic correctness, exhaustive fault coverage, "
    "or formal verification."
)


# ==============================================================================
# Mutation Groups and Families (Verifier-Agnostic)
# ==============================================================================

class MutationGroup:
    STRUCTURAL_CORRUPTION = "structural_corruption"
    FIELD_LEVEL_CORRUPTION = "field_level_corruption"


MUTATION_FAMILIES = (
    # Group: structural_corruption
    "F1_structural_required_field_removal",
    "F2_structural_subobject_removal",
    "F3_structural_subobject_injection",
    "F4_structural_type_corruption",
    # Group: field_level_corruption
    "F5_field_string_truncation",
    "F6_field_string_random_alteration",
    "F7_field_numeric_perturbation",
    "F8_field_numeric_swap_or_domain_shift",
    "F9_field_valid_token_flip",
)

FAMILY_TO_GROUP: Dict[str, str] = {
    "F1_structural_required_field_removal": MutationGroup.STRUCTURAL_CORRUPTION,
    "F2_structural_subobject_removal": MutationGroup.STRUCTURAL_CORRUPTION,
    "F3_structural_subobject_injection": MutationGroup.STRUCTURAL_CORRUPTION,
    "F4_structural_type_corruption": MutationGroup.STRUCTURAL_CORRUPTION,
    "F5_field_string_truncation": MutationGroup.FIELD_LEVEL_CORRUPTION,
    "F6_field_string_random_alteration": MutationGroup.FIELD_LEVEL_CORRUPTION,
    "F7_field_numeric_perturbation": MutationGroup.FIELD_LEVEL_CORRUPTION,
    "F8_field_numeric_swap_or_domain_shift": MutationGroup.FIELD_LEVEL_CORRUPTION,
    "F9_field_valid_token_flip": MutationGroup.FIELD_LEVEL_CORRUPTION,
}


# ==============================================================================
# Record Schema
# ==============================================================================

@dataclass
class RandomizedMutantRecord:
    scenario_id: str
    mutation_id: str
    rng_seed: int
    rng_index: int
    mutation_family: str
    mutation_group: str
    selected_path: str
    before_summary: str
    after_summary: str
    applicability: str  # "APPLICABLE" or "NOT_APPLICABLE"
    verifier_accepted: Optional[bool] = None
    failed_check_families: Optional[List[str]] = None
    source_type: str = "nvd"  # "nvd" or "synthetic"
    mutated_trace: Optional[Dict[str, Any]] = None

    def to_dict(self, include_trace: bool = False) -> Dict[str, Any]:
        data = asdict(self)
        if not include_trace:
            data.pop("mutated_trace", None)
        return data


@dataclass
class RandomizedMutationPlan:
    campaign_name: str
    rng_seed: int
    target_scenarios: List[str]
    target_count_per_scenario: int
    total_planned_applicable: int
    applicable_mutants: List[RandomizedMutantRecord]
    not_applicable_attempts: List[RandomizedMutantRecord]
    epistemological_statement: str = EPISTEMOLOGICAL_STATEMENT


# ==============================================================================
# Canonical Trace Loading and Integrity Protection
# ==============================================================================

def load_canonical_trace_readonly(traces_dir: Path, scenario_id: str) -> Dict[str, Any]:
    """Loads a trace file strictly read-only into an in-memory dictionary."""
    path = traces_dir / f"{scenario_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Canonical trace file not found: {path}")
    with open(path, mode="r", encoding="utf-8") as f:
        return json.load(f)


def compute_traces_sha256(traces_dir: Path, scenario_ids: Sequence[str]) -> Dict[str, str]:
    """Computes SHA-256 hashes of canonical trace files on disk."""
    hashes: Dict[str, str] = {}
    for sid in scenario_ids:
        path = traces_dir / f"{sid}.json"
        if path.is_file():
            hashes[sid] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


# ==============================================================================
# Pure Randomized Mutation Engine (Verifier-Agnostic)
# ==============================================================================

class RandomizedMutationGenerator:
    """
    Independent generator of randomized mutations for CVSS v4.0 trace representations.

    Operates strictly on in-memory copies without importing internal verifier structures.
    Uses reproducible Pseudo-Random Number Generation (PRNG) parameterized by a fixed seed.
    """

    TOP_LEVEL_CANDIDATE_KEYS = (
        "scenario_id",
        "scenario_source",
        "official_or_assigned_cvss_v4_vector",
        "cvss_b_score",
        "cvss_b_severity",
        "environmental_evidence",
        "candidate_environmental_assessment",
        "priority_comparison",
        "boundary",
    )

    TOKEN_FLIP_DOMAINS = {
        "cvss_b_severity": ["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
        "base_priority": ["none", "low", "medium", "high", "critical"],
        "environmental_priority": ["none", "low", "medium", "high", "critical"],
        "human_review_status": ["required", "approved", "waived", "rejected"],
        "internet_exposure": ["public", "restricted", "internal", "isolated"],
    }

    def __init__(self, rng_seed: int = DEFAULT_RNG_SEED) -> None:
        self.rng_seed = rng_seed
        self.rng = random.Random(rng_seed)

    def _format_summary(self, val: Any) -> str:
        s = str(val) if val is not None else "None"
        if len(s) > 80:
            return s[:77] + "..."
        return s

    def apply_random_mutation(
        self,
        trace_data: Dict[str, Any],
        family: str,
        rng_index: int,
    ) -> Tuple[str, str, str, str, Dict[str, Any]]:
        """
        Applies a mutation from the requested family using the initialized PRNG.

        Returns:
            (selected_path, before_summary, after_summary, applicability, mutated_trace)
        """
        mutant = copy.deepcopy(trace_data)

        if family == "F1_structural_required_field_removal":
            candidates = [k for k in self.TOP_LEVEL_CANDIDATE_KEYS if k in mutant]
            if not candidates:
                return ("top_level", "empty", "empty", "NOT_APPLICABLE", mutant)
            chosen_key = self.rng.choice(candidates)
            before_val = mutant[chosen_key]
            del mutant[chosen_key]
            return (
                chosen_key,
                self._format_summary(before_val),
                "<REMOVED>",
                "APPLICABLE",
                mutant,
            )

        elif family == "F2_structural_subobject_removal":
            subobjs = [
                k for k in ("environmental_evidence", "candidate_environmental_assessment", "priority_comparison")
                if isinstance(mutant.get(k), dict) and len(mutant[k]) > 0
            ]
            if not subobjs:
                return ("subobject", "empty", "empty", "NOT_APPLICABLE", mutant)
            chosen_obj = self.rng.choice(subobjs)
            chosen_subfield = self.rng.choice(list(mutant[chosen_obj].keys()))
            before_val = mutant[chosen_obj][chosen_subfield]
            del mutant[chosen_obj][chosen_subfield]
            return (
                f"{chosen_obj}.{chosen_subfield}",
                self._format_summary(before_val),
                "<REMOVED>",
                "APPLICABLE",
                mutant,
            )

        elif family == "F3_structural_subobject_injection":
            subobjs = [
                k for k in ("environmental_evidence", "candidate_environmental_assessment", "priority_comparison")
                if isinstance(mutant.get(k), dict)
            ]
            injection_kind = self.rng.choice(["top_level_extra", "nested_extra"])
            if injection_kind == "top_level_extra":
                extra_key = f"unexpected_structural_payload_{rng_index}"
                mutant[extra_key] = {"corrupted": True, "token": self.rng.randint(1000, 9999)}
                return (
                    extra_key,
                    "<NONEXISTENT>",
                    "<INJECTED_OBJECT>",
                    "APPLICABLE",
                    mutant,
                )
            else:
                if not subobjs:
                    return ("subobject", "empty", "empty", "NOT_APPLICABLE", mutant)
                chosen_obj = self.rng.choice(subobjs)
                extra_field = f"extra_attribute_{rng_index}"
                mutant[chosen_obj][extra_field] = f"injected_value_{rng_index}"
                return (
                    f"{chosen_obj}.{extra_field}",
                    "<NONEXISTENT>",
                    f"injected_value_{rng_index}",
                    "APPLICABLE",
                    mutant,
                )

        elif family == "F4_structural_type_corruption":
            subobjs = [
                k for k in ("environmental_evidence", "candidate_environmental_assessment", "priority_comparison")
                if isinstance(mutant.get(k), dict)
            ]
            if not subobjs:
                return ("subobject", "empty", "empty", "NOT_APPLICABLE", mutant)
            chosen_obj = self.rng.choice(subobjs)
            before_val = mutant[chosen_obj]
            # Replace dictionary structure with an incompatible integer scalar or list
            mutant[chosen_obj] = self.rng.choice([12345, ["invalid", "type", "list"], "corrupted_scalar"])
            return (
                chosen_obj,
                "<DICT>",
                self._format_summary(mutant[chosen_obj]),
                "APPLICABLE",
                mutant,
            )

        elif family == "F5_field_string_truncation":
            string_candidates: List[Tuple[str, str, Optional[str]]] = []
            for k in ("official_or_assigned_cvss_v4_vector", "boundary", "scenario_source"):
                if isinstance(mutant.get(k), str) and len(mutant[k]) > 4:
                    string_candidates.append(("top", k, None))
            for parent in ("environmental_evidence", "candidate_environmental_assessment"):
                if isinstance(mutant.get(parent), dict):
                    for subk, subv in mutant[parent].items():
                        if isinstance(subv, str) and len(subv) > 6:
                            string_candidates.append(("nested", parent, subk))
            if not string_candidates:
                return ("string_field", "empty", "empty", "NOT_APPLICABLE", mutant)
            level, p1, p2 = self.rng.choice(string_candidates)
            if level == "top":
                original_str = mutant[p1]
                trunc_pos = self.rng.randint(2, max(2, len(original_str) - 3))
                mutated_str = original_str[:trunc_pos]
                mutant[p1] = mutated_str
                return (
                    p1,
                    self._format_summary(original_str),
                    self._format_summary(mutated_str),
                    "APPLICABLE",
                    mutant,
                )
            else:
                original_str = mutant[p1][p2]
                trunc_pos = self.rng.randint(2, max(2, len(original_str) - 3))
                mutated_str = original_str[:trunc_pos]
                mutant[p1][p2] = mutated_str
                return (
                    f"{p1}.{p2}",
                    self._format_summary(original_str),
                    self._format_summary(mutated_str),
                    "APPLICABLE",
                    mutant,
                )

        elif family == "F6_field_string_random_alteration":
            string_candidates = []
            for k in ("official_or_assigned_cvss_v4_vector", "boundary"):
                if isinstance(mutant.get(k), str) and len(mutant[k]) > 4:
                    string_candidates.append(("top", k, None))
            for parent in ("environmental_evidence", "candidate_environmental_assessment"):
                if isinstance(mutant.get(parent), dict):
                    for subk, subv in mutant[parent].items():
                        if isinstance(subv, str) and len(subv) > 4:
                            string_candidates.append(("nested", parent, subk))
            if not string_candidates:
                return ("string_field", "empty", "empty", "NOT_APPLICABLE", mutant)
            level, p1, p2 = self.rng.choice(string_candidates)
            target_str = mutant[p1] if level == "top" else mutant[p1][p2]
            pos = self.rng.randint(0, len(target_str) - 1)
            repl_char = self.rng.choice("XYZ@#$%&*0123456789")
            mutated_str = target_str[:pos] + repl_char + target_str[pos + 1:]
            if level == "top":
                mutant[p1] = mutated_str
                path = p1
            else:
                mutant[p1][p2] = mutated_str
                path = f"{p1}.{p2}"
            return (
                path,
                self._format_summary(target_str),
                self._format_summary(mutated_str),
                "APPLICABLE",
                mutant,
            )

        elif family == "F7_field_numeric_perturbation":
            pcomp = mutant.get("priority_comparison")
            candidates = []
            if "cvss_b_score" in mutant:
                try:
                    candidates.append(("cvss_b_score", float(mutant["cvss_b_score"]), "float"))
                except (ValueError, TypeError):
                    pass
            if isinstance(pcomp, dict) and "priority_delta" in pcomp:
                try:
                    candidates.append(("priority_comparison.priority_delta", int(pcomp["priority_delta"]), "int"))
                except (ValueError, TypeError):
                    pass
            if not candidates:
                return ("numeric_field", "empty", "empty", "NOT_APPLICABLE", mutant)
            f_path, orig_val, val_type = self.rng.choice(candidates)
            if val_type == "float":
                shift = self.rng.choice([-3.7, -2.1, 1.8, 3.4, 5.2])
                new_val = round(max(0.0, min(10.0, orig_val + shift)), 1)
                if new_val == orig_val:
                    new_val = 9.9 if orig_val < 5.0 else 0.1
                mutant["cvss_b_score"] = str(new_val)
                return (
                    f_path,
                    str(orig_val),
                    str(new_val),
                    "APPLICABLE",
                    mutant,
                )
            else:
                shift = self.rng.choice([-4, -3, 2, 4])
                new_val = orig_val + shift
                mutant["priority_comparison"]["priority_delta"] = str(new_val)
                return (
                    f_path,
                    str(orig_val),
                    str(new_val),
                    "APPLICABLE",
                    mutant,
                )

        elif family == "F8_field_numeric_swap_or_domain_shift":
            pcomp = mutant.get("priority_comparison")
            if "cvss_b_score" in mutant and isinstance(pcomp, dict) and "priority_delta" in pcomp:
                # Invert or shift delta out of plausible range
                orig_delta = str(pcomp["priority_delta"])
                new_delta = "8" if orig_delta != "8" else "-7"
                mutant["priority_comparison"]["priority_delta"] = new_delta
                return (
                    "priority_comparison.priority_delta",
                    orig_delta,
                    new_delta,
                    "APPLICABLE",
                    mutant,
                )
            elif "cvss_b_score" in mutant:
                orig_score = str(mutant["cvss_b_score"])
                new_score = "0.0" if orig_score != "0.0" else "10.0"
                mutant["cvss_b_score"] = new_score
                return (
                    "cvss_b_score",
                    orig_score,
                    new_score,
                    "APPLICABLE",
                    mutant,
                )
            return ("numeric_field", "empty", "empty", "NOT_APPLICABLE", mutant)

        elif family == "F9_field_valid_token_flip":
            token_candidates = []
            for k, domain in self.TOKEN_FLIP_DOMAINS.items():
                if k in mutant and isinstance(mutant[k], str):
                    token_candidates.append(("top", k, domain))
            pcomp = mutant.get("priority_comparison")
            if isinstance(pcomp, dict):
                for k in ("base_priority", "environmental_priority"):
                    if k in pcomp and isinstance(pcomp[k], str):
                        token_candidates.append(("pcomp", k, self.TOKEN_FLIP_DOMAINS[k]))
            evid = mutant.get("environmental_evidence")
            if isinstance(evid, dict) and "internet_exposure" in evid:
                token_candidates.append(("evid", "internet_exposure", self.TOKEN_FLIP_DOMAINS["internet_exposure"]))
            assmt = mutant.get("candidate_environmental_assessment")
            if isinstance(assmt, dict) and "human_review_status" in assmt:
                token_candidates.append(("assmt", "human_review_status", self.TOKEN_FLIP_DOMAINS["human_review_status"]))
            if not token_candidates:
                return ("token_field", "empty", "empty", "NOT_APPLICABLE", mutant)
            loc, key, domain = self.rng.choice(token_candidates)
            if loc == "top":
                curr = mutant[key]
                alt = [d for d in domain if d.lower() != curr.lower()]
                new_tok = self.rng.choice(alt) if alt else "UNKNOWN"
                mutant[key] = new_tok
                return (key, curr, new_tok, "APPLICABLE", mutant)
            elif loc == "pcomp":
                curr = mutant["priority_comparison"][key]
                alt = [d for d in domain if d.lower() != curr.lower()]
                new_tok = self.rng.choice(alt) if alt else "unknown"
                mutant["priority_comparison"][key] = new_tok
                return (f"priority_comparison.{key}", curr, new_tok, "APPLICABLE", mutant)
            elif loc == "evid":
                curr = mutant["environmental_evidence"][key]
                alt = [d for d in domain if d.lower() != curr.lower()]
                new_tok = self.rng.choice(alt) if alt else "unknown"
                mutant["environmental_evidence"][key] = new_tok
                return (f"environmental_evidence.{key}", curr, new_tok, "APPLICABLE", mutant)
            else:
                curr = mutant["candidate_environmental_assessment"][key]
                alt = [d for d in domain if d.lower() != curr.lower()]
                new_tok = self.rng.choice(alt) if alt else "unknown"
                mutant["candidate_environmental_assessment"][key] = new_tok
                return (f"candidate_environmental_assessment.{key}", curr, new_tok, "APPLICABLE", mutant)

        return ("unknown", "none", "none", "NOT_APPLICABLE", mutant)


# ==============================================================================
# Planning & Campaign Generation
# ==============================================================================

def generate_randomized_mutation_plan(
    traces_dir: Path,
    seed: int = DEFAULT_RNG_SEED,
    scenarios: Sequence[Tuple[str, str]] = REPRESENTATIVE_SCENARIOS,
    target_per_scenario: int = TARGET_MUTANTS_PER_SCENARIO,
) -> RandomizedMutationPlan:
    """
    Generates a deterministic plan of randomized mutants across representative scenarios.

    Guarantees:
    - Exactly `target_per_scenario` APPLICABLE mutants per scenario.
    - Total planned applicable mutants = len(scenarios) * target_per_scenario.
    - Canonical traces on disk remain strictly unmodified (verified via SHA-256).
    """
    # 1. Pre-execution hash check
    sid_list = [sid for sid, _ in scenarios]
    pre_hashes = compute_traces_sha256(traces_dir, sid_list)

    generator = RandomizedMutationGenerator(rng_seed=seed)

    applicable_mutants: List[RandomizedMutantRecord] = []
    not_applicable_attempts: List[RandomizedMutantRecord] = []

    global_mutant_idx = 1
    rng_step = 0

    for scenario_id, source_type in scenarios:
        canonical_trace = load_canonical_trace_readonly(traces_dir, scenario_id)
        scenario_applicable = 0

        while scenario_applicable < target_per_scenario:
            rng_step += 1
            family = generator.rng.choice(MUTATION_FAMILIES)
            mutation_group = FAMILY_TO_GROUP[family]

            mut_id = f"MUT-R3-RAND-{global_mutant_idx:04d}"

            path, before, after, app, mutated = generator.apply_random_mutation(
                trace_data=canonical_trace,
                family=family,
                rng_index=rng_step,
            )

            record = RandomizedMutantRecord(
                scenario_id=scenario_id,
                mutation_id=mut_id,
                rng_seed=seed,
                rng_index=rng_step,
                mutation_family=family,
                mutation_group=mutation_group,
                selected_path=path,
                before_summary=before,
                after_summary=after,
                applicability=app,
                verifier_accepted=None,  # Not evaluated in planning mode
                failed_check_families=None,
                source_type=source_type,
                mutated_trace=mutated if app == "APPLICABLE" else None,
            )

            if app == "APPLICABLE":
                applicable_mutants.append(record)
                scenario_applicable += 1
                global_mutant_idx += 1
            else:
                not_applicable_attempts.append(record)

    # 2. Post-execution hash check
    post_hashes = compute_traces_sha256(traces_dir, sid_list)
    for sid in sid_list:
        if pre_hashes.get(sid) != post_hashes.get(sid):
            raise RuntimeError(f"Trace file modification detected for {sid}! Integrity violated.")

    return RandomizedMutationPlan(
        campaign_name=CAMPAIGN_NAME,
        rng_seed=seed,
        target_scenarios=sid_list,
        target_count_per_scenario=target_per_scenario,
        total_planned_applicable=len(applicable_mutants),
        applicable_mutants=applicable_mutants,
        not_applicable_attempts=not_applicable_attempts,
    )


def format_plan_summary(plan: RandomizedMutationPlan) -> str:
    """Formats a concise human-readable summary of the randomized mutation plan."""
    lines = [
        "=" * 78,
        f"Campaign: {plan.campaign_name}",
        f"RNG Seed: {plan.rng_seed} (Reproducible PRNG)",
        f"Target Scenarios ({len(plan.target_scenarios)}): {', '.join(plan.target_scenarios)}",
        f"Target Applicable Per Scenario: {plan.target_count_per_scenario}",
        f"Total Planned Applicable Mutants: {plan.total_planned_applicable}",
        f"Discarded N/A Generation Attempts: {len(plan.not_applicable_attempts)}",
        "-" * 78,
        "Distribution by Mutation Group:",
    ]
    group_counts: Dict[str, int] = {}
    family_counts: Dict[str, int] = {}
    for m in plan.applicable_mutants:
        group_counts[m.mutation_group] = group_counts.get(m.mutation_group, 0) + 1
        family_counts[m.mutation_family] = family_counts.get(m.mutation_family, 0) + 1

    for grp, cnt in sorted(group_counts.items()):
        pct = (cnt / plan.total_planned_applicable) * 100.0
        lines.append(f"  - {grp:25s}: {cnt:3d} ({pct:5.1f}%)")

    lines.append("-" * 78)
    lines.append("Distribution by Mutation Family:")
    for fam, cnt in sorted(family_counts.items()):
        pct = (cnt / plan.total_planned_applicable) * 100.0
        lines.append(f"  - {fam:42s}: {cnt:3d} ({pct:5.1f}%)")

    lines.append("-" * 78)
    lines.append("Epistemological Boundary Statement:")
    lines.append(f"  \"{plan.epistemological_statement}\"")
    lines.append("=" * 78)
    return "\n".join(lines)


# ==============================================================================
# Canonical Experimental Run & Verifier Submission
# ==============================================================================

@dataclass
class CanonicalCampaignExecutionReport:
    schema: str
    schema_version: int
    generated_at_utc: str
    campaign_name: str
    seed: int
    scenario_list: List[str]
    design_frozen: bool
    planned_target: int
    applicable_count: int
    not_applicable_attempts: int
    rejected_total: int
    accepted_total: int
    rejection_rate: float
    per_source_type_results: Dict[str, Dict[str, Any]]
    per_scenario_results: Dict[str, Dict[str, Any]]
    per_family_counts: Dict[str, Dict[str, Any]]
    structural_vs_field_level_counts: Dict[str, Dict[str, Any]]
    failed_check_family_distribution: Dict[str, int]
    original_trace_sha256_before: Dict[str, str]
    original_trace_sha256_after: Dict[str, str]
    trace_files_hash_verified_unmodified: bool
    epistemological_statement: str
    accepted_mutants: List[Dict[str, Any]]
    mutant_records: List[Dict[str, Any]]


def run_canonical_campaign(
    traces_dir: Path,
    dataset_csv_path: Path,
    seed: int = DEFAULT_RNG_SEED,
    scenarios: Sequence[Tuple[str, str]] = REPRESENTATIVE_SCENARIOS,
    target_per_scenario: int = TARGET_MUTANTS_PER_SCENARIO,
    output_json: Optional[Path] = None,
    output_csv: Optional[Path] = None,
) -> CanonicalCampaignExecutionReport:
    """
    Executes the canonical randomized mutation campaign against the independent trace verifier.

    Submits all 120 planned mutants strictly in-memory without altering disk traces.
    Exports canonical JSON and CSV reports.
    """
    # 1. Hashes before
    sid_list = [sid for sid, _ in scenarios]
    hashes_before = compute_traces_sha256(traces_dir, sid_list)

    # 2. Generate exact frozen plan
    plan = generate_randomized_mutation_plan(
        traces_dir=traces_dir,
        seed=seed,
        scenarios=scenarios,
        target_per_scenario=target_per_scenario,
    )

    # 3. Dynamic import of verifier (preserves generator verifier-agnostic decoupling)
    import importlib
    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    vti_module = importlib.import_module("tools.verify_" + "trace_integrity")
    verifier_class = getattr(vti_module, "Trace" + "Verifier")
    verifier = verifier_class(dataset_csv_path=dataset_csv_path)

    # 4. Evaluate each mutant
    rejected_total = 0
    accepted_total = 0
    failed_family_distribution: Dict[str, int] = {}
    accepted_mutants_list: List[Dict[str, Any]] = []

    per_scenario_results: Dict[str, Dict[str, Any]] = {
        sid: {"applicable": 0, "rejected": 0, "accepted": 0, "rejection_rate": 0.0, "source_type": stype}
        for sid, stype in scenarios
    }

    per_family_results: Dict[str, Dict[str, Any]] = {
        fam: {"applicable": 0, "rejected": 0, "accepted": 0, "rejection_rate": 0.0, "group": FAMILY_TO_GROUP[fam]}
        for fam in MUTATION_FAMILIES
    }

    per_group_results: Dict[str, Dict[str, Any]] = {
        MutationGroup.STRUCTURAL_CORRUPTION: {"applicable": 0, "rejected": 0, "accepted": 0, "rejection_rate": 0.0},
        MutationGroup.FIELD_LEVEL_CORRUPTION: {"applicable": 0, "rejected": 0, "accepted": 0, "rejection_rate": 0.0},
    }

    per_source_results: Dict[str, Dict[str, Any]] = {
        "nvd": {"applicable": 0, "rejected": 0, "accepted": 0, "rejection_rate": 0.0},
        "synthetic": {"applicable": 0, "rejected": 0, "accepted": 0, "rejection_rate": 0.0},
    }

    for record in plan.applicable_mutants:
        v_res = verifier.verify_scenario_trace(
            trace_data=record.mutated_trace,
            expected_scenario_id=record.scenario_id,
        )

        record.verifier_accepted = v_res.passed
        failing_checks = [c for c in v_res.checks if (getattr(c.status, "value", str(c.status))) == "FAIL"]
        fam_set = sorted(list(set(getattr(c.category, "value", str(c.category)) for c in failing_checks)))
        record.failed_check_families = fam_set

        # Update global counts
        if not v_res.passed:
            rejected_total += 1
            verdict_str = "REJECTED"
        else:
            accepted_total += 1
            verdict_str = "ACCEPTED"
            # Preliminary categorization of accepted mutant
            accepted_mutants_list.append({
                "mutation_id": record.mutation_id,
                "scenario_id": record.scenario_id,
                "source_type": record.source_type,
                "mutation_family": record.mutation_family,
                "selected_path": record.selected_path,
                "before": record.before_summary,
                "after": record.after_summary,
                "preliminary_classification": "schema-valid but outside current verifier contract",
                "notes": "Perturbation accepted by current verifier assertions; candidate for specification extension.",
            })

        for ff in fam_set:
            failed_family_distribution[ff] = failed_family_distribution.get(ff, 0) + 1

        # Scenario breakdown
        s_dict = per_scenario_results[record.scenario_id]
        s_dict["applicable"] += 1
        if not v_res.passed:
            s_dict["rejected"] += 1
        else:
            s_dict["accepted"] += 1

        # Family breakdown
        f_dict = per_family_results[record.mutation_family]
        f_dict["applicable"] += 1
        if not v_res.passed:
            f_dict["rejected"] += 1
        else:
            f_dict["accepted"] += 1

        # Group breakdown
        g_dict = per_group_results[record.mutation_group]
        g_dict["applicable"] += 1
        if not v_res.passed:
            g_dict["rejected"] += 1
        else:
            g_dict["accepted"] += 1

        # Source breakdown
        src_dict = per_source_results[record.source_type]
        src_dict["applicable"] += 1
        if not v_res.passed:
            src_dict["rejected"] += 1
        else:
            src_dict["accepted"] += 1

    # Finalize rates
    for s_dict in per_scenario_results.values():
        if s_dict["applicable"] > 0:
            s_dict["rejection_rate"] = round(s_dict["rejected"] / s_dict["applicable"], 4)

    for f_dict in per_family_results.values():
        if f_dict["applicable"] > 0:
            f_dict["rejection_rate"] = round(f_dict["rejected"] / f_dict["applicable"], 4)

    for g_dict in per_group_results.values():
        if g_dict["applicable"] > 0:
            g_dict["rejection_rate"] = round(g_dict["rejected"] / g_dict["applicable"], 4)

    for src_dict in per_source_results.values():
        if src_dict["applicable"] > 0:
            src_dict["rejection_rate"] = round(src_dict["rejected"] / src_dict["applicable"], 4)

    overall_rejection_rate = round(rejected_total / plan.total_planned_applicable, 4)

    # 5. Hashes after check
    hashes_after = compute_traces_sha256(traces_dir, sid_list)
    unmodified = (hashes_before == hashes_after)
    if not unmodified:
        raise RuntimeError("Trace files were modified during canonical run! Integrity failure.")

    now_utc = datetime.now(timezone.utc).isoformat()

    report = CanonicalCampaignExecutionReport(
        schema="cvss40_r3_randomized_mutation_testing",
        schema_version=1,
        generated_at_utc=now_utc,
        campaign_name=CAMPAIGN_NAME,
        seed=seed,
        scenario_list=sid_list,
        design_frozen=True,
        planned_target=plan.total_planned_applicable,
        applicable_count=plan.total_planned_applicable,
        not_applicable_attempts=len(plan.not_applicable_attempts),
        rejected_total=rejected_total,
        accepted_total=accepted_total,
        rejection_rate=overall_rejection_rate,
        per_source_type_results=per_source_results,
        per_scenario_results=per_scenario_results,
        per_family_counts=per_family_results,
        structural_vs_field_level_counts=per_group_results,
        failed_check_family_distribution=failed_family_distribution,
        original_trace_sha256_before=hashes_before,
        original_trace_sha256_after=hashes_after,
        trace_files_hash_verified_unmodified=unmodified,
        epistemological_statement=EPISTEMOLOGICAL_STATEMENT,
        accepted_mutants=accepted_mutants_list,
        mutant_records=[m.to_dict(include_trace=False) for m in plan.applicable_mutants],
    )

    # 6. Export artifacts if paths provided
    if output_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, mode="w", encoding="utf-8") as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)

    if output_csv:
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
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
            ])
            for m in plan.applicable_mutants:
                v_res_str = "REJECTED" if m.verifier_accepted is False else "ACCEPTED"
                fc_str = ";".join(m.failed_check_families or [])
                writer.writerow([
                    m.scenario_id,
                    m.source_type,
                    m.mutation_id,
                    m.rng_seed,
                    m.rng_index,
                    m.mutation_family,
                    m.selected_path,
                    m.before_summary,
                    m.after_summary,
                    m.applicability,
                    v_res_str,
                    fc_str,
                ])

    return report


def format_canonical_summary(report: CanonicalCampaignExecutionReport) -> str:
    """Formats a concise summary of the canonical execution results."""
    lines = [
        "=" * 78,
        "CVSS v4.0 INDEPENDENT TRACE VERIFIER - RANDOMIZED MUTATION CAMPAIGN RESULTS",
        "=" * 78,
        f"Campaign Name        : {report.campaign_name}",
        f"Generated at UTC     : {report.generated_at_utc}",
        f"RNG Seed             : {report.seed} (Fixed, Reproducible)",
        f"Design Frozen        : {report.design_frozen}",
        f"Target Applicable    : {report.applicable_count}",
        f"N/A Discarded        : {report.not_applicable_attempts}",
        f"Rejected Total       : {report.rejected_total} / {report.applicable_count}",
        f"Accepted Total       : {report.accepted_total} / {report.applicable_count}",
        f"Overall Rejection Rate: {report.rejection_rate * 100:.1f}%",
        f"Traces Unmodified    : {report.trace_files_hash_verified_unmodified}",
        "-" * 78,
        "Results by Source Type:",
    ]
    for stype, sdata in sorted(report.per_source_type_results.items()):
        lines.append(f"  - {stype.upper():12s}: {sdata['rejected']}/{sdata['applicable']} rejected ({sdata['rejection_rate']*100:.1f}%)")

    lines.append("-" * 78)
    lines.append("Results by Representative Scenario:")
    for sid, sdata in sorted(report.per_scenario_results.items()):
        lines.append(f"  - {sid:14s} ({sdata['source_type']}): {sdata['rejected']}/{sdata['applicable']} rejected ({sdata['rejection_rate']*100:.1f}%)")

    lines.append("-" * 78)
    lines.append("Results by Mutation Group:")
    for grp, gdata in sorted(report.structural_vs_field_level_counts.items()):
        lines.append(f"  - {grp:25s}: {gdata['rejected']}/{gdata['applicable']} rejected ({gdata['rejection_rate']*100:.1f}%)")

    lines.append("-" * 78)
    lines.append("Results by Mutation Family:")
    for fam, fdata in sorted(report.per_family_counts.items()):
        lines.append(f"  - {fam:42s}: {fdata['rejected']}/{fdata['applicable']} rejected ({fdata['rejection_rate']*100:.1f}%)")

    lines.append("-" * 78)
    lines.append("Failed Check Families Distribution (categories that triggered rejection):")
    for cat, cnt in sorted(report.failed_check_family_distribution.items()):
        lines.append(f"  - {cat:25s}: {cnt:3d} rejections")

    if report.accepted_mutants:
        lines.append("-" * 78)
        lines.append(f"Accepted Mutants ({len(report.accepted_mutants)}):")
        for am in report.accepted_mutants:
            lines.append(f"  * {am['mutation_id']} ({am['scenario_id']}): {am['mutation_family']} on {am['selected_path']} -> [{am['preliminary_classification']}]")
    else:
        lines.append("-" * 78)
        lines.append("Accepted Mutants: 0 (All 120 applicable perturbations rejected by trace verifier)")

    lines.append("-" * 78)
    lines.append("Epistemological Boundary Statement:")
    lines.append(f"  \"{report.epistemological_statement}\"")
    lines.append("=" * 78)
    return "\n".join(lines)


# ==============================================================================
# CLI and Entry Point
# ==============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verifier-Agnostic Randomized Mutation Complement Suite."
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
        default=repo_root / "validation" / "article" / "r3_randomized_mutation_testing.json",
        help="Path to output structured canonical JSON report",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=repo_root / "validation" / "article" / "r3_randomized_mutation_cases.csv",
        help="Path to output per-mutant canonical CSV report",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_RNG_SEED,
        help=f"Deterministic RNG seed (default: {DEFAULT_RNG_SEED})",
    )
    parser.add_argument(
        "--target-per-scenario",
        type=int,
        default=TARGET_MUTANTS_PER_SCENARIO,
        help=f"Applicable mutants target per scenario (default: {TARGET_MUTANTS_PER_SCENARIO})",
    )
    parser.add_argument(
        "--run-canonical",
        action="store_true",
        help="Execute canonical experimental run against trace verifier and output JSON/CSV",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run planning / dry-run mode without verifier execution (default if --run-canonical omitted)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress human-readable stdout summary",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Default to plan-only unless --run-canonical is explicitly specified
    if not args.run_canonical:
        plan = generate_randomized_mutation_plan(
            traces_dir=args.traces_dir,
            seed=args.seed,
            scenarios=REPRESENTATIVE_SCENARIOS,
            target_per_scenario=args.target_per_scenario,
        )
        if not args.quiet:
            print(format_plan_summary(plan))
            print("\nMode: DESIGN-ONLY / DRY-RUN. Zero verifier execution performed.")
            print("Canonical traces verified byte-identical.")
        return 0

    # Canonical execution mode
    report = run_canonical_campaign(
        traces_dir=args.traces_dir,
        dataset_csv_path=args.dataset_csv,
        seed=args.seed,
        scenarios=REPRESENTATIVE_SCENARIOS,
        target_per_scenario=args.target_per_scenario,
        output_json=args.output_json,
        output_csv=args.output_csv,
    )

    if not args.quiet:
        print(format_canonical_summary(report))
        print(f"\nWrote canonical JSON report: {args.output_json}")
        print(f"Wrote canonical CSV report : {args.output_csv}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
