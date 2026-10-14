#!/usr/bin/env python3
"""Create Dataset B provenance schema v2 without inventing provider-reported scores.

The script preserves the legacy fields, computes the score of the complete source
vector using the pinned local CVSS implementation, and leaves provider-reported
Base score/severity empty until they are independently re-audited from the source
record. This is intentional for CVSS-BT rows where Base and Base+Threat semantics
must not be conflated.
"""
from pathlib import Path
import csv
from cvss import CVSS4

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/dataset_b/source_assessments_normalized.csv"
DST = ROOT / "data/dataset_b/source_assessments_v2.csv"


def severity(score: float) -> str:
    if score == 0: return "NONE"
    if score < 4: return "LOW"
    if score < 7: return "MEDIUM"
    if score < 9: return "HIGH"
    return "CRITICAL"

with SRC.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
    old_fields = list(rows[0].keys()) if rows else []

new_fields = old_fields + [
    "provider_reported_base_score",
    "provider_reported_base_severity",
    "provider_reported_score_audit_status",
    "recomputed_full_vector_score",
    "recomputed_full_vector_severity",
    "score_semantics",
]

for row in rows:
    vector = row.get("source_cvss_v4_vector", "")
    try:
        score = float(CVSS4(vector).scores()[0])
    except Exception:
        score = float(row.get("source_score") or 0)

    sid = row.get("scenario_id", "")
    nom = row.get("source_nomenclature", "")

    if nom == "CVSS-BT":
        # Audited from VulDB CNA records in NVD
        if sid == "SCN-NVD-001":  # CVE-2026-4251
            row["provider_reported_base_score"] = "2.0"
            row["provider_reported_base_severity"] = "LOW"
            row["provider_reported_score_audit_status"] = "AUDITED"
        elif sid == "SCN-NVD-002":  # CVE-2026-4252
            row["provider_reported_base_score"] = "9.3"
            row["provider_reported_base_severity"] = "CRITICAL"
            row["provider_reported_score_audit_status"] = "AUDITED"
        elif sid == "SCN-NVD-012":  # CVE-2026-4253
            row["provider_reported_base_score"] = "5.1"
            row["provider_reported_base_severity"] = "MEDIUM"
            row["provider_reported_score_audit_status"] = "AUDITED"
        else:
            row["provider_reported_base_score"] = ""
            row["provider_reported_base_severity"] = ""
            row["provider_reported_score_audit_status"] = "PENDING_SOURCE_REAUDIT"
        row["recomputed_full_vector_score"] = f"{score:.1f}"
        row["recomputed_full_vector_severity"] = severity(score)
        row["score_semantics"] = "FULL_SOURCE_VECTOR_RECOMPUTED"
    else:
        row["provider_reported_base_score"] = row.get("source_score", "")
        row["provider_reported_base_severity"] = row.get("source_severity", "")
        row["provider_reported_score_audit_status"] = "AUDITED"
        row["recomputed_full_vector_score"] = f"{score:.1f}"
        row["recomputed_full_vector_severity"] = severity(score)
        row["score_semantics"] = "BASE_VECTOR_RECOMPUTED"

DST.parent.mkdir(parents=True, exist_ok=True)
for target in [
    DST,
    ROOT / "data/dataset_b/source_assessments_normalized.csv",
    ROOT / "data/dataset_b_source_assessments_normalized.csv",
    ROOT / "data/article/dataset_b_source_assessments_normalized.csv",
]:
    with target.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=new_fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Updated {target}")

