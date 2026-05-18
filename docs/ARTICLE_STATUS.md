# CVSS Article Current Status

## Current state

- Manuscript: D:/dev/cvss/article/main.tex
- PDF: D:/dev/cvss/article/main.pdf
- Latest clean deterministic run: outputs/runs/pci_segmented_lab_20260517_143146
- Run manifest: outputs/runs/pci_segmented_lab_20260517_143146/run_manifest.json
- Before-after table: outputs/runs/pci_segmented_lab_20260517_143146/before_after_comparison.csv
- Article-ready run table: outputs/runs/pci_segmented_lab_20260517_143146/article_table_env_effects.md

## Validation

- PDF exists: True
- PDF size: 161282 bytes
- Files checked: 17
- Bad token hits: 0
- LaTeX error markers: 2

## Completed

- Legacy IEEE draft, root ZIPs, obsolete backup files, and corrupted comparative section were archived.
- Canonical article tree was rebuilt under article/.
- Clean deterministic PCI segmented lab run was generated under outputs/runs/.
- Run manifest and input/output hashes were generated.
- Section 07 was updated from the clean deterministic run.
- Article rebuilt successfully after Section 07 update.

## Next priorities

1. Expand related work with current primary sources.
2. Add explicit methodology for the no-tool LLM and watcher multi-agent conditions.
3. Freeze expert-label protocol and run manifests for all final evaluation conditions.
4. Add limitations around deterministic baseline versus true multi-agent watcher condition.

## Related-work update

The related-work section was expanded with current primary sources for CVSS v4.0, NVD vulnerability metrics, SSVC, EPSS, environmental-aware vulnerability scoring, AutoCVS, and EvalSVA.
