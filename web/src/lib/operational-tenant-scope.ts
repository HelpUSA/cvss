export function operationalAssessmentScopeWhere(input: {
  organizationId: string;
  projectId: string;
  environmentId: string;
  assessmentId: string;
}) {
  return {
    id: input.assessmentId,
    status: {
      in: [
        "DRAFT",
        "ACTIVE",
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
  };
}
