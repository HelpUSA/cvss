import { NextResponse } from "next/server";

import {
  isDomainError,
} from "@/lib/domain-errors";

const NO_STORE_HEADERS = {
  "Cache-Control":
    "private, no-store, max-age=0",
};

export function mutationSuccess(
  payload: unknown,
  status = 200,
) {
  return NextResponse.json(
    payload,
    {
      status,
      headers: NO_STORE_HEADERS,
    },
  );
}

export function mutationNotFound() {
  return NextResponse.json(
    {
      error: "not_found",
      message: "Resource was not found.",
    },
    {
      status: 404,
      headers: NO_STORE_HEADERS,
    },
  );
}

export function mutationErrorResponse(
  error: unknown,
) {
  if (isDomainError(error)) {
    return NextResponse.json(
      {
        error: error.code,
        message: error.message,
      },
      {
        status: error.status,
        headers: NO_STORE_HEADERS,
      },
    );
  }

  console.error(
    "AUTH1D_MUTATION_FAILED",
    error instanceof Error
      ? error.name
      : "UnknownError",
  );

  return NextResponse.json(
    {
      error: "internal_error",
      message:
        "The operation could not be completed.",
    },
    {
      status: 500,
      headers: NO_STORE_HEADERS,
    },
  );
}
