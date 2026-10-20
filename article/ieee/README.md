# IEEE LaTeX manuscript package

Generated UTC: 2026-10-20T20:00:40.493178+00:00

Files:
- cvss40_double_blind.tex
- references.bib
- .gitignore

Dataset:
- Scenarios: 30
- NVD/CVSS v4.0 records: 12
- Synthetic scenarios: 18
- Priority shifts: 22/30

Approximate extracted word count: 946
Tables: 3
Bibliography entries: 17

Compile from PowerShell:

Set-Location D:\dev\cvss\article\ieee
latexmk -pdf -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex

The final page count must be checked in the compiled two-column PDF.
