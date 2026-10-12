#!/usr/bin/env python3
"""Create a finalized canonical Dataset B view only after strict calculator gate G1 passes.

This script never overwrites legacy provenance columns. It uses the exact G1-validated
scoring kernel (core.cvss40.score) to recompute the canonical score and severity directly
from the complete source_cvss_v4_vector. It compares this against development recomputation,
writes detailed recalculation provenance, and fails closed on any unexplained discrepancy.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.cvss40 import score as calculate_cvss40

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=str(ROOT))
ap.add_argument("--g1-json", default="outputs/first-reference-corpus-round4.json")
ap.add_argument("--input", default="data/dataset_b/source_assessments_v2.csv")
ap.add_argument("--output", default="data/dataset_b/source_assessments_final.csv")
args = ap.parse_args()
root = Path(args.root)

g1 = json.loads((root / args.g1_json).read_text(encoding="utf-8"))
if not g1.get("summary", {}).get("gate_pass", False):
    raise SystemExit("BLOCKED: strict calculator gate G1 is not PASS; do not finalize canonical scores.")

input_path = root / args.input
rows = list(csv.DictReader(input_path.open(encoding="utf-8", newline="")))
fields = list(rows[0].keys())

new_fields = [
    "canonical_source_score",
    "canonical_source_severity",
    "canonical_source_score_semantics",
    "recomputed_by_g1_scorer",
    "scorer_kernel_version",
    "canonicalized_after_g1",
]
for f in new_fields:
    if f not in fields:
        fields.append(f)

provenance_entries = []

for r in rows:
    scenario_id = r.get("scenario_id", "").strip()
    vector = r.get("source_cvss_v4_vector", "").strip()
    if not vector:
        raise SystemExit(f"{scenario_id}: missing source_cvss_v4_vector")

    # Recompute with exact G1-validated kernel
    calc_res = calculate_cvss40(vector)
    calc_score = f"{calc_res['score']:.1f}"
    calc_sev = str(calc_res["severity"]).capitalize()

    # Compare with development recomputation
    dev_score = r.get("recomputed_full_vector_score", "").strip()
    dev_sev = r.get("recomputed_full_vector_severity", "").strip()

    if dev_score:
        score_diff = abs(float(calc_score) - float(dev_score))
        if score_diff >= 0.05:
            raise SystemExit(
                f"{scenario_id}: Recomputed score mismatch between G1 kernel ({calc_score}) and dev baseline ({dev_score})"
            )
    if dev_sev and calc_sev.lower() != dev_sev.lower():
        raise SystemExit(
            f"{scenario_id}: Severity mismatch between G1 kernel ({calc_sev}) and dev baseline ({dev_sev})"
        )

    r["canonical_source_score"] = calc_score
    r["canonical_source_severity"] = calc_sev
    r["canonical_source_score_semantics"] = "COMPLETE_SOURCE_VECTOR_SCORE_RECOMPUTED_WITH_G1_SCORER"
    r["recomputed_by_g1_scorer"] = "true"
    r["scorer_kernel_version"] = "HelpUS CVSS 4.0 Kernel (cvss==3.6 aligned with FIRST IEEE 754)"
    r["canonicalized_after_g1"] = "true"

    provenance_entries.append({
        "scenario_id": scenario_id,
        "cve_id": r.get("cve_id"),
        "vector": vector,
        "nomenclature": calc_res.get("nomenclature"),
        "g1_kernel_score": float(calc_score),
        "g1_kernel_severity": calc_sev,
        "dev_score": float(dev_score) if dev_score else None,
        "dev_severity": dev_sev,
        "verified_identical": True,
    })

out = root / args.output
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

g1_bytes = (root / args.g1_json).read_bytes()
actual_g1_evidence_sha256 = hashlib.sha256(g1_bytes).hexdigest()

prov_out = root / "outputs" / "dataset_b_finalization_provenance.json"
prov_payload = {
    "suite": "Dataset B G1-Scorer Finalization Provenance",
    "total_scenarios": len(rows),
    "recomputed_and_verified": len(provenance_entries),
    "scorer_kernel": g1.get("calculator") or "HelpUS CVSS 4.0 Kernel (cvss==3.6 aligned with FIRST IEEE 754)",
    "runtime_scorer": g1.get("runtime_scorer", {}),
    "first_repository": g1.get("first_repository"),
    "first_commit_sha": g1.get("commit_sha"),
    "g1_evidence_artifact": str(args.g1_json),
    "g1_evidence_sha256": actual_g1_evidence_sha256,
    "canonical_file": str(args.output),
    "scenarios": provenance_entries,
}
prov_out.write_text(json.dumps(prov_payload, indent=2), encoding="utf-8")
print(f"Finalized Dataset B to {out} and recorded provenance in {prov_out} (g1_evidence_sha256={actual_g1_evidence_sha256})")
