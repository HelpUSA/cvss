from pathlib import Path
import json
import subprocess
from datetime import datetime, timezone

ROOT = Path.cwd()
DOCS = ROOT / "docs"
GENERATED = ROOT / "article" / "generated"
TOOLS = ROOT / "tools"
VALIDATION = ROOT / "validation" / "article"

print("CVSS40_PHASE6_MANUSCRIPT_INTEGRATION_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: run from repository root")

required = [
    DOCS / "CVSS40_OFFICIAL_READING_NOTES.md",
    DOCS / "ARTICLE_CLAIM_GUARDRAILS_CVSS40.md",
    DOCS / "ARTICLE_EVALUATION_RESULTS_CVSS40.md",
    DOCS / "ARTICLE_DATASET_PROVENANCE_CVSS40.md",
    GENERATED / "cvss40_evaluation_design_section.md",
    GENERATED / "cvss40_results_section.md",
    GENERATED / "cvss40_discussion_section.md",
    GENERATED / "cvss40_limitations_section.md",
    GENERATED / "cvss40_dataset_summary_table.md",
    GENERATED / "cvss40_priority_shift_table.md",
    GENERATED / "cvss40_traceability_table.md",
    VALIDATION / "cvss40_scenario_metrics.json",
]

missing = [p.relative_to(ROOT).as_posix() for p in required if not p.exists()]
if missing:
    print("MISSING_FILES")
    for p in missing:
        print(p)
    raise SystemExit(1)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"WROTE {path.relative_to(ROOT).as_posix()} size={len(text)}", flush=True)

def upsert(rel: str, marker: str, body: str):
    path = ROOT / rel
    old = read(path) if path.exists() else ""
    begin = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"
    block = begin + "\n" + body.rstrip() + "\n" + end + "\n"
    if begin in old and end in old:
        new = old.split(begin, 1)[0] + block + old.split(begin, 1)[1].split(end, 1)[1].lstrip("\n")
        action = "UPDATED"
    else:
        new = old + ("" if not old or old.endswith("\n") else "\n") + "\n" + block
        action = "APPENDED"
    write(path, new)
    print(f"{action} {rel} {marker}", flush=True)

metrics = json.loads(read(VALIDATION / "cvss40_scenario_metrics.json"))

evaluation = read(GENERATED / "cvss40_evaluation_design_section.md").replace("# Evaluation Design section draft", "").strip()
results = read(GENERATED / "cvss40_results_section.md").replace("# Results section draft", "").strip()
discussion = read(GENERATED / "cvss40_discussion_section.md").replace("# Discussion section draft", "").strip()
limitations = read(GENERATED / "cvss40_limitations_section.md").replace("# Limitations section draft", "").strip()

dataset_summary = read(GENERATED / "cvss40_dataset_summary_table.md").strip()
priority_shift = read(GENERATED / "cvss40_priority_shift_table.md").strip()
traceability = read(GENERATED / "cvss40_traceability_table.md").strip()

generated_at = datetime.now(timezone.utc).isoformat()

manuscript = f"""---
status: draft
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
format_target: "IEEE-style 5-8 page double-blind manuscript"
tags: [cvss-v4, article, manuscript, ai-watcher, environmental-metrics]
---

# Operationalizing CVSS v4.0 Environmental Metrics with AI-Assisted Evidence Collection and Traceability

Generated UTC: `{generated_at}`

## Abstract

CVSS v4.0 defines Environmental metrics that allow vulnerability severity to be adapted to a consumer organization's deployment context. However, selecting Environmental metric values remains an evidence-intensive and judgment-dependent task for human analysts because local asset criticality, exposure, compensating controls, and operational requirements are often distributed across multiple sources. This paper presents an AI/watcher-assisted workflow for collecting, structuring, and tracing environmental evidence used to support CVSS v4.0 Environmental metric assessment. The workflow preserves official CVSS v4.0 semantics and treats watcher output as evidence-backed candidate recommendations requiring human review, not as autonomous official scoring. We evaluate the approach using a hybrid dataset of {metrics.get('scenario_count')} scenarios, including {metrics.get('nvd_cvss_v4_rows')} real NVD/CVSS v4.0 vulnerability records and {metrics.get('synthetic_rows')} curated synthetic scenarios. The evaluation reports evidence coverage, trace completeness, uncertainty flags, human review status, and priority shifts between Base-only and Environmental-aware views. Results show 100% evidence and trace coverage in the generated dataset and priority changes in {metrics.get('priority_shift_count')} of {metrics.get('scenario_count')} scenarios, supporting the feasibility of using reproducible artifacts to assist human review of Environmental metric choices.

## Keywords

CVSS v4.0; Environmental metrics; vulnerability prioritization; cybersecurity risk; artificial intelligence; traceability; reproducibility; human review.

## I. Introduction

The Common Vulnerability Scoring System is widely used to communicate vulnerability severity. In practice, however, vulnerability handling decisions often require more than a Base score. A vulnerability affecting an isolated lab asset, an identity provider, a public API gateway, or an operational technology monitoring component may require different remediation urgency even when the Base severity appears similar.

CVSS v4.0 provides a structured way to distinguish Base, Threat, Environmental, and Supplemental information. This is important because Base metrics capture intrinsic vulnerability characteristics, while Environmental metrics allow a consumer organization to account for local deployment context. The challenge addressed in this work is not the absence of Environmental metrics in CVSS v4.0. Instead, the challenge is operational: selecting Environmental metric values consistently and justifiably requires evidence, local context, uncertainty handling, and reviewable decision records.

This paper proposes an AI/watcher-assisted workflow for Environmental metric assessment. The workflow helps collect and structure evidence, suggest candidate Environmental metric values, flag uncertainty, require human review status, and export trace artifacts. The contribution is a method and prototype workflow, not a new scoring standard.

## II. Background: CVSS v4.0 and Environmental Metrics

CVSS v4.0 separates vulnerability scoring and context into metric groups including Base, Threat, Environmental, and Supplemental. The paper preserves this structure. Base CVSS information is stored separately as the official severity baseline. Threat context is treated as time-sensitive evidence requiring review. Environmental metric support is the main focus of this work because it directly depends on consumer-side deployment context. Supplemental observations are treated as additional context and not as a direct modification of the official final score.

The workflow also preserves CVSS-B, CVSS-BT, CVSS-BE, and CVSS-BTE labeling discipline. A score or priority table should identify which metric groups are represented and should not mix Base-only severity with Environmental-aware prioritization.

## III. Problem Statement

Although CVSS v4.0 defines Environmental metrics, applying them in a real consumer environment remains difficult. Analysts must determine asset importance, exposure, privilege context, compensating controls, confidentiality requirements, integrity requirements, availability requirements, and candidate Modified Base metric values. These inputs are often incomplete, distributed, or inconsistently documented.

This creates three practical problems. First, Environmental decisions may not be reproducible because the evidence trail is missing. Second, analysts may make inconsistent choices across similar assets. Third, operational prioritization may over-rely on Base severity even when local context should change remediation urgency.

## IV. Proposed AI/Watcher Workflow

The proposed workflow supports the analyst through eight steps:

1. Ingest vulnerability and Base CVSS v4.0 information.
2. Collect local environmental evidence.
3. Structure the evidence into scenario fields.
4. Suggest candidate Environmental metric values.
5. Attach evidence and rationale to each recommendation.
6. Flag uncertainty and missing evidence.
7. Require explicit human review status.
8. Export CSV, JSON, report, and table artifacts for reproducibility.

The workflow does not modify the official CVSS v4.0 formula. It also does not present AI output as an autonomous official score. The intended output is a human-reviewable, evidence-backed recommendation.

## V. Prototype Architecture

The prototype uses a scenario dataset, validation scripts, trace JSON artifacts, generated Markdown tables, and article-ready result packages. Each scenario contains the Base vector and score, curated Environmental context, candidate Environmental assessment fields, evidence links, uncertainty flags, human review status, and priority comparison fields.

The current implementation produces:

- `data/article/cvss40_environmental_scenarios.csv`
- `validation/article/cvss40_scenario_metrics.json`
- `validation/article/trace/*.json`
- `article/generated/cvss40_dataset_summary_table.md`
- `article/generated/cvss40_priority_shift_table.md`
- `article/generated/cvss40_traceability_table.md`

## VI. Evaluation Design

{evaluation}

### Dataset Summary

{dataset_summary}

## VII. Results

{results}

### Priority Shift Table

{priority_shift}

### Traceability Table

{traceability}

## VIII. Discussion

{discussion}

## IX. Limitations and Threats to Validity

{limitations}

## X. Conclusion

This paper presents an AI/watcher-assisted workflow for supporting CVSS v4.0 Environmental metric assessment through evidence collection, traceability, uncertainty flags, and explicit human review status. The method preserves official CVSS v4.0 semantics and does not modify the standard. The current hybrid dataset demonstrates that the workflow can produce reproducible artifacts and operational priority shifts across curated scenarios. Future work should add independent expert adjudication, measure inter-rater agreement, and evaluate the workflow in production-like settings.

## References to add

- FIRST CVSS v4.0 main page.
- FIRST CVSS v4.0 Specification Document.
- FIRST CVSS v4.0 User Guide.
- FIRST CVSS v4.0 Implementation Guide.
- FIRST CVSS v4.0 Examples.
- FIRST CVSS v4.0 FAQ.
- NVD API documentation.
- NVD vulnerability records used in the dataset.
"""

write(GENERATED / "cvss40_ieee_manuscript_draft.md", manuscript)

commit_checklist = f"""---
status: active
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, commit-checklist, validation, article]
---

# CVSS v4.0 article commit checklist

Generated UTC: `{generated_at}`

## Current validation status

- Scenario validation: expected `CVSS40_SCENARIO_DATASET_VALIDATION_OK`
- Docs validation: expected `CVSS40_DOCS_VALIDATION_OK`
- Phase 5 results validation: expected `CVSS40_PHASE5_ARTICLE_RESULTS_VALIDATION_OK`
- Phase 6 manuscript validation: expected `CVSS40_PHASE6_MANUSCRIPT_VALIDATION_OK`
- `git diff --check`: expected rc=0

## Current dataset status

- Scenario count: {metrics.get('scenario_count')}
- NVD/CVSS v4.0 rows: {metrics.get('nvd_cvss_v4_rows')}
- Synthetic rows: {metrics.get('synthetic_rows')}
- Evidence coverage: {metrics.get('evidence_coverage_pct')}%
- Trace completeness: {metrics.get('trace_completeness_pct')}%
- Priority shift count: {metrics.get('priority_shift_count')}
- Priority shift percentage: {metrics.get('priority_shift_pct')}%

## Files likely intended for commit

Docs:

- `docs/CVSS40_OFFICIAL_READING_NOTES.md`
- `docs/CVSS40_OFFICIAL_SOURCE_SCAN.md`
- `docs/CVSS40_PHASE1_READING_QUEUE.md`
- `docs/ARTICLE_CLAIM_GUARDRAILS_CVSS40.md`
- `docs/ARTICLE_CVSS40_AI_WATCHER_STRATEGY.md`
- `docs/ARTICLE_CVSS40_CONTRIBUTION_MAP.md`
- `docs/ARTICLE_DATASET_SCHEMA.md`
- `docs/ARTICLE_DATASET_PROVENANCE_CVSS40.md`
- `docs/ARTICLE_EVALUATION_RESULTS_CVSS40.md`
- `docs/ARTICLE_EXPERIMENT_DESIGN_CVSS40.md`
- `docs/ARTICLE_IEEE_SKELETON_CVSS40_AI_WATCHER.md`
- `docs/ARTICLE_PHASE3_IMPLEMENTATION_PLAN_CVSS40.md`
- `docs/ARTICLE_PIPELINE_INTEGRATION_AUDIT_CVSS40.md`
- `docs/ARTICLE_ROUTINE_CVSS40_AI_WATCHER.md`
- `docs/CONFERENCE_TARGET_PROFILE.md`

Data and validation:

- `data/article/cvss40_environmental_scenarios.csv`
- `data/article/cvss40_nvd_candidates.csv`
- `validation/article/cvss40_scenario_metrics.json`
- `validation/article/cvss40_scenario_validation_report.md`
- `validation/article/trace/*.json`

Generated article material:

- `article/generated/cvss40_ieee_manuscript_draft.md`
- `article/generated/cvss40_dataset_summary_table.md`
- `article/generated/cvss40_priority_shift_table.md`
- `article/generated/cvss40_traceability_table.md`
- `article/generated/cvss40_evaluation_design_section.md`
- `article/generated/cvss40_results_section.md`
- `article/generated/cvss40_discussion_section.md`
- `article/generated/cvss40_limitations_section.md`

Tools:

- `tools/article_cvss40_phase1_source_scan.py`
- `tools/article_cvss40_phase2_notes_and_map.py`
- `tools/article_cvss40_phase3_pipeline_audit.py`
- `tools/article_cvss40_phase4_seed_dataset.py`
- `tools/article_cvss40_phase4b_nvd_candidates.py`
- `tools/article_cvss40_phase4c_nvd_safe_paged_scan.py`
- `tools/article_cvss40_phase5_generate_results.py`
- `tools/article_cvss40_phase6_integrate_manuscript.py`
- `tools/validate_article_cvss40_docs.py`
- `tools/validate_article_cvss40_scenarios.py`
- `tools/validate_article_phase3_pipeline_audit.py`
- `tools/validate_article_phase5_results.py`
- `tools/validate_article_phase6_manuscript.py`

## Files to review before commit

Backup CSVs were created during dataset promotion attempts. Review whether to commit or exclude:

- `data/article/cvss40_environmental_scenarios.backup.*.csv`

Recommendation: do not commit transient backups unless needed for audit history. Keep one intentional backup only if desired, or move backups outside the repo before commit.

## Safe claim boundary

The paper may claim:

- AI/watcher-assisted Environmental metric assessment.
- Evidence-backed candidate recommendations.
- Human-reviewable workflow.
- Traceability and reproducibility support.
- Hybrid dataset with NVD/CVSS v4.0 rows plus curated Environmental contexts.

The paper must not claim:

- The workflow modifies CVSS v4.0.
- AI autonomously produces official CVSS scores.
- Production validation.
- Predictive superiority.
- Replacement of human analysts.
"""

write(DOCS / "ARTICLE_COMMIT_CHECKLIST_CVSS40.md", commit_checklist)

validator = r'''
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
'''

write(TOOLS / "validate_article_phase6_manuscript.py", validator)

upsert(
    "docs/00_Index.md",
    "CVSS40_PHASE6_MANUSCRIPT_INDEX_20260713",
    """## CVSS v4.0 Phase 6 Manuscript Integration

- [Integrated IEEE manuscript draft](../article/generated/cvss40_ieee_manuscript_draft.md)
- [Commit checklist](ARTICLE_COMMIT_CHECKLIST_CVSS40.md)
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE6_MANUSCRIPT_NEXT_20260713",
    """## CVSS v4.0 Phase 6 manuscript integration completed

Next actions:

1. Review `article/generated/cvss40_ieee_manuscript_draft.md`.
2. Review `docs/ARTICLE_COMMIT_CHECKLIST_CVSS40.md`.
3. Decide whether to keep or remove transient backup CSV files before commit.
4. Run full validation one more time.
5. Commit the article docs, dataset, generated tables, trace artifacts, and validation scripts.
"""
)

print("\nRUN PHASE6 VALIDATION", flush=True)
validation_cmds = [
    ["python", "-X", "utf8", "tools/validate_article_cvss40_scenarios.py"],
    ["python", "-X", "utf8", "tools/validate_article_cvss40_docs.py"],
    ["python", "-X", "utf8", "tools/validate_article_phase5_results.py"],
    ["python", "-X", "utf8", "tools/validate_article_phase6_manuscript.py"],
]

for cmd in validation_cmds:
    print("-- " + " ".join(cmd), flush=True)
    cp = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
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

print("CVSS40_PHASE6_MANUSCRIPT_INTEGRATION_END", flush=True)
