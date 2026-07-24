import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";

import {
  hashPassword,
  verifyPassword,
} from "@/lib/password";
import { prisma } from "@/lib/prisma";

function requiredAuthSecret(): string {
  const value =
    process.env.BETTER_AUTH_SECRET?.trim();

  if (!value || value.length < 32) {
    throw new Error(
      "BETTER_AUTH_SECRET must contain at least 32 characters.",
    );
  }

  return value;
}

function requiredAuthBaseUrl(): string {
  const value =
    process.env.BETTER_AUTH_URL?.trim();

  if (!value) {
    throw new Error(
      "BETTER_AUTH_URL is required.",
    );
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
    enabled: true,
    disableSignUp: true,
    minPasswordLength: 12,
    maxPasswordLength: 128,

    password: {
      hash: hashPassword,
      verify: verifyPassword,
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
