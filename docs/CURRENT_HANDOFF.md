# Current Handoff - CVSS

Generated: 2026-05-20T10:16:09

## Current state

- GitHub repository: https://github.com/HelpUSA/cvss
- Vercel project: help-us/cvss
- Production domain: https://cvss.helpusbr.com
- Vercel alias: https://cvss-help-us.vercel.app
- Railway PostgreSQL is configured and seeded.
- Vercel Production has DATABASE_URL configured.
- Local workspace: D:/dev/cvss
- Current git HEAD when this handoff was written: 5aaf4f3
- Git remote: https://github.com/HelpUSA/cvss.git

## What is working

- Next.js dashboard builds successfully.
- Dashboard is publicly accessible.
- Dashboard displays CVSS Environmental Dashboard and pci_segmented_lab.
- Repository and Vercel project are both named cvss.
- web/.gitignore excludes .vercel and .env*.local.

## Current application behavior

The application currently displays the deterministic PCI segmented lab run and its before/after Environmental score effects. It reads from Railway PostgreSQL when DATABASE_URL exists and falls back to seed.json otherwise.

## Article state

The article tree is under article/. The manuscript has been rebuilt after related-work and evaluation updates. The current evidence should be framed as artifact validation of a deterministic baseline, not as the final watcher-mediated experiment.

## Immediate next task

Implement a dashboard data-source/status indicator and then add filters for comparison rows.

## Operator notification rule

If an agent stops for a human checkpoint, blocking error, deployment/security issue, or needs the operator to return, send an operator e-mail using D:/dev/autocode/ai-bridge/scripts/watcher/notify_operator.py before stopping.

Dry-run example:

text
python scripts/watcher/notify_operator.py --dry-run --subject "CVSS checkpoint" --message "CVSS needs operator attention."


Real send depends on AI_BRIDGE_NOTIFY_EMAIL_* environment variables.

## Git status at handoff generation

text
## main...origin/main


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

## 2026-05-28 legacy case loader update

The deterministic runner now accepts both current vulnerabilities.csv case folders and legacy vulnerability_findings.csv case folders. Validation was run against pci_segmented_lab, pci_demo, and complex using temporary outputs under temp. The legacy folders are now usable as compatibility smoke scenarios, while broader-study claims still require curated evidence, independent labels, and explicit experimental design.

## 2026-05-28 legacy case loader update

The deterministic runner now accepts both current vulnerabilities.csv case folders and legacy vulnerability_findings.csv case folders. Validation was run against pci_segmented_lab, pci_demo, and complex using temporary outputs under temp. The legacy folders are now usable as compatibility smoke scenarios, while broader-study claims still require curated evidence, independent labels, and explicit experimental design.

## 2026-05-28 broader-study protocol update

Added docs/BROADER_STUDY_PROTOCOL.md to define the next evaluation phase: manual expert assessment, LLM-only support, and watcher-mediated workflow. This protocol preserves the current manuscript boundary: deterministic artifact validation is complete, while broader comparative claims require curated scenarios and independent expert labels.

## 2026-05-28 broader-study protocol update

Added docs/BROADER_STUDY_PROTOCOL.md to define the next evaluation phase: manual expert assessment, LLM-only support, and watcher-mediated workflow. This protocol preserves the current manuscript boundary: deterministic artifact validation is complete, while broader comparative claims require curated scenarios and independent expert labels.

## 2026-05-28 curated-run summarizer update

Added scripts/summarize_curated_runs.ps1. It summarizes curated run folders into outputs/curated_run_summary.csv for manuscript tables and broader-study tracking. The first generated summary reflects the canonical pci_segmented_lab run; additional curated scenarios can be added after their evidence packages and labels are completed.

## 2026-05-28 curated-run summarizer update

Added scripts/summarize_curated_runs.ps1. It summarizes curated run folders into outputs/curated_run_summary.csv for manuscript tables and broader-study tracking. The first generated summary reflects the canonical pci_segmented_lab run; additional curated scenarios can be added after their evidence packages and labels are completed.
