"""Compatibility adapter for the evidence-grounded CVSS v4.0 pipeline.

The former implementation applied hand-authored numeric deltas to a Base score.
That model is intentionally removed. This adapter now requires a CVSS v4.0 source
vector, obtains candidate metrics from ``AIEvidenceEngine``, and delegates numeric
calculation to ``core.cvss40``.
"""
from __future__ import annotations

from typing import Any, Dict

from core.ai_evidence_engine import AIEvidenceEngine
from core.cvss40 import compare


def calculate(row: Dict[str, Any]) -> Dict[str, Any]:
    source_vector = row.get("source_cvss_vector") or row.get("cvss_vector") or row.get("vector") or row.get("base_vector")
    if not source_vector:
        raise ValueError("A CVSS v4.0 source vector is required; numeric-only base_score input is no longer supported")
    if not str(source_vector).startswith("CVSS:4.0/"):
        raise ValueError("Only CVSS v4.0 source vectors are supported by the environmental engine")

    evidence = dict(row.get("evidence") or {})
    # Backward-compatible evidence fields may be placed at the top level.
    for key in (
        "evidence_quality", "telemetry_age_days", "telemetry_profile", "max_telemetry_age_days",
        "conflict_flag", "firewall_status", "routing_table_status", "reachability",
        "internet_exposed", "routed_ip_access", "l2_broadcast_only", "local_host_only",
        "physical_access_only", "evidenced_exploit_preconditions_elevated",
        "organization_policy_id", "policy_version", "security_requirements", "modified_impacts",
    ):
        if key in row and key not in evidence:
            evidence[key] = row[key]

    inference = AIEvidenceEngine().analyze_scenario(
        base_vector=str(source_vector),
        evidence=evidence,
        cve_id=row.get("cve_id") or row.get("cve"),
    )

    if inference["review_status"] == "HUMAN_REVIEW_REQUIRED":
        src = score(str(source_vector))
        return {
            "source_vector": src["vector"],
            "source_nomenclature": src["nomenclature"],
            "source_score": src["score"],
            "source_severity": src["severity"],
            "environmental_vector": None,
            "environmental_nomenclature": None,
            "environmental_score": None,
            "environmental_severity": None,
            "delta": None,
            "decision": "abstained",
            "review_status": inference["review_status"],
            "human_review_status": "required",
            "auto_downgrade_permitted": False,
            "candidate_metrics": {},
            "adjustment_trace": inference["citations"],
            "rationale": inference["summary_rationale"],
        }

    scoring = compare(str(source_vector), inference["candidate_metrics"])
    src = scoring["source_cvss"]
    ctx = scoring["candidate_cvss"]
    delta = scoring["delta"]
    return {
        "source_vector": src["vector"],
        "source_nomenclature": src["nomenclature"],
        "source_score": src["score"],
        "source_severity": src["severity"],
        "environmental_vector": ctx["vector"],
        "environmental_nomenclature": ctx["nomenclature"],
        "environmental_score": ctx["score"],
        "environmental_severity": ctx["severity"],
        "delta": delta,
        "decision": "downgraded" if delta < 0 else ("upgraded" if delta > 0 else "unchanged"),
        "review_status": inference["review_status"],
        "human_review_status": "required",
        "auto_downgrade_permitted": False,
        "candidate_metrics": inference["candidate_metrics"],
        "adjustment_trace": inference["citations"],
        "rationale": inference["summary_rationale"],
    }
