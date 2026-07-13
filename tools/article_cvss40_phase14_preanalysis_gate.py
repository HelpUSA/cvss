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

PHASE13_MANIFEST = (
    VALIDATION
    / "phase13_response_locking_manifest.json"
)

PHASE14_MANIFEST = (
    VALIDATION
    / "phase14_preanalysis_gate_manifest.json"
)

READINESS_TOOL = (
    TOOLS
    / "check_expert_review_preanalysis_readiness.py"
)

VALIDATOR = (
    TOOLS
    / "validate_article_phase14_preanalysis_gate.py"
)

PRIVATE_PREANALYSIS = (
    REVIEW
    / "private"
    / "preanalysis"
)

print(
    "CVSS40_PHASE14_PREANALYSIS_GATE_GENERATOR_START",
    flush=True,
)
print("CWD=" + str(ROOT), flush=True)

if not (ROOT / ".git").exists():
    raise RuntimeError(
        "Run from the repository root"
    )

required = [
    PHASE13_MANIFEST,
    REVIEW / ".gitignore",
    REVIEW / "reviewer_assignment_plan.csv",
    REVIEW / "review_packet_A.csv",
    REVIEW / "review_packet_B.csv",
    REVIEW / "adjudication_answer_key.csv",
    REVIEW
    / "adjudication_answer_key.commitment.json",
    TOOLS
    / "validate_expert_reviewer_response.py",
    TOOLS
    / "intake_and_lock_expert_reviewer_response.py",
    TOOLS
    / "validate_article_phase13_response_locking.py",
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
    existing = (
        read_text(path)
        if path.exists()
        else ""
    )

    lines = existing.splitlines()

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

for ignore_line in [
    "reviewer_responses/",
    "reviewer_packages/",
    "private/",
    "adjudication_answer_key.csv",
    "reviewer_*_responses.csv",
]:
    ensure_line(
        gitignore,
        ignore_line,
    )

PRIVATE_PREANALYSIS.mkdir(
    parents=True,
    exist_ok=True,
)

print(
    "LOCAL_DIRECTORY_READY "
    + PRIVATE_PREANALYSIS
    .relative_to(ROOT)
    .as_posix(),
    flush=True,
)

readiness_tool = r'''
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import json
import subprocess
import sys

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"
TOOLS = ROOT / "tools"

ASSIGNMENTS = (
    REVIEW
    / "reviewer_assignment_plan.csv"
)

REGISTRY = (
    REVIEW
    / "private"
    / "response_lock_registry.csv"
)

ANSWER_KEY = (
    REVIEW
    / "adjudication_answer_key.csv"
)

ANSWER_COMMITMENT = (
    REVIEW
    / "adjudication_answer_key.commitment.json"
)

RESPONSE_VALIDATOR = (
    TOOLS
    / "validate_expert_reviewer_response.py"
)

PREANALYSIS = (
    REVIEW
    / "private"
    / "preanalysis"
)

READINESS_REPORT = (
    PREANALYSIS
    / "preanalysis_readiness_report.json"
)

RELEASE_TOKEN = (
    PREANALYSIS
    / "analysis_release.json"
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


def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def resolve_repository_path(value):
    path = Path(value)

    if not path.is_absolute():
        path = ROOT / path

    return path


def write_json(path, value):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def validate_locked_response(
    reviewer_code,
    locked_file,
):
    report_path = (
        PREANALYSIS
        / (
            "revalidated_"
            + reviewer_code
            + ".json"
        )
    )

    command = [
        sys.executable,
        "-X",
        "utf8",
        str(RESPONSE_VALIDATOR),
        str(locked_file),
        "--report",
        str(report_path),
    ]

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

    return (
        completed.returncode,
        report_path,
    )


parser = argparse.ArgumentParser()

parser.add_argument(
    "--require-ready",
    action="store_true",
)

parser.add_argument(
    "--write-release",
    action="store_true",
)

arguments = parser.parse_args()

PREANALYSIS.mkdir(
    parents=True,
    exist_ok=True,
)

required_files = [
    ASSIGNMENTS,
    ANSWER_KEY,
    ANSWER_COMMITMENT,
    RESPONSE_VALIDATOR,
]

for path in required_files:
    if not path.exists():
        raise FileNotFoundError(path)

_, assignments = read_csv(
    ASSIGNMENTS
)

if len(assignments) < 3:
    raise RuntimeError(
        "At least three reviewer assignments are required"
    )

assignment_map = {}

structural_errors = []
blockers = []
locked_records = []

for row in assignments:
    reviewer_code = row.get(
        "reviewer_code",
        "",
    ).strip()

    packet_version = row.get(
        "packet_version",
        "",
    ).strip().upper()

    if not reviewer_code:
        structural_errors.append({
            "type": "missing_reviewer_code",
        })

        continue

    if reviewer_code in assignment_map:
        structural_errors.append({
            "type": "duplicate_assignment",
            "reviewer_code": reviewer_code,
        })

        continue

    assignment_map[reviewer_code] = {
        "packet_version": packet_version,
    }

registry_rows = []

if REGISTRY.exists():
    _, registry_rows = read_csv(
        REGISTRY
    )

locked_by_reviewer = {}

for row in registry_rows:
    if row.get(
        "status",
        "",
    ).strip() != "locked":
        continue

    reviewer_code = row.get(
        "reviewer_code",
        "",
    ).strip()

    if reviewer_code not in assignment_map:
        structural_errors.append({
            "type": "unassigned_locked_response",
            "reviewer_code": reviewer_code,
        })

        continue

    locked_by_reviewer.setdefault(
        reviewer_code,
        [],
    ).append(row)

for reviewer_code, assignment in sorted(
    assignment_map.items()
):
    records = locked_by_reviewer.get(
        reviewer_code,
        [],
    )

    if not records:
        blockers.append({
            "type": "missing_locked_response",
            "reviewer_code": reviewer_code,
        })

        continue

    if len(records) != 1:
        structural_errors.append({
            "type": "multiple_locked_responses",
            "reviewer_code": reviewer_code,
            "count": len(records),
        })

        continue

    record = records[0]

    registry_packet = record.get(
        "packet_version",
        "",
    ).strip().upper()

    if registry_packet != assignment[
        "packet_version"
    ]:
        structural_errors.append({
            "type": "packet_version_mismatch",
            "reviewer_code": reviewer_code,
            "expected": assignment[
                "packet_version"
            ],
            "actual": registry_packet,
        })

        continue

    response_hash = record.get(
        "response_sha256",
        "",
    ).strip()

    if not response_hash:
        structural_errors.append({
            "type": "missing_response_hash",
            "reviewer_code": reviewer_code,
        })

        continue

    locked_file = resolve_repository_path(
        record.get(
            "locked_file",
            "",
        )
    )

    original_file = resolve_repository_path(
        record.get(
            "original_file",
            "",
        )
    )

    validation_report = resolve_repository_path(
        record.get(
            "validation_report",
            "",
        )
    )

    missing_paths = [
        str(path)
        for path in [
            locked_file,
            original_file,
            validation_report,
        ]
        if not path.exists()
    ]

    if missing_paths:
        structural_errors.append({
            "type": "missing_locked_artifacts",
            "reviewer_code": reviewer_code,
            "paths": missing_paths,
        })

        continue

    locked_hash = sha256(
        locked_file
    )

    original_hash = sha256(
        original_file
    )

    if locked_hash != response_hash:
        structural_errors.append({
            "type": "locked_hash_mismatch",
            "reviewer_code": reviewer_code,
        })

        continue

    if original_hash != response_hash:
        structural_errors.append({
            "type": "original_hash_mismatch",
            "reviewer_code": reviewer_code,
        })

        continue

    report = json.loads(
        validation_report.read_text(
            encoding="utf-8",
            errors="strict",
        )
    )

    if report.get("status") != "passed":
        structural_errors.append({
            "type": "stored_validation_failed",
            "reviewer_code": reviewer_code,
        })

        continue

    if int(
        report.get(
            "row_count",
            0,
        )
    ) != 30:
        structural_errors.append({
            "type": "stored_row_count_mismatch",
            "reviewer_code": reviewer_code,
        })

        continue

    revalidation_code, revalidation_report = (
        validate_locked_response(
            reviewer_code,
            locked_file,
        )
    )

    if revalidation_code != 0:
        structural_errors.append({
            "type": "strict_revalidation_failed",
            "reviewer_code": reviewer_code,
        })

        continue

    revalidated = json.loads(
        revalidation_report.read_text(
            encoding="utf-8",
            errors="strict",
        )
    )

    if revalidated.get("status") != "passed":
        structural_errors.append({
            "type": "revalidation_report_failed",
            "reviewer_code": reviewer_code,
        })

        continue

    locked_records.append({
        "reviewer_code": reviewer_code,
        "packet_version": registry_packet,
        "response_sha256": response_hash,
        "locked_file": (
            locked_file
            .relative_to(ROOT)
            .as_posix()
        ),
        "original_file": (
            original_file
            .relative_to(ROOT)
            .as_posix()
        ),
        "validation_report": (
            validation_report
            .relative_to(ROOT)
            .as_posix()
        ),
        "revalidation_report": (
            revalidation_report
            .relative_to(ROOT)
            .as_posix()
        ),
    })

commitment = json.loads(
    ANSWER_COMMITMENT.read_text(
        encoding="utf-8-sig",
        errors="strict",
    )
)

committed_answer_hash = str(
    commitment.get(
        "sha256",
        "",
    )
).strip()

actual_answer_hash = sha256(
    ANSWER_KEY
)

answer_key_verified = (
    bool(committed_answer_hash)
    and committed_answer_hash
    == actual_answer_hash
)

if not answer_key_verified:
    structural_errors.append({
        "type": "answer_key_commitment_mismatch",
    })

required_response_count = len(
    assignment_map
)

locked_response_count = len(
    locked_records
)

ready = (
    not structural_errors
    and not blockers
    and locked_response_count
    == required_response_count
)

if ready:
    status = "ready_for_analysis"
else:
    status = "waiting_for_locked_responses"

if RELEASE_TOKEN.exists() and not ready:
    structural_errors.append({
        "type": "stale_analysis_release_token_present",
        "path": (
            RELEASE_TOKEN
            .relative_to(ROOT)
            .as_posix()
        ),
    })

    ready = False
    status = "structural_error"

if structural_errors:
    status = "structural_error"

response_set_lines = [
    (
        record["reviewer_code"]
        + ":"
        + record["response_sha256"]
    )
    for record in sorted(
        locked_records,
        key=lambda item: item[
            "reviewer_code"
        ],
    )
]

response_set_sha256 = hashlib.sha256(
    "\n".join(
        response_set_lines
    ).encode("utf-8")
).hexdigest()

generated = datetime.now(
    timezone.utc
).isoformat()

readiness_report = {
    "phase": 14,
    "generated_utc": generated,
    "status": status,
    "ready_for_analysis": ready,
    "required_response_count": (
        required_response_count
    ),
    "locked_response_count": (
        locked_response_count
    ),
    "missing_response_count": (
        required_response_count
        - locked_response_count
    ),
    "answer_key_commitment_verified": (
        answer_key_verified
    ),
    "answer_key_content_parsed": False,
    "response_set_sha256": (
        response_set_sha256
    ),
    "locked_responses": locked_records,
    "blockers": blockers,
    "structural_errors": structural_errors,
    "release_token_present": (
        RELEASE_TOKEN.exists()
    ),
}

write_json(
    READINESS_REPORT,
    readiness_report,
)

if arguments.write_release:
    if not ready:
        print(
            json.dumps(
                readiness_report,
                indent=2,
                ensure_ascii=False,
            )
        )

        raise RuntimeError(
            "Analysis release cannot be created "
            "until all readiness gates pass"
        )

    release = {
        "phase": 14,
        "generated_utc": generated,
        "status": "analysis_released",
        "required_response_count": (
            required_response_count
        ),
        "locked_response_count": (
            locked_response_count
        ),
        "reviewer_codes": sorted(
            assignment_map
        ),
        "response_set_sha256": (
            response_set_sha256
        ),
        "answer_key_sha256": (
            actual_answer_hash
        ),
        "answer_key_commitment_verified": True,
        "response_content_versioned": False,
        "release_scope": (
            "local expert-review analysis only"
        ),
    }

    write_json(
        RELEASE_TOKEN,
        release,
    )

    print(
        "CVSS40_PHASE14_ANALYSIS_RELEASE_CREATED"
    )
    print(
        "release_file="
        + RELEASE_TOKEN
        .relative_to(ROOT)
        .as_posix()
    )
    print(
        "response_set_sha256="
        + response_set_sha256
    )

print(
    "CVSS40_PHASE14_PREANALYSIS_GATE_CHECK_OK"
)
print("status=" + status)
print(
    "required_response_count="
    + str(required_response_count)
)
print(
    "locked_response_count="
    + str(locked_response_count)
)
print(
    "blocker_count="
    + str(len(blockers))
)
print(
    "structural_error_count="
    + str(len(structural_errors))
)
print(
    "answer_key_commitment_verified="
    + str(answer_key_verified)
)
print(
    "ready_for_analysis="
    + str(ready)
)
print(
    "readiness_report="
    + READINESS_REPORT
    .relative_to(ROOT)
    .as_posix()
)

if structural_errors:
    raise SystemExit(1)

if arguments.require_ready and not ready:
    raise SystemExit(2)
'''

write_text(
    READINESS_TOOL,
    readiness_tool,
)

validator = r'''
from pathlib import Path
import argparse
import json
import subprocess
import sys

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"
TOOLS = ROOT / "tools"
VALIDATION = ROOT / "validation" / "article"

MANIFEST = (
    VALIDATION
    / "phase14_preanalysis_gate_manifest.json"
)

READINESS_REPORT = (
    REVIEW
    / "private"
    / "preanalysis"
    / "preanalysis_readiness_report.json"
)

RELEASE_TOKEN = (
    REVIEW
    / "private"
    / "preanalysis"
    / "analysis_release.json"
)

REQUIRED_PUBLIC_FILES = [
    REVIEW
    / "PREANALYSIS_READINESS_RUNBOOK.md",
    TOOLS
    / "check_expert_review_preanalysis_readiness.py",
    TOOLS
    / "validate_article_phase14_preanalysis_gate.py",
    ROOT
    / "docs"
    / "ARTICLE_PHASE14_PREANALYSIS_GATE_CVSS40.md",
    MANIFEST,
]

REQUIRED_IGNORES = [
    "reviewer_responses/",
    "reviewer_packages/",
    "private/",
    "adjudication_answer_key.csv",
    "reviewer_*_responses.csv",
]

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
        "article/expert_review/private",
        "article/expert_review/reviewer_responses",
        "article/expert_review/reviewer_packages",
        "article/expert_review/"
        "adjudication_answer_key.csv",
    ],
    cwd=ROOT,
    text=True,
).strip()

if tracked_private:
    raise RuntimeError(
        "Private expert-review artifacts are tracked: "
        + tracked_private
    )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8",
        errors="strict",
    )
)

if int(manifest.get("phase", 0)) != 14:
    raise RuntimeError(
        "Unexpected Phase 14 manifest phase"
    )

if manifest.get("status") != (
    "gate-ready-awaiting-independent-responses"
):
    raise RuntimeError(
        "Unexpected Phase 14 manifest status"
    )

if int(
    manifest.get(
        "required_locked_response_count",
        0,
    )
) < 3:
    raise RuntimeError(
        "At least three locked responses "
        "must be required"
    )

if int(
    manifest.get(
        "public_locked_response_count",
        -1,
    )
) != 0:
    raise RuntimeError(
        "The public manifest must not claim "
        "locked private responses"
    )

if manifest.get(
    "response_content_versioned"
) is not False:
    raise RuntimeError(
        "Reviewer response content must remain private"
    )

if manifest.get(
    "response_hashes_versioned"
) is not False:
    raise RuntimeError(
        "Reviewer response hashes must remain private"
    )

if manifest.get(
    "release_token_versioned"
) is not False:
    raise RuntimeError(
        "The analysis release token must remain private"
    )

if manifest.get(
    "answer_key_content_versioned"
) is not False:
    raise RuntimeError(
        "The answer key must remain private"
    )

if manifest.get(
    "all_reviewers_required"
) is not True:
    raise RuntimeError(
        "The gate must require every planned reviewer"
    )

if manifest.get(
    "analysis_allowed_without_release_token"
) is not False:
    raise RuntimeError(
        "Analysis cannot be allowed without "
        "the local release token"
    )

local_status = "not_checked"
local_locked_count = 0
local_ready = False

if arguments.require_local_state:
    command = [
        sys.executable,
        "-X",
        "utf8",
        str(
            TOOLS
            / "check_expert_review_preanalysis_readiness.py"
        ),
    ]

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
            "The local pre-analysis readiness "
            "check reported a structural error"
        )

    if not READINESS_REPORT.exists():
        raise FileNotFoundError(
            READINESS_REPORT
        )

    report = json.loads(
        READINESS_REPORT.read_text(
            encoding="utf-8",
            errors="strict",
        )
    )

    local_status = report.get(
        "status",
        "",
    )

    local_locked_count = int(
        report.get(
            "locked_response_count",
            0,
        )
    )

    local_ready = (
        report.get(
            "ready_for_analysis"
        )
        is True
    )

    required_count = int(
        report.get(
            "required_response_count",
            0,
        )
    )

    if required_count < 3:
        raise RuntimeError(
            "Local readiness report requires "
            "too few responses"
        )

    if local_locked_count > required_count:
        raise RuntimeError(
            "Local locked-response count exceeds "
            "the planned reviewer count"
        )

    if local_ready:
        if local_locked_count != required_count:
            raise RuntimeError(
                "Ready status has an incomplete "
                "locked-response set"
            )

        if report.get(
            "answer_key_commitment_verified"
        ) is not True:
            raise RuntimeError(
                "Ready status lacks answer-key "
                "commitment verification"
            )

        if not RELEASE_TOKEN.exists():
            print(
                "PHASE14_READY_WITHOUT_RELEASE_TOKEN"
            )
            print(
                "Run the readiness tool with "
                "--write-release after reviewing "
                "the readiness report."
            )
    else:
        if RELEASE_TOKEN.exists():
            raise RuntimeError(
                "A release token exists while "
                "the gate is not ready"
            )

print(
    "CVSS40_PHASE14_PREANALYSIS_GATE_VALIDATION_OK"
)
print(
    "required_locked_response_count="
    + str(
        manifest[
            "required_locked_response_count"
        ]
    )
)
print(
    "public_locked_response_count=0"
)
print(
    "local_state_required="
    + str(arguments.require_local_state)
)
print(
    "local_status="
    + local_status
)
print(
    "local_locked_response_count="
    + str(local_locked_count)
)
print(
    "local_ready_for_analysis="
    + str(local_ready)
)
'''

write_text(
    VALIDATOR,
    validator,
)

runbook = """# Expert-review pre-analysis readiness gate

## Purpose

The pre-analysis gate prevents expert-review analysis and adjudication from
starting before all independent responses are valid, preserved, and
cryptographically locked.

## Gate requirements

Analysis is eligible for release only when:

1. every planned reviewer has exactly one active locked response;
2. reviewer and packet assignments match;
3. every locked response has exactly 30 scenario rows;
4. every stored validation report passed;
5. every locked response passes strict revalidation;
6. original and locked file hashes match the registry;
7. no reviewer has multiple active locked responses;
8. the response set contains every planned reviewer;
9. the local answer key matches its versioned SHA-256 commitment;
10. no structural error is present.

## Readiness check

Run:

`python -X utf8 tools/check_expert_review_preanalysis_readiness.py`

The command is expected to succeed while responses are still missing. Its
machine-readable local report identifies the missing reviewer locks.

The local report is stored at:

`article/expert_review/private/preanalysis/preanalysis_readiness_report.json`

## Strict readiness requirement

To require a complete response set, run:

`python -X utf8 tools/check_expert_review_preanalysis_readiness.py --require-ready`

This command returns a nonzero status until every gate requirement passes.

## Analysis release

After manually reviewing the complete readiness report, create the local release
token with:

`python -X utf8 tools/check_expert_review_preanalysis_readiness.py --require-ready --write-release`

The local release token is stored at:

`article/expert_review/private/preanalysis/analysis_release.json`

The token contains:

- the required and locked response counts;
- the reviewer-code set;
- a SHA-256 commitment for the complete response set;
- the verified answer-key SHA-256 value;
- the analysis release scope.

## Answer-key boundary

The readiness gate hashes the answer-key bytes to verify the existing commitment.
It does not parse the answer-key CSV or compare reviewer decisions with watcher
decisions.

Semantic answer-key access remains prohibited until the local release token is
created.

## Privacy boundary

The following remain local and ignored by Git:

- reviewer responses;
- original and locked copies;
- response validation reports;
- response hashes;
- readiness reports;
- analysis release tokens;
- reviewer registries;
- answer-key content.

## Current expected state

Before real reviewer responses are collected, the gate should report:

- status: `waiting_for_locked_responses`;
- locked response count: `0`;
- ready for analysis: `False`;
- structural error count: `0`.

This expected waiting state is not a failure.
"""

write_text(
    REVIEW
    / "PREANALYSIS_READINESS_RUNBOOK.md",
    runbook,
)

phase13 = json.loads(
    read_text(PHASE13_MANIFEST)
)

existing_manifest = {}

if PHASE14_MANIFEST.exists():
    existing_manifest = json.loads(
        read_text(PHASE14_MANIFEST)
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
    "phase": 14,
    "generated_utc": generated,
    "status": (
        "gate-ready-awaiting-independent-responses"
    ),
    "scenario_count": int(
        phase13["scenario_count"]
    ),
    "planned_reviewer_count": int(
        phase13[
            "planned_reviewer_count"
        ]
    ),
    "planned_assessment_count": int(
        phase13[
            "planned_assessment_count"
        ]
    ),
    "required_locked_response_count": int(
        phase13[
            "planned_reviewer_count"
        ]
    ),
    "public_locked_response_count": 0,
    "all_reviewers_required": True,
    "one_active_lock_per_reviewer": True,
    "strict_revalidation_required": True,
    "original_hash_verification_required": True,
    "locked_hash_verification_required": True,
    "answer_key_commitment_verification_required": True,
    "answer_key_content_parsed_by_gate": False,
    "analysis_allowed_without_release_token": False,
    "response_content_versioned": False,
    "response_hashes_versioned": False,
    "release_token_versioned": False,
    "answer_key_content_versioned": False,
    "local_only_paths": [
        "article/expert_review/reviewer_responses/",
        "article/expert_review/private/",
        "article/expert_review/adjudication_answer_key.csv",
    ],
    "public_artifacts": [
        "article/expert_review/PREANALYSIS_READINESS_RUNBOOK.md",
        "tools/check_expert_review_preanalysis_readiness.py",
        "tools/validate_article_phase14_preanalysis_gate.py",
        "docs/ARTICLE_PHASE14_PREANALYSIS_GATE_CVSS40.md",
    ],
    "claim_boundaries": [
        "No reviewer response has been collected by this phase",
        "No reviewer response has been fabricated",
        "No agreement statistic has been calculated",
        "The answer key has not been semantically opened",
        "The public manifest contains no response hashes",
        "Analysis remains blocked until all reviewer responses are locked",
        "A local analysis release token is mandatory",
    ],
}

write_json(
    PHASE14_MANIFEST,
    manifest,
)

report = f"""---
status: preanalysis-gate-ready
last_updated: 2026-07-13
tags: [cvss-v4, phase14, expert-review, readiness-gate, preanalysis]
---

# CVSS v4.0 Phase 14 pre-analysis readiness gate

Generated UTC: `{generated}`

## Result

- Gate infrastructure: ready
- Planned reviewers: {manifest["planned_reviewer_count"]}
- Required locked responses: {manifest["required_locked_response_count"]}
- Publicly declared locked responses: 0
- All planned reviewers required: yes
- Strict revalidation required: yes
- Original and locked hash verification required: yes
- Answer-key commitment verification required: yes
- Analysis release token required: yes
- Reviewer response content versioned: no
- Reviewer response hashes versioned: no
- Release token versioned: no
- Answer-key content versioned: no

## Implemented controls

- exactly one active response lock per reviewer;
- assignment and packet-version verification;
- exact original and locked SHA-256 verification;
- strict response revalidation;
- validation-report verification;
- complete reviewer-set verification;
- answer-key commitment verification without semantic comparison;
- private machine-readable readiness report;
- private response-set commitment;
- private analysis release token.

## Current boundary

No real reviewer response is claimed. Until three valid independent responses are
received and locked, the expected gate state is
`waiting_for_locked_responses`.

The analysis and adjudication stages remain blocked.
"""

write_text(
    DOCS
    / "ARTICLE_PHASE14_PREANALYSIS_GATE_CVSS40.md",
    report,
)

upsert(
    DOCS / "00_Index.md",
    "CVSS40_PHASE14_PREANALYSIS_GATE_INDEX_20260713",
    """## CVSS v4.0 Phase 14 Pre-analysis Gate

- [Phase 14 report](ARTICLE_PHASE14_PREANALYSIS_GATE_CVSS40.md)
- [Pre-analysis readiness runbook](../article/expert_review/PREANALYSIS_READINESS_RUNBOOK.md)
- [Phase 14 manifest](../validation/article/phase14_preanalysis_gate_manifest.json)
""",
)

upsert(
    DOCS / "NEXT_ACTIONS.md",
    "CVSS40_PHASE14_PREANALYSIS_GATE_NEXT_20260713",
    """## CVSS v4.0 Phase 14 pre-analysis gate ready

The analysis gate is installed and currently awaits the independent reviewer
responses.

Next actions:

1. Recruit and qualify the three planned reviewers.
2. Distribute only the assigned local reviewer packages.
3. Receive each original response CSV.
4. Validate and cryptographically lock each accepted response.
5. Run the Phase 14 readiness check after every lock.
6. Confirm that all three reviewers have exactly one valid lock.
7. Review the private readiness report.
8. Create the local analysis release token.
9. Only then begin agreement analysis and adjudication.
""",
)

commands = [
    [
        sys.executable,
        "-m",
        "py_compile",
        str(
            ROOT
            / "tools"
            / "article_cvss40_phase14_preanalysis_gate.py"
        ),
        str(READINESS_TOOL),
        str(VALIDATOR),
    ],
    [
        sys.executable,
        "-X",
        "utf8",
        str(READINESS_TOOL),
    ],
    [
        sys.executable,
        "-X",
        "utf8",
        str(
            TOOLS
            / "validate_article_phase13_response_locking.py"
        ),
        "--require-local-state",
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
    "CVSS40_PHASE14_PREANALYSIS_GATE_GENERATOR_END",
    flush=True,
)
