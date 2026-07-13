from pathlib import Path
import csv
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone

ROOT = Path.cwd()
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"
DATASET = ROOT / "data" / "article" / "cvss40_environmental_scenarios.csv"

print("CVSS40_PHASE3_PIPELINE_AUDIT_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: run this from repository root")

required_docs = [
    DOCS / "CVSS40_OFFICIAL_READING_NOTES.md",
    DOCS / "ARTICLE_CLAIM_GUARDRAILS_CVSS40.md",
    DOCS / "ARTICLE_CVSS40_CONTRIBUTION_MAP.md",
    DOCS / "ARTICLE_DATASET_SCHEMA.md",
]
missing = [str(p.relative_to(ROOT)) for p in required_docs if not p.exists()]
if missing:
    raise SystemExit("ERROR missing required phase 2 docs: " + ", ".join(missing))

IGNORE_DIRS = {
    ".git",
    ".next",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
    ".venv",
    "venv",
}

INCLUDE_ROOTS = [
    "scripts",
    "validation",
    "web/src/app",
    "article",
    "docs",
    "data",
    "outputs/evidence/latest",
]

EXTS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".json",
    ".csv",
    ".md",
    ".tex",
    ".txt",
    ".yml",
    ".yaml",
}

TERMS = [
    "cvss",
    "CVSS",
    "official_cvss",
    "contextual_environmental",
    "environmental",
    "Environmental",
    "threat",
    "Threat",
    "supplemental",
    "Supplemental",
    "evidence",
    "Evidence",
    "trace",
    "Trace",
    "priority",
    "Priority",
    "scenario",
    "Scenario",
    "manifest",
    "before_after",
    "adjustment_trace",
    "validate_real_pipeline",
    "human_review",
    "uncertainty",
    "review_required",
    "cvss_b_score",
    "candidate_modified_metrics",
]

REQUIRED_FIELDS = [
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

def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & IGNORE_DIRS)

def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

def classify(path: Path) -> str:
    s = path.as_posix().lower()
    if s.startswith("scripts/"):
        return "pipeline/script"
    if s.startswith("validation/"):
        return "validation"
    if s.startswith("web/src/app/"):
        return "dashboard"
    if s.startswith("article/"):
        return "article"
    if s.startswith("docs/"):
        return "docs"
    if s.startswith("data/"):
        return "dataset"
    if s.startswith("outputs/"):
        return "evidence-output"
    return "other"

files = []
for rel_root in INCLUDE_ROOTS:
    base = ROOT / rel_root
    if not base.exists():
        continue
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.suffix.lower() not in EXTS:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = safe_read(path)
        lower = text.lower()
        counts = Counter()
        for term in TERMS:
            c = lower.count(term.lower())
            if c:
                counts[term] = c
        score = sum(counts.values())
        if score:
            files.append({
                "path": rel,
                "category": classify(Path(rel)),
                "suffix": path.suffix.lower(),
                "size": path.stat().st_size,
                "score": score,
                "counts": dict(counts),
            })

files.sort(key=lambda x: (-x["score"], x["path"]))

category_counts = Counter(f["category"] for f in files)

dataset_status = {
    "exists": DATASET.exists(),
    "rows": 0,
    "columns": [],
    "missing_columns": REQUIRED_FIELDS[:],
}
if DATASET.exists():
    with DATASET.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if rows:
        dataset_status["columns"] = rows[0]
        dataset_status["rows"] = max(0, len(rows) - 1)
        dataset_status["missing_columns"] = [c for c in REQUIRED_FIELDS if c not in rows[0]]

field_mentions = defaultdict(list)
for item in files:
    if item["category"] not in {"pipeline/script", "validation", "dashboard", "dataset"}:
        continue
    text = safe_read(ROOT / item["path"])
    lower = text.lower()
    for field in REQUIRED_FIELDS:
        if field.lower() in lower:
            field_mentions[field].append(item["path"])

def md_table_row(cols):
    return "| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in cols) + " |"

generated = datetime.now(timezone.utc).isoformat()

audit = []
audit.append("---")
audit.append("status: active")
audit.append("last_updated: 2026-07-10")
audit.append('owner: "Wagner / CVSS project"')
audit.append("tags: [cvss-v4, pipeline-audit, environmental-metrics, ai-watcher, article]")
audit.append("---")
audit.append("")
audit.append("# Article pipeline integration audit")
audit.append("")
audit.append(f"Generated UTC: `{generated}`")
audit.append("")
audit.append("## Purpose")
audit.append("")
audit.append("This audit identifies where the repository already contains CVSS, evidence, trace, dashboard, validation, and prioritization logic, so the CVSS v4.0 Environmental Metrics article work can be integrated without guessing.")
audit.append("")
audit.append("## Dataset status")
audit.append("")
audit.append(md_table_row(["Item", "Value"]))
audit.append(md_table_row(["---", "---"]))
audit.append(md_table_row(["Dataset path", DATASET.relative_to(ROOT).as_posix()]))
audit.append(md_table_row(["Exists", dataset_status["exists"]]))
audit.append(md_table_row(["Rows", dataset_status["rows"]]))
audit.append(md_table_row(["Columns", len(dataset_status["columns"])]))
audit.append(md_table_row(["Missing required columns", ", ".join(dataset_status["missing_columns"]) if dataset_status["missing_columns"] else "none"]))
audit.append("")
audit.append("## Relevant file categories")
audit.append("")
audit.append(md_table_row(["Category", "Relevant files"]))
audit.append(md_table_row(["---", "---:"]))
for cat, count in sorted(category_counts.items()):
    audit.append(md_table_row([cat, count]))
audit.append("")
audit.append("## Top relevant files")
audit.append("")
audit.append(md_table_row(["Rank", "File", "Category", "Score", "Size"]))
audit.append(md_table_row(["---:", "---", "---", "---:", "---:"]))
for idx, item in enumerate(files[:80], 1):
    audit.append(md_table_row([idx, item["path"], item["category"], item["score"], item["size"]]))
audit.append("")
audit.append("## Required field implementation visibility")
audit.append("")
audit.append(md_table_row(["Field", "Mentioned in implementation files?"]))
audit.append(md_table_row(["---", "---"]))
for field in REQUIRED_FIELDS:
    mentions = field_mentions.get(field, [])
    if mentions:
        shown = ", ".join(mentions[:6])
        if len(mentions) > 6:
            shown += f", ... +{len(mentions)-6}"
    else:
        shown = "not found"
    audit.append(md_table_row([field, shown]))
audit.append("")
audit.append("## Integration gaps")
audit.append("")
audit.append("- The dataset currently exists as a schema/header seed unless rows have been added.")
audit.append("- New CVSS v4.0 Environmental assessment fields must remain separated from official CVSS Base fields.")
audit.append("- The pipeline should not treat watcher recommendations as final scores without explicit `human_review_status`.")
audit.append("- Result tables for the article still need to be generated from the scenario dataset.")
audit.append("- Trace artifacts should connect each recommendation to evidence, uncertainty, and review status.")
audit.append("")
audit.append("## Recommended implementation order")
audit.append("")
audit.append("1. Keep this audit as the current integration map.")
audit.append("2. Populate 30 to 50 curated scenarios in `data/article/cvss40_environmental_scenarios.csv`.")
audit.append("3. Add a scenario validator that checks required fields, controlled values, evidence coverage, review status, and trace references.")
audit.append("4. Add result generation for article tables.")
audit.append("5. Only after dataset validation, connect outputs to dashboard or existing pipeline modules.")
audit.append("")
audit.append("## Important boundary")
audit.append("")
audit.append("This audit does not prove CVSS v4.0 formula implementation. It only maps repository integration points for the article workflow.")

audit_doc = DOCS / "ARTICLE_PIPELINE_INTEGRATION_AUDIT_CVSS40.md"
audit_doc.write_text("\n".join(audit).rstrip() + "\n", encoding="utf-8", newline="\n")
print(f"WROTE {audit_doc.relative_to(ROOT).as_posix()} size={audit_doc.stat().st_size}", flush=True)

plan = """---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags: [cvss-v4, implementation-plan, environmental-metrics, article]
---

# Phase 3 implementation plan: CVSS v4.0 AI/watcher article

## Objective

Move from documentation to executable article evidence without changing official CVSS semantics.

## Step 1 — Scenario dataset

Create 30 to 50 scenarios in:

- `data/article/cvss40_environmental_scenarios.csv`

Every row must include:

- Official or assigned CVSS v4.0 Base vector.
- CVSS-B score and severity.
- Local deployment context.
- Environmental evidence.
- Candidate Environmental metric values.
- Watcher recommendation.
- Uncertainty flags.
- Human review status.
- Base-only and Environmental-aware priority.
- Trace reference.

## Step 2 — Scenario validation

Create a validator that checks:

- Required columns exist.
- Required fields are not empty.
- Controlled values are valid.
- `human_review_status` is explicit.
- Evidence is present.
- Trace reference is present.
- Priority values are valid.
- No row claims autonomous official scoring.

## Step 3 — Article result generation

Generate:

- Dataset summary.
- Evidence coverage.
- Review status summary.
- Uncertainty summary.
- Priority shift summary.
- Trace completeness summary.

Target outputs:

- `validation/article/cvss40_scenario_validation_report.md`
- `validation/article/cvss40_scenario_metrics.json`
- `article/generated/cvss40_dataset_summary_table.md`
- `article/generated/cvss40_priority_shift_table.md`
- `article/generated/cvss40_traceability_table.md`

## Step 4 — Manuscript integration

Use generated outputs to write:

- Evaluation Design.
- Results.
- Discussion.
- Limitations.

## Step 5 — Dashboard/pipeline integration

Only after the dataset and article metrics are stable, connect the new fields to dashboard or existing pipeline outputs.
"""

plan_doc = DOCS / "ARTICLE_PHASE3_IMPLEMENTATION_PLAN_CVSS40.md"
plan_doc.write_text(plan.rstrip() + "\n", encoding="utf-8", newline="\n")
print(f"WROTE {plan_doc.relative_to(ROOT).as_posix()} size={plan_doc.stat().st_size}", flush=True)

validator = r'''
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
'''

validator_path = TOOLS / "validate_article_phase3_pipeline_audit.py"
validator_path.write_text(validator.lstrip(), encoding="utf-8", newline="\n")
print(f"WROTE {validator_path.relative_to(ROOT).as_posix()} size={validator_path.stat().st_size}", flush=True)

def upsert(rel: str, marker: str, body: str):
    path = ROOT / rel
    old = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    begin = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"
    block = begin + "\n" + body.rstrip() + "\n" + end + "\n"
    if begin in old and end in old:
        new = old.split(begin, 1)[0] + block + old.split(begin, 1)[1].split(end, 1)[1].lstrip("\n")
        action = "UPDATED"
    else:
        new = old + ("" if not old or old.endswith("\n") else "\n") + "\n" + block
        action = "APPENDED"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"{action} {rel} {marker}", flush=True)

upsert(
    "docs/00_Index.md",
    "CVSS40_PHASE3_PIPELINE_AUDIT_INDEX_20260710",
    """## CVSS v4.0 Phase 3 pipeline integration

- [Pipeline integration audit](ARTICLE_PIPELINE_INTEGRATION_AUDIT_CVSS40.md)
- [Phase 3 implementation plan](ARTICLE_PHASE3_IMPLEMENTATION_PLAN_CVSS40.md)
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE3_PIPELINE_AUDIT_NEXT_20260710",
    """## CVSS v4.0 Phase 3 pipeline audit completed

Next actions:

1. Review `docs/ARTICLE_PIPELINE_INTEGRATION_AUDIT_CVSS40.md`.
2. Start the scenario dataset with 30 to 50 rows.
3. Add a dataset validator for article-grade evidence fields.
4. Generate article result tables from the dataset.
5. Integrate stable outputs into the dashboard only after validation passes.
"""
)

print("\nRUN PHASE3 VALIDATION", flush=True)
cp = subprocess.run(["python", "-X", "utf8", str(validator_path)], cwd=ROOT, text=True, capture_output=True)
print("rc=" + str(cp.returncode), flush=True)
if cp.stdout:
    print(cp.stdout, flush=True)
if cp.stderr:
    print(cp.stderr, flush=True)
if cp.returncode != 0:
    raise SystemExit(cp.returncode)

print("\nVALIDATION SNAPSHOT", flush=True)
for label, cmd in [
    ("git status -sb", ["git", "status", "-sb"]),
    ("git diff --stat", ["git", "diff", "--stat"]),
    ("git diff --check", ["git", "diff", "--check"]),
]:
    print("\n-- " + label + " --", flush=True)
    cp = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    print("rc=" + str(cp.returncode), flush=True)
    if cp.stdout:
        print(cp.stdout[-12000:], flush=True)
    if cp.stderr:
        print(cp.stderr[-8000:], flush=True)

print("CVSS40_PHASE3_PIPELINE_AUDIT_END", flush=True)
