import {
  MembershipRole,
  MembershipStatus,
  OrganizationStatus,
  PlatformRole,
  PrismaClient,
  UserStatus,
} from "@prisma/client";
import { hashPassword } from "../src/lib/password";

const prisma = new PrismaClient();

function requiredEnvironmentVariable(
  name: string,
): string {
  const value = process.env[name]?.trim();

  if (!value) {
    throw new Error(
      `Missing environment variable: ${name}`,
    );
  }

  return value;
}

async function provisionIdentity(input: {
  email: string;
  name: string;
  organizationName: string;
  organizationSlug: string;
  passwordHash: string;
}) {
  const email = input.email.toLowerCase();

  const user = await prisma.user.upsert({
    where: {
      email,
    },
    update: {
      name: input.name,
      emailVerified: true,
      status: UserStatus.ACTIVE,
      platformRole: PlatformRole.USER,
      suspendedAt: null,
      disabledAt: null,
    },
    create: {
      email,
      name: input.name,
      emailVerified: true,
      status: UserStatus.ACTIVE,
      platformRole: PlatformRole.USER,
    },
  });

  await prisma.account.upsert({
    where: {
      providerId_accountId: {
        providerId: "credential",
        accountId: user.id,
      },
    },
    update: {
      userId: user.id,
      password: input.passwordHash,
    },
    create: {
      providerId: "credential",
      accountId: user.id,
      userId: user.id,
      password: input.passwordHash,
    },
  });

  const organization =
    await prisma.organization.upsert({
      where: {
        slug: input.organizationSlug,
      },
      update: {
        name: input.organizationName,
        status: OrganizationStatus.ACTIVE,
        suspendedAt: null,
        archivedAt: null,
      },
      create: {
        name: input.organizationName,
        slug: input.organizationSlug,
        status: OrganizationStatus.ACTIVE,
      },
    });

  const membership =
    await prisma.membership.upsert({
      where: {
        organizationId_userId: {
          organizationId: organization.id,
          userId: user.id,
        },
      },
      update: {
        role: MembershipRole.ADMIN,
        status: MembershipStatus.ACTIVE,
        suspendedAt: null,
        revokedAt: null,
      },
      create: {
        organizationId: organization.id,
        userId: user.id,
        role: MembershipRole.ADMIN,
        status: MembershipStatus.ACTIVE,
      },
    });

  return {
    userId: user.id,
    organizationId: organization.id,
    organizationSlug: organization.slug,
    membershipId: membership.id,
  };
}

async function main(): Promise<void> {
  const password = requiredEnvironmentVariable(
    "AUTH1G_PASSWORD",
  );

  const passwordHash = await hashPassword(password);

  const first = await provisionIdentity({
    email: requiredEnvironmentVariable(
      "AUTH1G_USER_A_EMAIL",
    ),
    name: "Auth 1G User A",
    organizationName:
      "Auth 1G Organization A",
    organizationSlug: "auth1g-org-a",
    passwordHash,
  });

  const second = await provisionIdentity({
    email: requiredEnvironmentVariable(
      "AUTH1G_USER_B_EMAIL",
    ),
    name: "Auth 1G User B",
    organizationName:
      "Auth 1G Organization B",
    organizationSlug: "auth1g-org-b",
    passwordHash,
  });

  console.log(
    JSON.stringify(
      {
        auth1gSeedOk: true,
        usersProvisioned: 2,
        organizationsProvisioned: 2,
        passwordPrinted: false,
        first,
        second,
      },
      null,
      2,
    ),
  );
}

main()
  .catch((error: unknown) => {
    console.error(
      error instanceof Error
        ? error.stack ?? error.message
        : String(error),
    );

    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });