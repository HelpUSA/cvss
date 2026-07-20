import type {
  OrganizationContext,
} from "@/lib/organization-context";
import { prisma } from "@/lib/prisma";

export async function getTenantOverview(
  context: OrganizationContext,
) {
  const [
    activeProjects,
    activeEnvironments,
    activeMembers,
  ] = await prisma.$transaction([
    prisma.project.count({
      where: {
        organizationId:
          context.organization.id,
        status: "ACTIVE",
      },
    }),

    prisma.environment.count({
      where: {
        status: "ACTIVE",

        project: {
          organizationId:
            context.organization.id,
          status: "ACTIVE",
        },
      },
    }),

    prisma.membership.count({
      where: {
        organizationId:
          context.organization.id,
        status: "ACTIVE",
      },
    }),
  ]);

  return {
    activeProjects,
    activeEnvironments,
    activeMembers,
  };
}

export async function listTenantProjects(
  context: OrganizationContext,
) {
  return prisma.project.findMany({
    where: {
      organizationId:
        context.organization.id,
      status: "ACTIVE",
    },

    select: {
      id: true,
      name: true,
      slug: true,
      status: true,
      createdAt: true,

      _count: {
        select: {
          environments: true,
        },
      },
    },

    orderBy: [
      {
        name: "asc",
      },
      {
        id: "asc",
      },
    ],
  });
}

export async function listTenantEnvironments(
  context: OrganizationContext,
) {
  return prisma.environment.findMany({
    where: {
      status: "ACTIVE",

      project: {
        organizationId:
          context.organization.id,
        status: "ACTIVE",
      },
    },

    select: {
      id: true,
      name: true,
      slug: true,
      status: true,
      createdAt: true,

      project: {
        select: {
          id: true,
          name: true,
          slug: true,
        },
      },
    },

    orderBy: [
      {
        project: {
          name: "asc",
        },
      },
      {
        name: "asc",
      },
      {
        id: "asc",
      },
    ],
  });
}
