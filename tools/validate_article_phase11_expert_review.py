
from pathlib import Path
import csv
import json
import re

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"

required = [
    REVIEW / "PROTOCOL.md",
    REVIEW / "REVIEWER_INSTRUCTIONS.md",
    REVIEW / "CODEBOOK.md",
    REVIEW / "ANALYSIS_PLAN.md",
    REVIEW / "ETHICS_AND_DATA_HANDLING.md",
    REVIEW / "blinded_scenarios_master.csv",
    REVIEW / "review_packet_A.csv",
    REVIEW / "review_packet_B.csv",
    REVIEW / "reviewer_response_template.csv",
    REVIEW / "reviewer_assignment_plan.csv",
    REVIEW / "adjudication_answer_key.csv",
    ROOT / "validation/article/phase11_expert_review_manifest.json",
    ROOT / "article/ieee/cvss40_double_blind.tex",
    ROOT / "article/ieee/cvss40_double_blind.pdf",
]

for path in required:
    if not path.exists():
        raise FileNotFoundError(path)

def csv_rows(path):
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as stream:
        return list(csv.DictReader(stream))

master = csv_rows(REVIEW / "blinded_scenarios_master.csv")
packet_a = csv_rows(REVIEW / "review_packet_A.csv")
packet_b = csv_rows(REVIEW / "review_packet_B.csv")
answers = csv_rows(REVIEW / "adjudication_answer_key.csv")
responses = csv_rows(REVIEW / "reviewer_response_template.csv")
assignments = csv_rows(REVIEW / "reviewer_assignment_plan.csv")

expected = len(master)

if expected != 30:
    raise RuntimeError(
        f"Expected 30 blinded scenarios, found {expected}"
    )

for name, rows in [
    ("packet A", packet_a),
    ("packet B", packet_b),
    ("answer key", answers),
    ("response template", responses),
]:
    if len(rows) != expected:
        raise RuntimeError(
            f"{name} count mismatch: {len(rows)} != {expected}"
        )

master_ids = {
    row["review_scenario_id"]
    for row in master
}

for name, rows in [
    ("packet A", packet_a),
    ("packet B", packet_b),
    ("answer key", answers),
    ("response template", responses),
]:
    ids = {
        row["review_scenario_id"]
        for row in rows
    }

    if ids != master_ids:
        raise RuntimeError(
            f"{name} scenario IDs do not match master"
        )

for row in master:
    serialized = " ".join(
        str(value)
        for value in row.values()
    ).lower()

    forbidden = [
        "cve-",
        "source_url",
        "candidate",
        "recommendation",
        "priority_delta",
        "watcher rationale",
    ]

    for term in forbidden:
        if term in serialized:
            raise RuntimeError(
                f"Blinding failure for "
                f"{row['review_scenario_id']}: {term}"
            )

if len(assignments) < 3:
    raise RuntimeError("Expected at least three reviewer assignments")

tex = (
    ROOT / "article/ieee/cvss40_double_blind.tex"
).read_text(
    encoding="utf-8",
    errors="strict",
)

required_tex_terms = [
    "\\section{Planned Independent Expert Evaluation}",
    "Blinded Review Design",
    "Agreement Measures",
    "Adjudication",
    "No expert agreement results are claimed",
]

normalized_tex = " ".join(tex.split()).lower()

for term in required_tex_terms:
    normalized_term = " ".join(term.split()).lower()

    if normalized_term not in normalized_tex:
        raise RuntimeError(
            "Missing Phase 11 manuscript term: " + term
        )

manifest = json.loads(
    (
        ROOT / "validation/article/"
        "phase11_expert_review_manifest.json"
    ).read_text(
        encoding="utf-8",
        errors="strict",
    )
)

if int(manifest.get("scenario_count", 0)) != expected:
    raise RuntimeError("Manifest scenario count mismatch")

if int(manifest.get("target_reviewers", 0)) < 3:
    raise RuntimeError("Manifest reviewer target is too low")

page_count = int(manifest.get("pdf_page_count", 0))

if page_count < 5 or page_count > 8:
    raise RuntimeError(
        f"PDF page count outside 5--8 range: {page_count}"
    )

if manifest.get("undefined_references") is not False:
    raise RuntimeError(
        "Manifest does not confirm resolved references"
    )

print("CVSS40_PHASE11_EXPERT_REVIEW_VALIDATION_OK")
print("scenario_count=" + str(expected))
print("target_reviewers=" + str(manifest["target_reviewers"]))
print(
    "planned_assessments="
    + str(manifest["planned_assessments"])
)
print("pdf_page_count=" + str(page_count))
