# CVSS Environmental Assessment Architecture

## Purpose

The system supports research and operational experimentation around CVSS Environmental scoring. It combines structured local context, deterministic rule-based assessment, audit traces, article-ready outputs, and a cloud dashboard.

## Components

### 1. Case inputs

Structured case data lives under cases/. The current canonical case is pci_segmented_lab.

Typical inputs include assets, vulnerabilities, expected labels, and local context relevant to Environmental metrics.

### 2. Prototype engine

The Python prototype under app/ loads case data, applies deterministic assessment logic, computes Environmental labels and scores, and emits run artifacts.

### 3. Output artifacts

Generated outputs live under outputs/runs/. A clean run includes summary.csv, before_after_comparison.csv, audit_trace.jsonl, report.md, run_manifest.json, and article_table_env_effects.md.

### 4. Database

The web dashboard uses Prisma with PostgreSQL. Railway PostgreSQL is the production database. The web app falls back to web/data/seed.json if DATABASE_URL is not present.

### 5. Web dashboard

The Next.js app under web/ displays run metrics, comparisons, assessments, manifest context, and audit-trace material. Production is deployed on Vercel.

### 6. Research article

The LaTeX article under article/ uses the deterministic run output as artifact-validation evidence. The article should not overstate the current deterministic run as a full multi-agent or human-comparative result.

## Future target architecture

The next production-grade architecture should split responsibilities:

- Vercel: frontend, dashboard, lightweight server-rendered pages;
- Railway: PostgreSQL and backend executor service;
- AI Bridge/watcher: mediated evidence analysis and multi-agent experimental condition;
- object/file storage: uploaded evidence and generated reports when needed.
