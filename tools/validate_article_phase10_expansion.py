
from pathlib import Path
import csv
import json
import re

ROOT = Path.cwd()

required = [
    ROOT / "article/ieee/cvss40_double_blind.tex",
    ROOT / "article/ieee/references.bib",
    ROOT / "article/ieee/cvss40_double_blind.pdf",
    ROOT / "article/ieee/RELATED_WORK_NOTES.md",
    ROOT / "validation/article/phase10_reproducibility_manifest.json",
]

for path in required:
    if not path.exists():
        raise FileNotFoundError(path)

tex = (
    ROOT / "article/ieee/cvss40_double_blind.tex"
).read_text(
    encoding="utf-8",
    errors="strict",
)

bib = (
    ROOT / "article/ieee/references.bib"
).read_text(
    encoding="utf-8",
    errors="strict",
)

required_sections = [
    "Background and Related Work",
    "Research Questions and Design Goals",
    "AI/Watcher Architecture",
    "Dataset and Experimental Method",
    "Results",
    "Discussion",
    "Threats to Validity",
    "Reproducibility",
    "Operational Adoption Path",
    "Conclusion",
]

for section in required_sections:
    marker = "\\section{" + section + "}"
    if marker not in tex:
        raise RuntimeError("Missing section: " + section)

required_terms = [
    "human-in-the-loop",
    "evidence coverage",
    "trace completeness",
    "not an official CVSS score",
    "does not claim",
    "curated consumer",
    "independent expert adjudication",
    "custom category delta",
]

normalized_tex = " ".join(tex.split()).lower()

for term in required_terms:
    if " ".join(term.split()).lower() not in normalized_tex:
        raise RuntimeError("Missing claim-boundary term: " + term)

forbidden_terms = [
    "ai replaces human analysts",
    "autonomous official scoring",
    "validated in production",
    "proves predictive superiority",
    "guarantees correct cvss",
    "nvd environmental context",
    "wagner",
    "helpusa",
    "d:\\dev\\cvss",
]

for term in forbidden_terms:
    if term.lower() in normalized_tex:
        raise RuntimeError("Forbidden manuscript term: " + term)

required_bib_keys = [
    "first_cvss40",
    "first_spec",
    "first_user_guide",
    "first_implementation",
    "fruhwirth2009",
    "howland2023",
    "jung2022cavp",
    "spring2021ssvc",
    "jacobs2020remediation",
    "jacobs2021epss",
    "jacobs2023epss",
    "nist80040r4",
    "koscinski2025",
    "nvd_api",
]

for key in required_bib_keys:
    if ("{" + key + ",").lower() not in bib.lower():
        raise RuntimeError("Missing bibliography key: " + key)

with (
    ROOT / "data/article/cvss40_environmental_scenarios.csv"
).open(
    "r",
    encoding="utf-8-sig",
    newline="",
) as stream:
    rows = list(csv.DictReader(stream))

nvd_rows = [
    row for row in rows
    if row.get("scenario_source")
    == "nvd_cvss_v4_with_curated_environment"
]

for row in nvd_rows:
    cve = row.get("cve_id", "").strip()

    if not cve:
        continue

    key = "nvd_" + cve.lower().replace("-", "_")

    if ("@misc{" + key + ",").lower() not in bib.lower():
        raise RuntimeError(
            "Missing NVD bibliography entry: " + cve
        )

if tex.count("\\begin{table") < 4:
    raise RuntimeError("Expected at least four tables")

if tex.count("\\begin{figure") < 1:
    raise RuntimeError("Expected at least one architecture figure")

if tex.count("\\begin{table") != tex.count("\\end{table"):
    raise RuntimeError("Unbalanced table environments")

if tex.count("\\begin{figure") != tex.count("\\end{figure"):
    raise RuntimeError("Unbalanced figure environments")

if re.search(r"__[A-Z0-9_]+__", tex):
    raise RuntimeError("Unresolved template marker")

manifest = json.loads(
    (
        ROOT / "validation/article/phase10_reproducibility_manifest.json"
    ).read_text(
        encoding="utf-8",
        errors="strict",
    )
)

page_count = int(manifest.get("pdf_page_count", 0))

if page_count < 5:
    raise RuntimeError(
        f"Manuscript too short after expansion: {page_count} pages"
    )

if page_count > 8:
    raise RuntimeError(
        f"Manuscript exceeds Phase 10 target: {page_count} pages"
    )

if not manifest.get("undefined_references") is False:
    raise RuntimeError(
        "Manifest does not confirm resolved references"
    )

print("CVSS40_PHASE10_ACADEMIC_EXPANSION_VALIDATION_OK")
print("page_count=" + str(page_count))
print("table_count=" + str(tex.count("\\begin{table")))
print("figure_count=" + str(tex.count("\\begin{figure")))
print("nvd_bibliography_entries=" + str(len(nvd_rows)))
