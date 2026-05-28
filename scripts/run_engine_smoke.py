import csv
from pathlib import Path
from core.cvss_environmental_engine import calculate
cases=[{'case_id':'pci_segmented_lab_20260517_143146','base_score':9.8,'internet_exposed':'no','network_segmented':'yes','pci_in_scope':'yes','firewall_restricted':'yes','compensating_controls':'yes','business_criticality':'high'},{'case_id':'internet_exposed_webapp_demo','base_score':6.5,'internet_exposed':'yes','network_segmented':'no','pci_in_scope':'yes','firewall_restricted':'no','compensating_controls':'no','business_criticality':'high'}]
out=[]
for c in cases:
 r=dict(c); r.update(calculate(c)); out.append(r)
p=Path('outputs/engine_smoke/environmental_engine_smoke.csv'); p.parent.mkdir(parents=True,exist_ok=True)
with p.open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print('wrote=',p)
