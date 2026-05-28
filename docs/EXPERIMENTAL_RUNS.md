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
