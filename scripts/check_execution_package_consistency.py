#!/usr/bin/env python3
"""Pre-freeze consistency checks for the HelpUS CVSS AI repository/artifact.

This script is intentionally conservative: it flags cross-document claims that
would incorrectly close a scientific release gate. It does not replace full
source audits or external validation.
"""
from __future__ import annotations
from pathlib import Path
import csv, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
notes: list[str] = []


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

# Dataset B: all canonical representations must agree on scenario IDs.
csv_path = ROOT / "data/dataset_b/source_assessments_normalized.csv"
json_path = ROOT / "data/dataset_b/scenarios.json"
if csv_path.exists() and json_path.exists():
    with csv_path.open(encoding="utf-8", newline="") as f:
        csv_ids = {row["scenario_id"] for row in csv.DictReader(f)}
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    rows = payload if isinstance(payload, list) else payload.get("scenarios", [])
    json_ids = {str(row.get("scenario_id")) for row in rows}
    if csv_ids != json_ids:
        errors.append(f"Dataset B ID mismatch: CSV-only={sorted(csv_ids-json_ids)}, JSON-only={sorted(json_ids-csv_ids)}")
else:
    errors.append("Canonical Dataset B CSV/JSON missing")

# BT rows must not ambiguously call a full-vector score a provider Base score.
if csv_path.exists():
    with csv_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row.get("source_nomenclature") == "CVSS-BT":
            cols = set(row)
            if "provider_reported_base_score" not in cols or "recomputed_full_vector_score" not in cols:
                errors.append("Dataset B schema lacks separate provider-reported Base and recomputed full-vector score fields for CVSS-BT rows")
                break

# JCS local implementation must not overclaim formal RFC conformance.
jcs = text(ROOT / "web/src/lib/jcs.ts")
if "lone high surrogate" not in jcs or "lone low surrogate" not in jcs:
    errors.append("JCS implementation lacks explicit lone-surrogate rejection")
route = text(ROOT / "web/src/app/api/analyze-environment/route.ts")
if "formal RFC 8785 conformance" not in route and "conformance corpus" not in route:
    notes.append("Audit receipt wording should explicitly qualify JCS conformance status")

# Operational priority must not be hard-coded from CVSS score inside the endpoint.
for token in ["if (score >= 9.0)", "if (score >= 7.0)", "if (score >= 4.0)"]:
    if token in route:
        errors.append("Web route still hard-codes P0-P4 directly from CVSS score instead of a versioned operational policy")
        break

# Current release-gate status must not claim G1-G8 all passed while FIRST corpus remains pending.
status = text(ROOT / "docs/scientific-validation/CURRENT_RELEASE_GATE_STATUS.md")
if not status:
    errors.append("CURRENT_RELEASE_GATE_STATUS.md missing")
if re.search(r"G1.*PASS", status, re.I) and re.search(r"FIRST.*pending|comprehensive.*pending", status, re.I):
    errors.append("Current gate status simultaneously marks G1 PASS and comprehensive FIRST validation pending")

# Production marketing terms should be absent from source snapshots when included.
for p in [ROOT / "index.html", ROOT / "web/src"]:
    if p.is_file():
        corpus = text(p)
        if re.search(r"30 Cen[aá]rios Validados|zero alucina|garantia de conformidade matem[aá]tica|Contrato Tripartite Imut[aá]vel", corpus, re.I):
            errors.append(f"Unsupported marketing claim remains in {p}")

print(json.dumps({"errors": errors, "notes": notes, "error_count": len(errors)}, ensure_ascii=False, indent=2))
sys.exit(1 if errors else 0)
