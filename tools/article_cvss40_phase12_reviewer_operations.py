from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import re
import shutil
import subprocess
import zipfile

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"
VALIDATION = ROOT / "validation" / "article"

ASSIGNMENTS = REVIEW / "reviewer_assignment_plan.csv"
PACKET_A = REVIEW / "review_packet_A.csv"
PACKET_B = REVIEW / "review_packet_B.csv"
BASE_RESPONSE_TEMPLATE = REVIEW / "reviewer_response_template.csv"
ANSWER_KEY = REVIEW / "adjudication_answer_key.csv"
ANSWER_COMMITMENT = (
    REVIEW
    / "adjudication_answer_key.commitment.json"
)
PHASE11_MANIFEST = (
    VALIDATION
    / "phase11_expert_review_manifest.json"
)

PHASE12_MANIFEST = (
    VALIDATION
    / "phase12_reviewer_operations_manifest.json"
)

PACKAGES_ROOT = REVIEW / "reviewer_packages"
RESPONSES_ROOT = REVIEW / "reviewer_responses"
PRIVATE_ROOT = REVIEW / "private"

print(
    "CVSS40_PHASE12_REVIEWER_OPERATIONS_GENERATOR_START",
    flush=True,
)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise RuntimeError(
        "Run the Phase 12 generator from the repository root"
    )

required_files = [
    ASSIGNMENTS,
    PACKET_A,
    PACKET_B,
    BASE_RESPONSE_TEMPLATE,
    ANSWER_KEY,
    ANSWER_COMMITMENT,
    PHASE11_MANIFEST,
    REVIEW / "PROTOCOL.md",
    REVIEW / "REVIEWER_INSTRUCTIONS.md",
    REVIEW / "CODEBOOK.md",
    REVIEW / "ANALYSIS_PLAN.md",
    REVIEW / "ETHICS_AND_DATA_HANDLING.md",
]

for path in required_files:
    if not path.exists():
        raise FileNotFoundError(path)


def read_text(path):
    return path.read_text(
        encoding="utf-8-sig",
        errors="strict",
    )


def write_text(path, content):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

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


def write_json(path, value):
    write_text(
        path,
        json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        ),
    )


def read_csv(path):
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as stream:
        reader = csv.DictReader(stream)

        return (
            list(reader.fieldnames or []),
            list(reader),
        )


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

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


def write_csv_if_missing(path, fieldnames, rows):
    if path.exists():
        print(
            "PRESERVED_LOCAL_FILE "
            + path.relative_to(ROOT).as_posix(),
            flush=True,
        )

        return

    write_csv(
        path,
        fieldnames,
        rows,
    )


def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def ensure_line(path, line):
    current = (
        read_text(path)
        if path.exists()
        else ""
    )

    lines = current.splitlines()

    if line not in lines:
        lines.append(line)
        action = "ADDED"
    else:
        action = "ALREADY_PRESENT"

    write_text(
        path,
        "\n".join(lines),
    )

    print(
        f"{action} "
        f"{path.relative_to(ROOT).as_posix()} "
        f"{line}",
        flush=True,
    )


def upsert(path, marker, body):
    old = (
        read_text(path)
        if path.exists()
        else ""
    )

    begin = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"

    block = (
        begin
        + "\n"
        + body.rstrip()
        + "\n"
        + end
        + "\n"
    )

    if begin in old and end in old:
        before = old.split(begin, 1)[0]

        after = (
            old.split(begin, 1)[1]
            .split(end, 1)[1]
        )

        new = (
            before
            + block
            + after.lstrip("\r\n")
        )

        action = "UPDATED"
    else:
        separator = (
            ""
            if not old or old.endswith("\n")
            else "\n"
        )

        new = (
            old
            + separator
            + "\n"
            + block
        )

        action = "APPENDED"

    write_text(
        path,
        new,
    )

    print(
        f"{action} "
        f"{path.relative_to(ROOT).as_posix()} "
        f"marker={marker}",
        flush=True,
    )


def deterministic_zip(source_directory, target_zip):
    fixed_timestamp = (
        2026,
        7,
        13,
        12,
        0,
        0,
    )

    target_zip.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if target_zip.exists():
        target_zip.unlink()

    with zipfile.ZipFile(
        target_zip,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        files = sorted(
            path
            for path in source_directory.rglob("*")
            if path.is_file()
        )

        for path in files:
            relative = (
                path.relative_to(source_directory)
                .as_posix()
            )

            info = zipfile.ZipInfo(
                filename=relative,
                date_time=fixed_timestamp,
            )

            info.compress_type = (
                zipfile.ZIP_DEFLATED
            )

            info.external_attr = (
                0o100644 << 16
            )

            archive.writestr(
                info,
                path.read_bytes(),
            )

    print(
        f"WROTE {target_zip.relative_to(ROOT).as_posix()} "
        f"size={target_zip.stat().st_size}",
        flush=True,
    )


def run(command):
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if completed.stdout:
        print(
            completed.stdout[-16000:],
            flush=True,
        )

    if completed.returncode != 0:
        raise RuntimeError(
            "Command failed: "
            + " ".join(command)
            + f" rc={completed.returncode}"
        )

    return completed.stdout


gitignore = REVIEW / ".gitignore"

for ignore_line in [
    "adjudication_answer_key.csv",
    "reviewer_*_responses.csv",
    "reviewer_packages/",
    "reviewer_responses/",
    "private/",
    "reviewer_contact_registry.csv",
    "reviewer_qualification_responses.csv",
    "reviewer_consent_records/",
]:
    ensure_line(
        gitignore,
        ignore_line,
    )

ignored_result = subprocess.run(
    [
        "git",
        "check-ignore",
        "-q",
        str(
            ANSWER_KEY.relative_to(ROOT)
        ),
    ],
    cwd=ROOT,
)

if ignored_result.returncode != 0:
    raise RuntimeError(
        "The local answer key is not ignored by Git"
    )

tracked_answer_key = subprocess.run(
    [
        "git",
        "ls-files",
        "--error-unmatch",
        str(
            ANSWER_KEY.relative_to(ROOT)
        ),
    ],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if tracked_answer_key.returncode == 0:
    raise RuntimeError(
        "The adjudication answer key is still tracked"
    )

commitment = json.loads(
    read_text(ANSWER_COMMITMENT)
)

answer_key_hash = sha256(
    ANSWER_KEY
)

committed_hash = str(
    commitment.get(
        "sha256",
        "",
    )
).strip()

if not committed_hash:
    raise RuntimeError(
        "The answer-key commitment has no SHA-256 value"
    )

if answer_key_hash != committed_hash:
    raise RuntimeError(
        "The local answer key does not match "
        "the committed SHA-256 value"
    )

print(
    "PHASE12_ANSWER_KEY_COMMITMENT_VERIFIED "
    + answer_key_hash,
    flush=True,
)

phase11_manifest = json.loads(
    read_text(PHASE11_MANIFEST)
)

existing_phase12_manifest = {}

if PHASE12_MANIFEST.exists():
    existing_phase12_manifest = json.loads(
        read_text(PHASE12_MANIFEST)
    )

generated = (
    existing_phase12_manifest.get(
        "generated_utc"
    )
    or datetime.now(
        timezone.utc
    ).isoformat()
)

assignment_fields, assignments = read_csv(
    ASSIGNMENTS
)

packet_a_fields, packet_a_rows = read_csv(
    PACKET_A
)

packet_b_fields, packet_b_rows = read_csv(
    PACKET_B
)

response_fields, base_response_rows = read_csv(
    BASE_RESPONSE_TEMPLATE
)

if len(assignments) < 3:
    raise RuntimeError(
        "At least three reviewer assignments are required"
    )

if len(packet_a_rows) != 30:
    raise RuntimeError(
        "Packet A must contain 30 scenarios"
    )

if len(packet_b_rows) != 30:
    raise RuntimeError(
        "Packet B must contain 30 scenarios"
    )

packet_map = {
    "A": (
        packet_a_fields,
        packet_a_rows,
    ),
    "B": (
        packet_b_fields,
        packet_b_rows,
    ),
}

required_response_fields = [
    "reviewer_code",
    "packet_version",
    "review_scenario_id",
    "review_duration_seconds",
    "evidence_sufficiency_1_to_5",
    "confidence_1_to_5",
    "reviewed_environmental_vector",
    "reviewed_operational_priority",
    "evidence_missing",
    "ambiguity_detected",
    "decision_status",
    "reviewer_comments",
]

for field in required_response_fields:
    if field not in response_fields:
        raise RuntimeError(
            "Missing response-template field: "
            + field
        )

invitation = """# Independent expert reviewer invitation template

## Subject

Invitation to participate in a blinded CVSS v4.0 Environmental assessment study

## Message

You are invited to participate as an independent reviewer in a research study
about evidence-supported CVSS v4.0 Environmental assessment.

The study examines whether specialists agree with candidate assessments produced
by an experimental human-in-the-loop workflow. Reviewers receive blinded
scenarios containing Base CVSS information and controlled consumer context.
They do not receive CVE identifiers, source URLs, watcher recommendations, or
the protected adjudication answer key.

Participation involves reviewing 30 scenarios, recording Environmental metric
decisions, evidence sufficiency, confidence, ambiguity, and review duration.

Participation is voluntary. The study does not request confidential production
data. Reviewer identity is represented by a pseudonymous code in study exports.

Before accepting, please review:

- the reviewer eligibility form;
- the participation and confidentiality agreement;
- the reviewer instructions;
- the ethics and data-handling checklist.

Please do not forward your assigned packet or discuss scenario decisions with
other reviewers before the independent-review period is closed.
"""

eligibility = """# Reviewer eligibility form

## Reviewer identification

This form should be stored privately and must not be committed to the public
repository.

- Reviewer code:
- Name:
- Email:
- Affiliation:
- Country or time zone:
- Preferred contact method:

## Experience

Record years of experience and a brief description for each applicable area.

- Vulnerability management:
- CVSS interpretation:
- Security operations:
- Patch management:
- Cybersecurity risk assessment:
- Asset or exposure management:
- Security research:
- Other relevant experience:

## Eligibility confirmation

The preferred reviewer has experience in at least two of the following:

- vulnerability management;
- CVSS interpretation;
- security operations;
- patch management;
- risk assessment;
- asset or exposure management.

## Conflict-of-interest screening

- Has the reviewer contributed directly to this project?
- Has the reviewer previously seen the answer key?
- Has the reviewer participated in scenario construction?
- Does the reviewer have another conflict that could affect independence?

## Decision

- Eligible:
- Ineligible:
- Requires principal-investigator review:
- Decision date:
- Decision rationale:
"""

agreement = """# Participation and confidentiality agreement

## Study boundaries

The participant understands that:

1. the watcher is experimental;
2. the watcher does not produce autonomous official CVSS scores;
3. the reviewer packet is blinded;
4. the packet must not be redistributed;
5. the reviewer must not search for hidden CVE identifiers;
6. independent responses must be completed before adjudication;
7. no confidential production data should be added to the response;
8. reviewer comments must not contain unnecessary personal information.

## Confidentiality

The participant agrees not to disclose:

- assigned scenario packets;
- independent scenario decisions before study closure;
- protected adjudication material;
- personal information about other reviewers.

## Data use

Pseudonymous responses may be used to calculate agreement, review effort,
confidence, evidence sufficiency, ambiguity, defer rates, and adjudication
outcomes.

Direct identifying information should remain outside the public repository.

## Participation

- Reviewer code:
- Agreement accepted:
- Acceptance date:
- Signature or approved electronic confirmation:
"""

session_checklist = """# Reviewer session checklist

## Before the session

- [ ] Confirm the reviewer code.
- [ ] Confirm the assigned packet version.
- [ ] Confirm that the answer key is unavailable.
- [ ] Confirm that no other reviewer is participating in the session.
- [ ] Open the reviewer instructions.
- [ ] Open the assigned scenario CSV.
- [ ] Open the response CSV.
- [ ] Use a device with local autosave or frequent manual saves.

## During the session

- [ ] Complete scenarios in presentation order.
- [ ] Record review duration.
- [ ] Record evidence sufficiency.
- [ ] Record confidence.
- [ ] Record missing evidence.
- [ ] Record ambiguity.
- [ ] Use a defer status when evidence is insufficient.
- [ ] Do not search for CVEs using scenario clues.
- [ ] Do not discuss decisions with other reviewers.

## Before returning the response

- [ ] Confirm that all 30 scenario IDs remain present.
- [ ] Confirm that reviewer code and packet version are consistent.
- [ ] Confirm that no personal or confidential information was added.
- [ ] Run the response-intake validator.
- [ ] Preserve the original response file.
- [ ] Return the file through the approved channel.
"""

intake_rules = """# Reviewer response intake rules

## Storage

Returned files must be placed in:

`article/expert_review/reviewer_responses/`

This directory is intentionally ignored by Git.

## File naming

Use:

`reviewer_RXX_responses.csv`

Example:

`reviewer_R01_responses.csv`

## Required structural checks

Every response file must:

- contain exactly 30 scenario rows;
- use the assigned reviewer code;
- use the assigned packet version;
- preserve the assigned presentation order;
- contain no duplicate scenario IDs;
- use evidence-sufficiency and confidence values from 1 to 5;
- use a permitted decision status;
- contain a reviewed vector and priority when status is `complete`;
- explain missing evidence or ambiguity when deferred.

## Validation command

Run:

`python -X utf8 tools/validate_expert_reviewer_response.py <response-file>`

A machine-readable report may be produced with:

`--report <report-file.json>`

## Preservation

The originally returned file must be preserved before cleaning, correcting, or
adjudicating data.
"""

collection_runbook = """# Expert-review collection runbook

## Stage 1: reviewer recruitment

1. Identify independent specialists.
2. Send the invitation template.
3. Record qualification data privately.
4. Screen conflicts of interest.
5. Assign a pseudonymous reviewer code.
6. Record agreement acceptance privately.

## Stage 2: package distribution

1. Confirm the assigned packet version.
2. Distribute only the corresponding reviewer ZIP.
3. Do not distribute the answer key.
4. Record the distribution timestamp privately.
5. Ask the reviewer to verify receipt.

## Stage 3: independent review

1. Reviewers work independently.
2. No adjudication discussion is permitted.
3. Reviewers return their response CSV.
4. Preserve the original returned file.
5. Run the response-intake validator.
6. Resolve only structural issues before locking responses.

## Stage 4: response locking

1. Calculate a SHA-256 value for each accepted response.
2. Mark the response as locked.
3. Preserve a read-only copy.
4. Record validation status and lock timestamp.
5. Confirm that all planned reviewers are complete.

## Stage 5: answer-key verification

1. Verify the local answer key against its versioned SHA-256 commitment.
2. Do not alter the answer key before verification.
3. Open the answer key only after independent responses are locked.
4. Preserve the verification output.

## Stage 6: analysis and adjudication

1. Calculate reviewer agreement.
2. Compare reviewers with the watcher candidate values.
3. Conduct structured adjudication.
4. Preserve original and adjudicated decisions.
5. Document disagreement causes.
6. Update the manuscript only after results are verified.
"""

write_text(
    REVIEW / "RECRUITMENT_INVITATION_TEMPLATE.md",
    invitation,
)

write_text(
    REVIEW / "REVIEWER_ELIGIBILITY_FORM.md",
    eligibility,
)

write_text(
    REVIEW
    / "PARTICIPATION_AND_CONFIDENTIALITY_AGREEMENT.md",
    agreement,
)

write_text(
    REVIEW / "REVIEW_SESSION_CHECKLIST.md",
    session_checklist,
)

write_text(
    REVIEW / "RESPONSE_INTAKE_RULES.md",
    intake_rules,
)

write_text(
    REVIEW / "COLLECTION_RUNBOOK.md",
    collection_runbook,
)

PRIVATE_ROOT.mkdir(
    parents=True,
    exist_ok=True,
)

RESPONSES_ROOT.mkdir(
    parents=True,
    exist_ok=True,
)

write_csv_if_missing(
    PRIVATE_ROOT / "reviewer_contact_registry.csv",
    [
        "reviewer_code",
        "name",
        "email",
        "affiliation",
        "country_or_timezone",
        "preferred_contact_method",
        "qualification_status",
        "conflict_status",
        "agreement_status",
        "invited_utc",
        "accepted_utc",
        "notes",
    ],
    [
        {
            "reviewer_code": row[
                "reviewer_code"
            ],
            "name": "",
            "email": "",
            "affiliation": "",
            "country_or_timezone": "",
            "preferred_contact_method": "",
            "qualification_status": (
                "not_reviewed"
            ),
            "conflict_status": "not_reviewed",
            "agreement_status": "not_sent",
            "invited_utc": "",
            "accepted_utc": "",
            "notes": "",
        }
        for row in assignments
    ],
)

write_csv_if_missing(
    PRIVATE_ROOT
    / "reviewer_qualification_responses.csv",
    [
        "reviewer_code",
        "vulnerability_management_years",
        "cvss_interpretation_years",
        "security_operations_years",
        "patch_management_years",
        "risk_assessment_years",
        "asset_exposure_management_years",
        "security_research_years",
        "eligible",
        "conflict_detected",
        "decision_date",
        "decision_rationale",
    ],
    [
        {
            "reviewer_code": row[
                "reviewer_code"
            ],
            "vulnerability_management_years": "",
            "cvss_interpretation_years": "",
            "security_operations_years": "",
            "patch_management_years": "",
            "risk_assessment_years": "",
            "asset_exposure_management_years": "",
            "security_research_years": "",
            "eligible": "",
            "conflict_detected": "",
            "decision_date": "",
            "decision_rationale": "",
        }
        for row in assignments
    ],
)

write_csv_if_missing(
    PRIVATE_ROOT / "collection_status.csv",
    [
        "reviewer_code",
        "packet_version",
        "package_created",
        "invitation_status",
        "qualification_status",
        "agreement_status",
        "packet_sent_utc",
        "response_received_utc",
        "response_validation_status",
        "response_sha256",
        "response_locked_utc",
        "adjudication_status",
    ],
    [
        {
            "reviewer_code": row[
                "reviewer_code"
            ],
            "packet_version": row[
                "packet_version"
            ],
            "package_created": "yes",
            "invitation_status": "not_sent",
            "qualification_status": (
                "not_reviewed"
            ),
            "agreement_status": "not_sent",
            "packet_sent_utc": "",
            "response_received_utc": "",
            "response_validation_status": (
                "not_received"
            ),
            "response_sha256": "",
            "response_locked_utc": "",
            "adjudication_status": "not_started",
        }
        for row in assignments
    ],
)

if PACKAGES_ROOT.exists():
    shutil.rmtree(
        PACKAGES_ROOT
    )

PACKAGES_ROOT.mkdir(
    parents=True,
    exist_ok=True,
)

package_records = []

for assignment in assignments:
    reviewer_code = assignment[
        "reviewer_code"
    ].strip()

    packet_version = assignment[
        "packet_version"
    ].strip().upper()

    if not re.fullmatch(
        r"R\d{2}",
        reviewer_code,
    ):
        raise RuntimeError(
            "Unexpected reviewer code: "
            + reviewer_code
        )

    if packet_version not in packet_map:
        raise RuntimeError(
            "Unexpected packet version: "
            + packet_version
        )

    packet_fields, packet_rows = packet_map[
        packet_version
    ]

    package_directory = (
        PACKAGES_ROOT
        / reviewer_code
    )

    package_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    scenarios_path = (
        package_directory
        / "scenarios.csv"
    )

    response_path = (
        package_directory
        / f"reviewer_{reviewer_code}_responses.csv"
    )

    write_csv(
        scenarios_path,
        packet_fields,
        packet_rows,
    )

    response_rows = []

    for packet_row in packet_rows:
        response_row = {
            field: ""
            for field in response_fields
        }

        response_row["reviewer_code"] = (
            reviewer_code
        )

        response_row["packet_version"] = (
            packet_version
        )

        response_row[
            "review_scenario_id"
        ] = packet_row[
            "review_scenario_id"
        ]

        response_rows.append(
            response_row
        )

    write_csv(
        response_path,
        response_fields,
        response_rows,
    )

    for source, target_name in [
        (
            REVIEW / "REVIEWER_INSTRUCTIONS.md",
            "REVIEWER_INSTRUCTIONS.md",
        ),
        (
            REVIEW / "CODEBOOK.md",
            "CODEBOOK.md",
        ),
        (
            REVIEW / "REVIEW_SESSION_CHECKLIST.md",
            "REVIEW_SESSION_CHECKLIST.md",
        ),
        (
            REVIEW
            / "PARTICIPATION_AND_CONFIDENTIALITY_AGREEMENT.md",
            "PARTICIPATION_AND_CONFIDENTIALITY_AGREEMENT.md",
        ),
    ]:
        shutil.copyfile(
            source,
            package_directory / target_name,
        )

    package_readme = f"""# Reviewer package {reviewer_code}

## Assignment

- Reviewer code: `{reviewer_code}`
- Packet version: `{packet_version}`
- Scenario count: {len(packet_rows)}

## Files

- `scenarios.csv`
- `reviewer_{reviewer_code}_responses.csv`
- `REVIEWER_INSTRUCTIONS.md`
- `CODEBOOK.md`
- `REVIEW_SESSION_CHECKLIST.md`
- `PARTICIPATION_AND_CONFIDENTIALITY_AGREEMENT.md`

## Important boundaries

- Do not search for hidden CVE identifiers.
- Do not open or request the adjudication answer key.
- Do not discuss decisions with another reviewer.
- Do not add confidential production information.
- Preserve the scenario order.
- Return only the completed response CSV.
"""

    write_text(
        package_directory / "README.md",
        package_readme,
    )

    package_manifest = {
        "phase": 12,
        "generated_utc": generated,
        "reviewer_code": reviewer_code,
        "packet_version": packet_version,
        "scenario_count": len(
            packet_rows
        ),
        "files": {},
        "boundaries": [
            "No answer key included",
            "No CVE identifiers included",
            "No source URLs included",
            "Independent review required",
        ],
    }

    for package_file in sorted(
        path
        for path in package_directory.rglob("*")
        if path.is_file()
    ):
        relative = (
            package_file
            .relative_to(package_directory)
            .as_posix()
        )

        package_manifest["files"][
            relative
        ] = {
            "sha256": sha256(
                package_file
            ),
            "size_bytes": (
                package_file.stat().st_size
            ),
        }

    write_json(
        package_directory
        / "reviewer_package_manifest.json",
        package_manifest,
    )

    zip_path = (
        PACKAGES_ROOT
        / f"{reviewer_code}_packet_{packet_version}.zip"
    )

    deterministic_zip(
        package_directory,
        zip_path,
    )

    package_records.append({
        "reviewer_code": reviewer_code,
        "packet_version": packet_version,
        "scenario_count": len(
            packet_rows
        ),
        "directory": (
            package_directory
            .relative_to(ROOT)
            .as_posix()
        ),
        "zip_file": (
            zip_path
            .relative_to(ROOT)
            .as_posix()
        ),
        "zip_sha256": sha256(
            zip_path
        ),
        "zip_size_bytes": (
            zip_path.stat().st_size
        ),
        "scenarios_sha256": sha256(
            scenarios_path
        ),
        "response_template_sha256": sha256(
            response_path
        ),
    })

intake_validator = r'''
from pathlib import Path
from datetime import datetime
import argparse
import csv
import json
import re
import sys

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"

ASSIGNMENTS = (
    REVIEW / "reviewer_assignment_plan.csv"
)

PACKETS = {
    "A": REVIEW / "review_packet_A.csv",
    "B": REVIEW / "review_packet_B.csv",
}

REQUIRED_FIELDS = [
    "reviewer_code",
    "packet_version",
    "review_scenario_id",
    "review_duration_seconds",
    "evidence_sufficiency_1_to_5",
    "confidence_1_to_5",
    "reviewed_environmental_vector",
    "reviewed_operational_priority",
    "evidence_missing",
    "ambiguity_detected",
    "decision_status",
    "reviewer_comments",
]

DECISION_STATUSES = {
    "complete",
    "defer_missing_evidence",
    "defer_ambiguity",
    "not_assessable",
}


def read_csv(path):
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as stream:
        reader = csv.DictReader(stream)

        return (
            list(reader.fieldnames or []),
            list(reader),
        )


def validate_rating(
    value,
    field,
    row_number,
    issues,
):
    value = value.strip()

    if not value:
        return

    if value not in {
        "1",
        "2",
        "3",
        "4",
        "5",
    }:
        issues.append({
            "row": row_number,
            "field": field,
            "issue": "expected integer from 1 to 5",
            "value": value,
        })


def validate_duration(
    value,
    row_number,
    issues,
):
    value = value.strip()

    if not value:
        return

    try:
        duration = float(value)
    except ValueError:
        issues.append({
            "row": row_number,
            "field": "review_duration_seconds",
            "issue": "not numeric",
            "value": value,
        })

        return

    if duration < 0:
        issues.append({
            "row": row_number,
            "field": "review_duration_seconds",
            "issue": "negative duration",
            "value": value,
        })


def validate_timestamp(
    value,
    field,
    row_number,
    issues,
):
    value = value.strip()

    if not value:
        return

    candidate = value.replace(
        "Z",
        "+00:00",
    )

    try:
        datetime.fromisoformat(
            candidate
        )
    except ValueError:
        issues.append({
            "row": row_number,
            "field": field,
            "issue": "invalid ISO 8601 timestamp",
            "value": value,
        })


parser = argparse.ArgumentParser()

parser.add_argument(
    "response_file",
)

parser.add_argument(
    "--report",
)

parser.add_argument(
    "--allow-incomplete",
    action="store_true",
)

arguments = parser.parse_args()

response_path = Path(
    arguments.response_file
)

if not response_path.is_absolute():
    response_path = (
        ROOT / response_path
    )

if not response_path.exists():
    raise FileNotFoundError(
        response_path
    )

assignment_fields, assignments = read_csv(
    ASSIGNMENTS
)

fields, rows = read_csv(
    response_path
)

issues = []

for required in REQUIRED_FIELDS:
    if required not in fields:
        issues.append({
            "field": required,
            "issue": "missing required column",
        })

if len(rows) != 30:
    issues.append({
        "issue": "unexpected row count",
        "expected": 30,
        "actual": len(rows),
    })

reviewer_codes = {
    row.get(
        "reviewer_code",
        "",
    ).strip()
    for row in rows
    if row.get(
        "reviewer_code",
        "",
    ).strip()
}

if len(reviewer_codes) != 1:
    issues.append({
        "issue": (
            "response must contain exactly "
            "one reviewer code"
        ),
        "values": sorted(
            reviewer_codes
        ),
    })

reviewer_code = (
    next(iter(reviewer_codes))
    if len(reviewer_codes) == 1
    else ""
)

assignment = next(
    (
        row
        for row in assignments
        if row.get(
            "reviewer_code",
            "",
        ).strip()
        == reviewer_code
    ),
    None,
)

if reviewer_code and assignment is None:
    issues.append({
        "issue": "reviewer code is not assigned",
        "value": reviewer_code,
    })

packet_version = ""

if assignment:
    packet_version = assignment.get(
        "packet_version",
        "",
    ).strip().upper()

    if packet_version not in PACKETS:
        issues.append({
            "issue": "invalid assigned packet version",
            "value": packet_version,
        })

expected_ids = []

if packet_version in PACKETS:
    _, packet_rows = read_csv(
        PACKETS[packet_version]
    )

    expected_ids = [
        row.get(
            "review_scenario_id",
            "",
        ).strip()
        for row in packet_rows
    ]

actual_ids = [
    row.get(
        "review_scenario_id",
        "",
    ).strip()
    for row in rows
]

if expected_ids and actual_ids != expected_ids:
    issues.append({
        "issue": (
            "scenario identifiers or order "
            "do not match assigned packet"
        ),
    })

if len(set(actual_ids)) != len(actual_ids):
    issues.append({
        "issue": "duplicate scenario identifiers",
    })

completed_count = 0
deferred_count = 0
incomplete_count = 0

for row_number, row in enumerate(
    rows,
    2,
):
    row_reviewer = row.get(
        "reviewer_code",
        "",
    ).strip()

    row_packet = row.get(
        "packet_version",
        "",
    ).strip().upper()

    if reviewer_code and row_reviewer != reviewer_code:
        issues.append({
            "row": row_number,
            "field": "reviewer_code",
            "issue": "inconsistent reviewer code",
            "value": row_reviewer,
        })

    if packet_version and row_packet != packet_version:
        issues.append({
            "row": row_number,
            "field": "packet_version",
            "issue": "incorrect packet version",
            "value": row_packet,
        })

    validate_rating(
        row.get(
            "evidence_sufficiency_1_to_5",
            "",
        ),
        "evidence_sufficiency_1_to_5",
        row_number,
        issues,
    )

    validate_rating(
        row.get(
            "confidence_1_to_5",
            "",
        ),
        "confidence_1_to_5",
        row_number,
        issues,
    )

    validate_duration(
        row.get(
            "review_duration_seconds",
            "",
        ),
        row_number,
        issues,
    )

    validate_timestamp(
        row.get(
            "review_started_utc",
            "",
        ),
        "review_started_utc",
        row_number,
        issues,
    )

    validate_timestamp(
        row.get(
            "review_completed_utc",
            "",
        ),
        "review_completed_utc",
        row_number,
        issues,
    )

    status = row.get(
        "decision_status",
        "",
    ).strip()

    if not status:
        incomplete_count += 1

        if not arguments.allow_incomplete:
            issues.append({
                "row": row_number,
                "field": "decision_status",
                "issue": "decision status is empty",
            })

        continue

    if status not in DECISION_STATUSES:
        issues.append({
            "row": row_number,
            "field": "decision_status",
            "issue": "invalid decision status",
            "value": status,
        })

        continue

    if status == "complete":
        completed_count += 1

        vector = row.get(
            "reviewed_environmental_vector",
            "",
        ).strip()

        priority = row.get(
            "reviewed_operational_priority",
            "",
        ).strip()

        if not vector:
            issues.append({
                "row": row_number,
                "field": (
                    "reviewed_environmental_vector"
                ),
                "issue": (
                    "required when status is complete"
                ),
            })

        if not priority:
            issues.append({
                "row": row_number,
                "field": (
                    "reviewed_operational_priority"
                ),
                "issue": (
                    "required when status is complete"
                ),
            })
    else:
        deferred_count += 1

        explanation = " ".join([
            row.get(
                "evidence_missing",
                "",
            ).strip(),
            row.get(
                "ambiguity_detected",
                "",
            ).strip(),
            row.get(
                "reviewer_comments",
                "",
            ).strip(),
        ]).strip()

        if not explanation:
            issues.append({
                "row": row_number,
                "issue": (
                    "deferred decisions require "
                    "an explanation"
                ),
            })

summary = {
    "response_file": (
        response_path
        .relative_to(ROOT)
        .as_posix()
        if response_path.is_relative_to(ROOT)
        else str(response_path)
    ),
    "reviewer_code": reviewer_code,
    "packet_version": packet_version,
    "row_count": len(rows),
    "completed_count": completed_count,
    "deferred_count": deferred_count,
    "incomplete_count": incomplete_count,
    "issue_count": len(issues),
    "status": (
        "passed"
        if not issues
        else "failed"
    ),
    "issues": issues,
}

if arguments.report:
    report_path = Path(
        arguments.report
    )

    if not report_path.is_absolute():
        report_path = (
            ROOT / report_path
        )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

if issues:
    print(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
        )
    )

    sys.exit(1)

print("CVSS40_REVIEWER_RESPONSE_VALIDATION_OK")
print("reviewer_code=" + reviewer_code)
print("packet_version=" + packet_version)
print("row_count=" + str(len(rows)))
print("completed_count=" + str(completed_count))
print("deferred_count=" + str(deferred_count))
print("incomplete_count=" + str(incomplete_count))
'''

write_text(
    TOOLS / "validate_expert_reviewer_response.py",
    intake_validator,
)

validator = r'''
from pathlib import Path
import argparse
import csv
import hashlib
import json
import subprocess

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"
VALIDATION = ROOT / "validation" / "article"
TOOLS = ROOT / "tools"

MANIFEST = (
    VALIDATION
    / "phase12_reviewer_operations_manifest.json"
)

REQUIRED_PUBLIC_FILES = [
    REVIEW / ".gitignore",
    REVIEW / "RECRUITMENT_INVITATION_TEMPLATE.md",
    REVIEW / "REVIEWER_ELIGIBILITY_FORM.md",
    REVIEW
    / "PARTICIPATION_AND_CONFIDENTIALITY_AGREEMENT.md",
    REVIEW / "REVIEW_SESSION_CHECKLIST.md",
    REVIEW / "RESPONSE_INTAKE_RULES.md",
    REVIEW / "COLLECTION_RUNBOOK.md",
    TOOLS / "validate_expert_reviewer_response.py",
    ROOT
    / "docs"
    / "ARTICLE_PHASE12_REVIEWER_OPERATIONS_CVSS40.md",
    MANIFEST,
]

REQUIRED_IGNORES = [
    "adjudication_answer_key.csv",
    "reviewer_*_responses.csv",
    "reviewer_packages/",
    "reviewer_responses/",
    "private/",
    "reviewer_contact_registry.csv",
    "reviewer_qualification_responses.csv",
    "reviewer_consent_records/",
]


def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def read_csv(path):
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as stream:
        reader = csv.DictReader(stream)

        return list(reader)


parser = argparse.ArgumentParser()

parser.add_argument(
    "--require-local-packages",
    action="store_true",
)

arguments = parser.parse_args()

for path in REQUIRED_PUBLIC_FILES:
    if not path.exists():
        raise FileNotFoundError(path)

gitignore_lines = (
    REVIEW / ".gitignore"
).read_text(
    encoding="utf-8-sig",
    errors="strict",
).splitlines()

for required_ignore in REQUIRED_IGNORES:
    if required_ignore not in gitignore_lines:
        raise RuntimeError(
            "Missing expert-review ignore rule: "
            + required_ignore
        )

tracked_answer_key = subprocess.run(
    [
        "git",
        "ls-files",
        "--error-unmatch",
        "article/expert_review/"
        "adjudication_answer_key.csv",
    ],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if tracked_answer_key.returncode == 0:
    raise RuntimeError(
        "The adjudication answer key is tracked"
    )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8",
        errors="strict",
    )
)

if int(manifest.get("phase", 0)) != 12:
    raise RuntimeError(
        "Unexpected manifest phase"
    )

if int(manifest.get("scenario_count", 0)) != 30:
    raise RuntimeError(
        "Phase 12 must contain 30 scenarios"
    )

if int(manifest.get("target_reviewers", 0)) < 3:
    raise RuntimeError(
        "Phase 12 must contain at least three reviewers"
    )

if int(manifest.get("package_count", 0)) < 3:
    raise RuntimeError(
        "Phase 12 must generate at least three packages"
    )

if manifest.get(
    "answer_key_commitment_verified"
) is not True:
    raise RuntimeError(
        "The answer-key commitment was not verified"
    )

if manifest.get(
    "answer_key_content_versioned"
) is not False:
    raise RuntimeError(
        "The answer-key content must not be versioned"
    )

packages = manifest.get(
    "packages",
    []
)

if len(packages) < 3:
    raise RuntimeError(
        "The package manifest is incomplete"
    )

reviewer_codes = {
    item.get("reviewer_code")
    for item in packages
}

if len(reviewer_codes) != len(packages):
    raise RuntimeError(
        "Duplicate reviewer package code"
    )

for package in packages:
    if int(
        package.get(
            "scenario_count",
            0,
        )
    ) != 30:
        raise RuntimeError(
            "Reviewer package scenario count mismatch"
        )

if arguments.require_local_packages:
    for package in packages:
        directory = (
            ROOT / package["directory"]
        )

        zip_path = (
            ROOT / package["zip_file"]
        )

        if not directory.exists():
            raise FileNotFoundError(directory)

        if not zip_path.exists():
            raise FileNotFoundError(zip_path)

        if sha256(zip_path) != package["zip_sha256"]:
            raise RuntimeError(
                "Reviewer ZIP hash mismatch: "
                + str(zip_path)
            )

        scenario_file = (
            directory / "scenarios.csv"
        )

        response_file = (
            directory
            / (
                "reviewer_"
                + package["reviewer_code"]
                + "_responses.csv"
            )
        )

        if not scenario_file.exists():
            raise FileNotFoundError(
                scenario_file
            )

        if not response_file.exists():
            raise FileNotFoundError(
                response_file
            )

        rows = read_csv(
            scenario_file
        )

        if len(rows) != 30:
            raise RuntimeError(
                "Local package row-count mismatch"
            )

    for local_private in [
        REVIEW
        / "private"
        / "reviewer_contact_registry.csv",
        REVIEW
        / "private"
        / "reviewer_qualification_responses.csv",
        REVIEW
        / "private"
        / "collection_status.csv",
    ]:
        if not local_private.exists():
            raise FileNotFoundError(
                local_private
            )

print("CVSS40_PHASE12_REVIEWER_OPERATIONS_VALIDATION_OK")
print("scenario_count=" + str(manifest["scenario_count"]))
print("target_reviewers=" + str(manifest["target_reviewers"]))
print("package_count=" + str(manifest["package_count"]))
print(
    "answer_key_commitment_verified="
    + str(manifest["answer_key_commitment_verified"])
)
print(
    "local_packages_required="
    + str(arguments.require_local_packages)
)
'''

write_text(
    TOOLS
    / "validate_article_phase12_reviewer_operations.py",
    validator,
)

manifest = {
    "phase": 12,
    "generated_utc": generated,
    "scenario_count": int(
        phase11_manifest[
            "scenario_count"
        ]
    ),
    "target_reviewers": int(
        phase11_manifest[
            "target_reviewers"
        ]
    ),
    "planned_assessments": int(
        phase11_manifest[
            "planned_assessments"
        ]
    ),
    "package_count": len(
        package_records
    ),
    "packages": package_records,
    "answer_key_commitment_verified": True,
    "answer_key_sha256": answer_key_hash,
    "answer_key_content_versioned": False,
    "answer_key_commitment_versioned": True,
    "local_only_paths": [
        "article/expert_review/reviewer_packages/",
        "article/expert_review/reviewer_responses/",
        "article/expert_review/private/",
        "article/expert_review/adjudication_answer_key.csv",
    ],
    "public_operational_artifacts": [
        "article/expert_review/RECRUITMENT_INVITATION_TEMPLATE.md",
        "article/expert_review/REVIEWER_ELIGIBILITY_FORM.md",
        "article/expert_review/PARTICIPATION_AND_CONFIDENTIALITY_AGREEMENT.md",
        "article/expert_review/REVIEW_SESSION_CHECKLIST.md",
        "article/expert_review/RESPONSE_INTAKE_RULES.md",
        "article/expert_review/COLLECTION_RUNBOOK.md",
        "tools/validate_expert_reviewer_response.py",
        "tools/validate_article_phase12_reviewer_operations.py",
    ],
    "claim_boundaries": [
        "No reviewer has been recruited by this generation step",
        "No reviewer response has been collected",
        "Reviewer contact information remains local",
        "Reviewer responses remain local",
        "The adjudication answer key remains local",
        "Only the answer-key commitment is versioned",
        "Package generation does not establish reviewer independence",
    ],
}

write_json(
    PHASE12_MANIFEST,
    manifest,
)

report = f"""---
status: operational-package-ready
last_updated: 2026-07-13
tags: [cvss-v4, phase12, expert-review, recruitment, collection]
---

# CVSS v4.0 Phase 12 reviewer operations

Generated UTC: `{generated}`

## Result

- Operational package status: ready
- Scenarios per reviewer: {manifest["scenario_count"]}
- Planned reviewers: {manifest["target_reviewers"]}
- Planned assessments: {manifest["planned_assessments"]}
- Local reviewer packages generated: {manifest["package_count"]}
- Packet versions: A and B
- Answer-key commitment verified: yes
- Answer-key content versioned: no
- Reviewer contact data versioned: no
- Reviewer response data versioned: no

## Public artifacts

- recruitment invitation template;
- reviewer eligibility form;
- participation and confidentiality agreement;
- reviewer session checklist;
- response-intake rules;
- collection runbook;
- response-file validator;
- Phase 12 operational validator;
- reproducibility manifest.

## Local-only artifacts

- one package per pseudonymous reviewer;
- deterministic reviewer ZIP files;
- contact registry;
- qualification-response registry;
- collection-status registry;
- returned reviewer responses;
- protected adjudication answer key.

## Answer-key verification

The locally generated answer key matched the previously committed SHA-256 value:

`{answer_key_hash}`

## Boundary

This phase prepares recruitment and collection operations. It does not claim
that reviewers were recruited, responses were collected, or agreement results
were obtained.
"""

write_text(
    DOCS
    / "ARTICLE_PHASE12_REVIEWER_OPERATIONS_CVSS40.md",
    report,
)

upsert(
    DOCS / "00_Index.md",
    "CVSS40_PHASE12_REVIEWER_OPERATIONS_INDEX_20260713",
    """## CVSS v4.0 Phase 12 Reviewer Operations

- [Phase 12 report](ARTICLE_PHASE12_REVIEWER_OPERATIONS_CVSS40.md)
- [Recruitment invitation](../article/expert_review/RECRUITMENT_INVITATION_TEMPLATE.md)
- [Reviewer eligibility form](../article/expert_review/REVIEWER_ELIGIBILITY_FORM.md)
- [Participation agreement](../article/expert_review/PARTICIPATION_AND_CONFIDENTIALITY_AGREEMENT.md)
- [Reviewer session checklist](../article/expert_review/REVIEW_SESSION_CHECKLIST.md)
- [Response-intake rules](../article/expert_review/RESPONSE_INTAKE_RULES.md)
- [Collection runbook](../article/expert_review/COLLECTION_RUNBOOK.md)
- [Phase 12 manifest](../validation/article/phase12_reviewer_operations_manifest.json)
""",
)

upsert(
    DOCS / "NEXT_ACTIONS.md",
    "CVSS40_PHASE12_REVIEWER_OPERATIONS_NEXT_20260713",
    f"""## CVSS v4.0 Phase 12 reviewer operations completed

The local operational package contains {manifest["package_count"]} reviewer
kits for {manifest["scenario_count"]} scenarios each.

Next actions:

1. Identify qualified independent reviewers.
2. Complete private qualification and conflict screening.
3. Record participation agreement acceptance.
4. Send only the assigned reviewer ZIP.
5. Collect and preserve original response CSV files.
6. Validate and cryptographically lock accepted responses.
7. Verify all responses are locked before opening the answer key.
8. Execute agreement analysis and structured adjudication.
""",
)

print(
    "VALIDATE_GENERATED_REVIEWER_TEMPLATES",
    flush=True,
)

for package in package_records:
    response_file = (
        ROOT
        / package["directory"]
        / (
            "reviewer_"
            + package["reviewer_code"]
            + "_responses.csv"
        )
    )

    run([
        "python",
        "-X",
        "utf8",
        "tools/validate_expert_reviewer_response.py",
        str(
            response_file.relative_to(ROOT)
        ),
        "--allow-incomplete",
    ])

print(
    "CVSS40_PHASE12_REVIEWER_OPERATIONS_GENERATOR_END",
    flush=True,
)
