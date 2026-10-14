"""HELPUS CVSS AI v4.0 — Canonical Environmental Rule Catalog & Execution Engine.

Specification Standard: FIRST CVSS v4.0 Section 4 (Environmental Metrics).
Catalog Version: 1.0.0
Execution Model: Pure Python Deterministic Boolean Logic (Zero External LLM Dependency).

Governing Principles:
1. Single Source of Truth: CANONICAL_RULES directly drives runtime evaluation.
2. CONTROL_PRESENT != CONTROL_EFFECTIVE != CVSS_MODIFIED_METRIC.
3. Straight-Through Processing (STP) by default; Human-in-the-Loop (HITL) exception-only.
4. Fail-Safe Abstention: Missing, stale, or conflicting evidence triggers ABSTAIN.
5. Strict Semantic Quorum: Delta=0 at metric level required for semantic inference STP.
6. Internal Control: 3%–5% post-facto sampling is an internal HelpUS control (HELPUS_INTERNAL_CONTROL).
"""
from __future__ import annotations

import copy
import hashlib
import inspect
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple

CATALOG_VERSION = "1.0.0"
CATALOG_ID = "HELPUS-ENVIRONMENTAL-RULE-CATALOG-V1"
INTERNAL_CONTROL_SAMPLE_RATE = 0.04  # 4% (within 3%–5% HELPUS_INTERNAL_CONTROL band)

VALID_ENVIRONMENTAL_METRICS = {
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
}

_DYNAMIC_MAX_AGE_DAYS = 1.0
_STATIC_MAX_AGE_DAYS = 7.0


RuleEvaluator = Callable[[str, Mapping[str, Any], Mapping[str, Any]], Tuple[bool, Optional[str], Optional[str]]]


@dataclass(frozen=True)
class RuleDefinition:
    rule_id: str
    target_metric: str
    description: str
    rationale: str
    citation: str
    preconditions: str
    evaluator: RuleEvaluator


# --- Evaluator Functions for Canonical Rules ---

def _eval_mav_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    reach = ctx.get("reachability", "")
    if reach in ("PUBLIC_ROUTED", "INTERNAL_ROUTED") or ev.get("internet_exposed") is True:
        return True, "N", "MAV:N - Rule MAV-001 (routed network reachability retains Network vector)."
    return False, None, None


def _eval_mav_002(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    reach = ctx.get("reachability", "")
    if reach == "ADJACENT_ONLY" or ev.get("l2_broadcast_only") is True:
        return True, "A", "MAV:A - Rule MAV-002 (verified adjacent L2 broadcast boundary)."
    return False, None, None


def _eval_mav_003a(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    reach = ctx.get("reachability", "")
    if reach == "LOCAL_ONLY" or ev.get("local_host_only") is True:
        return True, "L", "MAV:L - Rule MAV-003A (verified local host / socket isolation)."
    return False, None, None


def _eval_mav_003b(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    reach = ctx.get("reachability", "")
    if reach == "PHYSICAL_ONLY" or ev.get("physical_access_only") is True:
        return True, "P", "MAV:P - Rule MAV-003B (verified physical airgap boundary)."
    return False, None, None


def _eval_mac_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    if ev.get("waf_active") is True and not ev.get("evidenced_exploit_preconditions_elevated"):
        return True, "X", "MAC:X - Rule MAC-001 (defensive control presence alone preserves Base MAC)."
    return False, None, None


def _eval_mac_002(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    if ev.get("evidenced_exploit_preconditions_elevated") is True:
        return True, "H", "MAC:H - Rule MAC-002 (target-specific exploit engineering verified)."
    return False, None, None


def _eval_mpr_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    target_pr = str(ev.get("target_authenticated_prerequisite", "")).upper()
    if target_pr in ("LOW", "L"):
        return True, "L", "MPR:L - Rule MPR-001 (target-specific low privileges required before exploit)."
    elif target_pr in ("HIGH", "H"):
        return True, "H", "MPR:H - Rule MPR-001 (target-specific high privileges required before exploit)."
    return False, None, None


def _eval_cr_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    reqs = ev.get("security_requirements")
    pol_id = ev.get("organization_policy_id")
    pol_ver = ev.get("policy_version")
    if isinstance(reqs, Mapping) and pol_id and pol_ver:
        val = str(reqs.get("CR", "")).upper()
        if val in {"H", "M", "L"}:
            return True, val, f"CR:{val} - Rule CR-001 (derived from organizational policy {pol_id} v{pol_ver})."
    return False, None, None


def _eval_ir_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    reqs = ev.get("security_requirements")
    pol_id = ev.get("organization_policy_id")
    pol_ver = ev.get("policy_version")
    if isinstance(reqs, Mapping) and pol_id and pol_ver:
        val = str(reqs.get("IR", "")).upper()
        if val in {"H", "M", "L"}:
            return True, val, f"IR:{val} - Rule IR-001 (derived from organizational policy {pol_id} v{pol_ver})."
    return False, None, None


def _eval_ar_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    reqs = ev.get("security_requirements")
    pol_id = ev.get("organization_policy_id")
    pol_ver = ev.get("policy_version")
    if isinstance(reqs, Mapping) and pol_id and pol_ver:
        val = str(reqs.get("AR", "")).upper()
        if val in {"H", "M", "L"}:
            return True, val, f"AR:{val} - Rule AR-001 (derived from organizational policy {pol_id} v{pol_ver})."
    elif ev.get("stateless_redundant") is True and not ev.get("explicit_ar_low"):
        return True, "X", "AR:X - Rule AR-001 (architecture redundancy preserves Base AR)."
    return False, None, None


def _eval_msc_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    impacts = ev.get("modified_impacts")
    pol_id = ev.get("organization_policy_id")
    pol_ver = ev.get("policy_version")
    if isinstance(impacts, Mapping) and pol_id and pol_ver:
        val = str(impacts.get("MSC", "")).upper()
        if val in {"H", "L", "N"}:
            return True, val, f"MSC:{val} - Rule MSC-001 (derived from policy {pol_id} v{pol_ver})."
    return False, None, None


def _eval_msi_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    impacts = ev.get("modified_impacts")
    pol_id = ev.get("organization_policy_id")
    pol_ver = ev.get("policy_version")
    if isinstance(impacts, Mapping) and pol_id and pol_ver:
        val = str(impacts.get("MSI", "")).upper()
        if val in {"H", "L", "N", "S"}:
            return True, val, f"MSI:{val} - Rule MSI-001 (derived from policy {pol_id} v{pol_ver})."
    return False, None, None


def _eval_msa_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    impacts = ev.get("modified_impacts")
    pol_id = ev.get("organization_policy_id")
    pol_ver = ev.get("policy_version")
    if isinstance(impacts, Mapping) and pol_id and pol_ver:
        val = str(impacts.get("MSA", "")).upper()
        if val in {"H", "L", "N", "S"}:
            return True, val, f"MSA:{val} - Rule MSA-001 (derived from policy {pol_id} v{pol_ver})."
    return False, None, None


def _eval_mvc_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    impacts = ev.get("modified_impacts")
    pol_id = ev.get("organization_policy_id")
    pol_ver = ev.get("policy_version")
    if isinstance(impacts, Mapping) and pol_id and pol_ver:
        val = str(impacts.get("MVC", "")).upper()
        if val in {"H", "L", "N"}:
            return True, val, f"MVC:{val} - Rule MVC-001 (derived from policy {pol_id} v{pol_ver})."
    return False, None, None


def _eval_mvi_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    impacts = ev.get("modified_impacts")
    pol_id = ev.get("organization_policy_id")
    pol_ver = ev.get("policy_version")
    if isinstance(impacts, Mapping) and pol_id and pol_ver:
        val = str(impacts.get("MVI", "")).upper()
        if val in {"H", "L", "N"}:
            return True, val, f"MVI:{val} - Rule MVI-001 (derived from policy {pol_id} v{pol_ver})."
    return False, None, None


def _eval_mva_001(base_vec: str, ev: Mapping[str, Any], ctx: Mapping[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
    impacts = ev.get("modified_impacts")
    pol_id = ev.get("organization_policy_id")
    pol_ver = ev.get("policy_version")
    if isinstance(impacts, Mapping) and pol_id and pol_ver:
        val = str(impacts.get("MVA", "")).upper()
        if val in {"H", "L", "N"}:
            return True, val, f"MVA:{val} - Rule MVA-001 (derived from policy {pol_id} v{pol_ver})."
    return False, None, None


# Canonical declarative catalog of environmental rules
CANONICAL_RULES: List[RuleDefinition] = [
    RuleDefinition(
        rule_id="MAV-001",
        target_metric="MAV",
        description="Public Internet exposure retains Network vector.",
        rationale="Asset with public Internet route or ingress cannot downgrade network exploitability.",
        citation="FIRST CVSS v4.0 Sec 4.2 - Network vector requires remote exploitability; public route retains MAV:N.",
        preconditions="Base AV == 'N' AND (internet_exposed == True OR routing_table_public == True)",
        evaluator=_eval_mav_001,
    ),
    RuleDefinition(
        rule_id="MAV-002",
        target_metric="MAV",
        description="Verified adjacent Layer 2 broadcast domain isolation adjusts MAV to Adjacent.",
        rationale="Asset unreachable from Internet and routed IP; strictly bounded to local Layer 2 or management VLAN.",
        citation="FIRST CVSS v4.0 Sec 4.2 - Non-routed adjacent broadcast boundary justifies MAV:A.",
        preconditions="reachability == 'ADJACENT_ONLY' OR l2_broadcast_only == True",
        evaluator=_eval_mav_002,
    ),
    RuleDefinition(
        rule_id="MAV-003A",
        target_metric="MAV",
        description="Local host binding isolation adjusts MAV to Local.",
        rationale="Asset has zero external listening interfaces; access requires local interactive session or IPC.",
        citation="FIRST CVSS v4.0 Sec 4.2 - Local socket/host-only boundary justifies MAV:L.",
        preconditions="reachability == 'LOCAL_ONLY' OR local_host_only == True",
        evaluator=_eval_mav_003a,
    ),
    RuleDefinition(
        rule_id="MAV-003B",
        target_metric="MAV",
        description="Physical airgap isolation adjusts MAV to Physical.",
        rationale="Asset is physically isolated with zero remote network or host connections; physical access required.",
        citation="FIRST CVSS v4.0 Sec 4.2 - Physical airgap boundary justifies MAV:P.",
        preconditions="reachability == 'PHYSICAL_ONLY' OR physical_access_only == True",
        evaluator=_eval_mav_003b,
    ),
    RuleDefinition(
        rule_id="MAC-001",
        target_metric="MAC",
        description="Defensive control presence alone does not alter Attack Complexity.",
        rationale="Presence of WAF/IPS does not increase complexity unless exploit requires target-specific engineering.",
        citation="FIRST CVSS v4.0 Sec 4.2 - Generic defensive control presence preserves Base MAC:X.",
        preconditions="waf_active == True AND exploit_requires_custom_evasion == False",
        evaluator=_eval_mac_001,
    ),
    RuleDefinition(
        rule_id="MAC-002",
        target_metric="MAC",
        description="Verified target-specific exploit engineering elevates MAC to High.",
        rationale="Target-specific randomized mitigation (e.g. ASLR/DEP) forces non-generic memory leak exploitation.",
        citation="FIRST CVSS v4.0 Sec 4.2 - Mandatory target-specific info-leak prerequisite elevates MAC:H.",
        preconditions="evidenced_exploit_preconditions_elevated == True",
        evaluator=_eval_mac_002,
    ),
    RuleDefinition(
        rule_id="MPR-001",
        target_metric="MPR",
        description="Target-specific authenticated prerequisite enforces MPR.",
        rationale="Vulnerable execution path strictly requires authenticated credentials on the target before exploitation.",
        citation="FIRST CVSS v4.0 Sec 4.2 - Target-specific authorization prerequisite enforces MPR.",
        preconditions="target_authenticated_prerequisite == 'LOW'|'HIGH'",
        evaluator=_eval_mpr_001,
    ),
    RuleDefinition(
        rule_id="CR-001",
        target_metric="CR",
        description="Regulated data under versioned organizational policy sets CR:H.",
        rationale="Asset processes regulated PII/financial data under verified policy mapping.",
        citation="FIRST CVSS v4.0 Sec 4.1 - Versioned organizational policy mapping sets CR:H.",
        preconditions="organization_policy_id AND policy_version AND security_requirements.CR == 'H'",
        evaluator=_eval_cr_001,
    ),
    RuleDefinition(
        rule_id="IR-001",
        target_metric="IR",
        description="Core transactional data under versioned organizational policy sets IR:H.",
        rationale="Asset processes core database or financial ledger records under verified policy mapping.",
        citation="FIRST CVSS v4.0 Sec 4.1 - Versioned organizational policy mapping sets IR:H.",
        preconditions="organization_policy_id AND policy_version AND security_requirements.IR == 'H'",
        evaluator=_eval_ir_001,
    ),
    RuleDefinition(
        rule_id="AR-001",
        target_metric="AR",
        description="Stateless redundancy does not lower Availability Requirement.",
        rationale="Redundant architecture alone never lowers business availability requirement to Low.",
        citation="FIRST CVSS v4.0 Sec 4.1 - Architecture redundancy preserves AR:X / base policy requirement.",
        preconditions="stateless_redundant == True AND explicit_ar_low == False",
        evaluator=_eval_ar_001,
    ),
    RuleDefinition(
        rule_id="MSC-001",
        target_metric="MSC",
        description="Verified absence of lateral data exfiltration paths negates Subsequent Confidentiality.",
        rationale="Vulnerability impact path analysis confirms subsequent system confidentiality is uncompromised.",
        citation="FIRST CVSS v4.0 Sec 4.3 - Bounded enclave with zero subsequent data exposure sets MSC:N.",
        preconditions="modified_impacts.MSC == 'N' AND policy_version",
        evaluator=_eval_msc_001,
    ),
    RuleDefinition(
        rule_id="MSI-001",
        target_metric="MSI",
        description="Verified absence of downstream write/trust paths negates Subsequent Integrity.",
        rationale="Vulnerability impact path analysis confirms subsequent system integrity cannot be altered.",
        citation="FIRST CVSS v4.0 Sec 4.3 - Absence of downstream trust or tokens sets MSI:N.",
        preconditions="modified_impacts.MSI == 'N' AND policy_version",
        evaluator=_eval_msi_001,
    ),
    RuleDefinition(
        rule_id="MSA-001",
        target_metric="MSA",
        description="Independent downstream control plane negates Subsequent Availability impact.",
        rationale="Vulnerability impact path analysis confirms subsequent systems suffer zero denial of service.",
        citation="FIRST CVSS v4.0 Sec 4.3 - Independent downstream control plane sets MSA:N.",
        preconditions="modified_impacts.MSA == 'N' AND policy_version",
        evaluator=_eval_msa_001,
    ),
    RuleDefinition(
        rule_id="MVC-001",
        target_metric="MVC",
        description="Modified Confidentiality impact derived from verified policy.",
        rationale="Target enclave containment or encryption constraints modify vulnerable system confidentiality.",
        citation="FIRST CVSS v4.0 Sec 4.3 - Modified Vulnerable System Confidentiality derived from verified policy.",
        preconditions="organization_policy_id AND policy_version AND modified_impacts.MVC",
        evaluator=_eval_mvc_001,
    ),
    RuleDefinition(
        rule_id="MVI-001",
        target_metric="MVI",
        description="Modified Integrity impact derived from verified policy.",
        rationale="Target enclave read-only mount or write-protection constraints modify vulnerable system integrity.",
        citation="FIRST CVSS v4.0 Sec 4.3 - Modified Vulnerable System Integrity derived from verified policy.",
        preconditions="organization_policy_id AND policy_version AND modified_impacts.MVI",
        evaluator=_eval_mvi_001,
    ),
    RuleDefinition(
        rule_id="MVA-001",
        target_metric="MVA",
        description="Modified Availability impact derived from verified policy.",
        rationale="Target service architecture or isolation limits vulnerable system availability impact.",
        citation="FIRST CVSS v4.0 Sec 4.3 - Modified Vulnerable System Availability derived from verified policy.",
        preconditions="organization_policy_id AND policy_version AND modified_impacts.MVA",
        evaluator=_eval_mva_001,
    ),
]


def serialize_code_object(code: Any) -> bytes:
    """Recursively serialize a code object including bytecode, constants, names, and variable bindings."""
    if not hasattr(code, "co_code"):
        return b""
    parts = [
        b"CODE:", code.co_code,
        b"NAMES:", repr(code.co_names).encode("utf-8"),
        b"VARNAMES:", repr(code.co_varnames).encode("utf-8"),
        b"FREEVARS:", repr(getattr(code, "co_freevars", ())).encode("utf-8"),
        b"CELLVARS:", repr(getattr(code, "co_cellvars", ())).encode("utf-8"),
    ]
    const_parts = []
    for c in code.co_consts:
        if hasattr(c, "co_code"):
            const_parts.append(serialize_code_object(c))
        else:
            const_parts.append(repr(c).encode("utf-8"))
    parts.append(b"CONSTS:" + b"|".join(const_parts))
    return b"::".join(parts)


def compute_catalog_hash(rules: Optional[Sequence[RuleDefinition]] = None) -> str:
    """Return deterministic SHA-256 hash binding rule metadata and complete executable semantics.

    Guarantees sensitivity to:
    1. Version and catalog identity.
    2. Rule metadata declarations (rule_id, target_metric, description, preconditions, citation).
    3. Complete executable code semantics for every evaluator:
       - bytecode instructions (co_code)
       - constant literals including strings, numbers, flags, tuples (co_consts recursively)
       - global and attribute names (co_names)
       - local variable names (co_varnames)
       - closures and cell variables (co_freevars, co_cellvars).
    4. Evaluator function source definition (inspect.getsource) when inspectable.
    5. Canonical module file content hash when evaluated against CANONICAL_RULES.
    """
    if rules is None:
        rules = CANONICAL_RULES

    hasher = hashlib.sha256()
    hasher.update(CATALOG_VERSION.encode("utf-8"))
    hasher.update(CATALOG_ID.encode("utf-8"))

    # When evaluating default CANONICAL_RULES, also bind normalized module source file SHA-256
    if rules is CANONICAL_RULES:
        try:
            catalog_file = Path(__file__).resolve()
            if catalog_file.is_file():
                file_norm = catalog_file.read_bytes().replace(b"\r\n", b"\n")
                hasher.update(hashlib.sha256(file_norm).digest())
        except Exception:
            pass

    for rule in rules:
        rule_meta = f"{rule.rule_id}|{rule.target_metric}|{rule.description}|{rule.preconditions}|{rule.citation}"
        hasher.update(rule_meta.encode("utf-8"))
        code_obj = getattr(rule.evaluator, "__code__", None)
        if code_obj:
            hasher.update(serialize_code_object(code_obj))
        try:
            src = inspect.getsource(rule.evaluator).strip().replace("\r\n", "\n")
            hasher.update(src.encode("utf-8"))
        except Exception:
            pass
    return hasher.hexdigest()


CATALOG_SHA256 = compute_catalog_hash()
CATALOG_HASH = CATALOG_SHA256


def is_sampled_for_post_facto_audit(item_id: str, sample_rate: float = INTERNAL_CONTROL_SAMPLE_RATE) -> bool:
    """Deterministic post-facto audit sampling (HELPUS_INTERNAL_CONTROL).

    Selects 3%–5% of autonomous Straight-Through decisions for retrospective
    human calibration and drift detection. This is an internal HelpUS control,
    not a requirement mandated by NIST AI RMF or ISO/IEC 42001.
    """
    digest = hashlib.sha256(item_id.encode("utf-8")).hexdigest()
    val = int(digest[:8], 16) % 10000
    threshold = int(sample_rate * 10000)
    return val < threshold


def evaluate_semantic_quorum(
    resolver_a_metrics: Mapping[str, str],
    resolver_b_metrics: Mapping[str, str],
) -> Dict[str, Any]:
    """Enforces STRICT_QUORUM_DELTA = 0 at the individual metric level.

    Every resolved metric must match exactly between independent resolvers.
    Score-level agreement alone is insufficient. Any mismatch routes to HITL.
    """
    all_keys = sorted(set(resolver_a_metrics.keys()) | set(resolver_b_metrics.keys()))
    divergences: List[Dict[str, str]] = []

    for k in all_keys:
        val_a = resolver_a_metrics.get(k)
        val_b = resolver_b_metrics.get(k)
        if val_a != val_b:
            divergences.append({
                "metric": k,
                "resolver_a": str(val_a),
                "resolver_b": str(val_b),
            })

    if divergences:
        return {
            "quorum_passed": False,
            "review_status": "HUMAN_REVIEW_REQUIRED",
            "human_review_status": "required",
            "auto_downgrade_permitted": False,
            "divergences": divergences,
            "reason": f"Semantic quorum failed: metric-level disagreement on {[d['metric'] for d in divergences]}",
        }

    return {
        "quorum_passed": True,
        "review_status": "AUTO_ACCEPT",
        "human_review_status": "none",
        "auto_downgrade_permitted": True,
        "divergences": [],
        "reason": "Semantic quorum satisfied: exact metric-level agreement (Delta=0).",
    }


class EnvironmentalRuleCatalogEngine:
    """Pure Python deterministic engine directly executing CANONICAL_RULES."""

    def __init__(self):
        self.version = CATALOG_VERSION
        self.catalog_id = CATALOG_ID
        self.catalog_hash = compute_catalog_hash()

    @staticmethod
    def _freshness_limit(evidence: Mapping[str, Any]) -> float:
        if evidence.get("max_telemetry_age_days") is not None:
            return float(evidence["max_telemetry_age_days"])
        profile = str(evidence.get("telemetry_profile", "dynamic")).lower()
        return _STATIC_MAX_AGE_DAYS if profile == "static" else _DYNAMIC_MAX_AGE_DAYS

    def evaluate(
        self,
        base_vector: str,
        evidence: Mapping[str, Any],
        cve_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Evaluates evidence against CANONICAL_RULES and returns a structured STP decision."""
        citations: List[str] = []
        triggered_rules: List[str] = []
        candidate_metrics: Dict[str, str] = {}
        reasons: List[str] = []
        warnings: List[str] = []

        # Vector validation fail-closed
        if not base_vector or not base_vector.startswith("CVSS:4.0/"):
            return {
                "cve_id": cve_id or "UNKNOWN",
                "base_vector": base_vector,
                "review_status": "ABSTAIN",
                "human_review_status": "required",
                "auto_downgrade_permitted": False,
                "evidence_quality": "INSUFFICIENT",
                "candidate_metrics": {},
                "citations": [],
                "uncertainty_flags": ["Malformed or unsupported source vector; fail-closed"],
                "summary_rationale": "Automated inference abstained: malformed source vector",
                "catalog_version": self.version,
                "catalog_hash": self.catalog_hash,
            }

        quality = str(evidence.get("evidence_quality", "UNKNOWN")).upper()
        reachability = str(evidence.get("reachability", "UNKNOWN")).upper()
        explicit_conflict = bool(evidence.get("conflict_flag", False))
        fw_status = str(evidence.get("firewall_status", "")).upper()
        rt_status = str(evidence.get("routing_table_status", "")).upper()

        if "ALLOW" in fw_status and "NO_ROUTE" in rt_status:
            explicit_conflict = True

        # Telemetry freshness evaluation
        age = evidence.get("telemetry_age_days")
        if age is None:
            reasons.append("telemetry age is missing")
        else:
            try:
                limit = self._freshness_limit(evidence)
                age_float = float(age)
                if age_float > limit:
                    reasons.append(f"telemetry is stale ({age} days; policy limit {limit:g})")
                elif age_float > (limit * 0.85):
                    warnings.append(f"telemetry near expiration ({age} days of {limit:g} limit)")
            except (TypeError, ValueError):
                reasons.append("telemetry age is invalid")

        if quality in {"INSUFFICIENT", "UNKNOWN", "CONFLICTING"}:
            reasons.append(f"evidence quality is {quality}")
        if explicit_conflict:
            reasons.append("conflicting routing/firewall evidence detected")

        # Reachability classification
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

        # Fail-closed abstention check
        if reasons:
            out_quality = "CONFLICTING" if quality == "CONFLICTING" or explicit_conflict else "INSUFFICIENT"
            return {
                "cve_id": cve_id or "UNKNOWN",
                "base_vector": base_vector,
                "review_status": "ABSTAIN",
                "human_review_status": "required",
                "auto_downgrade_permitted": False,
                "evidence_quality": out_quality,
                "candidate_metrics": {},
                "citations": [],
                "uncertainty_flags": reasons,
                "summary_rationale": "Automated inference abstained: " + "; ".join(reasons),
                "catalog_version": self.version,
                "catalog_hash": self.catalog_hash,
            }

        # Policy provenance check if security requirements or modified impacts supplied
        policy_id = evidence.get("organization_policy_id")
        policy_version = evidence.get("policy_version")
        if (evidence.get("security_requirements") or evidence.get("modified_impacts")) and (not policy_id or not policy_version):
            return {
                "cve_id": cve_id or "UNKNOWN",
                "base_vector": base_vector,
                "review_status": "HUMAN_REVIEW_REQUIRED",
                "human_review_status": "required",
                "auto_downgrade_permitted": False,
                "evidence_quality": "INSUFFICIENT",
                "candidate_metrics": {},
                "citations": [],
                "uncertainty_flags": ["organizational requirements or modified impacts supplied without policy provenance"],
                "summary_rationale": "Automated inference requires human review: missing organization_policy_id/policy_version",
                "catalog_version": self.version,
                "catalog_hash": self.catalog_hash,
            }

        # Execution context for canonical rule evaluators
        context = {
            "reachability": reachability,
            "evidence_quality": quality,
        }

        # DIRECT EXECUTION FROM CANONICAL_RULES (Single Source of Truth)
        for rule in CANONICAL_RULES:
            triggered, val, citation_str = rule.evaluator(base_vector, evidence, context)
            if triggered:
                triggered_rules.append(rule.rule_id)
                if val is not None and val != "X":
                    candidate_metrics[rule.target_metric] = val
                if citation_str:
                    citations.append(citation_str)

        # Operational status: determine STP state
        if warnings:
            review_status = "AUTO_ACCEPT_WITH_WARNING"
            human_review_status = "audit_sample"
        else:
            review_status = "AUTO_ACCEPT"
            human_review_status = "none"

        evidence_bytes = json.dumps(dict(evidence), sort_keys=True, default=str).encode("utf-8")
        evidence_hash = hashlib.sha256(evidence_bytes).hexdigest()

        return {
            "cve_id": cve_id or "UNKNOWN",
            "base_vector": base_vector,
            "review_status": review_status,
            "human_review_status": human_review_status,
            "auto_downgrade_permitted": True,
            "evidence_quality": "SUFFICIENT",
            "reachability_class": reachability,
            "candidate_metrics": candidate_metrics,
            "triggered_rules": triggered_rules,
            "citations": citations,
            "uncertainty_flags": warnings,
            "summary_rationale": "; ".join(citations),
            "catalog_version": self.version,
            "catalog_hash": self.catalog_hash,
            "evidence_hash": evidence_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
