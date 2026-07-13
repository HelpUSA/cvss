# IEEE LaTeX manuscript package

Generated UTC: 2026-07-13T20:54:33.094742+00:00

## Files

- `cvss40_double_blind.tex`
- `references.bib`
- `cvss40_double_blind.pdf`
- `.gitignore`

## Dataset

- Scenarios: 30
- NVD/CVSS v4.0 records: 12
- Curated synthetic scenarios: 18
- Operational priority shifts: 22/30

## Compiled manuscript

- Status: passed
- Pages: 3
- Page size: 612 x 792 pts (letter)
- PDF size: 76617 bytes
- Undefined citations: none
- Tables: 3
- Bibliography entries: 17

## Manual compilation

Run from `article/ieee`:

    pdflatex -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex
    bibtex cvss40_double_blind
    pdflatex -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex
    pdflatex -interaction=nonstopmode -halt-on-error cvss40_double_blind.tex

The next phase should expand substantive academic content beyond the current
3 pages.
