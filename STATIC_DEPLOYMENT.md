# Static root deployment path

This is the clean deployment path for the public CVSS dashboard.

The existing Vercel project accumulated Next.js production overrides and continued to run npm build. This static root path removes Next.js, npm, Python serverless, and custom Root Directory requirements.

Clean Vercel settings: Framework Preset Other, Root Directory ./, Build Command empty, Install Command empty, Output Directory empty.

Expected public markers: CVSS Environmental Dashboard; Automated watcher IA validation; Curated validation runs; pci_segmented_lab_20260517_143146.

## Vercel JSON reset

Removed root vercel.json because the clean static Vercel deployment should rely only on index.html with Framework Preset Other and no build commands. This avoids invalid vercel.json validation and avoids Next.js/npm detection.


## Multi-scenario dashboard checkpoint

The static dashboard now summarizes generated values from multiple curated scenarios rather than only a single deploy marker. It remains intentionally static to preserve the clean Vercel deployment path.

