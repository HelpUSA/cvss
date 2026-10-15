import fs from "node:fs/promises";
import path from "node:path";

import { prisma } from "@/lib/prisma";

import {
  syntheticTestAuth,
} from "./synthetic-auth";

const DEFAULT_ORG_SLUG =
  "e2e-org";
const DEFAULT_USER_EMAIL =
  "synthetic-e2e@helpus.invalid";
const DEFAULT_POLICY_ID =
  "E2E-CVSS-ENV";
const DEFAULT_POLICY_VERSION =
  "1";

function assertSyntheticMode() {
  if (
    process.env.E2E_SYNTHETIC_AUTH !==
    "1"
  ) {
    return false;
  }

  const databaseUrl =
    process.env.DATABASE_URL ?? "";

  if (
    !databaseUrl ||
    !/localhost|127\.0\.0\.1|postgres/i.test(
      databaseUrl,
    )
  ) {
    throw new Error(
      "Synthetic auth requires an explicit disposable PostgreSQL DATABASE_URL.",
    );
  }

  return true;
}

export default async function globalSetup() {
  if (!assertSyntheticMode()) {
    return;
  }

  const baseURL =
    process.env.E2E_BASE_URL?.trim() ||
    "http://127.0.0.1:3000";
  const parsedBaseURL =
    new URL(baseURL);

  if (
    parsedBaseURL.protocol !== "http:" ||
    ![
      "127.0.0.1",
      "localhost",
    ].includes(parsedBaseURL.hostname)
  ) {
    throw new Error(
      "Synthetic E2E auth may only run against localhost/127.0.0.1.",
    );
  }

  const organizationSlug =
    process.env
      .E2E_ORGANIZATION_SLUG
      ?.trim() ||
    DEFAULT_ORG_SLUG;

  if (
    !organizationSlug.startsWith("e2e")
  ) {
    throw new Error(
      "Synthetic auth requires E2E_ORGANIZATION_SLUG to start with 'e2e'.",
    );
  }

  const user =
    await prisma.user.upsert({
      where: {
        email:
          DEFAULT_USER_EMAIL,
      },
      create: {
        name:
          "Synthetic E2E Operator",
        email:
          DEFAULT_USER_EMAIL,
        emailVerified: true,
        status: "ACTIVE",
        platformRole: "USER",
      },
      update: {
        name:
          "Synthetic E2E Operator",
        emailVerified: true,
        status: "ACTIVE",
        platformRole: "USER",
      },
      select: {
        id: true,
      },
    });

  const organization =
    await prisma.organization.upsert({
      where: {
        slug: organizationSlug,
      },
      create: {
        name:
          "E2E Synthetic Organization",
        slug: organizationSlug,
        status: "ACTIVE",
      },
      update: {
        name:
          "E2E Synthetic Organization",
        status: "ACTIVE",
      },
      select: {
        id: true,
      },
    });

  await prisma.membership.upsert({
    where: {
      organizationId_userId: {
        organizationId:
          organization.id,
        userId: user.id,
      },
    },
    create: {
      organizationId:
        organization.id,
      userId: user.id,
      role: "ADMIN",
      status: "ACTIVE",
    },
    update: {
      role: "ADMIN",
      status: "ACTIVE",
      suspendedAt: null,
      revokedAt: null,
    },
  });

  await prisma
    .organizationPolicyVersion
    .upsert({
      where: {
        organizationId_policyId_version:
          {
            organizationId:
              organization.id,
            policyId:
              DEFAULT_POLICY_ID,
            version:
              DEFAULT_POLICY_VERSION,
          },
      },
      create: {
        organizationId:
          organization.id,
        policyId:
          DEFAULT_POLICY_ID,
        version:
          DEFAULT_POLICY_VERSION,
        contentHash:
          "e2e-synthetic-policy-v1",
        status: "ACTIVE",
        effectiveFrom:
          new Date(0),
        createdByUserId:
          user.id,
      },
      update: {
        contentHash:
          "e2e-synthetic-policy-v1",
        status: "ACTIVE",
        effectiveFrom:
          new Date(0),
      },
    });

  const ctx =
    await syntheticTestAuth.$context;

  const cookies =
    await ctx.test.getCookies({
      userId: user.id,
      domain:
        parsedBaseURL.hostname,
    });

  const storagePath =
    process.env
      .E2E_STORAGE_STATE
      ?.trim() ||
    path.resolve(
      process.cwd(),
      "playwright/.auth/user.json",
    );

  await fs.mkdir(
    path.dirname(storagePath),
    {
      recursive: true,
    },
  );

  await fs.writeFile(
    storagePath,
    JSON.stringify(
      {
        cookies,
        origins: [],
      },
      null,
      2,
    ),
    "utf8",
  );

  process.env.E2E_ORGANIZATION_SLUG =
    organizationSlug;
  process.env.E2E_ACTIVE_POLICY_LABEL =
    `${DEFAULT_POLICY_ID} · v${DEFAULT_POLICY_VERSION}`;
}
