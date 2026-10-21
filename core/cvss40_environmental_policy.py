"""
Canonical CVSS v4.0 Environmental Policy and Priority Mapping Module.

Authoritative source of truth for:
- Ordered operational priority universe P = <defer, low, medium, high, critical> (Eq. 6)
- Bijective ordinal mapping g: P -> {0, 1, 2, 3, 4} (Eq. 7)
- Qualitative CVSS-B severity to base priority mapping: P_base = severity(S_base)
- Deployment environment profiles, contextual weights w_context(e) in {-2, 0, 1, 2, 3},
  and active compensating control weights w_control(e) in {-1, 0} (Eq. 8)
- Contextual priority recomputation with clamped bounds [0, 4] (Eq. 8)
- Category delta Delta_cat = g(P_env) - g(P_base) in [-3, +2] (Eq. 9)

Pure module without top-level I/O, network requests, or execution side-effects.
Safe for direct import across seed generators, trace verifiers, and test suites.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


# ==============================================================================
# Priority Universe and Severity Mappings (Manuscript Eq. 6 - 7)
# ==============================================================================

PRIORITY_ORDER: List[str] = ["defer", "low", "medium", "high", "critical"]

SEVERITY_TO_PRIORITY: Dict[str, str] = {
    "NONE": "defer",
    "LOW": "low",
    "MEDIUM": "medium",
    "HIGH": "high",
    "CRITICAL": "critical",
}


# ==============================================================================
# Deployment Environment Profiles and Policy Weights (Manuscript Eq. 8)
# ==============================================================================

ENV_PROFILES: List[Dict[str, Any]] = [
    {
        "asset_class": "public_web_application",
        "deployment_context": "Customer-facing web application handling authenticated user data.",
        "internet_exposure": "public",
        "privilege_context": "Externally reachable service with standard user accounts.",
        "compensating_controls": "WAF enabled, centralized logging, rate limiting, standard patch window.",
        "cr": "CR:H - confidentiality is high because customer data may be processed.",
        "ir": "IR:H - integrity is high because application state may affect user transactions.",
        "ar": "AR:M - availability is medium because outage affects customer access but has fallback operations.",
        "modified": "Candidate Modified Base metrics should be reviewed against public exposure, WAF, account privileges, and deployment controls.",
        "supplemental": "Automatable and provider urgency should be reviewed if official supplemental data exists.",
        "context_weight": 2,
        "control_weight": -1,
    },
    {
        "asset_class": "internal_admin_console",
        "deployment_context": "Internal administrative interface restricted to VPN and privileged operators.",
        "internet_exposure": "restricted",
        "privilege_context": "Administrative role required after VPN authentication.",
        "compensating_controls": "VPN, MFA, network segmentation, privileged access monitoring.",
        "cr": "CR:M - confidentiality depends on administrative data visible through the console.",
        "ir": "IR:H - integrity is high because admin actions may alter production configuration.",
        "ar": "AR:M - availability is medium due to operational dependency.",
        "modified": "Candidate Modified Base metrics should review restricted network path, MFA, privileges, and segmentation.",
        "supplemental": "Recovery and provider urgency may support operational discussion.",
        "context_weight": 0,
        "control_weight": -1,
    },
    {
        "asset_class": "identity_provider",
        "deployment_context": "Identity and access management component used by multiple internal systems.",
        "internet_exposure": "restricted",
        "privilege_context": "Authentication boundary component with privileged integration tokens.",
        "compensating_controls": "MFA, conditional access, monitoring, secrets rotation, incident response playbooks.",
        "cr": "CR:H - confidentiality is high because identity data and tokens may be affected.",
        "ir": "IR:H - integrity is high because identity compromise may affect trust decisions.",
        "ar": "AR:H - availability is high because authentication outage affects many services.",
        "modified": "Candidate Modified Base metrics should review identity blast radius, token exposure, and compensating controls.",
        "supplemental": "Value density and provider urgency may be important because identity systems concentrate risk.",
        "context_weight": 2,
        "control_weight": -1,
    },
    {
        "asset_class": "database_server",
        "deployment_context": "Backend database storing regulated business records.",
        "internet_exposure": "internal",
        "privilege_context": "Access limited to application service accounts and database administrators.",
        "compensating_controls": "Network isolation, backups, encryption at rest, privileged access logging.",
        "cr": "CR:H - confidentiality is high because regulated records may be stored.",
        "ir": "IR:H - integrity is high because records are authoritative.",
        "ar": "AR:H - availability is high because dependent business processes may stop.",
        "modified": "Candidate Modified Base metrics should review internal exposure, service account privileges, backups, and isolation.",
        "supplemental": "Recovery may be relevant because backups and restore time affect operational impact.",
        "context_weight": 2,
        "control_weight": -1,
    },
    {
        "asset_class": "developer_workstation",
        "deployment_context": "Developer endpoint with access to source code, build tools, and internal repositories.",
        "internet_exposure": "restricted",
        "privilege_context": "Standard developer user with access to internal repositories and CI credentials.",
        "compensating_controls": "EDR, device management, least privilege, repository access controls.",
        "cr": "CR:M - confidentiality is medium due to source code and secrets exposure risk.",
        "ir": "IR:H - integrity is high because code or pipeline changes may affect production.",
        "ar": "AR:L - availability impact is usually limited to one endpoint.",
        "modified": "Candidate Modified Base metrics should review endpoint controls, credentials, repository access, and user interaction.",
        "supplemental": "Automatable may be relevant if exploitation can be scaled across endpoints.",
        "context_weight": 1,
        "control_weight": -1,
    },
    {
        "asset_class": "isolated_lab_system",
        "deployment_context": "Non-production lab system isolated from production networks.",
        "internet_exposure": "isolated",
        "privilege_context": "Local lab accounts only, no production credentials.",
        "compensating_controls": "Network isolation, no production data, rebuildable images.",
        "cr": "CR:L - confidentiality is low because no production data is expected.",
        "ir": "IR:L - integrity is low because lab state is disposable.",
        "ar": "AR:L - availability is low because outage has limited operational effect.",
        "modified": "Candidate Modified Base metrics should review isolation, lack of production data, and rebuildability.",
        "supplemental": "Recovery is likely favorable because lab systems are rebuildable.",
        "context_weight": -2,
        "control_weight": -1,
    },
    {
        "asset_class": "ot_monitoring_gateway",
        "deployment_context": "Operational technology monitoring gateway connected to industrial telemetry.",
        "internet_exposure": "internal",
        "privilege_context": "Restricted operator and service accounts.",
        "compensating_controls": "Network segmentation, allow-listing, monitoring, maintenance window constraints.",
        "cr": "CR:M - confidentiality is medium because operational telemetry may be sensitive.",
        "ir": "IR:H - integrity is high because telemetry may influence operational decisions.",
        "ar": "AR:H - availability is high because monitoring loss may affect operations.",
        "modified": "Candidate Modified Base metrics should review OT segmentation, safety dependency, and maintenance constraints.",
        "supplemental": "Safety and recovery should be reviewed as supplemental context.",
        "context_weight": 2,
        "control_weight": 0,
    },
    {
        "asset_class": "public_api_gateway",
        "deployment_context": "Public API gateway serving partner integrations and mobile clients.",
        "internet_exposure": "public",
        "privilege_context": "API tokens and service-to-service credentials are used.",
        "compensating_controls": "API gateway policies, rate limiting, logging, schema validation, token rotation.",
        "cr": "CR:H - confidentiality is high because API traffic may expose sensitive data.",
        "ir": "IR:H - integrity is high because API actions may change business records.",
        "ar": "AR:H - availability is high because partners and clients depend on the API.",
        "modified": "Candidate Modified Base metrics should review public exposure, token scope, rate limiting, and API controls.",
        "supplemental": "Provider urgency and automatable may support operational prioritization.",
        "context_weight": 3,
        "control_weight": -1,
    },
]

ENV_PROFILES_BY_ASSET: Dict[str, Dict[str, Any]] = {
    p["asset_class"]: p for p in ENV_PROFILES
}

CONTEXT_WEIGHTS: Dict[str, int] = {
    p["asset_class"]: int(p["context_weight"]) for p in ENV_PROFILES
}

CONTROL_WEIGHTS: Dict[str, int] = {
    p["asset_class"]: int(p["control_weight"]) for p in ENV_PROFILES
}

DEFAULT_CONTROL_WEIGHT: int = -1


# ==============================================================================
# Pure Policy Functions
# ==============================================================================

def priority_to_num(value: str) -> int:
    """Bijective ordinal mapping g(p) for p in P (Eq. 7). Identical to priority_to_ordinal."""
    val = str(value).strip().lower()
    if val not in PRIORITY_ORDER:
        raise ValueError(f"Unknown priority '{value}'. Permitted: {PRIORITY_ORDER}")
    return PRIORITY_ORDER.index(val)


def priority_to_ordinal(priority: str) -> int:
    """Bijective ordinal mapping g(p) for p in P (Eq. 7)."""
    return priority_to_num(priority)


def ordinal_to_priority(val: int) -> str:
    """Inverse mapping g^{-1}(val) clamped to valid priority index range [0, 4]."""
    clamped = max(0, min(len(PRIORITY_ORDER) - 1, int(val)))
    return PRIORITY_ORDER[clamped]


def recompute_p_base(cvss_b_severity: str) -> str:
    """P_base = severity(S_base) canonical mapping."""
    sev_upper = str(cvss_b_severity).strip().upper()
    if sev_upper not in SEVERITY_TO_PRIORITY:
        raise ValueError(f"Unknown CVSS severity '{cvss_b_severity}'")
    return SEVERITY_TO_PRIORITY[sev_upper]


def compute_delta_cat(p_base: str, p_env: str) -> int:
    """Category delta Delta_cat = g(P_env) - g(P_base) (Eq. 9)."""
    return priority_to_ordinal(p_env) - priority_to_ordinal(p_base)


def lookup_nominal_weights(asset_class: str) -> Tuple[int, int]:
    """Retrieves nominal (w_context, w_control) for a given asset profile (Eq. 8)."""
    if asset_class not in CONTEXT_WEIGHTS:
        raise ValueError(f"Unknown asset_class '{asset_class}' for nominal weight lookup")
    w_ctx = CONTEXT_WEIGHTS[asset_class]
    w_ctrl = CONTROL_WEIGHTS.get(asset_class, DEFAULT_CONTROL_WEIGHT)
    return w_ctx, w_ctrl


def adjust_priority(base_priority: str, profile: Dict[str, Any]) -> str:
    """
    Canonical priority adjustment logic from seed generator:
    g(P_env) = min(4, max(0, g(P_base) + w_context + w_control))
    """
    idx = priority_to_num(base_priority)
    idx += int(profile.get("context_weight", 0))
    idx += int(profile.get("control_weight", DEFAULT_CONTROL_WEIGHT))
    idx = max(0, min(len(PRIORITY_ORDER) - 1, idx))
    return PRIORITY_ORDER[idx]


def recompute_p_env_nominal(p_base: str, asset_class: str) -> Tuple[str, int]:
    """
    Evaluates nominal contextual priority:
    g(P_env) = min(4, max(0, g(P_base) + w_context(e) + w_control(e)))
    Returns (P_env, Delta_cat).
    """
    g_base = priority_to_ordinal(p_base)
    w_ctx, w_ctrl = lookup_nominal_weights(asset_class)
    g_env = max(0, min(len(PRIORITY_ORDER) - 1, g_base + w_ctx + w_ctrl))
    env_priority = ordinal_to_priority(g_env)
    delta_cat = g_env - g_base
    return env_priority, delta_cat
