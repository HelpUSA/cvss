"""HCAL Gateway and Multi-AI Orchestrator.

Orchestrates optional cognitive assurance with provider-neutral fan-out,
asynchronous non-blocking execution, timeout/circuit-breaker, and graceful degradation.

Invariants:
- CORE_AUTONOMOUS_WITHOUT_AI: Core executes to completion even if all providers are down.
- Non-blocking execution: Timeouts and provider errors do not raise exceptions to the core.
- AI_ENRICHMENT_STATUS reflects enrichment health (AVAILABLE, DEGRADED, NOT_AVAILABLE, SKIPPED).
"""
from __future__ import annotations

import concurrent.futures
import enum
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Tuple

from core.ai_assurance.packages import BaseHCALPackage, PackageClassifier
from core.ai_assurance.provider_adapter import (
    AIProviderAdapter,
    DisabledProviderAdapter,
    FindingItem,
    ProviderResponse,
)
from core.ai_assurance.validation_firewall import (
    FirewallAuditEntry,
    FirewallFilteredResult,
    HCALValidationFirewall,
)


class OperatingMode(str, enum.Enum):
    CORE_AUTONOMOUS = "CORE_AUTONOMOUS"          # Mode 0: Zero external AI
    SINGLE_AI_AUGMENTATION = "SINGLE_AI"         # Mode 1: One provider review
    MULTI_AI_ASSURANCE = "MULTI_AI"              # Mode 2: Multi-provider fan-out & comparison


@dataclass
class MultiAIComparisonMatrix:
    total_providers_called: int
    successful_responses: int
    failed_responses: int
    consensus_agreed_findings: List[str] = field(default_factory=list)
    divergent_findings: List[Dict[str, Any]] = field(default_factory=list)
    quorum_metric_delta_zero: bool = True


@dataclass
class HCALEnrichmentResult:
    operating_mode: str
    ai_enrichment_status: str  # AVAILABLE, DEGRADED, NOT_AVAILABLE, SKIPPED
    latency_total_ms: float
    advisory_reports: List[Dict[str, Any]] = field(default_factory=list)
    validated_evidence_updates: Dict[str, Any] = field(default_factory=dict)
    rejected_attempts: List[Dict[str, Any]] = field(default_factory=list)
    comparison_matrix: Optional[Dict[str, Any]] = None
    firewall_audit_log: List[Dict[str, Any]] = field(default_factory=list)
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HCALGateway:
    """Non-blocking gateway managing optional cognitive assurance review."""

    def __init__(
        self,
        operating_mode: OperatingMode = OperatingMode.CORE_AUTONOMOUS,
        providers: Optional[List[AIProviderAdapter]] = None,
        default_timeout_seconds: float = 1.0,
    ):
        self.operating_mode = operating_mode
        self.providers: List[AIProviderAdapter] = providers or [DisabledProviderAdapter()]
        self.default_timeout_seconds = default_timeout_seconds

    def execute_review(
        self,
        package: BaseHCALPackage,
        existing_evidence: Mapping[str, Any],
        trusted_verification_source: Optional[Mapping[str, Any]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> HCALEnrichmentResult:
        """Execute non-blocking cognitive assurance review with graceful degradation."""
        start_time = time.time()
        timeout = timeout_seconds or self.default_timeout_seconds

        # Mode 0: Core Autonomous (No external AI)
        if self.operating_mode == OperatingMode.CORE_AUTONOMOUS or not self.providers:
            return HCALEnrichmentResult(
                operating_mode=self.operating_mode.value,
                ai_enrichment_status="SKIPPED",
                latency_total_ms=0.0,
            )

        active_providers = [p for p in self.providers if p.is_enabled]
        if not active_providers:
            return HCALEnrichmentResult(
                operating_mode=self.operating_mode.value,
                ai_enrichment_status="NOT_AVAILABLE",
                latency_total_ms=0.0,
            )

        responses: List[ProviderResponse] = []

        # Execute providers via thread pool with hard non-blocking isolation
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(active_providers))
        future_to_provider = {
            executor.submit(p.analyze_package, package, timeout): p
            for p in active_providers
        }
        try:
            done, not_done = concurrent.futures.wait(
                future_to_provider.keys(),
                timeout=timeout,
                return_when=concurrent.futures.ALL_COMPLETED,
            )
            for future in done:
                provider = future_to_provider[future]
                try:
                    resp = future.result()
                    responses.append(resp)
                except Exception as e:
                    responses.append(ProviderResponse(
                        provider_id=provider.provider_id,
                        status="ERROR",
                        latency_ms=(time.time() - start_time) * 1000.0,
                        error_message=f"Provider unhandled exception: {str(e)}",
                    ))
            for future in not_done:
                provider = future_to_provider[future]
                future.cancel()
                responses.append(ProviderResponse(
                    provider_id=provider.provider_id,
                    status="TIMEOUT",
                    latency_ms=timeout * 1000.0,
                    error_message=f"Gateway hard timeout exceeded ({timeout}s).",
                ))
        finally:
            # Hard non-blocking shutdown: caller never waits for hanging provider threads
            try:
                executor.shutdown(wait=False, cancel_futures=True)
            except TypeError:
                executor.shutdown(wait=False)

        elapsed_ms = (time.time() - start_time) * 1000.0

        # Assess health status
        success_count = sum(1 for r in responses if r.status == "SUCCESS")
        if success_count == 0:
            enrichment_status = "NOT_AVAILABLE"
        elif success_count < len(active_providers):
            enrichment_status = "DEGRADED"
        else:
            enrichment_status = "AVAILABLE"

        # Apply Validation Firewall
        advisories: List[Dict[str, Any]] = []
        rejected: List[Dict[str, Any]] = []
        audit_log: List[Dict[str, Any]] = []
        all_candidate_updates: Dict[str, List[Tuple[str, Any]]] = {}

        for resp in responses:
            if resp.status != "SUCCESS":
                continue
            filtered = HCALValidationFirewall.filter_response(
                resp,
                existing_evidence=existing_evidence,
                trusted_verification_source=trusted_verification_source,
            )
            advisories.extend(filtered.advisory_enrichments)
            rejected.extend(filtered.rejected_findings)
            for entry in filtered.audit_log:
                audit_log.append(asdict(entry))

            for k, v in filtered.validated_evidence_updates.items():
                if k not in all_candidate_updates:
                    all_candidate_updates[k] = []
                all_candidate_updates[k].append((resp.provider_id, v))

        # Multi-AI Quorum Evaluation for validated candidates (STRICT_QUORUM_DELTA = 0)
        consensus_updates: Dict[str, Any] = {}
        divergences: List[Dict[str, Any]] = []
        quorum_pass = True

        for k, prov_list in all_candidate_updates.items():
            vals = set(v for _, v in prov_list)
            if len(vals) == 1:
                consensus_updates[k] = list(vals)[0]
            else:
                quorum_pass = False
                divergences.append({
                    "field": k,
                    "providers_divergent": [{"provider": pid, "value": v} for pid, v in prov_list],
                })

        comparison_matrix = None
        if self.operating_mode == OperatingMode.MULTI_AI_ASSURANCE:
            comparison_matrix = {
                "total_providers_called": len(active_providers),
                "successful_responses": success_count,
                "failed_responses": len(active_providers) - success_count,
                "consensus_agreed_findings": list(consensus_updates.keys()),
                "divergent_findings": divergences,
                "quorum_metric_delta_zero": quorum_pass,
            }

        return HCALEnrichmentResult(
            operating_mode=self.operating_mode.value,
            ai_enrichment_status=enrichment_status,
            latency_total_ms=round(elapsed_ms, 2),
            advisory_reports=advisories,
            validated_evidence_updates=consensus_updates,
            rejected_attempts=rejected,
            comparison_matrix=comparison_matrix,
            firewall_audit_log=audit_log,
        )
