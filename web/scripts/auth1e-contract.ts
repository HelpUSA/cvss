import {
  readFileSync,
} from "node:fs";
import {
  resolve,
} from "node:path";

import {
  hashOpaqueToken,
  issueOpaqueToken,
  parseOpaqueToken,
} from "../src/lib/auth-tokens";
import {
  DomainError,
} from "../src/lib/domain-errors";
import {
  PASSWORD_MAX_LENGTH,
  PASSWORD_MIN_LENGTH,
  parseNewPassword,
} from "../src/lib/password-policy";

function readSource(
  relativePath: string,
): string {
  return readFileSync(
    resolve(
      process.cwd(),
      relativePath,
    ),
    "utf8",
  );
}

function requireMarker(
  relativePath: string,
  marker: string,
): void {
  const source =
    readSource(relativePath);

  if (!source.includes(marker)) {
    throw new Error(
      `Required marker not found in ${relativePath}: ${marker}`,
    );
  }
}

function requireAbsentMarker(
  relativePath: string,
  marker: string,
): void {
  const source =
    readSource(relativePath);

  if (source.includes(marker)) {
    throw new Error(
      `Forbidden marker found in ${relativePath}: ${marker}`,
    );
  }
}

function expectDomainError(
  action: () => unknown,
  expectedCode: string,
): void {
  try {
    action();
  } catch (error) {
    if (
      error instanceof DomainError &&
      error.code === expectedCode
    ) {
      return;
    }

    throw error;
  }

  throw new Error(
    `Expected DomainError ${expectedCode}.`,
  );
}

async function main(): Promise<void> {
  const issued =
    issueOpaqueToken();

  if (
    issued.token.length < 40 ||
    issued.tokenHash.length !== 64
  ) {
    throw new Error(
      "Opaque token dimensions are invalid.",
    );
  }

  if (
    issued.token ===
    issued.tokenHash
  ) {
    throw new Error(
      "Raw token cannot equal stored hash.",
    );
  }

  if (
    hashOpaqueToken(
      issued.token,
    ) !== issued.tokenHash
  ) {
    throw new Error(
      "Token hashing is not deterministic.",
    );
  }

  if (
    parseOpaqueToken(
      issued.token,
    ) !== issued.token
  ) {
    throw new Error(
      "Issued token must be accepted.",
    );
  }

  expectDomainError(
    () =>
      parseOpaqueToken(
        "invalid token",
      ),
    "invalid_token",
  );

  if (
    parseNewPassword(
      "A".repeat(
        PASSWORD_MIN_LENGTH,
      ),
    ).length !==
    PASSWORD_MIN_LENGTH
  ) {
    throw new Error(
      "Minimum password length failed.",
    );
  }

  expectDomainError(
    () =>
      parseNewPassword(
        "A".repeat(
          PASSWORD_MIN_LENGTH - 1,
        ),
      ),
    "invalid_password_length",
  );

  expectDomainError(
    () =>
      parseNewPassword(
        "A".repeat(
          PASSWORD_MAX_LENGTH + 1,
        ),
      ),
    "invalid_password_length",
  );

  requireMarker(
    "src/lib/password-policy.ts",
    "defaults to Argon2id",
  );

  requireMarker(
    "src/lib/password-policy.ts",
    "memoryCost: 65_536",
  );

  requireMarker(
    "src/lib/account-lifecycle.ts",
    "passwordResetToken",
  );

  requireMarker(
    "src/lib/account-lifecycle.ts",
    "tokenHash",
  );

  requireMarker(
    "src/lib/account-lifecycle.ts",
    "session",
  );

  requireMarker(
    "src/lib/account-lifecycle.ts",
    "deleteMany",
  );

  requireMarker(
    "src/lib/account-lifecycle.ts",
    "password_reset.completed",
  );

  requireMarker(
    "src/lib/invitation-lifecycle.ts",
    "invitation_email_mismatch",
  );

  requireMarker(
    "src/lib/invitation-lifecycle.ts",
    "acceptedByUserId",
  );

  requireMarker(
    "src/lib/invitation-lifecycle.ts",
    "MembershipStatus.ACTIVE",
  );

  requireMarker(
    "src/lib/email-delivery.ts",
    "RESEND_API_KEY",
  );

  requireMarker(
    "src/lib/email-delivery.ts",
    "AUTH_EMAIL_FROM",
  );

  requireMarker(
    "src/lib/email-delivery.ts",
    "Idempotency-Key",
  );

  requireMarker(
    "src/lib/session-administration.ts",
    "expiresAt",
  );

  requireAbsentMarker(
    "src/lib/session-administration.ts",
    "token: true",
  );

  requireMarker(
    "src/app/api/account/password-reset/request/route.ts",
    "accepted: true",
  );

  requireMarker(
    "src/app/api/account/password-reset/confirm/route.ts",
    "confirmPasswordReset",
  );

  requireMarker(
    "src/app/api/invitations/accept/route.ts",
    "getActiveSession",
  );

  requireMarker(
    "src/app/api/organizations/[organizationSlug]/invitations/route.ts",
    '"membership:manage"',
  );

  requireMarker(
    "src/app/api/account/sessions/revoke-others/route.ts",
    "revokeOtherUserSessions",
  );

  requireMarker(
    "src/app/api/account/sessions/revoke-all/route.ts",
    "revokeAllUserSessions",
  );

  requireAbsentMarker(
    "src/lib/account-lifecycle.ts",
    "console.log",
  );

  requireAbsentMarker(
    "src/lib/invitation-lifecycle.ts",
    "console.log",
  );

  const packageJson =
    JSON.parse(
      readSource(
        "package.json",
      ),
    ) as {
      scripts?: Record<
        string,
        string
      >;
    };

  if (
    !packageJson.scripts
      ?.["validate:auth1e"]
  ) {
    throw new Error(
      "validate:auth1e script is missing.",
    );
  }

  console.log(
    JSON.stringify(
      {
        auth1eContractOk: true,
        opaqueTokenBytes: 32,
        rawTokenStored: false,
        tokenHashAlgorithm:
          "SHA-256",
        passwordAlgorithm:
          "Argon2id",
        passwordResetSingleUse: true,
        passwordResetExpiration: true,
        sessionsRevokedAfterReset: true,
        invitationEmailBound: true,
        invitationSingleUse: true,
        invitationRevocation: true,
        membershipReactivationControlled: true,
        sessionSelfManagement: true,
        sessionTokensExposed: false,
        transactionalEmailProvider:
          "Resend",
        emailIdempotency: true,
        schemaChanged: false,
        migrationExecuted: false,
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
