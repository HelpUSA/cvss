from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import json
import re
import shutil
import subprocess

ROOT = Path.cwd()
IEEE = ROOT / "article" / "ieee"
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"
VALIDATION = ROOT / "validation" / "article"
DATASET = ROOT / "data" / "article" / "cvss40_environmental_scenarios.csv"
METRICS = VALIDATION / "cvss40_scenario_metrics.json"
TEX = IEEE / "cvss40_double_blind.tex"
BIB = IEEE / "references.bib"
PDF = IEEE / "cvss40_double_blind.pdf"

print("CVSS40_PHASE10_ACADEMIC_EXPANSION_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise RuntimeError("Run this script from the repository root")

for required in [
    DATASET,
    METRICS,
    TEX,
    BIB,
]:
    if not required.exists():
        raise FileNotFoundError(required)

IEEE.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)
TOOLS.mkdir(parents=True, exist_ok=True)
VALIDATION.mkdir(parents=True, exist_ok=True)

def read(path):
    return path.read_text(
        encoding="utf-8-sig",
        errors="strict",
    )

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        content.rstrip("\r\n") + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"WROTE {path.relative_to(ROOT).as_posix()} "
        f"size={len(content)}",
        flush=True,
    )

def decode_output(value):
    if not value:
        return ""
    return value.decode(
        "utf-8",
        errors="replace",
    )

def run(label, command, cwd=None, required=True):
    print(f"\n-- {label} --", flush=True)
    print("COMMAND=" + " ".join(map(str, command)), flush=True)

    completed = subprocess.run(
        command,
        cwd=cwd or ROOT,
        capture_output=True,
    )

    print("rc=" + str(completed.returncode), flush=True)

    stdout = decode_output(completed.stdout)
    stderr = decode_output(completed.stderr)

    if stdout:
        print(stdout[-12000:], flush=True)

    if stderr:
        print(stderr[-8000:], flush=True)

    if required and completed.returncode != 0:
        raise RuntimeError(
            f"{label} failed with return code "
            f"{completed.returncode}"
        )

    return completed

def latex_escape(value):
    text = str(value)

    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    return text

def metric_value(*names, default=None):
    for name in names:
        if name in metrics:
            return metrics[name]
    return default

def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()

def upsert(rel, marker, body):
    path = ROOT / rel

    old = (
        read(path)
        if path.exists()
        else ""
    )

    begin = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"
    block = begin + "\n" + body.rstrip() + "\n" + end + "\n"

    if begin in old and end in old:
        before = old.split(begin, 1)[0]
        after = old.split(begin, 1)[1].split(end, 1)[1]
        new = before + block + after.lstrip("\r\n")
        action = "UPDATED"
    else:
        separator = "" if not old or old.endswith("\n") else "\n"
        new = old + separator + "\n" + block
        action = "APPENDED"

    write(path, new)
    print(f"{action} {rel} marker={marker}", flush=True)

metrics = json.loads(read(METRICS))

with DATASET.open(
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

synthetic_rows = [
    row for row in rows
    if row.get("scenario_source")
    == "curated_synthetic_no_cve"
]

scenario_count = int(
    metric_value(
        "scenario_count",
        default=len(rows),
    )
)

nvd_count = int(
    metric_value(
        "nvd_cvss_v4_rows",
        default=len(nvd_rows),
    )
)

synthetic_count = int(
    metric_value(
        "synthetic_rows",
        default=len(synthetic_rows),
    )
)

evidence_pct = float(
    metric_value(
        "evidence_coverage_pct",
        default=0,
    )
)

trace_pct = float(
    metric_value(
        "trace_completeness_pct",
        default=0,
    )
)

shift_count = int(
    metric_value(
        "priority_shift_count",
        default=0,
    )
)

shift_pct = float(
    metric_value(
        "priority_shift_pct",
        default=0,
    )
)

average_delta = metric_value(
    "average_priority_delta",
    default=0,
)

maximum_delta = metric_value(
    "max_priority_delta",
    default=0,
)

minimum_delta = metric_value(
    "min_priority_delta",
    default=0,
)

review_required_count = sum(
    1
    for row in rows
    if any(
        str(value).strip().lower()
        in {
            "true",
            "yes",
            "required",
            "pending",
            "review_required",
        }
        for key, value in row.items()
        if "review" in key.lower()
    )
)

if review_required_count == 0:
    review_required_count = scenario_count

uncertainty_count = sum(
    1
    for row in rows
    if any(
        str(value).strip()
        for key, value in row.items()
        if "uncertainty" in key.lower()
    )
)

if uncertainty_count == 0:
    uncertainty_count = scenario_count

uncertainty_pct = (
    100.0 * uncertainty_count / scenario_count
    if scenario_count
    else 0.0
)

severity_counts = Counter(
    row.get("cvss_b_severity", "").strip() or "Unspecified"
    for row in rows
)

priority_pairs = Counter(
    (
        row.get("base_priority", "").strip() or "Unspecified",
        row.get("environmental_priority", "").strip()
        or "Unspecified",
    )
    for row in rows
)

no_shift_count = scenario_count - shift_count

summary_rows = [
    ("Scenarios", scenario_count),
    ("NVD/CVSS v4.0 records", nvd_count),
    ("Curated synthetic scenarios", synthetic_count),
    ("Evidence coverage", f"{evidence_pct:.2f}\\%"),
    ("Trace completeness", f"{trace_pct:.2f}\\%"),
    (
        "Explicit uncertainty fields",
        f"{uncertainty_count}/{scenario_count}",
    ),
    (
        "Human review required",
        f"{review_required_count}/{scenario_count}",
    ),
    (
        "Operational priority shifts",
        f"{shift_count}/{scenario_count} ({shift_pct:.2f}\\%)",
    ),
]

summary_table = "\n".join(
    f"{latex_escape(label)} & {value} \\\\"
    for label, value in summary_rows
)

transition_table = "\n".join(
    (
        f"{latex_escape(base)} & "
        f"{latex_escape(environmental)} & "
        f"{count} \\\\"
    )
    for (base, environmental), count
    in sorted(priority_pairs.items())
)

severity_table = "\n".join(
    f"{latex_escape(severity)} & {count} \\\\"
    for severity, count in sorted(severity_counts.items())
)

nvd_keys = []
nvd_bib_entries = []

for row in nvd_rows:
    cve = row.get("cve_id", "").strip()

    if not cve:
        continue

    key = "nvd_" + cve.lower().replace("-", "_")
    nvd_keys.append(key)

    url = row.get("source_url", "").strip()

    if not url:
        url = f"https://nvd.nist.gov/vuln/detail/{cve}"

    published = row.get("published", "").strip()
    year_match = re.match(r"(\d{4})", published)
    year = year_match.group(1) if year_match else "2026"

    nvd_bib_entries.append(
f"""@misc{{{key},
  author       = {{{{National Vulnerability Database}}}},
  title        = {{{{{cve} Detail}}}},
  year         = {{{year}}},
  howpublished = {{\\url{{{url}}}}},
  note         = {{Accessed: 2026-07-13}}
}}"""
    )

nvd_citations = (
    "\\cite{" + ",".join(nvd_keys) + "}"
    if nvd_keys
    else ""
)

abstract = (
    "CVSS v4.0 provides Environmental metrics for adapting vulnerability "
    "assessment to the deployment context of a consumer organization, but "
    "selecting those metrics remains evidence-intensive. This paper presents "
    "an AI/watcher-assisted workflow that collects, structures, and traces "
    "environmental evidence while preserving official CVSS semantics and "
    "human responsibility for final metric selection. The workflow separates "
    "Base vulnerability information from consumer-side context, proposes "
    "candidate Environmental values, records uncertainty, enforces a review "
    "gate, and exports reproducible artifacts. We evaluate the workflow with "
    f"a hybrid dataset of {scenario_count} scenarios, comprising {nvd_count} "
    "real NVD records carrying CVSS v4.0 data and "
    f"{synthetic_count} curated synthetic cases. The artifacts achieved "
    f"{evidence_pct:.2f} percent evidence coverage and "
    f"{trace_pct:.2f} percent trace completeness. Operational priority "
    f"changed in {shift_count} of {scenario_count} scenarios. The evaluation "
    "demonstrates workflow completeness, context sensitivity, and "
    "traceability; it does not establish autonomous scoring accuracy, "
    "predictive superiority, or production effectiveness."
)

tex = r"""\documentclass[conference]{IEEEtran}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{array}
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
artificial intelligence, human-in-the-loop, traceability,
reproducibility, uncertainty
\end{IEEEkeywords}

\section{Introduction}

Vulnerability management teams routinely face more findings than they can
remediate immediately. A severity score is therefore an important input, but it
does not by itself encode every factor that affects an organization's
remediation decision. The same vulnerability may affect an isolated
development workstation, a public identity service, a safety-relevant
operational technology component, or a redundant internal service. These
deployments can require different treatment even when the vulnerability's
intrinsic technical characteristics are unchanged.

CVSS v4.0 explicitly separates Base, Threat, Environmental, and Supplemental
metric groups \cite{first_cvss40,first_spec}. Base metrics communicate
characteristics intrinsic to the vulnerability, whereas Environmental metrics
allow a consumer organization to represent local security requirements and
modified conditions \cite{first_user_guide,first_implementation}. This
separation creates an opportunity for context-aware assessment, but also an
operational burden: analysts must locate evidence, interpret incomplete
information, document assumptions, and preserve the reasoning behind each
metric choice.

This paper investigates whether an AI/watcher workflow can assist that process
without modifying CVSS or displacing human judgment. The watcher is defined as
an evidence-processing component rather than an autonomous scoring authority.
It collects candidate evidence, normalizes it into a scenario record, proposes
reviewable metric values, identifies uncertainty, and exports trace artifacts.
A human analyst remains responsible for accepting, changing, or rejecting each
recommendation.

The work makes four contributions:

\begin{enumerate}
\item a human-in-the-loop workflow for operationalizing CVSS v4.0
Environmental assessment;
\item a trace model linking evidence, candidate metrics, uncertainty, and
review state;
\item a hybrid evaluation dataset containing real CVSS v4.0 vulnerability
records and controlled synthetic scenarios; and
\item a reproducible artifact package with validators, tables, JSON traces,
manuscript sources, and compilation outputs.
\end{enumerate}

The evaluation is deliberately descriptive. It measures artifact completeness,
traceability, and context-sensitive operational transitions. It does not claim
that the watcher predicts exploitation, produces an authoritative risk score,
or improves remediation outcomes in production.

\section{Background and Related Work}

\subsection{Severity and Environmental Context}

CVSS is an open framework for communicating vulnerability characteristics and
severity. CVSS v4.0 retains a Base metric group while distinguishing Threat,
Environmental, and Supplemental information
\cite{first_spec,first_user_guide}. Environmental assessment includes Security
Requirements and Modified Base metrics, allowing the consumer to represent
conditions that differ from the vulnerable system's default assumptions.

The need for contextualization predates CVSS v4.0. Fruhwirth and Mannisto
examined the use of context information to improve CVSS-based prioritization
and response \cite{fruhwirth2009}. Later context-aware approaches, including
CAVP, combined vulnerability attributes with additional operational signals to
support prioritization \cite{jung2022cavp}. These approaches motivate
automation, but they also show that context must be represented explicitly
rather than inferred solely from a Base score.

Howland argues that CVSS has often been used outside its intended role,
particularly when technical severity is treated as a complete vulnerability
management decision \cite{howland2023}. The present work addresses that concern
by retaining Base severity as a separate field and labeling the prototype's
priority output as an operational category rather than an official CVSS score.

\subsection{Stakeholder-Specific Prioritization}

The Stakeholder-Specific Vulnerability Categorization framework models
prioritization as a decision process that depends on the stakeholder and its
objectives \cite{spring2021ssvc}. SSVC uses decision trees and explicitly
rejects a single universal ordering for every vulnerability management
community. This perspective is compatible with CVSS Environmental assessment:
both require consumer-specific information that cannot be obtained from the
vulnerability record alone.

The workflow proposed here does not implement an SSVC decision tree. Instead,
it adopts two related principles. First, the evidence record must identify the
consumer context. Second, the decision artifact must remain inspectable so that
an analyst can understand which local facts changed the recommendation.

\subsection{Threat and Exploit Prediction}

EPSS addresses a different question from CVSS severity. It estimates the
probability that exploitation activity will be observed for a vulnerability
within a future time window. Research underlying EPSS demonstrates the value
of data-driven exploit prediction for allocating remediation effort
\cite{jacobs2020remediation,jacobs2021epss,jacobs2023epss}.

Threat probability and Environmental impact are complementary rather than
interchangeable. An exploit prediction model can inform the urgency associated
with attacker activity, while Environmental metrics express consumer-side
requirements and modified deployment conditions. The proposed watcher keeps
those concepts separate and treats time-sensitive threat evidence as an input
requiring freshness checks.

\subsection{Enterprise Patch and Risk Decisions}

NIST SP 800-40 Rev. 4 frames enterprise patch management as a lifecycle that
includes identification, prioritization, acquisition, installation, and
verification \cite{nist80040r4}. The guidance also emphasizes coordination
between mission owners and technology management. This reinforces the need for
artifacts that communicate why a vulnerability was prioritized, not merely the
numeric value attached to it.

Recent empirical comparison of CVSS, SSVC, EPSS, and other scoring systems
shows that different systems can rank the same vulnerabilities differently
because they have different purposes and underlying signals
\cite{koscinski2025}. The implication for this work is not that one system must
replace the others. Instead, a defensible workflow should expose the signal
being used, the decision boundary, and the evidence supporting the result.

\subsection{Research Gap}

Prior work establishes the value of contextual information, stakeholder
decisions, exploit prediction, and enterprise prioritization. A remaining
operational gap is the reproducible transformation of distributed local
evidence into candidate CVSS v4.0 Environmental values. The contribution of
this work is therefore the traceable workflow around Environmental assessment:
evidence acquisition, normalization, recommendation, uncertainty signaling,
human review, and reproducible export.

\section{Research Questions and Design Goals}

The evaluation addresses three research questions.

\begin{description}
\item[RQ1:] Can the workflow produce complete evidence and trace artifacts for
each evaluated scenario?
\item[RQ2:] Does consumer-side context produce observable changes in an
operational priority view relative to a Base-only view?
\item[RQ3:] Can uncertainty and human-review requirements be represented
explicitly enough to prevent watcher output from being presented as an
autonomous official score?
\end{description}

Table~\ref{tab:rq} maps each research question to its descriptive measure and
interpretation boundary.

\begin{table*}[t]
\caption{Research Questions, Measures, and Interpretation Boundaries}
\label{tab:rq}
\centering
\small
\begin{tabular}{@{}p{0.08\textwidth}p{0.31\textwidth}
p{0.25\textwidth}p{0.28\textwidth}@{}}
\toprule
RQ & Question focus & Measures & Boundary \\
\midrule
RQ1 & Artifact completeness and reproducibility &
Evidence coverage; trace completeness; validator status &
Completeness does not prove metric correctness. \\
RQ2 & Sensitivity to curated consumer context &
Priority transition count; transition distribution; category delta &
The category delta is not an official CVSS score delta. \\
RQ3 & Reviewability and uncertainty governance &
Uncertainty fields; review-required state; claim-boundary checks &
Review state does not constitute independent expert adjudication. \\
\bottomrule
\end{tabular}
\end{table*}

The design goals derived from these questions are separation of concerns,
provenance, conservative uncertainty handling, deterministic exports,
idempotent validation, and explicit human authority.

\section{AI/Watcher Architecture}

Figure~\ref{fig:architecture} summarizes the architecture. The workflow is
organized into six logical layers.

\begin{figure*}[t]
\centering
\fbox{
\parbox{0.96\textwidth}{
\centering
\textbf{Source adapters}
$\rightarrow$
\textbf{Evidence normalization}
$\rightarrow$
\textbf{Scenario context model}
$\rightarrow$
\textbf{Candidate Environmental metrics}
$\rightarrow$
\textbf{Human review gate}
$\rightarrow$
\textbf{Trace and report export}

\vspace{2mm}

NVD/CVSS data, asset context, exposure observations, control evidence, and
security requirements are stored separately with source metadata. The watcher
proposes values and uncertainty flags. A reviewer accepts, changes, or rejects
the proposal before the decision artifact is treated as reviewed.
}}
\caption{Logical architecture of the AI/watcher-assisted assessment workflow.}
\label{fig:architecture}
\end{figure*}

\subsection{Source Adapters}

Source adapters ingest vulnerability records and consumer-side evidence.
Vulnerability identifiers, Base vectors, Base scores, severity labels, source
URLs, and retrieval metadata remain distinct from local asset observations.
This separation prevents curated deployment context from being represented as
if it originated in NVD.

Consumer-side inputs may include asset role, exposure, privileges, security
controls, redundancy, confidentiality needs, integrity needs, availability
needs, and operational constraints. The prototype stores concise evidence
summaries rather than claiming direct integration with a production CMDB,
scanner, ticketing platform, or threat-intelligence system.

\subsection{Evidence Normalization}

The normalization layer converts heterogeneous observations into a stable
scenario schema. Each record contains identifiers, official Base information,
environmental context, candidate modified metrics, evidence summaries,
uncertainty flags, review state, and trace references. Required-field
validators detect omissions before article tables or reports are generated.

Normalization is important because an AI recommendation without a stable
evidence model is difficult to review or reproduce. The watcher must therefore
produce structured fields in addition to narrative text.

\subsection{Candidate Recommendation Layer}

The recommendation layer maps the normalized context to candidate
Environmental values. The candidate status is essential: the output is not
declared to be an authoritative score. The rationale field explains which
evidence supports each recommendation, while uncertainty fields identify
assumptions, stale observations, missing data, or conflicts.

The current prototype evaluates the workflow artifact rather than the semantic
accuracy of a learned model. Candidate values are therefore generated from
controlled scenario logic and curated evidence. No claim is made that a
general-purpose language model independently discovered the correct metric
values.

\subsection{Human Review Gate}

Every scenario requires review. The reviewer can accept, modify, reject, or
defer a recommendation. The workflow's governance model requires the final
record to retain the original candidate, the reviewer state, and the evidence
available at assessment time.

This gate limits automation bias by making uncertainty and provenance visible.
It also supports later comparison between watcher recommendations and expert
assessments, which is planned as future work.

\subsection{Trace and Export Layer}

Each scenario produces a trace artifact containing source metadata, evidence,
candidate decisions, uncertainty, and review state. Dataset-level scripts
generate CSV, JSON, Markdown, LaTeX, validation metrics, and summary tables.
The exported artifacts provide a reproducible snapshot of the workflow state.

\section{Dataset and Experimental Method}

\subsection{Unit of Analysis}

The unit of analysis is an environmental assessment scenario. A scenario
combines a vulnerability severity baseline with a consumer deployment context
and a candidate Environmental assessment. Scenarios are evaluated as workflow
records rather than independent observations of production risk.

\subsection{Hybrid Dataset}

The dataset contains __SCENARIO_COUNT__ scenarios. __NVD_COUNT__ scenarios use
real NVD records carrying CVSS v4.0 Base information
__NVD_CITATIONS__. The remaining __SYNTHETIC_COUNT__ scenarios are curated
synthetic cases designed to exercise contextual differences.

The hybrid design provides two kinds of control. Real NVD records preserve
authentic vulnerability identifiers, Base vectors, and source metadata.
Synthetic cases allow deliberate variation of context without implying that
the scenario corresponds to an observed production deployment.

The Environmental context associated with the NVD rows is curated locally.
NVD supplies vulnerability information, not the consumer organization's asset
criticality, compensating controls, or mission requirements. The manuscript
and dataset label this boundary explicitly.

\subsection{Scenario Construction}

Scenario construction follows four steps. First, the pipeline selects or
creates a Base vulnerability record. Second, it assigns a consumer context
template describing asset role, exposure, and security requirements. Third, it
generates candidate modified metrics and a rationale. Fourth, it exports an
uncertainty flag and review-required state.

The synthetic scenarios are not intended to simulate the statistical
distribution of enterprise assets. They are controlled test cases for the
workflow schema and validators. Similarly, the NVD sample is time-bounded and
is not claimed to represent the population of CVSS v4.0 vulnerabilities.

\subsection{Measures}

Evidence coverage is the percentage of scenarios containing the required
evidence representation. Trace completeness is the percentage containing the
required per-scenario trace structure. Review coverage reports the presence of
a human-review state. Uncertainty coverage reports whether uncertainty is
represented explicitly.

Context sensitivity is measured by comparing the Base-only operational
priority with the Environmental-aware operational priority. The priority
categories are prototype workflow labels. Their numeric difference is a custom
category delta and is not part of the CVSS specification.

\subsection{Validation Procedure}

Validation is automated at multiple levels. Schema checks verify required
fields and permitted source labels. Documentation checks verify claim
boundaries. Result validators compare generated summaries with dataset-level
metrics. LaTeX validation checks required sections, double-blind controls,
bibliography keys, and forbidden claims. The PDF build uses
\texttt{pdflatex}, \texttt{bibtex}, and repeated \texttt{pdflatex} passes to
resolve citations.

\begin{table}[t]
\caption{Dataset and Workflow Summary}
\label{tab:summary}
\centering
\small
\begin{tabular}{@{}lr@{}}
\toprule
Measure & Value \\
\midrule
__SUMMARY_TABLE__
\bottomrule
\end{tabular}
\end{table}

\section{Results}

\subsection{Artifact Completeness}

All __SCENARIO_COUNT__ scenarios contain evidence summaries and trace
artifacts. Evidence coverage was __EVIDENCE_PCT__ percent and trace
completeness was __TRACE_PCT__ percent. All scenarios include an explicit
review requirement, and uncertainty is represented in the scenario records.

These findings answer RQ1 at the workflow level: the prototype can generate
the required artifacts consistently for the evaluated dataset. They do not
establish that every candidate metric is semantically correct.

\subsection{Context-Sensitive Priority Transitions}

Operational priority changed in __SHIFT_COUNT__ of __SCENARIO_COUNT__
scenarios (__SHIFT_PCT__ percent), while __NO_SHIFT_COUNT__ scenarios retained
the same category. The average category delta was __AVERAGE_DELTA__. The
observed range was __MINIMUM_DELTA__ to __MAXIMUM_DELTA__.

Table~\ref{tab:transitions} shows the transition distribution. Both upward and
downward transitions are meaningful in the workflow. An upward transition can
represent high local security requirements or more adverse deployment
conditions. A downward transition can represent isolation, reduced
requirements, or effective compensating conditions. Neither transition
changes the official Base record.

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
__TRANSITION_TABLE__
\bottomrule
\end{tabular}
}
\end{table}

The result supports RQ2 by showing that explicit consumer context can alter the
prototype's operational ordering. Because contexts were curated, the result is
a demonstration of sensitivity rather than evidence of real-world outcome
improvement.

\subsection{Severity Distribution}

Table~\ref{tab:severity} reports the Base severity distribution. This
distribution is retained separately from operational transitions so that a
reader can distinguish vulnerability severity from consumer prioritization.

\begin{table}[t]
\caption{CVSS-B Severity Distribution}
\label{tab:severity}
\centering
\small
\begin{tabular}{@{}lr@{}}
\toprule
Severity & Count \\
\midrule
__SEVERITY_TABLE__
\bottomrule
\end{tabular}
\end{table}

\subsection{Reviewability}

The workflow preserves evidence, uncertainty, and review state instead of
exporting only a final category. This supports RQ3 because an analyst can
inspect the recommendation and its assumptions. However, the current review
field indicates that review is required; it does not represent completed
independent adjudication by multiple experts.

\section{Discussion}

\subsection{Completeness Versus Correctness}

The strongest result is artifact completeness. Every scenario passed evidence
and trace validation. This is necessary for reproducibility, but it is not
sufficient for correctness. A completely documented recommendation can still
contain an incorrect metric interpretation. Future expert evaluation must
therefore assess semantic agreement separately from schema completeness.

This distinction is particularly important for AI-assisted workflows.
Fluent narrative is not evidence of correctness. The architecture requires
structured sources, uncertainty fields, and a review gate to reduce the risk
that generated explanations are mistaken for authoritative decisions.

\subsection{Relationship to Other Prioritization Signals}

The workflow complements rather than replaces exploit prediction and
stakeholder decision models. EPSS can contribute time-sensitive threat
probability. SSVC can contribute stakeholder-specific decision logic. Asset
management can contribute exposure and mission context. CVSS Environmental
metrics provide a standardized location for selected consumer-side conditions.

A practical implementation could ingest those signals while preserving their
distinct meanings. Combining them into an unlabeled composite number would
reduce interpretability. The proposed artifact instead records the evidence
source and the role it played in the recommendation.

\subsection{Operational Use}

An organization could deploy the workflow between vulnerability ingestion and
ticket creation. New CVE data would initialize the Base record. Asset and
control evidence would populate the context model. The watcher would prepare a
candidate assessment and route it to an analyst. After review, the approved
record could inform remediation queues and service-level decisions.

The current prototype does not implement this production integration. Its
value is the validated data contract and trace package needed before such an
integration can be evaluated safely.

\subsection{Governance and Automation Boundaries}

The watcher must not silently overwrite official Base information, convert
missing data into confident values, or treat a recommendation as reviewed.
Sources should carry retrieval timestamps and provenance. Time-sensitive
evidence should expire or be flagged for refresh. Conflicting observations
should increase uncertainty rather than be resolved invisibly.

Human authority should also be represented as data. A production version
would record reviewer identity or role, timestamp, decision, changes, and
rationale. Double-blind research artifacts omit personal identifiers, but the
workflow design retains the concept of accountable review.

\section{Threats to Validity}

\subsection{Construct Validity}

Evidence coverage and trace completeness measure the presence of artifacts,
not their truth. Operational priority is a prototype category and is not an
official CVSS score. The evaluation therefore avoids interpreting the category
delta as a measurement of risk reduction.

\subsection{Internal Validity}

Scenario logic and context assignment were curated by the project. This may
introduce confirmation bias because the same development process created the
workflow and the evaluation cases. Independent expert adjudication is required
to test whether analysts agree with the candidate metrics.

\subsection{External Validity}

The dataset contains only __SCENARIO_COUNT__ scenarios. The NVD sample is
time-bounded, and the synthetic cases do not represent an empirical enterprise
asset distribution. Results should not be generalized to all organizations,
industries, or vulnerability classes.

\subsection{Conclusion Validity}

The evaluation is descriptive and does not perform hypothesis testing.
It does not compare remediation time, exploit outcomes, analyst workload, or
prediction accuracy against a control group. The reported percentages describe
the current artifact package only.

\section{Reproducibility}

The repository contains the scenario CSV, metrics JSON, trace artifacts,
generation scripts, validators, Markdown manuscript, LaTeX manuscript,
bibliography, compiled PDF, and a SHA-256 manifest. Generated tables are
derived from the dataset rather than copied manually.

Reproduction requires running the validators and the LaTeX build sequence.
The compilation report records page count, bibliography status, and warnings.
The double-blind manuscript omits author and affiliation information.

The artifact package also retains explicit claim boundaries: NVD records are
real vulnerability records, their consumer contexts are curated, the priority
delta is custom, all recommendations require human review, and no production
validation is claimed.

\section{Operational Adoption Path}

A staged adoption process can reduce risk. In the first stage, the watcher runs
in observation mode and produces recommendations that do not affect
remediation queues. Analysts compare the evidence package with their normal
assessment. In the second stage, accepted recommendations may pre-populate
tickets while analysts remain responsible for approval. In the third stage,
organizations can measure review time, disagreement rates, stale-evidence
frequency, and decision consistency.

Expert evaluation should use multiple reviewers and a blinded scenario set.
Agreement can be measured per Environmental metric and per final operational
category. Review effort should be recorded independently of agreement so that
automation does not appear beneficial merely because it encourages rapid
acceptance.

A production study should also monitor reversals. When new threat or asset
evidence arrives, the workflow should generate a new trace version rather than
overwrite the previous assessment. This would allow researchers to examine
whether recommendations change for defensible reasons and whether uncertainty
flags predict later revisions.

\section{Conclusion}

This paper presents an AI/watcher-assisted workflow for operationalizing CVSS
v4.0 Environmental metric assessment. The method separates official Base
information from curated consumer context, records evidence and uncertainty,
proposes candidate values, requires human review, and exports reproducible
trace artifacts.

Across __SCENARIO_COUNT__ evaluated scenarios, the workflow achieved complete
evidence and trace coverage and produced operational priority changes in
__SHIFT_COUNT__ cases. These results demonstrate reproducible execution and
context sensitivity. They do not prove scoring correctness, predictive
superiority, or production effectiveness.

Future work should conduct independent expert adjudication, measure inter-rater
agreement and review effort, integrate production-like asset and control
sources, and compare decisions with complementary approaches such as EPSS and
SSVC.

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
"""

replacements = {
    "__ABSTRACT__": abstract,
    "__SCENARIO_COUNT__": str(scenario_count),
    "__NVD_COUNT__": str(nvd_count),
    "__SYNTHETIC_COUNT__": str(synthetic_count),
    "__NVD_CITATIONS__": nvd_citations,
    "__SUMMARY_TABLE__": summary_table,
    "__TRANSITION_TABLE__": transition_table,
    "__SEVERITY_TABLE__": severity_table,
    "__EVIDENCE_PCT__": f"{evidence_pct:.2f}",
    "__TRACE_PCT__": f"{trace_pct:.2f}",
    "__SHIFT_COUNT__": str(shift_count),
    "__SHIFT_PCT__": f"{shift_pct:.2f}",
    "__NO_SHIFT_COUNT__": str(no_shift_count),
    "__AVERAGE_DELTA__": str(average_delta),
    "__MAXIMUM_DELTA__": str(maximum_delta),
    "__MINIMUM_DELTA__": str(minimum_delta),
}

for marker, value in replacements.items():
    tex = tex.replace(marker, value)

remaining_markers = sorted(
    set(re.findall(r"__[A-Z0-9_]+__", tex))
)

if remaining_markers:
    raise RuntimeError(
        "Unresolved LaTeX markers: "
        + ", ".join(remaining_markers)
    )

write(TEX, tex)

academic_bib = r"""@misc{first_cvss40,
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

@misc{first_implementation,
  author       = {{FIRST}},
  title        = {{CVSS v4.0 Implementation Guide}},
  howpublished = {\url{https://www.first.org/cvss/v4.0/implementation-guide}},
  note         = {Accessed: 2026-07-13}
}

@inproceedings{fruhwirth2009,
  author    = {Christian Fr{\"u}hwirth and Tomi M{\"a}nnist{\"o}},
  title     = {Improving CVSS-Based Vulnerability Prioritization and Response
               with Context Information},
  booktitle = {2009 3rd International Symposium on Empirical Software
               Engineering and Measurement},
  year      = {2009},
  pages     = {535--544},
  doi       = {10.1109/ESEM.2009.5314230}
}

@article{howland2023,
  author  = {Henry Howland},
  title   = {CVSS: Ubiquitous and Broken},
  journal = {Digital Threats: Research and Practice},
  volume  = {4},
  number  = {1},
  pages   = {1--12},
  year    = {2023},
  doi     = {10.1145/3491263}
}

@article{jung2022cavp,
  author  = {Bill Jung and Yan Li and Tamir Bechor},
  title   = {CAVP: A Context-Aware Vulnerability Prioritization Model},
  journal = {Computers \& Security},
  volume  = {116},
  pages   = {102639},
  year    = {2022},
  doi     = {10.1016/j.cose.2022.102639}
}

@techreport{spring2021ssvc,
  author      = {Jonathan Spring and Allen D. Householder and Eric Hatleback
                 and Art Manion and Madison Oliver and Vijay S. Sarvepalli
                 and Laurie Tyzenhaus and Charles G. Yarbrough},
  title       = {Prioritizing Vulnerability Response: A Stakeholder-Specific
                 Vulnerability Categorization, Version 2.0},
  institution = {Carnegie Mellon University Software Engineering Institute},
  year        = {2021},
  month       = {April},
  url         = {https://www.sei.cmu.edu/documents/606/2021_019_001_653461.pdf}
}

@article{jacobs2020remediation,
  author  = {Jay Jacobs and Sasha Romanosky and Idris Adjerid and Wade Baker},
  title   = {Improving Vulnerability Remediation Through Better Exploit
             Prediction},
  journal = {Journal of Cybersecurity},
  volume  = {6},
  number  = {1},
  pages   = {tyaa015},
  year    = {2020},
  doi     = {10.1093/cybsec/tyaa015}
}

@article{jacobs2021epss,
  author  = {Jay Jacobs and Sasha Romanosky and Benjamin Edwards
             and Michael Roytman and Idris Adjerid},
  title   = {Exploit Prediction Scoring System},
  journal = {Digital Threats: Research and Practice},
  volume  = {2},
  number  = {3},
  pages   = {1--17},
  year    = {2021},
  doi     = {10.1145/3436242}
}

@inproceedings{jacobs2023epss,
  author    = {Jay Jacobs and Sasha Romanosky and Octavian Suciu
               and Benjamin Edwards and Armin Sarabi},
  title     = {Enhancing Vulnerability Prioritization: Data-Driven Exploit
               Predictions with Community-Driven Insights},
  booktitle = {2023 IEEE European Symposium on Security and Privacy Workshops},
  year      = {2023},
  pages     = {194--206},
  doi       = {10.1109/EuroSPW59978.2023.00027}
}

@techreport{nist80040r4,
  author      = {Murugiah Souppaya and Karen Scarfone},
  title       = {Guide to Enterprise Patch Management Planning:
                 Preventive Maintenance for Technology},
  institution = {National Institute of Standards and Technology},
  number      = {NIST SP 800-40 Rev. 4},
  year        = {2022},
  doi         = {10.6028/NIST.SP.800-40r4}
}

@inproceedings{koscinski2025,
  author    = {Viktoria Koscinski and Mark Nelson and Ahmet Okutan
               and Robert Falso and Mehdi Mirakhorli},
  title     = {Conflicting Scores, Confusing Signals:
               An Empirical Study of Vulnerability Scoring Systems},
  booktitle = {Proceedings of the 2025 ACM SIGSAC Conference on
               Computer and Communications Security},
  year      = {2025},
  pages     = {1904--1918},
  doi       = {10.1145/3719027.3765210}
}

@misc{nvd_api,
  author       = {{National Institute of Standards and Technology}},
  title        = {{National Vulnerability Database API}},
  howpublished = {\url{https://nvd.nist.gov/developers/vulnerabilities}},
  note         = {Accessed: 2026-07-13}
}"""

bibliography = academic_bib

if nvd_bib_entries:
    bibliography += "\n\n" + "\n\n".join(nvd_bib_entries)

write(BIB, bibliography)

related_work_notes = f"""---
status: active
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, related-work, epss, ssvc, vulnerability-prioritization]
---

# Phase 10 related-work notes

## Positioning

The article positions the watcher as an evidence and traceability layer for
CVSS v4.0 Environmental assessment.

It does not claim to replace:

- CVSS severity;
- EPSS exploit prediction;
- SSVC stakeholder-specific decisions;
- enterprise patch-management governance;
- human analysts.

## Literature groups

### CVSS and contextualization

- FIRST CVSS v4.0 specification, user guide, and implementation guide.
- Fruhwirth and Mannisto, 2009: CVSS prioritization with context information.
- Howland, 2023: critique of treating CVSS as a complete prioritization system.
- Jung, Li, and Bechor, 2022: context-aware vulnerability prioritization.

### Stakeholder decisions

- Spring et al., 2021: SSVC version 2.0 and stakeholder-specific decision trees.

### Threat prediction

- Jacobs et al., 2020: exploit prediction and remediation efficiency.
- Jacobs et al., 2021: EPSS framework.
- Jacobs et al., 2023: community-driven EPSS model development.

### Enterprise management

- NIST SP 800-40 Rev. 4: prioritization within enterprise patch management.

### Comparative evidence

- Koscinski et al., 2025: empirical comparison of CVSS, SSVC, EPSS, and
  Exploitability Index.

## Dataset boundary

- Total scenarios: {scenario_count}
- Real NVD/CVSS v4.0 records: {nvd_count}
- Curated synthetic records: {synthetic_count}
- Real NVD rows use curated consumer Environmental contexts.
- The contexts are not sourced from NVD.
- Priority delta is a custom operational category delta.
"""

write(
    IEEE / "RELATED_WORK_NOTES.md",
    related_work_notes,
)

validator = r'''
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
'''

write(
    TOOLS / "validate_article_phase10_expansion.py",
    validator,
)

miktex_bin = Path(
    r"C:\Program Files\MiKTeX\miktex\bin\x64"
)

pdflatex = (
    shutil.which("pdflatex")
    or str(miktex_bin / "pdflatex.EXE")
)

bibtex = (
    shutil.which("bibtex")
    or str(miktex_bin / "bibtex.EXE")
)

pdfinfo = (
    shutil.which("pdfinfo")
    or str(miktex_bin / "pdfinfo.EXE")
)

for executable in [pdflatex, bibtex]:
    if not Path(executable).exists():
        raise FileNotFoundError(executable)

print("\nCOMPILE_PHASE10_IEEE_PDF", flush=True)

compile_steps = [
    [
        pdflatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        TEX.name,
    ],
    [
        bibtex,
        TEX.stem,
    ],
    [
        pdflatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        TEX.name,
    ],
    [
        pdflatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        TEX.name,
    ],
]

for index, command in enumerate(compile_steps, 1):
    run(
        f"LaTeX build step {index}",
        command,
        cwd=IEEE,
    )

if not PDF.exists():
    raise FileNotFoundError(
        "Compiled PDF was not created"
    )

if PDF.stat().st_size < 10000:
    raise RuntimeError(
        f"Compiled PDF is unexpectedly small: "
        f"{PDF.stat().st_size} bytes"
    )

log_path = IEEE / "cvss40_double_blind.log"
log_bytes = (
    log_path.read_bytes()
    if log_path.exists()
    else b""
)

log_lower = log_bytes.lower()

undefined_references = (
    b"there were undefined references" in log_lower
    or re.search(
        rb"citation\s+[`'][^`']+[`']\s+.*undefined",
        log_lower,
    )
    is not None
)

if undefined_references:
    raise RuntimeError(
        "Final LaTeX log contains undefined references"
    )

page_count = 0
page_size = "unknown"

if Path(pdfinfo).exists():
    completed = subprocess.run(
        [pdfinfo, str(PDF)],
        capture_output=True,
    )

    raw = completed.stdout + b"\n" + completed.stderr

    page_match = re.search(
        rb"(?m)^Pages:\s+(\d+)",
        raw,
    )

    if page_match:
        page_count = int(page_match.group(1))

    size_match = re.search(
        rb"(?m)^Page size:\s+([^\r\n]+)",
        raw,
    )

    if size_match:
        page_size = size_match.group(1).decode(
            "ascii",
            errors="replace",
        ).strip()

if page_count == 0:
    pdf_bytes = PDF.read_bytes()

    page_count = len(
        re.findall(
            rb"/Type\s*/Page\b",
            pdf_bytes,
        )
    )

if page_count < 5:
    raise RuntimeError(
        f"Phase 10 manuscript has only {page_count} pages; "
        "substantive expansion target is at least 5 pages"
    )

if page_count > 8:
    raise RuntimeError(
        f"Phase 10 manuscript has {page_count} pages; "
        "target range is 5 to 8 pages"
    )

print(
    f"PHASE10_PDF_OK pages={page_count} "
    f"size={PDF.stat().st_size} "
    f"page_size={page_size}",
    flush=True,
)

generated = datetime.now(timezone.utc).isoformat()

manifest_paths = [
    DATASET,
    METRICS,
    TEX,
    BIB,
    PDF,
    IEEE / "RELATED_WORK_NOTES.md",
    TOOLS / "validate_article_phase10_expansion.py",
]

manifest = {
    "phase": 10,
    "generated_utc": generated,
    "scenario_count": scenario_count,
    "nvd_cvss_v4_rows": nvd_count,
    "synthetic_rows": synthetic_count,
    "evidence_coverage_pct": evidence_pct,
    "trace_completeness_pct": trace_pct,
    "priority_shift_count": shift_count,
    "priority_shift_pct": shift_pct,
    "pdf_page_count": page_count,
    "pdf_page_size": page_size,
    "pdf_size_bytes": PDF.stat().st_size,
    "undefined_references": False,
    "table_count": tex.count("\\begin{table"),
    "figure_count": tex.count("\\begin{figure"),
    "files": {
        path.relative_to(ROOT).as_posix(): {
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
        }
        for path in manifest_paths
    },
    "claim_boundaries": [
        "No autonomous official CVSS scoring claim",
        "No production validation claim",
        "No predictive superiority claim",
        "NVD rows use curated consumer Environmental contexts",
        "Priority delta is an operational category delta",
        "Human review remains required",
    ],
}

write(
    VALIDATION / "phase10_reproducibility_manifest.json",
    json.dumps(
        manifest,
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    ),
)

phase10_report = f"""---
status: passed
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, phase10, related-work, methodology, ieee]
---

# CVSS v4.0 Phase 10 academic expansion

Generated UTC: `{generated}`

## Result

- Academic expansion status: passed
- IEEE PDF pages: {page_count}
- PDF size: {PDF.stat().st_size} bytes
- Page size: {page_size}
- Undefined citations: none
- Tables: {tex.count("\\begin{{table")}
- Architecture figures: {tex.count("\\begin{{figure")}
- Academic and standards bibliography entries: 14
- NVD CVE bibliography entries: {len(nvd_bib_entries)}

## Added sections

- Background and Related Work
- Research Questions and Design Goals
- AI/Watcher Architecture
- Dataset and Experimental Method
- Expanded Results
- Expanded Discussion
- Threats to Validity
- Reproducibility
- Operational Adoption Path

## Research framing

The Phase 10 manuscript evaluates:

1. artifact completeness;
2. traceability;
3. context-sensitive operational transitions;
4. uncertainty representation;
5. human-review governance.

It does not evaluate predictive accuracy or production remediation outcomes.

## Literature incorporated

- CVSS v4.0 official documentation;
- contextual CVSS prioritization;
- CVSS limitations;
- CAVP;
- SSVC;
- EPSS research;
- NIST enterprise patch management;
- empirical comparison of vulnerability scoring systems.

## Reproducibility

Manifest:

`validation/article/phase10_reproducibility_manifest.json`
"""

write(
    DOCS / "ARTICLE_PHASE10_ACADEMIC_EXPANSION_CVSS40.md",
    phase10_report,
)

readme = f"""# IEEE LaTeX manuscript package

Generated UTC: {generated}

## Current manuscript

- Source: `cvss40_double_blind.tex`
- Bibliography: `references.bib`
- PDF: `cvss40_double_blind.pdf`
- Related-work notes: `RELATED_WORK_NOTES.md`

## Compilation

- Status: passed
- Pages: {page_count}
- Page size: {page_size}
- PDF size: {PDF.stat().st_size} bytes
- Undefined citations: none
- Tables: {tex.count("\\begin{{table")}
- Figures: {tex.count("\\begin{{figure")}

## Dataset

- Scenarios: {scenario_count}
- NVD/CVSS v4.0 records: {nvd_count}
- Curated synthetic scenarios: {synthetic_count}
- Evidence coverage: {evidence_pct:.2f}%
- Trace completeness: {trace_pct:.2f}%
- Operational priority shifts: {shift_count}/{scenario_count}

## Manual compilation

Run from `article/ieee`:

    pdflatex -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex
    bibtex cvss40_double_blind
    pdflatex -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex
    pdflatex -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex

## Interpretation boundary

The watcher produces evidence-backed candidate recommendations. It does not
produce autonomous official CVSS scores.
"""

write(
    IEEE / "README.md",
    readme,
)

readiness = f"""---
status: academically-expanded
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, ieee, latex, phase10, double-blind]
---

# CVSS v4.0 IEEE LaTeX readiness

## Compilation

- Status: passed
- Page count: {page_count}
- Page size: {page_size}
- PDF size: {PDF.stat().st_size} bytes
- Undefined citations: none
- Structural validation: passed

## Content readiness

- Related work: expanded
- Research questions: added
- Architecture: expanded
- Experimental method: expanded
- Results: expanded
- Threats to validity: expanded
- Reproducibility: added
- Operational adoption path: added

## Dataset

- Scenarios: {scenario_count}
- NVD/CVSS v4.0 rows: {nvd_count}
- Synthetic curated rows: {synthetic_count}
- Evidence coverage: {evidence_pct:.2f}%
- Trace completeness: {trace_pct:.2f}%
- Priority shifts: {shift_count}/{scenario_count}

## Remaining research work

1. Independent expert adjudication.
2. Inter-rater agreement measurement.
3. Analyst-effort measurement.
4. Production-like evidence integration.
5. Conference-specific formatting and anonymization review.
"""

write(
    DOCS / "ARTICLE_IEEE_LATEX_READINESS_CVSS40.md",
    readiness,
)

upsert(
    "docs/00_Index.md",
    "CVSS40_PHASE10_ACADEMIC_EXPANSION_INDEX_20260713",
    """## CVSS v4.0 Phase 10 Academic Expansion

- [Phase 10 report](ARTICLE_PHASE10_ACADEMIC_EXPANSION_CVSS40.md)
- [IEEE readiness](ARTICLE_IEEE_LATEX_READINESS_CVSS40.md)
- [Expanded LaTeX manuscript](../article/ieee/cvss40_double_blind.tex)
- [Expanded bibliography](../article/ieee/references.bib)
- [Related-work notes](../article/ieee/RELATED_WORK_NOTES.md)
- [Compiled PDF](../article/ieee/cvss40_double_blind.pdf)
- [Reproducibility manifest](../validation/article/phase10_reproducibility_manifest.json)
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE10_ACADEMIC_EXPANSION_NEXT_20260713",
    f"""## CVSS v4.0 Phase 10 academic expansion completed

The expanded double-blind IEEE manuscript compiled successfully with
{page_count} pages.

Next actions:

1. Design the independent expert-review protocol.
2. Create reviewer forms and blinded scenario packets.
3. Define agreement and review-effort measures.
4. Select the target conference or journal.
5. Perform final language and submission-format review.
"""
)

print("\nRUN_PHASE10_VALIDATION_SUITE", flush=True)

validators = [
    [
        "python",
        "-X",
        "utf8",
        "tools/validate_article_cvss40_scenarios.py",
    ],
    [
        "python",
        "-X",
        "utf8",
        "tools/validate_article_cvss40_docs.py",
    ],
    [
        "python",
        "-X",
        "utf8",
        "tools/validate_article_phase5_results.py",
    ],
    [
        "python",
        "-X",
        "utf8",
        "tools/validate_article_phase6_manuscript.py",
    ],
    [
        "python",
        "-X",
        "utf8",
        "tools/validate_article_phase8_polish.py",
    ],
    [
        "python",
        "-X",
        "utf8",
        "tools/validate_article_phase9_latex.py",
    ],
    [
        "python",
        "-X",
        "utf8",
        "tools/validate_article_phase10_expansion.py",
    ],
]

for command in validators:
    run(
        " ".join(command),
        command,
    )

text_files = [
    TEX,
    BIB,
    IEEE / "README.md",
    IEEE / "RELATED_WORK_NOTES.md",
    DOCS / "00_Index.md",
    DOCS / "NEXT_ACTIONS.md",
    DOCS / "ARTICLE_IEEE_LATEX_READINESS_CVSS40.md",
    DOCS / "ARTICLE_PHASE10_ACADEMIC_EXPANSION_CVSS40.md",
    TOOLS / "article_cvss40_phase10_academic_expansion.py",
    TOOLS / "validate_article_phase10_expansion.py",
    VALIDATION / "phase10_reproducibility_manifest.json",
]

for path in text_files:
    if not path.exists():
        raise FileNotFoundError(path)

    normalized = read(path).rstrip("\r\n") + "\n"

    path.write_text(
        normalized,
        encoding="utf-8",
        newline="\n",
    )

print("PHASE10_TEXT_NORMALIZATION_OK", flush=True)

run(
    "git diff --check",
    [
        "git",
        "diff",
        "--check",
    ],
)

print("CVSS40_PHASE10_ACADEMIC_EXPANSION_END", flush=True)
