"""Evidence-constrained candidate-metric inference for CVSS v4.0.

This module delegates rule execution to the canonical, machine-readable
``core.environmental_rule_catalog.EnvironmentalRuleCatalogEngine``.
Numerical scoring is strictly delegated to ``core.cvss40``.

Research-safety invariants:
* Missing, stale, unknown, or conflicting reachability evidence -> ABSTAIN.
* Internal routed reachability remains MAV:N; lack of Internet exposure is not
  evidence of MAV:A or MAV:L.
* Generic Firewall/WAF presence alone never implies MAC:H (Rule MAC-001).
* CR/IR/AR are accepted only from an explicit, versioned organizational-policy
  mapping. Regulatory scope is evidence to that policy, not a CVSS value.
* High availability/redundancy never implies AR:L (Rule AR-001).
* Straight-Through Processing (STP) autonomous-by-default for valid structured evidence.
  HITL review is engaged strictly on exceptions (divergence, missing context, conflict).
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Mapping, Optional

from core.environmental_rule_catalog import (
    CATALOG_HASH,
    CATALOG_VERSION,
    EnvironmentalRuleCatalogEngine,
    VALID_ENVIRONMENTAL_METRICS,
    evaluate_semantic_quorum,
    is_sampled_for_post_facto_audit,
)

VALID_METRICS = dict(VALID_ENVIRONMENTAL_METRICS)
VALID_METRICS["E"] = {"A", "P", "U", "X"}


class AIEvidenceEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self._catalog_engine = EnvironmentalRuleCatalogEngine()

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

    def analyze_scenario(
        self,
        base_vector: str,
        evidence: Dict[str, Any],
        cve_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return candidate metrics or an exception/abstention decision via canonical catalog."""
        return self._catalog_engine.evaluate(
            base_vector=base_vector,
            evidence=evidence,
            cve_id=cve_id,
        )
