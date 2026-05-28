# Broader CVSS Environmental Study Protocol

## Purpose

This protocol defines the next evaluation phase after the deterministic artifact-validation baseline. It separates engineering reproducibility from comparative claims about assessment quality.

## Study arms

1. Manual expert assessment: independent reviewers assess each finding using the same local evidence bundle.
2. LLM-only support: reviewers or agents use the same evidence bundle without watcher-mediated collection.
3. Watcher-mediated workflow: the AI Bridge watcher collects or verifies local evidence, produces an auditable trace, and generates candidate CVSS Environmental labels.

## Required case package

Each scenario should include assets.csv, vulnerabilities.csv or legacy vulnerability_findings.csv, topology.yaml, firewall_rules.yaml, business_impact.yaml, pci_scope.yaml, expected_expert_labels.yaml, and case_description.md.

The deterministic runner now accepts both current vulnerabilities.csv and legacy vulnerability_findings.csv. Legacy cases may be used as smoke scenarios, but research claims require curated evidence and independent labels.

## Minimum validation checks

For each scenario, run app/run_demo.py successfully, preserve curated outputs under outputs/runs, verify summary.csv, assessments.json, audit_trace.jsonl, and report.md, compare generated labels with expected_expert_labels.yaml, record downgraded, unchanged, upgraded, mean delta, and maximum absolute delta, and confirm dashboard or manuscript tables are generated from run artifacts rather than manual transcription.

## Claim boundaries

The current manuscript may claim reproducibility, auditability, and deterministic artifact validation for the PCI segmented lab baseline. It should not claim human-level or superior performance until this broader protocol has independent expert labels, multiple scenarios, and arm-level analysis.

## Next implementation tasks

- Convert pci_demo and complex into curated scenarios by adding topology, firewall, business impact, PCI scope, and expected expert labels.
- Add a script that summarizes all curated runs into one CSV for manuscript tables.
- Add a reviewer-form template for independent expert assessment.
- Update the article only after the new scenarios are curated and validated.

## 2026-05-28 reviewer assessment form update

Added docs/REVIEWER_ASSESSMENT_FORM.md for the broader-study phase. The form supports independent manual, LLM-only, and watcher-mediated assessment arms and records finding-level CVSS Environmental labels, evidence, rationale, confidence, and adjudication notes.

## 2026-05-28 curated legacy scenarios update

Converted pci_demo and complex from legacy smoke folders into current-schema curated scenario packages by adding vulnerabilities.csv, case_description.md, topology.yaml, firewall_rules.yaml, business_impact.yaml, pci_scope.yaml, and expected_expert_labels.yaml. Curated runs were generated under outputs/runs and outputs/curated_run_summary.csv now summarizes the canonical pci_segmented_lab run plus the newly curated scenarios. These scenarios expand engineering validation coverage; independent expert assessment is still required before broader comparative claims.

## 2026-05-28 curated legacy scenarios update

Converted pci_demo and complex from legacy smoke folders into current-schema curated scenario packages by adding vulnerabilities.csv, case_description.md, topology.yaml, firewall_rules.yaml, business_impact.yaml, pci_scope.yaml, and expected_expert_labels.yaml. Curated runs were generated under outputs/runs and outputs/curated_run_summary.csv now summarizes the canonical pci_segmented_lab run plus the newly curated scenarios. These scenarios expand engineering validation coverage; independent expert assessment is still required before broader comparative claims.

## 2026-05-28 article curated-run summary update

The manuscript evaluation section now includes a curated-run engineering validation summary table covering pci_segmented_lab, pci_demo_curated, and complex_curated. The text keeps the claim boundary clear: these scenarios expand deterministic engineering validation, while independent expert review and arm-level adjudication remain required before broader comparative claims.

## 2026-05-28 article curated-run summary update

The manuscript evaluation section now includes a curated-run engineering validation summary table covering pci_segmented_lab, pci_demo_curated, and complex_curated. The text keeps the claim boundary clear: these scenarios expand deterministic engineering validation, while independent expert review and arm-level adjudication remain required before broader comparative claims.
