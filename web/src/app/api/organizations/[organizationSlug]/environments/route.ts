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
  createTenantEnvironment,
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
          "environment:manage",
      });

    if (!context) {
      return mutationNotFound();
    }

    const body =
      await readJsonObject(
        request,
      );

    const result =
      await createTenantEnvironment({
        context,

        actorUserId:
          currentSession.user.id,

        projectId:
          body.projectId,

        name: body.name,
        slug: body.slug,

        requestContext:
          getRequestAuditContext(
            request,
          ),
      });

    return mutationSuccess(
      result,
      201,
    );
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
