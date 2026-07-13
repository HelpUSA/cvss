from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess
import sys

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"
VALIDATION = ROOT / "validation" / "article"

PHASE12_MANIFEST = (
    VALIDATION
    / "phase12_reviewer_operations_manifest.json"
)

PHASE13_MANIFEST = (
    VALIDATION
    / "phase13_response_locking_manifest.json"
)

INTAKE_TOOL = (
    TOOLS
    / "intake_and_lock_expert_reviewer_response.py"
)

VALIDATOR = (
    TOOLS
    / "validate_article_phase13_response_locking.py"
)

print(
    "CVSS40_PHASE13_RESPONSE_LOCKING_GENERATOR_START",
    flush=True,
)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise RuntimeError(
        "Run from the repository root"
    )

required = [
    PHASE12_MANIFEST,
    REVIEW / ".gitignore",
    REVIEW / "reviewer_assignment_plan.csv",
    REVIEW / "review_packet_A.csv",
    REVIEW / "review_packet_B.csv",
    REVIEW / "adjudication_answer_key.csv",
    REVIEW
    / "adjudication_answer_key.commitment.json",
    TOOLS / "validate_expert_reviewer_response.py",
]

for path in required:
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

    write_text(path, new)

    print(
        f"{action} "
        f"{path.relative_to(ROOT).as_posix()} "
        f"marker={marker}",
        flush=True,
    )


gitignore = REVIEW / ".gitignore"

for line in [
    "reviewer_responses/",
    "reviewer_packages/",
    "private/",
    "reviewer_*_responses.csv",
    "adjudication_answer_key.csv",
]:
    ensure_line(
        gitignore,
        line,
    )

local_directories = [
    REVIEW / "reviewer_responses",
    REVIEW / "reviewer_responses" / "incoming",
    REVIEW / "reviewer_responses" / "original",
    REVIEW / "reviewer_responses" / "locked",
    REVIEW
    / "reviewer_responses"
    / "validation_reports",
    REVIEW / "reviewer_responses" / "quarantine",
    REVIEW / "private",
]

for directory in local_directories:
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "LOCAL_DIRECTORY_READY "
        + directory.relative_to(ROOT).as_posix(),
        flush=True,
    )

intake_tool = r'''
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"
TOOLS = ROOT / "tools"

ASSIGNMENTS = (
    REVIEW / "reviewer_assignment_plan.csv"
)

VALIDATOR = (
    TOOLS / "validate_expert_reviewer_response.py"
)

RESPONSES = (
    REVIEW / "reviewer_responses"
)

INCOMING = RESPONSES / "incoming"
ORIGINAL = RESPONSES / "original"
LOCKED = RESPONSES / "locked"

REPORTS = (
    RESPONSES / "validation_reports"
)

QUARANTINE = RESPONSES / "quarantine"

REGISTRY = (
    REVIEW
    / "private"
    / "response_lock_registry.csv"
)

REGISTRY_FIELDS = [
    "reviewer_code",
    "packet_version",
    "response_sha256",
    "original_file",
    "locked_file",
    "validation_report",
    "received_utc",
    "locked_utc",
    "status",
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

        return (
            list(reader.fieldnames or []),
            list(reader),
        )


def write_csv(path, fields, rows):
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
            fieldnames=fields,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(rows)


def relative_or_absolute(path):
    try:
        return path.relative_to(
            ROOT
        ).as_posix()
    except ValueError:
        return str(path)


def ensure_local_directories():
    for directory in [
        INCOMING,
        ORIGINAL,
        LOCKED,
        REPORTS,
        QUARANTINE,
        REGISTRY.parent,
    ]:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


def load_registry():
    if not REGISTRY.exists():
        return []

    _, rows = read_csv(REGISTRY)

    return rows


def save_registry(rows):
    write_csv(
        REGISTRY,
        REGISTRY_FIELDS,
        rows,
    )


def run_response_validator(
    response_path,
    report_path,
    allow_incomplete=False,
):
    command = [
        sys.executable,
        "-X",
        "utf8",
        str(VALIDATOR),
        str(response_path),
        "--report",
        str(report_path),
    ]

    if allow_incomplete:
        command.append(
            "--allow-incomplete"
        )

    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if completed.stdout:
        print(
            completed.stdout,
            flush=True,
        )

    return completed.returncode


def determine_identity(response_path):
    fields, rows = read_csv(
        response_path
    )

    if not rows:
        raise RuntimeError(
            "The response file has no rows"
        )

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

    packet_versions = {
        row.get(
            "packet_version",
            "",
        ).strip().upper()
        for row in rows
        if row.get(
            "packet_version",
            "",
        ).strip()
    }

    if len(reviewer_codes) != 1:
        raise RuntimeError(
            "Expected exactly one reviewer code"
        )

    if len(packet_versions) != 1:
        raise RuntimeError(
            "Expected exactly one packet version"
        )

    return (
        next(iter(reviewer_codes)),
        next(iter(packet_versions)),
    )


def make_read_only(path):
    try:
        os.chmod(
            path,
            0o444,
        )
    except OSError as error:
        print(
            "READ_ONLY_WARNING "
            + str(error),
            flush=True,
        )


def self_test():
    package_root = (
        REVIEW / "reviewer_packages"
    )

    templates = sorted(
        package_root.glob(
            "R*/reviewer_R*_responses.csv"
        )
    )

    if len(templates) < 3:
        raise RuntimeError(
            "Expected at least three local "
            "reviewer templates"
        )

    for template in templates:
        temporary_report = (
            REPORTS
            / (
                "self_test_"
                + template.stem
                + ".json"
            )
        )

        code = run_response_validator(
            template,
            temporary_report,
            allow_incomplete=True,
        )

        if code != 0:
            raise RuntimeError(
                "Self-test failed for "
                + str(template)
            )

        temporary_report.unlink(
            missing_ok=True
        )

    print(
        "CVSS40_PHASE13_RESPONSE_INTAKE_SELF_TEST_OK"
    )
    print(
        "templates_tested="
        + str(len(templates))
    )


parser = argparse.ArgumentParser()

parser.add_argument(
    "response_file",
    nargs="?",
)

parser.add_argument(
    "--lock",
    action="store_true",
)

parser.add_argument(
    "--self-test",
    action="store_true",
)

arguments = parser.parse_args()

ensure_local_directories()

if arguments.self_test:
    self_test()
    raise SystemExit(0)

if not arguments.response_file:
    raise RuntimeError(
        "A response file is required"
    )

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

response_hash = sha256(
    response_path
)

reviewer_code, packet_version = (
    determine_identity(
        response_path
    )
)

report_path = (
    REPORTS
    / (
        reviewer_code
        + "__"
        + response_hash
        + ".json"
    )
)

validation_code = (
    run_response_validator(
        response_path,
        report_path,
        allow_incomplete=False,
    )
)

received_utc = (
    datetime.now(
        timezone.utc
    ).isoformat()
)

if validation_code != 0:
    quarantine_directory = (
        QUARANTINE / reviewer_code
    )

    quarantine_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    quarantine_path = (
        quarantine_directory
        / (
            response_hash
            + "__"
            + response_path.name
        )
    )

    if not quarantine_path.exists():
        shutil.copyfile(
            response_path,
            quarantine_path,
        )

    print(
        "CVSS40_PHASE13_RESPONSE_QUARANTINED"
    )
    print(
        "reviewer_code="
        + reviewer_code
    )
    print(
        "response_sha256="
        + response_hash
    )
    print(
        "quarantine_file="
        + relative_or_absolute(
            quarantine_path
        )
    )

    raise SystemExit(1)

if not arguments.lock:
    print(
        "CVSS40_PHASE13_RESPONSE_VALIDATION_OK"
    )
    print(
        "reviewer_code="
        + reviewer_code
    )
    print(
        "packet_version="
        + packet_version
    )
    print(
        "response_sha256="
        + response_hash
    )
    print(
        "validation_report="
        + relative_or_absolute(
            report_path
        )
    )

    raise SystemExit(0)

registry_rows = load_registry()

existing = next(
    (
        row
        for row in registry_rows
        if row.get(
            "reviewer_code",
            "",
        ).strip()
        == reviewer_code
        and row.get(
            "status",
            "",
        ).strip()
        == "locked"
    ),
    None,
)

if existing:
    existing_hash = existing.get(
        "response_sha256",
        "",
    ).strip()

    if existing_hash != response_hash:
        raise RuntimeError(
            "Reviewer "
            + reviewer_code
            + " already has a different "
            "locked response"
        )

    print(
        "CVSS40_PHASE13_RESPONSE_ALREADY_LOCKED"
    )
    print(
        "reviewer_code="
        + reviewer_code
    )
    print(
        "response_sha256="
        + response_hash
    )

    raise SystemExit(0)

original_directory = (
    ORIGINAL / reviewer_code
)

locked_directory = (
    LOCKED / reviewer_code
)

original_directory.mkdir(
    parents=True,
    exist_ok=True,
)

locked_directory.mkdir(
    parents=True,
    exist_ok=True,
)

original_path = (
    original_directory
    / (
        response_hash
        + "__"
        + response_path.name
    )
)

locked_path = (
    locked_directory
    / (
        response_hash
        + ".csv"
    )
)

if not original_path.exists():
    shutil.copyfile(
        response_path,
        original_path,
    )

if not locked_path.exists():
    shutil.copyfile(
        response_path,
        locked_path,
    )

if sha256(original_path) != response_hash:
    raise RuntimeError(
        "Original preserved response hash mismatch"
    )

if sha256(locked_path) != response_hash:
    raise RuntimeError(
        "Locked response hash mismatch"
    )

make_read_only(
    original_path
)

make_read_only(
    locked_path
)

locked_utc = (
    datetime.now(
        timezone.utc
    ).isoformat()
)

report = json.loads(
    report_path.read_text(
        encoding="utf-8",
        errors="strict",
    )
)

report["intake"] = {
    "received_utc": received_utc,
    "locked_utc": locked_utc,
    "response_sha256": response_hash,
    "original_file": (
        relative_or_absolute(
            original_path
        )
    ),
    "locked_file": (
        relative_or_absolute(
            locked_path
        )
    ),
    "status": "locked",
}

report_path.write_text(
    json.dumps(
        report,
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
)

registry_rows.append({
    "reviewer_code": reviewer_code,
    "packet_version": packet_version,
    "response_sha256": response_hash,
    "original_file": (
        relative_or_absolute(
            original_path
        )
    ),
    "locked_file": (
        relative_or_absolute(
            locked_path
        )
    ),
    "validation_report": (
        relative_or_absolute(
            report_path
        )
    ),
    "received_utc": received_utc,
    "locked_utc": locked_utc,
    "status": "locked",
})

save_registry(
    registry_rows
)

print(
    "CVSS40_PHASE13_RESPONSE_LOCKED_OK"
)
print(
    "reviewer_code="
    + reviewer_code
)
print(
    "packet_version="
    + packet_version
)
print(
    "response_sha256="
    + response_hash
)
print(
    "original_file="
    + relative_or_absolute(
        original_path
    )
)
print(
    "locked_file="
    + relative_or_absolute(
        locked_path
    )
)
print(
    "validation_report="
    + relative_or_absolute(
        report_path
    )
)
'''

write_text(
    INTAKE_TOOL,
    intake_tool,
)

validator = r'''
from pathlib import Path
import argparse
import csv
import hashlib
import json
import subprocess
import sys

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"
TOOLS = ROOT / "tools"
VALIDATION = ROOT / "validation" / "article"

MANIFEST = (
    VALIDATION
    / "phase13_response_locking_manifest.json"
)

REGISTRY = (
    REVIEW
    / "private"
    / "response_lock_registry.csv"
)

REQUIRED_PUBLIC_FILES = [
    REVIEW / ".gitignore",
    REVIEW / "RESPONSE_LOCKING_RUNBOOK.md",
    TOOLS
    / "intake_and_lock_expert_reviewer_response.py",
    TOOLS
    / "validate_article_phase13_response_locking.py",
    ROOT
    / "docs"
    / "ARTICLE_PHASE13_RESPONSE_LOCKING_CVSS40.md",
    MANIFEST,
]

REQUIRED_IGNORES = [
    "reviewer_responses/",
    "reviewer_packages/",
    "private/",
    "reviewer_*_responses.csv",
    "adjudication_answer_key.csv",
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
    "--require-local-state",
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
            "Missing ignore rule: "
            + required_ignore
        )

tracked_private = subprocess.check_output(
    [
        "git",
        "ls-files",
        "article/expert_review/"
        "reviewer_responses",
        "article/expert_review/private",
        "article/expert_review/"
        "adjudication_answer_key.csv",
    ],
    cwd=ROOT,
    text=True,
).strip()

if tracked_private:
    raise RuntimeError(
        "Private Phase 13 files are tracked: "
        + tracked_private
    )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8",
        errors="strict",
    )
)

if int(manifest.get("phase", 0)) != 13:
    raise RuntimeError(
        "Unexpected Phase 13 manifest phase"
    )

if manifest.get("status") != (
    "ready-no-responses-collected"
):
    raise RuntimeError(
        "Unexpected Phase 13 readiness status"
    )

if int(
    manifest.get(
        "planned_reviewer_count",
        0,
    )
) < 3:
    raise RuntimeError(
        "At least three reviewers are required"
    )

if int(
    manifest.get(
        "locked_response_count",
        -1,
    )
) != 0:
    raise RuntimeError(
        "Versioned manifest must not claim "
        "locked responses"
    )

if manifest.get(
    "answer_key_required_for_intake"
) is not False:
    raise RuntimeError(
        "Response intake must not require "
        "the answer key"
    )

if manifest.get(
    "response_content_versioned"
) is not False:
    raise RuntimeError(
        "Reviewer response content must "
        "remain unversioned"
    )

local_locked_count = 0

if arguments.require_local_state:
    local_directories = [
        REVIEW / "reviewer_responses",
        REVIEW
        / "reviewer_responses"
        / "incoming",
        REVIEW
        / "reviewer_responses"
        / "original",
        REVIEW
        / "reviewer_responses"
        / "locked",
        REVIEW
        / "reviewer_responses"
        / "validation_reports",
        REVIEW
        / "reviewer_responses"
        / "quarantine",
        REVIEW / "private",
    ]

    for directory in local_directories:
        if not directory.exists():
            raise FileNotFoundError(
                directory
            )

    answer_key = (
        REVIEW
        / "adjudication_answer_key.csv"
    )

    if not answer_key.exists():
        raise FileNotFoundError(
            answer_key
        )

    ignored = subprocess.run(
        [
            "git",
            "check-ignore",
            "-q",
            str(
                answer_key.relative_to(ROOT)
            ),
        ],
        cwd=ROOT,
    )

    if ignored.returncode != 0:
        raise RuntimeError(
            "The answer key is not ignored"
        )

    self_test = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(
                TOOLS
                / "intake_and_lock_expert_reviewer_response.py"
            ),
            "--self-test",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if self_test.stdout:
        print(
            self_test.stdout,
            flush=True,
        )

    if self_test.returncode != 0:
        raise RuntimeError(
            "Phase 13 intake self-test failed"
        )

    if REGISTRY.exists():
        registry_rows = read_csv(
            REGISTRY
        )

        locked_rows = [
            row
            for row in registry_rows
            if row.get(
                "status",
                "",
            ).strip()
            == "locked"
        ]

        local_locked_count = len(
            locked_rows
        )

        reviewer_codes = [
            row.get(
                "reviewer_code",
                "",
            ).strip()
            for row in locked_rows
        ]

        if len(reviewer_codes) != len(
            set(reviewer_codes)
        ):
            raise RuntimeError(
                "More than one active lock exists "
                "for a reviewer"
            )

        for row in locked_rows:
            response_hash = row.get(
                "response_sha256",
                "",
            ).strip()

            locked_file = (
                ROOT / row[
                    "locked_file"
                ]
            )

            original_file = (
                ROOT / row[
                    "original_file"
                ]
            )

            report_file = (
                ROOT / row[
                    "validation_report"
                ]
            )

            for path in [
                locked_file,
                original_file,
                report_file,
            ]:
                if not path.exists():
                    raise FileNotFoundError(
                        path
                    )

            if sha256(
                locked_file
            ) != response_hash:
                raise RuntimeError(
                    "Locked response hash mismatch"
                )

            if sha256(
                original_file
            ) != response_hash:
                raise RuntimeError(
                    "Original response hash mismatch"
                )

            report = json.loads(
                report_file.read_text(
                    encoding="utf-8",
                    errors="strict",
                )
            )

            if report.get("status") != "passed":
                raise RuntimeError(
                    "Locked response has a failed "
                    "validation report"
                )

print(
    "CVSS40_PHASE13_RESPONSE_LOCKING_VALIDATION_OK"
)
print(
    "planned_reviewer_count="
    + str(
        manifest[
            "planned_reviewer_count"
        ]
    )
)
print(
    "versioned_locked_response_count=0"
)
print(
    "local_locked_response_count="
    + str(local_locked_count)
)
print(
    "local_state_required="
    + str(
        arguments.require_local_state
    )
)
'''

write_text(
    VALIDATOR,
    validator,
)

runbook = """# Expert reviewer response locking runbook

## Purpose

This runbook defines how an independently completed reviewer response is
received, validated, preserved, and cryptographically locked.

The process does not require access to the adjudication answer key.

## Incoming files

Place returned files in:

`article/expert_review/reviewer_responses/incoming/`

Expected naming:

`reviewer_RXX_responses.csv`

## Validation without locking

Run:

`python -X utf8 tools/intake_and_lock_expert_reviewer_response.py <response-file>`

This validates the response but does not create an accepted lock.

## Validation and locking

After confirming that the received file is the original reviewer submission,
run:

`python -X utf8 tools/intake_and_lock_expert_reviewer_response.py <response-file> --lock`

The tool:

1. runs the strict response validator;
2. calculates the response SHA-256 value;
3. preserves an exact original copy;
4. creates a locked read-only copy;
5. preserves the machine-readable validation report;
6. records the lock in the private local registry;
7. prevents replacement by a different response for the same reviewer.

## Failed responses

Structurally invalid responses are copied to:

`article/expert_review/reviewer_responses/quarantine/`

A failed response must not be manually converted into an accepted locked
response. The reviewer should correct the original submission and return a new
file.

## Protection boundary

The following remain local and ignored by Git:

- original responses;
- locked responses;
- validation reports;
- quarantine files;
- response-lock registry;
- reviewer contact information;
- adjudication answer key.

## Before opening the answer key

Confirm that:

- every planned reviewer has one locked response;
- every locked response has a passing validation report;
- every original and locked copy has the expected SHA-256 value;
- no reviewer response was replaced;
- the answer-key commitment still matches the local answer key.

The answer key must remain unopened until all independent responses are locked.
"""

write_text(
    REVIEW / "RESPONSE_LOCKING_RUNBOOK.md",
    runbook,
)

phase12 = json.loads(
    read_text(PHASE12_MANIFEST)
)

existing_manifest = {}

if PHASE13_MANIFEST.exists():
    existing_manifest = json.loads(
        read_text(PHASE13_MANIFEST)
    )

generated = (
    existing_manifest.get(
        "generated_utc"
    )
    or datetime.now(
        timezone.utc
    ).isoformat()
)

manifest = {
    "phase": 13,
    "generated_utc": generated,
    "status": (
        "ready-no-responses-collected"
    ),
    "scenario_count": int(
        phase12["scenario_count"]
    ),
    "planned_reviewer_count": int(
        phase12["target_reviewers"]
    ),
    "planned_assessment_count": int(
        phase12["planned_assessments"]
    ),
    "locked_response_count": 0,
    "collected_response_count": 0,
    "response_content_versioned": False,
    "response_hashes_versioned": False,
    "answer_key_content_versioned": False,
    "answer_key_required_for_intake": False,
    "lock_policy": (
        "one active cryptographically locked "
        "response per reviewer"
    ),
    "local_only_paths": [
        "article/expert_review/reviewer_responses/",
        "article/expert_review/private/",
        "article/expert_review/adjudication_answer_key.csv",
    ],
    "public_artifacts": [
        "article/expert_review/RESPONSE_LOCKING_RUNBOOK.md",
        "tools/intake_and_lock_expert_reviewer_response.py",
        "tools/validate_article_phase13_response_locking.py",
        "docs/ARTICLE_PHASE13_RESPONSE_LOCKING_CVSS40.md",
    ],
    "claim_boundaries": [
        "No reviewer response has been collected",
        "No reviewer response has been locked",
        "No agreement result has been calculated",
        "The adjudication answer key remains local",
        "Response content remains unversioned",
        "The intake process does not require the answer key",
    ],
}

write_json(
    PHASE13_MANIFEST,
    manifest,
)

report = f"""---
status: response-locking-ready
last_updated: 2026-07-13
tags: [cvss-v4, phase13, expert-review, response-intake, cryptographic-lock]
---

# CVSS v4.0 Phase 13 response intake and locking

Generated UTC: `{generated}`

## Result

- Intake infrastructure: ready
- Planned reviewers: {manifest["planned_reviewer_count"]}
- Planned assessments: {manifest["planned_assessment_count"]}
- Responses collected by this phase: 0
- Responses locked by this phase: 0
- Response content versioned: no
- Answer-key content versioned: no
- Answer key required during intake: no

## Implemented controls

- strict reviewer-response validation;
- preservation of exact original response bytes;
- SHA-256 calculation;
- read-only locked response copy;
- machine-readable validation report;
- one active lock per reviewer;
- quarantine of structurally invalid responses;
- private response-lock registry;
- local-only response storage.

## Boundary

This phase prepares the operational locking workflow. It does not claim that a
reviewer has returned a response or that agreement analysis has started.
"""

write_text(
    DOCS
    / "ARTICLE_PHASE13_RESPONSE_LOCKING_CVSS40.md",
    report,
)

upsert(
    DOCS / "00_Index.md",
    "CVSS40_PHASE13_RESPONSE_LOCKING_INDEX_20260713",
    """## CVSS v4.0 Phase 13 Response Locking

- [Phase 13 report](ARTICLE_PHASE13_RESPONSE_LOCKING_CVSS40.md)
- [Response-locking runbook](../article/expert_review/RESPONSE_LOCKING_RUNBOOK.md)
- [Phase 13 manifest](../validation/article/phase13_response_locking_manifest.json)
""",
)

upsert(
    DOCS / "NEXT_ACTIONS.md",
    "CVSS40_PHASE13_RESPONSE_LOCKING_NEXT_20260713",
    """## CVSS v4.0 Phase 13 response-locking workflow ready

Next actions:

1. Recruit and qualify the independent reviewers.
2. Send each reviewer only the assigned local ZIP package.
3. Place returned CSV files in the local incoming directory.
4. Validate each response without opening the answer key.
5. Preserve and cryptographically lock accepted responses.
6. Confirm one locked response for every planned reviewer.
7. Verify all response hashes and validation reports.
8. Open the answer key only after all independent responses are locked.
""",
)

commands = [
    [
        sys.executable,
        "-m",
        "py_compile",
        str(INTAKE_TOOL),
        str(VALIDATOR),
        str(
            ROOT
            / "tools"
            / "article_cvss40_phase13_response_locking.py"
        ),
    ],
    [
        sys.executable,
        "-X",
        "utf8",
        str(INTAKE_TOOL),
        "--self-test",
    ],
    [
        sys.executable,
        "-X",
        "utf8",
        str(
            ROOT
            / "tools"
            / "validate_article_phase12_reviewer_operations.py"
        ),
        "--require-local-packages",
    ],
    [
        sys.executable,
        "-X",
        "utf8",
        str(VALIDATOR),
        "--require-local-state",
    ],
]

for command in commands:
    print(
        "\nRUN "
        + " ".join(command),
        flush=True,
    )

    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if completed.stdout:
        print(
            completed.stdout,
            flush=True,
        )

    if completed.returncode != 0:
        raise RuntimeError(
            "Command failed: "
            + " ".join(command)
            + f" rc={completed.returncode}"
        )

print(
    "CVSS40_PHASE13_RESPONSE_LOCKING_GENERATOR_END",
    flush=True,
)
