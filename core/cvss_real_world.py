"""Current-world HelpUS assessment wrapper (CVSS v4.0 only).

Historical CVSS v3.x datasets remain archival research inputs and must not be
silently converted into v4.0 assessments.
"""
from __future__ import annotations

from core.cvss_environmental_engine import calculate


def assess_finding(row):
    vector = row.get("source_cvss_vector") or row.get("cvss_vector") or row.get("vector")
    if not vector:
        raise ValueError("source_cvss_vector/cvss_vector/vector is required")
    if not str(vector).startswith("CVSS:4.0/"):
        raise ValueError("Current HelpUS environmental assessment requires a CVSS v4.0 source vector")
    payload = dict(row)
    payload["source_cvss_vector"] = vector
    result = calculate(payload)
    source_cvss = {
        "vector": result.get("source_vector"),
        "nomenclature": result.get("source_nomenclature"),
        "score": result.get("source_score"),
        "severity": result.get("source_severity"),
    }
    evidence_dict = dict(row.get("evidence") or {})
    if not evidence_dict:
        evidence_dict = {
            k: v for k, v in row.items()
            if k not in ("source_cvss_vector", "cvss_vector", "vector")
        }
    return {
        "source_cvss": source_cvss,
        "official_cvss": source_cvss,  # deprecated compatibility alias
        "contextual_environmental": {
            "vector": result.get("environmental_vector"),
            "nomenclature": result.get("environmental_nomenclature"),
            "score": result.get("environmental_score"),
            "severity": result.get("environmental_severity"),
            "decision": result.get("decision"),
            "delta_from_source": result.get("delta"),
            "review_status": result.get("review_status"),
            "auto_downgrade_permitted": result.get("auto_downgrade_permitted", False),
            "trace": result.get("adjustment_trace", []),
        },
        "evidence": evidence_dict,
    }

