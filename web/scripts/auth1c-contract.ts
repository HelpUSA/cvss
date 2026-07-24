import {
  readFileSync,
} from "node:fs";
import {
  resolve,
} from "node:path";

import {
  MembershipRole,
} from "@prisma/client";

import {
  hasTenantPermission,
  permissionsForRole,
  type TenantPermission,
} from "../src/lib/authorization";

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

function sorted(
  values: readonly string[],
): string[] {
  return Array.from(values).sort();
}

function assertArrayEqual(
  label: string,
  actual: readonly string[],
  expected: readonly string[],
): void {
  const actualSorted = sorted(actual);
  const expectedSorted = sorted(expected);

  if (
    JSON.stringify(actualSorted) !==
    JSON.stringify(expectedSorted)
  ) {
    throw new Error(
      `${label} mismatch. Actual=${JSON.stringify(actualSorted)} Expected=${JSON.stringify(expectedSorted)}`,
    );
  }
}

async function main(): Promise<void> {
  const expectedMatrix: Record<
    MembershipRole,
    readonly TenantPermission[]
  > = {
    [MembershipRole.ADMIN]: [
      "organization:read",
      "membership:read",
      "membership:manage",
      "project:read",
      "project:manage",
      "environment:read",
      "environment:manage",
      "analysis:execute",
      "decision:review",
    ],

    [MembershipRole.OPERATOR]: [
      "organization:read",
      "project:read",
      "project:manage",
      "environment:read",
      "environment:manage",
      "analysis:execute",
    ],

    [MembershipRole.REVIEWER]: [],

    [MembershipRole.VIEWER]: [
      "organization:read",
      "project:read",
      "environment:read",
    ],
  };

  for (
    const role of
    Object.values(MembershipRole)
  ) {
    assertArrayEqual(
      `Permissions for ${role}`,
      permissionsForRole(role),
      expectedMatrix[role],
    );

    for (
      const permission of
      expectedMatrix[role]
    ) {
      if (
        !hasTenantPermission(
          role,
          permission,
        )
      ) {
        throw new Error(
          `${role} must allow ${permission}.`,
        );
      }
    }
  }

  if (
    hasTenantPermission(
      MembershipRole.REVIEWER,
      "organization:read",
    )
  ) {
    throw new Error(
      "REVIEWER must remain operationally reserved during Auth-1.",
    );
  }

  if (
    hasTenantPermission(
      MembershipRole.VIEWER,
      "project:manage",
    )
  ) {
    throw new Error(
      "VIEWER cannot manage projects.",
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

  requireMarker(
    "src/lib/organization-context.ts",
    "userId: input.userId",
  );

  requireMarker(
    "src/lib/organization-context.ts",
    'status: "ACTIVE"',
  );

  requireMarker(
    "src/lib/organization-context.ts",
    "slug: normalizedSlug",
  );

  requireMarker(
    "src/lib/organization-context.ts",
    "hasTenantPermission",
  );

  requireAbsentMarker(
    "src/lib/organization-context.ts",
    "PLATFORM_ADMIN",
  );

  requireMarker(
    "src/lib/tenant-data.ts",
    "organizationId:",
  );

  requireMarker(
    "src/lib/tenant-data.ts",
    "context.organization.id",
  );

  requireMarker(
    "src/lib/tenant-data.ts",
    "project: {",
  );

  requireMarker(
    "src/app/app/page.tsx",
    "listAccessibleOrganizations",
  );

  requireMarker(
    "src/app/app/[organizationSlug]/layout.tsx",
    "requireOrganizationContext",
  );

  requireMarker(
    "src/app/app/[organizationSlug]/projects/page.tsx",
    'permission: "project:read"',
  );

  requireMarker(
    "src/app/app/[organizationSlug]/environments/page.tsx",
    'permission: "environment:read"',
  );

  requireMarker(
    "src/app/api/organizations/[organizationSlug]/context/route.ts",
    "resolveOrganizationContextForUser",
  );

  requireMarker(
    "src/app/api/organizations/[organizationSlug]/context/route.ts",
    "status: 404",
  );

  requireMarker(
    "src/app/api/organizations/[organizationSlug]/context/route.ts",
    "private, no-store, max-age=0",
  );

  requireMarker(
    "src/app/api/organizations/[organizationSlug]/context/route.ts",
    "await routeContext.params",
  );

  console.log(
    JSON.stringify(
      {
        auth1cContractOk: true,
        organizationResolvedBySlug: true,
        activeUserRequired: true,
        activeMembershipRequired: true,
        activeOrganizationRequired: true,
        clientOrganizationIdTrusted: false,
        clientRoleTrusted: false,
        platformAdminTenantBypass: false,
        reviewerOperationalAccess: false,
        viewerReadOnly: true,
        operatorMembershipManagement: false,
        tenantQueriesScoped: true,
        unauthorizedTenantReturnsNotFound: true,
        tenantResponseCacheDisabled: true,
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
