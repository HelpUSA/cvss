export function MethodologySection() {
  return (
    <section
      className="methodology-section"
      id="methodology"
      aria-labelledby="methodology-title"
    >
      <div className="section-heading section-heading--centered">
        <span className="section-kicker">Como funciona</span>
        <h2 id="methodology-title">
          Uma decisão em três camadas rastreáveis
        </h2>
        <p>
          A plataforma mantém o score oficial separado das evidências utilizadas
          para ajustar prioridade, tratamento e urgência operacional.
        </p>
      </div>

      <div className="methodology-grid">
        <article className="methodology-card">
          <span className="methodology-card__number">01</span>
          <h3>CVSS oficial</h3>
          <p>
            O score técnico original permanece preservado como referência
            normativa e comparável.
          </p>
          <code>official_cvss</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">02</span>
          <h3>Evidências ambientais</h3>
          <p>
            Exposição, segmentação, criticidade, controles e impacto são
            associados ao ativo.
          </p>
          <code>evidence</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">03</span>
          <h3>Prioridade contextual</h3>
          <p>
            A decisão resultante apresenta delta, justificativa e trilha de
            auditoria sem reescrever o score oficial.
          </p>
          <code>contextual_environmental</code>
        </article>
      </div>

      <div className="methodology-note">
        <strong>Princípio central:</strong>
        priorização contextual não é uma nova versão do CVSS e não substitui a
        avaliação técnica oficial.
      </div>
    </section>
  );
}
