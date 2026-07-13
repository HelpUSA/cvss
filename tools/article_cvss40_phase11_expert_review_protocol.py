from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import random
import re
import shutil
import subprocess

ROOT = Path.cwd()
DATASET = ROOT / "data" / "article" / "cvss40_environmental_scenarios.csv"
IEEE = ROOT / "article" / "ieee"
REVIEW = ROOT / "article" / "expert_review"
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"
VALIDATION = ROOT / "validation" / "article"

TEX = IEEE / "cvss40_double_blind.tex"
BIB = IEEE / "references.bib"
PDF = IEEE / "cvss40_double_blind.pdf"

MANIFEST = VALIDATION / "phase11_expert_review_manifest.json"

SEED = 20260713
TARGET_REVIEWERS = 3

print("CVSS40_PHASE11_EXPERT_REVIEW_START", flush=True)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise RuntimeError("Run from the repository root")

for required in [DATASET, TEX, BIB, PDF]:
    if not required.exists():
        raise FileNotFoundError(required)

REVIEW.mkdir(parents=True, exist_ok=True)
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
        f"size={path.stat().st_size}",
        flush=True,
    )

def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"WROTE {path.relative_to(ROOT).as_posix()} "
        f"rows={len(rows)} "
        f"size={path.stat().st_size}",
        flush=True,
    )

def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()

def decode_output(value):
    if not value:
        return ""

    return value.decode(
        "utf-8",
        errors="replace",
    )

def run(label, command, cwd=None):
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

    if completed.returncode != 0:
        raise RuntimeError(
            f"{label} failed with return code "
            f"{completed.returncode}"
        )

    return completed

def upsert(rel, marker, body):
    path = ROOT / rel

    old = read(path) if path.exists() else ""

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
    print(
        f"{action} {rel} marker={marker}",
        flush=True,
    )

def scenario_id(row, index):
    for field in [
        "scenario_id",
        "id",
        "scenario",
    ]:
        value = row.get(field, "").strip()

        if value:
            return value

    return f"scenario-{index:03d}"

def blind_id(original_id):
    value = (
        f"phase11|{SEED}|{original_id}"
    ).encode("utf-8")

    digest = hashlib.sha256(value).hexdigest()[:12].upper()

    return "ER-" + digest

def first_value(row, candidates, default=""):
    for candidate in candidates:
        value = row.get(candidate, "").strip()

        if value:
            return value

    return default

def sanitize_blinded_value(value):
    """
    Remove vulnerability identifiers and URLs from reviewer-visible fields.

    The protected adjudication answer key remains unchanged.
    """
    text = str(value)

    text = re.sub(
        r"(?i)\bhttps?://[^\s,;)\]}>]+",
        "[redacted-source-url]",
        text,
    )

    text = re.sub(
        r"(?i)\bCVE-[A-Z0-9][A-Z0-9_.:-]*",
        "[redacted-vulnerability-id]",
        text,
    )

    return text

def classified_origin(row):
    source = row.get("scenario_source", "").strip()

    if source == "nvd_cvss_v4_with_curated_environment":
        return "real_cvss_v4_record_with_curated_context"

    if source == "curated_synthetic_no_cve":
        return "controlled_synthetic_scenario"

    return "other_controlled_record"

def detect_context_fields(fieldnames):
    allow_exact = {
        "scenario_title",
        "scenario_description",
        "deployment_context",
        "environment_context",
        "asset_context",
        "asset_role",
        "asset_type",
        "business_function",
        "service_role",
        "internet_exposed",
        "network_exposure",
        "exposure",
        "privileges",
        "privilege_context",
        "user_interaction",
        "security_requirements",
        "confidentiality_requirement",
        "integrity_requirement",
        "availability_requirement",
        "existing_controls",
        "compensating_controls",
        "control_context",
        "evidence_summary",
        "environmental_evidence",
        "deployment_evidence",
        "asset_evidence",
        "context_evidence",
    }

    allow_fragments = (
        "context",
        "asset",
        "exposure",
        "control",
        "requirement",
        "evidence",
        "deployment",
        "business",
        "service",
    )

    deny_fragments = (
        "candidate",
        "recommend",
        "priority",
        "delta",
        "review",
        "trace",
        "rationale",
        "uncertainty",
        "source_url",
        "retrieved",
        "published",
        "cve_id",
        "scenario_id",
        "environmental_vector",
        "modified_metric",
        "modified_metrics",
        "final_",
        "official_",
    )

    selected = []

    for field in fieldnames:
        lowered = field.lower()

        if any(fragment in lowered for fragment in deny_fragments):
            continue

        if (
            lowered in allow_exact
            or any(fragment in lowered for fragment in allow_fragments)
        ):
            selected.append(field)

    return selected

def detect_answer_fields(fieldnames):
    fragments = (
        "candidate",
        "recommend",
        "environmental",
        "modified",
        "priority",
        "delta",
        "rationale",
        "uncertainty",
        "review",
    )

    selected = []

    for field in fieldnames:
        lowered = field.lower()

        if any(fragment in lowered for fragment in fragments):
            selected.append(field)

    return selected

with DATASET.open(
    "r",
    encoding="utf-8-sig",
    newline="",
) as stream:
    reader = csv.DictReader(stream)
    rows = list(reader)
    fieldnames = list(reader.fieldnames or [])

if not rows:
    raise RuntimeError("Scenario dataset is empty")

scenario_count = len(rows)

context_fields = detect_context_fields(fieldnames)
answer_fields = detect_answer_fields(fieldnames)

base_vector_candidates = [
    "official_cvss_v4_vector",
    "cvss_b_vector",
    "cvss_base_vector",
    "base_vector",
    "official_vector",
]

base_score_candidates = [
    "official_cvss_v4_base_score",
    "cvss_b_score",
    "cvss_base_score",
    "base_score",
]

severity_candidates = [
    "cvss_b_severity",
    "cvss_base_severity",
    "base_severity",
    "severity",
]

blinded_rows = []
answer_rows = []

for index, row in enumerate(rows, 1):
    original_id = scenario_id(row, index)
    review_id = blind_id(original_id)

    blinded = {
        "review_scenario_id": review_id,
        "record_origin": classified_origin(row),
        "cvss_base_vector": first_value(
            row,
            base_vector_candidates,
            default="not_available",
        ),
        "cvss_base_score": first_value(
            row,
            base_score_candidates,
            default="not_available",
        ),
        "cvss_base_severity": first_value(
            row,
            severity_candidates,
            default="not_available",
        ),
    }

    for field in context_fields:
        value = row.get(field, "").strip()

        if value:
            blinded[field] = value

    # PHASE11_BLINDING_SANITIZATION
    blinded = {
        key: sanitize_blinded_value(value)
        for key, value in blinded.items()
    }

    blinded_serialized = " ".join(
        str(value)
        for value in blinded.values()
    ).lower()

    if "cve-" in blinded_serialized:
        raise RuntimeError(
            "CVE identifier remained after blinding "
            f"for {review_id}"
        )

    if (
        "http://" in blinded_serialized
        or "https://" in blinded_serialized
    ):
        raise RuntimeError(
            "Source URL remained after blinding "
            f"for {review_id}"
        )

    blinded_rows.append(blinded)

    answer = {
        "review_scenario_id": review_id,
        "original_scenario_id": original_id,
        "cve_id": row.get("cve_id", "").strip(),
        "scenario_source": row.get(
            "scenario_source",
            "",
        ).strip(),
    }

    for field in answer_fields:
        answer[field] = row.get(field, "").strip()

    answer_rows.append(answer)

base_blinded_fields = [
    "review_scenario_id",
    "record_origin",
    "cvss_base_vector",
    "cvss_base_score",
    "cvss_base_severity",
]

additional_blinded_fields = []

for row in blinded_rows:
    for key in row:
        if (
            key not in base_blinded_fields
            and key not in additional_blinded_fields
        ):
            additional_blinded_fields.append(key)

blinded_fields = (
    base_blinded_fields
    + sorted(additional_blinded_fields)
)

answer_fields_csv = [
    "review_scenario_id",
    "original_scenario_id",
    "cve_id",
    "scenario_source",
]

for field in answer_fields:
    if field not in answer_fields_csv:
        answer_fields_csv.append(field)

write_csv(
    REVIEW / "blinded_scenarios_master.csv",
    blinded_fields,
    blinded_rows,
)

write_csv(
    REVIEW / "adjudication_answer_key.csv",
    answer_fields_csv,
    answer_rows,
)

randomizer = random.Random(SEED)

packet_a = list(blinded_rows)
randomizer.shuffle(packet_a)

packet_b = list(reversed(packet_a))

packet_a_rows = []
packet_b_rows = []

for position, row in enumerate(packet_a, 1):
    item = {
        "packet_version": "A",
        "presentation_order": position,
    }
    item.update(row)
    packet_a_rows.append(item)

for position, row in enumerate(packet_b, 1):
    item = {
        "packet_version": "B",
        "presentation_order": position,
    }
    item.update(row)
    packet_b_rows.append(item)

packet_fields = [
    "packet_version",
    "presentation_order",
] + blinded_fields

write_csv(
    REVIEW / "review_packet_A.csv",
    packet_fields,
    packet_a_rows,
)

write_csv(
    REVIEW / "review_packet_B.csv",
    packet_fields,
    packet_b_rows,
)

reviewer_form_fields = [
    "reviewer_code",
    "packet_version",
    "review_scenario_id",
    "review_started_utc",
    "review_completed_utc",
    "review_duration_seconds",
    "evidence_sufficiency_1_to_5",
    "confidence_1_to_5",
    "reviewed_CR",
    "reviewed_IR",
    "reviewed_AR",
    "reviewed_MAV",
    "reviewed_MAC",
    "reviewed_MAT",
    "reviewed_MPR",
    "reviewed_MUI",
    "reviewed_MVC",
    "reviewed_MVI",
    "reviewed_MVA",
    "reviewed_MSC",
    "reviewed_MSI",
    "reviewed_MSA",
    "reviewed_environmental_vector",
    "reviewed_operational_priority",
    "evidence_missing",
    "ambiguity_detected",
    "decision_status",
    "reviewer_comments",
]

reviewer_form_rows = []

for row in packet_a_rows:
    reviewer_form_rows.append({
        "reviewer_code": "",
        "packet_version": "A",
        "review_scenario_id": row["review_scenario_id"],
        "review_started_utc": "",
        "review_completed_utc": "",
        "review_duration_seconds": "",
        "evidence_sufficiency_1_to_5": "",
        "confidence_1_to_5": "",
        "reviewed_CR": "",
        "reviewed_IR": "",
        "reviewed_AR": "",
        "reviewed_MAV": "",
        "reviewed_MAC": "",
        "reviewed_MAT": "",
        "reviewed_MPR": "",
        "reviewed_MUI": "",
        "reviewed_MVC": "",
        "reviewed_MVI": "",
        "reviewed_MVA": "",
        "reviewed_MSC": "",
        "reviewed_MSI": "",
        "reviewed_MSA": "",
        "reviewed_environmental_vector": "",
        "reviewed_operational_priority": "",
        "evidence_missing": "",
        "ambiguity_detected": "",
        "decision_status": "",
        "reviewer_comments": "",
    })

write_csv(
    REVIEW / "reviewer_response_template.csv",
    reviewer_form_fields,
    reviewer_form_rows,
)

assignment_rows = []

for reviewer_index in range(1, TARGET_REVIEWERS + 1):
    packet = "A" if reviewer_index % 2 else "B"

    assignment_rows.append({
        "reviewer_code": f"R{reviewer_index:02d}",
        "packet_version": packet,
        "scenario_count": scenario_count,
        "status": "not_started",
        "assigned_utc": "",
        "completed_utc": "",
        "response_file": (
            f"reviewer_R{reviewer_index:02d}_responses.csv"
        ),
    })

write_csv(
    REVIEW / "reviewer_assignment_plan.csv",
    [
        "reviewer_code",
        "packet_version",
        "scenario_count",
        "status",
        "assigned_utc",
        "completed_utc",
        "response_file",
    ],
    assignment_rows,
)

generated = datetime.now(timezone.utc).isoformat()

protocol = f"""---
status: protocol-ready
last_updated: 2026-07-13
tags: [cvss-v4, expert-review, blinded-study, human-in-the-loop]
---

# Independent expert-review protocol

Generated UTC: `{generated}`

## Objective

Evaluate whether independent vulnerability-management specialists agree with
the watcher-generated candidate CVSS v4.0 Environmental assessments.

This protocol evaluates agreement and review effort. It does not assume that
the watcher output or any single reviewer is an absolute ground truth.

## Study design

- Scenarios: {scenario_count}
- Target reviewers: {TARGET_REVIEWERS}
- Planned reviewer-scenario assessments:
  {scenario_count * TARGET_REVIEWERS}
- Packet versions: A and B
- Randomization seed: {SEED}
- Design: blinded, independently completed, counterbalanced ordering

## Blinding

Reviewers receive:

- a pseudonymous scenario identifier;
- Base vector, Base score, and Base severity when available;
- deployment and asset context;
- security requirements;
- control and evidence information.

Reviewers do not receive:

- CVE identifiers;
- source URLs;
- watcher candidate metric values;
- watcher rationales;
- priority deltas;
- watcher uncertainty decisions;
- original scenario identifiers;
- adjudication answer keys.

## Review task

For every scenario, the reviewer should:

1. inspect the supplied Base information;
2. inspect consumer-side context and evidence;
3. select Security Requirement values;
4. select applicable Modified Base metrics;
5. construct or record an Environmental vector;
6. select an operational priority category;
7. rate evidence sufficiency from 1 to 5;
8. rate confidence from 1 to 5;
9. record missing evidence and ambiguity;
10. record the time required.

## Reviewer eligibility

Recommended reviewers should have practical or research experience in at least
two of the following areas:

- vulnerability management;
- CVSS interpretation;
- security operations;
- patch management;
- risk assessment;
- asset or exposure management.

Reviewer experience must be documented separately from scenario responses.

## Independence

Reviewers must complete their first-pass assessments independently. Discussion
between reviewers is permitted only during a later adjudication stage.

## Adjudication

After independent review:

1. compare reviewer responses;
2. compare reviewers with the watcher answer key;
3. identify disagreements per metric;
4. conduct a structured adjudication meeting;
5. record whether disagreement resulted from insufficient evidence,
   interpretation ambiguity, reviewer error, or watcher error;
6. preserve both original and adjudicated decisions.

## Data-handling boundary

The current packet contains controlled research scenarios. It must not be
combined with confidential production evidence without an approved data
handling process.

Reviewer identifiers should remain pseudonymous in research exports.
"""

write(
    REVIEW / "PROTOCOL.md",
    protocol,
)

instructions = """# Reviewer instructions

## Before beginning

1. Use the reviewer code assigned to you.
2. Open only your assigned packet.
3. Do not open the adjudication answer key.
4. Do not search for a hidden CVE using contextual clues.
5. Complete the scenarios in the presented order.
6. Work independently.

## Allowed metric values

Security Requirements:

- CR: X, H, M, L
- IR: X, H, M, L
- AR: X, H, M, L

Modified Base metrics should use the values permitted by CVSS v4.0.

Use `X` when the Base value should remain inherited.

## Evidence sufficiency

- 1: insufficient for a defensible recommendation
- 2: substantial evidence missing
- 3: usable but incomplete
- 4: sufficient with minor limitations
- 5: clear and sufficient

## Confidence

- 1: very low confidence
- 2: low confidence
- 3: moderate confidence
- 4: high confidence
- 5: very high confidence

## Decision status

Use one of:

- `complete`
- `defer_missing_evidence`
- `defer_ambiguity`
- `not_assessable`

## Timing

Record start and completion timestamps or the total number of seconds spent on
each scenario.

Do not include personal or confidential information in reviewer comments.
"""

write(
    REVIEW / "REVIEWER_INSTRUCTIONS.md",
    instructions,
)

codebook = """# Expert-review data codebook

## Identification fields

- `reviewer_code`: pseudonymous reviewer identifier.
- `packet_version`: randomized order version A or B.
- `review_scenario_id`: blinded scenario identifier.

## Timing fields

- `review_started_utc`: ISO 8601 UTC timestamp.
- `review_completed_utc`: ISO 8601 UTC timestamp.
- `review_duration_seconds`: total scenario review time.

## Rating fields

- `evidence_sufficiency_1_to_5`: evidence sufficiency rating.
- `confidence_1_to_5`: reviewer confidence.

## CVSS Environmental fields

- `reviewed_CR`, `reviewed_IR`, `reviewed_AR`: Security Requirements.
- `reviewed_MAV` through `reviewed_MSA`: Modified Base metrics.
- `reviewed_environmental_vector`: assembled reviewed vector.

## Operational field

- `reviewed_operational_priority`: prototype operational category. It is not an
  official CVSS score.

## Governance fields

- `evidence_missing`: concise missing-evidence description.
- `ambiguity_detected`: concise ambiguity description.
- `decision_status`: complete or deferred state.
- `reviewer_comments`: optional rationale.

## Protected comparison fields

The adjudication answer key contains watcher recommendations and original
scenario identifiers. It must remain unavailable to reviewers until their
independent assessments are locked.
"""

write(
    REVIEW / "CODEBOOK.md",
    codebook,
)

analysis_plan = f"""# Expert-review analysis plan

## Sample

- Scenarios: {scenario_count}
- Planned reviewers: {TARGET_REVIEWERS}
- Planned assessments: {scenario_count * TARGET_REVIEWERS}
- Two counterbalanced packet orders

## Primary measures

### Metric-level exact agreement

For each CVSS Environmental metric:

- watcher-versus-reviewer exact agreement;
- pairwise reviewer exact agreement;
- majority-reviewer agreement with watcher;
- missing or deferred response rate.

### Multi-reviewer agreement

Where metric values are categorical, calculate:

- Fleiss' kappa when all reviewers assess every scenario;
- Krippendorff's alpha when missing values require a more flexible measure.

Report raw agreement alongside chance-corrected statistics.

### Operational-priority agreement

For ordered categories, calculate:

- exact agreement;
- adjacent-category agreement;
- weighted Cohen's kappa for pairwise comparisons;
- weighted multi-reviewer agreement where supported.

The priority category remains a prototype operational measure and is not an
official CVSS score.

## Secondary measures

- median review time per scenario;
- interquartile range of review time;
- median confidence;
- median evidence-sufficiency rating;
- defer rate;
- missing-evidence rate;
- ambiguity rate;
- watcher override rate after adjudication.

## Stratified analysis

Report measures separately for:

- real NVD/CVSS v4.0 records with curated consumer context;
- controlled synthetic scenarios;
- Base severity category;
- upward, downward, and unchanged watcher priority transitions;
- high-confidence versus low-confidence reviewer responses.

## Adjudication outcomes

Classify each disagreement as one of:

- insufficient evidence;
- ambiguous scenario language;
- reviewer interpretation difference;
- reviewer data-entry error;
- watcher recommendation error;
- CVSS specification interpretation issue;
- operational-priority framework issue.

## Interpretation boundary

The study can support claims about reviewer agreement, review effort, and
evidence sufficiency. It cannot by itself prove improved remediation outcomes,
exploit prediction, or production effectiveness.
"""

write(
    REVIEW / "ANALYSIS_PLAN.md",
    analysis_plan,
)

ethics = """# Ethics and data-handling checklist

- [ ] Reviewer participation requirements have been documented.
- [ ] Institutional or organizational review requirements have been checked.
- [ ] Reviewer identifiers are pseudonymous.
- [ ] No unnecessary personal data are collected.
- [ ] No confidential production asset data are included.
- [ ] Reviewers are informed that the watcher output is experimental.
- [ ] Reviewers complete independent assessments before adjudication.
- [ ] The answer key remains access-controlled until independent review ends.
- [ ] Original responses are preserved before adjudication.
- [ ] Research exports remove direct personal identifiers.
- [ ] Conflicts of interest are recorded.
- [ ] Reviewer consent or participation agreement is retained appropriately.
"""

write(
    REVIEW / "ETHICS_AND_DATA_HANDLING.md",
    ethics,
)

planned_section = r"""
\section{Planned Independent Expert Evaluation}

The next evaluation stage will compare watcher-generated candidate assessments
with independent specialist judgments. This stage is designed to test semantic
agreement and review effort, which are not established by the artifact
completeness results reported in this paper.

\subsection{Blinded Review Design}

Each reviewer receives a counterbalanced packet containing the Base vector,
Base score, Base severity, consumer deployment context, security requirements,
controls, and evidence. CVE identifiers, source URLs, watcher recommendations,
priority deltas, and rationales are withheld during the independent review.

Two deterministic packet orders reduce the likelihood that fatigue or learning
effects are confounded with a single presentation sequence. Reviewers record
Security Requirements, Modified Base metrics, an Environmental vector,
operational priority, confidence, evidence sufficiency, missing evidence,
ambiguity, and review duration.

\subsection{Agreement Measures}

The analysis plan reports raw metric-level agreement in addition to
chance-corrected measures. Fleiss' kappa or Krippendorff's alpha can be used for
multi-reviewer categorical agreement, depending on missing responses. Ordered
priority categories can be analyzed using weighted agreement. Review time,
confidence, evidence sufficiency, defer rates, and watcher override rates are
reported separately.

The operational priority remains a prototype category and is not an official
CVSS score. Agreement with the watcher is not treated as proof that either the
watcher or a reviewer is correct.

\subsection{Adjudication}

After independent responses are locked, disagreements are reviewed in a
structured adjudication stage. The adjudication record distinguishes
insufficient evidence, ambiguity, reviewer interpretation differences,
data-entry errors, watcher errors, specification interpretation issues, and
operational-priority framework issues.

This planned evaluation strengthens the human-in-the-loop design by measuring
where automation assists analysts and where it requires correction. No expert
agreement results are claimed in the present study.
""".strip()

tex = read(TEX)

section_marker = r"\section{Planned Independent Expert Evaluation}"
anchor = r"\section{Operational Adoption Path}"

if section_marker not in tex:
    if anchor not in tex:
        raise RuntimeError(
            "Operational Adoption Path section anchor not found"
        )

    tex = tex.replace(
        anchor,
        planned_section + "\n\n" + anchor,
        1,
    )

    print("INSERTED_PLANNED_EXPERT_EVALUATION_SECTION")
else:
    print("PLANNED_EXPERT_EVALUATION_SECTION_ALREADY_PRESENT")

write(TEX, tex)

validator = r'''
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
'''

write(
    TOOLS / "validate_article_phase11_expert_review.py",
    validator,
)

miktex = Path(
    r"C:\Program Files\MiKTeX\miktex\bin\x64"
)

pdflatex = (
    shutil.which("pdflatex")
    or str(miktex / "pdflatex.EXE")
)

bibtex = (
    shutil.which("bibtex")
    or str(miktex / "bibtex.EXE")
)

pdfinfo = (
    shutil.which("pdfinfo")
    or str(miktex / "pdfinfo.EXE")
)

for executable in [pdflatex, bibtex]:
    if not Path(executable).exists():
        raise FileNotFoundError(executable)

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

print("\nCOMPILE_PHASE11_MANUSCRIPT", flush=True)

for index, command in enumerate(compile_steps, 1):
    run(
        f"Phase 11 LaTeX step {index}",
        command,
        cwd=IEEE,
    )

if not PDF.exists():
    raise FileNotFoundError(PDF)

log = (
    IEEE / "cvss40_double_blind.log"
).read_bytes().lower()

undefined_references = (
    b"there were undefined references" in log
    or re.search(
        rb"citation\s+[`'][^`']+[`']\s+.*undefined",
        log,
    )
    is not None
)

if undefined_references:
    raise RuntimeError(
        "Undefined references remain after Phase 11 build"
    )

page_count = 0
page_size = "unknown"

if Path(pdfinfo).exists():
    completed = subprocess.run(
        [pdfinfo, str(PDF)],
        capture_output=True,
    )

    output = completed.stdout + b"\n" + completed.stderr

    match = re.search(
        rb"(?m)^Pages:\s+(\d+)",
        output,
    )

    if match:
        page_count = int(match.group(1))

    match = re.search(
        rb"(?m)^Page size:\s+([^\r\n]+)",
        output,
    )

    if match:
        page_size = match.group(1).decode(
            "ascii",
            errors="replace",
        ).strip()

if page_count == 0:
    page_count = len(
        re.findall(
            rb"/Type\s*/Page\b",
            PDF.read_bytes(),
        )
    )

if page_count < 5 or page_count > 8:
    raise RuntimeError(
        f"Phase 11 PDF has {page_count} pages; "
        "expected between 5 and 8"
    )

manifest_files = [
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
    TEX,
    BIB,
    PDF,
    TOOLS / "validate_article_phase11_expert_review.py",
]

manifest = {
    "phase": 11,
    "generated_utc": generated,
    "scenario_count": scenario_count,
    "target_reviewers": TARGET_REVIEWERS,
    "planned_assessments": scenario_count * TARGET_REVIEWERS,
    "packet_versions": ["A", "B"],
    "randomization_seed": SEED,
    "blinded_fields": blinded_fields,
    "protected_answer_fields": answer_fields_csv,
    "context_field_count": len(context_fields),
    "answer_field_count": len(answer_fields_csv),
    "pdf_page_count": page_count,
    "pdf_page_size": page_size,
    "pdf_size_bytes": PDF.stat().st_size,
    "undefined_references": False,
    "files": {
        path.relative_to(ROOT).as_posix(): {
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
        }
        for path in manifest_files
    },
    "claim_boundaries": [
        "Protocol only; no expert results have been collected",
        "Agreement does not establish absolute ground truth",
        "Priority category is not an official CVSS score",
        "Reviewers do not see watcher recommendations",
        "NVD consumer contexts remain curated",
        "No production effectiveness claim",
    ],
}

write(
    MANIFEST,
    json.dumps(
        manifest,
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    ),
)

report = f"""---
status: passed
last_updated: 2026-07-13
tags: [cvss-v4, phase11, expert-review, blinded-study]
---

# CVSS v4.0 Phase 11 expert-review protocol

Generated UTC: `{generated}`

## Result

- Protocol status: ready
- Scenarios: {scenario_count}
- Target reviewers: {TARGET_REVIEWERS}
- Planned assessments: {scenario_count * TARGET_REVIEWERS}
- Counterbalanced packets: A and B
- Randomization seed: {SEED}
- PDF pages after protocol section: {page_count}
- Undefined references: none

## Generated study artifacts

- blinded scenario master;
- packet A;
- packet B;
- reviewer response template;
- reviewer assignment plan;
- protected adjudication answer key;
- reviewer instructions;
- codebook;
- statistical analysis plan;
- ethics and data-handling checklist;
- reproducibility manifest.

## Important boundary

This phase creates the protocol and study instruments. No specialist responses
have been collected, and no agreement result is claimed.
"""

write(
    DOCS / "ARTICLE_PHASE11_EXPERT_REVIEW_PROTOCOL_CVSS40.md",
    report,
)

upsert(
    "docs/00_Index.md",
    "CVSS40_PHASE11_EXPERT_REVIEW_INDEX_20260713",
    """## CVSS v4.0 Phase 11 Expert Review

- [Phase 11 report](ARTICLE_PHASE11_EXPERT_REVIEW_PROTOCOL_CVSS40.md)
- [Review protocol](../article/expert_review/PROTOCOL.md)
- [Reviewer instructions](../article/expert_review/REVIEWER_INSTRUCTIONS.md)
- [Codebook](../article/expert_review/CODEBOOK.md)
- [Analysis plan](../article/expert_review/ANALYSIS_PLAN.md)
- [Ethics checklist](../article/expert_review/ETHICS_AND_DATA_HANDLING.md)
- [Blinded packet A](../article/expert_review/review_packet_A.csv)
- [Blinded packet B](../article/expert_review/review_packet_B.csv)
- [Response template](../article/expert_review/reviewer_response_template.csv)
- [Phase 11 manifest](../validation/article/phase11_expert_review_manifest.json)
"""
)

upsert(
    "docs/NEXT_ACTIONS.md",
    "CVSS40_PHASE11_EXPERT_REVIEW_NEXT_20260713",
    f"""## CVSS v4.0 Phase 11 expert-review protocol completed

The blinded expert-review protocol contains {scenario_count} scenarios,
{TARGET_REVIEWERS} planned reviewers, and
{scenario_count * TARGET_REVIEWERS} planned assessments.

Next actions:

1. Identify and invite qualified independent reviewers.
2. Assign pseudonymous reviewer codes.
3. Distribute packet A or B without the answer key.
4. Collect locked independent responses.
5. Execute the agreement and review-effort analysis.
6. Conduct structured adjudication.
"""
)

text_files = [
    TEX,
    REVIEW / "PROTOCOL.md",
    REVIEW / "REVIEWER_INSTRUCTIONS.md",
    REVIEW / "CODEBOOK.md",
    REVIEW / "ANALYSIS_PLAN.md",
    REVIEW / "ETHICS_AND_DATA_HANDLING.md",
    DOCS / "00_Index.md",
    DOCS / "NEXT_ACTIONS.md",
    DOCS / "ARTICLE_PHASE11_EXPERT_REVIEW_PROTOCOL_CVSS40.md",
    TOOLS / "article_cvss40_phase11_expert_review_protocol.py",
    TOOLS / "validate_article_phase11_expert_review.py",
    MANIFEST,
]

for path in text_files:
    if not path.exists():
        raise FileNotFoundError(path)

    path.write_text(
        read(path).rstrip("\r\n") + "\n",
        encoding="utf-8",
        newline="\n",
    )

print("PHASE11_TEXT_NORMALIZATION_OK", flush=True)

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
    [
        "python",
        "-X",
        "utf8",
        "tools/validate_article_phase11_expert_review.py",
    ],
]

print("\nRUN_PHASE11_VALIDATION_SUITE", flush=True)

for command in validators:
    run(
        " ".join(command),
        command,
    )

run(
    "git diff --check",
    [
        "git",
        "diff",
        "--check",
    ],
)

print(
    f"PHASE11_PDF_OK pages={page_count} "
    f"size={PDF.stat().st_size}",
    flush=True,
)

print("CVSS40_PHASE11_EXPERT_REVIEW_END", flush=True)
