import csv
from pathlib import Path
from core.cvss_environmental_engine import calculate

ROOT=Path(file).resolve().parents[1]
SCENARIOS=ROOT/'scenarios'
RUNS=ROOT/'outputs'/'runs'
SUMMARY=ROOT/'outputs'/'curated_run_summary.csv'

def read_csv(path):
 if not path.exists(): return []
 with path.open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def write_csv(path, rows, fields):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

summary=[]
for scenario in sorted([p for p in SCENARIOS.iterdir() if p.is_dir() and p.name!='templates']):
 vulns=read_csv(scenario/'vulnerabilities.csv')
 if not vulns: continue
 run_id=scenario.name
 outdir=RUNS/run_id
 rows=[]
 for v in vulns:
 r=dict(v)
 calc=calculate(v)
 r.update(calc)
 r['case_id']=scenario.name
 r['run_id']=run_id
 rows.append(r)
 fields=['case_id','run_id','finding_id','asset_id','cve','vulnerability_type','base_score','base_severity','base_vector','environmental_score','environmental_severity','delta','decision','rationale','internet_exposed','network_segmented','pci_in_scope','firewall_restricted','compensating_controls','business_criticality','notes']
 write_csv(outdir/'before_after_comparison.csv', rows, fields)
 downgraded=sum(1 for r in rows if r['decision']=='downgraded')
 upgraded=sum(1 for r in rows if r['decision']=='upgraded')
 unchanged=sum(1 for r in rows if r['decision']=='unchanged')
 mean_delta=round(sum(float(r['delta']) for r in rows)/len(rows),3)
 summary.append({'case_id':scenario.name,'run_id':run_id,'findings':len(rows),'assessments':len(rows),'downgraded':downgraded,'unchanged':unchanged,'upgraded':upgraded,'mean_delta':mean_delta,'source':'before_after_comparison.csv'})
write_csv(SUMMARY, summary, ['case_id','run_id','findings','assessments','downgraded','unchanged','upgraded','mean_delta','source'])
print('scenarios=',len(summary))
print('wrote=',SUMMARY)
