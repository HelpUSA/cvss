"""Load structured case-study files."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List, Any

import yaml


def load_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def load_case(case_dir: str | Path) -> Dict[str, Any]:
    root = Path(case_dir)
    return {
        "root": root,
        "assets": load_csv(root / "assets.csv"),
        "vulnerabilities": load_csv(root / "vulnerabilities.csv"),
        "topology": load_yaml(root / "topology.yaml"),
        "firewall_rules": load_yaml(root / "firewall_rules.yaml"),
        "business_impact": load_yaml(root / "business_impact.yaml"),
        "pci_scope": load_yaml(root / "pci_scope.yaml"),
        "expected": load_yaml(root / "expected_expert_labels.yaml"),
    }
