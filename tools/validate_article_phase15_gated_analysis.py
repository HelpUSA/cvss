
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
    / "phase15_gated_analysis_manifest.json"
)

RELEASE = (
    REVIEW
    / "private"
    / "preanalysis"
    / "analysis_release.json"
)

ANALYSIS_ROOT = (
    REVIEW
    / "private"
    / "analysis"
)

REQUIRED_PUBLIC_FILES = [
    REVIEW
    / "POSTRELEASE_ANALYSIS_RUNBOOK.md",
    TOOLS
    / "run_expert_review_gated_analysis.py",
    TOOLS
    / "validate_article_phase15_gated_analysis.py",
    ROOT
    / "docs"
    / "ARTICLE_PHASE15_GATED_ANALYSIS_CVSS40.md",
    MANIFEST,
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

if int(manifest.get("phase", 0)) != 15:
    raise RuntimeError(
        "Unexpected Phase 15 manifest"
    )

if manifest.get("status") != (
    "analysis-engine-ready-awaiting-release"
):
    raise RuntimeError(
        "Unexpected Phase 15 status"
    )

if manifest.get(
    "release_token_required"
) is not True:
    raise RuntimeError(
        "Release token must be required"
    )

if manifest.get(
    "answer_key_access_before_release"
) is not False:
    raise RuntimeError(
        "Answer-key access before release "
        "must be prohibited"
    )

if manifest.get(
    "response_content_versioned"
) is not False:
    raise RuntimeError(
        "Response content must remain private"
    )

if manifest.get(
    "analysis_results_versioned"
) is not False:
    raise RuntimeError(
        "Analysis results must remain private"
    )

if int(
    manifest.get(
        "public_result_claim_count",
        -1,
    )
) != 0:
    raise RuntimeError(
        "Public result claims must remain zero"
    )

local_state = "not_checked"

if arguments.require_local_state:
    if RELEASE.exists():
        command = [
            sys.executable,
            "-X",
            "utf8",
            str(
                TOOLS
                / "run_expert_review_gated_analysis.py"
            ),
            "--validate-release",
        ]

        marker = (
            "CVSS40_PHASE15_RELEASE_VALIDATION_OK"
        )

        local_state = "released"
    else:
        command = [
            sys.executable,
            "-X",
            "utf8",
            str(
                TOOLS
                / "run_expert_review_gated_analysis.py"
            ),
            "--check-blocked",
        ]

        marker = (
            "CVSS40_PHASE15_ANALYSIS_BLOCKED_OK"
        )

        local_state = "blocked"

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
            "Phase 15 local-state validation failed"
        )

    if marker not in (
        completed.stdout or ""
    ):
        raise RuntimeError(
            "Expected Phase 15 marker was not emitted"
        )

    if not RELEASE.exists():
        forbidden_outputs = [
            ANALYSIS_ROOT
            / "expert_review_analysis.json",
            ANALYSIS_ROOT
            / "expert_review_scenario_summary.csv",
            ANALYSIS_ROOT
            / "analysis_run_manifest.json",
        ]

        existing = [
            str(path)
            for path in forbidden_outputs
            if path.exists()
        ]

        if existing:
            raise RuntimeError(
                "Analysis outputs exist without release: "
                + repr(existing)
            )

print(
    "CVSS40_PHASE15_GATED_ANALYSIS_VALIDATION_OK"
)
print("release_token_required=True")
print("public_result_claim_count=0")
print("response_content_versioned=False")
print("analysis_results_versioned=False")
print("local_state=" + local_state)
