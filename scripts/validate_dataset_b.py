#!/usr/bin/env python3
"""Validate Dataset B structural invariants without asserting external CVE correctness."""
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/article/dataset_b_source_assessments_normalized.csv"
ENV = {"CR","IR","AR","MAV","MAC","MAT","MPR","MUI","MVC","MVI","MVA","MSC","MSI","MSA"}
VALID_DISP = {"P0_IMMEDIATE","P1_EXPEDITED","P2_SCHEDULED","P3_MONITOR","P4_DEFER_RECOMMENDED"}

def expected_nomenclature(vector: str) -> str:
    p = {}
    for item in vector.split("/"):
        if ":" in item:
            k,v = item.split(":",1); p[k]=v
    threat = p.get("E", "X") != "X"
    environmental = any(p.get(k, "X") != "X" for k in ENV)
    return "CVSS-BTE" if threat and environmental else ("CVSS-BT" if threat else ("CVSS-BE" if environmental else "CVSS-B"))

errors=[]
with PATH.open(newline="",encoding="utf-8") as f:
    rows=list(csv.DictReader(f))
seen=set()
for i,r in enumerate(rows, start=2):
    sid=r["scenario_id"]
    if sid in seen: errors.append(f"line {i}: duplicate scenario_id {sid}")
    seen.add(sid)
    exp=expected_nomenclature(r["source_cvss_v4_vector"])
    if r["source_nomenclature"] != exp:
        errors.append(f"line {i}: {sid} nomenclature {r['source_nomenclature']} != {exp}")
    if r["legacy_operational_disposition"] not in VALID_DISP:
        errors.append(f"line {i}: {sid} invalid operational disposition")
    if r.get("base_vector_origin") == "CNA_PUBLISHED" and not r.get("cve_id"):
        errors.append(f"line {i}: {sid} CNA_PUBLISHED without CVE")

print(f"rows={len(rows)} errors={len(errors)}")
for e in errors: print(e)
sys.exit(1 if errors else 0)
