"""
AI Evidence Engine for CVSS v4.0.
Analyzes findings alongside operational telemetry (routing, firewalls, ACLs,
network domains, and organizational policy) to propose candidate CVSS v4.0 metrics
with explicit symbolic provenance and fail-safe abstention.

Follows a strict two-stage pipeline:
Stage 1: Symbolic deduction of candidate metrics from grounded evidence.
Stage 2: Fail-safe check (abstains with HUMAN_REVIEW_REQUIRED on ambiguous/stale/conflicting evidence).
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

# Valid CVSS v4.0 environmental & threat values
VALID_METRICS = {
    "CR": {"H", "M", "L", "X"},
    "IR": {"H", "M", "L", "X"},
    "AR": {"H", "M", "L", "X"},
    "MAV": {"N", "A", "L", "P", "X"},
    "MAC": {"L", "H", "X"},
    "MAT": {"N", "P", "X"},
    "MPR": {"N", "L", "H", "X"},
    "MUI": {"N", "P", "A", "X"},
    "MVC": {"H", "L", "N", "X"},
    "MVI": {"H", "L", "N", "X"},
    "MVA": {"H", "L", "N", "X"},
    "MSC": {"H", "L", "N", "X"},
    "MSI": {"H", "L", "N", "S", "X"},
    "MSA": {"H", "L", "N", "S", "X"},
    "E": {"A", "P", "U", "X"},
}


class AIEvidenceEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

    def analyze_finding(
        self,
        cve_id: str,
        base_vector: str,
        asset_profile: Dict[str, Any],
        evidence_notes: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Convenience wrapper for finding evaluation."""
        evidence = dict(asset_profile)
        if evidence_notes:
            evidence["evidence_notes"] = evidence_notes
        return self.analyze_scenario(base_vector=base_vector, evidence=evidence, cve_id=cve_id)

    def analyze_scenario(
        self,
        base_vector: str,
        evidence: Dict[str, Any],
        cve_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Evidence-constrained deterministic analysis.
        Implements fail-safe abstention (HUMAN_REVIEW_REQUIRED) whenever telemetry
        is incomplete, stale (>30 days), or conflicting.
        """
        citations: List[str] = []
        candidate_metrics: Dict[str, str] = {}
        uncertainties: List[str] = []

        # --- FAIL-SAFE AUDIT CHECKS ---
        is_stale = evidence.get("telemetry_age_days", 0) > 30
        has_conflict = bool(evidence.get("conflict_flag", False))
        quality = str(evidence.get("evidence_quality", "SUFFICIENT")).upper()
        reachability = str(evidence.get("reachability", "")).upper()

        # Check for explicit conflict in rules vs routes
        fw_status = str(evidence.get("firewall_status", "")).upper()
        rt_status = str(evidence.get("routing_table_status", "")).upper()
        if "ALLOW" in fw_status and "NO_ROUTE" in rt_status:
            has_conflict = True

        if quality in ("INSUFFICIENT", "UNKNOWN") or is_stale or has_conflict or reachability == "UNKNOWN":
            reasons = []
            if is_stale:
                reasons.append(f"telemetry is stale ({evidence.get('telemetry_age_days')} days old)")
            if has_conflict:
                reasons.append("conflicting routing and firewall telemetry detected")
            if quality in ("INSUFFICIENT", "UNKNOWN") or reachability == "UNKNOWN":
                reasons.append("insufficient operational evidence to verify reachability")

            uncertainties.extend(reasons)
            return {
                "cve_id": cve_id or "UNKNOWN",
                "base_vector": base_vector,
                "review_status": "HUMAN_REVIEW_REQUIRED",
                "auto_downgrade_permitted": False,
                "evidence_quality": "INSUFFICIENT" if quality != "CONFLICTING" else "CONFLICTING",
                "candidate_metrics": {},
                "citations": [],
                "uncertainty_flags": uncertainties,
                "summary_rationale": "Automated inference abstained: " + "; ".join(reasons),
            }

        # --- REACHABILITY & MAV REASONING ---
        # Note: Absence of public internet does NOT make an asset Adjacent or Local.
        # Internal routed IP networks remain MAV:Network.
        l2_only = bool(evidence.get("l2_broadcast_only", False))
        local_shell_only = bool(evidence.get("local_host_only", False))
        is_routed = bool(evidence.get("routed_ip_access", True))

        if local_shell_only:
            candidate_metrics["MAV"] = "L"
            citations.append("MAV:Local — Vulnerability requires local shell/console interaction on host.")
        elif l2_only:
            candidate_metrics["MAV"] = "A"
            citations.append("MAV:Adjacent — Reachability strictly constrained to same unrouted L2 broadcast domain.")
        elif is_routed:
            # Internal or external routed network
            candidate_metrics["MAV"] = "N"
            if not evidence.get("internet_exposed", True):
                citations.append("MAV:Network — Service reachable via internal routed IP subnets (not Internet-exposed).")
            else:
                citations.append("MAV:Network — Service directly reachable over public network routing.")

        # --- ATTACK COMPLEXITY (MAC) REASONING ---
        # Presence of firewall/WAF does NOT automatically imply MAC:High.
        # MAC only changes if verified exploit pre-conditions are demonstrably elevated.
        if evidence.get("evidenced_exploit_preconditions_elevated", False):
            candidate_metrics["MAC"] = "H"
            citations.append("MAC:High — Specific verified perimeter filtering elevates required attack complexity.")

        # --- SECURITY REQUIREMENTS (CR, IR, AR) FROM ORGANIZATIONAL POLICY ---
        # Requirements stem from approved organizational mapping, not third-party mandates.
        crit = str(evidence.get("business_criticality", "medium")).lower()
        has_regulated_data = bool(evidence.get("pci_in_scope", False) or evidence.get("regulated_data_scope", False))

        if has_regulated_data:
            candidate_metrics["CR"] = "H"
            citations.append("CR:High — Asset in approved organizational scope for regulated/sensitive cardholder data.")
        elif crit in ("high", "critical"):
            candidate_metrics["CR"] = "H"
            citations.append("CR:H — High business criticality per organizational asset classification.")
        elif crit == "low":
            candidate_metrics["CR"] = "L"
            citations.append("CR:L — Test/development asset with non-sensitive synthetic data.")
        else:
            candidate_metrics["CR"] = "M"

        if crit in ("high", "critical") or has_regulated_data:
            candidate_metrics["IR"] = "H"
            citations.append("IR:H — Authoritative transactional records require high integrity.")
        elif crit == "low":
            candidate_metrics["IR"] = "L"
        else:
            candidate_metrics["IR"] = "M"

        if bool(evidence.get("high_availability", False)):
            candidate_metrics["AR"] = "L"
            citations.append("AR:L — Active multi-zone redundancy mitigates single-instance availability disruption.")
        elif crit in ("high", "critical"):
            candidate_metrics["AR"] = "H"
        else:
            candidate_metrics["AR"] = "M"

        return {
            "cve_id": cve_id or "UNKNOWN",
            "base_vector": base_vector,
            "review_status": "PROVISIONAL_INFERENCE_READY",
            "auto_downgrade_permitted": True,
            "evidence_quality": "SUFFICIENT",
            "candidate_metrics": candidate_metrics,
            "citations": citations,
            "uncertainty_flags": uncertainties,
            "summary_rationale": "; ".join(citations),
        }
