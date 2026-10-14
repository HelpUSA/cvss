import pytest
from pathlib import Path

def test_expert_portal_has_no_answer_leakage():
    root = Path(__file__).resolve().parent.parent
    expert_file = root / "experts" / "index.html"
    portal_file = root / "portal-especialistas.html"
    
    assert expert_file.exists(), "experts/index.html must exist"
    assert portal_file.exists(), "portal-especialistas.html must exist"
    
    content = expert_file.read_text(encoding="utf-8")
    
    # Assert blinding: no ground truth or vector leakage in expert bundle
    assert "official_vector" not in content, "Leaked official_vector found in expert bundle"
    assert "base_score" not in content, "Leaked base_score found in expert bundle"
    assert "base_severity" not in content, "Leaked base_severity found in expert bundle"
    assert "CR:H - " not in content, "Leaked CR hint found in expert bundle"
    assert "IR:H - " not in content, "Leaked IR hint found in expert bundle"
    assert "AR:H - " not in content, "Leaked AR hint found in expert bundle"

def test_expert_portal_has_synthetic_demonstration_banner():
    root = Path(__file__).resolve().parent.parent
    expert_file = root / "experts" / "index.html"
    content = expert_file.read_text(encoding="utf-8")
    
    assert "SYNTHETIC DEMONSTRATION" in content, "Persistent synthetic banner missing"
    assert "G9 PENDING ETHICS APPROVAL" in content, "G9 pending status notice missing"

def test_expert_portal_options_start_unanswered():
    root = Path(__file__).resolve().parent.parent
    expert_file = root / "experts" / "index.html"
    content = expert_file.read_text(encoding="utf-8")
    
    # Must have disabled placeholder option
    assert 'option value="" disabled selected' in content, "Unanswered placeholder option missing"
