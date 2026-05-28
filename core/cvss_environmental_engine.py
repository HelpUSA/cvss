def sev(s):
 s=float(s)
 if s>=9: return 'Critical'
 if s>=7: return 'High'
 if s>=4: return 'Medium'
 if s>0: return 'Low'
 return 'None'

def b(v):
 return str(v).strip().lower() in ['1','true','yes','y','sim','in-scope','restricted']

def clamp(x):
 return round(max(0.0,min(10.0,float(x))),1)

def calculate(row):
 base=clamp(str(row.get('base_score',0)).replace(',','.'))
 score=base
 reasons=[]
 if b(row.get('internet_exposed',False)):
 score += 0.4; reasons.append('internet exposure increased environmental risk')
 else:
 score -= 0.3; reasons.append('absence of internet exposure reduced environmental risk')
 if b(row.get('network_segmented',False)):
 score -= 0.7; reasons.append('network segmentation reduced reachable attack surface')
 if b(row.get('firewall_restricted',False)):
 score -= 0.5; reasons.append('firewall restrictions reduced exposure')
 if b(row.get('compensating_controls',False)):
 score -= 0.4; reasons.append('compensating controls reduced expected impact')
 if b(row.get('pci_in_scope',False)):
 score += 0.3; reasons.append('PCI scope increased business and compliance relevance')
 c=str(row.get('business_criticality','medium')).lower()
 if c=='high':
 score += 0.4; reasons.append('high business criticality increased environmental relevance')
 elif c=='low':
 score -= 0.2; reasons.append('low business criticality reduced environmental relevance')
 env=clamp(score)
 delta=round(env-base,1)
 decision='downgraded' if delta<0 else ('upgraded' if delta>0 else 'unchanged')
 return {'base_score':base,'environmental_score':env,'base_severity':sev(base),'environmental_severity':sev(env),'delta':delta,'decision':decision,'rationale':'; '.join(reasons)}
