
from pathlib import Path
import json
import sys

ROOT = Path.cwd()

required = [
    "article/generated/cvss40_ieee_manuscript_polished.md",
    "article/generated/cvss40_ieee_manuscript_double_blind.md",
    "docs/ARTICLE_REFERENCES_CVSS40.md",
    "docs/ARTICLE_SUBMISSION_READINESS_CVSS40.md",
    "validation/article/cvss40_scenario_metrics.json",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    print("MISSING_FILES")
    for p in missing:
        print(p)
    sys.exit(1)

polished = (ROOT / "article/generated/cvss40_ieee_manuscript_polished.md").read_text(encoding="utf-8", errors="replace")
double_blind = (ROOT / "article/generated/cvss40_ieee_manuscript_double_blind.md").read_text(encoding="utf-8", errors="replace")
refs = (ROOT / "docs/ARTICLE_REFERENCES_CVSS40.md").read_text(encoding="utf-8", errors="replace")

required_terms = [
    "CVSS v4.0",
    "Environmental metrics",
    "AI/watcher-assisted",
    "human review",
    "does not modify",
    "autonomous official",
    "hybrid dataset",
    "NVD",
    "References",
    "[1]",
]

combined = polished + "\n" + double_blind + "\n" + refs
missing_terms = [t for t in required_terms if t.lower() not in combined.lower()]
if missing_terms:
    print("MISSING_TERMS")
    for t in missing_terms:
        print(t)
    sys.exit(1)

forbidden_in_double_blind = [
    "Wagner / CVSS project",
    "owner:",
]
found = [t for t in forbidden_in_double_blind if t.lower() in double_blind.lower()]
if found:
    print("DOUBLE_BLIND_METADATA_FOUND")
    for t in found:
        print(t)
    sys.exit(1)

metrics = json.loads((ROOT / "validation/article/cvss40_scenario_metrics.json").read_text(encoding="utf-8", errors="replace"))
if int(metrics.get("nvd_cvss_v4_rows", 0)) < 1:
    print("NO_NVD_ROWS")
    sys.exit(1)

for rel in [
    "tools/article_cvss40_phase4c_nvd_safe_paged_scan.py",
    "tools/article_cvss40_phase7_precommit_clean_validate.py",
]:
    text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
    if text.endswith("\n\n"):
        print("EXTRA_BLANK_EOF", rel)
        sys.exit(1)

print("CVSS40_PHASE8_POLISH_REFERENCES_VALIDATION_OK")
