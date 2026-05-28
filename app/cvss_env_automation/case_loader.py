"""Load structured case-study files."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List

import yaml


def load_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def _legacy_vulnerabilities(root: Path) -> List[Dict[str, str]]:
    legacy = root / "vulnerability_findings.csv"
    rows = load_csv(legacy)
    normalized: List[Dict[str, str]] = []
    for idx, row in enumerate(rows, start=1):
        finding_id = row.get("finding_id") or row.get("id") or f"F-{idx:03d}"
        asset_id = row.get("asset_id") or row.get("asset") or row.get("host") or "UNKNOWN-ASSET"
        cve = row.get("cve") or row.get("CVE") or "CVE-UNKNOWN"
        vuln_type = row.get("vulnerability_type") or row.get("type") or row.get("category") or "SYS"
        base_vector = row.get("base_vector") or row.get("cvss_vector") or row.get("vector") or "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H"
        description = row.get("description") or row.get("summary") or row.get("title") or "Legacy vulnerability finding"
        normalized.append({
            "finding_id": finding_id,
            "asset_id": asset_id,
            "cve": cve,
            "software": row.get("software") or row.get("product") or "Legacy system",
            "vulnerability_type": vuln_type,
            "base_vector": base_vector,
            "description": description,
        })
    return normalized


def _load_vulnerabilities(root: Path) -> List[Dict[str, str]]:
    current = root / "vulnerabilities.csv"
    if current.exists():
        return load_csv(current)
    legacy = root / "vulnerability_findings.csv"
    if legacy.exists():
        return _legacy_vulnerabilities(root)
    raise FileNotFoundError(f"No vulnerabilities.csv or vulnerability_findings.csv found in {root}")


def load_case(case_dir: str | Path) -> Dict[str, Any]:
    root = Path(case_dir)
    return {
        "root": root,
        "assets": load_csv(root / "assets.csv"),
        "vulnerabilities": _load_vulnerabilities(root),
        "topology": load_yaml(root / "topology.yaml"),
        "firewall_rules": load_yaml(root / "firewall_rules.yaml"),
        "business_impact": load_yaml(root / "business_impact.yaml"),
        "pci_scope": load_yaml(root / "pci_scope.yaml"),
        "expected": load_yaml(root / "expected_expert_labels.yaml"),
    }
