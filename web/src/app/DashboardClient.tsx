"use client";

import { useMemo, useState } from "react";
import { AppHeader } from "./components/AppHeader";
import { HeroSection } from "./components/HeroSection";
import { MethodologySection } from "./components/MethodologySection";
import { MetricCard } from "./components/MetricCard";
import { RiskDistribution } from "./components/RiskDistribution";
import { SiteFooter } from "./components/SiteFooter";
import {
  CuratedRunsPanel,
  type Run as CuratedRun,
} from "./CuratedRunsPanel";

type AnyRow = Record<string, any>;

type DashboardData = {
  runId?: string;
  caseId?: string;
  source?: string;
  sourceDetail?: string;
  dataSource?: string;
  comparison?: AnyRow[];
  assessments?: AnyRow[];
  summary?: AnyRow[];
  curatedRuns?: CuratedRun[] | Record<string, CuratedRun>;
  manifest?: unknown;
  auditEvents?: unknown[];
  auditTrace?: unknown[];
  realAssessment?: AnyRow;
  watcherValidation?: AnyRow;
  metrics?: {
    findings?: number;
    assessments?: number;
    downgraded?: number;
    unchanged?: number;
    upgraded?: number;
    meanDelta?: number;
  };
};

function numberValue(value: unknown, fallback = 0) {
  const converted = Number(value);

  return Number.isFinite(converted) ? converted : fallback;
}

function formatScore(value: unknown) {
  const converted = Number(value);

  return Number.isFinite(converted)
    ? converted.toLocaleString("pt-BR", {
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
      })
    : "n/d";
}

function formatDelta(value: unknown) {
  const converted = Number(value);

  if (!Number.isFinite(converted)) {
    return "n/d";
  }

  return converted.toLocaleString("pt-BR", {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
    signDisplay: "exceptZero",
  });
}

function uniqueValues(rows: AnyRow[], key: string) {
  return Array.from(
    new Set(
      rows
        .map((row) => String(row[key] ?? ""))
        .filter(Boolean),
    ),
  ).sort();
}

function includesText(value: unknown, term: string) {
  return String(value ?? "")
    .toLocaleLowerCase("pt-BR")
    .includes(term.trim().toLocaleLowerCase("pt-BR"));
}

function booleanValue(value: unknown) {
  if (typeof value === "string") {
    return value.toLocaleLowerCase("pt-BR") === "true";
  }

  return Boolean(value);
}

function matchesExpected(row: AnyRow) {
  const values = [
    row.matches_expected_requirements,
    row.matchesExpectedRequirements,
    row.before_matches_expected,
    row.beforeMatchesExpected,
    row.after_matches_expected,
    row.afterMatchesExpected,
  ].filter((value) => value !== undefined && value !== null);

  return values.length === 0
    ? true
    : values.every((value) => booleanValue(value));
}

function effectLabel(effect: unknown) {
  const normalized = String(effect ?? "").toLocaleLowerCase("pt-BR");

  if (normalized === "downgraded") {
    return "Rebaixado";
  }

  if (normalized === "upgraded") {
    return "Elevado";
  }

  if (normalized === "unchanged") {
    return "Inalterado";
  }

  return normalized || "Sem classificação";
}

function effectClass(effect: unknown) {
  const normalized = String(effect ?? "").toLocaleLowerCase("pt-BR");

  if (normalized === "downgraded") {
    return "badge--down";
  }

  if (normalized === "upgraded") {
    return "badge--up";
  }

  return "badge--same";
}

function severityLabel(score: unknown) {
  const value = numberValue(score);

  if (value >= 9) {
    return "Crítico";
  }

  if (value >= 7) {
    return "Alto";
  }

  if (value >= 4) {
    return "Médio";
  }

  if (value > 0) {
    return "Baixo";
  }

  return "Sem score";
}

export function DashboardClient({
  data,
}: {
  data: DashboardData;
}) {
  const [asset, setAsset] = useState("all");
  const [cve, setCve] = useState("all");
  const [effect, setEffect] = useState("all");
  const [vulnerabilityType, setVulnerabilityType] =
    useState("all");
  const [expectedMatch, setExpectedMatch] = useState("all");
  const [query, setQuery] = useState("");
  const [activeFindingId, setActiveFindingId] =
    useState("");

  const comparison = useMemo(
    () =>
      Array.isArray(data.comparison)
        ? data.comparison
        : [],
    [data.comparison],
  );

  const assessments = useMemo(() => {
    if (Array.isArray(data.assessments)) {
      return data.assessments;
    }

    if (Array.isArray(data.summary)) {
      return data.summary;
    }

    return [];
  }, [data.assessments, data.summary]);

  const curatedRuns = useMemo(() => {
    if (Array.isArray(data.curatedRuns)) {
      return data.curatedRuns;
    }

    return Object.values(data.curatedRuns ?? {});
  }, [data.curatedRuns]);

  const auditEvents =
    data.auditEvents ?? data.auditTrace ?? [];

  const source =
    data.source && data.source !== "unknown"
      ? data.source
      : data.dataSource ?? "seed-fallback";

  const sourceDetail =
    data.sourceDetail ??
    (source.includes("postgres")
      ? "Dados carregados da persistência PostgreSQL."
      : "Fallback determinístico carregado do conjunto de evidências versionado.");

  const options = useMemo(
    () => ({
      assets: uniqueValues(comparison, "asset_id"),
      cves: uniqueValues(comparison, "cve"),
      effects: uniqueValues(comparison, "effect"),
      vulnerabilityTypes: uniqueValues(
        comparison,
        "vulnerability_type",
      ),
    }),
    [comparison],
  );

  const filteredComparison = useMemo(
    () =>
      comparison.filter((row) => {
        return (
          (asset === "all" || row.asset_id === asset) &&
          (cve === "all" || row.cve === cve) &&
          (effect === "all" || row.effect === effect) &&
          (vulnerabilityType === "all" ||
            row.vulnerability_type === vulnerabilityType) &&
          (expectedMatch === "all" ||
            String(matchesExpected(row)) === expectedMatch) &&
          (!query.trim() ||
            includesText(row.finding_id, query) ||
            includesText(row.asset_id, query) ||
            includesText(row.cve, query) ||
            includesText(row.vulnerability_type, query))
        );
      }),
    [
      comparison,
      asset,
      cve,
      effect,
      vulnerabilityType,
      expectedMatch,
      query,
    ],
  );

  const filteredAssessments = useMemo(() => {
    if (
      comparison.length > 0 &&
      filteredComparison.length === 0
    ) {
      return [];
    }

    const findingIds = new Set(
      filteredComparison.map((row) => row.finding_id),
    );

    if (findingIds.size === 0) {
      return assessments;
    }

    return assessments.filter((row) =>
      findingIds.has(row.finding_id),
    );
  }, [assessments, comparison.length, filteredComparison]);

  const activeFinding =
    filteredComparison.find(
      (row) => row.finding_id === activeFindingId,
    ) ?? filteredComparison[0];

  const metrics = {
    findings:
      data.metrics?.findings ?? comparison.length,
    assessments:
      data.metrics?.assessments ?? assessments.length,
    downgraded:
      data.metrics?.downgraded ??
      comparison.filter(
        (row) => row.effect === "downgraded",
      ).length,
    unchanged:
      data.metrics?.unchanged ??
      comparison.filter(
        (row) => row.effect === "unchanged",
      ).length,
    upgraded:
      data.metrics?.upgraded ??
      comparison.filter(
        (row) => row.effect === "upgraded",
      ).length,
    meanDelta:
      data.metrics?.meanDelta ??
      comparison.reduce(
        (total, row) => total + numberValue(row.delta),
        0,
      ) /
        Math.max(comparison.length, 1),
  };

  const realAssessment = data.realAssessment;
  const realSummary = realAssessment?.summary ?? {};

  const watcher = data.watcherValidation ?? {
    decisions: 1,
    accepted: 1,
    flagged: 0,
    unclear: 0,
    agreement: 100,
    meanConfidence: 0.7,
  };

  function resetFilters() {
    setAsset("all");
    setCve("all");
    setEffect("all");
    setVulnerabilityType("all");
    setExpectedMatch("all");
    setQuery("");
    setActiveFindingId("");
  }

  return (
    <>
      <a className="skip-link" href="#main-content">
        Pular para o conteúdo principal
      </a>

      <div id="top" />

      <AppHeader />

      <main id="main-content" className="page-shell">
        <HeroSection
          runId={data.runId}
          caseId={data.caseId}
          source={source}
          sourceDetail={sourceDetail}
        />

        <section
          className="dashboard-section"
          id="dashboard"
          aria-labelledby="dashboard-title"
        >
          <div className="section-heading">
            <div>
              <span className="section-kicker">
                Visão geral
              </span>
              <h2 id="dashboard-title">
                Estado atual da análise
              </h2>
            </div>

            <p>
              Métricas derivadas dos artefatos de comparação e
              da trilha ambiental carregada.
            </p>
          </div>

          <div className="metric-grid">
            <MetricCard
              label="Achados"
              value={metrics.findings}
              detail="Vulnerabilidades comparadas"
              tone="information"
            />

            <MetricCard
              label="Avaliações"
              value={metrics.assessments}
              detail="Estados antes e depois"
            />

            <MetricCard
              label="Rebaixados"
              value={metrics.downgraded}
              detail="Menor prioridade contextual"
              tone="positive"
            />

            <MetricCard
              label="Inalterados"
              value={metrics.unchanged}
              detail="Contexto sem mudança"
            />

            <MetricCard
              label="Elevados"
              value={metrics.upgraded}
              detail="Maior prioridade contextual"
              tone="critical"
            />

            <MetricCard
              label="Delta médio"
              value={formatDelta(metrics.meanDelta)}
              detail="Variação ambiental média"
              tone={
                metrics.meanDelta < 0
                  ? "positive"
                  : metrics.meanDelta > 0
                    ? "warning"
                    : "neutral"
              }
            />
          </div>

          <div className="overview-grid">
            <div className="panel">
              <RiskDistribution
                downgraded={metrics.downgraded}
                unchanged={metrics.unchanged}
                upgraded={metrics.upgraded}
              />
            </div>

            <aside className="panel context-snapshot">
              <span className="section-kicker">
                Contrato de dados
              </span>
              <h3>Separação preservada</h3>

              <dl>
                <div>
                  <dt>CVSS oficial</dt>
                  <dd>Referência técnica imutável</dd>
                </div>

                <div>
                  <dt>Contexto ambiental</dt>
                  <dd>Exposição, controles e criticidade</dd>
                </div>

                <div>
                  <dt>Decisão</dt>
                  <dd>Delta, efeito e evidência rastreável</dd>
                </div>
              </dl>
            </aside>
          </div>
        </section>

        <section
          className="explorer-section"
          id="explorer"
          aria-labelledby="explorer-title"
        >
          <div className="section-heading">
            <div>
              <span className="section-kicker">
                Explorador contextual
              </span>
              <h2 id="explorer-title">
                Entenda o impacto de uma evidência
              </h2>
            </div>

            <p>
              O explorador não recalcula nem substitui o CVSS
              oficial. Ele explica a mudança registrada na
              prioridade ambiental.
            </p>
          </div>

          {activeFinding ? (
            <div className="explorer-grid">
              <article className="explorer-primary">
                <div className="explorer-primary__heading">
                  <div>
                    <span className="section-kicker">
                      {activeFinding.finding_id}
                    </span>
                    <h3>{activeFinding.cve}</h3>
                    <p>
                      Ativo {activeFinding.asset_id} ·{" "}
                      {activeFinding.vulnerability_type}
                    </p>
                  </div>

                  <span
                    className={`badge ${effectClass(
                      activeFinding.effect,
                    )}`}
                  >
                    {effectLabel(activeFinding.effect)}
                  </span>
                </div>

                <div className="score-comparison">
                  <div>
                    <span>CVSS oficial</span>
                    <strong>
                      {formatScore(
                        activeFinding.base_score_before ??
                          activeFinding.base_score_after ??
                          activeFinding.environmental_before,
                      )}
                    </strong>
                    <small>
                      {severityLabel(
                        activeFinding.base_score_before ??
                          activeFinding.environmental_before,
                      )}
                    </small>
                  </div>

                  <span
                    className="score-comparison__arrow"
                    aria-hidden="true"
                  >
                    →
                  </span>

                  <div>
                    <span>Ambiental antes</span>
                    <strong>
                      {formatScore(
                        activeFinding.environmental_before,
                      )}
                    </strong>
                    <small>
                      MAV {activeFinding.mav_before || "n/d"}
                    </small>
                  </div>

                  <span
                    className="score-comparison__arrow"
                    aria-hidden="true"
                  >
                    →
                  </span>

                  <div>
                    <span>Ambiental depois</span>
                    <strong>
                      {formatScore(
                        activeFinding.environmental_after,
                      )}
                    </strong>
                    <small>
                      MAV {activeFinding.mav_after || "n/d"}
                    </small>
                  </div>
                </div>
              </article>

              <aside className="explorer-explanation">
                <span className="section-kicker">
                  Leitura da decisão
                </span>

                <strong className="explorer-delta">
                  {formatDelta(activeFinding.delta)}
                </strong>

                <p>
                  O delta representa a diferença observada após
                  aplicar evidências ambientais ao cenário. O
                  score técnico oficial continua preservado.
                </p>

                <ul>
                  <li>
                    Efeito:{" "}
                    <strong>
                      {effectLabel(activeFinding.effect)}
                    </strong>
                  </li>
                  <li>
                    Evidências esperadas:{" "}
                    <strong>
                      {matchesExpected(activeFinding)
                        ? "compatíveis"
                        : "revisão necessária"}
                    </strong>
                  </li>
                  <li>
                    Mudança de vetor:{" "}
                    <strong>
                      {activeFinding.mav_before || "n/d"} →{" "}
                      {activeFinding.mav_after || "n/d"}
                    </strong>
                  </li>
                </ul>
              </aside>
            </div>
          ) : (
            <div className="empty-state">
              <strong>Nenhum achado corresponde aos filtros.</strong>
              <p>
                Limpe os filtros para voltar a explorar as
                evidências disponíveis.
              </p>
              <button
                className="button button--secondary"
                type="button"
                onClick={resetFilters}
              >
                Limpar filtros
              </button>
            </div>
          )}
        </section>

        <section
          className="findings-section"
          id="findings"
          aria-labelledby="findings-title"
        >
          <div className="section-heading">
            <div>
              <span className="section-kicker">
                Investigação
              </span>
              <h2 id="findings-title">
                Achados e comparações
              </h2>
            </div>

            <p>
              Filtre ativos, CVEs, tipos e efeitos para localizar
              rapidamente as decisões relevantes.
            </p>
          </div>

          <div className="panel filter-panel">
            <div className="panel-heading">
              <div>
                <h3>Filtros</h3>
                <p
                  className="results-count"
                  aria-live="polite"
                >
                  Exibindo {filteredComparison.length} de{" "}
                  {comparison.length} achados.
                </p>
              </div>

              <button
                className="button button--quiet"
                type="button"
                onClick={resetFilters}
              >
                Limpar filtros
              </button>
            </div>

            <div className="filters">
              <div className="field field--search">
                <label htmlFor="finding-search">
                  Buscar
                </label>
                <input
                  id="finding-search"
                  value={query}
                  onChange={(event) =>
                    setQuery(event.target.value)
                  }
                  placeholder="Finding, ativo, CVE ou tipo"
                  autoComplete="off"
                />
              </div>

              <div className="field">
                <label htmlFor="asset-filter">Ativo</label>
                <select
                  id="asset-filter"
                  value={asset}
                  onChange={(event) =>
                    setAsset(event.target.value)
                  }
                >
                  <option value="all">Todos</option>
                  {options.assets.map((value) => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </div>

              <div className="field">
                <label htmlFor="cve-filter">CVE</label>
                <select
                  id="cve-filter"
                  value={cve}
                  onChange={(event) =>
                    setCve(event.target.value)
                  }
                >
                  <option value="all">Todas</option>
                  {options.cves.map((value) => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </div>

              <div className="field">
                <label htmlFor="effect-filter">
                  Efeito
                </label>
                <select
                  id="effect-filter"
                  value={effect}
                  onChange={(event) =>
                    setEffect(event.target.value)
                  }
                >
                  <option value="all">Todos</option>
                  {options.effects.map((value) => (
                    <option key={value} value={value}>
                      {effectLabel(value)}
                    </option>
                  ))}
                </select>
              </div>

              <div className="field">
                <label htmlFor="type-filter">Tipo</label>
                <select
                  id="type-filter"
                  value={vulnerabilityType}
                  onChange={(event) =>
                    setVulnerabilityType(
                      event.target.value,
                    )
                  }
                >
                  <option value="all">Todos</option>
                  {options.vulnerabilityTypes.map(
                    (value) => (
                      <option key={value} value={value}>
                        {value}
                      </option>
                    ),
                  )}
                </select>
              </div>

              <div className="field">
                <label htmlFor="evidence-filter">
                  Evidência
                </label>
                <select
                  id="evidence-filter"
                  value={expectedMatch}
                  onChange={(event) =>
                    setExpectedMatch(
                      event.target.value,
                    )
                  }
                >
                  <option value="all">Todas</option>
                  <option value="true">Compatível</option>
                  <option value="false">
                    Requer revisão
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div className="panel">
            <div className="panel-heading">
              <div>
                <h3>Antes e depois</h3>
                <p>
                  Comparação entre o cenário ambiental inicial e
                  o cenário apoiado pelas evidências locais.
                </p>
              </div>
            </div>

            {filteredComparison.length === 0 ? (
              <div className="empty-state">
                <strong>Nenhum resultado encontrado.</strong>
                <p>
                  Ajuste ou limpe os filtros para recuperar os
                  achados.
                </p>
              </div>
            ) : (
              <div className="table-wrap">
                <table>
                  <caption className="sr-only">
                    Comparação ambiental antes e depois
                  </caption>

                  <thead>
                    <tr>
                      <th scope="col">Finding</th>
                      <th scope="col">Ativo</th>
                      <th scope="col">CVE</th>
                      <th scope="col">Tipo</th>
                      <th scope="col">Antes</th>
                      <th scope="col">Depois</th>
                      <th scope="col">Delta</th>
                      <th scope="col">MAV</th>
                      <th scope="col">Efeito</th>
                      <th scope="col">
                        <span className="sr-only">
                          Ação
                        </span>
                      </th>
                    </tr>
                  </thead>

                  <tbody>
                    {filteredComparison.map((row) => (
                      <tr key={row.finding_id}>
                        <td>
                          <span className="table-primary">
                            {row.finding_id}
                          </span>
                        </td>
                        <td>{row.asset_id}</td>
                        <td className="mono">{row.cve}</td>
                        <td>{row.vulnerability_type}</td>
                        <td>
                          {formatScore(
                            row.environmental_before,
                          )}
                        </td>
                        <td>
                          {formatScore(
                            row.environmental_after,
                          )}
                        </td>
                        <td>{formatDelta(row.delta)}</td>
                        <td>
                          {row.mav_before} →{" "}
                          {row.mav_after}
                        </td>
                        <td>
                          <span
                            className={`badge ${effectClass(
                              row.effect,
                            )}`}
                          >
                            {effectLabel(row.effect)}
                          </span>
                        </td>
                        <td>
                          <button
                            className="table-action"
                            type="button"
                            onClick={() => {
                              setActiveFindingId(
                                row.finding_id,
                              );
                              document
                                .getElementById("explorer")
                                ?.scrollIntoView({
                                  behavior: "smooth",
                                  block: "start",
                                });
                            }}
                            aria-label={`Analisar ${row.finding_id}`}
                          >
                            Analisar
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          <details className="panel disclosure">
            <summary>
              <span>
                <strong>Linhas detalhadas de avaliação</strong>
                <small>
                  CR, IR, AR, MAV e compatibilidade das
                  evidências
                </small>
              </span>

              <span className="count-chip">
                {filteredAssessments.length}
              </span>
            </summary>

            <div className="table-wrap">
              <table>
                <caption className="sr-only">
                  Linhas detalhadas de avaliação ambiental
                </caption>

                <thead>
                  <tr>
                    <th scope="col">Finding</th>
                    <th scope="col">Estado</th>
                    <th scope="col">Ativo</th>
                    <th scope="col">CVE</th>
                    <th scope="col">Ambiental</th>
                    <th scope="col">CR</th>
                    <th scope="col">IR</th>
                    <th scope="col">AR</th>
                    <th scope="col">MAV</th>
                    <th scope="col">Evidência</th>
                  </tr>
                </thead>

                <tbody>
                  {filteredAssessments.map(
                    (row, index) => (
                      <tr
                        key={`${row.finding_id}-${row.state}-${index}`}
                      >
                        <td className="mono">
                          {row.finding_id}
                        </td>
                        <td>{row.state}</td>
                        <td>{row.asset_id}</td>
                        <td className="mono">
                          {row.cve}
                        </td>
                        <td>
                          {formatScore(
                            row.environmental_score,
                          )}
                        </td>
                        <td>{row.cr}</td>
                        <td>{row.ir}</td>
                        <td>{row.ar}</td>
                        <td>{row.mav}</td>
                        <td>
                          {matchesExpected(row)
                            ? "Compatível"
                            : "Revisar"}
                        </td>
                      </tr>
                    ),
                  )}
                </tbody>
              </table>
            </div>
          </details>
        </section>

        <section
          className="operations-grid"
          aria-label="Operação e automação"
        >
          <article className="panel baseline-panel">
            <span className="section-kicker">
              Baseline real
            </span>
            <h2>Varredura automatizada Trivy</h2>
            <p>
              Resultado mais recente do pipeline local aplicado
              ao repositório monitorado.
            </p>

            <div className="baseline-total">
              <strong>
                {realSummary.finding_count ?? 0}
              </strong>
              <span>achados detectados</span>
            </div>

            <div className="severity-grid">
              <div>
                <span className="severity-dot severity-dot--critical" />
                <strong>
                  {realSummary.critical ?? 0}
                </strong>
                <small>Críticos</small>
              </div>

              <div>
                <span className="severity-dot severity-dot--high" />
                <strong>{realSummary.high ?? 0}</strong>
                <small>Altos</small>
              </div>

              <div>
                <span className="severity-dot severity-dot--medium" />
                <strong>
                  {realSummary.medium ?? 0}
                </strong>
                <small>Médios</small>
              </div>

              <div>
                <span className="severity-dot severity-dot--low" />
                <strong>{realSummary.low ?? 0}</strong>
                <small>Baixos</small>
              </div>
            </div>

            <dl className="compact-data-list">
              <div>
                <dt>Ativo</dt>
                <dd>
                  {realAssessment?.asset?.id ??
                    "local-repository"}
                </dd>
              </div>

              <div>
                <dt>Scanner</dt>
                <dd>
                  {realAssessment?.scanner ?? "trivy"}
                </dd>
              </div>
            </dl>
          </article>

          <article className="panel watcher-panel">
            <span className="section-kicker">
              Watcher IA
            </span>
            <h2>Validação automatizada</h2>
            <p>
              Evidências ligadas a decisões reproduzíveis. A
              adjudicação humana independente permanece uma
              etapa comparativa futura.
            </p>

            <div className="watcher-stats">
              <div>
                <strong>
                  {watcher.decisions ?? 1}
                </strong>
                <span>Decisões</span>
              </div>

              <div>
                <strong>
                  {watcher.accepted ?? 1}
                </strong>
                <span>Aceitas</span>
              </div>

              <div>
                <strong>
                  {watcher.flagged ?? 0}
                </strong>
                <span>Sinalizadas</span>
              </div>

              <div>
                <strong>
                  {watcher.agreement ?? 100}%
                </strong>
                <span>Concordância</span>
              </div>
            </div>

            <div className="confidence-row">
              <span>Confiança média</span>
              <strong>
                {numberValue(
                  watcher.meanConfidence,
                  0.7,
                ).toLocaleString("pt-BR", {
                  minimumFractionDigits: 1,
                  maximumFractionDigits: 2,
                })}
              </strong>
            </div>
          </article>
        </section>

        <CuratedRunsPanel runs={curatedRuns} />

        <MethodologySection />

        <section
          className="evidence-section"
          id="evidence"
          aria-labelledby="evidence-title"
        >
          <div className="section-heading">
            <div>
              <span className="section-kicker">
                Transparência
              </span>
              <h2 id="evidence-title">
                Manifesto e trilha de auditoria
              </h2>
            </div>

            <p>
              Os artefatos completos permanecem disponíveis para
              inspeção técnica sem dominar a experiência
              principal.
            </p>
          </div>

          <div className="evidence-grid">
            <details className="evidence-card">
              <summary>
                <span>
                  <strong>Manifesto da execução</strong>
                  <small>
                    Arquivos, hashes, contagens e contexto do run
                  </small>
                </span>
                <span aria-hidden="true">+</span>
              </summary>

              <pre>
                {JSON.stringify(
                  data.manifest ?? {},
                  null,
                  2,
                )}
              </pre>
            </details>

            <details className="evidence-card">
              <summary>
                <span>
                  <strong>Eventos de auditoria</strong>
                  <small>
                    Evidências e justificativas em ordem
                    determinística
                  </small>
                </span>
                <span aria-hidden="true">+</span>
              </summary>

              <pre>
                {JSON.stringify(auditEvents, null, 2)}
              </pre>
            </details>
          </div>
        </section>
      </main>

      <SiteFooter />
    </>
  );
}
