export type Run = {
  run_id: string;
  case_id?: string;
  findings: number | string;
  assessments: number | string;
  downgraded: number | string;
  unchanged: number | string;
  upgraded: number | string;
  mean_delta: number | string;
  max_abs_delta?: number | string;
  source?: string;
};

function normalizeRuns(runs?: Run[] | Record<string, Run>) {
  if (Array.isArray(runs)) {
    return runs;
  }

  return Object.values(runs ?? {});
}

export function CuratedRunsPanel({
  runs,
}: {
  runs?: Run[] | Record<string, Run>;
}) {
  const normalizedRuns = normalizeRuns(runs);

  return (
    <section
      className="panel curated-runs"
      id="runs"
      aria-labelledby="curated-runs-title"
    >
      <div className="panel-heading">
        <div>
          <span className="section-kicker">Reprodutibilidade</span>
          <h2 id="curated-runs-title">Execuções validadas</h2>
          <p>
            Cenários determinísticos preservados para comparação, auditoria e
            repetição dos resultados.
          </p>
        </div>

        <span className="count-chip">
          {normalizedRuns.length}{" "}
          {normalizedRuns.length === 1 ? "execução" : "execuções"}
        </span>
      </div>

      {normalizedRuns.length === 0 ? (
        <div className="empty-state">
          <strong>Nenhuma execução curada disponível.</strong>
          <p>
            O painel continuará funcional com o baseline real ou com o conjunto
            demonstrativo local.
          </p>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <caption className="sr-only">
              Execuções determinísticas de validação
            </caption>

            <thead>
              <tr>
                <th scope="col">Run</th>
                <th scope="col">Achados</th>
                <th scope="col">Avaliações</th>
                <th scope="col">Rebaixados</th>
                <th scope="col">Inalterados</th>
                <th scope="col">Elevados</th>
                <th scope="col">Delta médio</th>
              </tr>
            </thead>

            <tbody>
              {normalizedRuns.map((run) => (
                <tr key={run.run_id}>
                  <td>
                    <span className="table-primary">{run.run_id}</span>
                    <span className="table-secondary">
                      {run.source || run.case_id || "artefato determinístico"}
                    </span>
                  </td>
                  <td>{run.findings}</td>
                  <td>{run.assessments}</td>
                  <td>
                    <span className="badge badge--down">
                      {run.downgraded}
                    </span>
                  </td>
                  <td>
                    <span className="badge badge--same">
                      {run.unchanged}
                    </span>
                  </td>
                  <td>
                    <span className="badge badge--up">
                      {run.upgraded}
                    </span>
                  </td>
                  <td>{run.mean_delta}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
