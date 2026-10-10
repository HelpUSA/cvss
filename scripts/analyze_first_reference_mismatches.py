#!/usr/bin/env python3
"""Analyze mismatch evidence without converting mismatches into passes."""
import json, sys
from collections import Counter
from pathlib import Path

p = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs/first-reference-corpus-round4.json")
d = json.loads(p.read_text(encoding="utf-8"))
mm = d.get("mismatches", [])
score_mm = [m for m in mm if m.get("expected_kind") == "score"]
print(f"mismatches={len(mm)} score_mismatches={len(score_mm)}")
print("delta histogram:", Counter(str(m.get("absolute_delta")) for m in score_mm))
print("severity mismatches:", sum((m.get("expected_severity") or '').lower() != (m.get("observed_severity") or '').lower() for m in score_mm))
print("\nREMEDIATION DECISION:")
print("- Do not waive +/-0.1 differences.")
print("- Differentially run the pinned FIRST reference JS calculator implementation on the same rows.")
print("- If the FIRST reference implementation matches vectorFiles, adopt/pin it or port its exact arithmetic/rounding and rerun this gate.")
print("- If the FIRST reference implementation also disagrees with vectorFiles, preserve G1=FAIL/PENDING and document the exact upstream inconsistency before any confirmatory study.")
