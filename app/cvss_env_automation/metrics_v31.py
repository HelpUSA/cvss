"""
CVSS v3.1 scoring utilities focused on environmental metrics.

This is a research prototype intended to support reproducible experiments.
It implements the CVSS v3.1 base/environmental formulas sufficiently for
controlled case-study scenarios and transparent audit output.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple


AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20}
AC = {"L": 0.77, "H": 0.44}
UI = {"N": 0.85, "R": 0.62}
S = {"U": "U", "C": "C"}
CIA = {"H": 0.56, "L": 0.22, "N": 0.0}
REQ = {"H": 1.5, "M": 1.0, "L": 0.5, "X": 1.0}
E = {"X": 1.0, "H": 1.0, "F": 0.97, "P": 0.94, "U": 0.91}
RL = {"X": 1.0, "U": 1.0, "W": 0.97, "T": 0.96, "O": 0.95}
RC = {"X": 1.0, "C": 1.0, "R": 0.96, "U": 0.92}


def _round_up_1(x: float) -> float:
    """CVSS round-up to one decimal place."""
    return math.ceil(x * 10.0 - 1e-7) / 10.0


def parse_vector(vector: str) -> Dict[str, str]:
    if not vector.startswith("CVSS:3."):
        raise ValueError(f"Only CVSS v3.x vectors are supported in this prototype: {vector}")
    metrics: Dict[str, str] = {}
    for part in vector.split("/")[1:]:
        if ":" not in part:
            continue
        key, value = part.split(":", 1)
        metrics[key] = value
    required = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]
    missing = [k for k in required if k not in metrics]
    if missing:
        raise ValueError(f"Missing base metrics {missing} in vector: {vector}")
    return metrics


def _pr_value(pr: str, scope: str) -> float:
    if pr == "N":
        return 0.85
    if pr == "L":
        return 0.62 if scope == "U" else 0.68
    if pr == "H":
        return 0.27 if scope == "U" else 0.50
    raise ValueError(f"Unknown PR value: {pr}")


def base_score(metrics: Dict[str, str]) -> float:
    iss = 1 - ((1 - CIA[metrics["C"]]) * (1 - CIA[metrics["I"]]) * (1 - CIA[metrics["A"]]))
    if metrics["S"] == "U":
        impact = 6.42 * iss
    else:
        impact = 7.52 * (iss - 0.029) - 3.25 * ((iss - 0.02) ** 15)
    exploitability = (
        8.22
        * AV[metrics["AV"]]
        * AC[metrics["AC"]]
        * _pr_value(metrics["PR"], metrics["S"])
        * UI[metrics["UI"]]
    )
    if impact <= 0:
        return 0.0
    if metrics["S"] == "U":
        return _round_up_1(min(impact + exploitability, 10.0))
    return _round_up_1(min(1.08 * (impact + exploitability), 10.0))


def environmental_score(base: Dict[str, str], env: Dict[str, str]) -> float:
    """Compute CVSS v3.1 environmental score using modified metrics."""
    ms = env.get("MS", "X")
    scope = base["S"] if ms == "X" else ms

    mav = env.get("MAV", "X")
    mac = env.get("MAC", "X")
    mpr = env.get("MPR", "X")
    mui = env.get("MUI", "X")
    mc = env.get("MC", "X")
    mi = env.get("MI", "X")
    ma = env.get("MA", "X")

    av = base["AV"] if mav == "X" else mav
    ac = base["AC"] if mac == "X" else mac
    pr = base["PR"] if mpr == "X" else mpr
    ui = base["UI"] if mui == "X" else mui
    c = base["C"] if mc == "X" else mc
    i = base["I"] if mi == "X" else mi
    a = base["A"] if ma == "X" else ma

    cr = env.get("CR", "X")
    ir = env.get("IR", "X")
    ar = env.get("AR", "X")

    miss = min(
        1 - ((1 - CIA[c] * REQ[cr]) * (1 - CIA[i] * REQ[ir]) * (1 - CIA[a] * REQ[ar])),
        0.915,
    )

    if scope == "U":
        modified_impact = 6.42 * miss
    else:
        modified_impact = 7.52 * (miss - 0.029) - 3.25 * ((miss * 0.9731 - 0.02) ** 13)

    modified_exploitability = 8.22 * AV[av] * AC[ac] * _pr_value(pr, scope) * UI[ui]

    if modified_impact <= 0:
        return 0.0

    temp = E[env.get("E", "X")] * RL[env.get("RL", "X")] * RC[env.get("RC", "X")]
    if scope == "U":
        return _round_up_1(_round_up_1(min(modified_impact + modified_exploitability, 10.0)) * temp)
    return _round_up_1(_round_up_1(min(1.08 * (modified_impact + modified_exploitability), 10.0)) * temp)


def build_environmental_vector(base_vector: str, env: Dict[str, str]) -> str:
    order = ["CR", "IR", "AR", "MAV", "MAC", "MPR", "MUI", "MS", "MC", "MI", "MA", "E", "RL", "RC"]
    parts = [base_vector]
    for key in order:
        if key in env and env[key] != "":
            parts.append(f"{key}:{env[key]}")
    return "/".join(parts)
