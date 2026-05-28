# CVSS pipeline artifact map

This document maps the research sequence to concrete artifacts.

## Inputs

- case_description.md
- topology.yaml
- firewall_rules.yaml
- business_impact.yaml
- pci_scope.yaml
- vulnerabilities.csv
- expected_expert_labels.yaml

## Core processing

The future stable scoring engine should live in a reusable module such as core/cvss_environmental_engine.py or an equivalent JavaScript implementation for static site use.

## Outputs

- outputs/runs/<run_id>/before_after_comparison.csv
- outputs/curated_run_summary.csv
- validation/queues/curated_validation_queue.csv
- validation/ai_review/outputs/ai_validation_rows.csv
- validation/ai_review/outputs/ai_validation_summary.csv
- validation/ai_review/reports/ai_validation_report.md
- docs/generated/automated_validation_article_inputs.md
- article/generated/automated_validation_summary_table.txt
- index.html
- article/main.pdf

## Full rebuild target

A future script, scripts/rebuild_all.ps1, should regenerate curated summaries, validation queue, IA validation rows, article inputs, static dashboard, and article PDF from the committed scenario artifacts.

## Current status

The project currently has a static public dashboard and committed article/reproducibility artifacts. The next scientific work is to strengthen the scoring engine and expand curated scenarios before building the full interactive website.
