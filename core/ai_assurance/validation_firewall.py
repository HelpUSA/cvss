"""HCAL Validation Firewall.

Enforces fundamental safety invariants:
1. AI_DIRECT_SCORE_OVERRIDE = PROHIBITED: Any attempted direct score alteration is rejected.
2. AI_FINDINGS = ADVISORY_BY_DEFAULT: Non-authoritative findings enrich reports only.
3. AUTHORITATIVE_CANDIDATE_FINDINGS_REQUIRE_EVIDENCE_VALIDATION: Candidate facts cannot
   modify metrics unless independently verified against structured evidence.
4. Metric candidates re-enter the deterministic EnvironmentalRuleCatalogEngine and FIRST core.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Tuple

from core.ai_assurance.provider_adapter import FindingItem, ProviderResponse

logger = logging.getLogger(__name__)


@dataclass
class FirewallAuditEntry:
    finding_id: str
    provider_id: str
    is_authoritative: bool
    action: str  # ADMITTED_ADVISORY, ADMITTED_VALIDATED_CANDIDATE, REJECTED_DIRECT_SCORE, REJECTED_UNVERIFIED
    details: str
    attempted_score_blocked: Optional[float] = None


@dataclass
class FirewallFilteredResult:
    advisory_enrichments: List[Dict[str, Any]] = field(default_factory=list)
    validated_evidence_updates: Dict[str, Any] = field(default_factory=dict)
    rejected_findings: List[Dict[str, Any]] = field(default_factory=list)
    audit_log: List[FirewallAuditEntry] = field(default_factory=list)


class HCALValidationFirewall:
    """Strict gatekeeper preventing untrusted AI outputs from contaminating CVSS metrics or scores."""

    @classmethod
    def filter_response(
        cls,
        response: ProviderResponse,
        existing_evidence: Mapping[str, Any],
        trusted_verification_source: Optional[Mapping[str, Any]] = None,
    ) -> FirewallFilteredResult:
        result = FirewallFilteredResult()
        trusted = trusted_verification_source or {}

        # 1. Process Non-Authoritative Findings (Advisory Only)
        for item in response.non_authoritative_findings:
            # Enforce: Direct score override blocked
            if item.attempted_direct_score is not None:
                result.audit_log.append(FirewallAuditEntry(
                    finding_id=item.finding_id,
                    provider_id=response.provider_id,
                    is_authoritative=False,
                    action="REJECTED_DIRECT_SCORE",
                    details="AI attempted direct score modification; rejected by firewall.",
                    attempted_score_blocked=item.attempted_direct_score,
                ))
                result.rejected_findings.append({
                    "finding_id": item.finding_id,
                    "reason": "Direct score override prohibited by HCAL policy.",
                })
                continue

            # Admitted as non-authoritative advisory note
            result.advisory_enrichments.append({
                "finding_id": item.finding_id,
                "provider_id": response.provider_id,
                "type": item.finding_type,
                "summary": item.summary,
                "details": item.details,
                "confidence": item.confidence,
                "authoritative": False,
            })
            result.audit_log.append(FirewallAuditEntry(
                finding_id=item.finding_id,
                provider_id=response.provider_id,
                is_authoritative=False,
                action="ADMITTED_ADVISORY",
                details="Admitted as non-authoritative report advisory.",
            ))

        # 2. Process Authoritative Candidate Facts
        for item in response.authoritative_candidate_facts:
            # Enforce: Direct score override blocked
            if item.attempted_direct_score is not None:
                result.audit_log.append(FirewallAuditEntry(
                    finding_id=item.finding_id,
                    provider_id=response.provider_id,
                    is_authoritative=True,
                    action="REJECTED_DIRECT_SCORE",
                    details="Authoritative candidate attempted direct score override; rejected.",
                    attempted_score_blocked=item.attempted_direct_score,
                ))
                result.rejected_findings.append({
                    "finding_id": item.finding_id,
                    "reason": "Direct score override prohibited.",
                })
                continue

            ref_field = item.evidence_field_reference
            suggested_val = item.suggested_value

            if not ref_field or suggested_val is None:
                result.audit_log.append(FirewallAuditEntry(
                    finding_id=item.finding_id,
                    provider_id=response.provider_id,
                    is_authoritative=True,
                    action="REJECTED_UNVERIFIED",
                    details="Missing evidence field reference or suggested value.",
                ))
                continue

            # Verify against trusted evidence source
            # An AI finding CANNOT alter evidence unless independent structured evidence confirms it
            if ref_field in trusted and str(trusted[ref_field]).upper() == str(suggested_val).upper():
                result.validated_evidence_updates[ref_field] = trusted[ref_field]
                result.audit_log.append(FirewallAuditEntry(
                    finding_id=item.finding_id,
                    provider_id=response.provider_id,
                    is_authoritative=True,
                    action="ADMITTED_VALIDATED_CANDIDATE",
                    details=f"Candidate fact '{ref_field}={suggested_val}' confirmed by trusted structured evidence.",
                ))
            else:
                # Unverified candidate fact -> rejected from altering metrics, retained as advisory warning
                result.audit_log.append(FirewallAuditEntry(
                    finding_id=item.finding_id,
                    provider_id=response.provider_id,
                    is_authoritative=True,
                    action="REJECTED_UNVERIFIED",
                    details=f"Candidate fact '{ref_field}={suggested_val}' unverified by structured telemetry.",
                ))
                result.advisory_enrichments.append({
                    "finding_id": item.finding_id,
                    "provider_id": response.provider_id,
                    "type": "UNVERIFIED_CANDIDATE_FACT_WARNING",
                    "summary": f"Unverified AI suggestion: {ref_field}={suggested_val}",
                    "details": item.details,
                    "confidence": item.confidence,
                    "authoritative": False,
                })

        return result
