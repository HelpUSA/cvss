#!/usr/bin/env python3
"""Expanded semantic copy and governance auditor for HelpUS CVSS public surfaces.
Validates absence of unsupported claims, hardcoded reviewer identities, unproven master approval claims,
and improper NVD/RFC references across HTML snapshots and live production endpoints.
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen

TARGET = sys.argv[1] if len(sys.argv) > 1 else 'index.html'

EXPANDED_PATTERNS = {
    'validated_30': r'30\s+Cen[aá]rios\s+Validados|30\s+Validated\s+Scenarios|30\s+Escenarios\s+Validados',
    'zero_hallucination': r'zero\s+hallucination|zero\s+alucina|sem\s+alucina|sin\s+alucina',
    'guaranteed_math': r'garantia\s+de\s+conformidade\s+matem[aá]tica|mathematical\s+compliance\s+guarantee|garant[ií]a\s+de\s+conformidad\s+matem[aá]tica',
    'nvd_official': r'NVD\s+Oficial|Official\s+NVD|NVD\s+Official',
    'score_oficial_nvd': r'score\s+oficial\s+NVD',
    'cvss_base_oficial_nvd': r'CVSS\s+Base\s+Oficial\s*\(NVD\)',
    'formula_oficial_first': r'f[oó]rmula\s+oficial\s+d[ea]\s+FIRST',
    'traceability_100': r'100%[^<\n]{0,80}(rastreabilidade|traceability|trazabilidad)|(rastreabilidade|traceability|trazabilidad)[^<\n]{0,80}100%',
    'rfc8785_unqualified': r'RFC\s*8785(?![^<\n]{0,120}(pending|pendente|pendiente|compatible|compat[ií]vel))',
    'immutable': r'Contrato\s+Tripartite\s+Imut[aá]vel|Immutable\s+Tripartite\s+Contract|immutable\s+proof',
    'hardcoded_master_identity': r'helpus\.ecommerce@gmail\.com',
    'hardcoded_wagner_name': r'Wagner\s+Santos',
    'unproven_master_approval': r'Aprovado\s+pelo\s+Master',
    'stale_telemetry_window_300s': r'<\s*300s',
}

def audit_content(content_str: str, target_desc: str, response_headers: dict = None) -> dict:
    raw_bytes = content_str.encode('utf-8', errors='replace')
    sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
    
    hits = {}
    matched_snippets = {}
    for rule_name, pattern in EXPANDED_PATTERNS.items():
        matches = list(re.finditer(pattern, content_str, re.IGNORECASE))
        hits[rule_name] = bool(matches)
        if matches:
            matched_snippets[rule_name] = [m.group(0) for m in matches[:3]]
            
    passed = not any(hits.values())
    
    result = {
        'target': target_desc,
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'http_content_bytes': len(raw_bytes),
        'content_sha256': sha256_hash,
        'prohibited_claim_hits': hits,
        'matched_snippets': matched_snippets,
        'response_headers': response_headers or {},
        'pass': passed,
    }
    return result

def main():
    if TARGET.startswith(('http://', 'https://')):
        req = Request(TARGET, headers={'User-Agent': 'HelpUS-Scientific-Copy-Audit/2.0'})
        try:
            with urlopen(req, timeout=30) as resp:
                headers = dict(resp.headers)
                html = resp.read().decode('utf-8', errors='replace')
                result = audit_content(html, TARGET, headers)
        except Exception as e:
            result = {
                'target': TARGET,
                'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                'error': str(e),
                'pass': False,
            }
    else:
        if not os.path.exists(TARGET):
            print(f"Error: Target file {TARGET} not found", file=sys.stderr)
            sys.exit(1)
        with open(TARGET, 'r', encoding='utf-8', errors='replace') as f:
            html = f.read()
        result = audit_content(html, TARGET)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get('pass', False) else 2)

if __name__ == '__main__':
    main()
