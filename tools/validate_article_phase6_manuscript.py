
from pathlib import Path
import json
import sys

ROOT = Path.cwd()

required = [
    "article/generated/cvss40_ieee_manuscript_draft.md",
    "docs/ARTICLE_COMMIT_CHECKLIST_CVSS40.md",
    "validation/article/cvss40_scenario_metrics.json",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    print("MISSING_FILES")
    for p in missing:
        print(p)
    sys.exit(1)

text = (ROOT / "article/generated/cvss40_ieee_manuscript_draft.md").read_text(encoding="utf-8", errors="replace")
lower = text.lower()

required_terms = [
    "cvss v4.0",
    "environmental metrics",
    "ai/watcher-assisted",
    "human review",
    "not as autonomous official",
    "hybrid dataset",
    "nvd",
    "trace",
    "uncertainty",
    "limitations",
    "does not modify",
]

missing_terms = [t for t in required_terms if t.lower() not in lower]
if missing_terms:
    print("MISSING_TERMS")
    for t in missing_terms:
        print(t)
    sys.exit(1)

forbidden_phrases = [
    "ai replaces human analysts",
    "validated in production",
    "proves predictive superiority",
    "modifies the cvss formula",
    "autonomously produces official cvss scores",
]

found_forbidden = [p for p in forbidden_phrases if p in lower]
if found_forbidden:
    print("FORBIDDEN_PHRASES")
    for p in found_forbidden:
        print(p)
    sys.exit(1)

metrics = json.loads((ROOT / "validation/article/cvss40_scenario_metrics.json").read_text(encoding="utf-8", errors="replace"))
if int(metrics.get("scenario_count", 0)) < 30:
    print("TOO_FEW_SCENARIOS")
    sys.exit(1)

if int(metrics.get("nvd_cvss_v4_rows", 0)) < 1:
    print("NO_NVD_ROWS")
    sys.exit(1)

print("CVSS40_PHASE6_MANUSCRIPT_VALIDATION_OK")
