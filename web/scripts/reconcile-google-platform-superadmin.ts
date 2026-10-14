import {
  PrismaClient,
} from "@prisma/client";

import {
  normalizeEmail,
} from "../src/lib/normalize-email";

const prisma = new PrismaClient();

function canonicalEmail(): string {
  return normalizeEmail(
    process.env.PLATFORM_SUPERADMIN_EMAIL?.trim() ||
      "helpus.ecommerce@gmail.com",
  );
}

async function main(): Promise<void> {
  const email = canonicalEmail();

  const user = await prisma.user.findUnique({
    where: {
      email,
    },
    include: {
      accounts: {
        select: {
          providerId: true,
        },
      },
    },
  });

  if (!user) {
    throw new Error(
      "Canonical SuperAdmin user does not exist yet. Sign in once with the configured Google account, then rerun this command.",
    );
  }

  const hasGoogleAccount =
    user.accounts.some(
      (account) =>
        account.providerId === "google",
    );

  if (!hasGoogleAccount) {
    throw new Error(
      "Refusing reconciliation: canonical SuperAdmin user is not linked to a Google account.",
    );
  }

  const updated =
    await prisma.$transaction(
      async (transaction) => {
        const result =
          await transaction.user.update({
            where: {
              id: user.id,
            },
            data: {
              status: "ACTIVE",
              platformRole:
                "PLATFORM_ADMIN",
              suspendedAt: null,
              disabledAt: null,
            },
            select: {
              id: true,
              email: true,
              status: true,
              platformRole: true,
            },
          });

        await transaction
          .securityAuditEvent
          .create({
            data: {
              actorUserId:
                user.id,
              action:
                "AUTH_GOOGLE_PLATFORM_SUPERADMIN_RECONCILED",
              targetType:
                "User",
              targetId:
                user.id,
              metadata: {
                source:
                  "environment-reconciliation",
                provider:
                  "google",
              },
            },
          });

        return result;
      },
      {
        isolationLevel:
          "Serializable",
      },
    );

  console.log(
    JSON.stringify(
      {
        ok: true,
        user: updated,
        googleLinked: true,
        passwordCreated: false,
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
        ? error.message
        : String(error),
    );

    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
