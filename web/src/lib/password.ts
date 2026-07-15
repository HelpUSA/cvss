import {
  hash,
  type Options,
  verify,
} from "@node-rs/argon2";

export const ARGON2ID_OPTIONS: Options = {
  algorithm: 2,
  memoryCost: 65_536,
  timeCost: 3,
  parallelism: 4,
  outputLen: 32,
};

export async function hashPassword(
  password: string,
): Promise<string> {
  if (password.length < 12 || password.length > 128) {
    throw new Error(
      "Password length must be between 12 and 128 characters.",
    );
  }

  return hash(password, ARGON2ID_OPTIONS);
}

export async function verifyPassword(input: {
  hash: string;
  password: string;
}): Promise<boolean> {
  try {
    return await verify(
      input.hash,
      input.password,
      ARGON2ID_OPTIONS,
    );
  } catch {
    return false;
  }
}
