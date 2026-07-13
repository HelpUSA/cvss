from pathlib import Path
import csv
import json
import subprocess
from datetime import datetime, timezone
from collections import Counter

ROOT = Path.cwd()
DOCS = ROOT / "docs"
GENERATED = ROOT / "article" / "generated"
TOOLS = ROOT / "tools"
VALIDATION = ROOT / "validation" / "article"
DATASET = ROOT / "data" / "article" / "cvss40_environmental_scenarios.csv"
METRICS = VALIDATION / "cvss40_scenario_metrics.json"

print("CVSS40_PHASE8_POLISH_REFERENCES_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: run from repository root")

required = [
    DATASET,
    METRICS,
    GENERATED / "cvss40_ieee_manuscript_draft.md",
    GENERATED / "cvss40_dataset_summary_table.md",
    GENERATED / "cvss40_priority_shift_table.md",
    GENERATED / "cvss40_traceability_table.md",
    GENERATED / "cvss40_evaluation_design_section.md",
    GENERATED / "cvss40_results_section.md",
    GENERATED / "cvss40_discussion_section.md",
    GENERATED / "cvss40_limitations_section.md",
]

missing = [p.relative_to(ROOT).as_posix() for p in required if not p.exists()]
if missing:
    print("MISSING_FILES")
    for p in missing:
        print(p)
    raise SystemExit(1)

DOCS.mkdir(parents=True, exist_ok=True)
GENERATED.mkdir(parents=True, exist_ok=True)
TOOLS.mkdir(parents=True, exist_ok=True)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"WROTE {path.relative_to(ROOT).as_posix()} size={len(text)}", flush=True)

def strip_extra_blank_eof(path: Path):
    if not path.exists():
        return False
    old = read(path)
    new = old.rstrip() + "\n"
    if new != old:
        path.write_text(new, encoding="utf-8", newline="\n")
        print(f"FIXED_EOF {path.relative_to(ROOT).as_posix()}", flush=True)
        return True
    print(f"EOF_OK {path.relative_to(ROOT).as_posix()}", flush=True)
    return False

for rel in [
    "tools/article_cvss40_phase4c_nvd_safe_paged_scan.py",
    "tools/article_cvss40_phase7_precommit_clean_validate.py",
]:
    strip_extra_blank_eof(ROOT / rel)

metrics = json.loads(read(METRICS))

with DATASET.open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

nvd_rows = [r for r in rows if r.get("scenario_source") == "nvd_cvss_v4_with_curated_environment"]
synthetic_rows = [r for r in rows if r.get("scenario_source") == "curated_synthetic_no_cve"]

source_counts = Counter(r.get("scenario_source", "") for r in rows)
severity_counts = Counter(r.get("cvss_b_severity", "") for r in rows)

dataset_summary = read(GENERATED / "cvss40_dataset_summary_table.md").strip()
priority_shift = read(GENERATED / "cvss40_priority_shift_table.md").strip()
traceability = read(GENERATED / "cvss40_traceability_table.md").strip()

evaluation = read(GENERATED / "cvss40_evaluation_design_section.md").replace("# Evaluation Design section draft", "").strip()
results = read(GENERATED / "cvss40_results_section.md").replace("# Results section draft", "").strip()
discussion = read(GENERATED / "cvss40_discussion_section.md").replace("# Discussion section draft", "").strip()
limitations = read(GENERATED / "cvss40_limitations_section.md").replace("# Limitations section draft", "").strip()

generated_at = datetime.now(timezone.utc).isoformat()

official_refs = [
    ("FIRST", "Common Vulnerability Scoring System version 4.0", "https://www.first.org/cvss/v4.0/"),
    ("FIRST", "Common Vulnerability Scoring System version 4.0: Specification Document", "https://www.first.org/cvss/v4.0/specification-document"),
    ("FIRST", "Common Vulnerability Scoring System version 4.0: User Guide", "https://www.first.org/cvss/v4.0/user-guide"),
    ("FIRST", "Common Vulnerability Scoring System version 4.0: Implementation Guide", "https://www.first.org/cvss/v4.0/implementation-guide"),
    ("FIRST", "Common Vulnerability Scoring System version 4.0: Examples", "https://www.first.org/cvss/v4.0/examples"),
    ("FIRST", "Common Vulnerability Scoring System version 4.0: FAQ", "https://www.first.org/cvss/v4.0/faq"),
    ("FIRST", "CVSS v4.0 Calculator", "https://www.first.org/cvss/calculator/4.0"),
    ("FIRST", "CVSS Data Representations", "https://www.first.org/cvss/data-representations"),
    ("National Institute of Standards and Technology", "National Vulnerability Database API", "https://nvd.nist.gov/developers/vulnerabilities"),
]

reference_lines = []
for i, (org, title, url) in enumerate(official_refs, 1):
    reference_lines.append(f"[{i}] {org}, \"{title}.\" [Online]. Available: {url}. Accessed: Jul. 13, 2026.")

base_idx = len(reference_lines) + 1
for offset, row in enumerate(nvd_rows, 0):
    cve = row.get("cve_id", "").strip()
    if not cve:
        continue
    url = row.get("source_url", "").strip() or f"https://nvd.nist.gov/vuln/detail/{cve}"
    reference_lines.append(f"[{base_idx + offset}] National Vulnerability Database, \"{cve} Detail.\" [Online]. Available: {url}. Accessed: Jul. 13, 2026.")

references_md = f"""---
status: draft
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, references, ieee, article]
---

# CVSS v4.0 article references

Generated UTC: `{generated_at}`

## IEEE-style reference list

{chr(10).join(reference_lines)}

## Notes

These references are a preliminary IEEE-style bibliography for the manuscript draft. Before final submission, verify exact access dates, publication metadata, and conference formatting requirements.

The NVD references correspond to the real CVE rows currently present in `data/article/cvss40_environmental_scenarios.csv`.
"""

write(DOCS / "ARTICLE_REFERENCES_CVSS40.md", references_md)

abstract = f"""CVSS v4.0 defines Environmental metrics that allow vulnerability severity to be adapted to a consumer organization's deployment context. However, selecting Environmental metric values remains evidence-intensive because local asset criticality, exposure, compensating controls, and operational requirements are often distributed across multiple sources. This paper presents an AI/watcher-assisted workflow for collecting, structuring, and tracing environmental evidence used to support CVSS v4.0 Environmental metric assessment. The workflow preserves official CVSS v4.0 semantics and treats watcher output as evidence-backed candidate recommendations requiring human review, not as autonomous official scoring. We evaluate the approach using a hybrid dataset of {metrics.get('scenario_count')} scenarios, including {metrics.get('nvd_cvss_v4_rows')} real NVD/CVSS v4.0 vulnerability records and {metrics.get('synthetic_rows')} curated synthetic scenarios. The evaluation reports evidence coverage, trace completeness, uncertainty flags, human review status, and priority shifts between Base-only and Environmental-aware views. Results show {metrics.get('evidence_coverage_pct')}% evidence coverage, {metrics.get('trace_completeness_pct')}% trace completeness, and priority changes in {metrics.get('priority_shift_count')} of {metrics.get('scenario_count')} scenarios, supporting the feasibility of reproducible artifacts for assisting human review of Environmental metric choices."""

polished = f"""# Operationalizing CVSS v4.0 Environmental Metrics with AI-Assisted Evidence Collection and Traceability

Generated UTC: `{generated_at}`

## Abstract

{abstract}

## Keywords

CVSS v4.0; Environmental metrics; vulnerability prioritization; cybersecurity risk; artificial intelligence; traceability; reproducibility; human review.

## I. Introduction

The Common Vulnerability Scoring System is widely used to communicate vulnerability severity. In practice, however, vulnerability handling decisions often require more than a Base score. A vulnerability affecting an isolated lab asset, an identity provider, a public API gateway, or an operational technology monitoring component may require different remediation urgency even when the Base severity appears similar.

CVSS v4.0 provides a structured distinction between Base, Threat, Environmental, and Supplemental information [1], [2]. This distinction matters because Base metrics describe vulnerability characteristics, while Environmental metrics allow a consumer organization to represent local deployment context [2], [3]. The challenge addressed in this work is therefore operational rather than definitional: selecting Environmental metric values consistently requires evidence, local context, uncertainty handling, and reviewable decision records.

This paper proposes an AI/watcher-assisted workflow for Environmental metric assessment. The workflow collects and structures evidence, suggests candidate Environmental metric values, flags uncertainty, requires human review status, and exports trace artifacts. The contribution is a method and prototype workflow, not a new scoring standard.

## II. Background: CVSS v4.0 and Environmental Metrics

CVSS v4.0 separates vulnerability scoring and contextual information into metric groups including Base, Threat, Environmental, and Supplemental metrics [1], [2]. The workflow in this paper preserves that structure. Base CVSS information is stored separately as the severity baseline. Threat context is treated as time-sensitive evidence requiring review. Environmental assessment support is the main focus because it depends directly on consumer-side deployment context.

The workflow also preserves CVSS-B, CVSS-BT, CVSS-BE, and CVSS-BTE labeling discipline [2], [3]. Any score or priority table should identify which metric groups are represented and should not mix Base-only severity with Environmental-aware prioritization.

## III. Problem Statement

Although CVSS v4.0 defines Environmental metrics, applying them in a real consumer environment remains difficult. Analysts must determine asset importance, exposure, privilege context, compensating controls, confidentiality requirements, integrity requirements, availability requirements, and candidate Modified Base metric values. These inputs may be incomplete, distributed across multiple systems, or inconsistently documented.

This creates three practical problems. First, Environmental decisions may not be reproducible when the evidence trail is missing. Second, analysts may make inconsistent choices across similar assets. Third, remediation prioritization may over-rely on Base severity even when local context should change urgency.

## IV. Proposed AI/Watcher Workflow

The proposed workflow supports the analyst through eight steps: ingest vulnerability and Base CVSS v4.0 information; collect local environmental evidence; structure that evidence into scenario fields; suggest candidate Environmental metric values; attach evidence and rationale to each recommendation; flag uncertainty and missing evidence; require explicit human review status; and export CSV, JSON, report, and table artifacts for reproducibility.

The workflow does not modify the official CVSS v4.0 formula. It also does not present AI output as an autonomous official score. The intended output is a human-reviewable, evidence-backed recommendation.

## V. Prototype Architecture

The prototype uses a scenario dataset, validation scripts, trace JSON artifacts, generated Markdown tables, and article-ready result packages. Each scenario contains the Base vector and score, curated Environmental context, candidate Environmental assessment fields, evidence links, uncertainty flags, human review status, and priority comparison fields.

The current implementation produces the following artifacts:

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

## References

{chr(10).join(reference_lines)}
"""

write(GENERATED / "cvss40_ieee_manuscript_polished.md", polished)

double_blind = f"""# Operationalizing CVSS v4.0 Environmental Metrics with AI-Assisted Evidence Collection and Traceability

## Abstract

{abstract}

## Keywords

CVSS v4.0; Environmental metrics; vulnerability prioritization; cybersecurity risk; artificial intelligence; traceability; reproducibility; human review.

## I. Introduction

The Common Vulnerability Scoring System is widely used to communicate vulnerability severity. In practice, however, vulnerability handling decisions often require more than a Base score. A vulnerability affecting an isolated lab asset, an identity provider, a public API gateway, or an operational technology monitoring component may require different remediation urgency even when the Base severity appears similar.

CVSS v4.0 provides a structured distinction between Base, Threat, Environmental, and Supplemental information [1], [2]. This distinction matters because Base metrics describe vulnerability characteristics, while Environmental metrics allow a consumer organization to represent local deployment context [2], [3]. The challenge addressed in this work is therefore operational rather than definitional: selecting Environmental metric values consistently requires evidence, local context, uncertainty handling, and reviewable decision records.

This paper proposes an AI/watcher-assisted workflow for Environmental metric assessment. The workflow collects and structures evidence, suggests candidate Environmental metric values, flags uncertainty, requires human review status, and exports trace artifacts. The contribution is a method and prototype workflow, not a new scoring standard.

## II. Background: CVSS v4.0 and Environmental Metrics

CVSS v4.0 separates vulnerability scoring and contextual information into metric groups including Base, Threat, Environmental, and Supplemental metrics [1], [2]. The workflow in this paper preserves that structure. Base CVSS information is stored separately as the severity baseline. Threat context is treated as time-sensitive evidence requiring review. Environmental assessment support is the main focus because it depends directly on consumer-side deployment context.

The workflow also preserves CVSS-B, CVSS-BT, CVSS-BE, and CVSS-BTE labeling discipline [2], [3]. Any score or priority table should identify which metric groups are represented and should not mix Base-only severity with Environmental-aware prioritization.

## III. Problem Statement

Although CVSS v4.0 defines Environmental metrics, applying them in a real consumer environment remains difficult. Analysts must determine asset importance, exposure, privilege context, compensating controls, confidentiality requirements, integrity requirements, availability requirements, and candidate Modified Base metric values. These inputs may be incomplete, distributed across multiple systems, or inconsistently documented.

This creates three practical problems. First, Environmental decisions may not be reproducible when the evidence trail is missing. Second, analysts may make inconsistent choices across similar assets. Third, remediation prioritization may over-rely on Base severity even when local context should change urgency.

## IV. Proposed AI/Watcher Workflow

The proposed workflow supports the analyst through eight steps: ingest vulnerability and Base CVSS v4.0 information; collect local environmental evidence; structure that evidence into scenario fields; suggest candidate Environmental metric values; attach evidence and rationale to each recommendation; flag uncertainty and missing evidence; require explicit human review status; and export CSV, JSON, report, and table artifacts for reproducibility.

The workflow does not modify the official CVSS v4.0 formula. It also does not present AI output as an autonomous official score. The intended output is a human-reviewable, evidence-backed recommendation.

## V. Prototype Architecture

The prototype uses a scenario dataset, validation scripts, trace JSON artifacts, generated Markdown tables, and article-ready result packages. Each scenario contains the Base vector and score, curated Environmental context, candidate Environmental assessment fields, evidence links, uncertainty flags, human review status, and priority comparison fields.

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

## References

{chr(10).join(reference_lines)}
"""

write(GENERATED / "cvss40_ieee_manuscript_double_blind.md", double_blind)

readiness = f"""---
status: active
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, submission-readiness, double-blind, ieee]
---

# CVSS v4.0 article submission readiness

Generated UTC: `{generated_at}`

## Current manuscript artifacts

- `article/generated/cvss40_ieee_manuscript_draft.md`
- `article/generated/cvss40_ieee_manuscript_polished.md`
- `article/generated/cvss40_ieee_manuscript_double_blind.md`
- `docs/ARTICLE_REFERENCES_CVSS40.md`

## Dataset status

- Scenario count: {metrics.get('scenario_count')}
- NVD/CVSS v4.0 rows: {metrics.get('nvd_cvss_v4_rows')}
- Synthetic rows: {metrics.get('synthetic_rows')}
- Evidence coverage: {metrics.get('evidence_coverage_pct')}%
- Trace completeness: {metrics.get('trace_completeness_pct')}%
- Priority shift count: {metrics.get('priority_shift_count')}
- Priority shift percentage: {metrics.get('priority_shift_pct')}%

## Source counts

{dict(source_counts)}

## Severity counts

{dict(severity_counts)}

## Ready

- The article has a coherent IEEE-style structure.
- The dataset is hybrid and traceable.
- The manuscript states that the workflow does not modify CVSS v4.0.
- The manuscript states that watcher output is not autonomous official scoring.
- The manuscript includes limitations and threats to validity.
- The double-blind version omits local project owner metadata.

## Still required before real submission

- Convert Markdown into IEEE template format.
- Verify page length after formatting.
- Verify exact bibliography formatting.
- Add final author metadata only after double-blind review requirements are satisfied.
- Consider expert adjudication as a future validation phase.
"""

write(DOCS / "ARTICLE_SUBMISSION_READINESS_CVSS40.md", readiness)

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

upsert(
    "docs/00_Index.md",
    "CVSS40_PHASE8_POLISH_REFERENCES_INDEX_20260713",
    """## CVSS v4.0 Phase 8 Polish and References

- [Submission readiness](ARTICLE_SUBMISSION_READINESS_CVSS40.md)
- [References](ARTICLE_REFERENCES_CVSS40.md)
- [Polished manuscript](../article/generated/cvss40_ieee_manuscript_polished.md)
- [Double-blind manuscript](../article/generated/cvss40_ieee_manuscript_double_blind.md)
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE8_POLISH_REFERENCES_NEXT_20260713",
    """## CVSS v4.0 Phase 8 polish/references completed

Next actions:

1. Review `article/generated/cvss40_ieee_manuscript_polished.md`.
2. Review `article/generated/cvss40_ieee_manuscript_double_blind.md`.
3. Review `docs/ARTICLE_REFERENCES_CVSS40.md`.
4. Convert the double-blind manuscript into the IEEE template when ready.
5. Commit Phase 8 polish artifacts after validation.
"""
)

validator = r'''
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
'''

write(TOOLS / "validate_article_phase8_polish.py", validator)

print("\nRUN PHASE8 VALIDATION", flush=True)
commands = [
    ["python", "-X", "utf8", "tools/validate_article_cvss40_scenarios.py"],
    ["python", "-X", "utf8", "tools/validate_article_cvss40_docs.py"],
    ["python", "-X", "utf8", "tools/validate_article_phase5_results.py"],
    ["python", "-X", "utf8", "tools/validate_article_phase6_manuscript.py"],
    ["python", "-X", "utf8", "tools/validate_article_phase8_polish.py"],
    ["git", "diff", "--check"],
]

for cmd in commands:
    print("-- " + " ".join(cmd), flush=True)
    cp = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    print("rc=" + str(cp.returncode), flush=True)
    if cp.stdout:
        print(cp.stdout[-12000:], flush=True)
    if cp.stderr:
        print(cp.stderr[-8000:], flush=True)
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

print("CVSS40_PHASE8_POLISH_REFERENCES_END", flush=True)
