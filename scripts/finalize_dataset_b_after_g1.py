#!/usr/bin/env python3
"""Create a finalized canonical Dataset B view only after strict calculator gate G1 passes.

This script never overwrites legacy provenance columns.  It adds canonical source score
fields derived from the complete source vector, while preserving provider-reported pure Base
values separately for CVSS-BT rows.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--root',default='.')
ap.add_argument('--g1-json',default='outputs/first-reference-corpus-round4.json')
ap.add_argument('--input',default='data/dataset_b/source_assessments_v2.csv')
ap.add_argument('--output',default='data/dataset_b/source_assessments_final.csv')
args=ap.parse_args(); root=Path(args.root)

g1=json.loads((root/args.g1_json).read_text(encoding='utf-8'))
if not g1.get('summary',{}).get('gate_pass',False):
    raise SystemExit('BLOCKED: strict calculator gate G1 is not PASS; do not finalize canonical scores.')

rows=list(csv.DictReader((root/args.input).open(encoding='utf-8',newline='')))
fields=list(rows[0].keys())
for f in ['canonical_source_score','canonical_source_severity','canonical_source_score_semantics','canonicalized_after_g1']:
    if f not in fields: fields.append(f)

for r in rows:
    score=r.get('recomputed_full_vector_score','').strip()
    sev=r.get('recomputed_full_vector_severity','').strip()
    if not score or not sev:
        raise SystemExit(f"{r.get('scenario_id')}: missing full-vector recomputation")
    r['canonical_source_score']=score
    r['canonical_source_severity']=sev
    r['canonical_source_score_semantics']='COMPLETE_SOURCE_VECTOR_SCORE'
    r['canonicalized_after_g1']='true'

out=root/args.output; out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',encoding='utf-8',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=fields); w.writeheader(); w.writerows(rows)
print(out)
