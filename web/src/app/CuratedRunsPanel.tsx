type Run = {
  run_id: string;
  findings: number;
  assessments: number;
  downgraded: number;
  unchanged: number;
  upgraded: number;
  mean_delta: number;
};

export function CuratedRunsPanel({ runs }: { runs?: Run[] }) {
  const normalizedRuns = Array.isArray(runs) ? runs : Object.values(runs ?? {}) as Run[];
 if (!normalizedRuns || normalizedRuns.length === 0) return null;
  return (
    <section className="rounded-2xl border bg-white p-5 shadow-sm">
      <div className="mb-3 flex items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold">Curated validation runs</h2>
          <p className="text-sm text-slate-600">Engineering-validation scenarios generated from deterministic run artifacts.</p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">{runs.length} runs</span>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="text-left text-slate-500">
            <tr>
              <th className="py-2 pr-4">Run</th>
              <th className="py-2 pr-4">Findings</th>
              <th className="py-2 pr-4">Assessments</th>
              <th className="py-2 pr-4">Down</th>
              <th className="py-2 pr-4">Same</th>
              <th className="py-2 pr-4">Up</th>
              <th className="py-2 pr-4">Mean delta</th>
            </tr>
          </thead>
          <tbody>
            {normalizedRuns.map((run) => (
              <tr key={run.run_id} className="border-t">
                <td className="py-2 pr-4 font-medium text-slate-800">{run.run_id}</td>
                <td className="py-2 pr-4">{run.findings}</td>
                <td className="py-2 pr-4">{run.assessments}</td>
                <td className="py-2 pr-4">{run.downgraded}</td>
                <td className="py-2 pr-4">{run.unchanged}</td>
                <td className="py-2 pr-4">{run.upgraded}</td>
                <td className="py-2 pr-4">{run.mean_delta}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}


