---
status: passed
last_updated: 2026-07-13
owner: "Wagner / CVSS project"
tags: [cvss-v4, ieee, latex, compilation, double-blind]
---

# CVSS v4.0 IEEE LaTeX compilation report

Generated UTC: `2026-07-13T20:54:33.094742+00:00`

## Result

- Compilation status: passed
- Output: `article/ieee/cvss40_double_blind.pdf`
- Page count: 3
- Page size: 612 x 792 pts (letter)
- File size: 76617 bytes
- Bibliography processing: passed
- Undefined citations after final pass: none
- LaTeX structural validation: passed
- Table count: 3
- NVD bibliography entries: 12

## Build route

`latexmk` could not execute because Perl is not installed.

Compilation passed with:

1. `pdflatex`
2. `bibtex`
3. `pdflatex`
4. `pdflatex`

## Non-blocking warnings

The compiler reported `Underfull hbox` warnings caused mainly by long
bibliography URLs. These warnings do not invalidate the PDF.

## Assessment

The manuscript compiles successfully with 3 pages. The next phase should
expand related work, methodology, experimental protocol, and analysis using
substantive academic content.
