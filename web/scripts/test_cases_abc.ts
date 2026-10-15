import { analyzeEnvironment } from "../src/lib/environmental-analysis-service";

const baseVector = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N";

console.log("=== CASE A: UNTOUCHED DEFAULTS (UNKNOWN / UNKNOWN / null) ===");
const caseA = analyzeEnvironment({
  cveId: "CVE-2024-CASE-A",
  baseVector,
  sourceAssessmentMeta: { provider: "CNA_PUBLISHED" },
  evidence: {
    reachability: "UNKNOWN",
    evidenceQuality: "UNKNOWN",
    telemetryAgeDays: null,
    maxTelemetryAgeDays: 1,
    telemetryProfile: "dynamic",
  },
});
console.log("Assessment:", JSON.stringify(caseA.environmentalAssessment, null, 2));
console.log("Inference Reasons:", caseA.inferenceAnalysis.abstentionReasons);

console.log("\n=== CASE B: EXPLICIT KNOWN EVIDENCE (INTERNAL_ROUTED / SUFFICIENT / age=0) ===");
const caseB = analyzeEnvironment({
  cveId: "CVE-2024-CASE-B",
  baseVector,
  sourceAssessmentMeta: { provider: "CNA_PUBLISHED" },
  evidence: {
    reachability: "INTERNAL_ROUTED",
    evidenceQuality: "SUFFICIENT",
    telemetryAgeDays: 0,
    maxTelemetryAgeDays: 1,
    telemetryProfile: "dynamic",
  },
});
console.log("Assessment:", JSON.stringify(caseB.environmentalAssessment, null, 2));
console.log("Candidate Metrics:", caseB.inferenceAnalysis.candidateMetrics);

console.log("\n=== CASE C1: INSUFFICIENT EVIDENCE ===");
const caseC1 = analyzeEnvironment({
  cveId: "CVE-2024-CASE-C1",
  baseVector,
  sourceAssessmentMeta: { provider: "CNA_PUBLISHED" },
  evidence: {
    reachability: "INTERNAL_ROUTED",
    evidenceQuality: "INSUFFICIENT",
    telemetryAgeDays: 0,
    maxTelemetryAgeDays: 1,
    telemetryProfile: "dynamic",
  },
});
console.log("Assessment:", JSON.stringify(caseC1.environmentalAssessment, null, 2));
console.log("Inference Reasons:", caseC1.inferenceAnalysis.abstentionReasons);

console.log("\n=== CASE C2: CONFLICTING EVIDENCE ===");
const caseC2 = analyzeEnvironment({
  cveId: "CVE-2024-CASE-C2",
  baseVector,
  sourceAssessmentMeta: { provider: "CNA_PUBLISHED" },
  evidence: {
    reachability: "INTERNAL_ROUTED",
    evidenceQuality: "CONFLICTING",
    telemetryAgeDays: 0,
    maxTelemetryAgeDays: 1,
    telemetryProfile: "dynamic",
  },
});
console.log("Assessment:", JSON.stringify(caseC2.environmentalAssessment, null, 2));
console.log("Inference Reasons:", caseC2.inferenceAnalysis.abstentionReasons);
