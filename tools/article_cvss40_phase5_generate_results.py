from pathlib import Path
import csv
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone

ROOT = Path.cwd()
DATASET = ROOT / "data" / "article" / "cvss40_environmental_scenarios.csv"
METRICS = ROOT / "validation" / "article" / "cvss40_scenario_metrics.json"
DOCS = ROOT / "docs"
GENERATED = ROOT / "article" / "generated"
TOOLS = ROOT / "tools"

print("CVSS40_PHASE5_ARTICLE_RESULTS_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: run from repository root")

if not DATASET.exists():
    raise SystemExit("ERROR: missing data/article/cvss40_environmental_scenarios.csv")

if not METRICS.exists():
    raise SystemExit("ERROR: missing validation/article/cvss40_scenario_metrics.json")

DOCS.mkdir(parents=True, exist_ok=True)
GENERATED.mkdir(parents=True, exist_ok=True)
TOOLS.mkdir(parents=True, exist_ok=True)

with DATASET.open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

metrics = json.loads(METRICS.read_text(encoding="utf-8", errors="replace"))

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

def esc(value):
    return str(value).replace("|", "\\|").replace("\n", " ").strip()

def table(headers, data_rows):
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in data_rows:
        out.append("| " + " | ".join(esc(x) for x in r) + " |")
    return "\n".join(out)

def pct(value):
    return f"{value:.2f}%"

scenario_count = int(metrics.get("scenario_count", len(rows)))
nvd_count = int(metrics.get("nvd_cvss_v4_rows", 0))
synthetic_count = int(metrics.get("synthetic_rows", 0))
evidence_pct = float(metrics.get("evidence_coverage_pct", 0))
trace_pct = float(metrics.get("trace_completeness_pct", 0))
uncertainty_pct = float(metrics.get("uncertainty_rate_pct", 0))
priority_shift_count = int(metrics.get("priority_shift_count", 0))
priority_shift_pct = float(metrics.get("priority_shift_pct", 0))
avg_delta = metrics.get("average_priority_delta", 0)
max_delta = metrics.get("max_priority_delta", 0)
min_delta = metrics.get("min_priority_delta", 0)

source_counts = Counter(r.get("scenario_source", "") for r in rows)
review_counts = Counter(r.get("human_review_status", "") for r in rows)
severity_counts = Counter(r.get("cvss_b_severity", "") for r in rows)
exposure_counts = Counter(r.get("internet_exposure", "") for r in rows)
asset_counts = Counter(r.get("asset_class", "") for r in rows)
priority_pairs = Counter((r.get("base_priority", ""), r.get("environmental_priority", "")) for r in rows)

nvd_rows = [r for r in rows if r.get("scenario_source") == "nvd_cvss_v4_with_curated_environment"]
synthetic_rows = [r for r in rows if r.get("scenario_source") == "curated_synthetic_no_cve"]

source_table = table(
    ["Scenario source", "Count"],
    [[k, v] for k, v in sorted(source_counts.items())]
)

severity_table = table(
    ["CVSS-B severity", "Count"],
    [[k, v] for k, v in sorted(severity_counts.items())]
)

exposure_table = table(
    ["Internet exposure", "Count"],
    [[k, v] for k, v in sorted(exposure_counts.items())]
)

asset_table = table(
    ["Asset class", "Count"],
    [[k, v] for k, v in sorted(asset_counts.items())]
)

priority_table = table(
    ["Base priority", "Environmental-aware priority", "Count"],
    [[base, env, count] for (base, env), count in sorted(priority_pairs.items())]
)

nvd_table_rows = []
for r in nvd_rows:
    nvd_table_rows.append([
        r.get("scenario_id", ""),
        r.get("cve_id", ""),
        r.get("cvss_b_score", ""),
        r.get("cvss_b_severity", ""),
        r.get("base_priority", ""),
        r.get("environmental_priority", ""),
        r.get("priority_delta", ""),
    ])

nvd_table = table(
    ["Scenario", "CVE", "CVSS-B score", "Severity", "Base priority", "Environmental priority", "Delta"],
    nvd_table_rows
)

summary_table = table(
    ["Metric", "Value"],
    [
        ["Scenario count", scenario_count],
        ["NVD CVSS v4.0 rows", nvd_count],
        ["Synthetic curated rows", synthetic_count],
        ["Evidence coverage", pct(evidence_pct)],
        ["Trace completeness", pct(trace_pct)],
        ["Uncertainty rate", pct(uncertainty_pct)],
        ["Human review required rows", review_counts.get("required", 0)],
        ["Priority shift count", priority_shift_count],
        ["Priority shift percentage", pct(priority_shift_pct)],
        ["Average priority delta", avg_delta],
        ["Maximum priority delta", max_delta],
        ["Minimum priority delta", min_delta],
    ]
)

generated_at = datetime.now(timezone.utc).isoformat()

evaluation_design = f"""# Evaluation Design section draft

This evaluation uses a curated hybrid scenario dataset to assess whether an AI/watcher-assisted workflow can support reproducible CVSS v4.0 Environmental metric assessment. The dataset contains {scenario_count} scenarios: {nvd_count} scenarios are based on real NVD vulnerability records with CVSS v4.0 data, and {synthetic_count} scenarios are synthetic curated cases used to preserve controlled variation across asset classes and deployment contexts.

For all scenarios, the official or assigned CVSS v4.0 Base vector and CVSS-B score are stored separately from the AI/watcher Environmental assessment fields. The local Environmental context is curated for article evaluation and includes asset class, deployment context, exposure, privilege assumptions, compensating controls, candidate Security Requirements, candidate Modified Base metric rationale, evidence summaries, uncertainty flags, and human review status.

The evaluation measures workflow properties rather than predictive superiority. The reported metrics are scenario count, evidence coverage, trace completeness, uncertainty flag coverage, explicit human review status, priority shifts between Base-only and Environmental-aware views, and the distribution of curated environment profiles. Watcher outputs are treated as evidence-backed candidate recommendations and not as autonomous official CVSS scores.
"""

results_section = f"""# Results section draft

The generated scenario dataset contains {scenario_count} scenarios. Of these, {nvd_count} use real NVD CVE records with CVSS v4.0 data and curated local Environmental contexts, while {synthetic_count} are explicitly marked as curated synthetic scenarios. Evidence coverage reached {evidence_pct:.2f}%, and trace completeness reached {trace_pct:.2f}%, indicating that each scenario contains evidence fields and a corresponding trace artifact.

All {scenario_count} scenarios retain explicit human review status, with {review_counts.get('required', 0)} marked as requiring review. This is consistent with the paper's boundary that AI/watcher output is a recommendation rather than a final official score. Uncertainty flags are present in {uncertainty_pct:.2f}% of scenarios, reflecting intentionally conservative handling of curated local context, threat-state uncertainty, and review requirements.

Priority changed in {priority_shift_count} of {scenario_count} scenarios ({priority_shift_pct:.2f}%) when moving from the Base-only view to the Environmental-aware view. The average priority delta was {avg_delta}, with a maximum upward shift of {max_delta} and a maximum downward shift of {min_delta}. These shifts show that the workflow can operationally differentiate vulnerability handling based on consumer-specific context while preserving the official CVSS v4.0 Base information as a separate baseline.
"""

discussion_section = """# Discussion section draft

The results support the feasibility of using an AI/watcher-assisted workflow to structure Environmental metric assessment around evidence, uncertainty, and reviewability. The workflow does not change the CVSS v4.0 formula and does not claim to produce autonomous official scores. Instead, it separates official Base severity from consumer-side Environmental assessment support.

The hybrid dataset improves over a purely synthetic evaluation by incorporating real NVD CVE records with CVSS v4.0 data. However, the Environmental contexts remain curated to evaluate the workflow under controlled assumptions. This design is appropriate for a method/prototype paper, but it should not be presented as evidence of production effectiveness or predictive superiority.

The strongest contribution is traceability: each scenario links the candidate Environmental assessment to evidence summaries, uncertainty flags, review status, and trace JSON. This makes the decision path inspectable and supports reproducibility. The main practical implication is that security teams can use the workflow to make Environmental assessment more explicit and auditable, while keeping final metric selection under human review.
"""

limitations_section = """# Limitations section draft

This work has several limitations. First, the dataset is curated and partially synthetic. Although part of the dataset uses real NVD CVE records with CVSS v4.0 data, the local Environmental contexts are curated for evaluation and do not represent production deployment measurements.

Second, the workflow does not validate predictive superiority, exploit likelihood, or real-world remediation outcomes. The evaluation measures traceability, evidence coverage, uncertainty handling, review status, and priority shifts, not whether the resulting priorities are objectively superior in production.

Third, the AI/watcher recommendations are not final official CVSS scores. The workflow requires explicit human review status, and final Environmental metric decisions remain analyst responsibility.

Fourth, threat context is treated conservatively. Unless a validated threat-intelligence process is integrated, threat-related fields should be interpreted as contextual evidence requiring review.

Finally, independent expert adjudication has not yet been completed. Future work should compare watcher-assisted recommendations with assessments by multiple security analysts and measure inter-rater agreement, review effort, and decision consistency.
"""

provenance_doc = f"""---
status: active
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, dataset, provenance, nvd, article]
---

# CVSS v4.0 article dataset provenance

Generated UTC: `{generated_at}`

## Summary

{summary_table}

## Source distribution

{source_table}

## CVSS-B severity distribution

{severity_table}

## Exposure distribution

{exposure_table}

## Asset class distribution

{asset_table}

## Priority transition distribution

{priority_table}

## NVD/CVSS v4.0 rows

{nvd_table if nvd_rows else "_No NVD CVSS v4.0 rows are currently present._"}

## Boundary

NVD rows use real NVD CVE records and CVSS v4.0 data where present in the dataset. The local Environmental context attached to those rows is curated for article evaluation. Synthetic rows are explicitly marked as `curated_synthetic_no_cve` and must not be presented as official CVE scoring.

The dataset supports workflow evaluation: evidence coverage, trace completeness, uncertainty handling, review status, and priority shifts. It does not prove production effectiveness or predictive superiority.
"""

results_doc = f"""---
status: draft
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, article, evaluation, results, environmental-metrics]
---

# CVSS v4.0 AI/watcher article: Evaluation and Results package

Generated UTC: `{generated_at}`

## Dataset summary

{summary_table}

## Dataset source distribution

{source_table}

## CVSS-B severity distribution

{severity_table}

## Exposure distribution

{exposure_table}

## Asset class distribution

{asset_table}

## Priority transition distribution

{priority_table}

## NVD/CVSS v4.0 scenario rows

{nvd_table if nvd_rows else "_No NVD CVSS v4.0 rows are currently present._"}

## Draft article text

{evaluation_design}

{results_section}

{discussion_section}

{limitations_section}

## Claim boundary

The article may describe the dataset as hybrid because it contains real NVD/CVSS v4.0 rows and curated synthetic rows. It must also state that the consumer Environmental context is curated and that watcher recommendations remain human-reviewable candidates, not autonomous official CVSS scores.
"""

write(GENERATED / "cvss40_evaluation_design_section.md", evaluation_design)
write(GENERATED / "cvss40_results_section.md", results_section)
write(GENERATED / "cvss40_discussion_section.md", discussion_section)
write(GENERATED / "cvss40_limitations_section.md", limitations_section)
write(DOCS / "ARTICLE_DATASET_PROVENANCE_CVSS40.md", provenance_doc)
write(DOCS / "ARTICLE_EVALUATION_RESULTS_CVSS40.md", results_doc)

upsert(
    "docs/ARTICLE_IEEE_SKELETON_CVSS40_AI_WATCHER.md",
    "CVSS40_PHASE5_GENERATED_EVALUATION_RESULTS_20260713",
    """## Generated Evaluation/Results material

Use the following generated files when expanding the IEEE manuscript:

- `article/generated/cvss40_evaluation_design_section.md`
- `article/generated/cvss40_results_section.md`
- `article/generated/cvss40_discussion_section.md`
- `article/generated/cvss40_limitations_section.md`
- `docs/ARTICLE_EVALUATION_RESULTS_CVSS40.md`
- `docs/ARTICLE_DATASET_PROVENANCE_CVSS40.md`

Current dataset framing: hybrid dataset with real NVD/CVSS v4.0 vulnerability records plus curated consumer Environmental contexts and explicitly marked synthetic scenarios.
"""
)

upsert(
    "docs/09_Paper_or_Article.md",
    "CVSS40_PHASE5_EVALUATION_RESULTS_20260713",
    """## Evaluation and Results status

The article now has generated Evaluation, Results, Discussion, and Limitations draft material based on the current scenario dataset.

Current dataset framing:

- Hybrid scenario dataset.
- Real NVD/CVSS v4.0 rows are used where available.
- Local Environmental context remains curated for workflow evaluation.
- Synthetic rows remain explicitly marked.
- Watcher outputs remain evidence-backed candidate recommendations requiring human review.
- The evaluation supports traceability/reproducibility claims, not production effectiveness or predictive superiority.
"""
)

upsert(
    "docs/00_Index.md",
    "CVSS40_PHASE5_EVALUATION_RESULTS_INDEX_20260713",
    """## CVSS v4.0 Phase 5 Evaluation/Results

- [Evaluation and Results package](ARTICLE_EVALUATION_RESULTS_CVSS40.md)
- [Dataset provenance](ARTICLE_DATASET_PROVENANCE_CVSS40.md)
- [Generated Evaluation Design](../article/generated/cvss40_evaluation_design_section.md)
- [Generated Results](../article/generated/cvss40_results_section.md)
- [Generated Discussion](../article/generated/cvss40_discussion_section.md)
- [Generated Limitations](../article/generated/cvss40_limitations_section.md)
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE5_EVALUATION_RESULTS_NEXT_20260713",
    """## CVSS v4.0 Phase 5 Evaluation/Results completed

Next actions:

1. Review `docs/ARTICLE_EVALUATION_RESULTS_CVSS40.md`.
2. Integrate generated Evaluation, Results, Discussion, and Limitations into the IEEE manuscript skeleton.
3. Tighten language to maintain the safe claim boundary.
4. Run full validation.
5. Prepare a commit once docs, dataset, generated tables, and validation scripts are stable.
"""
)

validator = r'''
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
'''

write(TOOLS / "validate_article_phase5_results.py", validator)

print("\nRUN PHASE5 VALIDATION", flush=True)
for cmd in [
    ["python", "-X", "utf8", "tools/validate_article_cvss40_scenarios.py"],
    ["python", "-X", "utf8", "tools/validate_article_cvss40_docs.py"],
    ["python", "-X", "utf8", "tools/validate_article_phase5_results.py"],
]:
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

print("CVSS40_PHASE5_ARTICLE_RESULTS_END", flush=True)
