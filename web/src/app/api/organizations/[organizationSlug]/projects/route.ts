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
  createTenantProject,
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
          "project:manage",
      });

    if (!context) {
      return mutationNotFound();
    }

    const body =
      await readJsonObject(
        request,
      );

    const project =
      await createTenantProject({
        context,

        actorUserId:
          currentSession.user.id,

        name: body.name,
        slug: body.slug,

        requestContext:
          getRequestAuditContext(
            request,
          ),
      });

    return mutationSuccess(
      {
        project,
      },
      201,
    );
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
