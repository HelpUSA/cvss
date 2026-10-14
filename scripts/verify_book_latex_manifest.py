#!/usr/bin/env python3
"""
Verify exact correspondence between:
1. book_latex/BUILD_MANIFEST_CHATGPT_ROUND4.json
2. Git blobs / canonical repository bytes
3. book_latex/main.pdf
4. book_latex/helpus_cvss_ai_monograph_overleaf_final_round4.zip
5. book_latex/LATEX_BUILD_REPORT_CHATGPT_ROUND4.md
"""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = ROOT / "book_latex"
MANIFEST_PATH = BOOK_DIR / "BUILD_MANIFEST_CHATGPT_ROUND4.json"
REPORT_PATH = BOOK_DIR / "LATEX_BUILD_REPORT_CHATGPT_ROUND4.md"

def main() -> int:
    errors = []
    if not MANIFEST_PATH.exists():
        print(f"FATAL: Manifest not found: {MANIFEST_PATH}")
        return 1

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    # 1. Verify main PDF
    pdf_info = manifest.get("main_pdf", {})
    pdf_path = BOOK_DIR / pdf_info.get("path", "main.pdf")
    if not pdf_path.exists():
        errors.append(f"main.pdf not found on disk: {pdf_path}")
    else:
        pdf_bytes = pdf_path.read_bytes()
        actual_pdf_sha = hashlib.sha256(pdf_bytes).hexdigest()
        actual_pdf_size = len(pdf_bytes)
        if actual_pdf_size != pdf_info.get("bytes"):
            errors.append(f"main.pdf size mismatch: expected {pdf_info.get('bytes')}, got {actual_pdf_size}")
        if actual_pdf_sha.lower() != pdf_info.get("sha256", "").lower():
            errors.append(f"main.pdf sha256 mismatch: expected {pdf_info.get('sha256')}, got {actual_pdf_sha}")

    # 2. Verify Overleaf ZIP
    zip_info = manifest.get("overleaf_zip", {})
    zip_path = BOOK_DIR / zip_info.get("path", "")
    if not zip_path.exists():
        errors.append(f"Overleaf ZIP not found on disk: {zip_path}")
    else:
        zip_bytes = zip_path.read_bytes()
        actual_zip_sha = hashlib.sha256(zip_bytes).hexdigest()
        actual_zip_size = len(zip_bytes)
        if actual_zip_size != zip_info.get("bytes"):
            errors.append(f"Overleaf ZIP size mismatch: expected {zip_info.get('bytes')}, got {actual_zip_size}")
        if actual_zip_sha.lower() != zip_info.get("sha256", "").lower():
            errors.append(f"Overleaf ZIP sha256 mismatch: expected {zip_info.get('sha256')}, got {actual_zip_sha}")

    # 3. Verify all declared source files against canonical Git blobs / LF bytes
    sources = manifest.get("source_files", [])
    matched_sources = 0
    for item in sources:
        rel_path = item["path"]
        expected_size = item["bytes"]
        expected_sha = item["sha256"].lower()

        # Try git show HEAD:book_latex/<rel_path> first
        git_cmd = ["git", "show", f"HEAD:book_latex/{rel_path}"]
        proc = subprocess.run(git_cmd, capture_output=True, cwd=ROOT)
        if proc.returncode == 0:
            raw = proc.stdout
        else:
            disk_path = BOOK_DIR / rel_path
            if not disk_path.exists():
                errors.append(f"Source file not found: {rel_path}")
                continue
            raw = disk_path.read_bytes().replace(b"\r\n", b"\n")

        actual_size = len(raw)
        actual_sha = hashlib.sha256(raw).hexdigest().lower()

        if actual_size != expected_size:
            errors.append(f"Source {rel_path} size mismatch: manifest={expected_size}, actual={actual_size}")
        elif actual_sha != expected_sha:
            errors.append(f"Source {rel_path} sha256 mismatch: manifest={expected_sha}, actual={actual_sha}")
        else:
            matched_sources += 1

    # 4. Verify LaTeX build report references matching PDF
    if REPORT_PATH.exists():
        report_text = REPORT_PATH.read_text(encoding="utf-8")
        if pdf_info.get("sha256") not in report_text:
            errors.append(f"Build report does not reference manifest PDF SHA-256 {pdf_info.get('sha256')}")
        if str(pdf_info.get("bytes")) not in report_text:
            errors.append(f"Build report does not reference manifest PDF byte size {pdf_info.get('bytes')}")
    else:
        errors.append(f"Build report missing: {REPORT_PATH}")

    if errors:
        print("FAIL: Book manifest verification errors:")
        for err in errors:
            print("  -", err)
        return 1

    print(f"PASS: Book manifest verified successfully. {matched_sources}/{len(sources)} source files match Git blobs exactly.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
