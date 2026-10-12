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
        "sha256": "f653914506e697a94a18b690c051144b295626c534737fb79c589a61c1e0e8a3",
        "size_bytes": 23490,
        "lines": 270,
    },
    "macro-scores": {
        "sha256": "b55926940d4fbb073a0d30a98d6983de93f4542209eee936a671713387f92213",
        "size_bytes": 36677,
        "lines": 270,
    },
    "reference-vectors": {
        "sha256": "fdcb3de3485354ff36577b41b2fcf7f8056785fb6d6bf6c6eed97e7d3bc934bf",
        "size_bytes": 6911531,
        "lines": 66331,
    },
    "reference-scores": {
        "sha256": "3b60f12899249bf8b48e01ff0aba451f052a836b22c6a3ffd880b7a5cc2fea4f",
        "size_bytes": 11648072,
        "lines": 66331,
    },
    "base-threat-vectors": {
        "sha256": "eb9cf89bab6712f368fe65c43f884e1ca4750e4e30181fabad4a61aaecccede1",
        "size_bytes": 28553472,
        "lines": 419904,
    },
    "base-threat-scores": {
        "sha256": "2695a9b8664608dbf589d48cc8f5cb3f136c7a20d180fa8a54787810c2566ba3",
        "size_bytes": 48848647,
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
