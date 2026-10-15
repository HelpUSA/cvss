type SupplementalMetrics = {
  S?: string;
  AU?: string;
  R?: string;
  V?: string;
  RE?: string;
  U?: string;
};

const LABELS: Record<string, string> = {
  S: "Safety",
  AU: "Automatable",
  R: "Recovery",
  V: "Value Density",
  RE: "Vulnerability Response Effort",
  U: "Provider Urgency",
};

export function SupplementalMetricsSummary({
  metadata,
}: {
  metadata: unknown;
}) {
  if (
    !metadata ||
    typeof metadata !== "object" ||
    Array.isArray(metadata)
  ) {
    return null;
  }

  const raw =
    (metadata as Record<string, unknown>)
      .supplementalMetrics;

  if (
    !raw ||
    typeof raw !== "object" ||
    Array.isArray(raw)
  ) {
    return null;
  }

  const metrics =
    Object.entries(
      raw as SupplementalMetrics,
    ).filter(
      ([, value]) =>
        typeof value === "string" &&
        value !== "X",
    );

  if (metrics.length === 0) {
    return null;
  }

  return (
    <section
      className="panel supplemental-summary"
      aria-labelledby="supplemental-summary-title"
    >
      <span className="section-kicker">
        Contexto suplementar
      </span>
      <h2 id="supplemental-summary-title">
        Supplemental Metrics
      </h2>
      <p>
        Estes valores adicionam contexto ao
        vetor e à análise local, mas não
        alteram o score CVSS numérico.
      </p>

      <dl>
        {metrics.map(
          ([metric, value]) => (
            <div key={metric}>
              <dt>
                {LABELS[metric] ?? metric}
                {" ("}
                {metric}
                {")"}
              </dt>
              <dd>{value}</dd>
            </div>
          ),
        )}
      </dl>
    </section>
  );
}
