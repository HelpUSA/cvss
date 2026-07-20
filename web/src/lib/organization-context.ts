import type {
  MembershipRole,
} from "@prisma/client";
import { notFound } from "next/navigation";

import {
  hasTenantPermission,
  type TenantPermission,
} from "@/lib/authorization";
import { prisma } from "@/lib/prisma";
import {
  requireActiveSession,
} from "@/lib/session";

export type OrganizationContext = {
  organization: {
    id: string;
    name: string;
    slug: string;
  };

  membership: {
    id: string;
    role: MembershipRole;
  };
};

export type AuthorizedOrganizationSummary = {
  organization: {
    id: string;
    name: string;
    slug: string;
  };

  membership: {
    id: string;
    role: MembershipRole;
  };
};

function normalizeOrganizationSlug(
  value: string,
): string | null {
  const normalized =
    value.trim().toLowerCase();

  if (
    !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(
      normalized,
    )
  ) {
    return null;
  }

  return normalized;
}

export async function listAccessibleOrganizations(
  userId: string,
): Promise<
  AuthorizedOrganizationSummary[]
> {
  const memberships =
    await prisma.membership.findMany({
      where: {
        userId,
        status: "ACTIVE",

        organization: {
          status: "ACTIVE",
        },
      },

      select: {
        id: true,
        role: true,

        organization: {
          select: {
            id: true,
            name: true,
            slug: true,
          },
        },
      },

      orderBy: {
        organization: {
          name: "asc",
        },
      },
    });

  return memberships
    .filter((membership) =>
      hasTenantPermission(
        membership.role,
        "organization:read",
      ),
    )
    .map((membership) => ({
      organization:
        membership.organization,

      membership: {
        id: membership.id,
        role: membership.role,
      },
    }));
}

export async function resolveOrganizationContextForUser(
  input: {
    userId: string;
    organizationSlug: string;
    permission?: TenantPermission;
  },
): Promise<OrganizationContext | null> {
  const normalizedSlug =
    normalizeOrganizationSlug(
      input.organizationSlug,
    );

  if (!normalizedSlug) {
    return null;
  }

  const permission =
    input.permission ??
    "organization:read";

  const membership =
    await prisma.membership.findFirst({
      where: {
        userId: input.userId,
        status: "ACTIVE",

        organization: {
          slug: normalizedSlug,
          status: "ACTIVE",
        },
      },

      select: {
        id: true,
        role: true,

        organization: {
          select: {
            id: true,
            name: true,
            slug: true,
          },
        },
      },
    });

  if (
    !membership ||
    !hasTenantPermission(
      membership.role,
      permission,
    )
  ) {
    return null;
  }

  return {
    organization:
      membership.organization,

    membership: {
      id: membership.id,
      role: membership.role,
    },
  };
}

export async function requireOrganizationContext(
  input: {
    organizationSlug: string;
    permission?: TenantPermission;
  },
) {
  const currentSession =
    await requireActiveSession();

  const context =
    await resolveOrganizationContextForUser({
      userId: currentSession.user.id,
      organizationSlug:
        input.organizationSlug,
      permission: input.permission,
    });

  if (!context) {
    notFound();
  }

  return {
    ...context,
    user: currentSession.user,
  };
}
