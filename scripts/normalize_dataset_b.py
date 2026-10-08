#!/usr/bin/env python3
"""Legacy-to-canonical Dataset B migration helper.

IMPORTANT: This script does NOT fetch authoritative CVE data and MUST NOT overwrite the
source-audited canonical file.  It converts the legacy development CSV into a *draft migration*
that can be compared with `dataset_b_source_assessments_normalized.csv` during local audit.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/article/cvss40_environmental_scenarios.csv"
OUT = ROOT / "data/article/dataset_b_source_assessments_migrated_draft.csv"
ENV = {"CR","IR","AR","MAV","MAC","MAT","MPR","MUI","MVC","MVI","MVA","MSC","MSI","MSA"}
DISP = {
    "critical":"P0_IMMEDIATE",
    "high":"P1_EXPEDITED",
    "medium":"P2_SCHEDULED",
    "low":"P3_MONITOR",
    "defer":"P4_DEFER_RECOMMENDED",
}

def nomenclature(vector: str) -> str:
    parts = {}
    for item in vector.split("/"):
        if ":" in item:
            key, value = item.split(":", 1)
            parts[key] = value
    threat = parts.get("E", "X") != "X"
    environmental = any(parts.get(k, "X") != "X" for k in ENV)
    if threat and environmental:
        return "CVSS-BTE"
    if threat:
        return "CVSS-BT"
    if environmental:
        return "CVSS-BE"
    return "CVSS-B"

with SRC.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

fields = [
    "scenario_id","cve_id","source_cvss_v4_vector","source_nomenclature",
    "legacy_source_score","legacy_source_severity","legacy_provider_hint","source_url",
    "asset_class","legacy_operational_disposition","legacy_priority_delta","audit_status"
]
with OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        vector = row["official_cvss_v4_vector"]
        writer.writerow({
            "scenario_id": row["scenario_id"],
            "cve_id": row.get("cve_id", ""),
            "source_cvss_v4_vector": vector,
            "source_nomenclature": nomenclature(vector),
            "legacy_source_score": row.get("cvss_b_score", ""),
            "legacy_source_severity": row.get("cvss_b_severity", ""),
            "legacy_provider_hint": row.get("cvss_source", ""),
            "source_url": row.get("source_url", ""),
            "asset_class": row.get("asset_class", ""),
            "legacy_operational_disposition": DISP.get(row.get("environmental_priority", "").lower(), "PENDING_MAPPING"),
            "legacy_priority_delta": row.get("priority_delta", ""),
            "audit_status": "PENDING_AUTHORITATIVE_SOURCE_RETRIEVAL",
        })
print(OUT)
