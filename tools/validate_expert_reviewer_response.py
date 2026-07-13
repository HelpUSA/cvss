
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
