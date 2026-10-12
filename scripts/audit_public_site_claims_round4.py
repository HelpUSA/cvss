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
    'unsupported_false_alert_reduction': r'reduzindo\s+o\s+falso\s+alerta|reduzindo\s+falsos?\s+alertas?|reducing\s+false\s+alerts?|reduciendo\s+falsas?\s+alertas?',
    'unsupported_crypto_signature': r'assinatura\s+criptogr[aá]fica(?![^<\n]{0,120}(exigem\s+sess[aã]o|não\s+constitui|não\s+autoritativo|simula[cç][aã]o|demo|demonstra[cç][aã]o))|carimbo\s+digital[^<\n]{0,100}integridade\s+criptogr[aá]fica\s+verific[aá]vel',
    'math_random_crypto_claim': r'Math\.random\(\)[^;\n]{0,80}(assinatura|crypto|cripto)',
    'unsupported_superadmin_master': r'SuperAdmin\s+Master',
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
    results = []
    overall_pass = True

    if TARGET.startswith(('http://', 'https://')):
        req = Request(TARGET, headers={'User-Agent': 'HelpUS-Scientific-Copy-Audit/2.0'})
        try:
            with urlopen(req, timeout=30) as resp:
                headers = dict(resp.headers)
                html = resp.read().decode('utf-8', errors='replace')
                res_html = audit_content(html, TARGET, headers)
                results.append(res_html)
                if not res_html.get('pass'):
                    overall_pass = False
        except Exception as e:
            results.append({
                'target': TARGET,
                'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                'error': str(e),
                'pass': False,
            })
            overall_pass = False

        # Audit linked production JS (app.js)
        js_url = TARGET.rstrip('/') + '/app.js'
        try:
            req_js = Request(js_url, headers={'User-Agent': 'HelpUS-Scientific-Copy-Audit/2.0'})
            with urlopen(req_js, timeout=30) as resp_js:
                js_content = resp_js.read().decode('utf-8', errors='replace')
                res_js = audit_content(js_content, js_url, dict(resp_js.headers))
                results.append(res_js)
                if not res_js.get('pass'):
                    overall_pass = False
        except Exception as e:
            # Fall back to local app.js if production server bundles or redirects
            if os.path.exists('app.js'):
                with open('app.js', 'r', encoding='utf-8', errors='replace') as f:
                    res_js = audit_content(f.read(), 'app.js (local fallback)')
                    results.append(res_js)
                    if not res_js.get('pass'):
                        overall_pass = False
    else:
        if not os.path.exists(TARGET):
            print(f"Error: Target file {TARGET} not found", file=sys.stderr)
            sys.exit(1)
        with open(TARGET, 'r', encoding='utf-8', errors='replace') as f:
            html = f.read()
        res_html = audit_content(html, TARGET)
        results.append(res_html)
        if not res_html.get('pass'):
            overall_pass = False

        # Also audit app.js if in repository
        if os.path.exists('app.js') and TARGET != 'app.js':
            with open('app.js', 'r', encoding='utf-8', errors='replace') as f:
                res_js = audit_content(f.read(), 'app.js')
                results.append(res_js)
                if not res_js.get('pass'):
                    overall_pass = False

    output = {
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'target': TARGET,
        'pass': overall_pass,
        'results': results,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    sys.exit(0 if overall_pass else 2)

if __name__ == '__main__':
    main()
