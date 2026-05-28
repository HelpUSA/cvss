import math

AV=dict(N=0.85,A=0.62,L=0.55,P=0.2)
AC=dict(L=0.77,H=0.44)
UI=dict(N=0.85,R=0.62)
CIA=dict(H=0.56,L=0.22,N=0.0)
PRU=dict(N=0.85,L=0.62,H=0.27)
PRC=dict(N=0.85,L=0.68,H=0.5)

def roundup(x):
 return math.ceil(float(x)10.0-1e-7)/10.0

def severity(s):
 s=float(s)
 if s==0: return 'None'
 if s<4: return 'Low'
 if s<7: return 'Medium'
 if s<9: return 'High'
 return 'Critical'

def parse_vector(vector):
 parts=str(vector).strip().split('/')
 if not parts or parts[0] not in ('CVSS:3.1','CVSS:3.0'):
 raise ValueError('only CVSS 3.x vectors supported')
 m={'version':parts.split(':')[1]}
 for part in parts[1:]:
 k,v=part.split(':',1)
 m[k]=v
 for k in ['AV','AC','PR','UI','S','C','I','A']:
 if k not in m: raise ValueError('missing metric '+k)
 return m

def base_score(vector):
 m=parse_vector(vector)
 scope=m['S']
 pr=(PRC if scope=='C' else PRU)[m['PR']]
 exploit=8.22AV[m['AV']]AC[m['AC']]prUI[m['UI']]
 isc=1-((1-CIA[m['C']])(1-CIA[m['I']])(1-CIA[m['A']]))
 impact=6.42isc if scope=='U' else 7.52*(isc-0.029)-3.25*((isc-0.02)*15)
 if impact<=0: score=0.0
 elif scope=='U': score=roundup(min(impact+exploit,10))
 else: score=roundup(min(1.08(impact+exploit),10))
 return {'version':m,'vector':vector,'base_score':score,'base_severity':severity(score),'scope':scope,'impact_subscore':round(impact,3),'exploitability_subscore':round(exploit,3),'metrics':m}

def official_cvss_output(vector):
 r=base_score(vector)
 return {'official_cvss':{'version':r,'vector':r,'base_score':r,'base_severity':r,'temporal_score':None,'environmental_score':None,'scope':r}}
