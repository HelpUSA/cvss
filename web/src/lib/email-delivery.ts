import { DomainError } from "@/lib/domain-errors";

type TransactionalEmailInput = {
  to: string;
  subject: string;
  text: string;
  html: string;
  idempotencyKey: string;
};

type ResendResponse = {
  id?: unknown;
};

function requiredEnvironment(
  name: string,
): string {
  const value =
    process.env[name]?.trim();

  if (!value) {
    throw new DomainError({
      code:
        "email_delivery_unavailable",

      message:
        "Transactional email delivery is not configured.",

      status: 503,
    });
  }

  return value;
}

export function escapeHtml(
  value: string,
): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export function buildPublicUrl(
  path: string,
): string {
  const configuredBase =
    process.env.AUTH_PUBLIC_BASE_URL
      ?.trim() ??
    process.env.BETTER_AUTH_URL
      ?.trim();

  if (!configuredBase) {
    throw new DomainError({
      code:
        "public_base_url_unavailable",

      message:
        "The public authentication URL is not configured.",

      status: 503,
    });
  }

  const base = new URL(
    configuredBase,
  );

  const isLocal =
    base.hostname === "localhost" ||
    base.hostname === "127.0.0.1";

  if (
    process.env.NODE_ENV ===
      "production" &&
    base.protocol !== "https:" &&
    !isLocal
  ) {
    throw new DomainError({
      code:
        "insecure_public_base_url",

      message:
        "The public authentication URL must use HTTPS.",

      status: 503,
    });
  }

  return new URL(
    path,
    base,
  ).toString();
}

export async function sendTransactionalEmail(
  input: TransactionalEmailInput,
): Promise<{
  providerMessageId: string;
}> {
  const apiKey =
    requiredEnvironment(
      "RESEND_API_KEY",
    );

  const from =
    requiredEnvironment(
      "AUTH_EMAIL_FROM",
    );

  const response = await fetch(
    "https://api.resend.com/emails",
    {
      method: "POST",

      headers: {
        Authorization:
          `Bearer ${apiKey}`,

        "Content-Type":
          "application/json",

        "Idempotency-Key":
          input.idempotencyKey,
      },

      body: JSON.stringify({
        from,
        to: [input.to],
        subject: input.subject,
        text: input.text,
        html: input.html,
      }),
    },
  );

  const payload: ResendResponse | null =
    await response
      .json()
      .catch(() => null);

  if (
    !response.ok ||
    typeof payload?.id !== "string"
  ) {
    throw new DomainError({
      code:
        "email_delivery_failed",

      message:
        "Transactional email delivery failed.",

      status: 503,
    });
  }

  return {
    providerMessageId:
      payload.id,
  };
}
