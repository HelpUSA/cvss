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
