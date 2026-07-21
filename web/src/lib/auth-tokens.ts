import {
  createHash,
  randomBytes,
} from "node:crypto";

import { DomainError } from "@/lib/domain-errors";

const TOKEN_BYTES = 32;
const TOKEN_PATTERN =
  /^[A-Za-z0-9_-]{40,200}$/;

export function hashOpaqueToken(
  token: string,
): string {
  return createHash("sha256")
    .update(token, "utf8")
    .digest("hex");
}

export function issueOpaqueToken(): {
  token: string;
  tokenHash: string;
} {
  const token =
    randomBytes(TOKEN_BYTES)
      .toString("base64url");

  return {
    token,
    tokenHash:
      hashOpaqueToken(token),
  };
}

export function parseOpaqueToken(
  value: unknown,
): string {
  if (typeof value !== "string") {
    throw new DomainError({
      code: "invalid_token",
      message:
        "The security token is invalid.",
      status: 400,
    });
  }

  const normalized = value.trim();

  if (
    !TOKEN_PATTERN.test(
      normalized,
    )
  ) {
    throw new DomainError({
      code: "invalid_token",
      message:
        "The security token is invalid.",
      status: 400,
    });
  }

  return normalized;
}
