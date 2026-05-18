import seed from "../../data/seed.json";
export function getSeedData() {
  const comparison = seed.comparison.map((row) => ({ ...row, environmental_before: Number(row.environmental_before), environmental_after: Number(row.environmental_after), delta: Number(row.delta) }));
  const summary = seed.summary.map((row) => ({ ...row, base_score: Number(row.base_score), environmental_score: Number(row.environmental_score) }));
  const downgraded = comparison.filter((row) => row.effect === "downgraded").length;
  const upgraded = comparison.filter((row) => row.effect === "upgraded").length;
  const unchanged = comparison.filter((row) => row.effect === "unchanged").length;
  const meanDelta = comparison.reduce((acc, row) => acc + row.delta, 0) / Math.max(comparison.length, 1);
  return { ...seed, comparison, summary, metrics: { findings: comparison.length, assessments: summary.length, downgraded, upgraded, unchanged, meanDelta } };
}
