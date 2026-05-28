param()

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
Write-Output 'REBUILD_ALL_START'
python scripts/run_curated_scenarios.py
if(Test-Path scripts/run_ai_validation_queue.ps1){ powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_ai_validation_queue.ps1 }
Write-Output 'TODO: article input and static dashboard generation should be folded into this script as the next checkpoint.'
Write-Output 'REBUILD_ALL_END'
