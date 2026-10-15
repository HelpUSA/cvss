"""Reference-backed sensitivity analysis helpers for HELPUS CVSS AI.

This module sits outside the canonical scorer. It does not invent new CVSS
semantics and it does not decide ABSTAIN policy. It only enumerates admissible
Threat/Environmental candidate values and asks core.cvss40 for the resulting
score.
"""
from __future__ import annotations

import itertools
from typing import Dict, Iterable, Mapping, Sequence

from core.cvss40 import CANDIDATE_METRICS, apply_candidates, score


class SensitivityAnalysisError(ValueError):
    """Raised when a requested sensitivity domain is invalid or too large."""


def _normalize_domains(metric_domains: Mapping[str, Iterable[str]]) -> Dict[str, Sequence[str]]:
    normalized: Dict[str, Sequence[str]] = {}
    for metric, raw_values in metric_domains.items():
        if metric not in CANDIDATE_METRICS:
            raise SensitivityAnalysisError(
                f"{metric} is not a Threat/Environmental candidate metric"
            )
        values = tuple(dict.fromkeys(raw_values))
        if not values:
            raise SensitivityAnalysisError(f"{metric} has an empty sensitivity domain")
        invalid = [value for value in values if value not in CANDIDATE_METRICS[metric]]
        if invalid:
            raise SensitivityAnalysisError(
                f"invalid values for {metric}: {','.join(map(str, invalid))}"
            )
        normalized[metric] = values
    return normalized


def score_envelope(
    base_vector: str,
    metric_domains: Mapping[str, Iterable[str]],
    *,
    max_combinations: int = 4096,
) -> Dict[str, object]:
    """Enumerate candidate domains and return the exact score envelope.

    invariant=True means every admissible assignment produced the same scalar
    score. That proves score invariance only; the underlying evidence can still
    be unresolved.
    """
    domains = _normalize_domains(metric_domains)
    if not domains:
        result = score(base_vector)
        return {
            "min_score": result["score"],
            "max_score": result["score"],
            "unique_scores": [result["score"]],
            "invariant": True,
            "combinations_evaluated": 1,
        }

    metric_names = tuple(domains)
    combination_count = 1
    for name in metric_names:
        combination_count *= len(domains[name])
    if combination_count > max_combinations:
        raise SensitivityAnalysisError(
            f"sensitivity domain expands to {combination_count} combinations; "
            f"limit is {max_combinations}"
        )

    scores = []
    for values in itertools.product(*(domains[name] for name in metric_names)):
        candidates = dict(zip(metric_names, values))
        vector = apply_candidates(base_vector, candidates)
        scores.append(float(score(vector)["score"]))

    unique_scores = sorted(set(scores))
    return {
        "min_score": min(scores),
        "max_score": max(scores),
        "unique_scores": unique_scores,
        "invariant": len(unique_scores) == 1,
        "combinations_evaluated": combination_count,
    }


def envelope_is_non_expanding(
    previous: Mapping[str, float],
    current: Mapping[str, float],
) -> bool:
    """Return True when current score bounds are contained in previous bounds."""
    return (
        float(current["min_score"]) >= float(previous["min_score"])
        and float(current["max_score"]) <= float(previous["max_score"])
    )
