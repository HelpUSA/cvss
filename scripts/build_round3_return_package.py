#!/usr/bin/env python3
"""Build final comprehensive round 3 return package for ChatGPT review."""
import hashlib
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIP_NAME = "helpus_cvss_ai_antigravity_round3_return_package_complete.zip"
OUT_ZIP = ROOT / ZIP_NAME

INCLUDE_PATHS = [
    "core",
    "tests",
    "scripts",
    "data/dataset_b",
    "data/article",
    "data/dataset_b_source_assessments_normalized.csv",
    "docs/scientific-validation",
    "outputs",
    "pyproject.toml",
    "requirements.txt",
    "pytest.ini",
    "03_DATASET_B_PROVENANCE_SUMMARY.md",
    "book_latex/main.pdf",
    "book_latex/helpus_cvss_ai_monograph_chatgpt_round3.pdf",
    "book_latex/helpus_cvss_ai_monograph_overleaf_final_round3.zip",
    "book_latex/BUILD_MANIFEST_CHATGPT_ROUND3.json",
    "book_latex/OVERLEAF_README_CHATGPT_ROUND3.md",
    "book_latex/ROUND3_BOOK_CHANGELOG.md",
    "book_latex/LATEX_BUILD_REPORT_CHATGPT_ROUND3.md",
    "web/src/lib/jcs.ts",
    "web/src/app/api/analyze-environment/route.ts",
    "web/scripts/test_jcs_conformance.ts",
    "web/scripts/test_analyze_route.ts",
    "web/package.json",
    "web/package-lock.json",
    "web/tsconfig.json",
    "index.html",
    "app.js",
]

def main():
    print(f"=== ASSEMBLING {ZIP_NAME} ===")
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for item in INCLUDE_PATHS:
            p = ROOT / item
            if not p.exists():
                print(f"Skipping missing: {p}")
                continue
            if p.is_file():
                z.write(p, item)
                print(f"Added file: {item}")
            elif p.is_dir():
                for root, dirs, files in os.walk(p):
                    dirs[:] = [d for d in dirs if d not in ["__pycache__", ".pytest_cache", ".next", "node_modules", ".git", "cvss_resources"]]
                    for file in files:
                        if file.endswith((".pyc", ".DS_Store", ".tmp")):
                            continue
                        full_path = Path(root) / file
                        rel_path = full_path.relative_to(ROOT)
                        z.write(full_path, str(rel_path))
                print(f"Added directory: {item}")

    h = hashlib.sha256()
    with OUT_ZIP.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    size = OUT_ZIP.stat().st_size
    print(f"\nFinal Round 3 return package created: {OUT_ZIP.name}")
    print(f"Size: {size:,} bytes ({size / (1024*1024):.2f} MB)")
    print(f"SHA-256: {h.hexdigest()}")

if __name__ == "__main__":
    main()
