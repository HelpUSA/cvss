#!/usr/bin/env python3
"""R6.2 Differential CVSS v4.0 Validation Runner (Corrected Protocol R2).

Suite: TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R2
Label: R6.2-DIFF-R2
Deviation: R6-DEV-005 (POST_RESULT_CHANGE)
Corpus: FIRST cvss-resources commit d766d0c8ab4368b67bf27dd0e411eb481f05fdbb (D_total = 486,472)
  - Primary Numeric Endpoint: D_numeric = 461,444
  - Secondary Negative Validation Endpoint: D_validation = 25,028
Comparator: cvss4py commit 9fe705cdb7d4a222770e0561f046d3e3f061088a
Primary: HelpUS Primary Scorer (Red Hat cvss 3.6 / core.cvss_calculator)

Operates strictly offline, deterministically, with two-pass rerun parity check.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
import math
import os
import subprocess
import sys
import time
import warnings
from pathlib import Path

# Silence third-party warnings and stdlib stderr pollution during batch evaluation
warnings.simplefilter("ignore")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "external" / "comparators" / "cvss4py"))
sys.path.insert(0, str(ROOT))

import cvss4py
import cvss
import cvss.cvss4
import cvss.exceptions

# Port exact FIRST reference calculator arithmetic (Math.round(x * 10) / 10)
cvss.cvss4.final_rounding = lambda x: math.floor(x * 10.0 + 0.5) / 10.0
from cvss import CVSS4

EXPECTED_HEAD = "096e2777e5f938ce70ef6a49c73847da7809415d"
EXPECTED_COMPARATOR_COMMIT = "9fe705cdb7d4a222770e0561f046d3e3f061088a"
EXPECTED_CORPUS_COMMIT = "d766d0c8ab4368b67bf27dd0e411eb481f05fdbb"
DENOMINATOR_TOTAL = 486472
DENOMINATOR_NUMERIC = 461444
DENOMINATOR_VALIDATION = 25028

FIXTURE_DIR = ROOT / "tests" / "fixtures" / "cvss_resources" / "vectorFiles"
OUTPUT_DIR = ROOT / "validation" / "article" / "r6_differential_r2"
ELIGIBILITY_MANIFEST_PATH = OUTPUT_DIR / "r6_differential_r2_corpus_eligibility_manifest.json"

HISTORICAL_R1_SHA256 = {
    "r6_differential_r1_results.json": "18563f9737b8e2f5c8eac632a56198d0f5adeb21b7decb10a22e39425a235dd6",
    "r6_differential_r1_summary.md": "ec7e748f0a21e070ad423be0528834b64b774e0d00d73fa80724412a21ce6f52",
    "r6_differential_r1_mismatch_analysis.md": "e1065dc3ac2df3d76f71dc48263e7d2559502bbc47bcaeb7092b9a8e7e2a6b44",
    "r6_differential_r1_execution_manifest.json": "0a0eb9a08beda042666a0210691372bed4a2772468c4790bf09ee910ef1565ce",
    "r6_differential_r1_mismatches.jsonl": "f298fd1e9a34e40147d3925e4741ae47fd14ee40ed39694bfc73535808ea5a98",
}

CORPUS_FILES = [
    {
        "filename": "macro-vectors",
        "sha256": "f653914506e697a94a18b690c051144b295626c534737fb79c589a61c1e0e8a3",
        "expected_records": 270,
        "scores_filename": "macro-scores",
    },
    {
        "filename": "reference-vectors",
        "sha256": "fdcb3de3485354ff36577b41b2fcf7f8056785fb6d6bf6c6eed97e7d3bc934bf",
        "expected_records": 66298,
        "scores_filename": "reference-scores",
    },
    {
        "filename": "base-threat-vectors",
        "sha256": "eb9cf89bab6712f368fe65c43f884e1ca4750e4e30181fabad4a61aaecccede1",
        "expected_records": 419904,
        "scores_filename": "base-threat-scores",
    },
]

# Expected validation exception types
CVSS4PY_EXPECTED_EXCEPTIONS = (
    cvss4py.classes.UnknownMetricValue,
    cvss4py.classes.InvalidEqClass,
    cvss4py.classes.MissingMetric,
    cvss4py.classes.UnknownMetric,
    SyntaxError,
    ValueError,
    KeyError,
)

HELPUS_EXPECTED_EXCEPTIONS = (
    cvss.exceptions.CVSS4MalformedError,
    cvss.exceptions.CVSS4MandatoryError,
    cvss.exceptions.CVSS4Error,
    cvss.exceptions.CVSSError,
    ValueError,
    KeyError,
)


def pre_execution_guard(check_head: bool = True):
    """Verify environmental, protocol, and cryptographic invariants before evaluation."""
    print("Executing Pre-Execution Guard for R2...")

    # 1. Git HEAD check
    if check_head:
        try:
            head = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip()
        except Exception as e:
            raise RuntimeError(f"Failed to check git HEAD: {e}")
        if not head.startswith(EXPECTED_HEAD[:7]):
            raise RuntimeError(f"HEAD guard failed: expected {EXPECTED_HEAD}, got {head}")

    # 2. R6-DEV-005 check in protocol deviation log
    dev_log_path = ROOT / "validation" / "article" / "r6_a1_protocol_deviation_log.md"
    if not dev_log_path.exists():
        raise RuntimeError("Protocol deviation log missing")
    dev_log = dev_log_path.read_text(encoding="utf-8")
    if "R6-DEV-005" not in dev_log or "POST_RESULT_CHANGE" not in dev_log:
        raise RuntimeError("R6-DEV-005 guard failed: entry not found as POST_RESULT_CHANGE in deviation log")

    # 3. Historical R1 preservation check
    r1_dir = ROOT / "validation" / "article" / "r6_differential_r1"
    for r1_file, expected_sha in HISTORICAL_R1_SHA256.items():
        p = r1_dir / r1_file
        if not p.exists():
            raise RuntimeError(f"Historical R1 file missing: {p}")
        actual_sha = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual_sha != expected_sha:
            raise RuntimeError(f"Historical R1 file corrupted ({r1_file}): expected {expected_sha}, got {actual_sha}")

    # 4. Eligibility manifest verification
    if not ELIGIBILITY_MANIFEST_PATH.exists():
        raise RuntimeError(f"Corpus eligibility manifest missing: {ELIGIBILITY_MANIFEST_PATH}")
    elig_data = json.loads(ELIGIBILITY_MANIFEST_PATH.read_text(encoding="utf-8"))
    p_sum = elig_data["partitions_summary"]
    if p_sum["valid_score_producing_vectors"] != DENOMINATOR_NUMERIC:
        raise RuntimeError(f"Manifest numeric count mismatch: {p_sum['valid_score_producing_vectors']} != {DENOMINATOR_NUMERIC}")
    if p_sum["negative_validation_cases"] != DENOMINATOR_VALIDATION:
        raise RuntimeError(f"Manifest negative count mismatch: {p_sum['negative_validation_cases']} != {DENOMINATOR_VALIDATION}")
    if p_sum["total_records"] != DENOMINATOR_TOTAL:
        raise RuntimeError(f"Manifest total mismatch: {p_sum['total_records']} != {DENOMINATOR_TOTAL}")

    # 5. FIRST corpus files integrity check
    total_records = 0
    for item in CORPUS_FILES:
        fpath = FIXTURE_DIR / item["filename"]
        if not fpath.exists():
            raise RuntimeError(f"Corpus fixture missing: {fpath}")
        raw_bytes = fpath.read_bytes()
        actual_sha = hashlib.sha256(raw_bytes).hexdigest()
        if actual_sha != item["sha256"]:
            raise RuntimeError(f"Corpus SHA mismatch on {item['filename']}: expected {item['sha256']}, got {actual_sha}")
        lines = [l.strip() for l in raw_bytes.decode("utf-8").splitlines() if l.strip() and not l.startswith("#") and "Validation Reference Set" not in l]
        if len(lines) != item["expected_records"]:
            raise RuntimeError(f"Record count mismatch on {item['filename']}: expected {item['expected_records']}, got {len(lines)}")
        total_records += len(lines)

    if total_records != DENOMINATOR_TOTAL:
        raise RuntimeError(f"Total corpus denominator guard failed: expected {DENOMINATOR_TOTAL}, got {total_records}")

    print("Pre-Execution Guard PASS: all preconditions satisfied.")
    return True


def load_corpus_with_eligibility() -> list[dict]:
    """Load all 486,472 records with pre-execution deterministic eligibility classification."""
    records = []
    for item in CORPUS_FILES:
        fname = item["filename"]
        fpath = FIXTURE_DIR / fname
        lines = fpath.read_text(encoding="utf-8").splitlines()

        for idx, line in enumerate(lines, 1):
            s = line.strip()
            if not s or s.startswith("#") or "Validation Reference Set" in s:
                continue

            # Deterministic classification based on frozen FIRST fixture semantics
            if fname == "macro-vectors":
                elig = "VALID_SCORE_VECTOR"
                endpoint = "PRIMARY_NUMERIC_SCORE_CONCORDANCE"
            elif fname == "base-threat-vectors":
                elig = "VALID_SCORE_VECTOR"
                endpoint = "PRIMARY_NUMERIC_SCORE_CONCORDANCE"
            elif fname == "reference-vectors":
                if 281 <= idx <= 25308:
                    elig = "NEGATIVE_VALIDATION_CASE"
                    endpoint = "SECONDARY_NEGATIVE_VALIDATION_CONCORDANCE"
                else:
                    elig = "VALID_SCORE_VECTOR"
                    endpoint = "PRIMARY_NUMERIC_SCORE_CONCORDANCE"
            else:
                raise ValueError(f"Unknown fixture file: {fname}")

            records.append({
                "source_file": fname,
                "line_index": idx,
                "vector": s,
                "eligibility_class": elig,
                "inclusion_endpoint": endpoint,
            })

    if len(records) != DENOMINATOR_TOTAL:
        raise RuntimeError(f"Loaded records count mismatch: {len(records)} != {DENOMINATOR_TOTAL}")

    v_count = sum(1 for r in records if r["eligibility_class"] == "VALID_SCORE_VECTOR")
    n_count = sum(1 for r in records if r["eligibility_class"] == "NEGATIVE_VALIDATION_CASE")
    if v_count != DENOMINATOR_NUMERIC or n_count != DENOMINATOR_VALIDATION:
        raise RuntimeError(f"Partition count mismatch: valid={v_count} (exp {DENOMINATOR_NUMERIC}), neg={n_count} (exp {DENOMINATOR_VALIDATION})")

    return records


def derive_severity(score: float | None) -> str | None:
    """Standard FIRST CVSS v4.0 Section 4.2 qualitative severity rating intervals."""
    if score is None:
        return None
    if score == 0.0:
        return "None"
    elif 0.1 <= score <= 3.9:
        return "Low"
    elif 4.0 <= score <= 6.9:
        return "Medium"
    elif 7.0 <= score <= 8.9:
        return "High"
    elif 9.0 <= score <= 10.0:
        return "Critical"
    return "Unknown"


def evaluate_record(record: dict) -> dict:
    """Evaluate a single record against both engines according to frozen protocol R2."""
    v = record["vector"]
    elig = record["eligibility_class"]

    # 1. Primary Scorer Evaluation
    p_ok = False
    p_crash = False
    s_p = None
    sev_p = None
    p_err = None
    try:
        c = CVSS4(v)
        s_p = float(c.scores()[0])
        sev_p = str(c.severities()[0])
        p_ok = True
    except HELPUS_EXPECTED_EXCEPTIONS as exc:
        p_ok = False
        p_err = type(exc).__name__
    except Exception as exc:
        p_crash = True
        p_err = f"CRASH:{type(exc).__name__}:{exc}"

    # 2. Comparator Evaluation (stdout silenced)
    c_ok = False
    c_crash = False
    s_c = None
    sev_c = None
    c_err = None
    null_out = io.StringIO()
    with contextlib.redirect_stdout(null_out):
        try:
            s_c = cvss4py.score_vector(v)
            c_ok = True
            sev_c = derive_severity(s_c)
        except CVSS4PY_EXPECTED_EXCEPTIONS as exc:
            c_ok = False
            c_err = type(exc).__name__
        except Exception as exc:
            c_crash = True
            c_err = f"CRASH:{type(exc).__name__}:{exc}"

    delta = None
    sev_diag = "NOT_APPLICABLE"
    category = None

    if elig == "VALID_SCORE_VECTOR":
        # PRIMARY NUMERIC ENDPOINT TAXONOMY:
        # EXECUTION_ERROR > VALIDITY_DISAGREEMENT > SCORE_MISMATCH > EXACT_SCORE_MATCH
        if p_crash or c_crash:
            category = "EXECUTION_ERROR"
        elif p_ok != c_ok:
            category = "VALIDITY_DISAGREEMENT"
        elif not p_ok and not c_ok:
            # Both rejected a record marked as valid score vector
            category = "VALIDITY_DISAGREEMENT"
        else:
            delta = round(abs(s_p - s_c), 10)
            if delta >= 0.0001:
                category = "SCORE_MISMATCH"
            else:
                category = "EXACT_SCORE_MATCH"

            # Derived severity diagnostic for score-producing vectors
            if sev_p and sev_c:
                if sev_p.lower() == sev_c.lower():
                    sev_diag = "SAME_SEVERITY_BAND"
                else:
                    sev_diag = "SEVERITY_BOUNDARY_CROSSED"

    elif elig == "NEGATIVE_VALIDATION_CASE":
        # SECONDARY NEGATIVE VALIDATION ENDPOINT TAXONOMY:
        # NEGATIVE_EXECUTION_ERROR > NEGATIVE_VALIDITY_DISAGREEMENT > SYNTAX_REJECTION_CONCORDANCE
        if p_crash or c_crash:
            category = "NEGATIVE_EXECUTION_ERROR"
        elif p_ok or c_ok:
            # One or both erroneously accepted a negative/invalid case
            category = "NEGATIVE_VALIDITY_DISAGREEMENT"
        else:
            # Both rejected the invalid case via expected validation exceptions
            category = "SYNTAX_REJECTION_CONCORDANCE"
    else:
        raise ValueError(f"Unknown eligibility class: {elig}")

    return {
        "eligibility_class": elig,
        "endpoint": record["inclusion_endpoint"],
        "category": category,
        "canonical_valid": p_ok,
        "comparator_valid": c_ok,
        "canonical_score": s_p,
        "comparator_score": s_c,
        "score_delta": delta,
        "canonical_severity": sev_p,
        "comparator_derived_severity": sev_c,
        "severity_diagnostic": sev_diag,
        "canonical_error": p_err,
        "comparator_error": c_err,
    }


def run_full_pass(records: list[dict], pass_num: int) -> dict:
    """Execute all records in corpus and aggregate results across decoupled endpoints."""
    print(f"\n--- Starting R2 Full Pass {pass_num} (N = {len(records)}) ---")
    t0 = time.time()

    primary_counts = {
        "EXECUTION_ERROR": 0,
        "VALIDITY_DISAGREEMENT": 0,
        "SCORE_MISMATCH": 0,
        "EXACT_SCORE_MATCH": 0,
    }

    negative_counts = {
        "NEGATIVE_EXECUTION_ERROR": 0,
        "NEGATIVE_VALIDITY_DISAGREEMENT": 0,
        "SYNTAX_REJECTION_CONCORDANCE": 0,
    }

    severity_counts = {
        "SAME_SEVERITY_BAND": 0,
        "SEVERITY_BOUNDARY_CROSSED": 0,
        "NOT_APPLICABLE": 0,
    }

    max_delta = 0.0
    delta_distribution = {}
    mismatches = []

    for i, record in enumerate(records):
        res = evaluate_record(record)
        elig = res["eligibility_class"]
        cat = res["category"]

        if elig == "VALID_SCORE_VECTOR":
            primary_counts[cat] += 1
            severity_counts[res["severity_diagnostic"]] += 1

            if cat == "SCORE_MISMATCH":
                d = res["score_delta"]
                if d > max_delta:
                    max_delta = d
                d_key = f"{d:.1f}"
                delta_distribution[d_key] = delta_distribution.get(d_key, 0) + 1
                mismatches.append({
                    "record_index": i + 1,
                    "source_file": record["source_file"],
                    "line_index": record["line_index"],
                    "vector": record["vector"],
                    "canonical_score": res["canonical_score"],
                    "comparator_score": res["comparator_score"],
                    "delta": d,
                    "canonical_severity": res["canonical_severity"],
                    "comparator_derived_severity": res["comparator_derived_severity"],
                    "severity_diagnostic": res["severity_diagnostic"],
                    "primary_category": cat,
                    "first_reference_diagnostic": "PENDING_DIAGNOSTIC",
                })
            elif cat in ("VALIDITY_DISAGREEMENT", "EXECUTION_ERROR"):
                mismatches.append({
                    "record_index": i + 1,
                    "source_file": record["source_file"],
                    "line_index": record["line_index"],
                    "vector": record["vector"],
                    "canonical_valid": res["canonical_valid"],
                    "comparator_valid": res["comparator_valid"],
                    "canonical_error": res["canonical_error"],
                    "comparator_error": res["comparator_error"],
                    "primary_category": cat,
                })

        elif elig == "NEGATIVE_VALIDATION_CASE":
            negative_counts[cat] += 1
            if cat in ("NEGATIVE_EXECUTION_ERROR", "NEGATIVE_VALIDITY_DISAGREEMENT"):
                mismatches.append({
                    "record_index": i + 1,
                    "source_file": record["source_file"],
                    "line_index": record["line_index"],
                    "vector": record["vector"],
                    "canonical_valid": res["canonical_valid"],
                    "comparator_valid": res["comparator_valid"],
                    "canonical_error": res["canonical_error"],
                    "comparator_error": res["comparator_error"],
                    "secondary_category": cat,
                })

        if (i + 1) % 100000 == 0:
            elapsed = time.time() - t0
            print(f"  Processed {i+1}/{len(records)} records ({elapsed:.1f}s, {i+1/elapsed:.0f} rec/s)...")

    elapsed = time.time() - t0
    print(f"Completed Pass {pass_num} in {elapsed:.2f}s ({len(records)/elapsed:.1f} rec/s).")
    print(f"  Primary Numeric Endpoint (D_numeric = {DENOMINATOR_NUMERIC}):")
    print(f"    EXACT_SCORE_MATCH:     {primary_counts['EXACT_SCORE_MATCH']}")
    print(f"    SCORE_MISMATCH:        {primary_counts['SCORE_MISMATCH']}")
    print(f"    VALIDITY_DISAGREEMENT: {primary_counts['VALIDITY_DISAGREEMENT']}")
    print(f"    EXECUTION_ERROR:       {primary_counts['EXECUTION_ERROR']}")
    print(f"    Sum:                   {sum(primary_counts.values())}")
    print(f"  Secondary Negative Endpoint (D_validation = {DENOMINATOR_VALIDATION}):")
    print(f"    SYNTAX_REJECTION_CONCORDANCE:   {negative_counts['SYNTAX_REJECTION_CONCORDANCE']}")
    print(f"    NEGATIVE_VALIDITY_DISAGREEMENT: {negative_counts['NEGATIVE_VALIDITY_DISAGREEMENT']}")
    print(f"    NEGATIVE_EXECUTION_ERROR:       {negative_counts['NEGATIVE_EXECUTION_ERROR']}")
    print(f"    Sum:                            {sum(negative_counts.values())}")

    return {
        "pass_number": pass_num,
        "processed_count": len(records),
        "elapsed_seconds": elapsed,
        "primary_counts": primary_counts,
        "primary_sum": sum(primary_counts.values()),
        "negative_counts": negative_counts,
        "negative_sum": sum(negative_counts.values()),
        "severity_counts": severity_counts,
        "max_delta": max_delta,
        "delta_distribution": delta_distribution,
        "mismatches": mismatches,
    }


def main():
    parser = argparse.ArgumentParser(description="R6.2 Differential CVSS v4.0 Validation Runner")
    parser.add_argument("--authorize-execution", action="store_true", help="Authorize full execution of corpus")
    args = parser.parse_args()

    print("=" * 70)
    print("R6.2 Differential CVSS v4.0 Validation Runner (TEST-SUITE-R6-DIFFERENTIAL-CVSS40-R2)")
    print("=" * 70)

    runner_bytes = Path(__file__).read_bytes()
    runner_sha256 = hashlib.sha256(runner_bytes).hexdigest()
    print(f"Runner Path: {Path(__file__).resolve()}")
    print(f"Runner SHA-256 (Frozen pre-run): {runner_sha256}")

    if not args.authorize_execution:
        print("\n[GUARD LOCKED] Execution authorization required.")
        print("This runner is frozen under PREREGISTERED_FROZEN_NOT_EXECUTED.")
        print("Execution must be explicitly authorized via order by the supervisor.")
        sys.exit(0)

    pre_execution_guard()
    records = load_corpus_with_eligibility()
    run1 = run_full_pass(records, 1)
    run2 = run_full_pass(records, 2)

    # Parity check
    if run1["primary_counts"] != run2["primary_counts"] or run1["negative_counts"] != run2["negative_counts"]:
        raise RuntimeError("Deterministic parity check failed between Run 1 and Run 2!")
    print("\nDeterministic Rerun Parity Status: PASS")


if __name__ == "__main__":
    main()
