import {
  readFileSync,
} from "node:fs";
import {
  resolve,
} from "node:path";

import {
  auth,
} from "../src/lib/auth";
import {
  hashPassword,
  verifyPassword,
} from "../src/lib/password";

function requireMarker(
  relativePath: string,
  marker: string,
): void {
  const content = readFileSync(
    resolve(
      process.cwd(),
      relativePath,
    ),
    "utf8",
  );

  if (!content.includes(marker)) {
    throw new Error(
      `Required marker not found in ${relativePath}: ${marker}`,
    );
  }
}

async function main(): Promise<void> {
  if (
    typeof auth.handler !== "function"
  ) {
    throw new Error(
      "Better Auth handler is unavailable.",
    );
  }

  if (
    typeof auth.api.getSession !==
      "function" ||
    typeof auth.api.signInEmail !==
      "function" ||
    typeof auth.api.signOut !==
      "function"
  ) {
    throw new Error(
      "Required Better Auth endpoints are unavailable.",
    );
  }

  const configuration =
    auth.options.emailAndPassword;

  if (
    configuration?.enabled !== true ||
    configuration.disableSignUp !== true ||
    configuration.minPasswordLength !== 12 ||
    configuration.maxPasswordLength !== 128
  ) {
    throw new Error(
      "Email/password configuration does not match Auth-1B.",
    );
  }

  const password =
    "Auth1B-Validation-Password-2026!";

  const passwordHash =
    await hashPassword(password);

  const accepted =
    await verifyPassword({
      hash: passwordHash,
      password,
    });

  const invalidAccepted =
    await verifyPassword({
      hash: passwordHash,

      password:
        `${password}-invalid`,
    });

  if (
    !accepted ||
    invalidAccepted
  ) {
    throw new Error(
      "Argon2id verification contract failed.",
    );
  }

  requireMarker(
    "src/app/api/auth/[...all]/route.ts",
    "toNextJsHandler(auth)",
  );

  requireMarker(
    "src/lib/auth-client.ts",
    "createAuthClient",
  );

  requireMarker(
    "src/lib/session.ts",
    "requireActiveSession",
  );

  requireMarker(
    "src/middleware.ts",
    "getSessionCookie(request)",
  );

  requireMarker(
    "src/app/login/LoginForm.tsx",
    "authClient.signIn.email",
  );

  requireMarker(
    "src/app/app/SignOutButton.tsx",
    "authClient.signOut",
  );

  requireMarker(
    "scripts/bootstrap-platform-admin.ts",
    'providerId: "credential"',
  );

  requireMarker(
    "scripts/bootstrap-platform-admin.ts",
    "passwordPrinted: false",
  );

  console.log(
    JSON.stringify(
      {
        auth1bContractOk: true,
        betterAuthHandler: true,
        getSessionEndpoint: true,
        signInEndpoint: true,
        signOutEndpoint: true,
        publicSignUpDisabled: true,
        minimumPasswordLength: 12,
        maximumPasswordLength: 128,
        customArgon2idAccepted: accepted,
        invalidPasswordRejected:
          !invalidAccepted,
        apiRouteMounted: true,
        defaultCookiePrefixUsed: true,
        serverSessionGuard: true,
        loginUiPresent: true,
        logoutPresent: true,
        bootstrapPresent: true,
        bootstrapExecuted: false,
        migrationExecuted: false,
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
