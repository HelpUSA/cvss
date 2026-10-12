import { NextRequest, NextResponse } from "next/server";
import crypto from "crypto";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { jcsCanonicalize } from "@/lib/jcs";

export const runtime = "nodejs";

export interface ReviewDecisionRequest {
  assessmentId: string;
  decision: "APPROVED" | "REJECTED";
  rationale: string;
  organizationPolicyId: string;
  policyVersion: string;
  rulesetVersion: string;
  calculatorVersion: string;
}

export async function POST(request: NextRequest) {
  try {
    const session = await auth.api.getSession({ headers: request.headers });

    // Enforce authentication
    if (!session || !session.user) {
      return NextResponse.json(
        {
          code: "UNAUTHENTICATED",
          error: "Sessão corporativa ativa necessária para homologação humana (HITL).",
          authorization_enforced: true,
        },
        { status: 401 }
      );
    }

    // Server-side authoritative platform role verification from Prisma (Strict Fail-Closed)
    let authoritativeRole: string | null = null;
    try {
      if (session.user.id) {
        const dbUser = await prisma.user.findUnique({
          where: { id: session.user.id },
          select: { platformRole: true },
        });
        if (dbUser && dbUser.platformRole) {
          authoritativeRole = dbUser.platformRole;
        }
      }
    } catch (dbErr: any) {
      console.error("[review/decision] Database user lookup failure:", dbErr);
      return NextResponse.json(
        {
          code: "DATABASE_LOOKUP_FAILURE",
          error: "Falha na verificação autoritativa do usuário no banco de dados. Operação recusada (fail-closed).",
          authorization_enforced: true,
        },
        { status: 503 }
      );
    }

    // Enforce PLATFORM_ADMIN authorization role (strictly matches Prisma enum PlatformRole)
    if (!authoritativeRole || authoritativeRole !== "PLATFORM_ADMIN") {
      return NextResponse.json(
        {
          code: "FORBIDDEN_NOT_PLATFORM_ADMIN",
          error: "Acesso restrito. Somente contas com papel PLATFORM_ADMIN comprovado no banco podem homologar decisões.",
          authorization_enforced: true,
          currentUserRole: authoritativeRole || "UNKNOWN",
        },
        { status: 403 }
      );
    }

    const body: Partial<ReviewDecisionRequest> = await request.json();

    if (!body.assessmentId || typeof body.assessmentId !== "string" || !body.assessmentId.trim()) {
      return NextResponse.json(
        {
          code: "INVALID_ASSESSMENT_ID",
          error: "O campo 'assessmentId' é obrigatório.",
        },
        { status: 400 }
      );
    }

    if (body.decision !== "APPROVED" && body.decision !== "REJECTED") {
      return NextResponse.json(
        {
          code: "INVALID_DECISION",
          error: "O campo 'decision' deve ser estritamente 'APPROVED' ou 'REJECTED'.",
        },
        { status: 400 }
      );
    }

    if (!body.rationale || typeof body.rationale !== "string" || body.rationale.trim().length < 10) {
      return NextResponse.json(
        {
          code: "INVALID_RATIONALE",
          error: "Justificativa técnica ('rationale') obrigatória (mínimo 10 caracteres).",
        },
        { status: 400 }
      );
    }

    // Strict Fail-Safe Policy Binding: No fabricated defaults allowed
    if (!body.organizationPolicyId || typeof body.organizationPolicyId !== "string" || !body.organizationPolicyId.trim()) {
      return NextResponse.json(
        {
          code: "MISSING_POLICY_BINDING",
          error: "Vinculação de política operacional obrigatória ('organizationPolicyId' não pode ser omitido).",
        },
        { status: 400 }
      );
    }

    if (!body.policyVersion || typeof body.policyVersion !== "string" || !body.policyVersion.trim()) {
      return NextResponse.json(
        {
          code: "MISSING_POLICY_VERSION",
          error: "Versão da política obrigatória ('policyVersion' não pode ser omitida).",
        },
        { status: 400 }
      );
    }

    if (!body.rulesetVersion || typeof body.rulesetVersion !== "string" || !body.rulesetVersion.trim()) {
      return NextResponse.json(
        {
          code: "MISSING_RULESET_VERSION",
          error: "Versão do conjunto de regras obrigatória ('rulesetVersion' não pode ser omitida).",
        },
        { status: 400 }
      );
    }

    if (!body.calculatorVersion || typeof body.calculatorVersion !== "string" || !body.calculatorVersion.trim()) {
      return NextResponse.json(
        {
          code: "MISSING_CALCULATOR_VERSION",
          error: "Versão do calculador obrigatória ('calculatorVersion' não pode ser omitida).",
        },
        { status: 400 }
      );
    }

    const reviewTimestamp = new Date().toISOString();
    const reviewId = `rev_${crypto.randomUUID()}`;

    const receiptPayload = {
      schemaVersion: "1.0",
      reviewId,
      reviewedAt: reviewTimestamp,
      assessmentId: body.assessmentId.trim(),
      decision: body.decision,
      rationale: body.rationale.trim(),
      reviewer: {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name || "Platform Admin Master",
        role: authoritativeRole,
      },
      policyBinding: {
        organizationPolicyId: body.organizationPolicyId.trim(),
        policyVersion: body.policyVersion.trim(),
        rulesetVersion: body.rulesetVersion.trim(),
        calculatorVersion: body.calculatorVersion.trim(),
      },
    };

    // RFC 8785 Canonical JSON receipt and SHA-256 fingerprint
    const receiptCanonicalJcs = jcsCanonicalize(receiptPayload);
    const receiptHashSha256 = crypto
      .createHash("sha256")
      .update(receiptCanonicalJcs, "utf8")
      .digest("hex");

    // Persist durable review decision event in Prisma SecurityAuditEvent (Fail-Closed)
    try {
      await prisma.securityAuditEvent.create({
        data: {
          actorUserId: session.user.id,
          action: `HITL_REVIEW_${body.decision}`,
          targetType: "ASSESSMENT",
          targetId: body.assessmentId.trim(),
          metadata: {
            ...receiptPayload,
            receiptHashSha256,
          },
        },
      });
    } catch (persistErr: any) {
      console.error("[review/decision] SecurityAuditEvent persistence failure:", persistErr);
      return NextResponse.json(
        {
          code: "DURABLE_PERSISTENCE_FAILED",
          error: "Falha crítica na persistência durável do evento de auditoria. Recibo não emitido (fail-closed).",
        },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      decision: body.decision,
      reviewId,
      reviewedAt: reviewTimestamp,
      receiptHashSha256,
      receiptCanonicalJcs,
      receipt: receiptPayload,
    });
  } catch (error: any) {
    console.error("[review/decision] Unexpected error:", error);
    return NextResponse.json(
      {
        code: "INTERNAL_SERVER_ERROR",
        error: "Falha interna no processamento da decisão de homologação.",
      },
      { status: 500 }
    );
  }
}
