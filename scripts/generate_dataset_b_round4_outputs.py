#!/usr/bin/env python3
"""Generate synchronized Dataset B development artifacts from schema-v2 CSV.

The generator deliberately preserves provider-reported Base score separately
from the score recomputed from a complete source vector.  It never interprets
Dataset B as confirmatory validation.
"""
from __future__ import annotations
import csv, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'data' / 'dataset_b' / 'source_assessments_v2.csv'
OUT = ROOT / 'generated'
OUT.mkdir(exist_ok=True)

rows = list(csv.DictReader(SRC.open(encoding='utf-8', newline='')))
if len(rows) != 30:
    raise SystemExit(f'Dataset B must contain exactly 30 development scenarios, found {len(rows)}')

required = {
    'scenario_id','cve_id','source_cvss_v4_vector','source_nomenclature',
    'provider_reported_base_score','provider_reported_base_severity',
    'recomputed_full_vector_score','recomputed_full_vector_severity',
    'metric_provider','base_vector_origin','asset_class','legacy_operational_disposition'
}
missing = required - set(rows[0])
if missing:
    raise SystemExit(f'Missing Dataset B v2 fields: {sorted(missing)}')

# Invariants.
for r in rows:
    if r['source_nomenclature'] == 'CVSS-BT':
        for field in ('provider_reported_base_score','provider_reported_base_severity','recomputed_full_vector_score','recomputed_full_vector_severity'):
            if not r.get(field):
                raise SystemExit(f"{r['scenario_id']}: CVSS-BT row missing {field}")

provider_base_sev = Counter(r['provider_reported_base_severity'] for r in rows if r['provider_reported_base_severity'])
full_source_sev = Counter(r['recomputed_full_vector_severity'] or r['provider_reported_base_severity'] for r in rows)
disposition = Counter(r['legacy_operational_disposition'] for r in rows)

payload = {
    'dataset_role': 'DEVELOPMENT_BENCHMARK_ONLY',
    'n': len(rows),
    'real_cve_scenarios': sum(bool(r['cve_id']) for r in rows),
    'synthetic_scenarios': sum(not bool(r['cve_id']) for r in rows),
    'provider_reported_base_severity_counts': dict(sorted(provider_base_sev.items())),
    'full_source_vector_severity_counts': dict(sorted(full_source_sev.items())),
    'operational_disposition_counts': dict(sorted(disposition.items())),
    'scenario_ids': [r['scenario_id'] for r in rows],
}
(OUT/'dataset_b_summary.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')

# A web-safe fixture with the same scenario identifiers and unambiguous score semantics.
fixture=[]
for r in rows:
    fixture.append({
        'scenario_id': r['scenario_id'],
        'cve_id': r['cve_id'] or None,
        'asset_class': r['asset_class'],
        'source_nomenclature': r['source_nomenclature'],
        'provider_reported_base_score': float(r['provider_reported_base_score']) if r['provider_reported_base_score'] else None,
        'provider_reported_base_severity': r['provider_reported_base_severity'] or None,
        'recomputed_full_vector_score': float(r['recomputed_full_vector_score']) if r['recomputed_full_vector_score'] else None,
        'recomputed_full_vector_severity': r['recomputed_full_vector_severity'] or None,
        'metric_provider': r['metric_provider'] or None,
        'origin': r['base_vector_origin'],
        'development_operational_disposition': r['legacy_operational_disposition'] or None,
    })
(OUT/'dataset_b_public_fixture.json').write_text(json.dumps({'dataset_role':'DEVELOPMENT_BENCHMARK_ONLY','scenarios':fixture}, indent=2, ensure_ascii=False), encoding='utf-8')

# Human-readable provenance summary generated from the same rows.
lines=[
    '# Dataset B Provenance Summary — Generated', '',
    '> **Role:** development/regression benchmark only. This document is generated from `data/dataset_b/source_assessments_v2.csv` and is not confirmatory evidence.', '',
    '| Scenario | CVE | Provider | Nom. | Provider Base | Full-vector score | Full severity | Origin |',
    '|---|---|---|---|---:|---:|---|---|',
]
for r in rows:
    lines.append('| {scenario_id} | {cve} | {provider} | {nom} | {base} | {full} | {sev} | {origin} |'.format(
        scenario_id=r['scenario_id'], cve=r['cve_id'] or '—', provider=r['metric_provider'] or '—', nom=r['source_nomenclature'],
        base=r['provider_reported_base_score'] or '—', full=r['recomputed_full_vector_score'] or '—', sev=r['recomputed_full_vector_severity'] or '—', origin=r['base_vector_origin']))
(OUT/'DATASET_B_PROVENANCE_SUMMARY_GENERATED.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps(payload, indent=2, ensure_ascii=False))
