
from pathlib import Path
import csv
import json
import sys

ROOT = Path.cwd()

required = [
    "article/ieee/cvss40_double_blind.tex",
    "article/ieee/references.bib",
    "article/ieee/README.md",
    "article/ieee/.gitignore",
    "docs/ARTICLE_IEEE_LATEX_READINESS_CVSS40.md",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    print("MISSING_FILES")
    for p in missing:
        print(p)
    sys.exit(1)

tex = (ROOT / "article/ieee/cvss40_double_blind.tex").read_text(
    encoding="utf-8",
    errors="replace",
)

bib = (ROOT / "article/ieee/references.bib").read_text(
    encoding="utf-8",
    errors="replace",
)

required_terms = [
    "\\documentclass[conference]{IEEEtran}",
    "Anonymous Author(s)",
    "\\begin{abstract}",
    "\\section{Evaluation Design}",
    "\\section{Results}",
    "\\section{Limitations and Threats to Validity}",
    "\\bibliographystyle{IEEEtran}",
    "\\bibliography{references}",
    "does not modify",
    "not an official CVSS Environmental score difference",
]

normalized_tex = " ".join(tex.split()).lower()

for term in required_terms:
    normalized_term = " ".join(term.split()).lower()
    if normalized_term not in normalized_tex:
        print("MISSING_TEX_TERM", term)
        sys.exit(1)

forbidden = [
    "Wagner",
    "HelpUSA",
    "D:\\dev\\cvss",
    "owner:",
    "validated in production",
    "proves predictive superiority",
]

for term in forbidden:
    normalized_term = " ".join(term.split()).lower()
    if normalized_term in normalized_tex:
        print("FORBIDDEN_DOUBLE_BLIND_TERM", term)
        sys.exit(1)

if tex.count("\\begin{table}") != 3:
    print("INVALID_TABLE_COUNT", tex.count("\\begin{table}"))
    sys.exit(1)

if tex.count("\\begin{table}") != tex.count("\\end{table}"):
    print("UNBALANCED_TABLES")
    sys.exit(1)

with (
    ROOT / "data/article/cvss40_environmental_scenarios.csv"
).open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

nvd_rows = [
    row for row in rows
    if row.get("scenario_source") == "nvd_cvss_v4_with_curated_environment"
]

for row in nvd_rows:
    cve = row.get("cve_id", "")
    key = "nvd_" + cve.lower().replace("-", "_")
    if ("@misc{" + key).lower() not in bib.lower():
        print("MISSING_NVD_BIB_ENTRY", cve)
        sys.exit(1)

metrics = json.loads(
    (
        ROOT / "validation/article/cvss40_scenario_metrics.json"
    ).read_text(encoding="utf-8")
)

if int(metrics.get("scenario_count", 0)) < 30:
    print("TOO_FEW_SCENARIOS")
    sys.exit(1)

if int(metrics.get("nvd_cvss_v4_rows", 0)) < 1:
    print("NO_NVD_ROWS")
    sys.exit(1)

print("CVSS40_PHASE9_IEEE_LATEX_VALIDATION_OK")
print("nvd_bibliography_entries=" + str(len(nvd_rows)))
print("table_count=" + str(tex.count("\\begin{table}")))
