
from pathlib import Path
import csv
import sys

ROOT = Path.cwd()

required_files = [
    "docs/CVSS40_OFFICIAL_READING_NOTES.md",
    "docs/ARTICLE_CLAIM_GUARDRAILS_CVSS40.md",
    "docs/ARTICLE_CVSS40_CONTRIBUTION_MAP.md",
    "docs/ARTICLE_DATASET_SCHEMA.md",
    "docs/ARTICLE_EXPERIMENT_DESIGN_CVSS40.md",
    "docs/ARTICLE_IEEE_SKELETON_CVSS40_AI_WATCHER.md",
    "data/article/cvss40_environmental_scenarios.csv",
]

missing = [p for p in required_files if not (ROOT / p).exists()]
if missing:
    print("MISSING_FILES")
    for p in missing:
        print(p)
    sys.exit(1)

combined = "\n".join((ROOT / p).read_text(encoding="utf-8", errors="replace") for p in required_files if p.endswith(".md"))

required_terms = [
    "CVSS v4.0",
    "Base",
    "Threat",
    "Environmental",
    "Supplemental",
    "CVSS-B",
    "CVSS-BE",
    "human review",
    "evidence",
    "trace",
    "uncertainty",
    "does not modify",
]

missing_terms = [t for t in required_terms if t.lower() not in combined.lower()]
if missing_terms:
    print("MISSING_TERMS")
    for t in missing_terms:
        print(t)
    sys.exit(1)

csv_path = ROOT / "data/article/cvss40_environmental_scenarios.csv"
with csv_path.open("r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)

required_columns = [
    "scenario_id",
    "cve_id",
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
    "threat_context",
    "supplemental_context",
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
]

missing_columns = [c for c in required_columns if c not in header]
if missing_columns:
    print("MISSING_COLUMNS")
    for c in missing_columns:
        print(c)
    sys.exit(1)

print("CVSS40_DOCS_VALIDATION_OK")
