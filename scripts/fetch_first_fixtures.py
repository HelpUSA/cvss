#!/usr/bin/env python3
"""Deterministic fixture acquisition and verification for FIRST CVSS v4.0 reference corpus.

Pinnned FIRST commit: d766d0c8ab4368b67bf27dd0e411eb481f05fdbb
Repository: https://github.com/FIRSTdotorg/cvss-resources
"""
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "cvss_resources" / "vectorFiles"
FIRST_COMMIT = "d766d0c8ab4368b67bf27dd0e411eb481f05fdbb"
RAW_BASE_URL = f"https://raw.githubusercontent.com/FIRSTdotorg/cvss-resources/{FIRST_COMMIT}/vectorFiles"

FIXTURE_MANIFEST = {
    "macro-vectors": {
        "sha256": "e11a88715465c1b763027b4c49f3d37d080241ad167cddf6d3e0d3ebb725a90c",
        "size_bytes": 23760,
        "lines": 270,
    },
    "macro-scores": {
        "sha256": "c422d64e908c7d605267521619bab880762584e5fa3108ca2c539751cbbd6f4b",
        "size_bytes": 36947,
        "lines": 270,
    },
    "reference-vectors": {
        "sha256": "81918c58ff73a0bd82567fbd6b57b3d587a7bb6d1bf7833a471dd70825808c34",
        "size_bytes": 6977862,
        "lines": 66331,
    },
    "reference-scores": {
        "sha256": "7bd6f6b162441a3bf591c946a7488e827776f390748133eb3cfb4df11fff6ad8",
        "size_bytes": 11714403,
        "lines": 66331,
    },
    "base-threat-vectors": {
        "sha256": "b62819bb46716e9de9628d24e266d27ddf04b3b0d1140bc1956909f9dd21bb2b",
        "size_bytes": 28973376,
        "lines": 419904,
    },
    "base-threat-scores": {
        "sha256": "eb8c4afddd8073b2aae2956e022678215e5e969d313e40a6efed4c206df4c7ca",
        "size_bytes": 49268551,
        "lines": 419904,
    },
}

def download_file(url: str, dest_path: Path):
    print(f"Downloading {url} -> {dest_path.name}...")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = dest_path.with_suffix(".tmp")
    req = urllib.request.Request(url, headers={"User-Agent": "HelpUS-CVSS-Fixture-Fetcher/1.0"})
    with urllib.request.urlopen(req) as resp, open(temp_path, "wb") as f:
        while chunk := resp.read(1024 * 1024):
            f.write(chunk)
    temp_path.replace(dest_path)

def verify_and_fetch():
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    verified = {}
    for filename, spec in FIXTURE_MANIFEST.items():
        filepath = FIXTURE_DIR / filename
        needs_fetch = False
        if not filepath.exists():
            needs_fetch = True
        else:
            data = filepath.read_bytes()
            if hashlib.sha256(data).hexdigest() != spec["sha256"]:
                needs_fetch = True

        if needs_fetch:
            url = f"{RAW_BASE_URL}/{filename}"
            download_file(url, filepath)

        data = filepath.read_bytes()
        actual_sha = hashlib.sha256(data).hexdigest()
        actual_size = len(data)
        actual_lines = data.count(b"\n")

        assert actual_sha == spec["sha256"], f"SHA mismatch on {filename}"
        assert actual_size == spec["size_bytes"], f"Size mismatch on {filename}"
        assert actual_lines == spec["lines"], f"Line mismatch on {filename}"

        verified[filename] = {
            "sha256": actual_sha,
            "size_bytes": actual_size,
            "lines": actual_lines,
            "verified": True,
        }
        print(f"  [OK] {filename}: {actual_size:,} bytes, {actual_lines:,} lines, sha256={actual_sha[:16]}...")

    manifest_path = FIXTURE_DIR / "FIXTURE_VERIFICATION_MANIFEST.json"
    manifest_path.write_text(json.dumps({"commit": FIRST_COMMIT, "fixtures": verified}, indent=2), encoding="utf-8")
    print("\nAll 6 FIRST CVSS v4.0 fixture files verified deterministically.")
    return True

if __name__ == "__main__":
    verify_and_fetch()
