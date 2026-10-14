import {
  mutationErrorResponse,
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  resolveOrganizationContextForUser,
} from "@/lib/organization-context";
import {
  assertJsonMutationRequest,
  getRequestAuditContext,
  readJsonObject,
} from "@/lib/request-security";
import {
  getActiveSession,
} from "@/lib/session";
import {
  createTenantOperationalAssessment,
} from "@/lib/tenant-administration";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

type RouteContext = {
  params: Promise<{
    organizationSlug: string;
  }>;
};

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
    } = await routeContext.params;

    const context =
      await resolveOrganizationContextForUser({
        userId:
          currentSession.user.id,
        organizationSlug,
        permission:
          "analysis:execute",
      });

    if (!context) {
      return mutationNotFound();
    }

    const body =
      await readJsonObject(
        request,
      );

    const assessment =
      await createTenantOperationalAssessment({
        context,
        actorUserId:
          currentSession.user.id,
        environmentId:
          body.environmentId,
        vulnerabilityId:
          body.vulnerabilityId,
        cve: body.cve,
        title: body.title,
        description:
          body.description,
        requestContext:
          getRequestAuditContext(
            request,
          ),
      });

    return mutationSuccess(
      {
        assessment,
      },
      201,
    );
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
