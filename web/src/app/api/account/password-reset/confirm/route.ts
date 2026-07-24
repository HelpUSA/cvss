import {
  mutationErrorResponse,
  mutationSuccess,
} from "@/lib/api-response";
import {
  confirmPasswordReset,
} from "@/lib/account-lifecycle";
import {
  assertJsonMutationRequest,
  getRequestAuditContext,
  readJsonObject,
} from "@/lib/request-security";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function POST(
  request: Request,
) {
  try {
    assertJsonMutationRequest(
      request,
    );

    const body =
      await readJsonObject(
        request,
      );

    const result =
      await confirmPasswordReset({
        token:
          body.token,

        password:
          body.password,

        requestContext:
          getRequestAuditContext(
            request,
          ),
      });

    return mutationSuccess({
      completed: true,
      sessionsRevoked:
        result.sessionsRevoked,
    });
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
