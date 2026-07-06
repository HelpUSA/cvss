import argparse
import json
import subprocess
from pathlib import Path

SEV_SCORE = {"CRITICAL": 9.5, "HIGH": 7.5, "MEDIUM": 5.0, "LOW": 2.5, "UNKNOWN": 0.0}

def severity_from_score(score):
    if score >= 9.0:
        return "Critical"
    if score >= 7.0:
        return "High"
    if score >= 4.0:
        return "Medium"
    if score > 0:
        return "Low"
    return "None"

def decision_from_score(score):
    if score >= 9.0:
        return "immediate_action"
    if score >= 7.0:
        return "prioritize_next_patch_window"
    if score >= 4.0:
        return "schedule_standard_remediation"
    if score > 0:
        return "monitor_or_bundle_with_next_change"
    return "informational"

def parse_bool(value):
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"invalid boolean value: {value}")

def official_cvss(vuln):
    cvss = vuln.get("CVSS") or {}
    for source in ["nvd", "ghsa", "redhat", "vendor"]:
        entry = cvss.get(source)
        if isinstance(entry, dict) and entry.get("V3Score") is not None:
            score = float(entry["V3Score"])
            return {
                "source": source,
                "base_score": score,
                "base_severity": severity_from_score(score),
                "vector": entry.get("V3Vector"),
            }
    raw = str(vuln.get("Severity") or "UNKNOWN").upper()
    score = SEV_SCORE.get(raw, 0.0)
    return {
        "source": "trivy_severity_fallback",
        "base_score": score,
        "base_severity": raw.title(),
        "vector": None,
    }

def contextualize(official, vuln, asset):
    base = float(official.get("base_score") or 0.0)
    delta = 0.0
    rationale = []

    if asset["internet_exposed"]:
        delta += 0.8
        rationale.append("asset is internet exposed")
    else:
        rationale.append("asset is not marked as internet exposed")

    if asset["environment"] == "production":
        delta += 0.6
        rationale.append("asset is production")
    elif asset["environment"] in ("development", "dev", "test") and not asset["internet_exposed"]:
        delta -= 0.4
        rationale.append("non-exposed non-production asset lowers urgency")

    if asset["business_criticality"] == "critical":
        delta += 1.0
        rationale.append("business criticality is critical")
    elif asset["business_criticality"] == "high":
        delta += 0.7
        rationale.append("business criticality is high")
    elif asset["business_criticality"] == "medium":
        delta += 0.2
        rationale.append("business criticality is medium")
    elif asset["business_criticality"] == "low":
        delta -= 0.1
        rationale.append("business criticality is low")

    if asset["data_sensitivity"] in ("pii", "phi", "payment", "credentials", "secrets"):
        delta += 0.5
        rationale.append("asset may process sensitive data")
    elif asset["data_sensitivity"] == "public":
        delta -= 0.1
        rationale.append("data sensitivity is public")

    if not vuln.get("FixedVersion"):
        delta += 0.2
        rationale.append("scanner did not provide a fixed version")

    score = round(max(0.0, min(10.0, base + delta)), 1)
    return {
        "score": score,
        "severity": severity_from_score(score),
        "decision": decision_from_score(score),
        "delta_from_official_base": round(score - base, 1),
        "rationale": rationale,
        "method": "mvp_static_context_heuristic_v1",
        "not_official_cvss": True,
    }

def iter_trivy_vulns(raw):
    for result in raw.get("Results") or []:
        target = result.get("Target")
        rtype = result.get("Type")
        for vuln in result.get("Vulnerabilities") or []:
            item = dict(vuln)
            item["_target"] = target
            item["_type"] = rtype
            yield item

def normalize(raw, asset, source_file):
    findings = []
    for index, vuln in enumerate(iter_trivy_vulns(raw), start=1):
        official = official_cvss(vuln)
        contextual = contextualize(official, vuln, asset)
        vuln_id = vuln.get("VulnerabilityID") or f"TRIVY-{index}"
        findings.append({
            "id": f"{asset['id']}:{vuln_id}:{index}",
            "asset": asset,
            "vulnerability": {
                "id": vuln_id,
                "title": vuln.get("Title"),
                "package": vuln.get("PkgName"),
                "installed_version": vuln.get("InstalledVersion"),
                "fixed_version": vuln.get("FixedVersion"),
                "severity": vuln.get("Severity"),
                "primary_url": vuln.get("PrimaryURL"),
                "references": vuln.get("References") or [],
            },
            "official_cvss": official,
            "contextual_environmental": contextual,
            "evidence": {
                "scanner": "trivy",
                "source_file": source_file,
                "target": vuln.get("_target"),
                "type": vuln.get("_type"),
                "raw_severity": vuln.get("Severity"),
                "description": vuln.get("Description"),
            },
        })

    def count(name):
        return sum(1 for finding in findings if finding["contextual_environmental"]["severity"] == name)

    return {
        "schema": "helpus.cvss.real_assessment",
        "schema_version": 1,
        "scanner": "trivy",
        "asset": asset,
        "summary": {
            "finding_count": len(findings),
            "critical": count("Critical"),
            "high": count("High"),
            "medium": count("Medium"),
            "low": count("Low"),
        },
        "findings": findings,
    }

def run_trivy(target, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["trivy", "fs", "--format", "json", "--output", str(output_path), target], check=True)
    return output_path

def build_asset(args):
    return {
        "id": args.asset_id,
        "name": args.asset_name,
        "environment": args.environment.lower(),
        "internet_exposed": args.internet_exposed,
        "business_criticality": args.business_criticality.lower(),
        "data_sensitivity": args.data_sensitivity.lower(),
        "owner": args.owner,
    }

def main():
    parser = argparse.ArgumentParser(description="Run a real-environment CVSS assessment")
    parser.add_argument("--scanner", choices=["trivy"], required=True)
    parser.add_argument("--target", default=".")
    parser.add_argument("--input")
    parser.add_argument("--output", default="outputs/assessments/latest_assessment.json")
    parser.add_argument("--raw-output", default="outputs/scans/trivy_latest.json")
    parser.add_argument("--asset-id", default="local-repository")
    parser.add_argument("--asset-name", default="Local Repository")
    parser.add_argument("--environment", default="development")
    parser.add_argument("--internet-exposed", type=parse_bool, default=False)
    parser.add_argument("--business-criticality", default="medium")
    parser.add_argument("--data-sensitivity", default="internal")
    parser.add_argument("--owner", default="engineering")
    args = parser.parse_args()

    asset = build_asset(args)
    if args.input:
        input_path = Path(args.input)
    else:
        input_path = run_trivy(args.target, Path(args.raw_output))

    raw = json.loads(input_path.read_text(encoding="utf-8"))
    assessment = normalize(raw, asset, str(input_path))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(assessment, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary = assessment["summary"]
    print("REAL_ASSESSMENT_OUTPUT", output_path)
    print("REAL_ASSESSMENT_FINDINGS", summary["finding_count"])
    print("REAL_ASSESSMENT_CRITICAL", summary["critical"])
    print("REAL_ASSESSMENT_HIGH", summary["high"])
    print("REAL_ASSESSMENT_MEDIUM", summary["medium"])
    print("REAL_ASSESSMENT_LOW", summary["low"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
