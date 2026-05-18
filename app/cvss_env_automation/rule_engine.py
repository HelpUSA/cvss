"""
Evidence-based CVSS Environmental inference.

The goal is not to hide analyst judgment. The goal is to make every environmental
metric proposal explainable by evidence from files, topology and scope.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .metrics_v31 import parse_vector, base_score, environmental_score, build_environmental_vector


def _asset_by_id(case: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    return {a["asset_id"]: a for a in case["assets"]}


def _impact_to_requirement(value: str) -> str:
    value = (value or "").strip().lower()
    if value in {"critical", "high", "h"}:
        return "H"
    if value in {"medium", "m", "moderate"}:
        return "M"
    if value in {"low", "l"}:
        return "L"
    return "M"


def _scope_for_state(asset: Dict[str, str], state: str) -> str:
    return asset.get(f"pci_scope_{state}", asset.get("pci_scope", "unknown")).strip().lower()


def infer_environmental_metrics(case: Dict[str, Any], vuln: Dict[str, str], state: str) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
    assets = _asset_by_id(case)
    asset = assets[vuln["asset_id"]]
    evidence: List[Dict[str, str]] = []

    scope = _scope_for_state(asset, state)
    business = case["business_impact"].get("assets", {}).get(vuln["asset_id"], {})

    # Security requirements: explicit business impact overrides heuristic.
    cr = _impact_to_requirement(business.get("confidentiality", ""))
    ir = _impact_to_requirement(business.get("integrity", ""))
    ar = _impact_to_requirement(business.get("availability", ""))

    if not business:
        if scope == "in_scope":
            cr, ir, ar = "H", "H", "M"
        elif asset.get("role") == "segmentation_enforcement":
            cr, ir, ar = "M", "H", "H"
        else:
            cr, ir, ar = "L", "L", "M"

    evidence.append({
        "metric": "CR/IR/AR",
        "source": "business_impact.yaml + pci_scope.yaml + assets.csv",
        "reason": f"asset={asset['asset_id']} scope_{state}={scope} role={asset.get('role', '')}",
    })

    # Modified Attack Vector: derive basic exposure from firewall/topology.
    base = parse_vector(vuln["base_vector"])
    env: Dict[str, str] = {"CR": cr, "IR": ir, "AR": ar, "E": "X", "RL": "X", "RC": "X"}

    exposure_key = f"external_exposure_{state}"
    exposure = asset.get(exposure_key, asset.get("external_exposure", "unknown")).strip().lower()

    if base["AV"] == "N":
        if exposure in {"none", "internal_only"}:
            env["MAV"] = "A"
            evidence.append({
                "metric": "MAV",
                "source": "assets.csv + firewall_rules.yaml",
                "reason": f"base AV=N but {exposure_key}={exposure}; network attack constrained to adjacent/internal segment.",
            })
        else:
            env["MAV"] = "N"
    else:
        env["MAV"] = base["AV"]

    # Keep other modified base metrics explicit to help audit reproducibility.
    env["MAC"] = base["AC"]
    env["MPR"] = base["PR"]
    env["MUI"] = base["UI"]
    env["MS"] = base["S"]
    env["MC"] = base["C"]
    env["MI"] = base["I"]
    env["MA"] = base["A"]

    evidence.append({
        "metric": "ModifiedBaseDefaults",
        "source": "vulnerabilities.csv",
        "reason": "Unchanged modified metrics inherit base values unless local evidence overrides them.",
    })

    return env, evidence


def assess_case(case: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    expected = case.get("expected", {}).get("expected_labels", {})

    for vuln in case["vulnerabilities"]:
        base = parse_vector(vuln["base_vector"])
        bscore = base_score(base)
        for state in ["before", "after"]:
            env, evidence = infer_environmental_metrics(case, vuln, state)
            escore = environmental_score(base, env)
            evector = build_environmental_vector(vuln["base_vector"], env)
            key = f"{vuln['finding_id']}:{state}"
            exp = expected.get(key, {})
            matches_expected = None
            if exp:
                matches_expected = all(env.get(k) == exp.get(k) for k in ["CR", "IR", "AR"])

            rows.append({
                "finding_id": vuln["finding_id"],
                "asset_id": vuln["asset_id"],
                "cve": vuln["cve"],
                "vulnerability_type": vuln["vulnerability_type"],
                "state": state,
                "base_vector": vuln["base_vector"],
                "base_score": bscore,
                "environmental_vector": evector,
                "environmental_score": escore,
                "environmental_metrics": env,
                "evidence": evidence,
                "matches_expected_requirements": matches_expected,
            })

    return rows
