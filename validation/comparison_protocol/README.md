# CVSS LLM-only vs watcher-mediated comparison protocol

Generated: 
2026-05-28 09:46:32

## Goal

Compare two workflows on the same CVSS environmental scoring cases:
- LLM-only: one-pass or constrained prompt-based assessment without watcher/tool orchestration.
- Watcher-mediated: deterministic artifact extraction, scripted summarization, review forms, and deployment/evidence checks mediated through watcher commands.

## Primary outcomes

- Agreement with independent/manual expert judgment.
- Number of unresolved/unclear judgments.
- Mean environmental-score delta versus expert accepted score.
- Traceability: proportion of decisions with cited source artifact.
- Reproducibility: ability to regenerate summary CSVs and manuscript tables from committed artifacts.

## Minimum study design

1. Freeze a case set and evidence bundle.
2. Run LLM-only assessment with locked prompt and no iterative watcher corrections.
3. Run watcher-mediated assessment using committed scripts and logs.
4. Blind/manual expert adjudicates disagreements.
5. Report results conservatively; avoid broader comparative claims until the sample includes enough heterogeneous cases.

## Immediate next tasks

- Add at least two more curated scenarios beyond pci_segmented_lab.
- Populate expert_validation_form.csv for each scenario.
- Add a script to summarize expert forms into agreement metrics.
- Update article text to state validation scope explicitly.
