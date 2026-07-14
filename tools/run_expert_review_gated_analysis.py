
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import argparse
import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"
TOOLS = ROOT / "tools"

ASSIGNMENTS = (
    REVIEW / "reviewer_assignment_plan.csv"
)

REGISTRY = (
    REVIEW
    / "private"
    / "response_lock_registry.csv"
)

RELEASE = (
    REVIEW
    / "private"
    / "preanalysis"
    / "analysis_release.json"
)

ANSWER_KEY = (
    REVIEW / "adjudication_answer_key.csv"
)

ANSWER_COMMITMENT = (
    REVIEW
    / "adjudication_answer_key.commitment.json"
)

OUTPUT = (
    REVIEW
    / "private"
    / "analysis"
)

ANALYSIS_JSON = (
    OUTPUT
    / "expert_review_analysis.json"
)

SCENARIO_CSV = (
    OUTPUT
    / "expert_review_scenario_summary.csv"
)

RUN_MANIFEST = (
    OUTPUT
    / "analysis_run_manifest.json"
)

RESPONSE_VALIDATOR = (
    TOOLS
    / "validate_expert_reviewer_response.py"
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


def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def resolve_path(value):
    path = Path(value)

    if not path.is_absolute():
        path = ROOT / path

    return path


def norm(value):
    return " ".join(
        str(value or "").strip().split()
    )


def norm_vector(value):
    return (
        norm(value)
        .replace(" ", "")
        .upper()
    )


def norm_priority(value):
    return norm(value).lower()


def numeric(value):
    value = norm(value)

    if not value:
        return None

    try:
        result = float(value)
    except ValueError:
        return None

    if not math.isfinite(result):
        return None

    return result


def mean(values):
    values = [
        value
        for value in values
        if value is not None
    ]

    return (
        sum(values) / len(values)
        if values
        else None
    )


def median(values):
    values = [
        value
        for value in values
        if value is not None
    ]

    return (
        statistics.median(values)
        if values
        else None
    )


def majority(values):
    values = [
        value
        for value in values
        if value
    ]

    if not values:
        return ""

    counts = Counter(values)
    ranked = counts.most_common()

    if (
        len(ranked) > 1
        and ranked[0][1] == ranked[1][1]
    ):
        return ""

    return ranked[0][0]


def cohen_kappa(first, second):
    if len(first) != len(second):
        raise RuntimeError(
            "Pairwise inputs have different lengths"
        )

    if not first:
        return None

    observed = sum(
        left == right
        for left, right in zip(
            first,
            second,
        )
    ) / len(first)

    first_counts = Counter(first)
    second_counts = Counter(second)

    categories = (
        set(first_counts)
        | set(second_counts)
    )

    expected = sum(
        (
            first_counts[category]
            / len(first)
        )
        * (
            second_counts[category]
            / len(second)
        )
        for category in categories
    )

    if abs(1 - expected) < 1e-12:
        return None

    return (
        observed - expected
    ) / (
        1 - expected
    )


def fleiss_kappa(items):
    if not items:
        return None

    rater_counts = {
        len(item)
        for item in items
    }

    if len(rater_counts) != 1:
        return None

    raters = next(iter(rater_counts))

    if raters < 2:
        return None

    total_counts = Counter()
    observed_values = []

    for item in items:
        counts = Counter(item)

        total_counts.update(counts)

        observed_values.append(
            (
                sum(
                    count * count
                    for count in counts.values()
                )
                - raters
            )
            / (
                raters
                * (raters - 1)
            )
        )

    observed = (
        sum(observed_values)
        / len(observed_values)
    )

    total_ratings = (
        len(items)
        * raters
    )

    expected = sum(
        (
            count
            / total_ratings
        ) ** 2
        for count in total_counts.values()
    )

    if abs(1 - expected) < 1e-12:
        return None

    return (
        observed - expected
    ) / (
        1 - expected
    )


def field_name(fields, candidates):
    mapping = {
        field.lower(): field
        for field in fields
    }

    for candidate in candidates:
        if candidate.lower() in mapping:
            return mapping[
                candidate.lower()
            ]

    return ""


def verify_release():
    if not RELEASE.exists():
        raise RuntimeError(
            "Phase 14 analysis release token is absent"
        )

    release = json.loads(
        RELEASE.read_text(
            encoding="utf-8",
            errors="strict",
        )
    )

    if release.get("status") != (
        "analysis_released"
    ):
        raise RuntimeError(
            "Unexpected release-token status"
        )

    if release.get(
        "answer_key_commitment_verified"
    ) is not True:
        raise RuntimeError(
            "Release token does not confirm "
            "the answer-key commitment"
        )

    return release


def load_locked_responses(release):
    _, assignments = read_csv(
        ASSIGNMENTS
    )

    assignment_map = {
        row["reviewer_code"].strip():
        row["packet_version"].strip().upper()
        for row in assignments
    }

    if not REGISTRY.exists():
        raise FileNotFoundError(REGISTRY)

    _, registry_rows = read_csv(
        REGISTRY
    )

    locked_rows = [
        row
        for row in registry_rows
        if row.get(
            "status",
            "",
        ).strip() == "locked"
    ]

    by_reviewer = {}

    for row in locked_rows:
        reviewer_code = row.get(
            "reviewer_code",
            "",
        ).strip()

        by_reviewer.setdefault(
            reviewer_code,
            [],
        ).append(row)

    if set(by_reviewer) != set(
        assignment_map
    ):
        raise RuntimeError(
            "Locked reviewer set does not match "
            "the assignment plan"
        )

    verified = []

    for reviewer_code in sorted(
        assignment_map
    ):
        records = by_reviewer[
            reviewer_code
        ]

        if len(records) != 1:
            raise RuntimeError(
                "Expected exactly one locked response "
                "for "
                + reviewer_code
            )

        record = records[0]

        packet_version = record.get(
            "packet_version",
            "",
        ).strip().upper()

        if packet_version != assignment_map[
            reviewer_code
        ]:
            raise RuntimeError(
                "Packet mismatch for "
                + reviewer_code
            )

        expected_hash = record.get(
            "response_sha256",
            "",
        ).strip()

        locked_file = resolve_path(
            record["locked_file"]
        )

        original_file = resolve_path(
            record["original_file"]
        )

        report_file = resolve_path(
            record["validation_report"]
        )

        for path in [
            locked_file,
            original_file,
            report_file,
        ]:
            if not path.exists():
                raise FileNotFoundError(path)

        if sha256(locked_file) != expected_hash:
            raise RuntimeError(
                "Locked hash mismatch for "
                + reviewer_code
            )

        if sha256(original_file) != expected_hash:
            raise RuntimeError(
                "Original hash mismatch for "
                + reviewer_code
            )

        stored_report = json.loads(
            report_file.read_text(
                encoding="utf-8",
                errors="strict",
            )
        )

        if stored_report.get("status") != "passed":
            raise RuntimeError(
                "Stored validation failed for "
                + reviewer_code
            )

        OUTPUT.mkdir(
            parents=True,
            exist_ok=True,
        )

        revalidation_report = (
            OUTPUT
            / (
                "strict_revalidation_"
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
            str(revalidation_report),
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
                "Strict response revalidation failed "
                "for "
                + reviewer_code
            )

        _, rows = read_csv(
            locked_file
        )

        if len(rows) != 30:
            raise RuntimeError(
                "Unexpected response row count for "
                + reviewer_code
            )

        verified.append({
            "reviewer_code": reviewer_code,
            "packet_version": packet_version,
            "response_sha256": expected_hash,
            "locked_file": locked_file,
            "rows": rows,
        })

    response_set_lines = [
        item["reviewer_code"]
        + ":"
        + item["response_sha256"]
        for item in verified
    ]

    response_set_hash = hashlib.sha256(
        "\n".join(
            response_set_lines
        ).encode("utf-8")
    ).hexdigest()

    if response_set_hash != release.get(
        "response_set_sha256"
    ):
        raise RuntimeError(
            "Response-set commitment mismatch"
        )

    return verified, response_set_hash


def load_answer_key(release):
    answer_hash = sha256(
        ANSWER_KEY
    )

    if answer_hash != release.get(
        "answer_key_sha256"
    ):
        raise RuntimeError(
            "Answer-key hash does not match "
            "the release token"
        )

    commitment = json.loads(
        ANSWER_COMMITMENT.read_text(
            encoding="utf-8-sig",
            errors="strict",
        )
    )

    if answer_hash != commitment.get(
        "sha256"
    ):
        raise RuntimeError(
            "Answer-key hash does not match "
            "the public commitment"
        )

    fields, rows = read_csv(
        ANSWER_KEY
    )

    if len(rows) != 30:
        raise RuntimeError(
            "Answer key must contain 30 rows"
        )

    return answer_hash, fields, rows


def run_analysis():
    release = verify_release()

    responses, response_set_hash = (
        load_locked_responses(
            release
        )
    )

    answer_hash, answer_fields, answers = (
        load_answer_key(
            release
        )
    )

    scenario_field = field_name(
        answer_fields,
        [
            "review_scenario_id",
            "scenario_id",
        ],
    )

    vector_field = field_name(
        answer_fields,
        [
            "candidate_environmental_vector",
            "watcher_environmental_vector",
            "environmental_vector",
            "candidate_vector",
        ],
    )

    priority_field = field_name(
        answer_fields,
        [
            "candidate_operational_priority",
            "watcher_operational_priority",
            "operational_priority",
            "watcher_recommendation",
            "recommendation",
        ],
    )

    if not scenario_field:
        raise RuntimeError(
            "Answer key has no scenario ID field"
        )

    answer_map = {
        row[scenario_field].strip(): row
        for row in answers
    }

    reviewer_codes = [
        item["reviewer_code"]
        for item in responses
    ]

    response_maps = {
        item["reviewer_code"]: {
            row[
                "review_scenario_id"
            ].strip(): row
            for row in item["rows"]
        }
        for item in responses
    }

    expected_ids = set(
        answer_map
    )

    for reviewer_code, mapping in (
        response_maps.items()
    ):
        if set(mapping) != expected_ids:
            raise RuntimeError(
                "Scenario-set mismatch for "
                + reviewer_code
            )

    scenario_rows = []
    priority_items = []
    vector_items = []

    evidence_values = []
    confidence_values = []
    duration_values = []

    completed = 0
    deferred = 0

    vector_unanimous = 0
    priority_unanimous = 0

    watcher_vector_comparisons = 0
    watcher_vector_matches = 0

    watcher_priority_comparisons = 0
    watcher_priority_matches = 0

    for scenario_id in answer_map:
        answer = answer_map[
            scenario_id
        ]

        watcher_vector = (
            norm_vector(
                answer.get(
                    vector_field,
                    "",
                )
            )
            if vector_field
            else ""
        )

        watcher_priority = (
            norm_priority(
                answer.get(
                    priority_field,
                    "",
                )
            )
            if priority_field
            else ""
        )

        vectors = []
        priorities = []
        statuses = []

        output_row = {
            "review_scenario_id":
                scenario_id,
            "watcher_vector":
                watcher_vector,
            "watcher_priority":
                watcher_priority,
        }

        for reviewer_code in reviewer_codes:
            response = response_maps[
                reviewer_code
            ][scenario_id]

            status = norm(
                response.get(
                    "decision_status",
                    "",
                )
            )

            vector = norm_vector(
                response.get(
                    "reviewed_environmental_vector",
                    "",
                )
            )

            priority = norm_priority(
                response.get(
                    "reviewed_operational_priority",
                    "",
                )
            )

            statuses.append(status)

            if status == "complete":
                completed += 1
                vectors.append(vector)
                priorities.append(priority)

                if watcher_vector and vector:
                    watcher_vector_comparisons += 1

                    if vector == watcher_vector:
                        watcher_vector_matches += 1

                if watcher_priority and priority:
                    watcher_priority_comparisons += 1

                    if priority == watcher_priority:
                        watcher_priority_matches += 1
            else:
                deferred += 1

            evidence_values.append(
                numeric(
                    response.get(
                        "evidence_sufficiency_1_to_5",
                        "",
                    )
                )
            )

            confidence_values.append(
                numeric(
                    response.get(
                        "confidence_1_to_5",
                        "",
                    )
                )
            )

            duration_values.append(
                numeric(
                    response.get(
                        "review_duration_seconds",
                        "",
                    )
                )
            )

            output_row[
                reviewer_code
                + "_status"
            ] = status

            output_row[
                reviewer_code
                + "_vector"
            ] = vector

            output_row[
                reviewer_code
                + "_priority"
            ] = priority

        all_complete = (
            statuses
            and all(
                status == "complete"
                for status in statuses
            )
        )

        vector_agreement = (
            all_complete
            and len(vectors)
            == len(reviewer_codes)
            and len(set(vectors)) == 1
        )

        priority_agreement = (
            all_complete
            and len(priorities)
            == len(reviewer_codes)
            and len(set(priorities)) == 1
        )

        if vector_agreement:
            vector_unanimous += 1

        if priority_agreement:
            priority_unanimous += 1

        if (
            all_complete
            and len(vectors)
            == len(reviewer_codes)
        ):
            vector_items.append(vectors)

        if (
            all_complete
            and len(priorities)
            == len(reviewer_codes)
        ):
            priority_items.append(
                priorities
            )

        output_row[
            "all_reviewers_complete"
        ] = str(all_complete)

        output_row[
            "vector_unanimous"
        ] = str(vector_agreement)

        output_row[
            "priority_unanimous"
        ] = str(priority_agreement)

        output_row[
            "majority_vector"
        ] = majority(vectors)

        output_row[
            "majority_priority"
        ] = majority(priorities)

        scenario_rows.append(
            output_row
        )

    pairwise_priority = {}
    pairwise_vector = {}

    for first_index in range(
        len(reviewer_codes)
    ):
        for second_index in range(
            first_index + 1,
            len(reviewer_codes),
        ):
            first_code = reviewer_codes[
                first_index
            ]

            second_code = reviewer_codes[
                second_index
            ]

            first_priorities = []
            second_priorities = []

            first_vectors = []
            second_vectors = []

            for scenario_id in answer_map:
                first = response_maps[
                    first_code
                ][scenario_id]

                second = response_maps[
                    second_code
                ][scenario_id]

                if (
                    norm(
                        first.get(
                            "decision_status",
                            "",
                        )
                    )
                    != "complete"
                    or norm(
                        second.get(
                            "decision_status",
                            "",
                        )
                    )
                    != "complete"
                ):
                    continue

                first_priority = norm_priority(
                    first.get(
                        "reviewed_operational_priority",
                        "",
                    )
                )

                second_priority = norm_priority(
                    second.get(
                        "reviewed_operational_priority",
                        "",
                    )
                )

                first_vector = norm_vector(
                    first.get(
                        "reviewed_environmental_vector",
                        "",
                    )
                )

                second_vector = norm_vector(
                    second.get(
                        "reviewed_environmental_vector",
                        "",
                    )
                )

                if first_priority and second_priority:
                    first_priorities.append(
                        first_priority
                    )

                    second_priorities.append(
                        second_priority
                    )

                if first_vector and second_vector:
                    first_vectors.append(
                        first_vector
                    )

                    second_vectors.append(
                        second_vector
                    )

            pair = (
                first_code
                + "__"
                + second_code
            )

            pairwise_priority[pair] = {
                "comparison_count":
                    len(first_priorities),
                "cohen_kappa":
                    cohen_kappa(
                        first_priorities,
                        second_priorities,
                    ),
            }

            pairwise_vector[pair] = {
                "comparison_count":
                    len(first_vectors),
                "cohen_kappa":
                    cohen_kappa(
                        first_vectors,
                        second_vectors,
                    ),
            }

    total_assessments = (
        len(answer_map)
        * len(reviewer_codes)
    )

    generated = datetime.now(
        timezone.utc
    ).isoformat()

    analysis = {
        "phase": 15,
        "generated_utc": generated,
        "status": "completed",
        "release_token_verified": True,
        "answer_key_opened_after_release": True,
        "answer_key_sha256": answer_hash,
        "response_set_sha256":
            response_set_hash,
        "scenario_count": len(answer_map),
        "reviewer_count":
            len(reviewer_codes),
        "reviewer_codes":
            reviewer_codes,
        "planned_assessment_count":
            total_assessments,
        "completed_assessment_count":
            completed,
        "deferred_assessment_count":
            deferred,
        "completion_rate": (
            completed / total_assessments
            if total_assessments
            else None
        ),
        "defer_rate": (
            deferred / total_assessments
            if total_assessments
            else None
        ),
        "exact_vector_unanimous_count":
            vector_unanimous,
        "exact_vector_unanimous_rate": (
            vector_unanimous
            / len(answer_map)
            if answer_map
            else None
        ),
        "priority_unanimous_count":
            priority_unanimous,
        "priority_unanimous_rate": (
            priority_unanimous
            / len(answer_map)
            if answer_map
            else None
        ),
        "priority_fleiss_kappa":
            fleiss_kappa(
                priority_items
            ),
        "exact_vector_fleiss_kappa":
            fleiss_kappa(
                vector_items
            ),
        "pairwise_priority_cohen_kappa":
            pairwise_priority,
        "pairwise_vector_cohen_kappa":
            pairwise_vector,
        "watcher_vector_comparison_count":
            watcher_vector_comparisons,
        "watcher_vector_match_count":
            watcher_vector_matches,
        "watcher_vector_match_rate": (
            watcher_vector_matches
            / watcher_vector_comparisons
            if watcher_vector_comparisons
            else None
        ),
        "watcher_priority_comparison_count":
            watcher_priority_comparisons,
        "watcher_priority_match_count":
            watcher_priority_matches,
        "watcher_priority_match_rate": (
            watcher_priority_matches
            / watcher_priority_comparisons
            if watcher_priority_comparisons
            else None
        ),
        "mean_evidence_sufficiency":
            mean(evidence_values),
        "median_evidence_sufficiency":
            median(evidence_values),
        "mean_confidence":
            mean(confidence_values),
        "median_confidence":
            median(confidence_values),
        "mean_review_duration_seconds":
            mean(duration_values),
        "median_review_duration_seconds":
            median(duration_values),
        "interpretation_boundaries": [
            "Agreement does not establish correctness",
            "Statistics describe this reviewer sample only",
            "Deferred decisions reduce available comparisons",
            "Watcher agreement is not official CVSS validation",
        ],
    }

    write_json(
        ANALYSIS_JSON,
        analysis,
    )

    write_csv(
        SCENARIO_CSV,
        list(scenario_rows[0]),
        scenario_rows,
    )

    run_manifest = {
        "phase": 15,
        "generated_utc": generated,
        "status": "analysis-completed",
        "release_token_sha256":
            sha256(RELEASE),
        "answer_key_sha256":
            answer_hash,
        "response_set_sha256":
            response_set_hash,
        "analysis_json":
            ANALYSIS_JSON
            .relative_to(ROOT)
            .as_posix(),
        "analysis_json_sha256":
            sha256(ANALYSIS_JSON),
        "scenario_csv":
            SCENARIO_CSV
            .relative_to(ROOT)
            .as_posix(),
        "scenario_csv_sha256":
            sha256(SCENARIO_CSV),
        "response_content_versioned":
            False,
        "analysis_results_versioned":
            False,
    }

    write_json(
        RUN_MANIFEST,
        run_manifest,
    )

    print(
        "CVSS40_PHASE15_GATED_ANALYSIS_OK"
    )
    print(
        "scenario_count="
        + str(len(answer_map))
    )
    print(
        "reviewer_count="
        + str(len(reviewer_codes))
    )
    print(
        "completed_assessment_count="
        + str(completed)
    )
    print(
        "deferred_assessment_count="
        + str(deferred)
    )
    print(
        "analysis_json="
        + ANALYSIS_JSON
        .relative_to(ROOT)
        .as_posix()
    )


parser = argparse.ArgumentParser()

parser.add_argument(
    "--check-blocked",
    action="store_true",
)

parser.add_argument(
    "--validate-release",
    action="store_true",
)

arguments = parser.parse_args()

if arguments.check_blocked:
    if RELEASE.exists():
        print(
            "CVSS40_PHASE15_RELEASE_TOKEN_PRESENT"
        )
        print(
            "release_token_present=True"
        )
    else:
        print(
            "CVSS40_PHASE15_ANALYSIS_BLOCKED_OK"
        )
        print(
            "release_token_present=False"
        )
        print(
            "answer_key_semantically_opened=False"
        )

    raise SystemExit(0)

if arguments.validate_release:
    release = verify_release()

    verified, response_set_hash = (
        load_locked_responses(
            release
        )
    )

    answer_hash = sha256(
        ANSWER_KEY
    )

    if answer_hash != release.get(
        "answer_key_sha256"
    ):
        raise RuntimeError(
            "Answer-key hash mismatch"
        )

    print(
        "CVSS40_PHASE15_RELEASE_VALIDATION_OK"
    )
    print(
        "locked_response_count="
        + str(len(verified))
    )
    print(
        "response_set_sha256="
        + response_set_hash
    )
    print(
        "answer_key_sha256="
        + answer_hash
    )

    raise SystemExit(0)

if not RELEASE.exists():
    print(
        "CVSS40_PHASE15_ANALYSIS_BLOCKED"
    )
    print(
        "reason=analysis_release_token_absent"
    )
    print(
        "answer_key_semantically_opened=False"
    )

    raise SystemExit(2)

run_analysis()
