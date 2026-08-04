import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { DomainError } from "../src/lib/domain-errors";
import {
  buildPublicUrl,
  escapeHtml,
  sendTransactionalEmail,
} from "../src/lib/email-delivery";

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
  if (
    !readSource(
      relativePath,
    ).includes(marker)
  ) {
    throw new Error(
      `Required marker missing in ${relativePath}: ${marker}`,
    );
  }
}

function requireAbsentMarker(
  relativePath: string,
  marker: string,
): void {
  if (
    readSource(
      relativePath,
    ).includes(marker)
  ) {
    throw new Error(
      `Forbidden marker found in ${relativePath}: ${marker}`,
    );
  }
}

function expectDomainError(
  action: () => unknown,
  code: string,
): void {
  try {
    action();
  } catch (error) {
    if (
      error instanceof DomainError &&
      error.code === code
    ) {
      return;
    }

    throw error;
  }

  throw new Error(
    `Expected DomainError ${code}.`,
  );
}

async function expectAsyncDomainError(
  action: () => Promise<unknown>,
  code: string,
): Promise<void> {
  try {
    await action();
  } catch (error) {
    if (
      error instanceof DomainError &&
      error.code === code
    ) {
      return;
    }

    throw error;
  }

  throw new Error(
    `Expected DomainError ${code}.`,
  );
}

function validateRuntimeContract(): void {
  const nodeRoutes = [
    "src/app/api/auth/[...all]/route.ts",
    "src/app/api/account/password-reset/request/route.ts",
    "src/app/api/account/password-reset/confirm/route.ts",
    "src/app/api/account/sessions/revoke-all/route.ts",
    "src/app/api/account/sessions/revoke-others/route.ts",
    "src/app/api/invitations/accept/route.ts",
    "src/app/api/organizations/[organizationSlug]/invitations/route.ts",
  ];

  for (const route of nodeRoutes) {
    requireMarker(
      route,
      'export const runtime = "nodejs";',
    );

    requireAbsentMarker(
      route,
      'runtime = "edge"',
    );

    requireAbsentMarker(
      route,
      "runtime = 'edge'",
    );
  }

  requireMarker(
    "src/lib/auth-tokens.ts",
    'from "node:crypto"',
  );

  requireMarker(
    "src/lib/password.ts",
    'from "@node-rs/argon2"',
  );

  requireMarker(
    "src/lib/email-delivery.ts",
    "https://api.resend.com/emails",
  );
}

async function validateEmailContract(): Promise<void> {
  const names = [
    "RESEND_API_KEY",
    "AUTH_EMAIL_FROM",
    "AUTH_PUBLIC_BASE_URL",
    "BETTER_AUTH_URL",
    "NODE_ENV",
  ] as const;

  const saved =
    new Map<
      string,
      string | undefined
    >();

  const originalFetch =
    globalThis.fetch;

  for (const name of names) {
    saved.set(
      name,
      process.env[name],
    );

    delete process.env[name];
  }

  try {
    expectDomainError(
      () =>
        buildPublicUrl(
          "/reset-password",
        ),
      "public_base_url_unavailable",
    );

    process.env.NODE_ENV =
      "production";

    process.env.AUTH_PUBLIC_BASE_URL =
      "http://cvss.example.invalid";

    expectDomainError(
      () =>
        buildPublicUrl(
          "/reset-password",
        ),
      "insecure_public_base_url",
    );

    process.env.AUTH_PUBLIC_BASE_URL =
      "https://cvss.example.invalid";

    if (
      buildPublicUrl(
        "/reset-password?token=contract",
      ) !==
      "https://cvss.example.invalid/reset-password?token=contract"
    ) {
      throw new Error(
        "Public URL contract failed.",
      );
    }

    if (
      escapeHtml(
        `<a href="'&">`,
      ) !==
      "&lt;a href=&quot;&#039;&amp;&quot;&gt;"
    ) {
      throw new Error(
        "HTML escaping contract failed.",
      );
    }

    process.env.AUTH_EMAIL_FROM =
      "CVSS Sandbox <sandbox@example.invalid>";

    await expectAsyncDomainError(
      () =>
        sendTransactionalEmail({
          to:
            "recipient@example.invalid",

          subject:
            "Auth-1H missing key",

          text:
            "contract",

          html:
            "<p>contract</p>",

          idempotencyKey:
            "auth1h-missing-key",
        }),
      "email_delivery_unavailable",
    );

    process.env.RESEND_API_KEY =
      "auth1h-contract-key";

    let capturedUrl = "";

    let capturedInit:
      RequestInit | undefined;

    globalThis.fetch =
      (async (
        input,
        init,
      ): Promise<Response> => {
        capturedUrl =
          input instanceof Request
            ? input.url
            : String(input);

        capturedInit =
          init;

        return new Response(
          JSON.stringify({
            id:
              "auth1h-contract-message",
          }),
          {
            status: 200,

            headers: {
              "Content-Type":
                "application/json",
            },
          },
        );
      }) as typeof fetch;

    const result =
      await sendTransactionalEmail({
        to:
          "recipient@example.invalid",

        subject:
          "Auth-1H contract",

        text:
          "contract text",

        html:
          "<p>contract html</p>",

        idempotencyKey:
          "auth1h-contract-idempotency",
      });

    const headers =
      new Headers(
        capturedInit?.headers,
      );

    const body =
      JSON.parse(
        String(
          capturedInit?.body,
        ),
      ) as {
        from?: unknown;
        to?: unknown;
      };

    if (
      result.providerMessageId !==
        "auth1h-contract-message" ||
      capturedUrl !==
        "https://api.resend.com/emails" ||
      capturedInit?.method !==
        "POST" ||
      headers.get(
        "Authorization",
      ) !==
        "Bearer auth1h-contract-key" ||
      headers.get(
        "Idempotency-Key",
      ) !==
        "auth1h-contract-idempotency" ||
      body.from !==
        "CVSS Sandbox <sandbox@example.invalid>" ||
      !Array.isArray(
        body.to,
      ) ||
      body.to[0] !==
        "recipient@example.invalid"
    ) {
      throw new Error(
        "Resend request contract failed.",
      );
    }

    globalThis.fetch =
      (async (): Promise<Response> =>
        new Response(
          JSON.stringify({
            message:
              "provider failure",
          }),
          {
            status: 500,

            headers: {
              "Content-Type":
                "application/json",
            },
          },
        )) as typeof fetch;

    await expectAsyncDomainError(
      () =>
        sendTransactionalEmail({
          to:
            "recipient@example.invalid",

          subject:
            "Auth-1H provider failure",

          text:
            "failure",

          html:
            "<p>failure</p>",

          idempotencyKey:
            "auth1h-provider-failure",
        }),
      "email_delivery_failed",
    );
  }
  finally {
    globalThis.fetch =
      originalFetch;

    for (const name of names) {
      const value =
        saved.get(name);

      if (value === undefined) {
        delete process.env[name];
      }
      else {
        process.env[name] =
          value;
      }
    }
  }
}

function requiredEnvironment(
  name: string,
): string {
  const value =
    process.env[name]?.trim();

  if (!value) {
    throw new Error(
      `Required environment missing: ${name}`,
    );
  }

  return value;
}

async function sendControlledSandboxEmail(): Promise<void> {
  const recipient =
    requiredEnvironment(
      "AUTH1H_EMAIL_TEST_TO",
    );

  const idempotencyKey =
    requiredEnvironment(
      "AUTH1H_SANDBOX_IDEMPOTENCY_KEY",
    );

  const context =
    process.env.AUTH1H_SANDBOX_CONTEXT
      ?.trim() ??
    "controlled";

  if (
    !recipient.includes("@") ||
    recipient.length > 320
  ) {
    throw new Error(
      "Controlled recipient is invalid.",
    );
  }

  const publicUrl =
    buildPublicUrl(
      "/auth1h-email-sandbox",
    );

  if (
    new URL(
      publicUrl,
    ).protocol !== "https:"
  ) {
    throw new Error(
      "Sandbox public URL must use HTTPS.",
    );
  }

  await sendTransactionalEmail({
    to:
      recipient,

    subject:
      "CVSS Auth-1H controlled sandbox",

    text:
      "Controlled CVSS Auth-1H email.\n" +
      `Context: ${context}\n`,

    html:
      "<p>Controlled CVSS Auth-1H email.</p>" +
      `<p>Context: ${escapeHtml(context)}</p>`,

    idempotencyKey,
  });
}

async function main(): Promise<void> {
  validateRuntimeContract();

  const mode =
    process.env.AUTH1H_MODE ??
    "contract";

  if (mode === "contract") {
    await validateEmailContract();

    console.log(
      JSON.stringify(
        {
          auth1hOperationalContractOk:
            true,

          runtime:
            "nodejs",

          externalEmailSent:
            false,

          fetchMocked:
            true,

          provider:
            "Resend",
        },
        null,
        2,
      ),
    );

    return;
  }

  if (mode === "sandbox") {
    await sendControlledSandboxEmail();

    console.log(
      JSON.stringify(
        {
          auth1hEmailSandboxOk:
            true,

          emailCount:
            1,

          recipientFromProtectedEnvironment:
            true,
        },
        null,
        2,
      ),
    );

    return;
  }

  throw new Error(
    `Unsupported AUTH1H_MODE: ${mode}`,
  );
}

main().catch(
  (
    error:
      unknown,
  ) => {
    console.error(
      error instanceof Error
        ? error.message
        : String(error),
    );

    process.exitCode =
      1;
  },
);