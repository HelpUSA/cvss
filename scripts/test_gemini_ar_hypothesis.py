#!/usr/bin/env python3
"""Empirical test of Gemini's AR / VA:N / SA:N sensitivity hypothesis.

Gemini assertion:
"Quando VA:N e SA:N, AR seria sempre irrelevante"
"""
from __future__ import annotations
import itertools
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.cvss_sensitivity import score_envelope
from core.cvss40 import score

def run_experiment():
    print("=== Testing Gemini AR Hypothesis: 'When VA=N and SA=N, AR is always irrelevant' ===")
    
    non_invariant_found = []
    tested = 0
    
    av_vals = ["N", "A", "L", "P"]
    ac_vals = ["L", "H"]
    at_vals = ["N", "P"]
    pr_vals = ["N", "L", "H"]
    ui_vals = ["N", "P", "A"]
    vc_vals = ["H", "L", "N"]
    vi_vals = ["H", "L", "N"]
    sc_vals = ["H", "L", "N"]
    si_vals = ["H", "L", "N"]
    
    # Grid search across all combinations of impacts with VA:N and SA:N
    for av in ["N", "L"]:
        for ac in ["L", "H"]:
            for at in ["N", "P"]:
                for pr in ["N", "L"]:
                    for ui in ["N", "P"]:
                        for vc in vc_vals:
                            for vi in vi_vals:
                                for sc in sc_vals:
                                    for si in si_vals:
                                        if vc == "N" and vi == "N" and sc == "N" and si == "N":
                                            continue
                                        vec = f"CVSS:4.0/AV:{av}/AC:{ac}/AT:{at}/PR:{pr}/UI:{ui}/VC:{vc}/VI:{vi}/VA:N/SC:{sc}/SI:{si}/SA:N"
                                        tested += 1
                                        res = score_envelope(vec, {"AR": ["L", "M", "H"]})
                                        if not res["invariant"]:
                                            non_invariant_found.append((vec, res))
    
    print(f"Total vectors tested: {tested}")
    print(f"Non-invariant vectors found: {len(non_invariant_found)}")
    
    if non_invariant_found:
        print("RESULT: HYPOTHESIS REFUTED!")
        print(f"Found {len(non_invariant_found)} counterexamples where VA=N and SA=N, but AR in {{L, M, H}} changes the score:")
        for vec, res in non_invariant_found[:10]:
            print(f"  Vector: {vec}")
            print(f"    min_score: {res['min_score']}, max_score: {res['max_score']}, unique: {res['unique_scores']}")
    else:
        print("RESULT: HYPOTHESIS CONFIRMED!")
        print("All tested vectors with VA=N and SA=N were invariant under AR in {L, M, H}.")

    # Also test CR, IR, AR full domains
    print("\n=== Sensitivity Table for Representative Vectors ===")
    sample_vectors = [
        ("Base Critical", "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"),
        ("Base High (VA:N)", "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"),
        ("Base Med (VA:N, SA:N)", "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"),
        ("Local Low (VA:N, SA:N)", "CVSS:4.0/AV:L/AC:H/AT:P/PR:H/UI:A/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"),
    ]
    
    for label, bvec in sample_vectors:
        print(f"\n--- {label}: {bvec} ---")
        for metric, domain in [
            ("AR", ["L", "M", "H"]),
            ("CR", ["L", "M", "H"]),
            ("IR", ["L", "M", "H"]),
            ("CR+IR+AR", {"CR": ["L", "M", "H"], "IR": ["L", "M", "H"], "AR": ["L", "M", "H"]}),
        ]:
            if isinstance(domain, dict):
                env = score_envelope(bvec, domain)
                print(f"  Domain: CR,IR,AR in {{L,M,H}} (27 comb) -> min={env['min_score']}, max={env['max_score']}, invariant={env['invariant']}")
            else:
                env = score_envelope(bvec, {metric: domain})
                print(f"  Domain: {metric} in {domain} (3 comb) -> min={env['min_score']}, max={env['max_score']}, invariant={env['invariant']}")

if __name__ == "__main__":
    run_experiment()
