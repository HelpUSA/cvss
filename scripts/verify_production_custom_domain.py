#!/usr/bin/env python3
"""Verify production custom domain cvss.helpusbr.com smoke and language capabilities."""
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_FILE = ROOT / "outputs" / "production_custom_domain_smoke.json"
URL = "https://cvss.helpusbr.com"

req = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Antigravity/PreFreezeAudit"}
)

response_code = None
content = ""
error_msg = None

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        response_code = resp.status
        content = resp.read().decode("utf-8", errors="replace")
except Exception as e:
    error_msg = str(e)

prohibited_patterns = [
    r"30 Cen[aá]rios Validados",
    r"zero alucina",
    r"garantia de conformidade matem[aá]tica",
    r"Contrato Tripartite Imut[aá]vel"
]

found_prohibited = []
for pat in prohibited_patterns:
    if re.search(pat, content, re.IGNORECASE):
        found_prohibited.append(pat)

lang_markers = {
    "pt": bool(re.search(r"Cenários|Auditoria|Avaliador|Prioridade", content)),
    "en": bool(re.search(r"English|Language|Dataset|Severity", content)),
    "es": bool(re.search(r"Español|Evaluador|Prioridad", content)),
}

result = {
    "target_url": URL,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "http_status": response_code,
    "response_bytes": len(content),
    "prohibited_marketing_claims_detected": found_prohibited,
    "marketing_claim_audit_pass": len(found_prohibited) == 0,
    "language_capabilities_detected": lang_markers,
    "operational_console_link_present": "href=\"/app\"" in content or "href=\"/login\"" in content or "/app" in content,
    "audit_status": "PASS" if response_code == 200 and len(found_prohibited) == 0 else "FAIL",
    "error": error_msg
}

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUT_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(f"Audit output written to {OUT_FILE}: status={result['audit_status']}")
