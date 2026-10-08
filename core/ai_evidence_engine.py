"""Evidence-constrained candidate-metric inference for CVSS v4.0.

This module does not calculate CVSS scores. It proposes candidate Threat/
Environmental metrics from explicit evidence and applies a conservative
fail-safe policy. Numerical scoring is delegated to ``core.cvss40``.

Research-safety invariants
--------------------------
* Missing, stale, unknown, or conflicting reachability evidence -> abstain.
* Internal routed reachability remains MAV:N; lack of Internet exposure is not
  evidence of MAV:A or MAV:L.
* Firewall/WAF presence alone never implies MAC:H.
* CR/IR/AR are accepted only from an explicit, versioned organizational-policy
  mapping. Regulatory scope is evidence to that policy, not a CVSS value.
* High availability/redundancy never implies AR:L. If a deployment has an
  approved Modified Availability Impact mapping, it may explicitly provide MVA.
* Candidate metrics always require HITL review before operational action;
  automatic downgrade is disabled by default.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Mapping, Optional

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

_DYNAMIC_MAX_AGE_DAYS = 1.0
_STATIC_MAX_AGE_DAYS = 7.0


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
        evidence = dict(asset_profile)
        if evidence_notes:
            evidence["evidence_notes"] = evidence_notes
        return self.analyze_scenario(base_vector=base_vector, evidence=evidence, cve_id=cve_id)

    @staticmethod
    def _freshness_limit(evidence: Mapping[str, Any]) -> float:
        if evidence.get("max_telemetry_age_days") is not None:
            return float(evidence["max_telemetry_age_days"])
        profile = str(evidence.get("telemetry_profile", "dynamic")).lower()
        return _STATIC_MAX_AGE_DAYS if profile == "static" else _DYNAMIC_MAX_AGE_DAYS

    @staticmethod
    def _validated_mapping(
        mapping: Any, allowed_names: set[str], citations: List[str], label: str
    ) -> Dict[str, str]:
        if not isinstance(mapping, Mapping):
            return {}
        out: Dict[str, str] = {}
        for name, value in mapping.items():
            name = str(name).upper()
            value = str(value).upper()
            if name not in allowed_names:
                continue
            if value not in VALID_METRICS[name] or value == "X":
                continue
            out[name] = value
        if out:
            citations.append(label)
        return out

    def _abstain(
        self,
        *,
        cve_id: Optional[str],
        base_vector: str,
        reasons: List[str],
        evidence_quality: str,
    ) -> Dict[str, Any]:
        return {
            "cve_id": cve_id or "UNKNOWN",
            "base_vector": base_vector,
            "review_status": "HUMAN_REVIEW_REQUIRED",
            "human_review_status": "required",
            "auto_downgrade_permitted": False,
            "evidence_quality": evidence_quality,
            "candidate_metrics": {},
            "citations": [],
            "uncertainty_flags": reasons,
            "summary_rationale": "Automated inference abstained: " + "; ".join(reasons),
        }

    def analyze_scenario(
        self,
        base_vector: str,
        evidence: Dict[str, Any],
        cve_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return candidate metrics or a fail-safe abstention decision."""
        citations: List[str] = []
        candidate_metrics: Dict[str, str] = {}
        reasons: List[str] = []

        quality = str(evidence.get("evidence_quality", "UNKNOWN")).upper()
        reachability = str(evidence.get("reachability", "UNKNOWN")).upper()
        explicit_conflict = bool(evidence.get("conflict_flag", False))
        fw_status = str(evidence.get("firewall_status", "")).upper()
        rt_status = str(evidence.get("routing_table_status", "")).upper()
        if "ALLOW" in fw_status and "NO_ROUTE" in rt_status:
            explicit_conflict = True

        age = evidence.get("telemetry_age_days")
        if age is None:
            reasons.append("telemetry age is missing")
        else:
            try:
                limit = self._freshness_limit(evidence)
                if float(age) > limit:
                    reasons.append(f"telemetry is stale ({age} days; policy limit {limit:g})")
            except (TypeError, ValueError):
                reasons.append("telemetry age is invalid")

        if quality in {"INSUFFICIENT", "UNKNOWN", "CONFLICTING"}:
            reasons.append(f"evidence quality is {quality}")
        if explicit_conflict:
            reasons.append("conflicting routing/firewall evidence detected")

        # A reachability class must be explicit. Legacy booleans are accepted only
        # when they determine one unambiguous class.
        allowed_reachability = {
            "PUBLIC_ROUTED",
            "INTERNAL_ROUTED",
            "ADJACENT_ONLY",
            "LOCAL_ONLY",
            "PHYSICAL_ONLY",
        }
        if reachability not in allowed_reachability:
            legacy_flags = {
                "LOCAL_ONLY": bool(evidence.get("local_host_only", False)),
                "ADJACENT_ONLY": bool(evidence.get("l2_broadcast_only", False)),
                "INTERNAL_ROUTED": bool(evidence.get("routed_ip_access", False))
                and not bool(evidence.get("internet_exposed", False)),
                "PUBLIC_ROUTED": bool(evidence.get("routed_ip_access", False))
                and bool(evidence.get("internet_exposed", False)),
                "PHYSICAL_ONLY": bool(evidence.get("physical_access_only", False)),
            }
            active = [name for name, enabled in legacy_flags.items() if enabled]
            if len(active) == 1:
                reachability = active[0]
            elif len(active) > 1:
                reasons.append("legacy reachability flags are conflicting")
            else:
                reasons.append("reachability is missing or unknown")

        if reasons:
            out_quality = "CONFLICTING" if quality == "CONFLICTING" or explicit_conflict else "INSUFFICIENT"
            return self._abstain(
                cve_id=cve_id,
                base_vector=base_vector,
                reasons=reasons,
                evidence_quality=out_quality,
            )

        reachability_to_mav = {
            "PUBLIC_ROUTED": "N",
            "INTERNAL_ROUTED": "N",
            "ADJACENT_ONLY": "A",
            "LOCAL_ONLY": "L",
            "PHYSICAL_ONLY": "P",
        }
        candidate_metrics["MAV"] = reachability_to_mav[reachability]
        citations.append(f"MAV:{candidate_metrics['MAV']} - verified reachability class {reachability}.")

        # MAC may change only with exploit-specific evidence.
        if evidence.get("evidenced_exploit_preconditions_elevated") is True:
            candidate_metrics["MAC"] = "H"
            citations.append("MAC:H - exploit-specific preconditions are explicitly evidenced; firewall presence alone was not used.")

        # Organizational requirements must be an explicit versioned mapping.
        policy_id = evidence.get("organization_policy_id")
        policy_version = evidence.get("policy_version")
        reqs = evidence.get("security_requirements")
        if reqs:
            if not policy_id or not policy_version:
                return self._abstain(
                    cve_id=cve_id,
                    base_vector=base_vector,
                    reasons=["security requirements supplied without organization_policy_id and policy_version"],
                    evidence_quality="INSUFFICIENT",
                )
            candidate_metrics.update(
                self._validated_mapping(
                    reqs,
                    {"CR", "IR", "AR"},
                    citations,
                    f"CR/IR/AR - derived from organizational policy {policy_id} version {policy_version}.",
                )
            )

        # Explicit approved Modified Impact mappings are distinct from Requirements.
        impacts = evidence.get("modified_impacts")
        if impacts:
            if not policy_id or not policy_version:
                return self._abstain(
                    cve_id=cve_id,
                    base_vector=base_vector,
                    reasons=["modified impacts supplied without organization_policy_id and policy_version"],
                    evidence_quality="INSUFFICIENT",
                )
            candidate_metrics.update(
                self._validated_mapping(
                    impacts,
                    {"MVC", "MVI", "MVA", "MSC", "MSI", "MSA"},
                    citations,
                    f"Modified impacts - derived from organizational policy {policy_id} version {policy_version}.",
                )
            )

        return {
            "cve_id": cve_id or "UNKNOWN",
            "base_vector": base_vector,
            "review_status": "PROVISIONAL_INFERENCE_READY",
            "human_review_status": "required",
            "auto_downgrade_permitted": False,
            "evidence_quality": "SUFFICIENT",
            "reachability_class": reachability,
            "candidate_metrics": candidate_metrics,
            "citations": citations,
            "uncertainty_flags": [],
            "summary_rationale": "; ".join(citations),
        }
