"""CVSS v4.0 scoring layer aligned with the FIRST specification.

Scores are computed by the ``cvss`` library (RedHat implementation of the
FIRST CVSS v4.0 MacroVector algorithm). This module adds:

* strict validation of metric names and values;
* the CVSS v4.0 nomenclature (CVSS-B, CVSS-BT, CVSS-BE, CVSS-BTE);
* a guarded merge of *candidate* Environmental/Threat metrics into a
  source CVSS v4.0 vector. Candidates can never override Base metrics, which
  keeps the source assessment separate from consumer-side context.

No heuristic adjustment is applied here. Every score returned by this module
is a CVSS v4.0 score computed from a vector.
"""
from __future__ import annotations

from typing import Dict, Mapping, Optional

from cvss import CVSS4
from cvss.exceptions import CVSS4Error

PREFIX = "CVSS:4.0"

BASE_METRICS: Dict[str, frozenset] = {
    "AV": frozenset("NALP"),
    "AC": frozenset("LH"),
    "AT": frozenset("NP"),
    "PR": frozenset("NLH"),
    "UI": frozenset("NPA"),
    "VC": frozenset("HLN"),
    "VI": frozenset("HLN"),
    "VA": frozenset("HLN"),
    "SC": frozenset("HLN"),
    "SI": frozenset("HLN"),
    "SA": frozenset("HLN"),
}

THREAT_METRICS: Dict[str, frozenset] = {
    "E": frozenset("XAPU"),
}

ENVIRONMENTAL_METRICS: Dict[str, frozenset] = {
    "CR": frozenset("XHML"),
    "IR": frozenset("XHML"),
    "AR": frozenset("XHML"),
    "MAV": frozenset("XNALP"),
    "MAC": frozenset("XLH"),
    "MAT": frozenset("XNP"),
    "MPR": frozenset("XNLH"),
    "MUI": frozenset("XNPA"),
    "MVC": frozenset("XHLN"),
    "MVI": frozenset("XHLN"),
    "MVA": frozenset("XHLN"),
    "MSC": frozenset("XHLN"),
    "MSI": frozenset("XSHLN"),
    "MSA": frozenset("XSHLN"),
}

SUPPLEMENTAL_METRICS: Dict[str, frozenset] = {
    "S": frozenset({"X", "N", "P"}),
    "AU": frozenset({"X", "N", "Y"}),
    "R": frozenset({"X", "A", "U", "I"}),
    "V": frozenset({"X", "D", "C"}),
    "RE": frozenset({"X", "L", "M", "H"}),
    "U": frozenset({"X", "Clear", "Green", "Amber", "Red"}),
}

ALL_METRICS: Dict[str, frozenset] = {
    **BASE_METRICS,
    **THREAT_METRICS,
    **ENVIRONMENTAL_METRICS,
    **SUPPLEMENTAL_METRICS,
}

# Canonical ordering from the CVSS v4.0 specification.
METRIC_ORDER = tuple(ALL_METRICS)

#: Metrics that a watcher/analyst candidate is allowed to propose.
CANDIDATE_METRICS: Dict[str, frozenset] = {**THREAT_METRICS, **ENVIRONMENTAL_METRICS}


class CVSS40ValidationError(ValueError):
    """Raised when a vector or candidate metric set is invalid."""


def parse_vector(vector: str) -> Dict[str, str]:
    """Parse and strictly validate a CVSS v4.0 vector into a metric dict."""
    if not isinstance(vector, str) or not vector.strip():
        raise CVSS40ValidationError("empty CVSS v4.0 vector")
    parts = vector.strip().split("/")
    if parts[0] != PREFIX:
        raise CVSS40ValidationError(f"vector must start with {PREFIX}: {vector!r}")

    metrics: Dict[str, str] = {}
    for segment in parts[1:]:
        if ":" not in segment:
            raise CVSS40ValidationError(f"invalid metric segment: {segment!r}")
        name, value = segment.split(":", 1)
        if name not in ALL_METRICS:
            raise CVSS40ValidationError(f"unknown CVSS v4.0 metric: {name}")
        if name in metrics:
            raise CVSS40ValidationError(f"duplicated metric: {name}")
        if value not in ALL_METRICS[name]:
            raise CVSS40ValidationError(f"invalid value {value!r} for metric {name}")
        metrics[name] = value

    missing = [name for name in BASE_METRICS if name not in metrics]
    if missing:
        raise CVSS40ValidationError("missing mandatory Base metrics: " + ",".join(missing))
    return metrics


def build_vector(metrics: Mapping[str, str]) -> str:
    """Build a canonical vector, omitting metrics set to ``X`` (Not Defined)."""
    segments = [PREFIX]
    for name in METRIC_ORDER:
        value = metrics.get(name)
        if value is None or (value == "X" and name not in BASE_METRICS):
            continue
        segments.append(f"{name}:{value}")
    return "/".join(segments)


def nomenclature(metrics: Mapping[str, str]) -> str:
    """Return CVSS-B, CVSS-BT, CVSS-BE or CVSS-BTE per the v4.0 specification."""
    has_threat = any(metrics.get(name, "X") != "X" for name in THREAT_METRICS)
    has_env = any(metrics.get(name, "X") != "X" for name in ENVIRONMENTAL_METRICS)
    return "CVSS-B" + ("T" if has_threat else "") + ("E" if has_env else "")


def score(vector: str) -> Dict[str, object]:
    """Compute the CVSS v4.0 result for a vector using the configured implementation."""
    metrics = parse_vector(vector)
    canonical = build_vector(metrics)
    try:
        computed = CVSS4(canonical)
    except CVSS4Error as exc:  # pragma: no cover - parse_vector should catch first
        raise CVSS40ValidationError(str(exc)) from exc
    return {
        "vector": canonical,
        "nomenclature": nomenclature(metrics),
        "score": float(computed.base_score),
        "severity": str(computed.severity),
        "macro_vector": computed.macroVector(),
    }


def apply_candidates(base_vector: str, candidates: Mapping[str, Optional[str]]) -> str:
    """Merge candidate Threat/Environmental metrics into a source CVSS v4.0 vector.

    Raises ``CVSS40ValidationError`` if a candidate tries to set a Base or
    Supplemental metric, or uses a value outside the specification.
    ``None`` and ``"X"`` mean "Not Defined" and leave the metric unset.
    """
    metrics = parse_vector(base_vector)
    for name, value in candidates.items():
        if name not in CANDIDATE_METRICS:
            raise CVSS40ValidationError(
                f"candidate metric {name} is not allowed; only Threat and "
                "Environmental metrics may be proposed"
            )
        if value is None:
            value = "X"
        if value not in CANDIDATE_METRICS[name]:
            raise CVSS40ValidationError(f"invalid candidate value {value!r} for {name}")
        if value == "X":
            metrics.pop(name, None)
        else:
            metrics[name] = value
    return build_vector(metrics)


def compare(base_vector: str, candidates: Mapping[str, Optional[str]]) -> Dict[str, object]:
    """Score the source vector and candidate-enriched vector side by side.

    ``official_cvss`` is retained as a deprecated compatibility alias only; new
    consumers should use ``source_cvss``.
    """
    source = score(base_vector)
    contextual = score(apply_candidates(base_vector, candidates))
    return {
        "source_cvss": source,
        "official_cvss": source,  # deprecated compatibility alias
        "candidate_cvss": contextual,
        "delta": round(contextual["score"] - source["score"], 1),
        "severity_changed": contextual["severity"] != source["severity"],
    }
