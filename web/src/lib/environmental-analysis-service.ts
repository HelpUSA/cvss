import crypto from "crypto";
import { fromVector } from "ae-cvss-calculator";

import {
  jcsCanonicalize,
} from "@/lib/jcs";

export type SourceAssessmentMeta = {
  provider: string;
  [key: string]: unknown;
};

export type AnalysisEvidence =
  Record<string, unknown>;

export type EnvironmentalAnalysisInput = {
  cveId: string;
  baseVector: string;
  sourceAssessmentMeta:
    SourceAssessmentMeta;
  evidence: AnalysisEvidence;
};

export type EnvironmentalAssessment = {
  vector: string;
  score: number;
  severity: string;
  nomenclature: string;
  delta: number;
  decision:
    | "downgraded"
    | "upgraded"
    | "unchanged";
};

export type EnvironmentalAnalysisResult = {
  timestamp: string;
  cveId: string;
  sourceAssessment: {
    vector: string;
    nomenclature: string;
    score: number;
    severity: string;
    [key: string]: unknown;
  };
  environmentalAssessment:
    | EnvironmentalAssessment
    | {
        status: "ABSTAINED";
        reasons: string[];
      };
  operationalDisposition:
    Record<string, unknown>;
  inferenceAnalysis: {
    reviewStatus: string;
    abstentionReasons: string[];
    candidateMetrics:
      Record<string, string>;
    supplementalMetrics:
      Record<string, string>;
    citations: string[];
    reachabilityClass: string;
  };
  governance: {
    review_status: string;
    human_approval_required: boolean;
    automatic_downgrade_permitted: boolean;
    authorization_enforced_by_this_route: boolean;
  };
  auditReceipt: {
    canonicalAlgorithm: string;
    digestAlgorithm: "SHA-256";
    receiptDigest: string;
    schemaVersion: string;
  };
};

type OperationalBand = {
  code:
    | "P0_IMMEDIATE"
    | "P1_EXPEDITED"
    | "P2_SCHEDULED"
    | "P3_MONITOR"
    | "P4_DEFER_RECOMMENDED";
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

function getSeverity(
  cvssScore: number,
): string {
  if (cvssScore >= 9.0) return "Critical";
  if (cvssScore >= 7.0) return "High";
  if (cvssScore >= 4.0) return "Medium";
  if (cvssScore > 0.0) return "Low";
  return "None";
}

function resolveOperationalDisposition(
  score: number | null,
  decision: string,
  evidence: AnalysisEvidence,
): Record<string, unknown> {
  if (
    score === null ||
    decision === "abstained"
  ) {
    return {
      code: "EVIDENCE_REMEDIATION_REQUIRED",
      label:
        "Evidência insuficiente para decisão ambiental",
      caveat:
        "A execução entrou em ABSTAIN. Corrija ou complete as evidências antes de afirmar métricas ambientais.",
      policyApplied: false,
    };
  }

  const policy =
    evidence.operationalPolicy as
      | OperationalPolicy
      | undefined;

  if (
    !policy ||
    !policy.policyId ||
    !policy.policyVersion ||
    !Array.isArray(policy.scoreBands)
  ) {
    return {
      code: "PENDING_POLICY_REVIEW",
      label:
        "Política Operacional Necessária",
      caveat:
        "O CVSS-BE foi calculado, mas P0-P4 não é derivado diretamente do score sem uma política organizacional explícita e versionada.",
      policyApplied: false,
    };
  }

  if (
    evidence.organizationPolicyId &&
    evidence.organizationPolicyId !==
      policy.policyId
  ) {
    return {
      code: "PENDING_POLICY_REVIEW",
      label:
        "Política Operacional Inconsistente",
      caveat:
        "operationalPolicy.policyId difere de organizationPolicyId.",
      policyApplied: false,
    };
  }

  if (
    evidence.policyVersion &&
    evidence.policyVersion !==
      policy.policyVersion
  ) {
    return {
      code: "PENDING_POLICY_REVIEW",
      label:
        "Versão de Política Inconsistente",
      caveat:
        "operationalPolicy.policyVersion difere de policyVersion.",
      policyApplied: false,
    };
  }

  const allowed = new Set([
    "P0_IMMEDIATE",
    "P1_EXPEDITED",
    "P2_SCHEDULED",
    "P3_MONITOR",
    "P4_DEFER_RECOMMENDED",
  ]);

  const validBands =
    policy.scoreBands.filter(
      (band) =>
        allowed.has(band.code) &&
        Number.isFinite(band.minScore) &&
        Number.isFinite(band.maxScore) &&
        band.minScore >= 0 &&
        band.maxScore <= 10 &&
        band.minScore <= band.maxScore,
    );

  const matches =
    validBands.filter(
      (band) =>
        score >= band.minScore &&
        score <= band.maxScore,
    );

  if (matches.length !== 1) {
    return {
      code: "PENDING_POLICY_REVIEW",
      label:
        "Política Operacional Ambígua",
      caveat:
        `O score ${score.toFixed(1)} deve corresponder a exatamente uma banda operacional; correspondências encontradas: ${matches.length}.`,
      policyApplied: false,
    };
  }

  const band = matches[0];

  return {
    code: band.code,
    label: band.label,
    caveat:
      band.caveat ??
      "Recomendação local sujeita a aprovação humana.",
    policyApplied: true,
    policyId: policy.policyId,
    policyVersion:
      policy.policyVersion,
  };
}

function applyEnvironmentalMetrics(
  vector: string,
  overrides: Record<string, string>,
): string {
  const parts = vector.split("/");
  const prefix = parts[0];
  const metricMap =
    new Map<string, string>();

  for (
    let index = 1;
    index < parts.length;
    index += 1
  ) {
    const part = parts[index];
    const colonIndex =
      part.indexOf(":");

    if (colonIndex > 0) {
      metricMap.set(
        part.substring(0, colonIndex),
        part.substring(colonIndex + 1),
      );
    }
  }

  for (
    const [key, value]
    of Object.entries(overrides)
  ) {
    if (value && value !== "X") {
      metricMap.set(key, value);
    } else {
      metricMap.delete(key);
    }
  }

  const canonicalOrder = [
    "AV",
    "AC",
    "AT",
    "PR",
    "UI",
    "VC",
    "VI",
    "VA",
    "SC",
    "SI",
    "SA",
    "E",
    "CR",
    "IR",
    "AR",
    "MAV",
    "MAC",
    "MAT",
    "MPR",
    "MUI",
    "MVC",
    "MVI",
    "MVA",
    "MSC",
    "MSI",
    "MSA",
    "S",
    "AU",
    "R",
    "V",
    "RE",
    "U",
  ];

  const orderedParts = [prefix];

  for (
    const key of canonicalOrder
  ) {
    if (metricMap.has(key)) {
      orderedParts.push(
        `${key}:${metricMap.get(key)}`,
      );
      metricMap.delete(key);
    }
  }

  for (
    const [key, value]
    of metricMap.entries()
  ) {
    orderedParts.push(
      `${key}:${value}`,
    );
  }

  return orderedParts.join("/");
}

function assertAnalysisInput(
  input: EnvironmentalAnalysisInput,
): void {
  if (
    !input.cveId ||
    typeof input.cveId !== "string"
  ) {
    throw new Error(
      "cveId é obrigatório",
    );
  }

  if (
    !input.baseVector ||
    typeof input.baseVector !==
      "string" ||
    !input.baseVector.startsWith(
      "CVSS:4.0/",
    )
  ) {
    throw new Error(
      "baseVector CVSS:4.0 é obrigatório",
    );
  }

  if (
    !input.evidence ||
    typeof input.evidence !==
      "object" ||
    Array.isArray(input.evidence)
  ) {
    throw new Error(
      "evidence é obrigatório",
    );
  }

  if (
    !input.sourceAssessmentMeta ||
    typeof input.sourceAssessmentMeta !==
      "object" ||
    !input.sourceAssessmentMeta.provider
  ) {
    throw new Error(
      "sourceAssessmentMeta.provider é obrigatório para provenance",
    );
  }
}

export function analyzeEnvironment(
  input: EnvironmentalAnalysisInput,
): EnvironmentalAnalysisResult {
  assertAnalysisInput(input);

  const {
    cveId,
    baseVector,
    sourceAssessmentMeta,
    evidence,
  } = input;

  const sourceCalculator =
    fromVector(baseVector);

  const sourceScore =
    sourceCalculator
      .calculateOverallScore();

  const sourceSeverity =
    getSeverity(sourceScore);

  const sourceNomenclature =
    sourceCalculator
      .getNomenclature();

  const citations: string[] = [];
  const reasons: string[] = [];

  const candidateMetrics:
    Record<string, string> = {};

  const quality =
    String(
      evidence.evidenceQuality ??
        "UNKNOWN",
    ).toUpperCase();

  const telemetryAge =
    typeof evidence.telemetryAgeDays ===
      "number"
      ? evidence.telemetryAgeDays
      : null;

  const maxAge =
    typeof evidence.maxTelemetryAgeDays ===
      "number"
      ? evidence.maxTelemetryAgeDays
      : evidence.telemetryProfile ===
          "static"
        ? 7.0
        : 1.0;

  if (telemetryAge === null) {
    reasons.push(
      "Idade da telemetria ausente",
    );
  } else if (telemetryAge > maxAge) {
    reasons.push(
      `Telemetria obsoleta (${telemetryAge} dias; limite ${maxAge} dias)`,
    );
  }

  if (
    [
      "UNKNOWN",
      "INSUFFICIENT",
      "CONFLICTING",
    ].includes(quality)
  ) {
    reasons.push(
      `Qualidade da evidência não suficiente (${quality})`,
    );
  }

  if (
    evidence.conflictFlag === true
  ) {
    reasons.push(
      "Conflito explícito de evidência",
    );
  }

  const reachability =
    String(
      evidence.reachability ??
        "UNKNOWN",
    ).toUpperCase();

  if (
    reachability ===
      "PUBLIC_ROUTED" ||
    reachability ===
      "INTERNAL_ROUTED"
  ) {
    candidateMetrics.MAV = "N";
    citations.push(
      `MAV:N - reachability ${reachability}`,
    );
  } else if (
    reachability === "ADJACENT_ONLY"
  ) {
    candidateMetrics.MAV = "A";
    citations.push(
      "MAV:A - adjacência explicitamente evidenciada",
    );
  } else if (
    reachability === "LOCAL_ONLY"
  ) {
    candidateMetrics.MAV = "L";
    citations.push(
      "MAV:L - exploração restrita a contexto local",
    );
  } else if (
    reachability === "PHYSICAL_ONLY"
  ) {
    candidateMetrics.MAV = "P";
    citations.push(
      "MAV:P - interação física requerida",
    );
  } else {
    reasons.push(
      "Classe de reachability ausente ou indeterminada",
    );
  }

  if (evidence.firewallActive) {
    citations.push(
      "Firewall/WAF registrado como evidência; MAC não foi alterado por essa condição isoladamente.",
    );
  }

  if (
    evidence
      .evidencedExploitPreconditionsElevated ===
    true
  ) {
    candidateMetrics.MAC = "H";
    citations.push(
      "MAC:H - precondições específicas de exploração evidenciadas",
    );
  }

  const threatIntelligence =
    evidence.threatIntelligence as
      | Record<string, unknown>
      | undefined;

  if (threatIntelligence) {
    const exploitMaturity =
      String(
        threatIntelligence.exploitMaturity ??
          "X",
      ).toUpperCase();

    const threatSource =
      typeof threatIntelligence.sourceReference ===
      "string"
        ? threatIntelligence.sourceReference.trim()
        : "";

    const observedAt =
      typeof threatIntelligence.observedAt ===
      "string"
        ? threatIntelligence.observedAt.trim()
        : "";

    if (
      ["A", "P", "U"].includes(
        exploitMaturity,
      )
    ) {
      if (!threatSource || !observedAt) {
        reasons.push(
          "Exploit Maturity explícita sem provenance completa de threat intelligence",
        );
      } else {
        candidateMetrics.E =
          exploitMaturity;
        citations.push(
          `E:${exploitMaturity} - threat intelligence ${threatSource} observada em ${observedAt}`,
        );
      }
    }
  }

  const supplementalInput =
    evidence.supplementalMetrics &&
    typeof evidence.supplementalMetrics === "object" &&
    !Array.isArray(evidence.supplementalMetrics)
      ? evidence.supplementalMetrics as Record<string, unknown>
      : null;

  const supplementalMetrics:
    Record<string, string> = {};

  if (supplementalInput) {
    const allowedSupplemental: Record<
      string,
      readonly string[]
    > = {
      S: ["N", "P"],
      AU: ["N", "Y"],
      R: ["A", "U", "I"],
      V: ["D", "C"],
      RE: ["L", "M", "H"],
      U: [
        "Clear",
        "Green",
        "Amber",
        "Red",
      ],
    };

    for (
      const [
        metric,
        allowedValues,
      ] of Object.entries(
        allowedSupplemental,
      )
    ) {
      const raw =
        supplementalInput[metric];

      if (
        typeof raw !== "string" ||
        raw === "X"
      ) {
        continue;
      }

      const value =
        metric === "U"
          ? raw
          : raw.toUpperCase();

      if (
        allowedValues.includes(
          value,
        )
      ) {
        supplementalMetrics[metric] =
          value;
      }
    }
  }

  const requirements =
    evidence.securityRequirements as
      | Record<string, unknown>
      | undefined;

  if (requirements) {
    if (
      !evidence.organizationPolicyId ||
      !evidence.policyVersion
    ) {
      reasons.push(
        "securityRequirements fornecido sem organizationPolicyId/policyVersion",
      );
    } else {
      for (
        const key of [
          "CR",
          "IR",
          "AR",
        ]
      ) {
        const value =
          requirements[key];

        const normalized =
          String(
            value ?? "",
          ).toUpperCase();

        if (
          ["H", "M", "L"].includes(
            normalized,
          )
        ) {
          candidateMetrics[key] =
            normalized;
        }
      }

      citations.push(
        `CR/IR/AR recebidos como mapping resolvido pela política ${String(evidence.organizationPolicyId)} v${String(evidence.policyVersion)}`,
      );
    }
  }

  const shouldAbstain =
    reasons.length > 0;

  let contextualCvss:
    | EnvironmentalAssessment
    | null = null;

  let decision =
    shouldAbstain
      ? "abstained"
      : "unchanged";

  if (!shouldAbstain) {
    const enrichedVector =
      applyEnvironmentalMetrics(
        baseVector,
        {
          ...candidateMetrics,
          ...supplementalMetrics,
        },
      );

    const environmentCalculator =
      fromVector(enrichedVector);

    const environmentScore =
      environmentCalculator
        .calculateOverallScore();

    const delta =
      Math.round(
        (
          environmentScore -
          sourceScore
        ) * 10,
      ) / 10;

    const resolvedDecision:
      EnvironmentalAssessment[
        "decision"
      ] =
      delta < 0
        ? "downgraded"
        : delta > 0
          ? "upgraded"
          : "unchanged";

    decision = resolvedDecision;

    contextualCvss = {
      vector: enrichedVector,
      score: environmentScore,
      severity:
        getSeverity(
          environmentScore,
        ),
      nomenclature:
        environmentCalculator
          .getNomenclature(),
      delta,
      decision:
        resolvedDecision,
    };
  }

  const disposition =
    resolveOperationalDisposition(
      contextualCvss?.score ?? null,
      decision,
      evidence,
    );

  const generatedAt =
    new Date().toISOString();

  const auditPayload = {
    schema_version:
      "helpus-audit-receipt-v2",
    cve_id: cveId,
    source_assessment: {
      vector: baseVector,
      nomenclature:
        sourceNomenclature,
      score: sourceScore,
      severity:
        sourceSeverity,
      ...sourceAssessmentMeta,
    },
    evidence,
    inferred_metrics:
      candidateMetrics,
    environmental_assessment:
      contextualCvss,
    operational_recommendation:
      disposition,
    governance: {
      review_status:
        shouldAbstain
          ? "EVIDENCE_REMEDIATION_REQUIRED"
          : "AUTO_ACCEPT_READY",
      human_approval_required: false,
      automatic_downgrade_permitted:
        false,
      authorization_enforced_by_this_route:
        false,
    },
    generated_at:
      generatedAt,
  };

  const canonicalJson =
    jcsCanonicalize(
      auditPayload,
    );

  const provenanceHash =
    crypto
      .createHash("sha256")
      .update(
        canonicalJson,
        "utf8",
      )
      .digest("hex");

  return {
    timestamp:
      generatedAt,
    cveId,
    sourceAssessment:
      auditPayload
        .source_assessment,
    environmentalAssessment:
      contextualCvss ?? {
        status:
          "ABSTAINED",
        reasons,
      },
    operationalDisposition:
      disposition,
    inferenceAnalysis: {
      reviewStatus:
        auditPayload
          .governance
          .review_status,
      abstentionReasons:
        reasons,
      candidateMetrics,
      supplementalMetrics,
      citations,
      reachabilityClass:
        reachability,
    },
    governance:
      auditPayload.governance,
    auditReceipt: {
      canonicalAlgorithm:
        "JCS-compatible local implementation; formal RFC 8785 conformance requires a pinned independent conformance corpus",
      digestAlgorithm:
        "SHA-256",
      receiptDigest:
        provenanceHash,
      schemaVersion:
        auditPayload
          .schema_version,
    },
  };
}
