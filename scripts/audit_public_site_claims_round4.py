#!/usr/bin/env python3
"""Fail the production-copy gate if unsupported claims remain on the custom domain."""
import json, re, sys
from urllib.request import Request, urlopen

URL=sys.argv[1] if len(sys.argv)>1 else 'https://cvss.helpusbr.com/'
patterns={
  'validated_30': r'30\s+Cen[aá]rios\s+Validados|30\s+Validated\s+Scenarios|30\s+Escenarios\s+Validados',
  'zero_hallucination': r'zero\s+hallucination|zero\s+alucina|sem\s+alucina|sin\s+alucina',
  'guaranteed_math': r'garantia\s+de\s+conformidade\s+matem[aá]tica|mathematical\s+compliance\s+guarantee|garant[ií]a\s+de\s+conformidad\s+matem[aá]tica',
  'nvd_official': r'NVD\s+Oficial|Official\s+NVD|NVD\s+Official',
  'traceability_100': r'100%[^<\n]{0,80}(rastreabilidade|traceability|trazabilidad)|(rastreabilidade|traceability|trazabilidad)[^<\n]{0,80}100%',
  'rfc8785_unqualified': r'RFC\s*8785(?![^<\n]{0,120}(pending|pendente|pendiente|compatible|compat[ií]vel))',
  'immutable': r'Contrato\s+Tripartite\s+Imut[aá]vel|Immutable\s+Tripartite\s+Contract|immutable\s+proof',
}
req=Request(URL,headers={'User-Agent':'HelpUS-Scientific-Copy-Audit/1.0'})
html=urlopen(req,timeout=30).read().decode('utf-8','replace')
hits={k:bool(re.search(v,html,re.I)) for k,v in patterns.items()}
result={'url':URL,'http_content_bytes':len(html.encode()),'prohibited_claim_hits':hits,'pass':not any(hits.values())}
print(json.dumps(result,indent=2,ensure_ascii=False))
raise SystemExit(0 if result['pass'] else 2)
