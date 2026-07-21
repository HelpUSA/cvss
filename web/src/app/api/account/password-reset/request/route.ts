import {
  mutationErrorResponse,
  mutationSuccess,
} from "@/lib/api-response";
import {
  requestPasswordReset,
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

    await requestPasswordReset({
      email:
        body.email,

      requestContext:
        getRequestAuditContext(
          request,
        ),
    });

    return mutationSuccess(
      {
        accepted: true,

        message:
          "If the account is eligible, password reset instructions will be sent.",
      },
      202,
    );
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
