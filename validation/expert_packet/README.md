# CVSS Expert Validation Packet

Generated: 
2026-05-28 09:46:32

Purpose: provide an independent/manual reviewer with a compact evidence package for validating curated CVSS environmental scoring scenarios without relying on broader comparative claims.

## Current canonical curated run

- Run id: pci_segmented_lab_20260517_143146
- Source summary: outputs/curated_run_summary.csv
- Findings: 6
- Assessments: 12
- Downgraded: 2
- Unchanged: 4
- Upgraded: 0
- Mean delta: -0,267
- Max absolute delta: 0,8

## Reviewer instructions

1. Review each finding and assessment row against the source evidence and CVSS environmental metric rules.
2. Record whether each automated adjustment is correct, incorrect, or unclear.
3. Provide a brief rationale and cite the source artifact used for the judgment.
4. Do not evaluate broad model superiority claims in this packet; this is only a scenario-level validation pass.

## Outputs expected

- Completed validation CSV using validation/templates/expert_validation_form.csv
- Free-text notes in validation/expert_packet/expert_notes.md
- Consensus summary after at least one independent review.
