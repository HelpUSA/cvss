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
    activeAssessments,
    completedRuns,
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

    prisma.operationalAssessment.count({
      where: {
        status: {
          in: ["DRAFT", "ACTIVE"],
        },
        environment: {
          project: {
            organizationId:
              context.organization.id,
            status: "ACTIVE",
          },
          status: "ACTIVE",
        },
      },
    }),

    prisma.operationalAssessmentRun.count({
      where: {
        assessment: {
          environment: {
            project: {
              organizationId:
                context.organization.id,
            },
          },
        },
      },
    }),
  ]);

  return {
    activeProjects,
    activeEnvironments,
    activeMembers,
    activeAssessments,
    completedRuns,
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

export async function listTenantMemberships(
  context: OrganizationContext,
) {
  return prisma.membership.findMany({
    where: {
      organizationId:
        context.organization.id,
    },

    select: {
      id: true,
      role: true,
      status: true,
      createdAt: true,
      suspendedAt: true,
      revokedAt: true,

      user: {
        select: {
          id: true,
          name: true,
          email: true,
          status: true,
        },
      },
    },

    orderBy: [
      {
        role: "asc",
      },
      {
        createdAt: "asc",
      },
      {
        id: "asc",
      },
    ],
  });
}


export async function listTenantOperationalAssessments(
  context: OrganizationContext,
) {
  return prisma.operationalAssessment.findMany({
    where: {
      status: {
        in: ["DRAFT", "ACTIVE"],
      },
      environment: {
        status: "ACTIVE",
        project: {
          organizationId:
            context.organization.id,
          status: "ACTIVE",
        },
      },
    },
    select: {
      id: true,
      vulnerabilityId: true,
      cve: true,
      title: true,
      description: true,
      status: true,
      createdAt: true,
      environment: {
        select: {
          id: true,
          name: true,
          slug: true,
          project: {
            select: {
              id: true,
              name: true,
              slug: true,
            },
          },
        },
      },
      _count: {
        select: {
          runs: true,
        },
      },
    },
    orderBy: [
      {
        createdAt: "desc",
      },
      {
        id: "asc",
      },
    ],
  });
}

export async function getTenantOperationalAssessment(
  context: OrganizationContext,
  assessmentId: string,
) {
  return prisma.operationalAssessment.findFirst({
    where: {
      id: assessmentId,
      status: {
        in: ["DRAFT", "ACTIVE"],
      },
      environment: {
        status: "ACTIVE",
        project: {
          organizationId:
            context.organization.id,
          status: "ACTIVE",
        },
      },
    },
    select: {
      id: true,
      vulnerabilityId: true,
      cve: true,
      title: true,
      description: true,
      status: true,
      createdAt: true,
      environment: {
        select: {
          id: true,
          name: true,
          slug: true,
          project: {
            select: {
              id: true,
              name: true,
              slug: true,
            },
          },
        },
      },
      runs: {
        select: {
          id: true,
          status: true,
          sourceVector: true,
          sourceScore: true,
          finalVector: true,
          finalScore: true,
          severity: true,
          decision: true,
          auditReceiptHash: true,
          createdAt: true,
          completedAt: true,
        },
        orderBy: {
          createdAt: "desc",
        },
        take: 20,
      },
    },
  });
}

export async function getTenantOperationalRun(
  context: OrganizationContext,
  assessmentId: string,
  runId: string,
) {
  return prisma.operationalAssessmentRun.findFirst({
    where: {
      id: runId,
      assessmentId,
      assessment: {
        environment: {
          project: {
            organizationId:
              context.organization.id,
          },
        },
      },
    },
    select: {
      id: true,
      status: true,
      sourceVector: true,
      sourceScore: true,
      finalVector: true,
      finalScore: true,
      severity: true,
      decision: true,
      abstentionReasons: true,
      candidateMetrics: true,
      operationalDisposition: true,
      engineCommit: true,
      ruleCatalogVersion: true,
      ruleCatalogHash: true,
      policyId: true,
      policyVersion: true,
      auditReceiptHash: true,
      startedAt: true,
      completedAt: true,
      createdAt: true,
      evidenceSnapshot: {
        select: {
          id: true,
          sourceType: true,
          sourceReference: true,
          capturedAt: true,
          expiresAt: true,
          canonicalHash: true,
        },
      },
      assessment: {
        select: {
          id: true,
          title: true,
          vulnerabilityId: true,
          cve: true,
          environment: {
            select: {
              id: true,
              name: true,
              project: {
                select: {
                  id: true,
                  name: true,
                },
              },
            },
          },
        },
      },
    },
  });
}


export async function listTenantEvidenceSnapshots(
  context: OrganizationContext,
) {
  return prisma.evidenceSnapshot.findMany({
    where: {
      environment: {
        project: {
          organizationId:
            context.organization.id,
        },
      },
    },
    select: {
      id: true,
      sourceType: true,
      sourceReference: true,
      capturedAt: true,
      expiresAt: true,
      canonicalHash: true,
      storageReference: true,
      createdAt: true,
      environment: {
        select: {
          id: true,
          name: true,
          slug: true,
          project: {
            select: {
              id: true,
              name: true,
              slug: true,
            },
          },
        },
      },
      _count: {
        select: {
          runs: true,
        },
      },
    },
    orderBy: [
      { capturedAt: "desc" },
      { id: "desc" },
    ],
    take: 200,
  });
}
