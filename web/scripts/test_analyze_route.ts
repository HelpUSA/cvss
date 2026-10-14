import { POST } from "../src/app/api/analyze-environment/route";
import fs from "fs";
import path from "path";

const baseBody = {
  cveId: "CVE-TEST-0001",
  baseVector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
  sourceAssessmentMeta: { provider: "TEST_PROVIDER", origin: "TEST_FIXTURE" },
};

function req(body: any) {
  return new Request("http://localhost:3000/api/analyze-environment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

async function main() {
  const results: any[] = [];
  const check = (name: string, passed: boolean, details: any = {}) => results.push({ name, passed, ...details });

  // 1. Missing evidence must fail closed (HTTP 400).
  const r1 = await POST(req(baseBody));
  check("1. missing evidence -> HTTP 400", r1.status === 400, { status: r1.status });

  // 2. Stale evidence must abstain.
  const r2 = await POST(req({ ...baseBody, evidence: { evidenceQuality: "SUFFICIENT", telemetryAgeDays: 3, telemetryProfile: "dynamic", reachability: "INTERNAL_ROUTED" } }));
  const d2 = await r2.json();
  check("2. stale evidence -> HUMAN_REVIEW_REQUIRED", d2.inferenceAnalysis?.reviewStatus === "HUMAN_REVIEW_REQUIRED" && d2.environmentalAssessment?.status === "ABSTAINED");

  // 3. Conflicting / insufficient evidence must abstain.
  const r3 = await POST(req({ ...baseBody, evidence: { evidenceQuality: "CONFLICTING", telemetryAgeDays: 0.1, reachability: "INTERNAL_ROUTED" } }));
  const d3 = await r3.json();
  check("3. conflicting/insufficient evidence -> HUMAN_REVIEW_REQUIRED", d3.inferenceAnalysis?.reviewStatus === "HUMAN_REVIEW_REQUIRED");

  // 4. INTERNAL_ROUTED -> MAV:N
  const r4 = await POST(req({ ...baseBody, evidence: { evidenceQuality: "SUFFICIENT", telemetryAgeDays: 0.1, reachability: "INTERNAL_ROUTED" } }));
  const d4 = await r4.json();
  check("4. INTERNAL_ROUTED -> MAV:N", d4.inferenceAnalysis?.candidateMetrics?.MAV === "N");

  // 5. ADJACENT_ONLY -> MAV:A
  const r5 = await POST(req({ ...baseBody, evidence: { evidenceQuality: "SUFFICIENT", telemetryAgeDays: 0.1, reachability: "ADJACENT_ONLY" } }));
  const d5 = await r5.json();
  check("5. ADJACENT_ONLY -> MAV:A", d5.inferenceAnalysis?.candidateMetrics?.MAV === "A");

  // 6. Security requirements without policy metadata must abstain.
  const r6 = await POST(req({ ...baseBody, evidence: { evidenceQuality: "SUFFICIENT", telemetryAgeDays: 0.1, reachability: "INTERNAL_ROUTED", securityRequirements: { CR: "H", IR: "H" } } }));
  const d6 = await r6.json();
  check("6. CR/IR/AR without policy metadata -> abstain/reject", d6.inferenceAnalysis?.reviewStatus === "HUMAN_REVIEW_REQUIRED");

  // 7. Absent operational policy -> PENDING_POLICY_REVIEW.
  const r7 = await POST(req({ ...baseBody, evidence: { evidenceQuality: "SUFFICIENT", telemetryAgeDays: 0.1, reachability: "INTERNAL_ROUTED" } }));
  const d7 = await r7.json();
  check("7. absent operational policy -> PENDING_POLICY_REVIEW", d7.operationalDisposition?.code === "PENDING_POLICY_REVIEW");

  // 8. Explicit versioned operational policy -> versioned P0-P4 mapping.
  const policy = {
    policyId: "POL-TEST-01",
    policyVersion: "1.0",
    scoreBands: [
      { code: "P4_DEFER_RECOMMENDED", label: "P4", minScore: 0.0, maxScore: 3.9 },
      { code: "P2_SCHEDULED", label: "P2", minScore: 4.0, maxScore: 6.9 },
      { code: "P1_EXPEDITED", label: "P1", minScore: 7.0, maxScore: 8.9 },
      { code: "P0_IMMEDIATE", label: "P0", minScore: 9.0, maxScore: 10.0 },
    ],
  };
  const r8 = await POST(req({ ...baseBody, evidence: { evidenceQuality: "SUFFICIENT", telemetryAgeDays: 0.1, reachability: "INTERNAL_ROUTED", organizationPolicyId: "POL-TEST-01", policyVersion: "1.0", operationalPolicy: policy } }));
  const d8 = await r8.json();
  check("8. explicit versioned operational policy -> disposition", d8.operationalDisposition?.policyApplied === true && d8.operationalDisposition?.policyId === "POL-TEST-01");

  // 9. Source vector already containing optional metrics -> no duplicate metrics in enriched vector!
  const vectorWithOptional = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/MAV:A/CR:M";
  const r9 = await POST(req({ ...baseBody, baseVector: vectorWithOptional, evidence: { evidenceQuality: "SUFFICIENT", telemetryAgeDays: 0.1, reachability: "INTERNAL_ROUTED" } }));
  const d9 = await r9.json();
  const enrichedVector = d9.environmentalAssessment?.vector ?? "";
  const mavCount = (enrichedVector.match(/\/MAV:/g) || []).length;
  const crCount = (enrichedVector.match(/\/CR:/g) || []).length;
  check("9. source vector containing optional metrics -> no duplicate metrics", mavCount === 1 && crCount === 1, { enrichedVector, mavCount, crCount });

  // 10. Nested provenance receipt canonicalization.
  const r10 = await POST(req({ ...baseBody, evidence: { evidenceQuality: "SUFFICIENT", telemetryAgeDays: 0.1, reachability: "INTERNAL_ROUTED" } }));
  const d10 = await r10.json();
  const digest = d10.auditReceipt?.receiptDigest;
  check("10. nested provenance receipt canonicalization", typeof digest === "string" && digest.length === 64, { digest });

  // 11. No automatic downgrade under incomplete evidence.
  const r11 = await POST(req({ ...baseBody, evidence: { evidenceQuality: "UNKNOWN", telemetryAgeDays: 0.1, reachability: "INTERNAL_ROUTED" } }));
  const d11 = await r11.json();
  check("11. no automatic downgrade under incomplete evidence", d11.governance?.automatic_downgrade_permitted === false && d11.governance?.human_approval_required === true);

  const summary = {
    suite: "Web API fail-safe + policy separation",
    timestamp: new Date().toISOString(),
    total: results.length,
    passed: results.filter((x) => x.passed).length,
    failed: results.filter((x) => !x.passed).length,
    results
  };

  const outPath = path.resolve(__dirname, "../../outputs/web_api_tests_results.json");
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(summary, null, 2), "utf8");
  console.log(JSON.stringify(summary, null, 2));

  if (summary.failed > 0) process.exit(1);
}

main().catch((err) => { console.error(err); process.exit(1); });
