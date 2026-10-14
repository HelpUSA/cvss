import {
  NextResponse,
} from "next/server";

import {
  consumeDemoRateLimit,
} from "@/lib/demo-rate-limit";
import {
  analyzeEnvironment,
} from "@/lib/environmental-analysis-service";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

function requestKey(
  request: Request,
): string {
  return (
    request.headers
      .get("x-forwarded-for")
      ?.split(",")[0]
      ?.trim() ||
    request.headers.get(
      "x-real-ip",
    ) ||
    "anonymous"
  );
}

export async function POST(
  request: Request,
) {
  try {
    const limit =
      consumeDemoRateLimit(
        requestKey(request),
      );

    if (!limit.allowed) {
      return NextResponse.json(
        {
          success: false,
          mode:
            "PUBLIC_STATELESS_DEMO",
          persisted: false,
          error:
            "Limite temporário da demonstração atingido. Tente novamente em instantes ou use o workspace autenticado.",
        },
        {
          status: 429,
          headers: {
            "Retry-After":
              String(
                Math.max(
                  1,
                  Math.ceil(
                    (
                      limit.resetAt -
                      Date.now()
                    ) / 1000,
                  ),
                ),
              ),
          },
        },
      );
    }

    const body =
      await request.json();

    const result =
      analyzeEnvironment({
        cveId: body?.cveId,
        baseVector:
          body?.baseVector,
        sourceAssessmentMeta:
          body?.sourceAssessmentMeta,
        evidence:
          body?.evidence,
      });

    return NextResponse.json(
      {
        success: true,
        mode:
          "PUBLIC_STATELESS_DEMO",
        persisted: false,
        tenantBound: false,
        disclaimer:
          "Demonstração pública sem persistência em tenant. Para histórico, governança e isolamento organizacional, use o workspace autenticado.",
        rateLimit: {
          remaining:
            limit.remaining,
          resetAt:
            new Date(
              limit.resetAt,
            ).toISOString(),
        },
        ...result,
      },
      {
        headers: {
          "Cache-Control":
            "no-store",
        },
      },
    );
  } catch (error) {
    return NextResponse.json(
      {
        success: false,
        mode:
          "PUBLIC_STATELESS_DEMO",
        persisted: false,
        error:
          error instanceof Error
            ? error.message
            : "Erro no processamento",
      },
      {
        status: 400,
      },
    );
  }
}
