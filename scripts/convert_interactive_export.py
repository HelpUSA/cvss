import argparse, csv, json
from pathlib import Path
FIELDS=['finding_id','asset_id','cve','vulnerability_type','base_score','base_severity','base_vector','internet_exposed','network_segmented','pci_in_scope','firewall_restricted','compensating_controls','business_criticality','notes']
p=argparse.ArgumentParser()
p.add_argument('input_json')
p.add_argument('--out-dir', default='scenarios/from_interactive')
a=p.parse_args()
data=json.loads(Path(a.input_json).read_text(encoding='utf-8'))
scenario=data.get('case_description',{}).get('scenario') or data.get('result',{}).get('scenario') or 'interactive_scenario'
out=Path(a.out_dir)/scenario
out.mkdir(parents=True, exist_ok=True)
(out/'case_description.md').write_text('# '+scenario+'

Generated from interactive static MVP export.
', encoding='utf-8')
rows=data.get('vulnerabilities') or []
with (out/'vulnerabilities.csv').open('w', newline='', encoding='utf-8') as f:
 w=csv.DictWriter(f, fieldnames=FIELDS)
 w.writeheader()
 for row in rows:
 w.writerow({k: row.get(k, '') for k in FIELDS})
print(out)
