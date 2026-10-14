import {
  OperationalAssessmentStatus,
  type Prisma,
} from "@prisma/client";

export function operationalAssessmentScopeWhere(input: {
  organizationId: string;
  projectId: string;
  environmentId: string;
  assessmentId: string;
}) {
  const where = {
    id: input.assessmentId,
    status: {
      in: [
        OperationalAssessmentStatus.DRAFT,
        OperationalAssessmentStatus.ACTIVE,
      ],
    },
    environment: {
      id: input.environmentId,
      status: "ACTIVE" as const,
      project: {
        id: input.projectId,
        status: "ACTIVE" as const,
        organizationId:
          input.organizationId,
        organization: {
          status:
            "ACTIVE" as const,
        },
      },
    },
  } satisfies Prisma.OperationalAssessmentWhereInput;

  return where;
}
