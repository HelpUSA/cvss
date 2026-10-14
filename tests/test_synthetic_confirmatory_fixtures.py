from __future__ import annotations

import json
from pathlib import Path


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_synthetic_c1_fixture_is_explicitly_non_confirmatory():
    data = _load("synthetic_confirmatory_c1_sample.json")
    assert data["synthetic_only"] is True
    assert data["generated_without_access_to_real_c1"] is True
    assert data["cases"]
    for case in data["cases"]:
        assert case["case_id"].startswith("SYN-C1-")
        assert "source_cvss_vector" in case
        assert "evidence" in case
        assert "oracle" in case


def test_synthetic_c2_fixture_declares_metamorphic_relations():
    data = _load("synthetic_confirmatory_c2_sample.json")
    assert data["synthetic_only"] is True
    assert data["generated_without_access_to_real_c2"] is True
    relations = {item["relation"] for item in data["metamorphic_cases"]}
    assert relations == {
        "MONOTONIC_HARDENING",
        "SUBSEQUENT_SYSTEM_CONFINEMENT",
        "NOISE_INVARIANCE",
        "INGESTION_COMMUTATIVITY",
    }
    for item in data["metamorphic_cases"]:
        assert item["relation_id"].startswith("MR-")
        assert item["precondition"]
        assert item["original"]
        assert item["mutated"]
        assert item["invariant"]


def test_synthetic_fixture_ids_do_not_claim_real_confirmatory_provenance():
    c1 = _load("synthetic_confirmatory_c1_sample.json")
    c2 = _load("synthetic_confirmatory_c2_sample.json")

    serialized = json.dumps({"c1": c1, "c2": c2})
    assert "data/c1_real_world_benchmark.json" not in serialized
    assert "data/c2_adversarial_metamorphic_benchmark.json" not in serialized
    assert "SYNTH-CVE-" in serialized
