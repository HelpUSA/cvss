# Experimental Runs

## Latest clean PCI segmented lab run

- Run: `outputs/runs/pci_segmented_lab_20260517_143146`
- Assessments: 12
- Findings: 6
- Downgraded: 2
- Unchanged: 4
- Upgraded: 0
- Mean delta: -0.267
- Max absolute delta: 0.8

Generated artifacts:
- `outputs/runs/pci_segmented_lab_20260517_143146/run_manifest.json`
- `outputs/runs/pci_segmented_lab_20260517_143146/summary.csv`
- `outputs/runs/pci_segmented_lab_20260517_143146/before_after_comparison.csv`
- `outputs/runs/pci_segmented_lab_20260517_143146/article_table_env_effects.md`
- `outputs/runs/pci_segmented_lab_20260517_143146/assessments.json`
- `outputs/runs/pci_segmented_lab_20260517_143146/audit_trace.jsonl`
- `outputs/runs/pci_segmented_lab_20260517_143146/report.md`

The run is a deterministic artifact validation run. It should not be presented as evidence that the watcher workflow outperforms human experts until the multi-condition evaluation is executed.

## 2026-05-27 manuscript and experiment status update

Validated continuation work:
- Article evaluation section now uses artifact-validation framing and includes a deterministic baseline results table from pci_segmented_lab outputs.
- Threats-to-validity and conclusion now explicitly separate artifact validation from broader comparative claims.
- Current committed validation chain includes web build, article build where local LaTeX is available, production marker checks, and pushed commits.

Completed commits:
- a52e058 Add CVSS artifact validation results table
- afbf8e8 Harden CVSS manuscript validity framing

Remaining research work is no longer dashboard implementation; it is the next study phase: add more scenarios, collect or encode independent expert labels, and compare manual assessment, LLM-only support, and watcher-mediated evidence collection.

## 2026-05-27 manuscript and experiment status update

Validated continuation work:
- Article evaluation section now uses artifact-validation framing and includes a deterministic baseline results table from pci_segmented_lab outputs.
- Threats-to-validity and conclusion now explicitly separate artifact validation from broader comparative claims.
- Current committed validation chain includes web build, article build where local LaTeX is available, production marker checks, and pushed commits.

Completed commits:
- a52e058 Add CVSS artifact validation results table
- afbf8e8 Harden CVSS manuscript validity framing

Remaining research work is no longer dashboard implementation; it is the next study phase: add more scenarios, collect or encode independent expert labels, and compare manual assessment, LLM-only support, and watcher-mediated evidence collection.

## 2026-05-27 additional case compatibility check

The canonical runnable case remains pci_segmented_lab because it includes the complete current schema required by app/run_demo.py, including vulnerabilities.csv and the environmental evidence YAML files. The older pci_demo and complex folders contain legacy vulnerability_findings.csv files and are not directly runnable with the current deterministic runner without schema migration.

Next engineering task for the broader-study phase: add a small case migration or compatibility loader that accepts legacy vulnerability_findings.csv inputs, or convert pci_demo and complex to the current case schema before using them as additional experimental scenarios.

## 2026-05-27 additional case compatibility check

The canonical runnable case remains pci_segmented_lab because it includes the complete current schema required by app/run_demo.py, including vulnerabilities.csv and the environmental evidence YAML files. The older pci_demo and complex folders contain legacy vulnerability_findings.csv files and are not directly runnable with the current deterministic runner without schema migration.

Next engineering task for the broader-study phase: add a small case migration or compatibility loader that accepts legacy vulnerability_findings.csv inputs, or convert pci_demo and complex to the current case schema before using them as additional experimental scenarios.

## 2026-05-28 legacy case loader update

The deterministic runner now accepts both current vulnerabilities.csv case folders and legacy vulnerability_findings.csv case folders. Validation was run against pci_segmented_lab, pci_demo, and complex using temporary outputs under temp. The legacy folders are now usable as compatibility smoke scenarios, while broader-study claims still require curated evidence, independent labels, and explicit experimental design.

## 2026-05-28 legacy case loader update

The deterministic runner now accepts both current vulnerabilities.csv case folders and legacy vulnerability_findings.csv case folders. Validation was run against pci_segmented_lab, pci_demo, and complex using temporary outputs under temp. The legacy folders are now usable as compatibility smoke scenarios, while broader-study claims still require curated evidence, independent labels, and explicit experimental design.

## 2026-05-28 broader-study protocol update

Added docs/BROADER_STUDY_PROTOCOL.md to define the next evaluation phase: manual expert assessment, LLM-only support, and watcher-mediated workflow. This protocol preserves the current manuscript boundary: deterministic artifact validation is complete, while broader comparative claims require curated scenarios and independent expert labels.

## 2026-05-28 broader-study protocol update

Added docs/BROADER_STUDY_PROTOCOL.md to define the next evaluation phase: manual expert assessment, LLM-only support, and watcher-mediated workflow. This protocol preserves the current manuscript boundary: deterministic artifact validation is complete, while broader comparative claims require curated scenarios and independent expert labels.
