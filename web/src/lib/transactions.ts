import {
  Prisma,
} from "@prisma/client";

import { prisma } from "@/lib/prisma";

const MAX_SERIALIZABLE_ATTEMPTS = 3;

export function isUniqueConstraintError(
  error: unknown,
): boolean {
  return (
    error instanceof
      Prisma.PrismaClientKnownRequestError &&
    error.code === "P2002"
  );
}

function isRetryableTransactionError(
  error: unknown,
): boolean {
  return (
    error instanceof
      Prisma.PrismaClientKnownRequestError &&
    error.code === "P2034"
  );
}

export async function withSerializableRetry<T>(
  operation: (
    transaction: Prisma.TransactionClient,
  ) => Promise<T>,
): Promise<T> {
  let lastError: unknown;

  for (
    let attempt = 1;
    attempt <= MAX_SERIALIZABLE_ATTEMPTS;
    attempt += 1
  ) {
    try {
      return await prisma.$transaction(
        operation,
        {
          isolationLevel:
            Prisma.TransactionIsolationLevel
              .Serializable,
        },
      );
    } catch (error) {
      lastError = error;

      if (
        !isRetryableTransactionError(
          error,
        ) ||
        attempt ===
          MAX_SERIALIZABLE_ATTEMPTS
      ) {
        throw error;
      }
    }
  }

  throw lastError;
}
