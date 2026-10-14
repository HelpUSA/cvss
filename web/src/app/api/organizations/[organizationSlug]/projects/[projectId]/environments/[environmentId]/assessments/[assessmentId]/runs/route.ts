import crypto from "crypto";
import type {
  Prisma,
} from "@prisma/client";

import {
  mutationErrorResponse,
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  analyzeEnvironment,
  type EnvironmentalAssessment,
} from "@/lib/environmental-analysis-service";
import {
  jcsCanonicalize,
} from "@/lib/jcs";
import {
  resolveOrganizationContextForUser,
} from "@/lib/organization-context";
import {
  prisma,
} from "@/lib/prisma";
import {
  operationalAssessmentScopeWhere,
} from "@/lib/operational-tenant-scope";
import {
  assertJsonMutationRequest,
  getRequestAuditContext,
  readJsonObject,
} from "@/lib/request-security";
import {
  appendSecurityAuditEvent,
} from "@/lib/security-audit";
import {
  getActiveSession,
} from "@/lib/session";
import {
  normalizeId,
} from "@/lib/validation";

export const dynamic =
  "force-dynamic";
export const runtime = "nodejs";

type RouteContext = {
  params: Promise<{
    organizationSlug: string;
    projectId: string;
    environmentId: string;
    assessmentId: string;
  }>;
};

function operationalEngineCommit(): string {
  return (
    process.env
      .HELPUS_OPERATIONAL_ENGINE_COMMIT
      ?.trim() ||
    process.env
      .VERCEL_GIT_COMMIT_SHA
      ?.trim() ||
    "development-unpinned"
  );
}

function optionalString(
  value: unknown,
): string | undefined {
  if (
    typeof value !== "string"
  ) {
    return undefined;
  }

  const normalized =
    value.trim();

  return normalized ||
    undefined;
}

export async function POST(
  request: Request,
  routeContext: RouteContext,
) {
  try {
    assertJsonMutationRequest(
      request,
    );

    const currentSession =
      await getActiveSession();

    if (!currentSession) {
      return mutationNotFound();
    }

    const {
      organizationSlug,
      projectId: rawProjectId,
      environmentId:
        rawEnvironmentId,
      assessmentId:
        rawAssessmentId,
    } = await routeContext.params;

    const context =
      await resolveOrganizationContextForUser(
        {
          userId:
            currentSession.user.id,
          organizationSlug,
          permission:
            "analysis:execute",
        },
      );

    if (!context) {
      return mutationNotFound();
    }

    const projectId =
      normalizeId(
        rawProjectId,
        "projectId",
      );

    const environmentId =
      normalizeId(
        rawEnvironmentId,
        "environmentId",
      );

    const assessmentId =
      normalizeId(
        rawAssessmentId,
        "assessmentId",
      );

    const assessment =
      await prisma
        .operationalAssessment
        .findFirst({
          where:
            operationalAssessmentScopeWhere({
              organizationId:
                context.organization.id,
              projectId,
              environmentId,
              assessmentId,
            }),
          select: {
            id: true,
            vulnerabilityId:
              true,
            cve: true,
            environmentId:
              true,
          },
        });

    if (!assessment) {
      return mutationNotFound();
    }

    const body =
      await readJsonObject(
        request,
      );

    const evidence =
      body.evidence;

    if (
      !evidence ||
      typeof evidence !==
        "object" ||
      Array.isArray(evidence)
    ) {
      throw new Error(
        "evidence é obrigatório",
      );
    }

    const sourceAssessmentMeta =
      body.sourceAssessmentMeta;

    if (
      !sourceAssessmentMeta ||
      typeof sourceAssessmentMeta !==
        "object" ||
      Array.isArray(
        sourceAssessmentMeta,
      )
    ) {
      throw new Error(
        "sourceAssessmentMeta é obrigatório",
      );
    }

    const baseVector =
      optionalString(
        body.baseVector,
      );

    if (!baseVector) {
      throw new Error(
        "baseVector é obrigatório",
      );
    }

    const cveId =
      optionalString(body.cveId) ||
      assessment.cve ||
      assessment.vulnerabilityId;

    const evidenceObject =
      evidence as Record<
        string,
        unknown
      >;

    const analysis =
      analyzeEnvironment({
        cveId,
        baseVector,
        sourceAssessmentMeta:
          sourceAssessmentMeta as {
            provider: string;
            [key: string]:
              unknown;
          },
        evidence:
          evidenceObject,
      });

    const evidenceCanonical =
      jcsCanonicalize(
        evidenceObject,
      );

    const evidenceHash =
      crypto
        .createHash("sha256")
        .update(
          evidenceCanonical,
          "utf8",
        )
        .digest("hex");

    const capturedAtRaw =
      optionalString(
        body.capturedAt,
      );

    const capturedAt =
      capturedAtRaw
        ? new Date(
            capturedAtRaw,
          )
        : new Date();

    if (
      Number.isNaN(
        capturedAt.getTime(),
      )
    ) {
      throw new Error(
        "capturedAt é inválido",
      );
    }

    const expiresAtRaw =
      optionalString(
        body.expiresAt,
      );

    const expiresAt =
      expiresAtRaw
        ? new Date(
            expiresAtRaw,
          )
        : null;

    if (
      expiresAt &&
      Number.isNaN(
        expiresAt.getTime(),
      )
    ) {
      throw new Error(
        "expiresAt é inválido",
      );
    }

    const environmental =
      analysis
        .environmentalAssessment;

    const abstained =
      "status" in environmental &&
      environmental.status ===
        "ABSTAINED";

    const finalAssessment:
      EnvironmentalAssessment | null =
      abstained
        ? null
        : environmental as EnvironmentalAssessment;

    const requestAudit =
      getRequestAuditContext(
        request,
      );

    const result =
      await prisma
        .$transaction(
          async (
            transaction,
          ) => {
            const snapshot =
              await transaction
                .evidenceSnapshot
                .create({
                  data: {
                    environmentId:
                      assessment
                        .environmentId,
                    sourceType:
                      optionalString(
                        body.sourceType,
                      ) ??
                      "API_SUBMISSION",
                    sourceReference:
                      optionalString(
                        body.sourceReference,
                      ),
                    capturedAt,
                    expiresAt,
                    canonicalHash:
                      evidenceHash,
                    storageReference:
                      optionalString(
                        body.storageReference,
                      ),
                    metadata:
                      evidenceObject as Prisma.InputJsonObject,
                    createdByUserId:
                      currentSession
                        .user.id,
                  },
                });

            const run =
              await transaction
                .operationalAssessmentRun
                .create({
                  data: {
                    assessmentId:
                      assessment.id,
                    executedByUserId:
                      currentSession
                        .user.id,
                    status:
                      abstained
                        ? "ABSTAINED"
                        : "COMPLETED",
                    sourceVector:
                      analysis
                        .sourceAssessment
                        .vector,
                    sourceScore:
                      analysis
                        .sourceAssessment
                        .score,
                    finalVector:
                      finalAssessment
                        ?.vector ??
                      null,
                    finalScore:
                      finalAssessment
                        ?.score ??
                      null,
                    severity:
                      finalAssessment
                        ?.severity ??
                      null,
                    decision:
                      abstained
                        ? "abstained"
                        : finalAssessment
                            ?.decision ??
                          "unchanged",
                    abstentionReasons:
                      abstained
                        ? analysis
                            .inferenceAnalysis
                            .abstentionReasons
                        : undefined,
                    candidateMetrics:
                      analysis
                        .inferenceAnalysis
                        .candidateMetrics,
                    operationalDisposition:
                      analysis
                        .operationalDisposition as Prisma.InputJsonObject,
                    engineCommit:
                      operationalEngineCommit(),
                    ruleCatalogVersion:
                      process.env
                        .HELPUS_RULE_CATALOG_VERSION
                        ?.trim() ||
                      null,
                    ruleCatalogHash:
                      process.env
                        .HELPUS_RULE_CATALOG_HASH
                        ?.trim() ||
                      null,
                    policyId:
                      optionalString(
                        evidenceObject
                          .organizationPolicyId,
                      ) ??
                      null,
                    policyVersion:
                      optionalString(
                        evidenceObject
                          .policyVersion,
                      ) ??
                      null,
                    evidenceSnapshotId:
                      snapshot.id,
                    auditReceiptHash:
                      analysis
                        .auditReceipt
                        .receiptDigest,
                    completedAt:
                      new Date(),
                  },
                });

            await appendSecurityAuditEvent(
              transaction,
              {
                organizationId:
                  context
                    .organization.id,
                actorUserId:
                  currentSession
                    .user.id,
                action:
                  "operational_assessment.run.executed",
                targetType:
                  "OperationalAssessmentRun",
                targetId:
                  run.id,
                metadata: {
                  assessmentId:
                    assessment.id,
                  environmentId,
                  projectId,
                  evidenceSnapshotId:
                    snapshot.id,
                  runStatus:
                    run.status,
                  auditReceiptHash:
                    run
                      .auditReceiptHash,
                },
                requestContext:
                  requestAudit,
              },
            );

            return {
              snapshot,
              run,
            };
          },
          {
            isolationLevel:
              "Serializable",
          },
        );

    return mutationSuccess(
      {
        persisted: true,
        organization: {
          id: context
            .organization.id,
          slug: context
            .organization.slug,
        },
        projectId,
        environmentId,
        assessmentId:
          assessment.id,
        run: result.run,
        evidenceSnapshot: {
          id:
            result.snapshot.id,
          canonicalHash:
            result.snapshot
              .canonicalHash,
          capturedAt:
            result.snapshot
              .capturedAt,
          expiresAt:
            result.snapshot
              .expiresAt,
        },
        analysis,
      },
      201,
    );
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
