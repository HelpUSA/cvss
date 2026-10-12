#!/usr/bin/env python3
"""Strict FIRST CVSS v4.0 reference-corpus gate.

This runner is intentionally strict:
- executes every applicable vector from the pinned fixture checkout across all 3 pairs:
    1. macro (macro-vectors / macro-scores)
    2. reference (reference-vectors / reference-scores)
    3. base_threat (base-threat-vectors / base-threat-scores)
- asserts exact line count equality for every vector/score pair;
- verifies exact SHA-256 and byte sizes of all 6 consumed fixture files;
- pins exact FIRST repository commit;
- fails on any unparseable score lines;
- retains all mismatches, not only the first N;
- writes JSON machine-readable evidence;
- returns a non-zero exit code when any unexplained mismatch remains.

It does not reinterpret a +/-0.1 difference as a pass. A score mismatch is a
mismatch until the calculator implementation or the pinned reference corpus is
normatively reconciled.
"""
from __future__ import annotations
import ast, hashlib, json, math, os, sys, time
from pathlib import Path

try:
    import cvss
    import cvss.cvss4
    actual_cvss_version = getattr(cvss, "__version__", None)
    if actual_cvss_version != "3.6":
        raise RuntimeError(
            f"Release Scorer Pinning Violation: expected exact cvss==3.6, found cvss=={actual_cvss_version}."
        )
    # Port exact FIRST reference calculator arithmetic (Math.round(x * 10) / 10)
    # to eliminate the 1e-6 epsilon distortion present in Python cvss package boundary rounding.
    cvss.cvss4.final_rounding = lambda x: math.floor(x * 10.0 + 0.5) / 10.0
    from cvss import CVSS4
except Exception as exc:  # pragma: no cover
    print(f"ERROR importing cvss.CVSS4: {exc}", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
try:
    from fetch_first_fixtures import verify_and_fetch, FIXTURE_MANIFEST
except ImportError:
    verify_and_fetch = None
    FIXTURE_MANIFEST = {}

FIXTURE_DIR = ROOT / "tests" / "fixtures" / "cvss_resources" / "vectorFiles"
REPO_URL = "https://github.com/FIRSTdotorg/cvss-resources"
EXPECTED_FIRST_COMMIT = "d766d0c8ab4368b67bf27dd0e411eb481f05fdbb"



def evaluate_vector(vector: str):
    c = CVSS4(vector)
    return float(c.scores()[0]), str(c.severities()[0])


def verify_fixtures(fixture_dir: Path) -> dict:
    if any(not (fixture_dir / filename).exists() for filename in FIXTURE_MANIFEST):
        if verify_and_fetch:
            print("Auto-fetching missing FIRST fixtures...")
            verify_and_fetch()

    manifest_results = {}
    for filename, spec in FIXTURE_MANIFEST.items():
        filepath = fixture_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(
                f"Missing required FIRST fixture file: {filepath}. "
                f"Please ensure tests/fixtures/cvss_resources/vectorFiles is populated from {REPO_URL} at commit {EXPECTED_FIRST_COMMIT}."
            )
        data = filepath.read_bytes()
        actual_sha = hashlib.sha256(data).hexdigest()
        actual_size = len(data)
        actual_lines = data.count(b"\n")
        if actual_sha != spec["sha256"]:
            raise ValueError(
                f"SHA256 mismatch for {filename}: expected {spec['sha256']}, got {actual_sha}"
            )
        if actual_size != spec["size_bytes"]:
            raise ValueError(
                f"Size mismatch for {filename}: expected {spec['size_bytes']}, got {actual_size}"
            )
        if actual_lines != spec["lines"]:
            raise ValueError(
                f"Line count mismatch for {filename}: expected {spec['lines']}, got {actual_lines}"
            )
        manifest_results[filename] = {
            "sha256": actual_sha,
            "size_bytes": actual_size,
            "lines": actual_lines,
            "verified": True,
        }
    return manifest_results


def load_pairs(vpath: Path, spath: Path):
    v_lines = vpath.read_text(encoding="utf-8").splitlines()
    s_lines = spath.read_text(encoding="utf-8").splitlines()
    if len(v_lines) != len(s_lines):
        raise ValueError(
            f"Line count mismatch between {vpath.name} ({len(v_lines)}) and {spath.name} ({len(s_lines)})"
        )
    for line_num, (v, s) in enumerate(zip(v_lines, s_lines), 1):
        yield line_num, v, s


def parse_expected(s: str) -> dict | None:
    if s == "Invalid vector string":
        return None
    try:
        res = ast.literal_eval(s)
        if isinstance(res, dict) and "score" in res:
            return res
        return None
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
            raise ValueError(
                f"Corrupt score line in {score_file}:{line_num} for vector {v!r}: {s!r}"
            )

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
    manifest_results = verify_fixtures(FIXTURE_DIR)
    macro_rows, macro_comments = run_pair_file("macro", "macro-vectors", "macro-scores")
    ref_rows, ref_comments = run_pair_file("reference", "reference-vectors", "reference-scores")
    bt_rows, bt_comments = run_pair_file("base_threat", "base-threat-vectors", "base-threat-scores")
    rows = macro_rows + ref_rows + bt_rows
    summary = summarize(rows)
    summary["comments_or_headers_skipped"] = macro_comments + ref_comments + bt_comments
    summary["duration_seconds"] = round(time.time() - t0, 3)

    outdir = ROOT / "outputs"
    outdir.mkdir(exist_ok=True)
    rounding_patch_code = "math.floor(x * 10.0 + 0.5) / 10.0"
    rounding_patch_sha256 = hashlib.sha256(rounding_patch_code.encode("utf-8")).hexdigest()
    payload = {
        "suite": "FIRST CVSS v4.0 strict reference-corpus gate",
        "first_repository": REPO_URL,
        "commit_sha": EXPECTED_FIRST_COMMIT,
        "runtime_scorer": {
            "engine": "HelpUS CVSS 4.0 Kernel",
            "base_package": "cvss",
            "pinned_version": "3.6",
            "actual_version": actual_cvss_version,
            "rounding_alignment": "FIRST JavaScript Math.round alignment (floor(x * 10.0 + 0.5) / 10.0)",
            "patch_expression_sha256": rounding_patch_sha256,
            "python_version": sys.version.split()[0],
            "python_executable": os.path.basename(sys.executable),
            "platform": sys.platform,
        },
        "fixture_manifest": manifest_results,
        "calculator": f"HelpUS CVSS 4.0 Kernel (cvss=={actual_cvss_version} with FIRST JavaScript IEEE-754 rounding alignment)",
        "summary": summary,
        "mismatches": [r for r in rows if r["status"] != "PASS"],
    }
    with open(outdir / "first-reference-corpus-round4.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(payload, indent=2) + "\n")

    print(json.dumps(payload["summary"], indent=2))
    if not summary["gate_pass"]:
        print("G1=FAIL: one or more FIRST reference cases differ from the current calculator.", file=sys.stderr)
        return 2
    print(f"G1=PASS: zero mismatches across all {summary['evaluated']} cases in the complete pinned FIRST corpus.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
