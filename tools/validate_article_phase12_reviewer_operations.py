
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
