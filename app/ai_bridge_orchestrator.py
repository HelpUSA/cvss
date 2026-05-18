#!/usr/bin/env python3
"""
AI Bridge Orchestrator for CVSS Environmental Assessment.
Uses the Watcher to collect evidence and compute environmental scores.
"""
import json
import csv
from pathlib import Path

WORKSPACE = Path("D:/dev/cvss")

class EnvironmentalScorer:
    """Simplified CVSS environmental score calculator."""

    @staticmethod
    def modified_attack_vector(asset_info: dict) -> str:
        """Determine MAV based on segmentation."""
        if asset_info.get("segmented", False):
            return "Adjacent"
        if asset_info.get("exposed_to_internet", False):
            return "Network"
        return "Local"

    @staticmethod
    def requirements(asset_info: dict) -> dict:
        """Return IR, IR, AR based on asset criticality."""
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
    evidence = {}
    assets_csv = case_dir / "assets.csv"
    if assets_csv.exists():
        with open(assets_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            evidence['assets'] = list(reader)
    vuln_csv = case_dir / "vulnerability_findings.csv"
    if vuln_csv.exists():
        with open(vuln_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            evidence['vulnerabilities'] = list(reader)
    return evidence

def main():
    """Main orchestration logic."""
    case_dir = WORKSPACE / "cases" / "pci_demo"
    if not case_dir.exists():
        print("Case directory not found. Creating it...")
        case_dir.mkdir(parents=True)
    print("Collecting evidence...")
    evidence = load_case_study(case_dir)
    if 'vulnerabilities' not in evidence:
        print("Error: No vulnerability findings found.")
        return
    results = []
    for row in evidence['vulnerabilities']:
        asset_id = row['asset_id']
        base_score = float(row['base_score'])
        asset_info = next((a for a in evidence.get('assets', []) if a['asset_id'] == asset_id), None)
        if not asset_info:
            print(f"Warning: Asset {{asset_id}} not found")
            continue
        mav = EnvironmentalScorer.modified_attack_vector(asset_info)
        req = EnvironmentalScorer.requirements(asset_info)
        env_score = EnvironmentalScorer.compute_score(
            base_score=base_score, mav=mav,
            cr=req['CR'], ir=req['IR'], ar=req['AR']
        )
        results.append({
            "finding_id": row['finding_id'], "asset_id": asset_id,
            "cve": row['cve'], "base_score": base_score,
            "environmental_score": env_score, "mav": mav,
            "cr": req['CR'], "ir": req['IR'], "ar": req['AR']
        })
    output_dir = WORKSPACE / "outputs" / "demo_run"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "assessments.json").write_text(json.dumps(results, indent=2))
    with open(output_dir / "summary.csv", 'w', newline='') as f:
        fields = ["finding_id", "asset_id", "cve", "base_score",
                    "environmental_score", "mav", "cr", "ir", "ar"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
    print(f"Assessment completed. Results in {output_dir}")

if __name__ == "__main__":
    main()
