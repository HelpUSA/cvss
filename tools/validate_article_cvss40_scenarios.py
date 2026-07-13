from pathlib import Path
import csv
import json
import sys
from collections import Counter

ROOT = Path.cwd()
DATASET = ROOT / "data/article/cvss40_environmental_scenarios.csv"

REQUIRED_COLUMNS = [
    "scenario_id",
    "vulnerability_summary",
    "official_cvss_v4_vector",
    "cvss_b_score",
    "cvss_b_severity",
    "asset_class",
    "deployment_context",
    "internet_exposure",
    "privilege_context",
    "compensating_controls",
    "confidentiality_requirement",
    "integrity_requirement",
    "availability_requirement",
    "candidate_modified_metrics",
    "evidence_links",
    "evidence_summary",
    "watcher_recommendation",
    "uncertainty_flags",
    "review_required",
    "human_review_status",
    "base_priority",
    "environmental_priority",
    "priority_delta",
    "trace_json",
    "scenario_source",
]

VALID_REVIEW = {"required", "reviewed", "not_required"}
VALID_PRIORITY = {"critical", "high", "medium", "low", "defer"}
VALID_EXPOSURE = {"public", "restricted", "internal", "isolated", "unknown"}

if not DATASET.exists():
    print("DATASET_MISSING")
    sys.exit(1)

with DATASET.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    header = reader.fieldnames or []

missing_cols = [c for c in REQUIRED_COLUMNS if c not in header]
if missing_cols:
    print("MISSING_COLUMNS")
    for c in missing_cols:
        print(c)
    sys.exit(1)

if len(rows) < 30:
    print(f"TOO_FEW_ROWS {len(rows)}")
    sys.exit(1)

errors = []
ids = set()
for idx, row in enumerate(rows, 2):
    sid = row.get("scenario_id", "").strip()
    if not sid:
        errors.append(f"line {idx}: missing scenario_id")
    elif sid in ids:
        errors.append(f"line {idx}: duplicate scenario_id {sid}")
    ids.add(sid)

    for col in REQUIRED_COLUMNS:
        if not row.get(col, "").strip():
            errors.append(f"line {idx}: missing required value {col}")

    if row.get("human_review_status") not in VALID_REVIEW:
        errors.append(f"line {idx}: invalid human_review_status {row.get('human_review_status')}")

    if row.get("base_priority") not in VALID_PRIORITY:
        errors.append(f"line {idx}: invalid base_priority {row.get('base_priority')}")

    if row.get("environmental_priority") not in VALID_PRIORITY:
        errors.append(f"line {idx}: invalid environmental_priority {row.get('environmental_priority')}")

    if row.get("internet_exposure") not in VALID_EXPOSURE:
        errors.append(f"line {idx}: invalid internet_exposure {row.get('internet_exposure')}")

    try:
        float(row.get("priority_delta", ""))
    except Exception:
        errors.append(f"line {idx}: priority_delta is not numeric")

    trace_rel = row.get("trace_json", "")
    if trace_rel and not (ROOT / trace_rel).exists():
        errors.append(f"line {idx}: trace_json does not exist {trace_rel}")

if errors:
    print("SCENARIO_VALIDATION_ERRORS")
    for e in errors[:100]:
        print(e)
    if len(errors) > 100:
        print(f"... {len(errors)-100} more")
    sys.exit(1)

source_counts = Counter(row.get("scenario_source", "") for row in rows)
print("CVSS40_SCENARIO_DATASET_VALIDATION_OK")
print("rows=" + str(len(rows)))
print("source_counts=" + json.dumps(dict(source_counts), sort_keys=True))
