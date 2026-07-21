import {
  hash,
} from "@node-rs/argon2";

import { DomainError } from "@/lib/domain-errors";

export const PASSWORD_MIN_LENGTH = 12;
export const PASSWORD_MAX_LENGTH = 128;

export function parseNewPassword(
  value: unknown,
): string {
  if (typeof value !== "string") {
    throw new DomainError({
      code: "invalid_password",
      message:
        "A valid password is required.",
      status: 400,
    });
  }

  if (
    value.length <
      PASSWORD_MIN_LENGTH ||
    value.length >
      PASSWORD_MAX_LENGTH
  ) {
    throw new DomainError({
      code: "invalid_password_length",
      message:
        `Password must contain between ${PASSWORD_MIN_LENGTH} and ${PASSWORD_MAX_LENGTH} characters.`,
      status: 400,
    });
  }

  return value;
}

export async function hashCredentialPassword(
  password: string,
): Promise<string> {
  // @node-rs/argon2 2.0.2 defaults to Argon2id.
  return hash(
    password,
    {

      memoryCost: 65_536,
      timeCost: 3,
      parallelism: 1,
      outputLen: 32,
    },
  );
}
