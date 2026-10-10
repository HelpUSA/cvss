#!/usr/bin/env python3
"""Guard against reintroduction of known Round-3 scientific/editorial errors."""
from pathlib import Path
import re, sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'book_latex')
files=list(root.rglob('*.tex'))
text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in files)
checks={
    'legacy nP3 typo': r'\bnP3_MONITOR\b',
    'manual CVSS metric delta': r'MAV:[A-Z]\s*=\s*-?0\.|MPR:[A-Z]\s*=\s*-?\d',
    'official FIRST calculator claim': r'official\s+FIRST\s+(calculator|engine)',
    'NVD Official wording': r'NVD\s+Official|Official\s+NVD',
    'deprecated case CVE-2023-39417': r'CVE-2023-39417',
    'wrong EQ1 bundle': r'EQ1[^\n]{0,100}AV[^\n]{0,40}AC[^\n]{0,40}AT[^\n]{0,40}PR[^\n]{0,40}UI',
}
errors=[]
for name,pat in checks.items():
    if re.search(pat,text,re.I): errors.append(name)
print({'errors':errors,'tex_files':len(files)})
raise SystemExit(2 if errors else 0)
