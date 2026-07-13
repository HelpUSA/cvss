
from pathlib import Path
import json
import sys

ROOT = Path.cwd()

required = [
    "docs/ARTICLE_EVALUATION_RESULTS_CVSS40.md",
    "docs/ARTICLE_DATASET_PROVENANCE_CVSS40.md",
    "article/generated/cvss40_evaluation_design_section.md",
    "article/generated/cvss40_results_section.md",
    "article/generated/cvss40_discussion_section.md",
    "article/generated/cvss40_limitations_section.md",
    "validation/article/cvss40_scenario_metrics.json",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    print("MISSING_FILES")
    for p in missing:
        print(p)
    sys.exit(1)

metrics = json.loads((ROOT / "validation/article/cvss40_scenario_metrics.json").read_text(encoding="utf-8", errors="replace"))

if int(metrics.get("scenario_count", 0)) < 30:
    print("TOO_FEW_SCENARIOS")
    sys.exit(1)

text = "\n".join((ROOT / p).read_text(encoding="utf-8", errors="replace") for p in required if p.endswith(".md"))

required_terms = [
    "hybrid",
    "NVD",
    "CVSS v4.0",
    "curated",
    "Environmental",
    "human review",
    "not autonomous official CVSS scores",
    "trace",
    "uncertainty",
    "predictive superiority",
]

missing_terms = [t for t in required_terms if t.lower() not in text.lower()]
if missing_terms:
    print("MISSING_TERMS")
    for t in missing_terms:
        print(t)
    sys.exit(1)

print("CVSS40_PHASE5_ARTICLE_RESULTS_VALIDATION_OK")
