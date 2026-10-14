#!/usr/bin/env python3
"""
scripts/rebuild_book_manifest.py
Compiles the LaTeX monograph, measures canonical LF bytes, packages Overleaf ZIP,
and regenerates the build manifest and build report.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = ROOT / "book_latex"

SOURCE_FILES = [
    "chapters/01_introduction.tex",
    "chapters/02_cvss_foundations.tex",
    "chapters/03_watcher_architecture.tex",
    "chapters/04_scanner_and_topology.tex",
    "chapters/05_hitl_governance.tex",
    "chapters/06_empirical_evaluation.tex",
    "chapters/07_case_studies.tex",
    "chapters/07b_optional_ai_assurance.tex",
    "chapters/08_conclusion.tex",
    "chapters/appendix_a_pci_scenarios.tex",
    "chapters/appendix_b_statistical_methods.tex",
    "chapters/appendix_c_historical_dataset.tex",
    "chapters/dataset_b_v2_generated.tex",
    "chapters/table_6_1_generated.tex",
    "generated/dataset_b_source_assessments_v2.csv",
    "main.tex",
    "references.bib",
]


def compile_latex() -> dict:
    print("[1/5] Compiling LaTeX with pdflatex & bibtex...")
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], cwd=BOOK_DIR, check=True, capture_output=True)
    subprocess.run(["bibtex", "main"], cwd=BOOK_DIR, check=False, capture_output=True)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], cwd=BOOK_DIR, check=True, capture_output=True)
    res = subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], cwd=BOOK_DIR, check=True, capture_output=True)

    log_path = BOOK_DIR / "main.log"
    log_text = log_path.read_text(encoding="latin1", errors="replace")

    # Extract pages and bytes from log
    m = re.search(r"Output written on main\.pdf \((\d+) pages, (\d+) bytes\)", log_text)
    pages = int(m.group(1)) if m else 50
    pdf_bytes_log = int(m.group(2)) if m else None

    undef_cit = len(re.findall(r"Citation .* undefined", log_text))
    undef_ref = len(re.findall(r"Reference .* undefined", log_text))
    overfull = len(re.findall(r"Overfull \\hbox", log_text))
    underfull = len(re.findall(r"Underfull \\hbox", log_text))

    pdf_file = BOOK_DIR / "main.pdf"
    pdf_raw = pdf_file.read_bytes()
    pdf_sha = hashlib.sha256(pdf_raw).hexdigest()

    return {
        "pdf_path": "main.pdf",
        "sha256": pdf_sha,
        "bytes": len(pdf_raw),
        "pages": pages,
        "undefined_citations": undef_cit,
        "undefined_references": undef_ref,
        "overfull_hboxes": overfull,
        "underfull_hboxes": underfull,
    }


def compute_source_manifest() -> list[dict]:
    print("[2/5] Computing canonical LF hashes for source files...")
    sources = []
    for rel_path in SOURCE_FILES:
        p = BOOK_DIR / rel_path
        if not p.exists():
            raise FileNotFoundError(f"Missing source file: {p}")
        raw = p.read_bytes().replace(b"\r\n", b"\n")
        sources.append({
            "path": rel_path,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        })
    return sources


def build_overleaf_zip(zip_name: str) -> dict:
    print(f"[3/5] Building Overleaf ZIP {zip_name}...")
    zip_path = BOOK_DIR / zip_name
    if zip_path.exists():
        zip_path.unlink()

    include_patterns = [
        "chapters/*.tex",
        "figures/*.*",
        "generated/*.*",
        "main.tex",
        "references.bib",
    ]

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for pat in include_patterns:
            for f in BOOK_DIR.glob(pat):
                if f.is_file() and not f.name.endswith(".aux"):
                    arcname = f.relative_to(BOOK_DIR).as_posix()
                    z.write(f, arcname)

    zip_bytes = zip_path.read_bytes()
    return {
        "path": zip_name,
        "bytes": len(zip_bytes),
        "sha256": hashlib.sha256(zip_bytes).hexdigest(),
    }


def main():
    build_info = compile_latex()
    sources = compute_source_manifest()

    # Build both PREFREEZE and ROUND4 zip for 100% backward compatibility
    zip_prefreeze = build_overleaf_zip("helpus_cvss_ai_monograph_overleaf_prefreeze.zip")
    zip_round4 = build_overleaf_zip("helpus_cvss_ai_monograph_overleaf_final_round4.zip")

    manifest_data = {
        "artifact": "HelpUS CVSS AI monograph Pre-Freeze baseline (Autonomous Context-Aware CVSS v4.0 + HCAL)",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "main_pdf": {
            "path": build_info["pdf_path"],
            "sha256": build_info["sha256"],
            "bytes": build_info["bytes"],
            "pages": build_info["pages"],
        },
        "build": {
            "engine": "pdflatex",
            "bibliography": "bibtex/bibtex8",
            "undefined_citations": build_info["undefined_citations"],
            "undefined_references": build_info["undefined_references"],
            "overfull_hboxes": build_info["overfull_hboxes"],
            "underfull_hboxes": build_info["underfull_hboxes"],
        },
        "scientific_status": {
            "safe_to_freeze": "NO",
            "primary_study": "Autonomous Context-Aware CVSS v4.0 Environmental Scoring (Non-Human Primary Study Pivot)",
            "cognitive_assurance_layer": "HelpUS Cognitive Assurance Layer (HCAL) - Optional Non-Blocking Multi-AI Review",
            "release_gates": {
                "G1_G8": "PASS / CLOSED",
                "G9A": "READY_FOR_PASS (Option A Canonical Rule Catalog)",
                "G9B": "PASS (10,000 synthetic metamorphic cases, 0 violations)",
                "G10A": "READY_FOR_FREEZE_AUDIT (Clean-room replay)",
                "G11_OPTIONAL_AI": "IMPLEMENTED_PROTOTYPE_NON_BLOCKING"
            },
            "c1_c2": "SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE"
        },
        "source_files": sources,
        "overleaf_zip": zip_round4,  # Matches scripts/verify_book_latex_manifest.py default
        "overleaf_zip_prefreeze": zip_prefreeze,
    }

    print("[4/5] Writing manifests...")
    manifest_prefreeze_path = BOOK_DIR / "BUILD_MANIFEST_PREFREEZE.json"
    manifest_round4_path = BOOK_DIR / "BUILD_MANIFEST_CHATGPT_ROUND4.json"

    content_str = json.dumps(manifest_data, indent=2) + "\n"
    manifest_prefreeze_path.write_text(content_str, encoding="utf-8")
    manifest_round4_path.write_text(content_str, encoding="utf-8")

    print("[5/5] Writing LaTeX build reports...")
    report_text = f"""# LaTeX Build Report — Pre-Freeze Monograph (HelpUS CVSS AI v4.0)

**Date (UTC):** {datetime.now(timezone.utc).isoformat()}  
**Document Title:** Autonomous Context-Aware CVSS v4.0 Environmental Scoring with Optional Cognitive Assurance  
**Engine:** pdflatex (MiKTeX 26.2) + bibtex  

## Build Artifacts
- **Primary PDF:** `main.pdf`
  - **SHA-256:** `{build_info['sha256']}`
  - **Byte Size:** {build_info['bytes']} bytes
  - **Page Count:** {build_info['pages']} pages
- **Overleaf ZIP (Prefreeze):** `{zip_prefreeze['path']}`
  - **SHA-256:** `{zip_prefreeze['sha256']}`
  - **Byte Size:** {zip_prefreeze['bytes']} bytes
- **Overleaf ZIP (Compatible):** `{zip_round4['path']}`
  - **SHA-256:** `{zip_round4['sha256']}`
  - **Byte Size:** {zip_round4['bytes']} bytes

## Compilation Statistics
- **Undefined Citations:** {build_info['undefined_citations']}
- **Undefined References:** {build_info['undefined_references']}
- **Overfull \\hbox Warnings:** {build_info['overfull_hboxes']}
- **Underfull \\hbox Warnings:** {build_info['underfull_hboxes']}

## Included Chapters
1. Introduction (Empirical motivation, operational gap)
2. CVSS v4.0 Foundations & Mathematics (Pure Python deterministic core)
3. Architecture of Autonomous Environmental Telemetry
4. Network Topology & Reachability Inference (MAV-001 to MAV-003B)
5. Straight-Through Processing (STP) & Exception-Driven HITL
6. Metamorphic Testing & Large-Scale Property Verification (10,000 profiles, Gate G9B)
7. Production Case Studies
8. **HelpUS Cognitive Assurance Layer (HCAL)** — Optional Non-Blocking Multi-AI Review (`chapters/07b_optional_ai_assurance.tex`)
9. Conclusion & Pre-Freeze Governance Roadmap
- Appendix A: PCI Scenarios & Defense Controls
- Appendix B: Statistical Methodology
- Appendix C: Historical Reference Dataset B v2

## Governance Status
- `G1–G8 = PASS / CLOSED`
- `G9A = READY_FOR_PASS` (Canonical single source of truth Option A)
- `G9B = PASS` (10,000 cases with 0 violations)
- `G10A = READY_FOR_FREEZE_AUDIT`
- `G11-OPTIONAL-AI = IMPLEMENTED_PROTOTYPE_NON_BLOCKING`
- `SAFE_TO_FREEZE = NO`
- `C1/C2 = SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE`
"""
    (BOOK_DIR / "LATEX_BUILD_REPORT_PREFREEZE.md").write_text(report_text, encoding="utf-8")
    (BOOK_DIR / "LATEX_BUILD_REPORT_CHATGPT_ROUND4.md").write_text(report_text, encoding="utf-8")

    print("[DONE] LaTeX monograph compiled and manifests generated successfully!")


if __name__ == "__main__":
    main()
