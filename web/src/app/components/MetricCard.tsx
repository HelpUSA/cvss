import type { ReactNode } from "react";

type MetricTone =
  | "neutral"
  | "positive"
  | "warning"
  | "critical"
  | "information";

type MetricCardProps = {
  label: string;
  value: ReactNode;
  detail: string;
  tone?: MetricTone;
};

export function MetricCard({
  label,
  value,
  detail,
  tone = "neutral",
}: MetricCardProps) {
  return (
    <article className={`metric-card metric-card--${tone}`}>
      <span className="metric-card__label">{label}</span>
      <strong className="metric-card__value">{value}</strong>
      <span className="metric-card__detail">{detail}</span>
    </article>
  );
}
