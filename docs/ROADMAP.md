# CVSS Roadmap

## Current phase

The project is in cloud MVP stage. The dashboard is deployed and the deterministic PCI segmented lab run is visible online.

## Phase 1 - Stabilize cloud MVP

- Verify cvss.helpusbr.com after DNS/cache propagation.
- Add visible data-source indicator: Railway PostgreSQL versus seed fallback.
- Add a small health/status section to the dashboard.
- Keep GitHub, Vercel and Railway names aligned with cvss.

## Phase 2 - Improve dashboard usability

- Add filters by asset, CVE, effect, vulnerability type and expected-match status.
- Add finding detail pages.
- Add charts for before/after scores, delta distribution and effect counts.
- Add export buttons for CSV, JSON and Markdown.

## Phase 3 - Add case authoring and run history

- Add case list and run history.
- Add input screens or upload flow for assets and vulnerabilities.
- Persist cases, runs, evidence and reports in the database.
- Add run status and execution logs.

## Phase 4 - Add backend executor

- Create a Railway backend service for long-running assessment jobs.
- Keep Vercel focused on UI and server-rendered dashboard pages.
- Add job queue or async execution flow if needed.

## Phase 5 - Research evaluation

- Freeze the final expert-label protocol.
- Run final deterministic baseline.
- Run no-tool LLM condition.
- Run watcher/AI Bridge mediated condition.
- Compare accuracy, reproducibility, traceability, and failure modes.

## Phase 6 - Article finalization

- Update methodology with final experimental design.
- Add final results tables and figures.
- Add limitations and threat-to-validity discussion.
- Add cloud artifact/dashboard description.
- Prepare submission-ready PDF.

## 2026-05-27 continuation update

- Dashboard source/status indicator validated locally and in production.
- Comparison filters validated locally and in production.
- Article evaluation section reframed from preliminary evaluation plan to artifact validation and baseline results.
- Current next work: finalize manuscript framing, verify generated tables and figures from pci_segmented_lab outputs, rebuild article, then commit and push validated changes.

## 2026-05-27 continuation update

- Dashboard source/status indicator validated locally and in production.
- Comparison filters validated locally and in production.
- Article evaluation section reframed from preliminary evaluation plan to artifact validation and baseline results.
- Current next work: finalize manuscript framing, verify generated tables and figures from pci_segmented_lab outputs, rebuild article, then commit and push validated changes.

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
