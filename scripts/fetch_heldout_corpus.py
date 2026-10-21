#!/usr/bin/env python3
"""
Held-out corpus acquisition, verification and lock tool for R6-A1.
Strictly adheres to validation/article/r6_a1_heldout_corpus_protocol.md.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# 1. Path Portability (Relative to repository root)
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "validation" / "article" / "r6_heldout"
REGISTRY_PATH = REPO_ROOT / "validation" / "article" / "r6_a1_experiment_registry.json"

# 2. Frozen Protocol Constants
PRIMARY_ENDPOINT = "https://api.github.com/advisories"
WINDOW_START = "2026-09-01T00:00:00Z"
WINDOW_END = "2026-10-01T00:00:00Z"
PER_PAGE = 100
QUERY_PARAMS = {
    "type": "reviewed",
    "published": f"{WINDOW_START}..{WINDOW_END}",
    "per_page": PER_PAGE
}

# Frozen Parent Commit from Preregistration Lock
PREREGISTRATION_PARENT_COMMIT = "106049618eff5e2f2a34aa591475c4a042bdba37"

# Expected Frozen Hashes (Post-Lock Ground Truth)
FROZEN_HASHES = {
    "acquisition_metadata.json": "0821b7cc11a6c3e967fad38e0607140fd2f90a3ecbd3f6dbd1011ebbc5f756b4",
    "eligible_corpus_manifest.json": "b09a8cc45147f25073103c005d87b4244ea9e03a8233b7059fbd310cc13a22cf",
    "inclusion_exclusion_ledger.json": "171c89aa26404da7728d10ccc69b7eea6bb2b271ad9df50cb569e0ff8040c69c",
    "raw_source_snapshot.json": "eb0d5e80dfd6827896aa87315f1f9fd63748f243ae831185c068cf4c35641df2"
}

# Known R5 Baseline Identifiers (for zero-overlap matching strictly by identity/alias)
R5_CVES = {
    "CVE-2026-28490", "CVE-2026-28498", "CVE-2026-29510", "CVE-2026-29513",
    "CVE-2026-29520", "CVE-2026-29521", "CVE-2026-3644", "CVE-2026-4224",
    "CVE-2026-4251", "CVE-2026-4252", "CVE-2026-4253", "CVE-2026-4270"
}


def get_auth_token():
    """Retrieve optional API token from environment variable or gh CLI without logging secrets."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token.strip()
    try:
        gh_token = os.popen("gh auth token").read().strip()
        if gh_token and gh_token.startswith("gh"):
            return gh_token
    except Exception:
        pass
    return None


def fetch_raw_candidates():
    """Execute cursor-based pagination over official GitHub Advisory Database endpoint."""
    token = get_auth_token()
    headers = {
        "User-Agent": "HelpUS-Scientific-Validation-R6",
        "Accept": "application/vnd.github+json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    base_query = (
        f"{PRIMARY_ENDPOINT}?"
        f"type={QUERY_PARAMS['type']}&"
        f"published={QUERY_PARAMS['published']}&"
        f"per_page={QUERY_PARAMS['per_page']}"
    )
    url = base_query

    raw_records = []
    page = 1

    print(f"Starting acquisition from {url}...")
    while url:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_records.extend(data)
            print(f"Page {page}: fetched {len(data)} items. (Cumulative: {len(raw_records)})")

            link_header = resp.headers.get("Link", "")
            next_url = None
            if link_header:
                match = re.search(r'<([^>]+)>;\s*rel="next"', link_header)
                if match:
                    next_url = match.group(1)
            url = next_url
            page += 1

    return raw_records, page - 1


def evaluate_and_filter(raw_records):
    """Apply deterministic pre-registered inclusion and exclusion rules."""
    seen_ghsa = set()
    eligible_cases = []
    ledger = []

    exclusion_counts = {
        "MALWARE_ADVISORY": 0,
        "UNREVIEWED_STATUS": 0,
        "OUTSIDE_TEMPORAL_WINDOW": 0,
        "INVALID_GHSA_ID": 0,
        "INSUFFICIENT_METADATA": 0,
        "R5_SCENARIO_OVERLAP": 0,
        "DUPLICATE_GHSA_RECORD": 0
    }

    r5_overlaps_found = []

    for record in raw_records:
        ghsa_id = record.get("ghsa_id")
        cve_id = record.get("cve_id")
        advisory_type = record.get("type", "")
        published_at = record.get("published_at", "")
        summary = record.get("summary", "")
        description = record.get("description", "")
        vulnerabilities = record.get("vulnerabilities", [])

        # Check 1: Valid GHSA ID
        if not ghsa_id or not ghsa_id.startswith("GHSA-"):
            exclusion_counts["INVALID_GHSA_ID"] += 1
            ledger.append({
                "ghsa_id": ghsa_id or "UNKNOWN",
                "cve_id": cve_id,
                "decision": "EXCLUDED",
                "reason_code": "INVALID_GHSA_ID",
                "rule_reference": "Protocol Section 3.1 Rule 5",
                "details": "Missing or malformed GHSA identifier"
            })
            continue

        # Check 2: Deduplication
        if ghsa_id in seen_ghsa:
            exclusion_counts["DUPLICATE_GHSA_RECORD"] += 1
            ledger.append({
                "ghsa_id": ghsa_id,
                "cve_id": cve_id,
                "decision": "EXCLUDED",
                "reason_code": "DUPLICATE_GHSA_RECORD",
                "rule_reference": "Protocol Section 3.2 Rule 4",
                "details": f"Duplicate record encountered for {ghsa_id}"
            })
            continue
        seen_ghsa.add(ghsa_id)

        # Check 3: Reviewed status
        if advisory_type != "reviewed":
            exclusion_counts["UNREVIEWED_STATUS"] += 1
            ledger.append({
                "ghsa_id": ghsa_id,
                "cve_id": cve_id,
                "decision": "EXCLUDED",
                "reason_code": "UNREVIEWED_STATUS",
                "rule_reference": "Protocol Section 3.1 Rule 2 / Section 3.2 Rule 2",
                "details": f"Advisory type is '{advisory_type}', expected 'reviewed'"
            })
            continue

        # Check 4: Non-malware
        is_malware = False
        if "malware" in advisory_type.lower() or "malicious" in summary.lower():
            is_malware = True
        for vuln in vulnerabilities:
            pkg = vuln.get("package", {})
            if pkg.get("ecosystem") == "malware":
                is_malware = True
        if is_malware:
            exclusion_counts["MALWARE_ADVISORY"] += 1
            ledger.append({
                "ghsa_id": ghsa_id,
                "cve_id": cve_id,
                "decision": "EXCLUDED",
                "reason_code": "MALWARE_ADVISORY",
                "rule_reference": "Protocol Section 3.1 Rule 3 / Section 3.2 Rule 1",
                "details": "Classified as malware campaign"
            })
            continue

        # Check 5: Temporal window (2026-09-01T00:00:00Z <= published_at < 2026-10-01T00:00:00Z)
        if not (WINDOW_START <= published_at < WINDOW_END):
            exclusion_counts["OUTSIDE_TEMPORAL_WINDOW"] += 1
            ledger.append({
                "ghsa_id": ghsa_id,
                "cve_id": cve_id,
                "decision": "EXCLUDED",
                "reason_code": "OUTSIDE_TEMPORAL_WINDOW",
                "rule_reference": "Protocol Section 3.1 Rule 4 / Section 3.2 Rule 3",
                "details": f"Published timestamp {published_at} outside range [{WINDOW_START}, {WINDOW_END})"
            })
            continue

        # Check 6: Zero overlap with 30 R5 baseline scenarios
        is_r5_overlap = False
        overlap_cve = None
        if cve_id and cve_id in R5_CVES:
            is_r5_overlap = True
            overlap_cve = cve_id
        for ident in record.get("identifiers", []):
            if ident.get("type") == "CVE" and ident.get("value") in R5_CVES:
                is_r5_overlap = True
                overlap_cve = ident.get("value")

        if is_r5_overlap:
            exclusion_counts["R5_SCENARIO_OVERLAP"] += 1
            r5_overlaps_found.append({"ghsa_id": ghsa_id, "cve_id": overlap_cve})
            ledger.append({
                "ghsa_id": ghsa_id,
                "cve_id": overlap_cve,
                "decision": "EXCLUDED",
                "reason_code": "R5_SCENARIO_OVERLAP",
                "rule_reference": "Protocol Section 3.1 Rule 8 / Section 3.2 Rule 5",
                "details": f"Overlaps with R5 baseline scenario using {overlap_cve}"
            })
            continue

        # Check 7: Sufficient metadata (description/summary and package/ecosystem)
        has_text = bool(summary or description)
        has_package = bool(vulnerabilities and any(v.get("package", {}).get("name") for v in vulnerabilities))
        if not (has_text and has_package):
            exclusion_counts["INSUFFICIENT_METADATA"] += 1
            ledger.append({
                "ghsa_id": ghsa_id,
                "cve_id": cve_id,
                "decision": "EXCLUDED",
                "reason_code": "INSUFFICIENT_METADATA",
                "rule_reference": "Protocol Section 3.1 Rule 6 / Section 3.2 Rule 6",
                "details": f"Missing text or package info (has_text={has_text}, has_package={has_package})"
            })
            continue

        # Passed all checks -> INCLUDED
        aliases = []
        if cve_id:
            aliases.append(cve_id)
        for ident in record.get("identifiers", []):
            val = ident.get("value")
            if val and val != ghsa_id and val not in aliases:
                aliases.append(val)

        packages_info = []
        for v in vulnerabilities:
            pkg = v.get("package", {})
            packages_info.append({
                "ecosystem": pkg.get("ecosystem"),
                "name": pkg.get("name"),
                "vulnerable_version_range": v.get("vulnerable_version_range"),
                "first_patched_version": v.get("first_patched_version")
            })

        eligible_entry = {
            "canonical_ghsa_id": ghsa_id,
            "aliases": sorted(aliases),
            "published_at": published_at,
            "review_status": advisory_type,
            "summary": summary,
            "severity_source": record.get("severity"),
            "cvss_source": record.get("cvss"),
            "cvss_severities_source": record.get("cvss_severities"),
            "cwes": [c.get("cwe_id") for c in record.get("cwes", []) if c.get("cwe_id")],
            "affected_packages": packages_info,
            "source_references": record.get("references", []),
            "source_provenance": "GitHub Advisory Database (reviewed global advisory)",
            "status": "ELIGIBLE_LOCKED"
        }
        eligible_cases.append(eligible_entry)
        ledger.append({
            "ghsa_id": ghsa_id,
            "cve_id": cve_id,
            "decision": "INCLUDED",
            "reason_code": "ELIGIBLE",
            "rule_reference": "Protocol Section 3.1 Rules 1-8",
            "details": "Meets all inclusion criteria strictly"
        })

    # Sort eligible cases deterministically by canonical_ghsa_id
    eligible_cases.sort(key=lambda x: x["canonical_ghsa_id"])
    return eligible_cases, ledger, exclusion_counts, r5_overlaps_found


def verify_existing_artifacts():
    """Execute local offline verification of the locked corpus artifacts without network calls."""
    print("Executing offline verification of existing locked corpus artifacts...")

    required_files = [
        "raw_source_snapshot.json",
        "eligible_corpus_manifest.json",
        "inclusion_exclusion_ledger.json",
        "acquisition_metadata.json",
        "SHA256SUMS.txt"
    ]
    for rf in required_files:
        fpath = OUTPUT_DIR / rf
        if not fpath.exists():
            print(f"VERIFY FAILED: Missing artifact {fpath}", file=sys.stderr)
            return False

    with open(OUTPUT_DIR / "raw_source_snapshot.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
    with open(OUTPUT_DIR / "eligible_corpus_manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
    with open(OUTPUT_DIR / "inclusion_exclusion_ledger.json", "r", encoding="utf-8") as f:
        ledger = json.load(f)
    with open(OUTPUT_DIR / "acquisition_metadata.json", "r", encoding="utf-8") as f:
        meta = json.load(f)

    raw_count = len(raw)
    cases = manifest.get("cases", [])
    eligible_count = len(cases)
    ledger_count = len(ledger)

    reasons = {}
    for entry in ledger:
        rc = entry.get("reason_code", "UNKNOWN")
        reasons[rc] = reasons.get(rc, 0) + 1

    print(f"Counts: raw={raw_count}, eligible={eligible_count}, ledger={ledger_count}")
    print(f"Ledger reasons: {reasons}")

    # Check partition
    if raw_count != 947 or eligible_count != 938 or reasons.get("MALWARE_ADVISORY", 0) != 9:
        print(f"VERIFY FAILED: Counts mismatch. Expected 947/938/9, observed {raw_count}/{eligible_count}/{reasons.get('MALWARE_ADVISORY', 0)}", file=sys.stderr)
        return False

    if raw_count != eligible_count + reasons["MALWARE_ADVISORY"]:
        print("VERIFY FAILED: Partition raw != eligible + excluded", file=sys.stderr)
        return False

    # Check deduplication
    ghsas = [c["canonical_ghsa_id"] for c in cases]
    if len(ghsas) != len(set(ghsas)):
        print("VERIFY FAILED: Duplicate canonical GHSA detected", file=sys.stderr)
        return False

    # Check temporal window & review status
    for c in cases:
        pub = c.get("published_at", "")
        if not (WINDOW_START <= pub < WINDOW_END):
            print(f"VERIFY FAILED: Case {c.get('canonical_ghsa_id')} published_at {pub} outside temporal window", file=sys.stderr)
            return False
        if c.get("review_status") != "reviewed":
            print(f"VERIFY FAILED: Case {c.get('canonical_ghsa_id')} not reviewed", file=sys.stderr)
            return False

    # Check R5 overlap
    for c in cases:
        aliases = set(c.get("aliases", []))
        overlap = aliases.intersection(R5_CVES)
        if overlap:
            print(f"VERIFY FAILED: Overlap with R5 detected: {c.get('canonical_ghsa_id')} -> {overlap}", file=sys.stderr)
            return False

    # Check SHA-256 hashes against frozen ground truth
    calculated_hashes = {}
    for fname, exp_hash in FROZEN_HASHES.items():
        fpath = OUTPUT_DIR / fname
        h = hashlib.sha256()
        with open(fpath, "rb") as fp:
            while chunk := fp.read(65536):
                h.update(chunk)
        digest = h.hexdigest()
        calculated_hashes[fname] = digest
        if digest != exp_hash:
            print(f"VERIFY FAILED: Hash mismatch on {fname}. Expected {exp_hash}, calculated {digest}", file=sys.stderr)
            return False
        print(f"  {fname}: {digest} (MATCH)")

    # Check SHA256SUMS.txt
    with open(OUTPUT_DIR / "SHA256SUMS.txt", "r", encoding="utf-8") as fp:
        sums_content = fp.read()
    for fname, exp_hash in FROZEN_HASHES.items():
        if exp_hash not in sums_content:
            print(f"VERIFY FAILED: {fname} hash not recorded in SHA256SUMS.txt", file=sys.stderr)
            return False

    # Check registry consistency
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, "r", encoding="utf-8") as fp:
            reg = json.load(fp)
        if reg.get("corpus_manifest_sha256") != FROZEN_HASHES["eligible_corpus_manifest.json"]:
            print("VERIFY FAILED: Registry corpus_manifest_sha256 does not match frozen manifest hash", file=sys.stderr)
            return False
        if not reg.get("corpus_collected") or not reg.get("corpus_locked"):
            print("VERIFY FAILED: Registry corpus_collected or corpus_locked is not True", file=sys.stderr)
            return False
        print("Registry consistency confirmed.")

    print("ALL OFFLINE CHECKS PASSED: Corpus lock is verified 100% intact.")
    return True


def execute_acquisition():
    """Execute network acquisition and produce locked artifacts."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    acquisition_start_utc = datetime.now(timezone.utc).isoformat()
    raw_records, total_pages = fetch_raw_candidates()
    acquisition_end_utc = datetime.now(timezone.utc).isoformat()

    eligible_cases, ledger, exclusion_counts, r5_overlaps = evaluate_and_filter(raw_records)

    print(f"Acquisition finished. Total raw candidates: {len(raw_records)}")
    print(f"Eligible natural cases: {len(eligible_cases)}")
    print(f"Exclusion breakdown: {exclusion_counts}")
    print(f"R5 overlaps detected: {len(r5_overlaps)}")

    # 1. Write raw source snapshot
    raw_snapshot_path = OUTPUT_DIR / "raw_source_snapshot.json"
    with open(raw_snapshot_path, "w", encoding="utf-8") as f:
        json.dump(raw_records, f, indent=2, ensure_ascii=False)

    # 2. Write eligible corpus manifest
    manifest_path = OUTPUT_DIR / "eligible_corpus_manifest.json"
    manifest_data = {
        "schema": "https://helpus.org/schemas/r6_eligible_corpus_manifest_v1.json",
        "schema_version": "1.0.0",
        "manifest_type": "HELD_OUT_PUBLIC_CORPUS_MANIFEST",
        "acquisition_timestamp_utc": acquisition_start_utc,
        "preregistration_parent_commit": PREREGISTRATION_PARENT_COMMIT,
        "primary_source": "GitHub Advisory Database (reviewed global advisories)",
        "temporal_window_start": WINDOW_START,
        "temporal_window_end_exclusive": WINDOW_END,
        "eligible_natural_count": len(eligible_cases),
        "externality_boundary": (
            "The R6 held-out corpus provides independent public vulnerability evidence "
            "and tests transfer of the verification contract. Public vulnerability advisories "
            "do not, by themselves, establish real organizational Environmental metric ground truth. "
            "Any controlled environmental context used for execution must therefore remain "
            "explicitly labeled controlled context and must not be presented as independent "
            "human or organizational ground truth."
        ),
        "cases": eligible_cases
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    # 3. Write inclusion/exclusion ledger
    ledger_path = OUTPUT_DIR / "inclusion_exclusion_ledger.json"
    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)

    # 4. Write acquisition metadata
    meta_path = OUTPUT_DIR / "acquisition_metadata.json"
    meta_data = {
        "acquisition_timestamp_utc": acquisition_start_utc,
        "acquisition_completed_utc": acquisition_end_utc,
        "primary_source_endpoint": PRIMARY_ENDPOINT,
        "pagination_mechanism": "cursor_based_link_header",
        "total_pages_fetched": total_pages,
        "query_parameters": QUERY_PARAMS,
        "raw_candidate_count": len(raw_records),
        "eligible_natural_count": len(eligible_cases),
        "total_exclusions": len(raw_records) - len(eligible_cases),
        "exclusion_breakdown": exclusion_counts,
        "r5_overlap_count": len(r5_overlaps),
        "r5_overlap_candidates": r5_overlaps,
        "zero_selection_by_cvss_or_result": True,
        "corpus_collected": True,
        "corpus_locked": True,
        "results_available": False,
        "experiments_executed": False
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=2, ensure_ascii=False)

    # 5. Compute SHA256SUMS.txt
    files_to_hash = [
        "raw_source_snapshot.json",
        "eligible_corpus_manifest.json",
        "inclusion_exclusion_ledger.json",
        "acquisition_metadata.json"
    ]
    checksums = {}
    checksums_txt_lines = []
    for fname in sorted(files_to_hash):
        fpath = OUTPUT_DIR / fname
        h = hashlib.sha256()
        with open(fpath, "rb") as fp:
            while chunk := fp.read(65536):
                h.update(chunk)
        digest = h.hexdigest()
        checksums[fname] = digest
        checksums_txt_lines.append(f"{digest}  {fname}\n")

    sums_path = OUTPUT_DIR / "SHA256SUMS.txt"
    with open(sums_path, "w", encoding="utf-8") as f:
        f.writelines(checksums_txt_lines)

    manifest_sha256 = checksums["eligible_corpus_manifest.json"]
    print("SHA256SUMS calculated successfully.")
    for k, v in checksums.items():
        print(f"  {k}: {v}")

    # 6. Update experiment registry
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            reg = json.load(f)

        reg["held_out_source_specification"] = "FROZEN"
        reg["corpus_collected"] = True
        reg["corpus_locked"] = True
        reg["results_available"] = False
        reg["experiments_executed"] = False
        reg["eligible_case_count"] = len(eligible_cases)
        reg["raw_candidate_count"] = len(raw_records)
        reg["acquisition_timestamp_utc"] = acquisition_start_utc
        reg["corpus_manifest_sha256"] = manifest_sha256

        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(reg, f, indent=2, ensure_ascii=False)

        print("Updated experiment registry successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="R6-A1 Held-Out Corpus Acquisition and Verification Tool"
    )
    parser.add_argument(
        "--verify-existing",
        action="store_true",
        help="Run local offline integrity and hash verification against already locked artifacts."
    )
    parser.add_argument(
        "--force-regenerate",
        action="store_true",
        help="Force re-acquisition and overwrite existing locked artifacts (strictly disallowed when locked)."
    )
    args = parser.parse_args()

    if args.verify_existing:
        success = verify_existing_artifacts()
        sys.exit(0 if success else 1)

    # Fail-closed safety check
    manifest_lock = OUTPUT_DIR / "eligible_corpus_manifest.json"
    if manifest_lock.exists() and not args.force_regenerate:
        print(
            "FAIL-CLOSED: Held-out corpus manifest already exists and is locked. "
            "To verify existing lock without network calls, use --verify-existing. "
            "Re-acquisition requires explicit --force-regenerate.",
            file=sys.stderr
        )
        sys.exit(1)

    execute_acquisition()


if __name__ == "__main__":
    main()
