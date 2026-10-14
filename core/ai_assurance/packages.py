"""HCAL Data Packages and Sanitization.

Defines versioned, hash-bound, minimized packages exported to optional AI providers:
- VulnerabilityAnalysisPackage
- EnvironmentReviewPackage
- ExecutiveRiskPackage

Enforces secret stripping, field allowlisting, and sensitivity classification.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Set

SCHEMA_VERSION = "1.0.0"

_SECRET_PATTERNS = [
    re.compile(r"(?i)(password|secret|token|api[_-]?key|bearer|credential|private[_-]?key)\s*[:=]\s*['\"]?([^'\"\s,;]+)", re.IGNORECASE),
    re.compile(r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{16,}", re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]+ PRIVATE KEY-----", re.IGNORECASE),
]

_ALLOWLIST_CORE_FIELDS = {
    "cve_id", "cve", "source_cvss_vector", "vector", "base_vector",
    "reachability", "evidence_quality", "telemetry_age_days",
    "telemetry_profile", "max_telemetry_age_days", "firewall_status",
    "routing_table_status", "l2_broadcast_only", "local_host_only",
    "physical_access_only", "internet_exposed", "routed_ip_access",
    "evidenced_exploit_preconditions_elevated", "waf_active",
    "organization_policy_id", "policy_version", "security_requirements",
    "modified_impacts", "target_authenticated_prerequisite",
}


def sanitize_data(data: Any) -> Any:
    """Recursively strip credentials, tokens, and private secrets from payload."""
    if isinstance(data, str):
        sanitized = data
        for pattern in _SECRET_PATTERNS:
            sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
        return sanitized
    elif isinstance(data, Mapping):
        out = {}
        for k, v in data.items():
            k_str = str(k).lower()
            if any(secret_term in k_str for secret_term in ("secret", "token", "password", "api_key", "private_key")):
                out[k] = "[REDACTED_SECRET]"
            else:
                out[k] = sanitize_data(v)
        return out
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    return data


def filter_allowlist(evidence: Mapping[str, Any], allowed_keys: Optional[Set[str]] = None) -> Dict[str, Any]:
    """Filter evidence fields to strictly permitted allowlist."""
    allow = allowed_keys or _ALLOWLIST_CORE_FIELDS
    return {k: v for k, v in evidence.items() if k in allow}


@dataclass(frozen=True)
class BaseHCALPackage:
    package_type: str
    package_id: str
    schema_version: str
    cve_id: str
    classification: str  # PUBLIC, INTERNAL_CONFIDENTIAL, RESTRICTED
    source_vector: str
    minimized_payload: Dict[str, Any]
    payload_hash: str
    timestamp_utc: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PackageClassifier:
    """Builder and sanitizer for versioned, hash-bound HCAL export packages."""

    @staticmethod
    def _compute_payload_hash(payload: Mapping[str, Any]) -> str:
        dumped = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(dumped).hexdigest()

    @classmethod
    def build_vulnerability_analysis_package(
        cls,
        cve_id: str,
        source_vector: str,
        description: str,
        evidence: Mapping[str, Any],
        classification: str = "INTERNAL_CONFIDENTIAL",
    ) -> BaseHCALPackage:
        filtered = filter_allowlist(evidence)
        sanitized_ev = sanitize_data(filtered)
        sanitized_desc = sanitize_data(description)
        payload = {
            "cve_id": cve_id,
            "source_vector": source_vector,
            "description": sanitized_desc,
            "evidence": sanitized_ev,
        }
        p_hash = cls._compute_payload_hash(payload)
        pkg_id = f"PKG-VAP-{cve_id}-{p_hash[:8]}"
        return BaseHCALPackage(
            package_type="VulnerabilityAnalysisPackage",
            package_id=pkg_id,
            schema_version=SCHEMA_VERSION,
            cve_id=cve_id,
            classification=classification,
            source_vector=source_vector,
            minimized_payload=payload,
            payload_hash=p_hash,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def build_environment_review_package(
        cls,
        cve_id: str,
        source_vector: str,
        environmental_summary: Mapping[str, Any],
        classification: str = "INTERNAL_CONFIDENTIAL",
    ) -> BaseHCALPackage:
        sanitized_summary = sanitize_data(dict(environmental_summary))
        p_hash = cls._compute_payload_hash(sanitized_summary)
        pkg_id = f"PKG-ERP-{cve_id}-{p_hash[:8]}"
        return BaseHCALPackage(
            package_type="EnvironmentReviewPackage",
            package_id=pkg_id,
            schema_version=SCHEMA_VERSION,
            cve_id=cve_id,
            classification=classification,
            source_vector=source_vector,
            minimized_payload=sanitized_summary,
            payload_hash=p_hash,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def build_executive_risk_package(
        cls,
        cve_id: str,
        source_vector: str,
        deterministic_result: Mapping[str, Any],
        classification: str = "INTERNAL_CONFIDENTIAL",
    ) -> BaseHCALPackage:
        payload = {
            "cve_id": cve_id,
            "source_score": deterministic_result.get("source_score"),
            "environmental_score": deterministic_result.get("environmental_score"),
            "decision": deterministic_result.get("decision"),
            "summary_rationale": sanitize_data(deterministic_result.get("rationale", "")),
        }
        p_hash = cls._compute_payload_hash(payload)
        pkg_id = f"PKG-EXP-{cve_id}-{p_hash[:8]}"
        return BaseHCALPackage(
            package_type="ExecutiveRiskPackage",
            package_id=pkg_id,
            schema_version=SCHEMA_VERSION,
            cve_id=cve_id,
            classification=classification,
            source_vector=source_vector,
            minimized_payload=payload,
            payload_hash=p_hash,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )


# Backward compatibility aliases
VulnerabilityAnalysisPackage = BaseHCALPackage
EnvironmentReviewPackage = BaseHCALPackage
ExecutiveRiskPackage = BaseHCALPackage
