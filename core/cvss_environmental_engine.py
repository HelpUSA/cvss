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
 trace=[]
 def add(field,direction,amount,reason):
 nonlocal score
 score += amount
 trace.append({'field':field,'direction':direction,'amount':round(amount,2),'reason':reason})
 if b(row.get('internet_exposed',False)):
 add('internet_exposed','increase',0.4,'internet exposure increased environmental risk')
 else:
 add('internet_exposed','decrease',-0.3,'absence of internet exposure reduced environmental risk')
 if b(row.get('network_segmented',False)):
 add('network_segmented','decrease',-0.7,'network segmentation reduced reachable attack surface')
 if b(row.get('firewall_restricted',False)):
 add('firewall_restricted','decrease',-0.5,'firewall restrictions reduced exposure')
 if b(row.get('compensating_controls',False)):
 add('compensating_controls','decrease',-0.4,'compensating controls reduced expected impact')
 if b(row.get('pci_in_scope',False)):
 add('pci_in_scope','increase',0.3,'PCI scope increased business and compliance relevance')
 c=str(row.get('business_criticality','medium')).lower()
 if c=='high':
 add('business_criticality','increase',0.4,'high business criticality increased environmental relevance')
 elif c=='low':
 add('business_criticality','decrease',-0.2,'low business criticality reduced environmental relevance')
 env=clamp(score)
 delta=round(env-base,1)
 decision='downgraded' if delta<0 else ('upgraded' if delta>0 else 'unchanged')
 rationale='; '.join([t['reason'] for t in trace])
 return {'base_score':base,'environmental_score':env,'base_severity':sev(base),'environmental_severity':sev(env),'delta':delta,'decision':decision,'rationale':rationale,'adjustment_trace':trace,'trace_count':len(trace),'trace_total_adjustment':round(sum(t['amount'] for t in trace),2)}
