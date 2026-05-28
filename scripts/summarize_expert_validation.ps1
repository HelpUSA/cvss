param(
 [string]$InputCsv = 'validation/templates/expert_validation_form.csv',
 [string]$OutputCsv = 'validation/outputs/expert_validation_summary.csv'
)

$ErrorActionPreference = 'Stop'
if(-not (Test-Path -LiteralPath $InputCsv)){ throw 'Input CSV not found' }
$rows = @(Import-Csv -LiteralPath $InputCsv)
$allowed = @('correct','incorrect','unclear')
$usable = @($rows | Where-Object { $_.manual_judgment -and ($allowed -contains $_.manual_judgment) })
$groups = $usable | Group-Object case_id
$summary = foreach($g in $groups){
 $items = @($g.Group)
 $correct = @($items | Where-Object { $_.manual_judgment -eq 'correct' }).Count
 $incorrect = @($items | Where-Object { $_.manual_judgment -eq 'incorrect' }).Count
 $unclear = @($items | Where-Object { $_.manual_judgment -eq 'unclear' }).Count
 $rate = $null
 if($items.Count -gt 0){ $rate = [math]::Round(($correct / $items.Count), 4) }
 [pscustomobject]@{
 case_id = $g.Name
 assessments = $items.Count
 correct = $correct
 incorrect = $incorrect
 unclear = $unclear
 agreement_rate = $rate
 reviewers = (($items | Select-Object -ExpandProperty reviewer -Unique) -join ';')
 }
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputCsv) | Out-Null
$summary | Export-Csv -LiteralPath $OutputCsv -NoTypeInformation -Encoding UTF8
Write-Output ('rows=' + $rows.Count)
Write-Output ('usable_rows=' + $usable.Count)
Write-Output ('summary_rows=' + @($summary).Count)
Write-Output ('wrote=' + $OutputCsv)


