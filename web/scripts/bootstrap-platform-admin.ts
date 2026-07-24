import {
  PrismaClient,
} from "@prisma/client";

import {
  normalizeEmail,
} from "../src/lib/normalize-email";
import {
  hashPassword,
} from "../src/lib/password";

const prisma = new PrismaClient();

function requiredEnvironmentValue(
  name: string,
): string {
  const value =
    process.env[name]?.trim();

  if (!value) {
    throw new Error(
      `Required environment variable is missing: ${name}`,
    );
  }

  return value;
}

async function main(): Promise<void> {
  const email = normalizeEmail(
    requiredEnvironmentValue(
      "PLATFORM_ADMIN_EMAIL",
    ),
  );

  const name =
    requiredEnvironmentValue(
      "PLATFORM_ADMIN_NAME",
    );

  const password =
    requiredEnvironmentValue(
      "PLATFORM_ADMIN_PASSWORD",
    );

  if (
    name.length < 2 ||
    name.length > 160
  ) {
    throw new Error(
      "PLATFORM_ADMIN_NAME must contain between 2 and 160 characters.",
    );
  }

  const passwordHash =
    await hashPassword(password);

  const result = await prisma.$transaction(
    async (transaction) => {
      const existingUser =
        await transaction.user.findUnique({
          where: {
            email,
          },

          include: {
            accounts: {
              where: {
                providerId: "credential",
              },

              select: {
                id: true,
              },
            },
          },
        });

      if (existingUser) {
        if (
          existingUser.platformRole !==
          "PLATFORM_ADMIN"
        ) {
          throw new Error(
            "The configured email belongs to a non-platform-admin user.",
          );
        }

        if (
          existingUser.status !== "ACTIVE"
        ) {
          throw new Error(
            "The configured platform administrator is not active.",
          );
        }

        if (
          existingUser.accounts.length > 0
        ) {
          return {
            status: "already_configured",
            userId: existingUser.id,
          };
        }

        await transaction.account.create({
          data: {
            accountId: existingUser.id,
            providerId: "credential",
            userId: existingUser.id,
            password: passwordHash,
          },
        });

        await transaction.securityAuditEvent.create({
          data: {
            actorUserId: existingUser.id,

            action:
              "AUTH_PLATFORM_ADMIN_CREDENTIAL_CREATED",

            targetType: "User",
            targetId: existingUser.id,

            metadata: {
              source:
                "environment-bootstrap",
            },
          },
        });

        return {
          status: "credential_created",
          userId: existingUser.id,
        };
      }

      const user =
        await transaction.user.create({
          data: {
            email,
            name,
            emailVerified: true,
            status: "ACTIVE",

            platformRole:
              "PLATFORM_ADMIN",
          },
        });

      await transaction.account.create({
        data: {
          accountId: user.id,
          providerId: "credential",
          userId: user.id,
          password: passwordHash,
        },
      });

      await transaction.securityAuditEvent.create({
        data: {
          actorUserId: user.id,

          action:
            "AUTH_PLATFORM_ADMIN_BOOTSTRAPPED",

          targetType: "User",
          targetId: user.id,

          metadata: {
            source:
              "environment-bootstrap",
          },
        },
      });

      return {
        status: "created",
        userId: user.id,
      };
    },
    {
      isolationLevel: "Serializable",
    },
  );

  console.log(
    JSON.stringify(
      {
        ok: true,
        status: result.status,
        userId: result.userId,
        email,
        organizationCreated: false,
        passwordPrinted: false,
        passwordHashPrinted: false,
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
