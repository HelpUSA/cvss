
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
