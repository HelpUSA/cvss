# IEEE LaTeX Manuscript Package (Major Revision R1)

Title: Operationalizing CVSS v4.0 Environmental Metrics with Evidence Normalization, Governance, and Traceability

Files:
- cvss40_double_blind.tex
- references.bib
- README.md

Dataset:
- Scenarios: 30 (12 real NVD CVEs carrying CVSS v4.0 data + 18 curated synthetic scenarios)
- Priority shifts: 22/30 (Category Delta mean = 0.2, range [-3.0, +2.0])

Tables:
- Table I: Research Questions, Measures, and Interpretation Boundaries
- Table II: Dataset and Workflow Summary
- Table III: Operational Priority Transitions
- Table IV: CVSS-B Severity Distribution
- Table V: Controlled Workflow Evaluation on 12 Real NVD CVEs

Figures:
- Figure 1: TikZ native vector architecture pipeline

Bibliography entries: 26 (including 12 NVD primary CVE records and FIRST standards)

Compilation Instructions (Overleaf / pdflatex):
1. pdflatex -interaction=nonstopmode cvss40_double_blind.tex
2. bibtex cvss40_double_blind
3. pdflatex -interaction=nonstopmode cvss40_double_blind.tex
4. pdflatex -interaction=nonstopmode cvss40_double_blind.tex
