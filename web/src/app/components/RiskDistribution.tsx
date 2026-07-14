type RiskDistributionProps = {
  downgraded: number;
  unchanged: number;
  upgraded: number;
};

function percentage(value: number, total: number) {
  if (total <= 0) {
    return 0;
  }

  return (value / total) * 100;
}

export function RiskDistribution({
  downgraded,
  unchanged,
  upgraded,
}: RiskDistributionProps) {
  const total = downgraded + unchanged + upgraded;

  const downWidth = percentage(downgraded, total);
  const unchangedWidth = percentage(unchanged, total);
  const upgradedWidth = percentage(upgraded, total);

  const unchangedX = downWidth;
  const upgradedX = downWidth + unchangedWidth;

  return (
    <div className="risk-distribution">
      <div className="risk-distribution__heading">
        <div>
          <span className="section-kicker">Distribuição contextual</span>
          <h3>Impacto das evidências locais</h3>
        </div>

        <strong>{total} achados</strong>
      </div>

      <svg
        className="risk-chart"
        viewBox="0 0 100 12"
        role="img"
        aria-labelledby="risk-chart-title risk-chart-description"
        preserveAspectRatio="none"
      >
        <title id="risk-chart-title">
          Distribuição dos efeitos contextuais
        </title>

        <desc id="risk-chart-description">
          {downgraded} rebaixados, {unchanged} inalterados e {upgraded} elevados.
        </desc>

        <rect
          className="risk-chart__background"
          x="0"
          y="0"
          width="100"
          height="12"
          rx="6"
        />

        {downWidth > 0 ? (
          <rect
            className="risk-chart__down"
            x="0"
            y="0"
            width={downWidth}
            height="12"
            rx="6"
          />
        ) : null}

        {unchangedWidth > 0 ? (
          <rect
            className="risk-chart__unchanged"
            x={unchangedX}
            y="0"
            width={unchangedWidth}
            height="12"
          />
        ) : null}

        {upgradedWidth > 0 ? (
          <rect
            className="risk-chart__up"
            x={upgradedX}
            y="0"
            width={upgradedWidth}
            height="12"
            rx="6"
          />
        ) : null}
      </svg>

      <div className="risk-legend">
        <div>
          <span className="risk-legend__dot risk-legend__dot--down" />
          <span>Rebaixados</span>
          <strong>{downgraded}</strong>
        </div>

        <div>
          <span className="risk-legend__dot risk-legend__dot--same" />
          <span>Inalterados</span>
          <strong>{unchanged}</strong>
        </div>

        <div>
          <span className="risk-legend__dot risk-legend__dot--up" />
          <span>Elevados</span>
          <strong>{upgraded}</strong>
        </div>
      </div>
    </div>
  );
}
