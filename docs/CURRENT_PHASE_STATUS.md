# CVSS current phase status

Updated: 
2026-05-28 13:34:05

## Completed in current phase

- Research sequence and interactive-site order documented.
- Scenario input and pipeline output schemas documented.
- Deterministic environmental scoring engine checkpoint added.
- Pilot and additional curated scenarios added.
- Scenario runner generates before/after comparison and curated summary outputs.
- Automated watcher IA validation queue and outputs regenerated.
- Static dashboard refreshed from generated curated scenario values.
- Static interactive CVSS calculator MVP added to index.html.
- JSON, CSV, and pipeline JSON export path added for the interactive MVP.
- scripts/convert_interactive_export.py converts pipeline JSON into scenario package structure.

## Current public deployment model

The production site should remain a clean static Vercel project from repository root. Do not return to the old Next.js project or npm build path.

## Next checkpoint

1. Verify the clean Vercel static project autodeploys commit 6d6f44a or newer.
2. If production does not show the interactive MVP, redeploy the clean static project from Vercel UI, not the old Next.js project.
3. Add more realistic CVSS vectors and scenario evidence files for each curated scenario.
4. Fold converter, dashboard generation, article input generation, and PDF build into scripts/rebuild_all.ps1.
5. Update article Results and Discussion with multi-scenario totals and interactive MVP scope.

## Scenario evidence enrichment - 
2026-05-28 13:59:31

Added standardized evidence files to each curated scenario: topology.yaml, firewall_rules.yaml, business_impact.yaml, pci_scope.yaml, and expected_expert_labels.yaml. Rebuild wrapper was run to keep generated outputs synchronized.

