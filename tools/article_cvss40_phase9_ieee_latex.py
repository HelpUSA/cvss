from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv
import json
import re
import shutil
import subprocess
import sys

ROOT = Path.cwd()
DATASET = ROOT / "data/article/cvss40_environmental_scenarios.csv"
METRICS = ROOT / "validation/article/cvss40_scenario_metrics.json"
IEEE = ROOT / "article/ieee"
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"

print("CVSS40_PHASE9_IEEE_LATEX_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise SystemExit("ERROR: execute from repository root")

for path in [DATASET, METRICS]:
    if not path.exists():
        raise SystemExit(f"ERROR: missing {path.relative_to(ROOT)}")

IEEE.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)
TOOLS.mkdir(parents=True, exist_ok=True)

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"WROTE {path.relative_to(ROOT).as_posix()} size={len(text)}", flush=True)

def esc(value):
    text = str(value)
    for old, new in [
        ("&", r"\&"),
        ("%", r"\%"),
        ("_", r"\_"),
        ("#", r"\#"),
    ]:
        text = text.replace(old, new)
    return text

def run(label, cmd, fail=True, cwd=None):
    print(f"\n-- {label} --", flush=True)
    cp = subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        text=True,
        capture_output=True,
    )
    print("rc=" + str(cp.returncode), flush=True)
    if cp.stdout:
        print(cp.stdout[-12000:], flush=True)
    if cp.stderr:
        print(cp.stderr[-8000:], flush=True)
    if fail and cp.returncode != 0:
        raise SystemExit(cp.returncode)
    return cp

metrics = json.loads(METRICS.read_text(encoding="utf-8"))

with DATASET.open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

nvd_rows = [
    row for row in rows
    if row.get("scenario_source") == "nvd_cvss_v4_with_curated_environment"
]

synthetic_rows = [
    row for row in rows
    if row.get("scenario_source") == "curated_synthetic_no_cve"
]

scenario_count = int(metrics.get("scenario_count", len(rows)))
nvd_count = int(metrics.get("nvd_cvss_v4_rows", len(nvd_rows)))
synthetic_count = int(metrics.get("synthetic_rows", len(synthetic_rows)))
evidence_pct = float(metrics.get("evidence_coverage_pct", 0))
trace_pct = float(metrics.get("trace_completeness_pct", 0))
uncertainty_pct = float(metrics.get("uncertainty_rate_pct", 0))
shift_count = int(metrics.get("priority_shift_count", 0))
shift_pct = float(metrics.get("priority_shift_pct", 0))
average_delta = metrics.get("average_priority_delta", 0)
maximum_delta = metrics.get("max_priority_delta", 0)
minimum_delta = metrics.get("min_priority_delta", 0)

severity_counts = Counter(row.get("cvss_b_severity", "") for row in rows)

priority_pairs = Counter(
    (
        row.get("base_priority", ""),
        row.get("environmental_priority", ""),
    )
    for row in rows
)

summary_rows = [
    ("Scenarios", scenario_count),
    ("NVD/CVSS v4.0 records", nvd_count),
    ("Curated synthetic scenarios", synthetic_count),
    ("Evidence coverage", f"{evidence_pct:.2f}\\%"),
    ("Trace completeness", f"{trace_pct:.2f}\\%"),
    ("Rows requiring review", scenario_count),
    ("Priority shifts", f"{shift_count} ({shift_pct:.2f}\\%)"),
]

summary_tex = "\n".join(
    f"{esc(label)} & {value} \\\\"
    for label, value in summary_rows
)

transition_tex = "\n".join(
    f"{esc(base)} & {esc(environmental)} & {count} \\\\"
    for (base, environmental), count in sorted(priority_pairs.items())
)

severity_tex = "\n".join(
    f"{esc(severity)} & {count} \\\\"
    for severity, count in sorted(severity_counts.items())
)

nvd_keys = []
nvd_bib = []

for row in nvd_rows:
    cve = row.get("cve_id", "").strip()
    if not cve:
        continue

    key = "nvd_" + cve.lower().replace("-", "_")
    nvd_keys.append(key)

    url = row.get("source_url", "").strip()
    if not url:
        url = f"https://nvd.nist.gov/vuln/detail/{cve}"

    published = row.get("published", "")
    match = re.match(r"(\d{4})", published)
    year = match.group(1) if match else "2026"

    nvd_bib.append(
f"""@misc{{{key},
  author       = {{{{National Vulnerability Database}}}},
  title        = {{{{{cve} Detail}}}},
  year         = {{{year}}},
  howpublished = {{\\url{{{url}}}}},
  note         = {{Accessed: 2026-07-13}}
}}"""
    )

nvd_citation = (
    "\\cite{" + ",".join(nvd_keys) + "}"
    if nvd_keys else ""
)

abstract = (
    f"CVSS v4.0 defines Environmental metrics that adapt vulnerability "
    f"assessment to a consumer organization's deployment context. This paper "
    f"presents an AI/watcher-assisted workflow for collecting, structuring, "
    f"and tracing evidence used to support Environmental metric assessment. "
    f"The workflow preserves official CVSS semantics and treats its outputs "
    f"as evidence-backed candidate recommendations requiring human review. "
    f"The evaluation uses {scenario_count} scenarios, including {nvd_count} "
    f"NVD records carrying CVSS v4.0 data and {synthetic_count} curated "
    f"synthetic scenarios. Generated artifacts achieved {evidence_pct:.2f} "
    f"percent evidence coverage and {trace_pct:.2f} percent trace completeness. "
    f"Operational priority changed in {shift_count} of {scenario_count} "
    f"scenarios. These results demonstrate workflow execution and "
    f"traceability, not predictive superiority or production effectiveness."
)

tex = r"""\documentclass[conference]{IEEEtran}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{url}
\usepackage[hidelinks]{hyperref}
\usepackage{microtype}

\title{Operationalizing CVSS v4.0 Environmental Metrics with
AI-Assisted Evidence Collection and Traceability}

\author{
\IEEEauthorblockN{Anonymous Author(s)}
\IEEEauthorblockA{Affiliation withheld for double-blind review}
}

\begin{document}
\maketitle

\begin{abstract}
__ABSTRACT__
\end{abstract}

\begin{IEEEkeywords}
CVSS v4.0, Environmental metrics, vulnerability prioritization,
artificial intelligence, traceability, reproducibility, human review
\end{IEEEkeywords}

\section{Introduction}

The Common Vulnerability Scoring System is widely used to communicate
vulnerability severity. Operational remediation decisions, however, frequently
require more than a Base score because asset criticality, deployment context,
exposure, and compensating controls can change remediation urgency.

CVSS v4.0 distinguishes Base, Threat, Environmental, and Supplemental metric
groups \cite{first_cvss40,first_spec}. Environmental metrics allow consumer
organizations to represent local context \cite{first_user_guide,first_impl}.
Selecting these values consistently requires evidence, uncertainty handling,
and reviewable decision records.

This paper presents an AI/watcher-assisted workflow that structures evidence,
suggests candidate Environmental values, flags uncertainty, requires human
review, and exports reproducible trace artifacts. The contribution is a method
and prototype workflow, not a new scoring standard.

\section{Background}

The workflow preserves CVSS-B, CVSS-BT, CVSS-BE, and CVSS-BTE labeling.
Base information remains separate from consumer-side Environmental assessment.
Threat information is treated as time-sensitive evidence requiring independent
review. Supplemental information remains contextual.

Environmental assessment includes Security Requirements and Modified Base
metrics. Their selection depends on asset importance, architecture, exposure,
privileges, and compensating controls. The proposed workflow assists evidence
organization and analyst review rather than autonomous scoring.

\section{Problem Statement}

Environmental assessment can be difficult because relevant evidence is often
incomplete or distributed across multiple systems. This can reduce
reproducibility, create inconsistent assessments across similar assets, and
cause remediation decisions to over-rely on Base severity.

\section{Proposed Workflow}

The workflow performs eight activities:

\begin{enumerate}
\item ingest vulnerability and Base CVSS information;
\item collect consumer-side environmental evidence;
\item structure evidence into scenario fields;
\item suggest candidate Environmental metric values;
\item attach evidence and rationale;
\item flag uncertainty and missing evidence;
\item require explicit human review; and
\item export CSV, JSON, report, and table artifacts.
\end{enumerate}

The workflow does not modify the CVSS v4.0 formula. Its outputs are
human-reviewable candidate recommendations, not autonomous official scores.

\section{Prototype Architecture}

The prototype contains a scenario dataset, validators, per-scenario trace JSON,
generated tables, and manuscript artifacts. Each scenario stores Base
information separately from curated Environmental context, candidate metric
values, evidence, uncertainty flags, review status, and operational priority.

\section{Evaluation Design}

The evaluation uses __SCENARIO_COUNT__ scenarios. __NVD_COUNT__ scenarios use
NVD vulnerability records carrying CVSS v4.0 information
__NVD_CITATION__. The remaining __SYNTHETIC_COUNT__ scenarios are explicitly
marked as curated synthetic cases.

The Environmental contexts attached to the records are curated for workflow
evaluation. A real CVE record does not imply that its local deployment context
was obtained from NVD.

The evaluation measures workflow properties rather than predictive superiority:
evidence coverage, trace completeness, uncertainty coverage, review status,
and operational priority transitions.

\begin{table}[t]
\caption{Dataset and Workflow Summary}
\label{tab:summary}
\centering
\small
\begin{tabular}{@{}lr@{}}
\toprule
Measure & Value \\
\midrule
__SUMMARY_ROWS__
\bottomrule
\end{tabular}
\end{table}

\section{Results}

All __SCENARIO_COUNT__ scenarios contain evidence summaries and trace artifacts.
Every scenario requires human review. Uncertainty flags are present in
__UNCERTAINTY_PCT__ percent of records.

Operational priority changed in __SHIFT_COUNT__ of __SCENARIO_COUNT__ scenarios
(__SHIFT_PCT__ percent). The average category delta was __AVERAGE_DELTA__, with
a maximum upward delta of __MAXIMUM_DELTA__ and a maximum downward delta of
__MINIMUM_DELTA__.

The priority delta is an operational category transition. It is not an official
CVSS Environmental score difference and must not be interpreted as a
modification of the CVSS formula.

\begin{table}[t]
\caption{Operational Priority Transitions}
\label{tab:transitions}
\centering
\scriptsize
\resizebox{\columnwidth}{!}{
\begin{tabular}{@{}lll@{}}
\toprule
Base priority & Environmental-aware priority & Count \\
\midrule
__TRANSITION_ROWS__
\bottomrule
\end{tabular}
}
\end{table}

\begin{table}[t]
\caption{CVSS-B Severity Distribution}
\label{tab:severity}
\centering
\small
\begin{tabular}{@{}lr@{}}
\toprule
Severity & Count \\
\midrule
__SEVERITY_ROWS__
\bottomrule
\end{tabular}
\end{table}

\section{Discussion}

The results support the feasibility of structuring Environmental assessment
around evidence, uncertainty, traceability, and reviewability. The hybrid
dataset includes NVD records carrying CVSS v4.0 information \cite{nvd_api},
but the attached consumer contexts remain curated.

The results demonstrate artifact completeness and workflow execution. They do
not establish production effectiveness, scoring correctness, or predictive
superiority.

\section{Limitations and Threats to Validity}

The dataset is curated and partially synthetic. The consumer Environmental
contexts do not represent measured production deployments.

The evaluation does not measure exploit likelihood, remediation outcomes,
analyst time savings, or predictive superiority. Independent expert
adjudication has not yet been completed. The NVD sample is time-bounded and
must not be interpreted as representative of all CVSS v4.0 records.

\section{Conclusion}

This paper presents an AI/watcher-assisted workflow for supporting CVSS v4.0
Environmental metric assessment through evidence collection, traceability,
uncertainty flags, and explicit human review. The method preserves official
CVSS semantics and does not modify the standard.

Future work should add expert adjudication, peer-reviewed comparative
baselines, inter-rater agreement analysis, and production-like evaluation.

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
"""

replacements = {
    "__ABSTRACT__": abstract,
    "__SCENARIO_COUNT__": str(scenario_count),
    "__NVD_COUNT__": str(nvd_count),
    "__SYNTHETIC_COUNT__": str(synthetic_count),
    "__NVD_CITATION__": nvd_citation,
    "__SUMMARY_ROWS__": summary_tex,
    "__TRANSITION_ROWS__": transition_tex,
    "__SEVERITY_ROWS__": severity_tex,
    "__UNCERTAINTY_PCT__": f"{uncertainty_pct:.2f}",
    "__SHIFT_COUNT__": str(shift_count),
    "__SHIFT_PCT__": f"{shift_pct:.2f}",
    "__AVERAGE_DELTA__": str(average_delta),
    "__MAXIMUM_DELTA__": str(maximum_delta),
    "__MINIMUM_DELTA__": str(minimum_delta),
}

for marker, value in replacements.items():
    tex = tex.replace(marker, value)

write(IEEE / "cvss40_double_blind.tex", tex)

official_bib = r"""@misc{first_cvss40,
  author       = {{FIRST}},
  title        = {{Common Vulnerability Scoring System Version 4.0}},
  howpublished = {\url{https://www.first.org/cvss/v4.0/}},
  note         = {Accessed: 2026-07-13}
}

@misc{first_spec,
  author       = {{FIRST}},
  title        = {{CVSS v4.0 Specification Document}},
  howpublished = {\url{https://www.first.org/cvss/v4.0/specification-document}},
  note         = {Accessed: 2026-07-13}
}

@misc{first_user_guide,
  author       = {{FIRST}},
  title        = {{CVSS v4.0 User Guide}},
  howpublished = {\url{https://www.first.org/cvss/v4.0/user-guide}},
  note         = {Accessed: 2026-07-13}
}

@misc{first_impl,
  author       = {{FIRST}},
  title        = {{CVSS v4.0 Implementation Guide}},
  howpublished = {\url{https://www.first.org/cvss/v4.0/implementation-guide}},
  note         = {Accessed: 2026-07-13}
}

@misc{nvd_api,
  author       = {{National Institute of Standards and Technology}},
  title        = {{National Vulnerability Database API}},
  howpublished = {\url{https://nvd.nist.gov/developers/vulnerabilities}},
  note         = {Accessed: 2026-07-13}
}"""

bibliography = official_bib
if nvd_bib:
    bibliography += "\n\n" + "\n\n".join(nvd_bib)

write(IEEE / "references.bib", bibliography)

write(
    IEEE / ".gitignore",
    """*.aux
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
build/
"""
)

word_source = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", tex)
word_source = re.sub(r"[{}\\]", " ", word_source)
word_count = len(re.findall(r"\b[\w'-]+\b", word_source))

readme = f"""# IEEE LaTeX manuscript package

Generated UTC: {datetime.now(timezone.utc).isoformat()}

Files:
- cvss40_double_blind.tex
- references.bib
- .gitignore

Dataset:
- Scenarios: {scenario_count}
- NVD/CVSS v4.0 records: {nvd_count}
- Synthetic scenarios: {synthetic_count}
- Priority shifts: {shift_count}/{scenario_count}

Approximate extracted word count: {word_count}
Tables: 3
Bibliography entries: {5 + len(nvd_bib)}

Compile from PowerShell:

Set-Location D:\\dev\\cvss\\article\\ieee
latexmk -pdf -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex

The final page count must be checked in the compiled two-column PDF.
"""

write(IEEE / "README.md", readme)

readiness = f"""---
status: active
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, ieee, latex, double-blind]
---

# CVSS v4.0 IEEE LaTeX readiness

## Artifacts

- `article/ieee/cvss40_double_blind.tex`
- `article/ieee/references.bib`
- `article/ieee/README.md`

## Snapshot

- Scenarios: {scenario_count}
- NVD/CVSS v4.0 rows: {nvd_count}
- Synthetic rows: {synthetic_count}
- Evidence coverage: {evidence_pct:.2f}%
- Trace completeness: {trace_pct:.2f}%
- Priority shifts: {shift_count}/{scenario_count}
- Extracted word count: {word_count}

## Double-blind controls

- Anonymous author block.
- Affiliation withheld.
- No local Windows path inside the manuscript.
- No project owner metadata inside the manuscript.

## Remaining work

1. Compile and inspect the two-column PDF.
2. Verify target conference page limit.
3. Add peer-reviewed related work.
4. Verify conference anonymization requirements.
5. Consider independent expert adjudication.
"""

write(DOCS / "ARTICLE_IEEE_LATEX_READINESS_CVSS40.md", readiness)

validator = r'''
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
    "\\section{Results}",
    "\\bibliographystyle{IEEEtran}",
    "\\bibliography{references}",
]

normalized_tex = " ".join(tex.split()).lower()

phase9_compatibility_groups = [
    [
        "\\section{Evaluation Design}",
        "\\section{Dataset and Experimental Method}",
    ],
    [
        "\\section{Limitations and Threats to Validity}",
        "\\section{Threats to Validity}",
    ],
    [
        "does not modify",
        "without modifying CVSS",
    ],
    [
        "not an official CVSS Environmental score difference",
        "not an official CVSS score",
    ],
]

for alternatives in phase9_compatibility_groups:
    normalized_alternatives = [
        " ".join(term.split()).lower()
        for term in alternatives
    ]

    if not any(
        term in normalized_tex
        for term in normalized_alternatives
    ):
        print(
            "MISSING_TEX_COMPATIBILITY_GROUP",
            " OR ".join(alternatives),
        )
        sys.exit(1)

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
'''

write(TOOLS / "validate_article_phase9_latex.py", validator)

latexmk = shutil.which("latexmk")
pdflatex = shutil.which("pdflatex")

print("LATEXMK=" + (latexmk or "not-found"), flush=True)
print("PDFLATEX=" + (pdflatex or "not-found"), flush=True)

print("\nRUN PHASE9 VALIDATION", flush=True)

commands = [
    ["python", "-X", "utf8", "tools/validate_article_cvss40_scenarios.py"],
    ["python", "-X", "utf8", "tools/validate_article_cvss40_docs.py"],
    ["python", "-X", "utf8", "tools/validate_article_phase8_polish.py"],
    ["python", "-X", "utf8", "tools/validate_article_phase9_latex.py"],
    ["git", "diff", "--check"],
]

for cmd in commands:
    run(" ".join(cmd), cmd, fail=True)

print("\nVALIDATION SNAPSHOT", flush=True)

for label, cmd in [
    ("git status -sb", ["git", "status", "-sb"]),
    ("git diff --stat", ["git", "diff", "--stat"]),
    ("git diff --check", ["git", "diff", "--check"]),
]:
    run(label, cmd, fail=True)

print("CVSS40_PHASE9_IEEE_LATEX_END", flush=True)
