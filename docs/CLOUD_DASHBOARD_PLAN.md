# Cloud Dashboard Plan

Architecture: Next.js dashboard in `web/`, Vercel hosting, Railway PostgreSQL via Prisma. The initial dashboard is seeded from the latest deterministic run and shows summary metrics, before-after effects, assessment rows, manifest metadata, and audit-trace samples.

Deployment sequence:
1. Validate local Next.js build.
2. Initialize or link a GitHub repository.
3. Provision Railway PostgreSQL.
4. Push Prisma schema and seed the latest run.
5. Deploy the dashboard to Vercel.
6. Add the production `DATABASE_URL` to Vercel when the dashboard switches from static seed mode to DB-backed mode.
