#
# CVSS Environmental Assessment with AI Bridge

This repository contains a continuation-study prototype for CVSS Environmental assessment.

## Canonical structure

- `article/` - active LaTeX manuscript.
- `cases/` - structured case-study evidence.
- `app/` - Python prototype for deterministic scoring and reporting.
- `outputs/` - generated outputs. Final runs must use clean run directories.
- `ai_bridge/` - watcher/agent prompts and execution notes.
- `docs/` - project status and planning.
- `research/source_papers/` - source papers and reference PDFs.
- `_archive/` - legacy drafts, imported ZIPs, backups, and discarded material.

## Scientific thesis

The prior PCI-DSS inspired study showed that manual CVSS Environmental assessment becomes harder as segmentation and dependencies increase. This project evaluates whether a watcher-mediated AI Bridge workflow can make the same task more reproducible, auditable, and evidence-based.

The claim is deliberately conservative: the workflow does not replace expert judgment. It operationalizes evidence collection, scoring, review, and traceability so that expert decisions can be inspected and repeated.
