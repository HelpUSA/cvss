# Article language audit

Updated: 2026-05-28 15:28:35

## Purpose

Check that the manuscript language remains aligned with the current evidence package.

## Required language

- Current scenarios are synthetic curated scenarios.
- Current validation is automated watcher IA validation.
- Independent human expert adjudication is future work.
- Engine is a prototype deterministic scoring policy unless the official CVSS environmental formula is implemented.

## Scan results

### human expert validation
- no matches

### independent human expert adjudication
- D:\dev\cvss\article\generated\automated_validation_summary_table.txt:11 Interpretation: automated watcher IA validation only; no completed independent human expert adjudication is claimed.
- D:\dev\cvss\article\sections\07_expected_evaluation.tex:135 Automated watcher IA validation scope. The current validation workflow is automated and watcher mediated. The pipeline generates evidence linked review rows and reports under validation/ai_review from committed curated artifacts. It does not claim completed independent human expert adjudication. Human expert review is treated as future comparative work rather than a dependency for the present evaluation.
- D:\dev\cvss\article\sections\07_expected_evaluation.tex:157 as upgraded. These values are generated from committed scenario artifacts and automated watcher IA validation outputs, not from completed independent human expert adjudication.

### production-grade
- no matches

### official CVSS
- D:\dev\cvss\article\sections\03_related_work_and_gap.tex:4 CVSS is the reference scoring vocabulary for many vulnerability-management workflows. CVSS v3.1 organizes metrics into Base, Temporal, and Environmental groups, while CVSS v4.0 reorganizes the model into Base, Threat, Environmental, and Supplemental groups. This distinction is important for the present work because Base metrics describe intrinsic vulnerability properties, whereas Environmental metrics describe characteristics that are unique to the consumer's deployment environment \cite{firstcvss31,firstcvss40}. The official CVSS v4.0 specification explicitly recommends enriching Base metrics with Threat and Environmental values when the consumer needs a score that better reflects organizational risk context \cite{firstcvss40}.

### synthetic curated scenarios
- D:\dev\cvss\article\sections\07_expected_evaluation.tex:166 Synthetic curated scenarios. The current scenario package uses synthetic curated scenarios and placeholder CVE-like identifiers for method development and reproducibility. These fixtures support deterministic pipeline testing and article artifact generation, but they should not be interpreted as claims about real-world CVE exploitability or production incident risk.

### automated watcher IA validation
- D:\dev\cvss\article\generated\automated_validation_summary_table.txt:11 Interpretation: automated watcher IA validation only; no completed independent human expert adjudication is claimed.
- D:\dev\cvss\article\sections\07_expected_evaluation.tex:135 Automated watcher IA validation scope. The current validation workflow is automated and watcher mediated. The pipeline generates evidence linked review rows and reports under validation/ai_review from committed curated artifacts. It does not claim completed independent human expert adjudication. Human expert review is treated as future comparative work rather than a dependency for the present evaluation.
- D:\dev\cvss\article\sections\07_expected_evaluation.tex:138 Automated watcher IA validation summary table.
- D:\dev\cvss\article\sections\07_expected_evaluation.tex:139 Automated watcher IA validation outputs were not found during this run.
- D:\dev\cvss\article\sections\07_expected_evaluation.tex:157 as upgraded. These values are generated from committed scenario artifacts and automated watcher IA validation outputs, not from completed independent human expert adjudication.
- D:\dev\cvss\article\sections\07_expected_evaluation.tex:163 Results package artifacts. The current results package includes curated run summaries, automated watcher IA validation summaries, and adjustment trace summaries. These artifacts provide the basis for the reported scenario totals, decision counts, and traceability claims.

### prototype deterministic
- no matches

