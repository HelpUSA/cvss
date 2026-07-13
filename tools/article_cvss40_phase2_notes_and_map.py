from pathlib import Path
import csv
import json
import subprocess
from datetime import datetime, timezone

ROOT = Path.cwd()
DOCS = ROOT / "docs"
DATA = ROOT / "data" / "article"
TOOLS = ROOT / "tools"
SCAN_JSON = ROOT / "outputs" / "cvss40_official_scan" / "source_scan.json"

print("CVSS40_PHASE2_NOTES_AND_MAP_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: run this from the repository root, expected .git directory")

if not SCAN_JSON.exists():
    raise SystemExit("ERROR: missing outputs/cvss40_official_scan/source_scan.json. Run Script 1 first.")

DOCS.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)
TOOLS.mkdir(parents=True, exist_ok=True)

scan = json.loads(SCAN_JSON.read_text(encoding="utf-8", errors="replace"))

def esc(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"WROTE {path.relative_to(ROOT).as_posix()} size={len(text)}", flush=True)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

def upsert(rel: str, marker: str, body: str):
    path = ROOT / rel
    old = read(path)
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

sources = scan.get("sources", [])
source_rows = []
for item in sources:
    label = item.get("label", "")
    status = item.get("status")
    error = item.get("error")
    title = item.get("title", "")
    heading_count = item.get("heading_count", 0)
    text_length = item.get("text_length", 0)
    term_counts = item.get("term_counts", {})
    source_rows.append(
        f"| `{esc(label)}` | {esc(status if status is not None else 'ERR')} | {esc(title)} | {text_length} | {heading_count} | {term_counts.get('Environmental', 0)} | {term_counts.get('Threat', 0)} | {term_counts.get('Supplemental', 0)} | {esc(error or '')} |"
    )

generated_at = datetime.now(timezone.utc).isoformat()

official_notes = f"""---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - cvss
  - cvss-v4
  - official-reading
  - environmental-metrics
  - ai-watcher
  - article
---

# CVSS v4.0 official reading notes for the AI/watcher article

Generated UTC: `{generated_at}`

This file is an article working note. It summarizes what must be verified and cited from the official FIRST CVSS v4.0 documentation. It intentionally avoids copying large portions of official documentation.

## Source inventory status

| Source | HTTP status | Title | Text length | Headings | Environmental hits | Threat hits | Supplemental hits | Error |
|---|---:|---|---:|---:|---:|---:|---:|---|
{chr(10).join(source_rows)}

## Official sources to cite in the manuscript

- FIRST CVSS v4.0 main page: `https://www.first.org/cvss/v4.0/`
- FIRST CVSS v4.0 Specification Document: `https://www.first.org/cvss/v4.0/specification-document`
- FIRST CVSS v4.0 User Guide: `https://www.first.org/cvss/v4.0/user-guide`
- FIRST CVSS v4.0 Implementation Guide: `https://www.first.org/cvss/v4.0/implementation-guide`
- FIRST CVSS v4.0 Examples: `https://www.first.org/cvss/v4.0/examples`
- FIRST CVSS v4.0 FAQ: `https://www.first.org/cvss/v4.0/faq`
- FIRST CVSS v4.0 Calculator: `https://www.first.org/cvss/calculator/4.0`
- FIRST CVSS data representations: `https://www.first.org/cvss/data-representations`

## Article-safe interpretation

CVSS v4.0 already provides a richer structure than a Base-only score. The article should therefore avoid presenting the project as a new scoring standard or as an extension that modifies CVSS. The project should be framed as an operational workflow that helps a consumer organization apply Environmental metric assessment in a more evidence-backed, reviewable, and reproducible way.

## Core official concepts to preserve

### Base metrics

Base metrics represent intrinsic vulnerability characteristics. In the article, Base metrics should be treated as the official severity foundation. The prototype must preserve this information and must not overwrite or relabel it as operational risk.

Article use:

- Store official Base vector and Base score separately.
- Display Base-only priority as a baseline.
- Never claim the system improves the Base score.

### Threat metrics

Threat metrics represent information that may change over time, such as exploit or threat-related context. The watcher may help collect or timestamp threat evidence, but must not be described as authoritative threat intelligence unless a validated threat-intelligence source and process are implemented.

Article use:

- Treat threat evidence as contextual input.
- Record source, timestamp, and uncertainty.
- Flag missing or conflicting evidence.

### Environmental metrics

Environmental metrics represent characteristics relevant to a specific consumer environment. This is the strongest fit for the article because the watcher can help collect local evidence, suggest candidate metric values, and attach justification.

Article use:

- Focus the paper on Environmental metric assessment.
- Treat AI/watcher outputs as candidate recommendations.
- Require `human_review_status` before treating any candidate value as final.
- Preserve traceability between evidence and recommendation.

### Supplemental metrics

Supplemental metrics provide additional context and should not be presented as directly modifying the official final score. The watcher can capture supplemental observations, but these should be reported as supporting context.

Article use:

- Capture supplemental signals as optional context.
- Use them in discussion or operational prioritization, not as a formula change.
- Avoid saying supplemental values change CVSS-BTE directly.

### CVSS-B, CVSS-BT, CVSS-BE, CVSS-BTE

The paper must label scores based on which metric groups are used. This avoids mixing Base-only severity with Threat/Environmental-aware scoring.

Article use:

- Use explicit labels in tables and dashboard output.
- Do not report a score without its vector and metric-group label.
- Compare Base-only versus Environmental-aware assessment clearly.

## Main problem statement

Although CVSS v4.0 defines Environmental metrics for adapting vulnerability severity to a consumer's environment, selecting those metrics remains an evidence-intensive and judgment-dependent task for human analysts. Local asset criticality, deployment context, exposure, compensating controls, and business requirements are often distributed across documentation, configuration, and operational knowledge. This creates difficulty in consistency, auditability, and reproducibility.

## Proposed contribution

The project proposes an AI/watcher-assisted workflow that supports consumer-side Environmental metric assessment by:

1. Collecting local environmental evidence.
2. Structuring evidence into scenario fields.
3. Suggesting candidate Environmental metric values.
4. Linking each suggestion to explicit evidence.
5. Recording uncertainty and missing evidence.
6. Requiring human review status.
7. Exporting traceable CSV, JSON, manifest, and report artifacts.
8. Comparing Base-only and Environmental-aware prioritization.

## Claims allowed

- The prototype preserves official CVSS v4.0 semantics.
- The watcher assists Environmental metric assessment.
- Outputs are evidence-backed candidate recommendations.
- Human review status is explicit.
- The method improves traceability and reproducibility of the assessment workflow.
- The evaluation reports evidence coverage, trace completeness, uncertainty flags, and priority shifts across curated scenarios.

## Claims prohibited

- The system improves CVSS.
- The system changes or extends the official CVSS formula.
- The watcher autonomously produces official CVSS scores.
- AI replaces human analysts.
- The prototype is validated in production.
- The method proves predictive superiority.
- The article introduces new official Environmental metrics.
- Supplemental metrics directly modify the official CVSS-BTE score.

## Manuscript sentence to use

Although CVSS v4.0 defines Environmental metrics for adapting vulnerability severity to a consumer's environment, selecting those metrics remains an evidence-intensive and judgment-dependent task for human analysts. This work proposes an AI/watcher-assisted workflow that collects, structures, and traces environmental evidence to support reproducible CVSS v4.0 Environmental metric assessment without modifying the official CVSS standard.

## Immediate use in the article

Use this document to write:

- Background section.
- Problem statement.
- Contribution list.
- Evaluation boundaries.
- Limitations and threats to validity.
"""

claim_guardrails = """---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - article
  - claim-guardrails
  - cvss-v4
  - environmental-metrics
  - ai-watcher
---

# Claim guardrails for the CVSS v4.0 AI/watcher article

## Safe positioning

The project should be positioned as:

> An AI/watcher-assisted workflow for evidence-backed, human-reviewable CVSS v4.0 Environmental metric assessment.

## Do

Use these phrases:

- "AI-assisted"
- "watcher-assisted"
- "evidence-backed recommendation"
- "candidate Environmental metric value"
- "human-reviewable"
- "human review status"
- "uncertainty flag"
- "trace artifact"
- "CVSS v4.0 semantics are preserved"
- "official CVSS formula is not modified"
- "consumer-side Environmental assessment"
- "artifact and reproducibility validation"

## Do not

Avoid these phrases unless explicitly negated as a limitation:

- "improves CVSS"
- "fixes CVSS"
- "replaces CVSS"
- "new CVSS score"
- "new official Environmental metrics"
- "autonomous official scoring"
- "AI replaces analysts"
- "validated in production"
- "proves better prediction"
- "proves real-world effectiveness"
- "modifies the CVSS formula"

## Required limitation language

The paper must state:

1. The prototype does not modify the official CVSS v4.0 standard.
2. Watcher output is a recommendation, not an autonomous final score.
3. Human review remains required for final Environmental metric decisions.
4. Current evaluation is based on curated scenarios.
5. Current validation demonstrates reproducibility and traceability, not production effectiveness.
6. Independent expert adjudication is future work unless actually completed.

## Review checklist before submission

- Does every score table identify the metric group label?
- Does every Environmental recommendation have evidence?
- Does every recommendation have a review status?
- Are uncertainty flags reported?
- Are official CVSS fields separated from watcher fields?
- Does the article avoid claiming predictive superiority?
- Does the article cite FIRST CVSS v4.0 official documentation?
"""

contribution_map = """---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - cvss-v4
  - contribution-map
  - environmental-metrics
  - ai-watcher
---

# CVSS v4.0 contribution map for the AI/watcher article

| Official CVSS v4.0 concept | Human difficulty | AI/watcher support | Artifact produced | Allowed claim | Claim to avoid |
|---|---|---|---|---|---|
| CVSS-B Base score | Analysts may treat severity as full organizational risk | Preserve official Base vector and score as separate baseline | `official_cvss_v4_vector`, `cvss_b_score` | The prototype preserves CVSS-B as the baseline | The prototype improves Base CVSS |
| Threat metric group | Threat context may change and evidence may be scattered | Collect threat notes, timestamps, and uncertainty flags | `threat_context`, evidence notes | The watcher supports evidence collection for time-sensitive context | The watcher has authoritative threat intelligence |
| Environmental Security Requirements | CR, IR, and AR require local business and asset judgment | Link asset criticality evidence to candidate CR/IR/AR rationale | `confidentiality_requirement`, `integrity_requirement`, `availability_requirement` | The workflow supports reviewable Environmental metric selection | AI decides the final Environmental score |
| Modified Base Metrics | Deployment, controls, privileges, and exposure are local | Map deployment evidence to candidate Modified metrics | `candidate_modified_metrics`, `trace_json` | The workflow makes Modified metric choices auditable | The workflow changes official CVSS semantics |
| Supplemental metrics | Optional context may be used inconsistently | Capture supplemental observations as contextual signals | `supplemental_context` | Supplemental signals can inform operational discussion | Supplemental metrics directly modify CVSS-BTE |
| CVSS-B / CVSS-BT / CVSS-BE / CVSS-BTE labels | Scores may be miscommunicated | Force explicit metric-group labels in outputs | labeled CSV/dashboard outputs | The output identifies the metric groups used | A score without vector or label is sufficient |
| Consumer responsibility | Local organizations must apply their own context | Assist consumer-side analyst and require review status | `human_review_status` | The watcher assists consumer-side Environmental assessment | Providers should apply one Environmental score for all consumers |
| Evidence and auditability | Decisions may be undocumented or inconsistent | Attach evidence, uncertainty, and trace artifacts to each recommendation | manifest, CSV, trace report | The workflow improves traceability and reproducibility | The workflow proves real-world effectiveness |
| Human review | Analysts need decision support, not replacement | Mark review as required/reviewed/not required | `human_review_status`, `review_required` | AI supports human review | AI replaces analysts |
| Evaluation | Broad real-world validation is not yet available | Evaluate curated scenarios with reproducible artifacts | result tables, trace completeness metrics | The evaluation demonstrates feasibility and traceability | The evaluation proves predictive superiority |
"""

dataset_schema = """---
status: active
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - dataset
  - schema
  - cvss-v4
  - environmental-metrics
  - article
---

# Article dataset schema: CVSS v4.0 Environmental Metrics with AI/watcher assistance

Planned dataset:

- `data/article/cvss40_environmental_scenarios.csv`

## Required fields

| Field | Type | Required | Purpose |
|---|---|---:|---|
| `scenario_id` | string | yes | Stable scenario identifier |
| `cve_id` | string | no | CVE if available |
| `vulnerability_summary` | string | yes | Short vulnerability description |
| `official_cvss_v4_vector` | string | yes | Official or assigned CVSS v4.0 vector |
| `cvss_b_score` | number | yes | Base score |
| `cvss_b_severity` | string | yes | Base severity label |
| `asset_class` | string | yes | Type of affected asset |
| `deployment_context` | string | yes | How the system is deployed |
| `internet_exposure` | string | yes | Exposure level |
| `privilege_context` | string | yes | Account or privilege context |
| `compensating_controls` | string | yes | Controls such as WAF, segmentation, hardening, monitoring |
| `confidentiality_requirement` | string | yes | Candidate CR value and rationale |
| `integrity_requirement` | string | yes | Candidate IR value and rationale |
| `availability_requirement` | string | yes | Candidate AR value and rationale |
| `candidate_modified_metrics` | string | yes | Candidate Modified Base metrics |
| `threat_context` | string | no | Threat or exploit information |
| `supplemental_context` | string | no | Supplemental observations |
| `evidence_links` | string | yes | Evidence references or local evidence IDs |
| `evidence_summary` | string | yes | Human-readable evidence summary |
| `watcher_recommendation` | string | yes | AI/watcher recommendation text |
| `uncertainty_flags` | string | yes | Missing/conflicting evidence markers |
| `review_required` | boolean | yes | Whether human review is required |
| `human_review_status` | enum | yes | `required`, `reviewed`, or `not_required` |
| `base_priority` | string | yes | Priority from Base-only view |
| `environmental_priority` | string | yes | Priority after Environmental-aware assessment |
| `priority_delta` | number | yes | Difference between priorities |
| `trace_json` | string | yes | Path or ID of trace artifact |

## Controlled values

### `internet_exposure`

- `public`
- `restricted`
- `internal`
- `isolated`
- `unknown`

### `human_review_status`

- `required`
- `reviewed`
- `not_required`

### `base_priority` and `environmental_priority`

- `critical`
- `high`
- `medium`
- `low`
- `defer`

## Rule

No candidate Environmental metric should be treated as final unless `human_review_status` is explicit. The article may report watcher-assisted candidate values, evidence coverage, and trace completeness, but must not report autonomous official scoring.
"""

experiment_design = """---
status: draft
last_updated: 2026-07-10
owner: "Wagner / CVSS project"
tags:
  - experiment-design
  - cvss-v4
  - environmental-metrics
  - ai-watcher
  - article
---

# Experiment design for the CVSS v4.0 AI/watcher article

## Goal

Evaluate whether an AI/watcher-assisted workflow can make CVSS v4.0 Environmental metric assessment more traceable, reviewable, and reproducible across curated vulnerability scenarios.

## Dataset

Use 30 to 50 curated scenarios.

Each scenario must include:

- Base CVSS v4.0 information.
- Asset and deployment context.
- Environmental evidence.
- Candidate Environmental metric recommendations.
- Uncertainty flags.
- Human review status.
- Base-only priority.
- Environmental-aware priority.
- Trace artifact reference.

## Evaluation metrics

| Metric | Description |
|---|---|
| Scenario count | Number of scenarios in dataset |
| Evidence coverage | Percentage of scenarios with non-empty evidence |
| Recommendation coverage | Percentage of scenarios with watcher recommendation |
| Trace completeness | Percentage of scenarios with trace artifact reference |
| Review explicitness | Percentage of scenarios with explicit human review status |
| Uncertainty rate | Percentage of scenarios with uncertainty flags |
| Priority shift count | Number of scenarios where Environmental-aware priority differs from Base-only priority |
| Priority shift percentage | Priority shift count divided by scenario count |
| Average priority delta | Mean delta between Base-only and Environmental-aware priority |
| Maximum upward shift | Largest increase in urgency |
| Maximum downward shift | Largest decrease in urgency |

## Interpretation boundaries

These metrics evaluate workflow quality, not predictive superiority. The evaluation can support claims about traceability, reproducibility, and operational differentiation. It cannot support claims about production effectiveness or superiority over CVSS.

## Required output tables for paper

- Dataset overview table.
- Evidence coverage table.
- Priority shift table.
- Trace completeness table.
- Limitation summary table.
"""

validation_script = r'''
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
'''

write(DOCS / "CVSS40_OFFICIAL_READING_NOTES.md", official_notes)
write(DOCS / "ARTICLE_CLAIM_GUARDRAILS_CVSS40.md", claim_guardrails)
write(DOCS / "ARTICLE_CVSS40_CONTRIBUTION_MAP.md", contribution_map)
write(DOCS / "ARTICLE_DATASET_SCHEMA.md", dataset_schema)
write(DOCS / "ARTICLE_EXPERIMENT_DESIGN_CVSS40.md", experiment_design)
write(TOOLS / "validate_article_cvss40_docs.py", validation_script)

csv_path = DATA / "cvss40_environmental_scenarios.csv"
header = [
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

if csv_path.exists():
    existing = csv_path.read_text(encoding="utf-8", errors="replace").splitlines()
    if existing:
        print(f"KEPT existing {csv_path.relative_to(ROOT).as_posix()} lines={len(existing)}", flush=True)
    else:
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(header)
        print(f"WROTE empty-header {csv_path.relative_to(ROOT).as_posix()}", flush=True)
else:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow(header)
    print(f"WROTE {csv_path.relative_to(ROOT).as_posix()} header_columns={len(header)}", flush=True)

upsert(
    "docs/00_Index.md",
    "CVSS40_PHASE2_NOTES_MAP_INDEX_20260710",
    """## CVSS v4.0 Phase 2 notes and mapping

- [CVSS v4.0 official reading notes](CVSS40_OFFICIAL_READING_NOTES.md)
- [CVSS v4.0 claim guardrails](ARTICLE_CLAIM_GUARDRAILS_CVSS40.md)
- [CVSS v4.0 contribution map](ARTICLE_CVSS40_CONTRIBUTION_MAP.md)
- [Article dataset schema](ARTICLE_DATASET_SCHEMA.md)
- [Experiment design](ARTICLE_EXPERIMENT_DESIGN_CVSS40.md)
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE2_NOTES_MAP_NEXT_20260710",
    """## CVSS v4.0 Phase 2 completed

Next actions:

1. Review official reading notes and confirm all statements against FIRST documentation.
2. Start populating `data/article/cvss40_environmental_scenarios.csv` with 30 to 50 scenarios.
3. Add validation for evidence coverage, review status, uncertainty flags, and trace completeness.
4. Generate result tables from the dataset.
5. Rewrite article sections using the safe claim guardrails.
"""
)

print("\nRUN CUSTOM VALIDATION", flush=True)
cp = subprocess.run(["python", "-X", "utf8", "tools/validate_article_cvss40_docs.py"], cwd=ROOT, text=True, capture_output=True)
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

print("CVSS40_PHASE2_NOTES_AND_MAP_END", flush=True)
