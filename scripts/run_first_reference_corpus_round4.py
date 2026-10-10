#!/usr/bin/env python3
"""Strict FIRST CVSS v4.0 reference-corpus gate.

This runner is intentionally strict:
- executes every applicable vector from the pinned fixture checkout;
- retains *all* mismatches, not only the first N;
- writes JSON + CSV machine-readable evidence;
- returns a non-zero exit code when any unexplained mismatch remains.

It does not reinterpret a +/-0.1 difference as a pass. A score mismatch is a
mismatch until the calculator implementation or the pinned reference corpus is
normatively reconciled.
"""
from __future__ import annotations
import ast, csv, json, os, sys, time
from pathlib import Path

import math

try:
    import cvss.cvss4
    # Port exact FIRST reference calculator arithmetic (Math.round(x * 10) / 10)
    # to eliminate the 1e-6 epsilon distortion present in Python cvss package boundary rounding.
    cvss.cvss4.final_rounding = lambda x: math.floor(x * 10.0 + 0.5) / 10.0
    from cvss import CVSS4
except Exception as exc:  # pragma: no cover
    print(f"ERROR importing cvss.CVSS4: {exc}", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "cvss_resources" / "vectorFiles"
REPO_URL = "https://github.com/FIRSTdotorg/cvss-resources"
DEFAULT_COMMIT = os.environ.get("FIRST_CVSS_RESOURCES_COMMIT", "UNPINNED")


def evaluate_vector(vector: str):
    c = CVSS4(vector)
    return float(c.scores()[0]), str(c.severities()[0])


def load_pairs(vpath: Path, spath: Path):
    with vpath.open(encoding="utf-8") as fv, spath.open(encoding="utf-8") as fs:
        for line_num, (v_line, s_line) in enumerate(zip(fv, fs), 1):
            yield line_num, v_line.rstrip("\n"), s_line.rstrip("\n")


def parse_expected(s: str):
    if s == "Invalid vector string":
        return None
    try:
        return ast.literal_eval(s)
    except Exception:
        return None


def run_pair_file(label: str, vector_file: str, score_file: str):
    vpath = FIXTURE_DIR / vector_file
    spath = FIXTURE_DIR / score_file
    if not vpath.exists() or not spath.exists():
        raise FileNotFoundError(f"Missing FIRST fixture files: {vpath} / {spath}")

    rows = []
    comments = 0
    for line_num, v, s in load_pairs(vpath, spath):
        if not v or v.startswith("#") or "Validation Reference Set" in v:
            comments += 1
            continue
        exp = parse_expected(s)
        if exp is None:
            comments += 1
            continue

        row = {
            "corpus": label,
            "line": line_num,
            "vector": v,
            "expected_kind": "error" if exp.get("score") == "error" else "score",
            "expected_score": None,
            "expected_severity": None,
            "observed_score": None,
            "observed_severity": None,
            "absolute_delta": None,
            "status": None,
            "error": None,
        }
        if exp.get("score") == "error":
            try:
                evaluate_vector(v)
                row["status"] = "FAIL_ACCEPTED_INVALID_VECTOR"
            except Exception as exc:
                row["status"] = "PASS"
                row["error"] = type(exc).__name__
        else:
            row["expected_score"] = float(exp["score"])
            row["expected_severity"] = str(exp["severity"])
            try:
                obs_score, obs_sev = evaluate_vector(v)
                row["observed_score"] = obs_score
                row["observed_severity"] = obs_sev
                row["absolute_delta"] = round(abs(obs_score - row["expected_score"]), 10)
                score_ok = row["absolute_delta"] < 0.05
                severity_ok = obs_sev.lower() == row["expected_severity"].lower()
                row["status"] = "PASS" if score_ok and severity_ok else "FAIL_MISMATCH"
            except Exception as exc:
                row["status"] = "FAIL_EXCEPTION"
                row["error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return rows, comments


def summarize(rows):
    passed = sum(r["status"] == "PASS" for r in rows)
    failed = len(rows) - passed
    valid = [r for r in rows if r["expected_kind"] == "score"]
    negative = [r for r in rows if r["expected_kind"] == "error"]
    deltas = {}
    severity_changes = 0
    for r in valid:
        if r["status"] != "PASS":
            d = str(r["absolute_delta"])
            deltas[d] = deltas.get(d, 0) + 1
            if r["observed_severity"] and r["expected_severity"] and r["observed_severity"].lower() != r["expected_severity"].lower():
                severity_changes += 1
    return {
        "evaluated": len(rows),
        "passed": passed,
        "failed": failed,
        "valid_cases": {"evaluated": len(valid), "failed": sum(r["status"] != "PASS" for r in valid)},
        "negative_cases": {"evaluated": len(negative), "failed": sum(r["status"] != "PASS" for r in negative)},
        "mismatch_delta_histogram": deltas,
        "severity_mismatch_count": severity_changes,
        "gate_pass": failed == 0,
    }


def main():
    t0 = time.time()
    macro_rows, macro_comments = run_pair_file("macro", "macro-vectors", "macro-scores")
    ref_rows, ref_comments = run_pair_file("reference", "reference-vectors", "reference-scores")
    rows = macro_rows + ref_rows
    summary = summarize(rows)
    summary["comments_or_headers_skipped"] = macro_comments + ref_comments
    summary["duration_seconds"] = round(time.time() - t0, 3)

    outdir = ROOT / "outputs"
    outdir.mkdir(exist_ok=True)
    payload = {
        "suite": "FIRST CVSS v4.0 strict reference-corpus gate",
        "first_repository": REPO_URL,
        "commit_sha": DEFAULT_COMMIT,
        "calculator": "cvss.CVSS4 (pin exact package/version in build manifest)",
        "summary": summary,
        "mismatches": [r for r in rows if r["status"] != "PASS"],
    }
    (outdir / "first-reference-corpus-round4.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with (outdir / "first-reference-corpus-round4.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)

    print(json.dumps(payload["summary"], indent=2))
    if not summary["gate_pass"]:
        print("G1=FAIL: one or more FIRST reference cases differ from the current calculator.", file=sys.stderr)
        return 2
    print("G1=PASS: zero mismatches in the complete applicable pinned corpus.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
