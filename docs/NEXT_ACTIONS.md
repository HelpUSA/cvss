# CVSS next actions

Updated: 
2026-05-28 11:42:01

## Completed now

- Article PDF build artifact exists at article/main.pdf.
- Automated watcher IA validation artifacts are generated and committed.
- Delivery manifest is present.
- Dashboard source includes automated watcher IA validation panel.
- Public production domain still appears to serve an older dashboard build.

## Recommended next sequence

1. Treat cvss.helpusbr.com freshness as an operational deployment or alias issue.
2. Debug Vercel project binding and domain routing in a dedicated deployment pass.
3. Expand curated scenario coverage after production routing is resolved or in parallel.
4. Regenerate curated summary, validation queue, automated IA rows, and article inputs after each new scenario batch.
5. Keep human expert validation only as future comparative work, not as a project blocker.

## Current stop condition

Core manuscript and reproducibility deliverables are complete. The only unresolved item is public production dashboard freshness.

## Static root deployment reset - 
2026-05-28 12:45:36

Prepared a static root dashboard in index.html and vercel.json to avoid Next.js, npm build, Python serverless, and custom Root Directory behavior. If the old Vercel project continues to use Production Overrides, create a new clean Vercel project from repository root and move cvss.helpusbr.com after verifying the static markers.

