from core.cvss31 import base_score, official_cvss_output

def test_cvss31_critical_98():
 r=base_score('CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H')
 assert r['base_score'] == 9.8
 assert r['base_severity'] == 'Critical'

def test_cvss31_high_88():
 r=base_score('CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H')
 assert r['base_score'] == 8.8
 assert r['base_severity'] == 'High'

def test_cvss31_scope_changed_61():
 r=base_score('CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N')
 assert r['base_score'] == 6.1
 assert r['base_severity'] == 'Medium'

def test_official_output_separate():
 o=official_cvss_output('CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H')
 assert o['official_cvss']['base_score'] == 9.8
 assert 'contextual_environmental' not in o
