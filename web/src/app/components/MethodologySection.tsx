export function MethodologySection() {
  return (
    <section
      className="methodology-section"
      id="methodology"
      aria-labelledby="methodology-title"
    >
      <div className="section-heading section-heading--centered">
        <span className="section-kicker">
          Arquitetura de avaliação
        </span>
        <h2 id="methodology-title">
          Cinco camadas, sem misturar CVSS
          com política operacional
        </h2>
        <p>
          O fluxo preserva a avaliação de
          origem, registra evidências,
          resolve métricas sob regras
          versionadas, calcula o CVSS
          determinístico e mantém auditoria
          da execução.
        </p>
      </div>

      <div
        className="methodology-grid"
        style={{
          gridTemplateColumns:
            "repeat(auto-fit, minmax(200px, 1fr))",
        }}
      >
        <article className="methodology-card">
          <span className="methodology-card__number">
            01
          </span>
          <h3>Origem</h3>
          <p>
            Vetor e score CVSS-B publicados
            pela fonte permanecem
            preservados.
          </p>
          <code>source_cvss</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">
            02
          </span>
          <h3>Evidências</h3>
          <p>
            Contexto observado, origem,
            atualidade e qualidade da
            evidência.
          </p>
          <code>evidence_snapshot</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">
            03
          </span>
          <h3>Métricas ambientais</h3>
          <p>
            Regras determinísticas resolvem
            apenas métricas sustentadas pela
            evidência.
          </p>
          <code>environmental_metrics</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">
            04
          </span>
          <h3>Score</h3>
          <p>
            O cálculo final usa o scorer
            CVSS v4.0 determinístico e mantém
            a nomenclatura FIRST.
          </p>
          <code>CVSS-BE / CVSS-BTE</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">
            05
          </span>
          <h3>Auditoria</h3>
          <p>
            Evidência, vetor, versão do motor
            e recibo ficam associados à
            execução. Revisão humana é
            opcional conforme política local,
            não requisito do score.
          </p>
          <code>audit_receipt</code>
        </article>
      </div>
    </section>
  );
}
