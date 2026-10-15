import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";

import {
  hashPassword,
  verifyPassword,
} from "@/lib/password";
import { prisma } from "@/lib/prisma";
import { isCanonicalPlatformSuperAdminEmail } from "@/lib/platform-superadmin";

function requiredAuthSecret(): string {
  const value = process.env.BETTER_AUTH_SECRET?.trim();

  if (!value || value.length < 32) {
    throw new Error(
      "Configuration Error: BETTER_AUTH_SECRET must be explicitly set and be at least 32 characters long. Startup aborted in fail-closed mode."
    );
  }

  return value;
}

function requiredAuthBaseUrl(): string {
  const value =
    process.env.BETTER_AUTH_URL?.trim();

  if (!value) {
    if (process.env.VERCEL_URL) {
      return `https://${process.env.VERCEL_URL}`;
    }
    return "https://cvss.helpusbr.com";
  }

  return new URL(value).origin;
}

function trustedOrigins(): string[] {
  const origins = new Set<string>();

  origins.add(requiredAuthBaseUrl());

  for (const rawValue of (
    process.env.AUTH_TRUSTED_ORIGINS ?? ""
  ).split(",")) {
    const value = rawValue.trim();

    if (!value) {
      continue;
    }

    origins.add(new URL(value).origin);
  }

  return Array.from(origins);
}

export const auth = betterAuth({
  appName: "HelpUS CVSS",
  baseURL: requiredAuthBaseUrl(),
  basePath: "/api/auth",
  secret: requiredAuthSecret(),
  trustedOrigins: trustedOrigins(),

  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),

  emailAndPassword: {
    enabled: false,
    disableSignUp: true,
  },

  socialProviders: {
    google: {
      clientId:
        process.env.GOOGLE_CLIENT_ID ||
        process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID ||
        "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
      prompt: "select_account",
      accessType: "offline",
    },
  },

  user: {
    additionalFields: {
      status: {
        type: "string",
        required: false,
        defaultValue: "ACTIVE",
        input: false,
      },

      platformRole: {
        type: "string",
        required: false,
        defaultValue: "USER",
        input: false,
      },
    },
  },

  session: {
    expiresIn: 60 * 60 * 12,
    updateAge: 60 * 60,
  },

  databaseHooks: {
    user: {
      create: {
        before: async (user) => {
          if (
            isCanonicalPlatformSuperAdminEmail(
              user.email,
            )
          ) {
            return {
              data: {
                ...user,
                status: "ACTIVE",
                platformRole: "PLATFORM_ADMIN",
              },
            };
          }

          return {
            data: user,
          };
        },
      },
    },

    session: {
      create: {
        before: async (session) => {
          const user = await prisma.user.findUnique({
            where: {
              id: session.userId,
            },

            select: {
              status: true,
            },
          });

          if (!user || user.status !== "ACTIVE") {
            return false;
          }

          return {
            data: session,
          };
        },
      },
    },
  },
});
