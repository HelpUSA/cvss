import { NextRequest, NextResponse } from "next/server";
import { headers } from "next/headers";
import crypto from "crypto";
import { auth } from "@/lib/auth";
import { jcsCanonicalize } from "@/lib/jcs";

export const runtime = "nodejs";

export interface ReviewDecisionRequest {
  assessmentId: string;
  decision: "APPROVED" | "REJECTED";
  rationale: string;
  organizationPolicyId?: string;
  policyVersion?: string;
  rulesetVersion?: string;
  calculatorVersion?: string;
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

    // Enforce SuperAdmin authorization role
    const userRole = (session.user as any).platformRole || (session.user as any).role || "USER";
    if (userRole !== "SUPERADMIN") {
      return NextResponse.json(
        {
          code: "FORBIDDEN_NOT_SUPERADMIN",
          error: "Acesso restrito. Somente contas com papel SuperAdmin Master podem homologar decisões.",
          authorization_enforced: true,
          currentUserRole: userRole,
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
        name: session.user.name || "SuperAdmin Master",
        role: userRole,
      },
      policyBinding: {
        organizationPolicyId: body.organizationPolicyId || "helpus-operational-pci-segmented",
        policyVersion: body.policyVersion || "1.0.0",
        rulesetVersion: body.rulesetVersion || "1.0.0",
        calculatorVersion: body.calculatorVersion || "0.2.0-aligned-first-cvss40",
      },
    };

    const canonicalReceipt = jcsCanonicalize(receiptPayload);
    const receiptHash = crypto.createHash("sha256").update(canonicalReceipt, "utf8").digest("hex");

    return NextResponse.json(
      {
        success: true,
        reviewId,
        decision: body.decision,
        reviewedAt: reviewTimestamp,
        authorization_enforced: true,
        receipt: receiptPayload,
        receiptCanonicalJcs: canonicalReceipt,
        receiptSha256: receiptHash,
      },
      { status: 200 }
    );
  } catch (err: any) {
    return NextResponse.json(
      {
        code: "INTERNAL_ERROR",
        error: err?.message || "Erro interno no processamento da decisão de homologação.",
      },
      { status: 500 }
    );
  }
}
