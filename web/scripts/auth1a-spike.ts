import { prismaAdapter } from "better-auth/adapters/prisma";
import { betterAuth } from "better-auth";

import { normalizeEmail } from "../src/lib/normalize-email";
import {
  ARGON2ID_OPTIONS,
  hashPassword,
  verifyPassword,
} from "../src/lib/password";

async function main(): Promise<void> {
  const nodeMajor = Number.parseInt(
    process.versions.node.split(".")[0] ?? "0",
    10,
  );

  if (process.release.name !== "node") {
    throw new Error("Node.js runtime is required.");
  }

  if (nodeMajor !== 22) {
    throw new Error(
      `Expected Node.js 22.x; received ${process.versions.node}.`,
    );
  }

  if (typeof betterAuth !== "function") {
    throw new Error("Better Auth import failed.");
  }

  if (typeof prismaAdapter !== "function") {
    throw new Error("Prisma adapter import failed.");
  }

  const normalizedEmail = normalizeEmail(
    "  PLATFORM.ADMIN@HELPUSBR.COM  ",
  );

  if (normalizedEmail !== "platform.admin@helpusbr.com") {
    throw new Error("Email normalization failed.");
  }

  const password = "Auth1A-Argon2id-Spike-2026!";
  const encodedHash = await hashPassword(password);

  if (!encodedHash.startsWith("$argon2id$")) {
    throw new Error("Argon2id marker was not generated.");
  }

  const accepted = await verifyPassword({
    hash: encodedHash,
    password,
  });

  const rejected = !(await verifyPassword({
    hash: encodedHash,
    password: `${password}-invalid`,
  }));

  if (!accepted || !rejected) {
    throw new Error("Password verification contract failed.");
  }

  console.log(
    JSON.stringify(
      {
        auth1aSpikeOk: true,
        runtime: process.release.name,
        nodeVersion: process.versions.node,
        betterAuthImport: true,
        prismaAdapterImport: true,
        algorithm: "argon2id",
        algorithmValue: ARGON2ID_OPTIONS.algorithm,
        memoryCost: ARGON2ID_OPTIONS.memoryCost,
        timeCost: ARGON2ID_OPTIONS.timeCost,
        parallelism: ARGON2ID_OPTIONS.parallelism,
        outputLen: ARGON2ID_OPTIONS.outputLen,
        normalizedEmail,
        correctPasswordAccepted: accepted,
        invalidPasswordRejected: rejected,
        passwordPrinted: false,
        passwordHashPrinted: false,
      },
      null,
      2,
    ),
  );
}

main().catch((error: unknown) => {
  console.error(
    error instanceof Error
      ? error.message
      : String(error),
  );

  process.exitCode = 1;
});
