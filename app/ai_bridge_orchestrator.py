#!/usr/bin/env python3
"""
AI Bridge Orchestrator for CVSS Environmental Assessment.
Uses the Watcher to collect evidence and compute environmental scores.
"""
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from cvss_env_automation.reporting import write_outputs
except ModuleNotFoundError:  # Allows importing as app.ai_bridge_orchestrator in tests.
    from app.cvss_env_automation.reporting import write_outputs


WORKSPACE = Path("D:/dev/cvss")


def _truthy(value: Any) -> bool:
    """Return a safe bool for CSV values such as true/false/yes/no/1/0."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _optional_bool(value: Any) -> Optional[bool]:
    """Parse an optional CSV boolean while preserving missing values as None."""
    if value in (None, ""):
        return None
    return _truthy(value)


def _severity_from_score(score: Optional[float]) -> Optional[str]:
    """Return CVSS v3.x severity label for a numeric score."""
    if score is None:
        return None
    if score >= 9.0:
        return "Critical"
    if score >= 7.0:
        return "High"
    if score >= 4.0:
        return "Medium"
    if score > 0.0:
        return "Low"
    return "None"


def _decision_from_delta(delta: float) -> str:
    """Describe whether contextual scoring changed the official base score."""
    if delta > 0:
        return "upgraded"
    if delta < 0:
        return "lowered"
    return "unchanged"


class EnvironmentalScorer:
    """Simplified CVSS environmental score calculator."""

    @staticmethod
    def modified_attack_vector(asset_info: dict) -> str:
        """Determine MAV based on segmentation."""
        if _truthy(asset_info.get("segmented", False)):
            return "Adjacent"
        if _truthy(asset_info.get("exposed_to_internet", False)):
            return "Network"
        return "Local"

    @staticmethod
    def requirements(asset_info: dict) -> dict:
        """Return CR, IR, AR based on asset criticality."""
        return {
            "CR": asset_info.get("cr", "Medium"),
            "IR": asset_info.get("ir", "Medium"),
            "AR": asset_info.get("ar", "Medium"),
        }

    @staticmethod
    def compute_score(base_score: float, mav: str, cr: str, ir: str, ar: str) -> float:
        """Simplified environmental score calculation."""
        if mav == "Adjacent" and cr == "Medium":
            return round(base_score - 0.8, 1)
        return round(base_score, 1)


def load_case_study(case_dir: Path) -> dict:
    """Load all evidence files from case study."""
    evidence: Dict[str, List[Dict[str, str]]] = {}

    assets_csv = case_dir / "assets.csv"
    if assets_csv.exists():
        with assets_csv.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            evidence["assets"] = list(reader)

    vuln_csv = case_dir / "vulnerability_findings.csv"
    if vuln_csv.exists():
        with vuln_csv.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            evidence["vulnerabilities"] = list(reader)

    return evidence


def build_assessment_rows(evidence: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Build report rows with legacy, official CVSS, and contextual layers."""
    results: List[Dict[str, Any]] = []
    assets = evidence.get("assets", [])

    for row in evidence.get("vulnerabilities", []):
        asset_id = row.get("asset_id")
        base_score = float(row.get("base_score", 0.0))
        asset_info = next((a for a in assets if a.get("asset_id") == asset_id), None)
        if not asset_info:
            print(f"Warning: Asset {asset_id} not found")
            continue

        mav = EnvironmentalScorer.modified_attack_vector(asset_info)
        req = EnvironmentalScorer.requirements(asset_info)
        env_score = EnvironmentalScorer.compute_score(
            base_score=base_score,
            mav=mav,
            cr=req["CR"],
            ir=req["IR"],
            ar=req["AR"],
        )
        delta = round(env_score - base_score, 1)

        results.append({
            "finding_id": row.get("finding_id"),
            "asset_id": asset_id,
            "cve": row.get("cve"),
            "vulnerability_type": row.get("vulnerability_type", row.get("type", "unknown")),
            "state": row.get("state", "open"),
            "base_score": base_score,
            "environmental_score": env_score,
            "environmental_metrics": {
                "CR": req["CR"],
                "IR": req["IR"],
                "AR": req["AR"],
                "MAV": mav,
            },
            "mav": mav,
            "cr": req["CR"],
            "ir": req["IR"],
            "ar": req["AR"],
            "matches_expected_requirements": _optional_bool(
                row.get("matches_expected_requirements")
            ),
            "official_cvss": {
                "base_score": base_score,
                "base_severity": _severity_from_score(base_score),
            },
            "contextual_environmental": {
                "contextual_score": env_score,
                "contextual_severity": _severity_from_score(env_score),
                "decision": _decision_from_delta(delta),
                "delta_from_official_base": delta,
            },
            "evidence": {
                "finding": row,
                "asset": asset_info,
            },
        })

    return results


def main():
    """Main orchestration logic."""
    case_dir = WORKSPACE / "cases" / "pci_demo"
    if not case_dir.exists():
        print("Case directory not found. Creating it...")
        case_dir.mkdir(parents=True)

    print("Collecting evidence...")
    evidence = load_case_study(case_dir)
    if "vulnerabilities" not in evidence:
        print("Error: No vulnerability findings found.")
        return

    results = build_assessment_rows(evidence)

    output_dir = WORKSPACE / "outputs" / "demo_run"
    write_outputs(results, output_dir)
    print(f"Assessment completed. Results in {output_dir}")


if __name__ == "__main__":
    main()
