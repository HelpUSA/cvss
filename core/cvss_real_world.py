from core.cvss31 import official_cvss_output
from core.cvss_environmental_engine import calculate

def assess_finding(row):
    vector = row.get("cvss_vector") or row.get("vector")
    if not vector:
        raise ValueError("cvss_vector is required for real-world assessment")
    official = official_cvss_output(vector)["official_cvss"]
    contextual_input = dict(row)
    contextual_input["base_score"] = official["base_score"]
    raw = calculate(contextual_input)
    contextual = {
        "contextual_score": raw["environmental_score"],
        "contextual_severity": raw["environmental_severity"],
        "decision": raw["decision"],
        "delta_from_official_base": raw["delta"],
        "trace": raw["adjustment_trace"],
    }
    evidence = {
        "cve": row.get("cve"),
        "asset_id": row.get("asset_id"),
        "source_url": row.get("source_url"),
        "environment": row.get("environment"),
        "business_criticality": row.get("business_criticality"),
        "pci_in_scope": row.get("pci_in_scope"),
    }
    return {
        "official_cvss": official,
        "contextual_environmental": contextual,
        "evidence": evidence,
    }
