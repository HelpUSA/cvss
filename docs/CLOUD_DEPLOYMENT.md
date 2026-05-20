# Cloud Deployment Status

## Current production setup

- Public domain: https://cvss.helpusbr.com
- Vercel project: help-us/cvss
- Vercel project ID: prj_59QUsZ5l4W0YbgPP6QIC6JKPIvOf
- GitHub repository: https://github.com/HelpUSA/cvss
- Railway project: cvss-environmental-dashboard
- Database service: Railway PostgreSQL
- Production environment variable: DATABASE_URL configured in Vercel Production

## Validation already completed

- Vercel deployment protection was disabled for public access.
- The Vercel project was renamed from web to cvss.
- The local .vercel project metadata was relinked to projectName cvss.
- The public alias https://cvss-help-us.vercel.app returned HTTP 200.
- The deployed page body contained CVSS Environmental Dashboard.
- The deployed page body contained pci_segmented_lab.
- The GitHub repository was renamed to HelpUSA/cvss and pushed.

## Domain

The operator configured cvss.helpusbr.com in Vercel and reported it is online.

Recommended final check after DNS/cache settles:

text
curl -I -L https://cvss.helpusbr.com
curl -L https://cvss.helpusbr.com | findstr /C:"CVSS Environmental Dashboard" /C:"pci_segmented_lab"


## Notes

The old Vercel alias https://web-help-us.vercel.app may continue to respond because it was the previous project production URL. The canonical operator-facing URL is now https://cvss.helpusbr.com.
