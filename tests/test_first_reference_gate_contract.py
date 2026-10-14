from pathlib import Path


def test_round4_first_gate_runner_is_strict_and_persists_all_mismatches():
    p = Path(__file__).resolve().parents[1] / "scripts" / "run_first_reference_corpus_round4.py"
    text = p.read_text(encoding="utf-8")
    assert '"gate_pass": failed == 0' in text
    assert '"mismatches": [r for r in rows if r["status"] != "PASS"]' in text
    assert "len(mismatches) <" not in text
