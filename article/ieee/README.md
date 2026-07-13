# IEEE LaTeX manuscript package

Generated UTC: 2026-07-13T22:17:49.605488+00:00

## Current manuscript

- Source: `cvss40_double_blind.tex`
- Bibliography: `references.bib`
- PDF: `cvss40_double_blind.pdf`
- Related-work notes: `RELATED_WORK_NOTES.md`

## Compilation

- Status: passed
- Pages: 6
- Page size: 612 x 792 pts (letter)
- PDF size: 151250 bytes
- Undefined citations: none
- Tables: 0
- Figures: 0

## Dataset

- Scenarios: 30
- NVD/CVSS v4.0 records: 12
- Curated synthetic scenarios: 18
- Evidence coverage: 100.00%
- Trace completeness: 100.00%
- Operational priority shifts: 22/30

## Manual compilation

Run from `article/ieee`:

    pdflatex -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex
    bibtex cvss40_double_blind
    pdflatex -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex
    pdflatex -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex

## Interpretation boundary

The watcher produces evidence-backed candidate recommendations. It does not
produce autonomous official CVSS scores.
