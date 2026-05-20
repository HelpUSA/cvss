# CVSS Environmental Assessment

Cloud prototype and research artifact for CVSS Environmental assessment with local-context evidence, before/after scoring, audit traces, and an article-ready evaluation workflow.

## Current cloud state

- Public domain: https://cvss.helpusbr.com
- Vercel project: help-us/cvss
- GitHub repository: https://github.com/HelpUSA/cvss
- Local workspace: D:/dev/cvss
- Database: Railway PostgreSQL
- Web app: Next.js under web/
- Data layer: Prisma with DATABASE_URL in Vercel Production and local seed fallback

## What the application does now

The current application is a visual dashboard for the deterministic PCI segmented lab run. It displays:

- run and case metadata;
- core metrics for the current assessment run;
- before/after CVSS Environmental score comparison;
- finding-level rows with asset, CVE, vulnerability type, score delta, MAV change, and expected-label match;
- assessment rows for before and after states;
- audit-trace material and run manifest context.

Current validated run characteristics:

- case: pci_segmented_lab;
- findings: 6;
- assessments: 12;
- downgraded findings: 2;
- unchanged findings: 4;
- upgraded findings: 0;
- mean environmental delta: approximately -0.267.

## Important URLs

- Production domain: https://cvss.helpusbr.com
- Vercel alias: https://cvss-help-us.vercel.app
- Last generated deployment example: https://cvss-gq625yfi5-help-us.vercel.app

## Repository layout

text
article/ LaTeX manuscript and sections
app/ Python prototype and deterministic assessment logic
cases/ Structured lab cases and input evidence
outputs/ Generated runs, manifests, comparisons, traces and reports
research/ Research notes and source material
web/ Next.js dashboard, Prisma schema, seed data and frontend
_docs/archive Historical or obsolete material when applicable


## Local validation

text
cd D:/dev/cvss/web
npm install
npm run build


## Database workflow

text
cd D:/dev/cvss/web
npm run db:push
npm run db:seed


Production uses the Railway PostgreSQL connection through Vercel environment variable DATABASE_URL.

## Next implementation priorities

1. Add dashboard filters and finding detail pages.
2. Add case/run history and explicit data-source indicator.
3. Add upload/manual case creation for assets, findings and environment context.
4. Add backend execution path for running new assessments from the UI.
5. Add report export in CSV, JSON, Markdown and article-table formats.
6. Add authentication before using sensitive customer evidence.
7. Integrate the watcher/AI Bridge mediated condition for the research evaluation.
