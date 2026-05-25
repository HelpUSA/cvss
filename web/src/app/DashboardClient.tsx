"use client";

import { useMemo, useState } from "react";

type AnyRow = Record<string, any>;

function fmt(value: number | string | null | undefined) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toFixed(1) : "n/a";
}

function uniqueValues(rows: AnyRow[], key: string) {
  return Array.from(new Set(rows.map((row) => String(row[key] ?? "")).filter(Boolean))).sort();
}

function includesText(value: unknown, term: string) {
  return String(value ?? "").toLowerCase().includes(term.trim().toLowerCase());
}

export function DashboardClient({ data }: { data: any }) {
  const [asset, setAsset] = useState("all");
  const [cve, setCve] = useState("all");
  const [effect, setEffect] = useState("all");
  const [vulnerabilityType, setVulnerabilityType] = useState("all");
  const [expectedMatch, setExpectedMatch] = useState("all");
  const [query, setQuery] = useState("");

  const comparison: AnyRow[] = data.comparison ?? [];
  const assessments: AnyRow[] = data.assessments ?? [];
  const manifest = data.manifest as any;

  const options = useMemo(() => ({
    assets: uniqueValues(comparison, "asset_id"),
    cves: uniqueValues(comparison, "cve"),
    effects: uniqueValues(comparison, "effect"),
    vulnerabilityTypes: uniqueValues(comparison, "vulnerability_type"),
  }), [comparison]);

  const filteredComparison = useMemo(() => comparison.filter((row) => {
    const matchExpected = row.matches_expected_requirements ?? row.matchesExpectedRequirements;
    return (asset === "all" || row.asset_id === asset)
      && (cve === "all" || row.cve === cve)
      && (effect === "all" || row.effect === effect)
      && (vulnerabilityType === "all" || row.vulnerability_type === vulnerabilityType)
      && (expectedMatch === "all" || String(Boolean(matchExpected)) === expectedMatch)
      && (
        !query.trim()
        || includesText(row.finding_id, query)
        || includesText(row.asset_id, query)
        || includesText(row.cve, query)
        || includesText(row.vulnerability_type, query)
      );
  }), [comparison, asset, cve, effect, vulnerabilityType, expectedMatch, query]);

  const filteredFindingIds = new Set(filteredComparison.map((row) => row.finding_id));
  const filteredAssessments = assessments.filter((row) => !filteredFindingIds.size || filteredFindingIds.has(row.finding_id));

  function resetFilters() {
    setAsset("all");
    setCve("all");
    setEffect("all");
    setVulnerabilityType("all");
    setExpectedMatch("all");
    setQuery("");
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <div className="eyebrow">AI Bridge / Watcher Artifact</div>
          <h1 className="title">CVSS Environmental Dashboard</h1>
          <p className="subtitle">Interactive cloud-ready view of the PCI segmented lab run. The dashboard connects local environmental evidence, CVSS Environmental labels, before-after score deltas, and audit-trace material used by the manuscript.</p>
        </div>
        <div className="card mono">
          <div className="label">Latest run</div>
          <div>{data.runId}</div>
          <div className="label" style={{ marginTop: 12 }}>Case</div>
          <div>{data.caseId}</div>
          <div className="label" style={{ marginTop: 12 }}>Data source</div>
          <div><span className="badge unchanged">{data.source}</span></div>
          <div className="label" style={{ marginTop: 12 }}>{data.sourceDetail}</div>
        </div>
      </section>

      <section className="grid cards">
        <div className="card"><div className="metric">{data.metrics.findings}</div><div className="label">Findings</div></div>
        <div className="card"><div className="metric">{data.metrics.assessments}</div><div className="label">Assessments</div></div>
        <div className="card"><div className="metric">{data.metrics.downgraded}</div><div className="label">Downgraded</div></div>
        <div className="card"><div className="metric">{data.metrics.unchanged}</div><div className="label">Unchanged</div></div>
        <div className="card"><div className="metric">{data.metrics.meanDelta.toFixed(3)}</div><div className="label">Mean delta</div></div>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h2>Finding filters</h2>
            <p className="label">Showing {filteredComparison.length} of {comparison.length} findings.</p>
          </div>
          <button className="button" type="button" onClick={resetFilters}>Reset filters</button>
        </div>
        <div className="filters">
          <label>Search<input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Finding, asset, CVE, type" /></label>
          <label>Asset<select value={asset} onChange={(event) => setAsset(event.target.value)}><option value="all">All assets</option>{options.assets.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
          <label>CVE<select value={cve} onChange={(event) => setCve(event.target.value)}><option value="all">All CVEs</option>{options.cves.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
          <label>Effect<select value={effect} onChange={(event) => setEffect(event.target.value)}><option value="all">All effects</option>{options.effects.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
          <label>Type<select value={vulnerabilityType} onChange={(event) => setVulnerabilityType(event.target.value)}><option value="all">All types</option>{options.vulnerabilityTypes.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
          <label>Expected match<select value={expectedMatch} onChange={(event) => setExpectedMatch(event.target.value)}><option value="all">All</option><option value="true">Matches</option><option value="false">Does not match</option></select></label>
        </div>
      </section>

      <section className="panel">
        <h2>Before/after environmental effects</h2>
        <div className="table-wrap">
          <table>
            <thead><tr><th>Finding</th><th>Asset</th><th>CVE</th><th>Type</th><th>Before</th><th>After</th><th>Delta</th><th>MAV</th><th>Effect</th></tr></thead>
            <tbody>{filteredComparison.map((row) => (
              <tr key={row.finding_id}>
                <td className="mono">{row.finding_id}</td>
                <td>{row.asset_id}</td>
                <td className="mono">{row.cve}</td>
                <td>{row.vulnerability_type}</td>
                <td>{fmt(row.environmental_before)}</td>
                <td>{fmt(row.environmental_after)}</td>
                <td>{Number(row.delta).toFixed(1)}</td>
                <td>{row.mav_before} → {row.mav_after}</td>
                <td><span className={`badge ${row.effect}`}>{row.effect}</span></td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </section>

      <section className="panel">
        <h2>Assessment rows</h2>
        <div className="table-wrap">
          <table>
            <thead><tr><th>Finding</th><th>State</th><th>Asset</th><th>CVE</th><th>Environmental</th><th>CR</th><th>IR</th><th>AR</th><th>MAV</th><th>Expected match</th></tr></thead>
            <tbody>{filteredAssessments.map((row: any) => (
              <tr key={row.id}>
                <td className="mono">{row.finding_id}</td>
                <td>{row.state}</td>
                <td>{row.asset_id}</td>
                <td className="mono">{row.cve}</td>
                <td>{fmt(row.environmental_score)}</td>
                <td>{row.cr}</td>
                <td>{row.ir}</td>
                <td>{row.ar}</td>
                <td>{row.mav}</td>
                <td>{String(Boolean(row.matches_expected_requirements ?? row.matchesExpectedRequirements))}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </section>

      <section className="panel">
        <h2>Audit and manifest context</h2>
        <div className="grid two">
          <div className="card"><div className="label">Manifest</div><pre>{JSON.stringify(manifest, null, 2)}</pre></div>
          <div className="card"><div className="label">Audit events</div><pre>{JSON.stringify(data.auditEvents ?? [], null, 2)}</pre></div>
        </div>
      </section>
    </main>
  );
}


