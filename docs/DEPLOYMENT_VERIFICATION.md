# Public deployment verification

Date: 2026-07-08

## Purpose

This note documents how to verify that the public CVSS URL is serving this repository's real dashboard instead of an unrelated Vercel project or stale domain alias.

## Current local source state

The real public dashboard source is the Next.js app under `web/src/app`.

Tracked deploy-related files confirmed locally:

- `web/package.json`
- `web/vercel.json`
- `web/next.config.mjs`
- `web/src/app/layout.tsx`
- `web/src/app/page.tsx`
- `web/src/app/DashboardClient.tsx`
- `.github/workflows/real-pipeline.yml`

The Vercel config tracked in `web/vercel.json` declares:

```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "installCommand": "npm install"
}
```

`web/next.config.mjs` uses `output: "standalone"`.

## Public mismatch previously observed

A previous public check showed the domain reachable but serving unrelated HairStyle Studio content instead of the CVSS Environmental Dashboard.

That symptom indicates a public deployment routing/configuration problem, such as:

- Vercel domain assigned to the wrong project.
- Vercel project connected to the wrong repository or branch.
- Vercel project Root Directory not set to `web`.
- A stale alias or preview deployment being checked instead of the production dashboard.
- Cached or unrelated static content being served by the public URL.

Local validation cannot fix a wrong domain mapping, but docs and verification steps can make the mismatch explicit.

## Expected public identity markers

The public HTML should make these CVSS dashboard markers visible in rendered content, metadata, or deploy-verification markup:

- `CVSS Environmental Dashboard`
- `official_cvss`
- `contextual_environmental`
- `evidence`

The public HTML must not contain known wrong-site markers such as:

- `HairStyle Studio`
- `hairstyle`
- `hair style`

## Manual verification

After deployment, check the public URL with a simple fetch:

```bash
python -<<'PY'
from urllib.request import urlopen

url = "https://<public-domain>"
html = urlopen(url, timeout=20).read().decode("utf-8", errors="replace")

expected = [
    "CVSS Environmental Dashboard",
    "official_cvss",
    "contextual_environmental",
    "evidence",
]
forbidden = [
    "HairStyle Studio",
    "hairstyle",
    "hair style",
]

missing = [marker for marker in expected if marker not in html]
present_forbidden = [marker for marker in forbidden if marker.lower() in html.lower()]

print("missing=", missing)
print("forbidden=", present_forbidden)

if missing or present_forbidden:
    raise SystemExit(1)
print("CVSS_PUBLIC_DEPLOY_VERIFY_OK", url)
PY
```

## Acceptance criteria

Accept the public deployment only when all of the following are true:

1. Local repo is clean and synced with `origin/real-world-cvss`.
2. `npm run build --prefix web` succeeds.
3. `python scripts/validate_real_pipeline.py --export-evidence` succeeds.
4. Vercel deployment is connected to this repository and the `real-world-cvss` branch or the intended production branch.
5. Vercel Root Directory is `web` when the project is configured from the repository root.
6. The public URL contains the expected CVSS markers.
7. The public URL does not contain wrong-site markers such as HairStyle Studio.
8. The accepted URL is recorded in the release/deploy note.

## Troubleshooting

If local validation passes but public verification fails:

1. Open the Vercel project settings.
2. Confirm the Git repository is `HelpUSA/cvss`.
3. Confirm the selected branch matches the intended deployment branch.
4. Confirm the project Root Directory is `web`.
5. Confirm the custom domain points to this Vercel project, not another project.
6. Redeploy after changing project settings.
7. Re-run the public verification snippet above.
