type HeroSectionProps = {
  runId?: string;
  caseId?: string;
  source?: string;
  sourceDetail?: string;
};

function normalizeSource(source?: string) {
  if (!source || source === "unknown") {
    return "Fonte demonstrativa";
  }

  if (source.includes("railway") || source.includes("postgres")) {
    return "PostgreSQL conectado";
  }

  if (source.includes("seed")) {
    return "Baseline demonstrativo";
  }

  return source;
}

export function HeroSection({
  runId,
  caseId,
  source,
  sourceDetail,
}: HeroSectionProps) {
  return (
    <section className="hero-section" aria-labelledby="hero-title">
      <div className="hero-section__content">
        <div className="hero-kicker">
          <span className="status-dot" aria-hidden="true" />
          Plataforma de priorização contextual
        </div>

        <h1 id="hero-title">
          Contexto operacional sem distorcer o{" "}
          <span>CVSS oficial.</span>
        </h1>

        <p className="hero-lead">
          Compare scores, controles, exposição e criticidade para transformar
          vulnerabilidades em decisões priorizadas, explicáveis e auditáveis.
        </p>

        <div className="hero-contract" aria-label="Contrato de separação">
          <span>
            <code>official_cvss</code>
            permanece imutável
          </span>

          <span aria-hidden="true">→</span>

          <span>
            <code>contextual_environmental</code>
            orienta a prioridade
          </span>
        </div>

        <div className="hero-actions">
          <a className="button button--primary" href="#dashboard">
            Ver visão geral
          </a>

          <a className="button button--secondary" href="#methodology">
            Entender metodologia
          </a>
        </div>
      </div>

      <aside className="hero-context" aria-label="Contexto da execução">
        <div className="hero-context__topline">
          <span>Execução ativa</span>
          <span className="live-chip">
            <span aria-hidden="true" />
            Dados disponíveis
          </span>
        </div>

        <dl className="context-list">
          <div>
            <dt>Run</dt>
            <dd>{runId || "baseline-local"}</dd>
          </div>

          <div>
            <dt>Caso</dt>
            <dd>{caseId || "contextual-assessment"}</dd>
          </div>

          <div>
            <dt>Origem</dt>
            <dd>{normalizeSource(source)}</dd>
          </div>
        </dl>

        <p className="context-detail">
          {sourceDetail ||
            "Dados validados pelo pipeline determinístico do projeto."}
        </p>
      </aside>
    </section>
  );
}
