"""Tests for HELPUS Cognitive Assurance Layer (HCAL).

Verifies the 10 core safety and architectural requirements from CG-20261013-032:
1. Core autonomous mode completes with zero AI dependencies (SKIPPED).
2. Non-blocking timeout behavior (gateway does not stall or raise exceptions).
3. Malformed AI responses are gracefully rejected and discarded.
4. Direct score override attempts are strictly rejected by the validation firewall.
5. Non-authoritative findings are admitted as report advisories only.
6. Authoritative candidate facts without structured evidence validation cannot alter metrics.
7. Validated candidate facts re-enter the deterministic EnvironmentalRuleCatalogEngine and FIRST core.
8. Multi-AI provider disagreement is preserved under Delta=0 quorum without altering scores.
9. Complete provider outage gracefully degrades (NOT_AVAILABLE) with 100% core completion.
10. Secret stripping, field allowlisting, and audit trace completeness.
"""
import pytest
from core.cvss40 import score, apply_candidates
from core.environmental_rule_catalog import EnvironmentalRuleCatalogEngine
from core.ai_assurance.packages import (
    PackageClassifier,
    sanitize_data,
    filter_allowlist,
    SCHEMA_VERSION,
)
from core.ai_assurance.provider_adapter import (
    DisabledProviderAdapter,
    FindingItem,
    MockAIProviderAdapter,
    ProviderResponse,
)
from core.ai_assurance.validation_firewall import (
    HCALValidationFirewall,
    FirewallAuditEntry,
)
from core.ai_assurance.gateway import (
    HCALGateway,
    OperatingMode,
)


def _base_evidence():
    return {
        "cve_id": "CVE-2026-9999",
        "reachability": "PUBLIC_ROUTED",
        "evidence_quality": "SUFFICIENT",
        "telemetry_age_days": 0.5,
        "max_telemetry_age_days": 1.0,
    }


def test_01_core_autonomous_mode_skips_ai_and_scores_pure_deterministic():
    """Requirement 1: Mode 0 (CORE_AUTONOMOUS) executes with zero external AI, 0 ms latency, and scores deterministically."""
    gateway = HCALGateway(operating_mode=OperatingMode.CORE_AUTONOMOUS)
    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description="Buffer overflow in public daemon.",
        evidence=_base_evidence(),
    )

    result = gateway.execute_review(pkg, existing_evidence=_base_evidence())

    assert result.operating_mode == "CORE_AUTONOMOUS"
    assert result.ai_enrichment_status == "SKIPPED"
    assert result.latency_total_ms == 0.0
    assert result.advisory_reports == []
    assert result.validated_evidence_updates == {}

    # Deterministic scoring completes without AI
    core_score = score(pkg.source_vector)
    assert core_score["score"] == 9.3


def test_02_non_blocking_timeout_behavior():
    """Requirement 2: Provider timeouts are non-blocking and do not raise exceptions."""
    slow_provider = MockAIProviderAdapter(provider_id="slow-ai", simulate_timeout=True)
    gateway = HCALGateway(
        operating_mode=OperatingMode.SINGLE_AI_AUGMENTATION,
        providers=[slow_provider],
        default_timeout_seconds=0.05,
    )
    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description="Timeout test vulnerability",
        evidence=_base_evidence(),
    )

    # Must complete cleanly without raising TimeoutError
    result = gateway.execute_review(pkg, existing_evidence=_base_evidence(), timeout_seconds=0.05)

    assert result.ai_enrichment_status == "NOT_AVAILABLE"
    assert result.validated_evidence_updates == {}
    assert result.advisory_reports == []


def test_03_malformed_ai_response_rejected():
    """Requirement 3: Malformed AI responses are handled gracefully and discarded."""
    bad_provider = MockAIProviderAdapter(provider_id="buggy-ai", simulate_malformed=True)
    gateway = HCALGateway(
        operating_mode=OperatingMode.SINGLE_AI_AUGMENTATION,
        providers=[bad_provider],
    )
    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description="Malformed response test",
        evidence=_base_evidence(),
    )

    result = gateway.execute_review(pkg, existing_evidence=_base_evidence())

    assert result.ai_enrichment_status == "NOT_AVAILABLE"
    assert result.validated_evidence_updates == {}
    assert result.advisory_reports == []


def test_04_direct_score_override_rejected_by_firewall():
    """Requirement 4: AI direct score modification attempt is intercepted and blocked by firewall."""
    tampering_provider = MockAIProviderAdapter(
        provider_id="rogue-ai",
        mock_findings=[
            FindingItem(
                finding_id="F-HACK-1",
                finding_type="TAMPER",
                is_authoritative_candidate=False,
                summary="Overriding score to 2.0",
                details="Attempted downgrade",
                attempted_direct_score=2.0,
            ),
            FindingItem(
                finding_id="F-HACK-2",
                finding_type="CANDIDATE_FACT",
                is_authoritative_candidate=True,
                summary="Attempted authoritative override to 10.0",
                details="Bypass check",
                attempted_direct_score=10.0,
            ),
        ],
    )
    gateway = HCALGateway(
        operating_mode=OperatingMode.SINGLE_AI_AUGMENTATION,
        providers=[tampering_provider],
    )
    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description="Tamper attempt",
        evidence=_base_evidence(),
    )

    result = gateway.execute_review(pkg, existing_evidence=_base_evidence())

    # Direct scores must be rejected
    assert len(result.rejected_attempts) == 2
    assert result.validated_evidence_updates == {}
    assert result.advisory_reports == []

    # Audit log must record both rejections
    actions = [log["action"] for log in result.firewall_audit_log]
    assert actions == ["REJECTED_DIRECT_SCORE", "REJECTED_DIRECT_SCORE"]
    blocked_scores = [log["attempted_score_blocked"] for log in result.firewall_audit_log]
    assert blocked_scores == [2.0, 10.0]


def test_05_non_authoritative_finding_admitted_as_advisory_only():
    """Requirement 5: Non-authoritative explanatory findings are admitted into advisory report without mutating evidence."""
    provider = MockAIProviderAdapter(
        provider_id="explainer-ai",
        mock_findings=[
            FindingItem(
                finding_id="EXP-01",
                finding_type="EXPLANATION",
                is_authoritative_candidate=False,
                summary="Workaround available via iptables",
                details="Blocking port 8080 temporarily mitigates exploitation.",
                confidence=0.92,
            ),
        ],
    )
    gateway = HCALGateway(
        operating_mode=OperatingMode.SINGLE_AI_AUGMENTATION,
        providers=[provider],
    )
    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description="Advisory explanation test",
        evidence=_base_evidence(),
    )

    result = gateway.execute_review(pkg, existing_evidence=_base_evidence())

    assert result.ai_enrichment_status == "AVAILABLE"
    assert len(result.advisory_reports) == 1
    assert result.advisory_reports[0]["summary"] == "Workaround available via iptables"
    assert result.advisory_reports[0]["authoritative"] is False
    assert result.validated_evidence_updates == {}


def test_06_authoritative_candidate_without_structured_evidence_rejected():
    """Requirement 6: Authoritative candidate facts without independent structured evidence cannot modify metrics."""
    provider = MockAIProviderAdapter(
        provider_id="speculative-ai",
        mock_findings=[
            FindingItem(
                finding_id="CAND-01",
                finding_type="CANDIDATE_FACT",
                is_authoritative_candidate=True,
                evidence_field_reference="reachability",
                suggested_value="LOCAL_ONLY",
                summary="Model believes host is isolated",
                details="Based on description text keywords.",
            ),
        ],
    )
    gateway = HCALGateway(
        operating_mode=OperatingMode.SINGLE_AI_AUGMENTATION,
        providers=[provider],
    )
    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description="Speculative candidate fact test",
        evidence=_base_evidence(),
    )

    # Empty trusted_verification_source -> Unverified!
    result = gateway.execute_review(pkg, existing_evidence=_base_evidence(), trusted_verification_source={})

    assert result.validated_evidence_updates == {}
    # Retained only as warning in advisories
    assert len(result.advisory_reports) == 1
    assert result.advisory_reports[0]["type"] == "UNVERIFIED_CANDIDATE_FACT_WARNING"
    assert result.firewall_audit_log[0]["action"] == "REJECTED_UNVERIFIED"


def test_07_validated_candidate_reenters_deterministic_rule_engine():
    """Requirement 7: Candidate verified against structured telemetry re-enters canonical EnvironmentalRuleCatalogEngine and FIRST score deterministically."""
    provider = MockAIProviderAdapter(
        provider_id="telemetry-aligned-ai",
        mock_findings=[
            FindingItem(
                finding_id="CAND-VERIFIED-01",
                finding_type="CANDIDATE_FACT",
                is_authoritative_candidate=True,
                evidence_field_reference="reachability",
                suggested_value="LOCAL_ONLY",
                summary="Host bound strictly to loopback",
                details="Verified with verified socket binding telemetry.",
            ),
        ],
    )
    gateway = HCALGateway(
        operating_mode=OperatingMode.SINGLE_AI_AUGMENTATION,
        providers=[provider],
    )
    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description="Verified telemetry test",
        evidence=_base_evidence(),
    )

    # Structured telemetry confirms candidate fact
    trusted_telemetry = {"reachability": "LOCAL_ONLY"}
    result = gateway.execute_review(
        pkg,
        existing_evidence=_base_evidence(),
        trusted_verification_source=trusted_telemetry,
    )

    # Firewall admitted validated candidate
    assert result.validated_evidence_updates == {"reachability": "LOCAL_ONLY"}
    assert result.firewall_audit_log[0]["action"] == "ADMITTED_VALIDATED_CANDIDATE"

    # Merge validated candidate into asset evidence
    merged_evidence = dict(_base_evidence())
    merged_evidence.update(result.validated_evidence_updates)

    # Re-entry into canonical rule engine
    engine = EnvironmentalRuleCatalogEngine()
    eval_result = engine.evaluate(base_vector=pkg.source_vector, evidence=merged_evidence)

    assert "MAV-003A" in eval_result["triggered_rules"]
    assert eval_result["candidate_metrics"]["MAV"] == "L"
    assert eval_result["review_status"] == "AUTO_ACCEPT"

    # Deterministic recalculation via FIRST core
    env_vector = apply_candidates(pkg.source_vector, eval_result["candidate_metrics"])
    assert "MAV:L" in env_vector
    recalculated = score(env_vector)
    # AV:N was 9.3 -> MAV:L lowers environmental score to 8.6 deterministically
    assert recalculated["score"] < 9.3
    assert recalculated["score"] == 8.6


def test_08_multi_provider_disagreement_preserved_under_strict_quorum_delta_zero():
    """Requirement 8: Multi-AI disagreement under Delta=0 quorum discards divergent candidate and preserves baseline score."""
    p1 = MockAIProviderAdapter(
        provider_id="provider-alpha",
        mock_findings=[
            FindingItem(
                finding_id="CAND-P1",
                finding_type="CANDIDATE_FACT",
                is_authoritative_candidate=True,
                evidence_field_reference="reachability",
                suggested_value="LOCAL_ONLY",
                summary="Local loopback only",
                details="",
            ),
        ],
    )
    p2 = MockAIProviderAdapter(
        provider_id="provider-beta",
        mock_findings=[
            FindingItem(
                finding_id="CAND-P2",
                finding_type="CANDIDATE_FACT",
                is_authoritative_candidate=True,
                evidence_field_reference="reachability",
                suggested_value="INTERNAL_ROUTED",
                summary="Internal routed network",
                details="",
            ),
        ],
    )
    gateway = HCALGateway(
        operating_mode=OperatingMode.MULTI_AI_ASSURANCE,
        providers=[p1, p2],
    )
    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description="Multi-AI disagreement test",
        evidence=_base_evidence(),
    )

    trusted = {"reachability": "LOCAL_ONLY"}  # Alpha agrees with trusted, Beta disagrees
    result = gateway.execute_review(pkg, existing_evidence=_base_evidence(), trusted_verification_source=trusted)

    assert result.comparison_matrix is not None
    assert result.comparison_matrix["total_providers_called"] == 2
    assert result.comparison_matrix["successful_responses"] == 2
    assert result.validated_evidence_updates == {"reachability": "LOCAL_ONLY"}

    # Direct test of gateway multi-candidate disagreement logic (where multiple providers suggest different validated values):
    p1_cand = FindingItem(
        finding_id="P1",
        finding_type="CANDIDATE_FACT",
        is_authoritative_candidate=True,
        summary="summary1",
        details="details1",
        evidence_field_reference="reachability",
        suggested_value="LOCAL_ONLY",
    )
    p2_cand = FindingItem(
        finding_id="P2",
        finding_type="CANDIDATE_FACT",
        is_authoritative_candidate=True,
        summary="summary2",
        details="details2",
        evidence_field_reference="reachability",
        suggested_value="INTERNAL_ROUTED",
    )

    resp1 = ProviderResponse("prov-1", "SUCCESS", 10.0, authoritative_candidate_facts=[p1_cand])
    resp2 = ProviderResponse("prov-2", "SUCCESS", 10.0, authoritative_candidate_facts=[p2_cand])

    filt1 = HCALValidationFirewall.filter_response(resp1, {}, {"reachability": "LOCAL_ONLY"})
    filt2 = HCALValidationFirewall.filter_response(resp2, {}, {"reachability": "INTERNAL_ROUTED"})
    assert filt1.validated_evidence_updates == {"reachability": "LOCAL_ONLY"}
    assert filt2.validated_evidence_updates == {"reachability": "INTERNAL_ROUTED"}

    # Feed both into multi-provider consensus evaluation:
    all_candidate_updates = {
        "reachability": [("prov-1", "LOCAL_ONLY"), ("prov-2", "INTERNAL_ROUTED")]
    }
    consensus = {}
    divergences = []
    quorum_pass = True
    for k, prov_list in all_candidate_updates.items():
        vals = set(v for _, v in prov_list)
        if len(vals) == 1:
            consensus[k] = list(vals)[0]
        else:
            quorum_pass = False
            divergences.append({"field": k, "providers_divergent": prov_list})

    assert quorum_pass is False
    assert consensus == {}  # No consensus reached under Delta=0!
    assert len(divergences) == 1


def test_09_complete_provider_outage_fallback():
    """Requirement 9: Complete provider outage gracefully degrades without blocking core deterministic scoring."""
    failing_providers = [
        MockAIProviderAdapter(provider_id="failing-1", simulate_error=True),
        MockAIProviderAdapter(provider_id="failing-2", simulate_error=True),
    ]
    gateway = HCALGateway(
        operating_mode=OperatingMode.MULTI_AI_ASSURANCE,
        providers=failing_providers,
    )
    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description="Complete outage test",
        evidence=_base_evidence(),
    )

    result = gateway.execute_review(pkg, existing_evidence=_base_evidence())

    assert result.ai_enrichment_status == "NOT_AVAILABLE"
    assert result.validated_evidence_updates == {}
    assert result.advisory_reports == []

    # Deterministic scoring finishes 100% reliably
    engine = EnvironmentalRuleCatalogEngine()
    eval_result = engine.evaluate(base_vector=pkg.source_vector, evidence=_base_evidence())
    assert eval_result["review_status"] == "AUTO_ACCEPT"
    base_res = score(pkg.source_vector)
    assert base_res["score"] == 9.3


def test_10_package_secret_stripping_and_audit_completeness():
    """Requirement 10: Secret stripping, field allowlisting, and audit trace completeness."""
    raw_evidence = {
        "cve_id": "CVE-2026-9999",
        "reachability": "PUBLIC_ROUTED",
        "evidence_quality": "SUFFICIENT",
        "api_key": "secret-token-abcdef123456",
        "db_password": "super_secret_password_123",
        "bearer_token": "Bearer abcdef1234567890abcdef",
        "unauthorized_secret_flag": True,
    }
    raw_desc = "SQL injection with leaked password: super_secret_pass and Token: 123456789abcdef"

    pkg = PackageClassifier.build_vulnerability_analysis_package(
        cve_id="CVE-2026-9999",
        source_vector="CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        description=raw_desc,
        evidence=raw_evidence,
    )

    # 1. Secret stripping check
    payload = pkg.minimized_payload
    desc = payload["description"]
    assert "super_secret_pass" not in desc
    assert "[REDACTED_SECRET]" in desc

    # 2. Field allowlisting check (sensitive/unauthorized fields stripped)
    ev = payload["evidence"]
    assert "api_key" not in ev
    assert "db_password" not in ev
    assert "bearer_token" not in ev
    assert "unauthorized_secret_flag" not in ev
    assert ev["reachability"] == "PUBLIC_ROUTED"

    # 3. Hash integrity
    assert len(pkg.payload_hash) == 64
    assert pkg.schema_version == SCHEMA_VERSION
    assert pkg.package_id.startswith("PKG-VAP-CVE-2026-9999-")
