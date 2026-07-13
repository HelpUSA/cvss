
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
