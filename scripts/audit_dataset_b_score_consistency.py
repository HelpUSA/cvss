#!/usr/bin/env python3
"""Expose, rather than overwrite, Dataset B score/vector inconsistencies."""
import csv,json,sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else 'data/dataset_b/source_assessments_v2.csv')
rows=list(csv.DictReader(p.open(encoding='utf-8')))
mm=[]
for r in rows:
    legacy=r.get('source_score','').strip(); recomputed=r.get('recomputed_full_vector_score','').strip()
    if legacy and recomputed and abs(float(legacy)-float(recomputed)) >= 0.05:
        mm.append({'scenario_id':r['scenario_id'],'origin':r['base_vector_origin'],'nomenclature':r['source_nomenclature'],'legacy_source_score':legacy,'current_recomputed_full_vector_score':recomputed,'delta':round(float(recomputed)-float(legacy),3)})
print(json.dumps({'rows':len(rows),'score_vector_mismatches':len(mm),'mismatches':mm},indent=2))
# This audit intentionally exits nonzero while inconsistencies exist; finalization is blocked until G1.
raise SystemExit(2 if mm else 0)
