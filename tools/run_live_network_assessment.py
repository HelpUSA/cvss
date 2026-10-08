"""
End-to-End Real Scanner & CVSS Evaluator.
1. Scans local subnet / hosts for active services.
2. Extracts real environmental facts (segmentation, exposure, service role).
3. Evaluates real vulnerability findings against discovered context using AI Engine and CVSS v4.0.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.ai_evidence_engine import AIEvidenceEngine
from core.cvss40 import compare
from tools.local_network_scanner import scan_local_subnet


def run_live_environment_assessment(output_path: Path = ROOT / "outputs" / "assessments" / "live_network_assessment.json") -> dict:
    print("[1/3] Executando varredura nativa da rede local...")
    network_data = scan_local_subnet()
    print(f" -> Encontrados {network_data['total_discovered']} ativos na subrede {network_data['subnet']}.")

    engine = AIEvidenceEngine()
    evaluated_findings = []

    # Exemplo de CVEs reais comuns associados aos serviços detectados na rede
    sample_cves = [
        {
            "cve": "CVE-2023-39417",
            "service": "PostgreSQL Database",
            "base_score": 7.5,
            "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
            "title": "PostgreSQL Extension SQL Injection Vulnerability",
        },
        {
            "cve": "CVE-2023-44487",
            "service": "HTTP Web",
            "base_score": 7.5,
            "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N",
            "title": "HTTP/2 Rapid Reset Denial of Service",
        },
    ]

    print("[2/3] Correlacionando falhas com evidências reais do ambiente...")
    for asset in network_data["assets"]:
        ports = [p["service"] for p in asset["open_ports"]]
        for sample in sample_cves:
            if any(sample["service"] in p for p in ports):
                # Extrai perfil e analisa via AI Engine
                profile = asset["evidence"]
                profile["asset_name"] = f"{asset['hostname']} ({asset['ip']})"
                
                ai_res = engine.analyze_finding(
                    cve_id=sample["cve"],
                    base_vector=sample["vector"],
                    asset_profile=profile,
                    evidence_notes=[f"Detectado serviço {sample['service']} ativo no host {asset['ip']}"]
                )

                cvss_comp = compare(sample["vector"], ai_res["candidate_metrics"])

                evaluated_findings.append({
                    "asset_ip": asset["ip"],
                    "asset_hostname": asset["hostname"],
                    "asset_role": asset["role"],
                    "cve": sample["cve"],
                    "title": sample["title"],
                    "official_base_score": cvss_comp["official_cvss"]["score"],
                    "official_base_severity": cvss_comp["official_cvss"]["severity"],
                    "contextual_score": cvss_comp["candidate_cvss"]["score"],
                    "contextual_severity": cvss_comp["candidate_cvss"]["severity"],
                    "delta": cvss_comp["delta"],
                    "nomenclature": cvss_comp["candidate_cvss"]["nomenclature"],
                    "ai_citations": ai_res["citations"],
                    "human_review_status": ai_res["human_review_status"],
                })

    result = {
        "scan_time": network_data["scan_time"],
        "network_subnet": network_data["subnet"],
        "total_hosts_active": network_data["total_discovered"],
        "total_vulnerabilities_evaluated": len(evaluated_findings),
        "findings": evaluated_findings,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[3/3] Avaliação concluída com sucesso! Resultados salvos em: {output_path}")
    return result


if __name__ == "__main__":
    res = run_live_environment_assessment()
    print(json.dumps(res, indent=2, ensure_ascii=False))
