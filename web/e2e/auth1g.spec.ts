import {
  expect,
  test,
  type APIResponse,
  type Browser,
  type BrowserContext,
  type Page,
} from "@playwright/test";

const baseURL =
  process.env.AUTH1G_BASE_URL ??
  "http://127.0.0.1:3000";

const userAEmail =
  process.env.AUTH1G_USER_A_EMAIL ?? "";

const userBEmail =
  process.env.AUTH1G_USER_B_EMAIL ?? "";

const password =
  process.env.AUTH1G_PASSWORD ?? "";

function absoluteUrl(path: string): string {
  return new URL(path, baseURL).toString();
}

async function responseDescription(
  response: APIResponse,
): Promise<string> {
  return JSON.stringify(
    {
      status: response.status(),
      statusText: response.statusText(),
      body: await response.text(),
    },
    null,
    2,
  );
}

async function sessionPayload(
  context: BrowserContext,
): Promise<unknown> {
  const response =
    await context.request.get(
      absoluteUrl(
        "/api/auth/get-session",
      ),
      {
        headers: {
          Origin: baseURL,
        },
      },
    );

  const text = await response.text();

  if (!text.trim()) {
    return null;
  }

  try {
    return JSON.parse(text) as unknown;
  } catch {
    return null;
  }
}

function isRecord(
  value: unknown,
): value is Record<string, unknown> {
  return (
    value !== null &&
    typeof value === "object" &&
    !Array.isArray(value)
  );
}

function isAuthenticatedPayload(
  payload: unknown,
): boolean {
  if (!isRecord(payload)) {
    return false;
  }

  return Boolean(
    isRecord(payload.user) &&
    isRecord(payload.session),
  );
}

async function isAuthenticated(
  context: BrowserContext,
): Promise<boolean> {
  return isAuthenticatedPayload(
    await sessionPayload(context),
  );
}

async function login(
  page: Page,
  email: string,
): Promise<void> {
  await page.goto("/login", {
    waitUntil: "domcontentloaded",
  });

  const emailInput =
    page.getByLabel("E-mail");

  const passwordInput =
    page.getByLabel("Senha");

  const submitButton =
    page.getByRole(
      "button",
      {
        name: "Entrar",
      },
    );

  await expect(emailInput).toBeVisible();
  await expect(passwordInput).toBeVisible();
  await expect(submitButton).toBeVisible();

  await emailInput.fill(email);
  await passwordInput.fill(password);
  await submitButton.click();

  await expect
    .poll(
      () =>
        isAuthenticated(
          page.context(),
        ),
      {
        message:
          `Expected ${email} to have an active session.`,
      },
    )
    .toBe(true);
}

async function organizationContext(
  context: BrowserContext,
  organizationSlug: string,
): Promise<APIResponse> {
  return context.request.get(
    absoluteUrl(
      `/api/organizations/${organizationSlug}/context`,
    ),
    {
      headers: {
        Origin: baseURL,
      },
    },
  );
}

async function sessionCookies(
  context: BrowserContext,
) {
  const cookies =
    await context.cookies(baseURL);

  return cookies.filter(
    (cookie) =>
      cookie.value.length > 0 &&
      /better-auth|session/i.test(
        cookie.name,
      ),
  );
}

async function signOut(
  context: BrowserContext,
): Promise<void> {
  const response =
    await context.request.post(
      absoluteUrl(
        "/api/auth/sign-out",
      ),
      {
        data: {},
        headers: {
          Origin: baseURL,
          "Content-Type":
            "application/json",
        },
      },
    );

  expect(
    response.ok(),
    await responseDescription(response),
  ).toBeTruthy();

  await expect
    .poll(
      () =>
        isAuthenticated(context),
    )
    .toBe(false);
}

async function createContext(
  browser: Browser,
): Promise<BrowserContext> {
  return browser.newContext({
    baseURL,
  });
}

test(
  "Auth-1G validates cookies, tenant isolation and session revocation",
  async ({ browser }) => {
    expect(userAEmail).not.toBe("");
    expect(userBEmail).not.toBe("");
    expect(password).not.toBe("");

    const contextA =
      await createContext(browser);

    const contextASecondary =
      await createContext(browser);

    const contextB =
      await createContext(browser);

    const anonymousContext =
      await createContext(browser);

    try {
      const pageA =
        await contextA.newPage();

      const pageB =
        await contextB.newPage();

      await login(pageA, userAEmail);
      await login(pageB, userBEmail);

      const cookiesA =
        await sessionCookies(contextA);

      const cookiesB =
        await sessionCookies(contextB);

      expect(
        cookiesA.length,
        "User A must receive a session cookie.",
      ).toBeGreaterThan(0);

      expect(
        cookiesB.length,
        "User B must receive a session cookie.",
      ).toBeGreaterThan(0);

      expect(
        cookiesA.some(
          (cookie) => cookie.httpOnly,
        ),
        "User A session cookie must be HttpOnly.",
      ).toBe(true);

      expect(
        cookiesB.some(
          (cookie) => cookie.httpOnly,
        ),
        "User B session cookie must be HttpOnly.",
      ).toBe(true);

      expect(
        cookiesA[0]?.value,
        "Independent users must not share a session token.",
      ).not.toBe(cookiesB[0]?.value);

      const ownContextA =
        await organizationContext(
          contextA,
          "auth1g-org-a",
        );

      const foreignContextFromA =
        await organizationContext(
          contextA,
          "auth1g-org-b",
        );

      const ownContextB =
        await organizationContext(
          contextB,
          "auth1g-org-b",
        );

      const foreignContextFromB =
        await organizationContext(
          contextB,
          "auth1g-org-a",
        );

      const anonymousContextA =
        await organizationContext(
          anonymousContext,
          "auth1g-org-a",
        );

      expect(
        ownContextA.status(),
        await responseDescription(
          ownContextA,
        ),
      ).toBe(200);

      expect(
        ownContextB.status(),
        await responseDescription(
          ownContextB,
        ),
      ).toBe(200);

      expect(
        foreignContextFromA.status(),
        await responseDescription(
          foreignContextFromA,
        ),
      ).toBe(404);

      expect(
        foreignContextFromB.status(),
        await responseDescription(
          foreignContextFromB,
        ),
      ).toBe(404);

      expect(
        anonymousContextA.status(),
        await responseDescription(
          anonymousContextA,
        ),
      ).toBe(404);

      const ownPayloadA =
        (await ownContextA.json()) as {
          organization: {
            slug: string;
          };
        };

      const ownPayloadB =
        (await ownContextB.json()) as {
          organization: {
            slug: string;
          };
        };

      expect(
        ownPayloadA.organization.slug,
      ).toBe("auth1g-org-a");

      expect(
        ownPayloadB.organization.slug,
      ).toBe("auth1g-org-b");

      const secondaryPageA =
        await contextASecondary.newPage();

      await login(
        secondaryPageA,
        userAEmail,
      );

      await expect
        .poll(
          () =>
            isAuthenticated(
              contextASecondary,
            ),
        )
        .toBe(true);

      const revokeResponse =
        await contextA.request.post(
          absoluteUrl(
            "/api/account/sessions/revoke-others",
          ),
          {
            data: {},
            headers: {
              Origin: baseURL,
              "Content-Type":
                "application/json",
            },
          },
        );

      expect(
        revokeResponse.status(),
        await responseDescription(
          revokeResponse,
        ),
      ).toBe(200);

      await expect
        .poll(
          () =>
            isAuthenticated(
              contextASecondary,
            ),
          {
            message:
              "The secondary session must be revoked.",
          },
        )
        .toBe(false);

      await expect
        .poll(
          () =>
            isAuthenticated(contextA),
        )
        .toBe(true);

      await expect
        .poll(
          () =>
            isAuthenticated(contextB),
        )
        .toBe(true);

      await signOut(contextA);

      await expect
        .poll(
          () =>
            isAuthenticated(contextA),
        )
        .toBe(false);

      await expect
        .poll(
          () =>
            isAuthenticated(contextB),
        )
        .toBe(true);
    } finally {
      await anonymousContext.close();
      await contextB.close();
      await contextASecondary.close();
      await contextA.close();
    }
  },
);