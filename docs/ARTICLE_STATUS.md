# CVSS Article Current Status

## Current state

- Manuscript: D:/dev/cvss/article/main.tex
- PDF: D:/dev/cvss/article/main.pdf
- Canonical article sections: D:/dev/cvss/article/sections
- References: D:/dev/cvss/article/references.bib
- Current cloud artifact: https://cvss.helpusbr.com

## Completed

- Legacy IEEE draft, obsolete backups, old ZIPs and corrupted comparative material were archived.
- Canonical article tree was rebuilt under article/.
- Related work was expanded with CVSS, NVD, SSVC, EPSS and prior environmental-scoring sources.
- A clean deterministic PCI segmented lab run was generated under outputs/runs/.
- Run manifest and input/output hashes were generated.
- Section 07 was updated from the clean deterministic run.
- LaTeX and BibTeX issues were corrected and the article rebuilt successfully.
- A cloud dashboard was created and deployed for the artifact.

## Current artifact-validation result

The current deterministic run should be described as an artifact-validation result:

- case: pci_segmented_lab;
- findings: 6;
- assessments: 12;
- downgraded findings: 2;
- unchanged findings: 4;
- upgraded findings: 0;
- all expected label checks passed in the controlled case;
- mean environmental delta: approximately -0.267;
- maximum absolute delta: 0.8.

## Important caution

The current run is not yet the final human-vs-LLM-vs-watcher comparison. It validates the deterministic artifact and establishes a reproducible baseline.

## Next priorities

1. Add explicit methodology for the no-tool LLM and watcher multi-agent conditions.
2. Freeze expert-label protocol and final evaluation manifests.
3. Run and document all final evaluation conditions.
4. Add limitations around deterministic baseline versus true multi-agent watcher condition.
5. Add a figure or short artifact description for the cloud dashboard.
6. Prepare final submission-ready PDF after experimental results are complete.

## 2026-05-27 dashboard validation update

Validated by watcher on 
2026-05-27 23:43:00
:

- Local npm run build passed in web with Prisma client generation and Next.js production build.
- Production domain https://cvss.helpusbr.com responded and contained dashboard markers.
- Vercel alias https://cvss-help-us.vercel.app responded and contained dashboard markers.
- Data-source indicator is present in the dashboard: Data source, data.source, and data.sourceDetail.
- Comparison-row filters are present and active: asset, CVE, effect, vulnerability type, expected-label match, and text query.

Immediate dashboard handoff tasks from the previous handoff are now validated. Next focus shifts to article, manuscript, and experiment formalization.

## 2026-05-27 manuscript hardening update

- Threats-to-validity section expanded to distinguish artifact validation from generalizable assessment claims.
- Conclusion rewritten to state the current contribution as a traceable deterministic baseline rather than autonomous expert replacement.
- Next remaining research work is broader comparative evaluation with more scenarios and independent expert labels.

## 2026-05-27 manuscript hardening update

- Threats-to-validity section expanded to distinguish artifact validation from generalizable assessment claims.
- Conclusion rewritten to state the current contribution as a traceable deterministic baseline rather than autonomous expert replacement.
- Next remaining research work is broader comparative evaluation with more scenarios and independent expert labels.

## 2026-05-28 broader-study protocol update

Added docs/BROADER_STUDY_PROTOCOL.md to define the next evaluation phase: manual expert assessment, LLM-only support, and watcher-mediated workflow. This protocol preserves the current manuscript boundary: deterministic artifact validation is complete, while broader comparative claims require curated scenarios and independent expert labels.

## 2026-05-28 broader-study protocol update

Added docs/BROADER_STUDY_PROTOCOL.md to define the next evaluation phase: manual expert assessment, LLM-only support, and watcher-mediated workflow. This protocol preserves the current manuscript boundary: deterministic artifact validation is complete, while broader comparative claims require curated scenarios and independent expert labels.

## 2026-05-28 curated-run summarizer update

Added scripts/summarize_curated_runs.ps1. It summarizes curated run folders into outputs/curated_run_summary.csv for manuscript tables and broader-study tracking. The first generated summary reflects the canonical pci_segmented_lab run; additional curated scenarios can be added after their evidence packages and labels are completed.

## 2026-05-28 curated-run summarizer update

Added scripts/summarize_curated_runs.ps1. It summarizes curated run folders into outputs/curated_run_summary.csv for manuscript tables and broader-study tracking. The first generated summary reflects the canonical pci_segmented_lab run; additional curated scenarios can be added after their evidence packages and labels are completed.

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

## Automated watcher IA validation scope - 
2026-05-28 10:25:18

Current manuscript scope: validation evidence for this project is generated by the automated watcher IA pipeline under validation/ai_review and scripts/run_ai_validation_queue.ps1. The article must not claim completed independent human or manual expert validation. Human expert adjudication is deferred to Future Work as an optional comparative study against the automated watcher IA outputs.


## Article automated validation result note - 
2026-05-28 10:39:49

Automated watcher IA validation outputs were not found during this run.


## Article PDF build status - 
2026-05-28 11:32:00

Built article/main.pdf from article/main.tex with MiKTeX tooling available locally. Current article evidence includes automated watcher IA validation artifacts and generated article table inputs. Human expert adjudication remains future comparative work and is not claimed as completed validation.


## Curated scenario expansion results - 
2026-05-28 13:16:02

Expanded the deterministic scenario set to 
1
 curated scenarios with 
6
 findings and 
12
 assessments. Outputs were regenerated through the scenario runner, automated watcher IA validation, generated article inputs, and static dashboard. Human expert adjudication remains future comparative work.


## Results package finalized - 
2026-05-28 15:03:39

The manuscript support package now includes multi-scenario curated summaries, automated watcher IA validation summaries, adjustment trace summaries, rebuild report, static interactive MVP, and article PDF artifact. Remaining article work is editorial refinement, not pipeline blocking.


<!-- BEGIN CVSS40_AI_WATCHER_PIVOT_20260709 -->
## Strategic direction: CVSS v4.0 AI/watcher Environmental metric assessment

Date: 2026-07-09

The article should be repositioned around CVSS v4.0 Environmental metric assessment assisted by AI/watcher. CVSS v4.0 already includes official Base, Threat, Environmental, and Supplemental metric groups, so the project must not claim to add or modify official Environmental metrics.

The defensible contribution is an operational evidence layer: the watcher helps analysts collect environmental evidence, suggest candidate Environmental metric choices, link suggestions to evidence, record uncertainty, flag human-review needs, and generate reproducible trace artifacts.

Safe thesis:

> Although CVSS v4.0 defines Environmental metrics for adapting vulnerability severity to a consumer's environment, selecting those metrics remains a difficult and evidence-intensive task for human analysts. This paper proposes an AI-assisted watcher workflow that collects, structures, and traces environmental evidence to support reproducible CVSS v4.0 Environmental metric assessment without modifying the official CVSS standard.

Target paper posture: English IEEE-style method/prototype paper, double-blind, 5 to 8 pages, using ICITEICS-2026 requirements as a model but preparing for a later conference.
<!-- END CVSS40_AI_WATCHER_PIVOT_20260709 -->
