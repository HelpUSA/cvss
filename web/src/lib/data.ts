import { PrismaClient } from "@prisma/client";
import seed from "../../data/seed.json";

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };
const prisma = globalForPrisma.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;

type ComparisonRow = {
  finding_id: string;
  asset_id: string;
  cve: string;
  vulnerability_type: string;
  environmental_before: number;
  environmental_after: number;
  delta: number;
  effect: string;
  mav_before: string;
  mav_after: string;
  before_matches_expected: boolean;
  after_matches_expected: boolean;
};

type SummaryRow = {
  finding_id: string;
  asset_id: string;
  cve: string;
  vulnerability_type: string;
  state: string;
  base_score: number;
  environmental_score: number;
  cr: string;
  ir: string;
  ar: string;
  mav: string;
  matches_expected_requirements: boolean;
};

function withMetrics(payload: any, source = "unknown", sourceDetail = "Unknown data source") {
  const comparison = payload.comparison.map((row: any) => ({
    ...row,
    environmental_before: Number(row.environmental_before),
    environmental_after: Number(row.environmental_after),
    delta: Number(row.delta),
  })) as ComparisonRow[];
  const summary = payload.summary.map((row: any) => ({
    ...row,
    base_score: Number(row.base_score),
    environmental_score: Number(row.environmental_score),
  })) as SummaryRow[];
  const downgraded = comparison.filter((row) => row.effect === "downgraded").length;
  const upgraded = comparison.filter((row) => row.effect === "upgraded").length;
  const unchanged = comparison.filter((row) => row.effect === "unchanged").length;
  const meanDelta = comparison.reduce((acc, row) => acc + row.delta, 0) / Math.max(comparison.length, 1);
  return { ...payload, comparison, summary, curatedRuns: payload.curatedRuns ?? (seed as any).curatedRuns ?? [], source, sourceDetail, metrics: { findings: comparison.length, assessments: summary.length, downgraded, upgraded, unchanged, meanDelta } };
}

export function getSeedData() {
  return withMetrics(seed, "seed-fallback", "Local bundled seed.json fallback");
}

export async function getDashboardData() {
  if (!process.env.DATABASE_URL) {
    return getSeedData();
  }

  try {
    const latestRun = await prisma.run.findFirst({
      orderBy: { generatedAt: "desc" },
      include: {
        summaries: { orderBy: { findingId: "asc" } },
        comparisons: { orderBy: { findingId: "asc" } },
        auditEvents: { orderBy: { ordinal: "asc" }, take: 40 },
      },
    });

    if (!latestRun) {
      return getSeedData();
    }

    const comparison: ComparisonRow[] = latestRun.comparisons.map((row) => ({
      finding_id: row.findingId,
      asset_id: row.assetId,
      cve: row.cve,
      vulnerability_type: row.vulnerabilityType,
      environmental_before: row.environmentalBefore,
      environmental_after: row.environmentalAfter,
      delta: row.delta,
      effect: row.effect,
      mav_before: row.mavBefore,
      mav_after: row.mavAfter,
      before_matches_expected: row.beforeMatchesExpected,
      after_matches_expected: row.afterMatchesExpected,
    }));

    const summary: SummaryRow[] = latestRun.summaries.map((row) => ({
      finding_id: row.findingId,
      asset_id: row.assetId,
      cve: row.cve,
      vulnerability_type: row.vulnerabilityType,
      state: row.state,
      base_score: row.baseScore,
      environmental_score: row.environmentalScore,
      cr: row.cr,
      ir: row.ir,
      ar: row.ar,
      mav: row.mav,
      matches_expected_requirements: row.matchesExpectedRequirements,
    }));

    const auditTrace = latestRun.auditEvents.map((row) => row.event);
    return withMetrics({
      runId: latestRun.id,
      caseId: latestRun.caseId,
      manifest: latestRun.manifest,
      comparison,
      summary,
      auditTrace,
      dataSource: "railway-postgres",
    });
  } catch (error) {
    console.error("Falling back to seed data after database read failed", error);
    return { ...getSeedData(), dataSource: "seed-fallback" };
  }
}



