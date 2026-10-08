export function MethodologySection() {
  return (
    <section
      className="methodology-section"
      id="methodology"
      aria-labelledby="methodology-title"
    >
      <div className="section-heading section-heading--centered">
        <span className="section-kicker">Arquitetura de Avaliação</span>
        <h2 id="methodology-title">
          Decisão Operacional em Cinco Camadas Auditáveis
        </h2>
        <p>
          Separação formal entre o score oficial de origem, as evidências ambientais observadas,
          o score ambiental derivado, a política de fluxo local (P0–P4) e a governança com especialista humano.
        </p>
      </div>

      <div className="methodology-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))" }}>
        <article className="methodology-card">
          <span className="methodology-card__number">01</span>
          <h3>Score de Origem</h3>
          <p>
            O score oficial (CNA/NVD) permanece preservado como referência normativa e comparável.
          </p>
          <code>source_cvss</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">02</span>
          <h3>Evidências Locais</h3>
          <p>
            Topologia, telemetria com controle de idade e políticas organizacionais versionadas.
          </p>
          <code>telemetry_evidence</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">03</span>
          <h3>CVSS v4.0 Ambiental</h3>
          <p>
            Cálculo determinístico via algoritmo MacroVector FIRST CVSS v4.0 (sem deltas ad-hoc).
          </p>
          <code>environmental_cvss</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">04</span>
          <h3>Disposição P0–P4</h3>
          <p>
            Mapeamento operacional da fila de remediação local (P0 a P4_DEFER_RECOMMENDED).
          </p>
          <code>operational_policy</code>
        </article>

        <article className="methodology-card">
          <span className="methodology-card__number">05</span>
          <h3>Governança HITL</h3>
          <p>
            Homologação obrigatória por analista humano credenciado e recibo criptográfico SHA-256.
          </p>
          <code>hitl_audit_receipt</code>
        </article>
      </div>

      <div className="methodology-note">
        <strong>Princípio central:</strong>
        A priorização ambiental HelpUS não substitui nem revoga o score de origem do NVD/CNA.
        A classificação P4_DEFER_RECOMMENDED constitui recomendação técnica e NÃO configura aceitação de risco sem autorização formal.
      </div>
    </section>
  );
}
