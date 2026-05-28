import csv
from pathlib import Path
from core.cvss_environmental_engine import calculate

def test_segmented_pci_downgrades():
 r = calculate({'base_score':'9.8','internet_exposed':'no','network_segmented':'yes','pci_in_scope':'yes','firewall_restricted':'yes','compensating_controls':'yes','business_criticality':'high'})
 assert r['decision'] == 'downgraded'
 assert r['environmental_score'] < r['base_score']
 assert r['trace_count'] >= 1

def test_public_high_risk_upgrades():
 r = calculate({'base_score':'6.5','internet_exposed':'yes','network_segmented':'no','pci_in_scope':'yes','firewall_restricted':'no','compensating_controls':'no','business_criticality':'high'})
 assert r['environmental_score'] >= r['base_score']

def test_curated_summary_exists_after_pipeline():
 p = Path('outputs/curated_run_summary.csv')
 assert p.exists()
 rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))
 assert len(rows) >= 1
