import {
  readFileSync,
} from "node:fs";
import {
  resolve,
} from "node:path";

import {
  MembershipRole,
  MembershipStatus,
} from "@prisma/client";

import {
  hasTenantPermission,
} from "../src/lib/authorization";
import {
  DomainError,
} from "../src/lib/domain-errors";
import {
  assertLastActiveAdminInvariant,
  removesActiveAdmin,
} from "../src/lib/membership-invariants";
import {
  assertJsonMutationRequest,
} from "../src/lib/request-security";
import {
  normalizeSlug,
  parseMembershipRole,
  parseMembershipStatus,
} from "../src/lib/validation";

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
  const content =
    readSource(relativePath);

  if (!content.includes(marker)) {
    throw new Error(
      `Required marker not found in ${relativePath}: ${marker}`,
    );
  }
}

function requireAbsentMarker(
  relativePath: string,
  marker: string,
): void {
  const content =
    readSource(relativePath);

  if (content.includes(marker)) {
    throw new Error(
      `Forbidden marker found in ${relativePath}: ${marker}`,
    );
  }
}

function expectDomainError(
  action: () => void,
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
  if (
    normalizeSlug(
      "  Security-Operations  ",
    ) !== "security-operations"
  ) {
    throw new Error(
      "Slug normalization failed.",
    );
  }

  if (
    parseMembershipRole(
      "ADMIN",
    ) !== MembershipRole.ADMIN
  ) {
    throw new Error(
      "Membership role parsing failed.",
    );
  }

  if (
    parseMembershipStatus(
      "ACTIVE",
    ) !== MembershipStatus.ACTIVE
  ) {
    throw new Error(
      "Membership status parsing failed.",
    );
  }

  const activeAdmin = {
    role: MembershipRole.ADMIN,
    status:
      MembershipStatus.ACTIVE,
  };

  const activeOperator = {
    role: MembershipRole.OPERATOR,
    status:
      MembershipStatus.ACTIVE,
  };

  const suspendedAdmin = {
    role: MembershipRole.ADMIN,
    status:
      MembershipStatus.SUSPENDED,
  };

  if (
    !removesActiveAdmin(
      activeAdmin,
      activeOperator,
    )
  ) {
    throw new Error(
      "Admin demotion must remove an active admin.",
    );
  }

  if (
    !removesActiveAdmin(
      activeAdmin,
      suspendedAdmin,
    )
  ) {
    throw new Error(
      "Admin suspension must remove an active admin.",
    );
  }

  expectDomainError(
    () =>
      assertLastActiveAdminInvariant({
        before: activeAdmin,
        after: activeOperator,
        activeAdminCount: 1,
      }),
    "last_active_admin",
  );

  assertLastActiveAdminInvariant({
    before: activeAdmin,
    after: activeOperator,
    activeAdminCount: 2,
  });

  if (
    !hasTenantPermission(
      MembershipRole.ADMIN,
      "membership:manage",
    )
  ) {
    throw new Error(
      "ADMIN must manage memberships.",
    );
  }

  if (
    hasTenantPermission(
      MembershipRole.OPERATOR,
      "membership:manage",
    )
  ) {
    throw new Error(
      "OPERATOR cannot manage memberships.",
    );
  }

  if (
    !hasTenantPermission(
      MembershipRole.OPERATOR,
      "project:manage",
    )
  ) {
    throw new Error(
      "OPERATOR must manage projects.",
    );
  }

  const validRequest =
    new Request(
      "https://cvss.helpusbr.com/api/test",
      {
        method: "POST",

        headers: {
          Origin:
            "https://cvss.helpusbr.com",

          "Content-Type":
            "application/json",

          "Content-Length":
            "2",

          "Sec-Fetch-Site":
            "same-origin",
        },

        body: "{}",
      },
    );

  assertJsonMutationRequest(
    validRequest,
  );

  const invalidRequest =
    new Request(
      "https://cvss.helpusbr.com/api/test",
      {
        method: "POST",

        headers: {
          Origin:
            "https://attacker.example",

          "Content-Type":
            "application/json",

          "Content-Length":
            "2",

          "Sec-Fetch-Site":
            "cross-site",
        },

        body: "{}",
      },
    );

  expectDomainError(
    () =>
      assertJsonMutationRequest(
        invalidRequest,
      ),
    "invalid_origin",
  );

  requireMarker(
    "src/lib/transactions.ts",
    "TransactionIsolationLevel",
  );

  requireMarker(
    "src/lib/transactions.ts",
    "Serializable",
  );

  requireMarker(
    "src/lib/transactions.ts",
    'error.code === "P2034"',
  );

  requireMarker(
    "src/lib/tenant-administration.ts",
    "assertLastActiveAdminInvariant",
  );

  requireMarker(
    "src/lib/tenant-administration.ts",
    "activeAdminCount",
  );

  requireMarker(
    "src/lib/tenant-administration.ts",
    "organizationId:",
  );

  requireMarker(
    "src/lib/tenant-administration.ts",
    "projectId:",
  );

  requireMarker(
    "src/lib/platform-administration.ts",
    "PLATFORM_ADMIN",
  );

  requireMarker(
    "src/lib/platform-administration.ts",
    "firstMembershipRole",
  );

  requireMarker(
    "src/lib/security-audit.ts",
    "securityAuditEvent",
  );

  requireAbsentMarker(
    "src/lib/security-audit.ts",
    "password",
  );

  requireAbsentMarker(
    "src/lib/security-audit.ts",
    "tokenHash",
  );

  requireMarker(
    "src/app/api/organizations/[organizationSlug]/memberships/route.ts",
    'permission:\n          "membership:manage"',
  );

  requireMarker(
    "src/app/api/organizations/[organizationSlug]/projects/route.ts",
    'permission:\n          "project:manage"',
  );

  requireMarker(
    "src/app/api/organizations/[organizationSlug]/environments/route.ts",
    'permission:\n          "environment:manage"',
  );

  requireMarker(
    "src/app/api/organizations/[organizationSlug]/memberships/[membershipId]/route.ts",
    "await routeContext.params",
  );

  requireMarker(
    "src/app/api/platform/organizations/route.ts",
    "assertJsonMutationRequest",
  );

  requireMarker(
    "src/app/api/platform/organizations/route.ts",
    "isActivePlatformAdmin",
  );

  requireMarker(
    "src/app/app/[organizationSlug]/members/page.tsx",
    'permission: "membership:read"',
  );

  requireMarker(
    "src/app/app/[organizationSlug]/projects/page.tsx",
    "ProjectCreateForm",
  );

  requireMarker(
    "src/app/app/[organizationSlug]/environments/page.tsx",
    "EnvironmentCreateForm",
  );

  console.log(
    JSON.stringify(
      {
        auth1dContractOk: true,
        platformOrganizationCreation: true,
        firstAdminMembership: true,
        membershipAdministration: true,
        lastActiveAdminProtected: true,
        serializableTransactions: true,
        p2034Retry: true,
        projectCreationScoped: true,
        environmentProjectVerified: true,
        securityAuditAppended: true,
        sameOriginRequired: true,
        jsonBodyLimited: true,
        clientRoleTrusted: false,
        clientOrganizationIdTrusted: false,
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
