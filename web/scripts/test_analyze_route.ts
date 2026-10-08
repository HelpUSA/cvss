import { POST } from "../src/app/api/analyze-environment/route";

async function main() {
  console.log("=== TEST 1: Valid fresh evidence ===");
  const req1 = new Request("http://localhost:3000/api/analyze-environment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      cveId: "CVE-2024-4251",
      baseVector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
      evidence: {
        evidenceQuality: "SUFFICIENT",
        telemetryAgeDays: 0.5,
        reachability: "INTERNAL_ROUTED",
        organizationPolicyId: "POL-01",
        policyVersion: "1.0",
      },
    }),
  });
  const res1 = await POST(req1);
  const data1 = await res1.json();
  console.log("Decision:", data1.environmentalAssessment?.decision, "Review status:", data1.inferenceAnalysis.reviewStatus);

  console.log("\n=== TEST 2: Stale telemetry (Fail-Safe Abstention) ===");
  const req2 = new Request("http://localhost:3000/api/analyze-environment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      cveId: "CVE-2024-4251",
      baseVector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
      evidence: {
        evidenceQuality: "SUFFICIENT",
        telemetryAgeDays: 2.5,
        reachability: "INTERNAL_ROUTED",
      },
    }),
  });
  const res2 = await POST(req2);
  const data2 = await res2.json();
  console.log("Environmental status:", data2.environmentalAssessment?.status, "Disposition:", data2.operationalDisposition.code);
  console.log("Abstention reasons:", data2.inferenceAnalysis.abstentionReasons);
}

main().catch(console.error);
