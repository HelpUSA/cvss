
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
