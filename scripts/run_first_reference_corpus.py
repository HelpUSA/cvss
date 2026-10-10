#!/usr/bin/env python3
"""Run the official FIRST reference corpus from FIRSTdotorg/cvss-resources.

Pinned repository: https://github.com/FIRSTdotorg/cvss-resources
Pinned commit: d766d0c8ab4368b67bf27dd0e411eb481f05fdbb
Consumes: vectorFiles/reference-vectors and vectorFiles/reference-scores (66,331 lines)
Plus: vectorFiles/macro-vectors and vectorFiles/macro-scores (270 lines)
"""
import ast
import json
import time
from pathlib import Path
from cvss import CVSS4

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "cvss_resources" / "vectorFiles"
REPO_URL = "https://github.com/FIRSTdotorg/cvss-resources"
COMMIT_SHA = "d766d0c8ab4368b67bf27dd0e411eb481f05fdbb"

def run_macro_corpus():
    print("--> Running 270 FIRST Macro Vectors...")
    vec_path = FIXTURE_DIR / "macro-vectors"
    score_path = FIXTURE_DIR / "macro-scores"
    vectors = vec_path.read_text().splitlines()
    scores = score_path.read_text().splitlines()

    passed = 0
    failed = 0
    mismatches = []

    for idx, (v, s_str) in enumerate(zip(vectors, scores), 1):
        v = v.strip()
        if not v or v.startswith("#"):
            continue
        exp = ast.literal_eval(s_str.strip())
        exp_score = float(exp["score"])
        exp_sev = exp["severity"]

        try:
            c = CVSS4(v)
            obs_score = float(c.scores()[0])
            obs_sev = c.severities()[0]
            ok = abs(obs_score - exp_score) < 0.05 and obs_sev.lower() == exp_sev.lower()
            if ok:
                passed += 1
            else:
                failed += 1
                mismatches.append({"index": idx, "vector": v, "expected": exp, "observed": {"score": obs_score, "severity": obs_sev}})
        except Exception as e:
            failed += 1
            mismatches.append({"index": idx, "vector": v, "expected": exp, "error": str(e)})

    return {"total": passed + failed, "passed": passed, "failed": failed, "mismatches": mismatches}

def run_reference_corpus(max_cases=None):
    print("--> Running FIRST Reference Set (Valid + Negative)...")
    vec_path = FIXTURE_DIR / "reference-vectors"
    score_path = FIXTURE_DIR / "reference-scores"

    valid_passed = 0
    valid_failed = 0
    neg_passed = 0
    neg_failed = 0
    skipped_comments = 0
    mismatches = []

    t0 = time.time()
    with open(vec_path, encoding="utf-8") as fv, open(score_path, encoding="utf-8") as fs:
        line_num = 0
        for v_line, s_line in zip(fv, fs):
            line_num += 1
            if max_cases and line_num > max_cases:
                break
            v = v_line.strip()
            s = s_line.strip()

            if not v or v.startswith("#") or "Validation Reference Set" in v:
                skipped_comments += 1
                continue

            if s == "Invalid vector string":
                # Header lines or unparseable comment lines that FIRST check script marked invalid
                skipped_comments += 1
                continue

            try:
                exp = ast.literal_eval(s)
            except Exception:
                skipped_comments += 1
                continue

            if exp.get("score") == "error":
                # NEGATIVE TEST
                try:
                    CVSS4(v)
                    # Should have raised error
                    neg_failed += 1
                    if len(mismatches) < 20:
                        mismatches.append({"line": line_num, "type": "negative", "vector": v, "expected_error": exp.get("error"), "status": "FAIL_ACCEPTED_BY_CALCULATOR"})
                except Exception:
                    neg_passed += 1
            else:
                # VALID TEST
                try:
                    exp_score = float(exp["score"])
                    exp_sev = exp["severity"]
                    c = CVSS4(v)
                    obs_score = float(c.scores()[0])
                    obs_sev = c.severities()[0]
                    ok = abs(obs_score - exp_score) < 0.05 and obs_sev.lower() == exp_sev.lower()
                    if ok:
                        valid_passed += 1
                    else:
                        valid_failed += 1
                        if len(mismatches) < 20:
                            mismatches.append({"line": line_num, "type": "valid", "vector": v, "expected": {"score": exp_score, "severity": exp_sev}, "observed": {"score": obs_score, "severity": obs_sev}})
                except Exception as e:
                    valid_failed += 1
                    if len(mismatches) < 20:
                        mismatches.append({"line": line_num, "type": "valid", "vector": v, "error": str(e)})

            if line_num % 10000 == 0:
                print(f"    ... processed {line_num} lines ({valid_passed} valid pass, {neg_passed} neg pass, {valid_failed + neg_failed} fail)")

    dur = time.time() - t0
    total_eval = valid_passed + valid_failed + neg_passed + neg_failed
    print(f"--> Reference set finished in {dur:.2f}s: {total_eval} evaluated ({valid_passed} valid, {neg_passed} negative), {valid_failed + neg_failed} failed.")

    return {
        "lines_processed": line_num,
        "total_evaluated": total_eval,
        "valid_cases": {"passed": valid_passed, "failed": valid_failed},
        "negative_cases": {"passed": neg_passed, "failed": neg_failed},
        "skipped_comments": skipped_comments,
        "duration_seconds": round(dur, 2),
        "mismatches": mismatches,
    }

def main():
    print("=== EXECUTING FULL FIRST CVSS v4.0 REFERENCE CORPUS (GATE G1) ===")
    print(f"Repository: {REPO_URL}")
    print(f"Commit SHA: {COMMIT_SHA}")
    print(f"Calculator: Red Hat cvss==3.6\n")

    macro_res = run_macro_corpus()
    ref_res = run_reference_corpus()

    total_all = macro_res["total"] + ref_res["total_evaluated"]
    total_passed = macro_res["passed"] + ref_res["valid_cases"]["passed"] + ref_res["negative_cases"]["passed"]
    total_failed = macro_res["failed"] + ref_res["valid_cases"]["failed"] + ref_res["negative_cases"]["failed"]

    overall_conformance = (total_passed / total_all) * 100 if total_all else 0.0

    summary = {
        "suite": "Official FIRST CVSS v4.0 Reference Corpus Execution",
        "gate": "G1",
        "first_repository": REPO_URL,
        "commit_sha": COMMIT_SHA,
        "checkout_date": "2026-10-09",
        "calculator_package": "cvss==3.6 (Red Hat specification implementation)",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": {
            "total_cases_evaluated": total_all,
            "passed": total_passed,
            "failed": total_failed,
            "conformance_rate": f"{overall_conformance:.4f}%",
        },
        "macro_corpus": macro_res,
        "reference_corpus": ref_res,
    }

    out_file = ROOT / "outputs" / "first-reference-corpus-results.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nResults saved to {out_file}")
    print(f"TOTAL: {total_all:,} evaluated | PASSED: {total_passed:,} | FAILED: {total_failed} ({overall_conformance:.2f}%)")

if __name__ == "__main__":
    main()
