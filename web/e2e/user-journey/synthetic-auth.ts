import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { testUtils } from "better-auth/plugins";

import { prisma } from "@/lib/prisma";

function requiredTestSecret(): string {
  const value =
    process.env.BETTER_AUTH_SECRET?.trim();

  if (!value || value.length < 32) {
    throw new Error(
      "BETTER_AUTH_SECRET must be set to at least 32 characters for synthetic E2E auth.",
    );
  }

  return value;
}

function requiredLocalBaseUrl(): string {
  const raw =
    process.env.E2E_BASE_URL?.trim() ||
    "http://127.0.0.1:3000";

  const url = new URL(raw);

  if (
    url.protocol !== "http:" ||
    !["127.0.0.1", "localhost"].includes(
      url.hostname,
    )
  ) {
    throw new Error(
      "Synthetic E2E auth is restricted to local HTTP hosts (127.0.0.1/localhost).",
    );
  }

  return url.origin;
}

export const syntheticTestAuth =
  betterAuth({
    appName:
      "HelpUS CVSS Synthetic E2E",
    baseURL: requiredLocalBaseUrl(),
    basePath: "/api/auth",
    secret: requiredTestSecret(),
    trustedOrigins: [
      requiredLocalBaseUrl(),
    ],
    database: prismaAdapter(prisma, {
      provider: "postgresql",
    }),
    emailAndPassword: {
      enabled: false,
      disableSignUp: true,
    },
    session: {
      expiresIn: 60 * 60,
      updateAge: 60 * 10,
    },
    plugins: [
      testUtils(),
    ],
  });
