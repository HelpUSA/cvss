import {
  mutationErrorResponse,
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  createOrganization,
  isActivePlatformAdmin,
} from "@/lib/platform-administration";
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

export async function POST(
  request: Request,
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

    const body =
      await readJsonObject(
        request,
      );

    const result =
      await createOrganization({
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
      result,
      201,
    );
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
