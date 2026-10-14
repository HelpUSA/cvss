#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data/dataset_b/source_assessments_v2.csv"
errors=[]
with P.open(encoding="utf-8", newline="") as f:
    rows=list(csv.DictReader(f))
if len(rows)!=30: errors.append(f"expected 30 rows, found {len(rows)}")
for r in rows:
    if r.get("source_nomenclature") == "CVSS-BT":
        if not r.get("recomputed_full_vector_score"):
            errors.append(f"{r['scenario_id']}: BT row missing recomputed full-vector score")
        if r.get("provider_reported_score_audit_status") != "AUDITED":
            errors.append(f"{r['scenario_id']}: provider-reported Base score not independently audited")
    if r.get("base_vector_origin") not in {"CNA_PUBLISHED","NVD_ANALYZED","INVESTIGATOR_AUTHORED","SYNTHETIC"}:
        errors.append(f"{r['scenario_id']}: invalid base_vector_origin={r.get('base_vector_origin')}")
print("PASS" if not errors else "FAIL")
for e in errors: print("-",e)
sys.exit(1 if errors else 0)
