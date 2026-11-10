#!/usr/bin/env python3
"""Validate provenance, dates, endpoints, amounts, and important research distinctions."""
import json,re
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'public/data/atlas.json').read_text())
deals=D['deals'];companies=D['companies'];ids={c['id'] for c in companies};byid={d['id']:d for d in deals}
assert len(ids)==len(companies)
assert len(byid)==len(deals),'Duplicate deal ID'
required={'amazon','google','meta','microsoft','apple','applied-materials','nvidia','tsmc','tesla','spacex','openai','anthropic','intel','oracle'}
assert required<=ids
assert {c['id'] for c in companies if c['requested']}==required
types={'investment','compute','partnership','acquisition','supply','financing'}
statuses={'announced','signed','completed','proposed','reported','terminated'}
for d in deals:
    assert d['source'] in ids and d['target'] in ids and d['source']!=d['target'],d['id']
    assert d['type'] in types and d['status'] in statuses,d['id']
    assert re.fullmatch(r'\d{4}(-\d{2})?(-\d{2})?',d['announced_at']),d['id']
    assert d['announced_at']<='2026-11-10',d['id']
    date.fromisoformat(d['announced_at']+{4:'-01-01',7:'-01',10:''}[len(d['announced_at'])])
    assert d['verified_at']<='2026-11-10',d['id']
    for field in ['title_he','summary_he','direction_he']:
        assert re.search('[א-ת]',d[field]),(d['id'],field)
        assert '\u2014' not in d[field],d['id']
    value=d['value'];assert isinstance(value,dict)
    assert value['amount'] is None or isinstance(value['amount'],(int,float)) and value['amount']>=0,d['id']
    assert value['amount'] is None or value['currency'] in {'USD','EUR','GBP'},d['id']
    assert d['sources'],d['id']
    for s in d['sources']:
        assert s['url'].startswith('https://'),d['id']
        assert s['title'] and s['publisher'],d['id']
        assert s['kind'] in {'primary','secondary'},d['id']
        assert not s['published_at'] or s['published_at']<='2026-11-10',(d['id'],s)
for c in companies:
    assert (ROOT/'public'/c['logo']).exists(),f'Missing logo {c["id"]}'
    assert any(d['source']==c['id'] or d['target']==c['id'] for d in deals)
    size=c.get('size',{})
    if size.get('usd_billion') is not None:
        assert size['usd_billion']>0,c['id']
        assert size['kind'] in {'market_cap','private_valuation'},c['id']
        assert size['as_of']<='2026-11-10',c['id']
        assert size['source']['url'].startswith('https://'),c['id']
# These distinguish the corrected dataset from common misleading diagrams.
assert byid['microsoft-mistral-investment-2024']['value']=={'amount':15000000,'currency':'EUR','qualifier_he':byid['microsoft-mistral-investment-2024']['value']['qualifier_he']}
assert byid['amazon-openai-investment-2026']['status']=='completed'
assert byid['nv-iren-warrant-2026']['status']!='completed'
assert byid['nv-sb-energy-guarantee-2026']['type']=='financing'
assert byid['nv-openai-loi-2025']['default_visible'] is False
assert byid['meta-manus-acquisition-unwound']['status']=='terminated'
assert byid['hw-broadcom-anthropic-risk-support']['value']['amount'] is None
assert byid['hw-marvell-lumentum-merger']['status']!='completed'
print(f'PASS: {len(deals)} records; {len(companies)} companies/entities; provenance and research distinctions validated.')
