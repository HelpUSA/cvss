
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
