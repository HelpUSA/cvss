param(
 [string]$Runs = 'outputs/runs',
 [string]$Out = 'outputs/curated_run_summary.csv'
)
$rows = @()
if (Test-Path -LiteralPath $Runs) {
 Get-ChildItem -LiteralPath $Runs -Directory | Sort-Object Name | ForEach-Object {
 $run = $PSItem
 $compPath = Join-Path $run.FullName 'before_after_comparison.csv'
 $summaryPath = Join-Path $run.FullName 'summary.csv'
 if (Test-Path -LiteralPath $compPath) {
 $comp = Import-Csv -LiteralPath $compPath
 $deltas = @($comp | ForEach-Object { [double]$PSItem.delta })
 $effects = @($comp | ForEach-Object { $PSItem.effect })
 $meanDelta = if ($deltas.Count) { [math]::Round(($deltas | Measure-Object -Average).Average, 3) } else { '' }
 $maxAbs = if ($deltas.Count) { [math]::Round((($deltas | ForEach-Object { [math]::Abs($PSItem) }) | Measure-Object -Maximum).Maximum, 1) } else { '' }
 $rows += [pscustomobject]@{ run_id=$run.Name; case_id=$run.Name; findings=$comp.Count; assessments=($comp.Count*2); downgraded=($effects | Where-Object { $PSItem -eq 'downgraded' }).Count; unchanged=($effects | Where-Object { $PSItem -eq 'unchanged' }).Count; upgraded=($effects | Where-Object { $PSItem -eq 'upgraded' }).Count; mean_delta=$meanDelta; max_abs_delta=$maxAbs; source='before_after_comparison.csv' }
 } elseif (Test-Path -LiteralPath $summaryPath) {
 $sum = Import-Csv -LiteralPath $summaryPath
 $findings = @($sum | Select-Object -ExpandProperty finding_id -Unique)
 $rows += [pscustomobject]@{ run_id=$run.Name; case_id=$run.Name; findings=$findings.Count; assessments=$sum.Count; downgraded=''; unchanged=''; upgraded=''; mean_delta=''; max_abs_delta=''; source='summary.csv' }
 }
 }
}
$outDir = Split-Path -Parent $Out
if ($outDir) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }
$rows | Export-Csv -LiteralPath $Out -NoTypeInformation -Encoding UTF8
Write-Output ('WROTE ' + $Out + ' rows=' + $rows.Count)
