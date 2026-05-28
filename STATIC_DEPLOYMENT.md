# Static root deployment path

This is the clean deployment path for the public CVSS dashboard.

The existing Vercel project accumulated Next.js production overrides and continued to run npm build. This static root path removes Next.js, npm, Python serverless, and custom Root Directory requirements.

Clean Vercel settings: Framework Preset Other, Root Directory ./, Build Command empty, Install Command empty, Output Directory empty.

Expected public markers: CVSS Environmental Dashboard; Automated watcher IA validation; Curated validation runs; pci_segmented_lab_20260517_143146.
