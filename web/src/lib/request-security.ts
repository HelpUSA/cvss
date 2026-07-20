import { DomainError } from "@/lib/domain-errors";

const MAX_MUTATION_BODY_BYTES = 16_384;

function expectedOrigins(
  request: Request,
): Set<string> {
  const values = new Set<string>();

  values.add(
    new URL(request.url).origin,
  );

  const forwardedHost =
    request.headers.get(
      "x-forwarded-host",
    );

  const host =
    forwardedHost ??
    request.headers.get("host");

  const forwardedProto =
    request.headers.get(
      "x-forwarded-proto",
    );

  const protocol =
    forwardedProto ??
    new URL(request.url)
      .protocol
      .replace(":", "");

  if (host) {
    values.add(
      `${protocol}://${host}`,
    );
  }

  return values;
}

export function assertJsonMutationRequest(
  request: Request,
): void {
  const origin =
    request.headers.get("origin");

  if (
    !origin ||
    !expectedOrigins(request).has(origin)
  ) {
    throw new DomainError({
      code: "invalid_origin",
      message: "Request origin is not allowed.",
      status: 403,
    });
  }

  const fetchSite =
    request.headers.get(
      "sec-fetch-site",
    );

  if (
    fetchSite &&
    fetchSite !== "same-origin"
  ) {
    throw new DomainError({
      code: "invalid_fetch_site",
      message: "Cross-site mutation is not allowed.",
      status: 403,
    });
  }

  const contentType =
    request.headers.get(
      "content-type",
    ) ?? "";

  if (
    !contentType
      .toLowerCase()
      .startsWith("application/json")
  ) {
    throw new DomainError({
      code: "invalid_content_type",
      message:
        "Mutation requests must use application/json.",
      status: 415,
    });
  }

  const contentLength =
    request.headers.get(
      "content-length",
    );

  if (contentLength) {
    const parsed =
      Number.parseInt(
        contentLength,
        10,
      );

    if (
      !Number.isFinite(parsed) ||
      parsed < 0 ||
      parsed > MAX_MUTATION_BODY_BYTES
    ) {
      throw new DomainError({
        code: "request_too_large",
        message:
          "Mutation request exceeds the permitted size.",
        status: 413,
      });
    }
  }
}

export async function readJsonObject(
  request: Request,
): Promise<Record<string, unknown>> {
  let value: unknown;

  try {
    value = await request.json();
  } catch {
    throw new DomainError({
      code: "invalid_json",
      message: "Request body is not valid JSON.",
      status: 400,
    });
  }

  if (
    !value ||
    typeof value !== "object" ||
    Array.isArray(value)
  ) {
    throw new DomainError({
      code: "invalid_json_object",
      message:
        "Request body must be a JSON object.",
      status: 400,
    });
  }

  return value as Record<string, unknown>;
}

export type RequestAuditContext = {
  ipAddress?: string;
  userAgent?: string;
};

function truncate(
  value: string | null,
  maximum: number,
): string | undefined {
  if (!value) {
    return undefined;
  }

  const normalized = value.trim();

  if (!normalized) {
    return undefined;
  }

  return normalized.slice(0, maximum);
}

export function getRequestAuditContext(
  request: Request,
): RequestAuditContext {
  const forwarded =
    request.headers.get(
      "x-forwarded-for",
    );

  const ipAddress = truncate(
    forwarded
      ?.split(",")[0]
      ?.trim() ??
      request.headers.get(
        "x-real-ip",
      ),
    128,
  );

  const userAgent = truncate(
    request.headers.get(
      "user-agent",
    ),
    512,
  );

  return {
    ipAddress,
    userAgent,
  };
}
