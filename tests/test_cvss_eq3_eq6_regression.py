"""Targeted regression around the coupled EQ3/EQ6 macrovector dimension.

The full FIRST reference-corpus gate remains the normative oracle. These tests
make the historically error-prone impact/security-requirement region visible in
the fast unit suite.
"""

from itertools import product

from core.cvss40 import apply_candidates, score

PARTIAL_IMPACT_VECTORS = (
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N",
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N",
)


def test_eq3_eq6_security_requirement_cross_product_scores_without_lookup_failure():
    for base in PARTIAL_IMPACT_VECTORS:
        for cr, ir, ar in product(("L", "M", "H"), repeat=3):
            vector = apply_candidates(base, {"CR": cr, "IR": ir, "AR": ar})
            result = score(vector)
            assert 0.0 <= result["score"] <= 10.0
            macro = str(result["macro_vector"])
            assert len(macro) == 6
            assert macro.isdigit()


def test_eq3_eq6_cross_product_is_deterministic_on_repeat():
    base = PARTIAL_IMPACT_VECTORS[0]
    vectors = [
        apply_candidates(base, {"CR": cr, "IR": ir, "AR": ar})
        for cr, ir, ar in product(("L", "M", "H"), repeat=3)
    ]
    first = [(v, score(v)["score"], score(v)["macro_vector"]) for v in vectors]
    second = [(v, score(v)["score"], score(v)["macro_vector"]) for v in vectors]
    assert second == first
