import { PrismaClient } from "@prisma/client";
import seed from "../data/seed.json";
const prisma = new PrismaClient();
function num(value: unknown): number { const parsed = Number(value); return Number.isFinite(parsed) ? parsed : 0; }
async function main() {
  await prisma.run.upsert({ where: { id: seed.runId }, update: { caseId: seed.caseId, manifest: seed.manifest as any }, create: { id: seed.runId, caseId: seed.caseId, manifest: seed.manifest as any } });
  for (const row of seed.summary as any[]) {
    await prisma.assessment.upsert({ where: { id: `${seed.runId}:${row.finding_id}:${row.state}` }, update: {}, create: { id: `${seed.runId}:${row.finding_id}:${row.state}`, runId: seed.runId, findingId: row.finding_id, assetId: row.asset_id, cve: row.cve, vulnerabilityType: row.vulnerability_type, state: row.state, baseScore: num(row.base_score), environmentalScore: num(row.environmental_score), cr: row.cr, ir: row.ir, ar: row.ar, mav: row.mav, matchesExpectedRequirements: String(row.matches_expected_requirements).toLowerCase() === "true" } });
  }
  for (const row of seed.comparison as any[]) {
    await prisma.comparison.upsert({ where: { id: `${seed.runId}:${row.finding_id}` }, update: {}, create: { id: `${seed.runId}:${row.finding_id}`, runId: seed.runId, findingId: row.finding_id, assetId: row.asset_id, cve: row.cve, vulnerabilityType: row.vulnerability_type, environmentalBefore: num(row.environmental_before), environmentalAfter: num(row.environmental_after), delta: num(row.delta), effect: row.effect, mavBefore: row.mav_before, mavAfter: row.mav_after, beforeMatchesExpected: String(row.before_matches_expected).toLowerCase() === "true", afterMatchesExpected: String(row.after_matches_expected).toLowerCase() === "true", raw: row } });
  }
  for (const [index, event] of (seed.auditTrace as any[]).entries()) {
    await prisma.auditEvent.upsert({ where: { id: `${seed.runId}:audit:${index}` }, update: {}, create: { id: `${seed.runId}:audit:${index}`, runId: seed.runId, ordinal: index, event } });
  }
}
main().finally(async () => prisma.$disconnect());
