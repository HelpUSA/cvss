from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import re

ROOT = Path.cwd()
REVIEW = ROOT / "article" / "expert_review"
VALIDATION = ROOT / "validation" / "article"
DOCS = ROOT / "docs"

VISIBLE_FILES = [
    REVIEW / "blinded_scenarios_master.csv",
    REVIEW / "review_packet_A.csv",
    REVIEW / "review_packet_B.csv",
]

ANSWER_KEY = (
    REVIEW / "adjudication_answer_key.csv"
)

COMMITMENT = (
    REVIEW
    / "adjudication_answer_key.commitment.json"
)

MANIFEST = (
    VALIDATION
    / "phase11_expert_review_manifest.json"
)

AUDIT_JSON = (
    VALIDATION
    / "phase11_blinding_audit.json"
)

AUDIT_DOC = (
    DOCS
    / "ARTICLE_PHASE11_BLINDING_AUDIT_CVSS40.md"
)

for path in VISIBLE_FILES + [
    ANSWER_KEY,
    MANIFEST,
]:
    if not path.exists():
        raise FileNotFoundError(path)

def read_csv(path):
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        fields = list(reader.fieldnames or [])

    return fields, rows

def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()

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
        f"WROTE "
        f"{path.relative_to(ROOT).as_posix()} "
        f"size={path.stat().st_size}"
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

def upsert(path, marker, body):
    old = (
        path.read_text(
            encoding="utf-8-sig",
            errors="strict",
        )
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
        f"marker={marker}"
    )

identifier_pattern = re.compile(
    r"(?i)\bCVE-\d{4}-\d{4,}\b"
)

url_pattern = re.compile(
    r"(?i)\bhttps?://"
)

nvd_pattern = re.compile(
    r"(?i)nvd\.nist\.gov|services\.nvd\.nist\.gov"
)

forbidden_headers = {
    "cve_id",
    "original_scenario_id",
    "source_url",
    "official_source_url",
    "candidate_environmental_vector",
    "priority_delta",
    "recommendation_rationale",
    "watcher_recommendation",
}

visible_ids = {}
file_results = {}
issues = []

redacted_identifier_occurrences = 0
redacted_url_occurrences = 0

for path in VISIBLE_FILES:
    fields, rows = read_csv(path)

    invalid_headers = sorted(
        field
        for field in fields
        if field.lower() in forbidden_headers
    )

    if invalid_headers:
        issues.append({
            "file": path.relative_to(
                ROOT
            ).as_posix(),
            "type": "forbidden_headers",
            "values": invalid_headers,
        })

    if len(rows) != 30:
        issues.append({
            "file": path.relative_to(
                ROOT
            ).as_posix(),
            "type": "row_count",
            "expected": 30,
            "actual": len(rows),
        })

    ids = set()

    for row_number, row in enumerate(
        rows,
        2,
    ):
        review_id = row.get(
            "review_scenario_id",
            "",
        ).strip()

        if not review_id:
            issues.append({
                "file": path.relative_to(
                    ROOT
                ).as_posix(),
                "type": (
                    "missing_review_scenario_id"
                ),
                "row": row_number,
            })
        else:
            ids.add(review_id)

        for field, raw_value in row.items():
            value = str(raw_value or "")

            redacted_identifier_occurrences += (
                value.count(
                    "[redacted-vulnerability-id]"
                )
            )

            redacted_url_occurrences += (
                value.count(
                    "[redacted-source-url]"
                )
            )

            if identifier_pattern.search(value):
                issues.append({
                    "file": path.relative_to(
                        ROOT
                    ).as_posix(),
                    "type": "cve_identifier",
                    "row": row_number,
                    "field": field,
                    "value": value[:180],
                })

            if url_pattern.search(value):
                issues.append({
                    "file": path.relative_to(
                        ROOT
                    ).as_posix(),
                    "type": "source_url",
                    "row": row_number,
                    "field": field,
                    "value": value[:180],
                })

            if nvd_pattern.search(value):
                issues.append({
                    "file": path.relative_to(
                        ROOT
                    ).as_posix(),
                    "type": "nvd_reference",
                    "row": row_number,
                    "field": field,
                    "value": value[:180],
                })

    visible_ids[path.name] = ids

    file_results[
        path.relative_to(ROOT).as_posix()
    ] = {
        "row_count": len(rows),
        "field_count": len(fields),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
    }

master_ids = visible_ids[
    "blinded_scenarios_master.csv"
]

for packet_name in [
    "review_packet_A.csv",
    "review_packet_B.csv",
]:
    if visible_ids[packet_name] != master_ids:
        issues.append({
            "file": packet_name,
            "type": (
                "scenario_id_set_mismatch"
            ),
        })

answer_fields, answer_rows = read_csv(
    ANSWER_KEY
)

answer_ids = {
    row.get(
        "review_scenario_id",
        "",
    ).strip()
    for row in answer_rows
}

answer_cve_ids = [
    row.get("cve_id", "").strip()
    for row in answer_rows
    if row.get("cve_id", "").strip()
]

valid_answer_cve_ids = [
    value
    for value in answer_cve_ids
    if identifier_pattern.fullmatch(value)
]

if len(answer_rows) != 30:
    issues.append({
        "file": ANSWER_KEY.relative_to(
            ROOT
        ).as_posix(),
        "type": "answer_key_row_count",
        "expected": 30,
        "actual": len(answer_rows),
    })

if len(valid_answer_cve_ids) != 12:
    issues.append({
        "file": ANSWER_KEY.relative_to(
            ROOT
        ).as_posix(),
        "type": "protected_cve_count",
        "expected": 12,
        "actual": len(valid_answer_cve_ids),
    })

if answer_ids != master_ids:
    issues.append({
        "file": ANSWER_KEY.relative_to(
            ROOT
        ).as_posix(),
        "type": (
            "answer_key_scenario_id_mismatch"
        ),
    })

if issues:
    print(
        json.dumps(
            issues,
            indent=2,
            ensure_ascii=False,
        )
    )

    raise RuntimeError(
        "Phase 11 blinding audit found "
        f"{len(issues)} issue(s)"
    )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8-sig",
        errors="strict",
    )
)

generated = manifest.get(
    "generated_utc",
    datetime.now(timezone.utc).isoformat(),
)

answer_hash = sha256(ANSWER_KEY)

scenario_set_hash = hashlib.sha256(
    "\n".join(
        sorted(answer_ids)
    ).encode("utf-8")
).hexdigest()

commitment = {
    "phase": 11,
    "generated_utc": generated,
    "publication_status": (
        "answer-key content excluded; "
        "cryptographic commitment versioned"
    ),
    "sha256": answer_hash,
    "row_count": len(answer_rows),
    "field_count": len(answer_fields),
    "field_names": answer_fields,
    "protected_cve_identifier_count": len(
        valid_answer_cve_ids
    ),
    "scenario_id_set_sha256": (
        scenario_set_hash
    ),
}

write_json(
    COMMITMENT,
    commitment,
)

audit = {
    "phase": 11,
    "generated_utc": generated,
    "status": "passed",
    "scenario_count": len(master_ids),
    "visible_file_count": len(
        VISIBLE_FILES
    ),
    "reviewer_visible_cve_identifier_count": 0,
    "reviewer_visible_url_count": 0,
    "forbidden_header_count": 0,
    "packet_id_sets_match": True,
    "answer_key_id_set_matches": True,
    "protected_answer_key_rows": len(
        answer_rows
    ),
    "protected_cve_identifier_count": len(
        valid_answer_cve_ids
    ),
    "redacted_identifier_occurrences": (
        redacted_identifier_occurrences
    ),
    "redacted_url_occurrences": (
        redacted_url_occurrences
    ),
    "answer_key_commitment": (
        COMMITMENT
        .relative_to(ROOT)
        .as_posix()
    ),
    "protected_answer_key_sha256": (
        answer_hash
    ),
    "files": file_results,
}

write_json(
    AUDIT_JSON,
    audit,
)

manifest["blinding_audit"] = {
    "status": "passed",
    "audit_file": (
        AUDIT_JSON
        .relative_to(ROOT)
        .as_posix()
    ),
    "reviewer_visible_cve_identifier_count": 0,
    "reviewer_visible_url_count": 0,
    "protected_cve_identifier_count": len(
        valid_answer_cve_ids
    ),
    "packet_id_sets_match": True,
}

manifest["answer_key_publication"] = {
    "content_versioned": False,
    "commitment_versioned": True,
    "commitment_file": (
        COMMITMENT
        .relative_to(ROOT)
        .as_posix()
    ),
    "sha256": answer_hash,
}

write_json(
    MANIFEST,
    manifest,
)

audit_doc = f"""---
status: passed
last_updated: 2026-07-13
tags: [cvss-v4, phase11, blinding, audit]
---

# CVSS v4.0 Phase 11 blinding audit

Generated UTC: `{generated}`

## Result

- Audit status: passed
- Scenarios: {len(master_ids)}
- Reviewer-visible CVE identifiers: 0
- Reviewer-visible source URLs: 0
- Forbidden reviewer-visible headers: 0
- Protected CVE identifiers: {len(valid_answer_cve_ids)}
- Packet A and B scenario-ID sets: matched
- Protected answer-key scenario-ID set: matched

## Answer-key protection

The adjudication answer-key CSV is generated locally and excluded from Git.

The versioned commitment contains the SHA-256 value:

`{answer_hash}`

This permits later verification after independent reviewer responses are
locked.

## Interpretation boundary

The audit checks direct identifier, URL, and protected-field leakage. It does
not prove that contextual information could never permit indirect inference.
"""

write_text(
    AUDIT_DOC,
    audit_doc,
)

upsert(
    DOCS / "00_Index.md",
    "CVSS40_PHASE11_BLINDING_AUDIT_INDEX_20260713",
    """## CVSS v4.0 Phase 11 Blinding Audit

- [Blinding audit report](ARTICLE_PHASE11_BLINDING_AUDIT_CVSS40.md)
- [Machine-readable audit](../validation/article/phase11_blinding_audit.json)
- [Answer-key commitment](../article/expert_review/adjudication_answer_key.commitment.json)
"""
)

upsert(
    DOCS / "NEXT_ACTIONS.md",
    "CVSS40_PHASE11_PROTECTED_ANSWER_KEY_NEXT_20260713",
    """## CVSS v4.0 Phase 11 protected answer key

The adjudication answer key remains local and excluded from Git.

Requirements:

1. Do not distribute the answer-key CSV to reviewers.
2. Lock independent responses before opening the answer key.
3. Preserve original reviewer files before adjudication.
4. Verify the revealed key against its committed SHA-256 value.
"""
)

print("CVSS40_PHASE11_BLINDING_AUDIT_OK")
print(f"scenario_count={len(master_ids)}")
print("reviewer_visible_cve_identifiers=0")
print("reviewer_visible_urls=0")
print(
    "protected_cve_identifiers="
    + str(len(valid_answer_cve_ids))
)
print(
    "answer_key_sha256="
    + answer_hash
)
