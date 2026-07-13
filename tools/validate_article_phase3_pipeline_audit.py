from pathlib import Path
import sys

ROOT = Path.cwd()
required = [
    "docs/ARTICLE_PIPELINE_INTEGRATION_AUDIT_CVSS40.md",
    "docs/ARTICLE_PHASE3_IMPLEMENTATION_PLAN_CVSS40.md",
    "docs/ARTICLE_DATASET_SCHEMA.md",
    "data/article/cvss40_environmental_scenarios.csv",
]
missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    print("MISSING")
    for p in missing:
        print(p)
    sys.exit(1)

audit = (ROOT / "docs/ARTICLE_PIPELINE_INTEGRATION_AUDIT_CVSS40.md").read_text(encoding="utf-8", errors="replace")
for term in [
    "Dataset status",
    "Top relevant files",
    "Required field implementation visibility",
    "Integration gaps",
    "Recommended implementation order",
]:
    if term not in audit:
        print("MISSING_AUDIT_TERM", term)
        sys.exit(1)

print("CVSS40_PHASE3_PIPELINE_AUDIT_VALIDATION_OK")
