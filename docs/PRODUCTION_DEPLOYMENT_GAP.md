# Production deployment gap

Updated: 
2026-05-28 11:35:01

## Observed status

The repository, local web build, article PDF, and automated watcher IA validation artifacts are complete. If cvss.helpusbr.com does not expose the newest dashboard markers, the remaining issue is production deployment freshness or Vercel alias mapping.

## Source-side markers

- web/src/app/DashboardClient.tsx includes Automated watcher IA validation.
- validation/ai_review/outputs/ai_validation_summary.csv exists.
- article/main.pdf exists and was built locally.

## Next operational actions

1. Inspect Vercel project binding for D:/dev/cvss/web.
2. Deploy latest web build to production.
3. Set cvss.helpusbr.com alias to the deployment whose HTML includes Automated watcher IA validation.
4. Reprobe public HTML markers.

This operational gap does not change committed reproducibility artifacts.

## Targeted Vercel deploy attempt - 
2026-05-28 11:36:36

Ran a targeted Vercel production deploy/alias attempt from web. Public HTML markers were reprobed afterward. If markers remain absent, the next step is deeper Vercel project binding or domain routing diagnosis.


## Targeted Vercel deploy attempt - 
2026-05-28 11:37:05

Ran a targeted Vercel production deploy/alias attempt from web. Public HTML markers were reprobed afterward. If markers remain absent, the next step is deeper Vercel project binding or domain routing diagnosis.


## Vercel diagnostic note - 
2026-05-28 11:41:00

Repeated Vercel CLI diagnostics sometimes returned empty stdout through the watcher bridge. Public HTML still lacks the newest automated watcher IA validation markers while the repository source, local build, article PDF, and validation artifacts are complete. Treat this as an operational domain/deployment issue for a separate deployment debugging pass.


## Resolved - 
2026-05-28 14:58:03

The prior production deployment gap is resolved. Repository was made public, a deployment trigger commit was pushed, the static dashboard rebuild was fixed to preserve the interactive calculator, and production now serves the interactive MVP.

