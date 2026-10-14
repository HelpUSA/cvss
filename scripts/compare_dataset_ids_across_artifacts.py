#!/usr/bin/env python3
"""Check that canonical Dataset B scenario/CVE identifiers agree across generated artifacts.

This checker does not scrape production.  Production HTML/snapshot may be passed with
--site-snapshot and is checked for unexpected CVE IDs in the Dataset-B section only if a
simple marker block is present.
"""
import argparse,csv,json,re
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--site-snapshot'); args=ap.parse_args()
root = Path(args.root)
csv_path = root / 'data/dataset_b/source_assessments_final.csv'
if not csv_path.exists():
    csv_path = root / 'data/dataset_b/source_assessments_v2.csv'
rows = list(csv.DictReader(csv_path.open(encoding='utf-8')))
ids={r['scenario_id'] for r in rows}; cves={r['cve_id'] for r in rows if r['cve_id']}
errors=[]
for rel in ['generated/dataset_b_summary.json','generated/dataset_b_public_fixture.json']:
    p=root/rel
    if not p.exists(): errors.append(f'missing {rel}'); continue
    d=json.loads(p.read_text(encoding='utf-8'))
    if rel.endswith('summary.json') and set(d.get('scenario_ids',[])) != ids: errors.append(f'{rel}: scenario IDs differ from canonical CSV')
    if rel.endswith('fixture.json') and {x['scenario_id'] for x in d.get('scenarios',[])} != ids: errors.append(f'{rel}: scenario IDs differ from canonical CSV')
if args.site_snapshot:
    txt=Path(args.site_snapshot).read_text(encoding='utf-8',errors='ignore')
    shown=set(re.findall(r'CVE-\d{4}-\d{4,7}',txt))
    unexpected=sorted(shown-cves)
    if unexpected: errors.append('site snapshot contains CVEs not present in canonical Dataset B: '+', '.join(unexpected[:30]))
print(json.dumps({'canonical_scenarios':len(ids),'canonical_real_cves':len(cves),'errors':errors},indent=2))
raise SystemExit(2 if errors else 0)
