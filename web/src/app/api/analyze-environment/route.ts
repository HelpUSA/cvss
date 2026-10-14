import { NextResponse } from "next/server";
import { fromVector } from "ae-cvss-calculator";
import crypto from "crypto";
import { jcsCanonicalize } from "@/lib/jcs";

function getSeverity(cvssScore: number): string {
  if (cvssScore >= 9.0) return "Critical";
  if (cvssScore >= 7.0) return "High";
  if (cvssScore >= 4.0) return "Medium";
  if (cvssScore > 0.0) return "Low";
  return "None";
}

type OperationalBand = {
  code: "P0_IMMEDIATE" | "P1_EXPEDITED" | "P2_SCHEDULED" | "P3_MONITOR" | "P4_DEFER_RECOMMENDED";
  label: string;
  minScore: number;
  maxScore: number;
  caveat?: string;
};

type OperationalPolicy = {
  policyId: string;
  policyVersion: string;
  scoreBands: OperationalBand[];
};

function resolveOperationalDisposition(score: number | null, decision: string, evidence: any) {
  if (score === null || decision === "abstained") {
    return {
      code: "PENDING_HUMAN_REVIEW",
      label: "Revisão Humana Obrigatória",
      caveat: "Inferência em abstenção segura; nenhuma disposição operacional foi aprovada.",
      policyApplied: false,
    };
  }

  const policy = evidence?.operationalPolicy as OperationalPolicy | undefined;
  if (!policy || !policy.policyId || !policy.policyVersion || !Array.isArray(policy.scoreBands)) {
    return {
      code: "PENDING_POLICY_REVIEW",
      label: "Política Operacional Necessária",
      caveat: "O CVSS-BE foi calculado, mas P0-P4 não é derivado diretamente do score sem uma política organizacional explícita e versionada.",
      policyApplied: false,
    };
  }

  if (evidence.organizationPolicyId && evidence.organizationPolicyId !== policy.policyId) {
    return {
      code: "PENDING_POLICY_REVIEW",
      label: "Política Operacional Inconsistente",
      caveat: "operationalPolicy.policyId difere de organizationPolicyId.",
      policyApplied: false,
    };
  }
  if (evidence.policyVersion && evidence.policyVersion !== policy.policyVersion) {
    return {
      code: "PENDING_POLICY_REVIEW",
      label: "Versão de Política Inconsistente",
      caveat: "operationalPolicy.policyVersion difere de policyVersion.",
      policyApplied: false,
    };
  }

  const allowed = new Set(["P0_IMMEDIATE", "P1_EXPEDITED", "P2_SCHEDULED", "P3_MONITOR", "P4_DEFER_RECOMMENDED"]);
  const validBands = policy.scoreBands.filter((band) =>
    allowed.has(band.code) &&
    Number.isFinite(band.minScore) &&
    Number.isFinite(band.maxScore) &&
    band.minScore >= 0 &&
    band.maxScore <= 10 &&
    band.minScore <= band.maxScore
  );

  const matches = validBands.filter((band) => score >= band.minScore && score <= band.maxScore);
  if (matches.length !== 1) {
    return {
      code: "PENDING_POLICY_REVIEW",
      label: "Política Operacional Ambígua",
      caveat: `O score ${score.toFixed(1)} deve corresponder a exatamente uma banda operacional; correspondências encontradas: ${matches.length}.`,
      policyApplied: false,
    };
  }

  const band = matches[0];
  return {
    code: band.code,
    label: band.label,
    caveat: band.caveat ?? "Recomendação local sujeita a aprovação humana.",
    policyApplied: true,
    policyId: policy.policyId,
    policyVersion: policy.policyVersion,
  };
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { cveId, baseVector, sourceAssessmentMeta, evidence } = body ?? {};

    if (!cveId || typeof cveId !== "string") {
      return NextResponse.json({ success: false, error: "cveId é obrigatório" }, { status: 400 });
    }
    if (!baseVector || typeof baseVector !== "string" || !baseVector.startsWith("CVSS:4.0/")) {
      return NextResponse.json({ success: false, error: "baseVector CVSS:4.0 é obrigatório" }, { status: 400 });
    }
    if (!evidence || typeof evidence !== "object") {
      return NextResponse.json({ success: false, error: "evidence é obrigatório; presets de demonstração devem ser enviados explicitamente" }, { status: 400 });
    }
    if (!sourceAssessmentMeta || typeof sourceAssessmentMeta !== "object" || !sourceAssessmentMeta.provider) {
      return NextResponse.json({ success: false, error: "sourceAssessmentMeta.provider é obrigatório para provenance" }, { status: 400 });
    }

    const sourceCalculator = fromVector(baseVector);
    const sourceScore = sourceCalculator.calculateOverallScore();
    const sourceSeverity = getSeverity(sourceScore);
    const sourceNomenclature = sourceCalculator.getNomenclature();

    const citations: string[] = [];
    const reasons: string[] = [];
    const candidateMetrics: Record<string, string> = {};

    const quality = String(evidence.evidenceQuality ?? "UNKNOWN").toUpperCase();
    const telemetryAge = typeof evidence.telemetryAgeDays === "number" ? evidence.telemetryAgeDays : null;
    const maxAge = typeof evidence.maxTelemetryAgeDays === "number"
      ? evidence.maxTelemetryAgeDays
      : evidence.telemetryProfile === "static" ? 7.0 : 1.0;

    if (telemetryAge === null) reasons.push("Idade da telemetria ausente");
    else if (telemetryAge > maxAge) reasons.push(`Telemetria obsoleta (${telemetryAge} dias; limite ${maxAge} dias)`);

    if (["UNKNOWN", "INSUFFICIENT", "CONFLICTING"].includes(quality)) reasons.push(`Qualidade da evidência não suficiente (${quality})`);
    if (evidence.conflictFlag === true) reasons.push("Conflito explícito de evidência");

    const reachability = String(evidence.reachability ?? "UNKNOWN").toUpperCase();
    if (reachability === "PUBLIC_ROUTED" || reachability === "INTERNAL_ROUTED") {
      candidateMetrics.MAV = "N";
      citations.push(`MAV:N - reachability ${reachability}`);
    } else if (reachability === "ADJACENT_ONLY") {
      candidateMetrics.MAV = "A";
      citations.push("MAV:A - adjacência explicitamente evidenciada");
    } else if (reachability === "LOCAL_ONLY") {
      candidateMetrics.MAV = "L";
      citations.push("MAV:L - exploração restrita a contexto local");
    } else if (reachability === "PHYSICAL_ONLY") {
      candidateMetrics.MAV = "P";
      citations.push("MAV:P - interação física requerida");
    } else {
      reasons.push("Classe de reachability ausente ou indeterminada");
    }

    if (evidence.firewallActive) citations.push("Firewall/WAF registrado como evidência; MAC não foi alterado por essa condição isoladamente.");
    if (evidence.evidencedExploitPreconditionsElevated === true) {
      candidateMetrics.MAC = "H";
      citations.push("MAC:H - precondições específicas de exploração evidenciadas");
    }

    // CR/IR/AR are accepted only as values already resolved by an explicit versioned policy.
    const reqs = evidence.securityRequirements;
    if (reqs) {
      if (!evidence.organizationPolicyId || !evidence.policyVersion) {
        reasons.push("securityRequirements fornecido sem organizationPolicyId/policyVersion");
      } else {
        for (const key of ["CR", "IR", "AR"]) {
          const val = reqs[key];
          if (val && ["H", "M", "L"].includes(String(val).toUpperCase())) candidateMetrics[key] = String(val).toUpperCase();
        }
        citations.push(`CR/IR/AR recebidos como mapping resolvido pela política ${evidence.organizationPolicyId} v${evidence.policyVersion}`);
      }
    }

    const shouldAbstain = reasons.length > 0;
    let contextualCvss: null | { vector: string; score: number; severity: string; nomenclature: string; delta: number; decision: string } = null;
    let decision = shouldAbstain ? "abstained" : "unchanged";

    function applyEnvironmentalMetrics(vector: string, overrides: Record<string, string>): string {
      const parts = vector.split("/");
      const prefix = parts[0];
      const metricMap = new Map<string, string>();
      for (let i = 1; i < parts.length; i++) {
        const p = parts[i];
        const colonIdx = p.indexOf(":");
        if (colonIdx > 0) {
          metricMap.set(p.substring(0, colonIdx), p.substring(colonIdx + 1));
        }
      }
      for (const [k, v] of Object.entries(overrides)) {
        if (v && v !== "X") {
          metricMap.set(k, v);
        } else {
          metricMap.delete(k);
        }
      }
      const canonicalOrder = [
        "AV", "AC", "AT", "PR", "UI", "VC", "VI", "VA", "SC", "SI", "SA",
        "E",
        "CR", "IR", "AR",
        "MAV", "MAC", "MAT", "MPR", "MUI", "MVC", "MVI", "MVA", "MSC", "MSI", "MSA"
      ];
      const orderedParts = [prefix];
      for (const k of canonicalOrder) {
        if (metricMap.has(k)) {
          orderedParts.push(`${k}:${metricMap.get(k)}`);
          metricMap.delete(k);
        }
      }
      for (const [k, v] of metricMap.entries()) {
        orderedParts.push(`${k}:${v}`);
      }
      return orderedParts.join("/");
    }

    if (!shouldAbstain) {
      const enrichedVector = applyEnvironmentalMetrics(baseVector, candidateMetrics);
      const envCalc = fromVector(enrichedVector);
      const envScore = envCalc.calculateOverallScore();
      const delta = Math.round((envScore - sourceScore) * 10) / 10;
      decision = delta < 0 ? "downgraded" : delta > 0 ? "upgraded" : "unchanged";
      contextualCvss = { vector: enrichedVector, score: envScore, severity: getSeverity(envScore), nomenclature: envCalc.getNomenclature(), delta, decision };
    }

    const disposition = resolveOperationalDisposition(contextualCvss?.score ?? null, decision, evidence);
    const generatedAt = new Date().toISOString();

    const auditPayload = {
      schema_version: "helpus-audit-receipt-v2",
      cve_id: cveId,
      source_assessment: {
        vector: baseVector,
        nomenclature: sourceNomenclature,
        score: sourceScore,
        severity: sourceSeverity,
        ...sourceAssessmentMeta,
      },
      evidence,
      inferred_metrics: candidateMetrics,
      environmental_assessment: contextualCvss,
      operational_recommendation: disposition,
      governance: {
        review_status: shouldAbstain ? "HUMAN_REVIEW_REQUIRED" : "PROVISIONAL_INFERENCE_READY",
        human_approval_required: true,
        automatic_downgrade_permitted: false,
        authorization_enforced_by_this_route: false,
      },
      generated_at: generatedAt,
    };

    const canonicalJson = jcsCanonicalize(auditPayload);
    const provenanceHash = crypto.createHash("sha256").update(canonicalJson, "utf8").digest("hex");

    return NextResponse.json({
      success: true,
      timestamp: generatedAt,
      cveId,
      sourceAssessment: auditPayload.source_assessment,
      environmentalAssessment: contextualCvss ?? { status: "ABSTAINED", reasons },
      operationalDisposition: disposition,
      inferenceAnalysis: {
        reviewStatus: auditPayload.governance.review_status,
        abstentionReasons: reasons,
        candidateMetrics,
        citations,
        reachabilityClass: reachability,
      },
      governance: auditPayload.governance,
      auditReceipt: {
        canonicalAlgorithm: "JCS-compatible local implementation; formal RFC 8785 conformance requires a pinned independent conformance corpus",
        digestAlgorithm: "SHA-256",
        receiptDigest: provenanceHash,
        schemaVersion: auditPayload.schema_version,
      },
    });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err?.message || "Erro no processamento" }, { status: 400 });
  }
}
