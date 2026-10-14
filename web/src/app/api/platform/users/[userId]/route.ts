import {
  mutationErrorResponse,
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  isActivePlatformAdmin,
} from "@/lib/platform-administration";
import {
  updatePlatformUser,
} from "@/lib/platform-user-administration";
import {
  assertJsonMutationRequest,
  getRequestAuditContext,
  readJsonObject,
} from "@/lib/request-security";
import {
  getActiveSession,
} from "@/lib/session";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

type RouteContext = {
  params: Promise<{
    userId: string;
  }>;
};

export async function PATCH(
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

    const permitted =
      await isActivePlatformAdmin(
        currentSession.user.id,
      );

    if (!permitted) {
      return mutationNotFound();
    }

    const {
      userId,
    } = await routeContext.params;

    const body =
      await readJsonObject(
        request,
      );

    const user =
      await updatePlatformUser({
        actorUserId:
          currentSession.user.id,
        targetUserId: userId,
        status: body.status,
        platformRole:
          body.platformRole,
        requestContext:
          getRequestAuditContext(
            request,
          ),
      });

    return mutationSuccess({
      user,
    });
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
