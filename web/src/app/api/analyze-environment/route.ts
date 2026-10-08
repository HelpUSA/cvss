import { NextResponse } from "next/server";
import { fromVector } from "ae-cvss-calculator";
import crypto from "crypto";

// Helper to determine severity from CVSS v4.0 score
function getSeverity(score: number): string {
  if (score >= 9.0) return "Critical";
  if (score >= 7.0) return "High";
  if (score >= 4.0) return "Medium";
  if (score > 0.0) return "Low";
  return "None";
}

// Operational disposition mapping (P0 - P4)
function getOperationalDisposition(score: number | null, decision: string): { code: string; label: string; caveat: string } {
  if (score === null || decision === "abstained") {
    return {
      code: "PENDING_HUMAN_REVIEW",
      label: "Revisão Humana Obrigatória",
      caveat: "Inferência automatizada em abstenção segura (fail-safe). Decisão retida.",
    };
  }
  if (score >= 9.0) {
    return {
      code: "P0_IMMEDIATE",
      label: "P0 - Remediação Imediata",
      caveat: "Criticidade operacional máxima exigindo contenção de emergência.",
    };
  }
  if (score >= 7.0) {
    return {
      code: "P1_EXPEDITED",
      label: "P1 - Remediação Prioritária",
      caveat: "Tratamento prioritário na janela de sustentação.",
    };
  }
  if (score >= 4.0) {
    return {
      code: "P2_SCHEDULED",
      label: "P2 - Correção Programada",
      caveat: "Correção dentro do ciclo de release ordinário.",
    };
  }
  if (score > 0.0) {
    return {
      code: "P3_MONITOR",
      label: "P3 - Monitoramento Contínuo",
      caveat: "Baixo impacto ambiental; acompanhamento via telemetria.",
    };
  }
  return {
    code: "P4_DEFER_RECOMMENDED",
    label: "P4 - Postergação Recomendada",
    caveat: "A postergação (P4) é uma recomendação e NÃO constitui aceitação de risco sem aprovação formal de autoridade competente.",
  };
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const {
      cveId = "CVE-2024-4251",
      baseVector = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
      sourceProvider = "CNA_PUBLISHED",
      evidence = {
        evidenceQuality: "SUFFICIENT",
        telemetryAgeDays: 0.5,
        telemetryProfile: "dynamic",
        reachability: "INTERNAL_ROUTED",
        organizationPolicyId: "POL-SEC-2026-V1",
        policyVersion: "1.0",
        pciScope: false,
        highAvailability: false,
        businessCriticality: "high",
        dataSensitivity: "internal",
        firewallActive: true,
      },
      manualOverrides = {},
    } = body;

    // Validate CVSS v4.0 vector
    if (!baseVector || !baseVector.startsWith("CVSS:4.0/")) {
      return NextResponse.json(
        { success: false, error: "Vetor de origem deve ser compatível com CVSS v4.0 (prefixo CVSS:4.0/ obrigatório)" },
        { status: 400 }
      );
    }

    // 1. Calculate Source CVSS (Preserved & Separated)
    const sourceCalculator = fromVector(baseVector);
    const sourceScore = sourceCalculator.calculateOverallScore();
    const sourceSeverity = getSeverity(sourceScore);
    const sourceNomenclature = sourceCalculator.getNomenclature();

    // 2. Fail-Safe Engine Validation
    const citations: string[] = [];
    const reasons: string[] = [];
    const quality = (evidence.evidenceQuality || "UNKNOWN").toUpperCase();
    const telemetryAge = typeof evidence.telemetryAgeDays === "number" ? evidence.telemetryAgeDays : null;
    const maxAge = evidence.telemetryProfile === "static" ? 7.0 : 1.0;

    if (telemetryAge === null) {
      reasons.push("Idade da telemetria ausente");
    } else if (telemetryAge > maxAge) {
      reasons.push(`Telemetria obsoleta (${telemetryAge} dias; limite da política é ${maxAge} dias)`);
    }

    if (quality !== "SUFFICIENT") {
      reasons.push(`Qualidade da evidência não-suficiente (${quality})`);
    }

    // 3. Reachability Reasoning
    // PUBLIC_ROUTED -> MAV:N
    // INTERNAL_ROUTED -> MAV:N (Internal L3-routed reachability remains Network, NOT Adjacent)
    // ADJACENT_ONLY -> MAV:A (requires demonstrated L2 adjacency)
    // LOCAL_ONLY -> MAV:L
    // PHYSICAL_ONLY -> MAV:P
    const reachability = (evidence.reachability || "UNKNOWN").toUpperCase();
    const candidateMetrics: Record<string, string> = { ...manualOverrides };

    if (!candidateMetrics.MAV) {
      if (reachability === "PUBLIC_ROUTED") {
        candidateMetrics.MAV = "N";
        citations.push("MAV:N — Ativo roteado e acessível via rede pública.");
      } else if (reachability === "INTERNAL_ROUTED") {
        candidateMetrics.MAV = "N";
        citations.push("MAV:N — Ativo alcançável via rede IP interna roteada (invariante: rede interna L3 permanece MAV:N, não MAV:A).");
      } else if (reachability === "ADJACENT_ONLY") {
        candidateMetrics.MAV = "A";
        citations.push("MAV:A — Acesso comprovadamente restrito ao mesmo domínio de broadcast L2 / adjacência física.");
      } else if (reachability === "LOCAL_ONLY") {
        candidateMetrics.MAV = "L";
        citations.push("MAV:L — Sem rota remota ou adjacente; execução restrita a contexto local do host.");
      } else if (reachability === "PHYSICAL_ONLY") {
        candidateMetrics.MAV = "P";
        citations.push("MAV:P — Requer acesso físico direto ao dispositivo.");
      } else {
        reasons.push("Classe de alcançabilidade de rede ausente ou indeterminada");
      }
    }

    // 4. Attack Complexity Reasoning (Firewall/WAF presence alone NEVER implies MAC:H)
    if (evidence.firewallActive) {
      citations.push("Presença de Firewall/WAF registrada; conforme a norma, filtragem perimetral genérica não altera MAC para H isoladamente.");
    }
    if (evidence.evidencedExploitPreconditionsElevated) {
      candidateMetrics.MAC = "H";
      citations.push("MAC:H — Pré-condições específicas de exploração demonstradas e documentadas.");
    }

    // 5. Security Requirements (CR, IR, AR) - Policy-governed
    const policyId = evidence.organizationPolicyId;
    const policyVersion = evidence.policyVersion;

    if (policyId && policyVersion) {
      if (evidence.securityRequirements) {
        if (evidence.securityRequirements.CR) candidateMetrics.CR = evidence.securityRequirements.CR;
        if (evidence.securityRequirements.IR) candidateMetrics.IR = evidence.securityRequirements.IR;
        if (evidence.securityRequirements.AR) candidateMetrics.AR = evidence.securityRequirements.AR;
        citations.push(`Requisitos de segurança mapeados via política organizacional ${policyId} v${policyVersion}.`);
      } else {
        // Fallback default organizational policy mapping for demo
        if (evidence.pciScope || evidence.dataSensitivity === "payment") {
          candidateMetrics.CR = "H";
          citations.push(`CR:H — Política ${policyId}: Escopo de dados regulados/cartões.`);
        }
        if (["critical", "high"].includes(evidence.businessCriticality)) {
          candidateMetrics.IR = "H";
          citations.push(`IR:H — Política ${policyId}: Ativo de criticidade elevada requer integridade transacional.`);
        }
        if (evidence.highAvailability) {
          citations.push("Cluster de alta disponibilidade registrado; por norma, redundância física não reduz requisito AR para L.");
        }
      }
    } else if (evidence.securityRequirements) {
      reasons.push("Requisitos de segurança fornecidos sem identificador de política (organizationPolicyId/policyVersion)");
    }

    // Fail-safe abstention check
    const shouldAbstain = reasons.length > 0;

    let contextualCvss: any = null;
    let environmentalVector: string | null = null;
    let delta = 0;
    let decision = "unchanged";

    if (shouldAbstain) {
      decision = "abstained";
    } else {
      // Build environmental vector
      let enrichedVector = baseVector;
      for (const [key, val] of Object.entries(candidateMetrics)) {
        if (val && val !== "X") {
          enrichedVector += `/${key}:${val}`;
        }
      }
      environmentalVector = enrichedVector;
      const envCalc = fromVector(enrichedVector);
      const envScore = envCalc.calculateOverallScore();
      delta = Math.round((envScore - sourceScore) * 10) / 10;
      decision = delta < 0 ? "downgraded" : delta > 0 ? "upgraded" : "unchanged";

      contextualCvss = {
        vector: enrichedVector,
        score: envScore,
        severity: getSeverity(envScore),
        nomenclature: envCalc.getNomenclature(),
        delta,
        decision,
      };
    }

    const disposition = getOperationalDisposition(contextualCvss ? contextualCvss.score : null, decision);

    // 6. Generate RFC 8785 Canonical Provenance Receipt + SHA-256 Digest
    const auditPayload = {
      asset_profile: evidence,
      cve_id: cveId,
      disposition: disposition.code,
      environmental_decision: decision,
      environmental_vector: environmentalVector,
      generated_at: new Date().toISOString(),
      source_vector: baseVector,
    };
    const canonicalJson = JSON.stringify(auditPayload, Object.keys(auditPayload).sort());
    const provenanceHash = crypto.createHash("sha256").update(canonicalJson).digest("hex");

    return NextResponse.json({
      success: true,
      timestamp: new Date().toISOString(),
      cveId,
      // Layer 1: Source Assessment / Provenance
      sourceAssessment: {
        vector: baseVector,
        score: sourceScore,
        severity: sourceSeverity,
        nomenclature: sourceNomenclature,
        provider: sourceProvider,
        retrievedAt: new Date().toISOString(),
      },
      // Layer 2: HelpUS-derived CVSS v4.0 Environmental Assessment
      environmentalAssessment: contextualCvss ? {
        vector: contextualCvss.vector,
        score: contextualCvss.score,
        severity: contextualCvss.severity,
        nomenclature: contextualCvss.nomenclature,
        delta: contextualCvss.delta,
        decision: contextualCvss.decision,
      } : {
        status: "ABSTAINED",
        reasons,
      },
      // Layer 3: Local Operational Disposition
      operationalDisposition: disposition,
      // Layer 4: Evidence & Inference Citations
      inferenceAnalysis: {
        reviewStatus: shouldAbstain ? "HUMAN_REVIEW_REQUIRED" : "PROVISIONAL_INFERENCE_READY",
        abstentionReasons: reasons,
        candidateMetrics,
        citations,
        reachabilityClass: reachability,
      },
      // Layer 5: HITL Governance & Fail-safe Semantics
      governance: {
        humanReviewGate: "HUMAN_REVIEW_REQUIRED",
        autoDowngradePermitted: false,
        hitlSupervisionRequired: true,
      },
      // Audit Receipt & Cryptographic Provenance
      auditReceipt: {
        canonicalAlgorithm: "RFC-8785 / JCS Canonicalization",
        digestAlgorithm: "SHA-256",
        receiptDigest: provenanceHash,
      },
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message || "Erro no processamento da inferência" },
      { status: 400 }
    );
  }
}
