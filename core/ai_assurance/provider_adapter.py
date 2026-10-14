"""HCAL Provider Adapters.

Defines provider-neutral abstract adapter interface and concrete implementations:
- AIProviderAdapter (ABC)
- DisabledProviderAdapter (first-class no-AI mode)
- MockAIProviderAdapter (for deterministic testing & simulation)
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from core.ai_assurance.packages import BaseHCALPackage


@dataclass
class FindingItem:
    finding_id: str
    finding_type: str  # EXPLANATION, HYPOTHESIS, ANOMALY_WARNING, CANDIDATE_FACT
    is_authoritative_candidate: bool
    summary: str
    details: str
    evidence_field_reference: Optional[str] = None
    suggested_value: Optional[str] = None
    confidence: float = 0.8
    attempted_direct_score: Optional[float] = None  # Blocked by firewall if present


@dataclass
class ProviderResponse:
    provider_id: str
    status: str  # SUCCESS, TIMEOUT, ERROR, DISABLED, MALFORMED
    latency_ms: float
    non_authoritative_findings: List[FindingItem] = field(default_factory=list)
    authoritative_candidate_facts: List[FindingItem] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class AIProviderAdapter(ABC):
    """Abstract interface for replaceable AI cognitive review providers."""

    def __init__(self, provider_id: str, provider_type: str = "local"):
        self.provider_id = provider_id
        self.provider_type = provider_type  # "local", "private_enterprise", "external_api", "disabled"

    @property
    @abstractmethod
    def is_enabled(self) -> bool:
        """Return True if adapter is configured and active."""
        pass

    @abstractmethod
    def analyze_package(self, package: BaseHCALPackage, timeout_seconds: float = 2.0) -> ProviderResponse:
        """Analyze an exported HCAL package and return normalized response."""
        pass


class DisabledProviderAdapter(AIProviderAdapter):
    """First-class no-AI adapter: produces zero external calls and immediate no-op response."""

    def __init__(self):
        super().__init__(provider_id="disabled-provider", provider_type="disabled")

    @property
    def is_enabled(self) -> bool:
        return False

    def analyze_package(self, package: BaseHCALPackage, timeout_seconds: float = 2.0) -> ProviderResponse:
        return ProviderResponse(
            provider_id=self.provider_id,
            status="DISABLED",
            latency_ms=0.0,
            error_message="AI cognitive assurance is disabled (Core Autonomous Mode).",
        )


class MockAIProviderAdapter(AIProviderAdapter):
    """Deterministic mock provider for unit testing, fault injection, and multi-AI simulation."""

    def __init__(
        self,
        provider_id: str = "mock-ai-1",
        simulate_timeout: bool = False,
        simulate_error: bool = False,
        simulate_malformed: bool = False,
        simulate_sleep_seconds: float = 0.0,
        mock_findings: Optional[List[FindingItem]] = None,
        latency_ms: float = 10.0,
    ):
        super().__init__(provider_id=provider_id, provider_type="local")
        self.simulate_timeout = simulate_timeout
        self.simulate_error = simulate_error
        self.simulate_malformed = simulate_malformed
        self.simulate_sleep_seconds = simulate_sleep_seconds
        self.mock_findings = mock_findings or []
        self._latency_ms = latency_ms

    @property
    def is_enabled(self) -> bool:
        return True

    def analyze_package(self, package: BaseHCALPackage, timeout_seconds: float = 2.0) -> ProviderResponse:
        if self.simulate_sleep_seconds > 0:
            time.sleep(self.simulate_sleep_seconds)

        if self.simulate_timeout:
            return ProviderResponse(
                provider_id=self.provider_id,
                status="TIMEOUT",
                latency_ms=timeout_seconds * 1000.0,
                error_message=f"Provider timed out after {timeout_seconds}s.",
            )

        if self.simulate_error:
            return ProviderResponse(
                provider_id=self.provider_id,
                status="ERROR",
                latency_ms=self._latency_ms,
                error_message="Simulated upstream network/quota failure.",
            )

        if self.simulate_malformed:
            return ProviderResponse(
                provider_id=self.provider_id,
                status="MALFORMED",
                latency_ms=self._latency_ms,
                raw_response={"garbage": "%%% invalid structure %%%"},
                error_message="Provider returned malformed schema.",
            )

        non_auth = [f for f in self.mock_findings if not f.is_authoritative_candidate]
        auth = [f for f in self.mock_findings if f.is_authoritative_candidate]

        return ProviderResponse(
            provider_id=self.provider_id,
            status="SUCCESS",
            latency_ms=self._latency_ms,
            non_authoritative_findings=non_auth,
            authoritative_candidate_facts=auth,
            raw_response={"finding_count": len(self.mock_findings)},
        )
