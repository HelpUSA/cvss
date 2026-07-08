# CVSS public deployment readiness

Date: 2026-07-08

## Summary

The local repository is structured for a Next.js dashboard deployment from `web/`.

Confirmed tracked files include:

- `web/package.json`
- `web/vercel.json`
- `web/next.config.mjs`
- `web/src/app/layout.tsx`
- `web/src/app/page.tsx`
- `web/src/app/DashboardClient.tsx`

The local dashboard title is `CVSS Environmental Dashboard`.

## Readiness conclusion

The local source appears consistent with the CVSS dashboard, but the previous public-domain observation showed unrelated HairStyle Studio content. Therefore, the remaining risk is public routing/configuration, not the local dashboard source.

The public deployment should not be accepted until the URL is verified using `docs/DEPLOYMENT_VERIFICATION.md`.

## Next deploy action

Use the checklist in `docs/DEPLOYMENT_VERIFICATION.md` after the next Vercel deploy. If the public URL still serves unrelated content, fix Vercel project/domain mapping before changing local application code.
