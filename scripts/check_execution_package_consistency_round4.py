#!/usr/bin/env python3
import csv, json, re, sys
from pathlib import Path

root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
errors=[]; notes=[]

def need(path):
    p=root/path
    if not p.exists(): errors.append(f'MISSING: {path}')
    return p

# Structural completeness
for x in ['core','app','tests','scripts','web/src','web/scripts','.github/workflows/real-pipeline.yml','data/dataset_b/source_assessments_v2.csv','docs/scientific-validation/CURRENT_RELEASE_GATE_STATUS.md']:
    need(x)

# G1 cannot be PASS with mismatches.
status=need('docs/scientific-validation/CURRENT_RELEASE_GATE_STATUS.md')
if status.exists():
    txt=status.read_text(encoding='utf-8')
    if re.search(r'G1[^\n]*\bPASS\b',txt,re.I):
        out=root/'outputs/first-reference-corpus-round4.json'
        if out.exists():
            d=json.loads(out.read_text(encoding='utf-8'))
            if not d.get('summary',{}).get('gate_pass',False): errors.append('G1 marked PASS but strict corpus gate has mismatches')
        else: errors.append('G1 marked PASS without strict round4 corpus evidence')

# Expert count must be consistent and fixed before freeze.
for p in (root/'docs/scientific-validation').glob('*.md') if (root/'docs/scientific-validation').exists() else []:
    txt=p.read_text(encoding='utf-8',errors='ignore')
    if re.search(r'\b3\s+(independent\s+)?experts?\b|\b3\s+especialistas\b',txt,re.I): notes.append(f'legacy 3-expert wording: {p.name}')

# Dataset v2 semantics.
p=root/'data/dataset_b/source_assessments_v2.csv'
if p.exists():
    rows=list(csv.DictReader(p.open(encoding='utf-8')))
    if len(rows)!=30: errors.append(f'Dataset B v2 row count {len(rows)} != 30')
    for r in rows:
        if r.get('source_nomenclature')=='CVSS-BT' and not r.get('provider_reported_base_score'):
            errors.append(f"BT row missing provider base score: {r.get('scenario_id')}")

print(json.dumps({'errors':errors,'notes':notes,'error_count':len(errors),'note_count':len(notes)},indent=2))
raise SystemExit(2 if errors else 0)
