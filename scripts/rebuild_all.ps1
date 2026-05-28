param()

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)

Write-Output 'REBUILD_ALL_START'
python scripts/run_curated_scenarios.py

New-Item -ItemType Directory -Force -Path 'validation/queues','validation/ai_review/outputs','validation/ai_review/reports','docs/generated','article/generated' | Out-Null
$rows = @(Import-Csv 'outputs/curated_run_summary.csv')
$queue = @()
foreach($r in $rows){
 $queue += [pscustomobject]@{ case_id=$r.case_id; run_id=$r.run_id; validation_status='pending_automated_watcher_ia_review'; findings=$r.findings; assessments=$r.assessments; downgraded=$r.downgraded; unchanged=$r.unchanged; upgraded=$r.upgraded; mean_delta=$r.mean_delta; source=$r.source; reviewer='watcher_ai'; review_file=('validation/ai_review/outputs/'+$r.case_id+'.csv') }
}
$queue | Export-Csv 'validation/queues/curated_validation_queue.csv' -NoTypeInformation -Encoding UTF8

if(Test-Path 'scripts/run_ai_validation_queue.ps1'){ powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_ai_validation_queue.ps1 }

$sum = @(Import-Csv 'outputs/curated_run_summary.csv')
$ai = @()
if(Test-Path 'validation/ai_review/outputs/ai_validation_summary.csv'){ $ai = @(Import-Csv 'validation/ai_review/outputs/ai_validation_summary.csv') }
$total=0; $accepted=0; $flagged=0; $unclear=0
foreach($r in $ai){ $total += [int]$r.decisions; $accepted += [int]$r.correct; $flagged += [int]$r.incorrect; $unclear += [int]$r.unclear }
$totalScen=$sum.Count
$totalFind=($sum | Measure-Object findings -Sum).Sum
$totalAssess=($sum | Measure-Object assessments -Sum).Sum
$md=@('# Automated validation article table inputs','',('Curated scenarios: '+$totalScen),('Findings: '+$totalFind),('Assessments: '+$totalAssess),('Automated validation decisions: '+$total),('Accepted decisions: '+$accepted),('Flagged decisions: '+$flagged),('Unclear decisions: '+$unclear),'','Interpretation: automated watcher IA validation only; no completed independent human expert adjudication is claimed.')
$md | Set-Content 'docs/generated/automated_validation_article_inputs.md' -Encoding UTF8
$md | Set-Content 'article/generated/automated_validation_summary_table.txt' -Encoding UTF8

$curRows=''
foreach($r in $sum){ $curRows += '<tr><td>'+$r.case_id+'</td><td>'+$r.findings+'</td><td>'+$r.assessments+'</td><td>'+$r.downgraded+'</td><td>'+$r.unchanged+'</td><td>'+$r.upgraded+'</td><td>'+$r.mean_delta+'</td></tr>' }
$html=@('<!doctype html>','<html><head><meta charset=utf-8><meta name=viewport content=width=device-width,initial-scale=1><title>CVSS Environmental Dashboard</title><style>body{font-family:Arial,sans-serif;margin:0;background:#0f172a;color:#e5e7eb}main{max-width:1200px;margin:0 auto;padding:32px 18px 64px}.panel{background:#111827;border:1px solid #334155;border-radius:18px;padding:22px;margin:18px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px}.card{background:#0b1220;border:1px solid #1f2937;border-radius:14px;padding:16px}.metric{font-size:30px;font-weight:700}.note{color:#cbd5e1;line-height:1.55}table{width:100%;border-collapse:collapse;margin-top:12px}th,td{border-bottom:1px solid #334155;padding:10px;text-align:left}th{color:#93c5fd}</style></head><body><main>','<h1>CVSS Environmental Dashboard</h1>','<p class=note>Static research dashboard generated from committed CVSS artifacts across curated scenarios.</p>','<section class=panel><h2>Automated watcher IA validation</h2><div class=grid><div class=card><div>Scenarios</div><div class=metric>'+$totalScen+'</div></div><div class=card><div>Findings</div><div class=metric>'+$totalFind+'</div></div><div class=card><div>Decisions</div><div class=metric>'+$total+'</div></div><div class=card><div>Accepted</div><div class=metric>'+$accepted+'</div></div><div class=card><div>Flagged</div><div class=metric>'+$flagged+'</div></div></div><p class=note>Automated only. Not completed independent human expert validation.</p></section>','<section class=panel><h2>Curated validation runs</h2><table><thead><tr><th>Case</th><th>Findings</th><th>Assessments</th><th>Downgraded</th><th>Unchanged</th><th>Upgraded</th><th>Mean delta</th></tr></thead><tbody>'+$curRows+'</tbody></table></section>','<section class=panel><h2>Reference markers</h2><p>pci_segmented_lab_20260517_143146; internet_exposed_webapp; internal_erp_segmented; payment_database_zone; cloud_storage_misconfiguration</p></section>','</main></body></html>')
$html | Set-Content 'index.html' -Encoding UTF8

Write-Output 'REBUILD_ALL_END'
