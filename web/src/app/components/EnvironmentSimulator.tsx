"use client";

import { useState } from "react";

export function EnvironmentSimulator() {
  const [cveId, setCveId] = useState("CVE-2024-4251");
  const [baseVector, setBaseVector] = useState("CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N");
  const [sourceProvider, setSourceProvider] = useState("CNA_PUBLISHED");
  const [reachability, setReachability] = useState("INTERNAL_ROUTED");
  const [telemetryAgeDays, setTelemetryAgeDays] = useState(0.5);
  const [evidenceQuality, setEvidenceQuality] = useState("SUFFICIENT");
  const [firewallActive, setFirewallActive] = useState(true);
  const [pciScope, setPciScope] = useState(true);
  const [highAvailability, setHighAvailability] = useState(true);
  const [businessCriticality, setBusinessCriticality] = useState("high");
  const [dataSensitivity, setDataSensitivity] = useState("payment");

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [analystDecision, setAnalystDecision] = useState<string | null>(null);

  const runAnalysis = async () => {
    setLoading(true);
    setAnalystDecision(null);
    try {
      const res = await fetch("/api/analyze-environment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cveId,
          baseVector,
          sourceProvider,
          evidence: {
            evidenceQuality,
            telemetryAgeDays: Number(telemetryAgeDays),
            telemetryProfile: "dynamic",
            reachability,
            organizationPolicyId: "POL-SEC-2026-V1",
            policyVersion: "1.0",
            pciScope,
            highAvailability,
            businessCriticality,
            dataSensitivity,
            firewallActive,
          },
        }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section
      id="simulator"
      className="panel"
      style={{
        margin: "2.5rem 0",
        padding: "2rem",
        borderRadius: "var(--radius-lg)",
        background: "linear-gradient(180deg, var(--surface-strong) 0%, var(--surface) 100%)",
        border: "1px solid var(--border-strong)",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem" }}>
        <div>
          <span className="section-kicker" style={{ color: "var(--primary)" }}>
            ⚡ Laboratório Interativo & Benchmark Experimental
          </span>
          <h2 style={{ fontSize: "1.75rem", margin: "0.25rem 0 0.5rem" }}>
            Simulador de Ambiente Operacional CVSS v4.0 (5 Camadas)
          </h2>
          <p style={{ color: "var(--text-soft)", maxWidth: "800px", margin: 0 }}>
            Avaliação contextual determinística em estrita conformidade com o algoritmo de MacroVetores FIRST CVSS v4.0.
            Separação formal entre score de origem, vetor ambiental derivado, disposição operacional P0–P4 e governança HITL.
          </p>
        </div>

        <button
          onClick={runAnalysis}
          disabled={loading}
          className="button button--primary"
          style={{ padding: "0.85rem 1.75rem", fontSize: "1rem", cursor: "pointer" }}
        >
          {loading ? "Processando Inferência..." : "▶ Executar Avaliação CVSS v4.0"}
        </button>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "1.25rem",
          marginTop: "1.75rem",
        }}
      >
        {/* Coluna 1: Dados da Origem */}
        <div style={{ background: "var(--surface-soft)", padding: "1.25rem", borderRadius: "var(--radius-md)" }}>
          <h4 style={{ margin: "0 0 1rem", color: "var(--text)" }}>1. Vetor de Origem (Source)</h4>
          <div style={{ marginBottom: "0.8rem" }}>
            <label style={{ display: "block", fontSize: "0.85rem", color: "var(--text-soft)", marginBottom: "0.3rem" }}>
              Identificador CVE
            </label>
            <input
              type="text"
              value={cveId}
              onChange={(e) => setCveId(e.target.value)}
              style={{
                width: "100%",
                padding: "0.5rem",
                borderRadius: "var(--radius-sm)",
                background: "var(--background)",
                border: "1px solid var(--border)",
                color: "var(--text)",
              }}
            />
          </div>

          <div style={{ marginBottom: "0.8rem" }}>
            <label style={{ display: "block", fontSize: "0.85rem", color: "var(--text-soft)", marginBottom: "0.3rem" }}>
              Vetor CVSS v4.0 de Origem
            </label>
            <input
              type="text"
              value={baseVector}
              onChange={(e) => setBaseVector(e.target.value)}
              style={{
                width: "100%",
                padding: "0.5rem",
                borderRadius: "var(--radius-sm)",
                background: "var(--background)",
                border: "1px solid var(--border)",
                color: "var(--text)",
                fontSize: "0.8rem",
                fontFamily: "monospace",
              }}
            />
          </div>

          <div>
            <label style={{ display: "block", fontSize: "0.85rem", color: "var(--text-soft)", marginBottom: "0.3rem" }}>
              Origem do Registro
            </label>
            <select
              value={sourceProvider}
              onChange={(e) => setSourceProvider(e.target.value)}
              style={{
                width: "100%",
                padding: "0.5rem",
                borderRadius: "var(--radius-sm)",
                background: "var(--background)",
                border: "1px solid var(--border)",
                color: "var(--text)",
              }}
            >
              <option value="CNA_PUBLISHED">CNA Autorizado (CNA_PUBLISHED)</option>
              <option value="NVD_INDEXED">Indexado pelo NVD (NVD_INDEXED)</option>
              <option value="INVESTIGATOR_GROUND_TRUTH">Pesquisa Experimental (Anotação de Especialistas)</option>
            </select>
          </div>
        </div>

        {/* Coluna 2: Telemetria & Topologia */}
        <div style={{ background: "var(--surface-soft)", padding: "1.25rem", borderRadius: "var(--radius-md)" }}>
          <h4 style={{ margin: "0 0 1rem", color: "var(--text)" }}>2. Topologia & Telemetria</h4>
          
          <div style={{ marginBottom: "0.8rem" }}>
            <label style={{ display: "block", fontSize: "0.85rem", color: "var(--text-soft)", marginBottom: "0.3rem" }}>
              Classe de Alcançabilidade (MAV)
            </label>
            <select
              value={reachability}
              onChange={(e) => setReachability(e.target.value)}
              style={{
                width: "100%",
                padding: "0.5rem",
                borderRadius: "var(--radius-sm)",
                background: "var(--background)",
                border: "1px solid var(--border)",
                color: "var(--text)",
              }}
            >
              <option value="PUBLIC_ROUTED">PUBLIC_ROUTED → MAV:N (Internet pública)</option>
              <option value="INTERNAL_ROUTED">INTERNAL_ROUTED → MAV:N (Rede interna L3)</option>
              <option value="ADJACENT_ONLY">ADJACENT_ONLY → MAV:A (Adjacência L2 restrita)</option>
              <option value="LOCAL_ONLY">LOCAL_ONLY → MAV:L (Sessão local no host)</option>
              <option value="PHYSICAL_ONLY">PHYSICAL_ONLY → MAV:P (Acesso físico)</option>
            </select>
          </div>

          <div style={{ marginBottom: "0.8rem" }}>
            <label style={{ display: "block", fontSize: "0.85rem", color: "var(--text-soft)", marginBottom: "0.3rem" }}>
              Idade da Telemetria: <strong>{telemetryAgeDays} dia(s)</strong> (Limite: 1.0 dia)
            </label>
            <input
              type="range"
              min="0.0"
              max="3.0"
              step="0.1"
              value={telemetryAgeDays}
              onChange={(e) => setTelemetryAgeDays(parseFloat(e.target.value))}
              style={{ width: "100%" }}
            />
            {telemetryAgeDays > 1.0 && (
              <small style={{ color: "var(--critical)", display: "block", marginTop: "0.2rem" }}>
                ⚠️ Acima de 1.0 dia aciona abstenção fail-safe (telemetria obsoleta).
              </small>
            )}
          </div>

          <div>
            <label style={{ display: "block", fontSize: "0.85rem", color: "var(--text-soft)", marginBottom: "0.3rem" }}>
              Qualidade da Evidência
            </label>
            <select
              value={evidenceQuality}
              onChange={(e) => setEvidenceQuality(e.target.value)}
              style={{
                width: "100%",
                padding: "0.5rem",
                borderRadius: "var(--radius-sm)",
                background: "var(--background)",
                border: "1px solid var(--border)",
                color: "var(--text)",
              }}
            >
              <option value="SUFFICIENT">SUFFICIENT (Evidência verificada)</option>
              <option value="INSUFFICIENT">INSUFFICIENT (Força abstenção)</option>
              <option value="CONFLICTING">CONFLICTING (Força abstenção)</option>
            </select>
          </div>
        </div>

        {/* Coluna 3: Governança & Política Organizacional */}
        <div style={{ background: "var(--surface-soft)", padding: "1.25rem", borderRadius: "var(--radius-md)" }}>
          <h4 style={{ margin: "0 0 1rem", color: "var(--text)" }}>3. Política & Controles</h4>
          
          <div style={{ marginBottom: "0.8rem" }}>
            <label style={{ display: "block", fontSize: "0.85rem", color: "var(--text-soft)", marginBottom: "0.3rem" }}>
              Criticidade Operacional do Ativo
            </label>
            <select
              value={businessCriticality}
              onChange={(e) => setBusinessCriticality(e.target.value)}
              style={{
                width: "100%",
                padding: "0.5rem",
                borderRadius: "var(--radius-sm)",
                background: "var(--background)",
                border: "1px solid var(--border)",
                color: "var(--text)",
              }}
            >
              <option value="critical">Crítica (Interrupção de Serviços Core)</option>
              <option value="high">Alta (Operação Corporativa)</option>
              <option value="medium">Média (Sustentação Interna)</option>
              <option value="low">Baixa (Dev / Sandbox)</option>
            </select>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
            <label style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.85rem", cursor: "pointer" }}>
              <input
                type="checkbox"
                checked={firewallActive}
                onChange={(e) => setFirewallActive(e.target.checked)}
              />
              Firewall / WAF perimetral ativo (não altera MAC:H isoladamente)
            </label>

            <label style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.85rem", cursor: "pointer" }}>
              <input
                type="checkbox"
                checked={pciScope}
                onChange={(e) => setPciScope(e.target.checked)}
              />
              Escopo PCI-DSS (Mapeamento formal via POL-SEC-2026-V1)
            </label>

            <label style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.85rem", cursor: "pointer" }}>
              <input
                type="checkbox"
                checked={highAvailability}
                onChange={(e) => setHighAvailability(e.target.checked)}
              />
              Cluster de Alta Disponibilidade (não reduz AR:L por norma)
            </label>
          </div>
        </div>
      </div>

      {/* Exibição dos Resultados em 5 Camadas */}
      {result && (
        <div
          style={{
            marginTop: "2rem",
            padding: "1.5rem",
            borderRadius: "var(--radius-md)",
            background: "rgba(10, 25, 45, 0.95)",
            border: "1px solid var(--primary-strong)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem" }}>
            <h3 style={{ margin: 0, color: "var(--primary)" }}>
              📊 Arquitetura de Avaliação em 5 Camadas Auditáveis
            </h3>
            <span
              style={{
                padding: "0.3rem 0.8rem",
                borderRadius: "999px",
                fontSize: "0.85rem",
                background: result.inferenceAnalysis.reviewStatus === "HUMAN_REVIEW_REQUIRED" ? "var(--warning-soft)" : "var(--positive-soft)",
                color: result.inferenceAnalysis.reviewStatus === "HUMAN_REVIEW_REQUIRED" ? "var(--warning)" : "var(--positive)",
                border: "1px solid var(--border)",
                fontWeight: "bold",
              }}
            >
              Status: {result.inferenceAnalysis.reviewStatus}
            </span>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
              gap: "1rem",
              margin: "1.25rem 0",
            }}
          >
            {/* Camada 1 */}
            <div style={{ padding: "1rem", borderRadius: "var(--radius-sm)", background: "var(--surface-soft)" }}>
              <span style={{ fontSize: "0.8rem", color: "var(--text-soft)", display: "block" }}>
                Camada 1: Score de Origem (Preservado)
              </span>
              <div style={{ fontSize: "1.75rem", fontWeight: "bold", color: "var(--critical)" }}>
                {result.sourceAssessment.score.toFixed(1)}
              </div>
              <small style={{ color: "var(--text-muted)", display: "block" }}>
                Classificação: {result.sourceAssessment.nomenclature} ({result.sourceAssessment.severity})
              </small>
              <small style={{ color: "var(--text-muted)" }}>
                Origem: {result.sourceAssessment.provider}
              </small>
            </div>

            {/* Camada 2 */}
            <div style={{ padding: "1rem", borderRadius: "var(--radius-sm)", background: "var(--surface-soft)" }}>
              <span style={{ fontSize: "0.8rem", color: "var(--text-soft)", display: "block" }}>
                Camada 2: CVSS v4.0 Ambiental Derivado
              </span>
              {result.environmentalAssessment.status === "ABSTAINED" ? (
                <div>
                  <div style={{ fontSize: "1.4rem", fontWeight: "bold", color: "var(--warning)" }}>
                    ABSTENÇÃO
                  </div>
                  <small style={{ color: "var(--text-muted)" }}>
                    Fail-safe: Sem rebaixamento automático
                  </small>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: "1.75rem", fontWeight: "bold", color: "var(--positive)" }}>
                    {result.environmentalAssessment.score.toFixed(1)}
                  </div>
                  <small style={{ color: "var(--text-muted)", display: "block" }}>
                    Classificação: {result.environmentalAssessment.nomenclature} ({result.environmentalAssessment.severity})
                  </small>
                  <small style={{ color: result.environmentalAssessment.delta < 0 ? "var(--positive)" : "var(--warning)" }}>
                    Delta: {result.environmentalAssessment.delta > 0 ? `+${result.environmentalAssessment.delta}` : result.environmentalAssessment.delta}
                  </small>
                </div>
              )}
            </div>

            {/* Camada 3 */}
            <div style={{ padding: "1rem", borderRadius: "var(--radius-sm)", background: "var(--surface-soft)" }}>
              <span style={{ fontSize: "0.8rem", color: "var(--text-soft)", display: "block" }}>
                Camada 3: Disposição Operacional Local
              </span>
              <div style={{ fontSize: "1.3rem", fontWeight: "bold", color: "var(--primary)" }}>
                {result.operationalDisposition.code}
              </div>
              <small style={{ color: "var(--text-soft)", display: "block", marginTop: "0.2rem" }}>
                {result.operationalDisposition.label}
              </small>
              <small style={{ color: "var(--text-muted)", display: "block", marginTop: "0.2rem", fontSize: "0.75rem" }}>
                {result.operationalDisposition.caveat}
              </small>
            </div>
          </div>

          {/* Camada 4: Citações & Proveniência */}
          <div style={{ marginTop: "1rem" }}>
            <h4 style={{ margin: "0 0 0.5rem", fontSize: "0.95rem" }}>
              🔍 Camada 4: Justificativas de Inferência & Cadeia de Evidências:
            </h4>
            {result.inferenceAnalysis.abstentionReasons.length > 0 && (
              <div style={{ marginBottom: "0.5rem", padding: "0.5rem", background: "rgba(255, 100, 100, 0.1)", borderRadius: "var(--radius-sm)" }}>
                <strong style={{ color: "var(--critical)", fontSize: "0.85rem" }}>Motivos da Abstenção Segura:</strong>
                <ul style={{ margin: "0.2rem 0 0", paddingLeft: "1.2rem", color: "var(--text-soft)", fontSize: "0.85rem" }}>
                  {result.inferenceAnalysis.abstentionReasons.map((r: string, idx: number) => (
                    <li key={idx}>{r}</li>
                  ))}
                </ul>
              </div>
            )}
            <ul style={{ margin: 0, paddingLeft: "1.25rem", color: "var(--text-soft)", fontSize: "0.85rem" }}>
              {result.inferenceAnalysis.citations.map((c: string, idx: number) => (
                <li key={idx} style={{ marginBottom: "0.25rem" }}>
                  {c}
                </li>
              ))}
            </ul>
          </div>

          {/* Recibo Criptográfico */}
          <div style={{ marginTop: "1rem", padding: "0.75rem", background: "rgba(0,0,0,0.3)", borderRadius: "var(--radius-sm)", fontSize: "0.8rem" }}>
            <span style={{ color: "var(--text-muted)" }}>Recibo Criptográfico de Auditoria (RFC 8785 Canonical JSON → SHA-256):</span>
            <div style={{ fontFamily: "monospace", color: "var(--primary)", marginTop: "0.25rem", wordBreak: "break-all" }}>
              {result.auditReceipt.receiptDigest}
            </div>
          </div>

          {/* Camada 5: HITL Gate */}
          <div
            style={{
              marginTop: "1.5rem",
              paddingTop: "1.25rem",
              borderTop: "1px solid var(--border)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: "1rem",
            }}
          >
            <div>
              <strong>Camada 5: Governança HITL (Human-in-the-Loop Obrigatória):</strong>
              <div style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
                Rebaixamento automático desativado por política. Nenhuma recomendação entra em vigor sem homologação de especialista credenciado.
              </div>
            </div>

            {analystDecision ? (
              <span
                style={{
                  padding: "0.5rem 1rem",
                  borderRadius: "var(--radius-sm)",
                  background: analystDecision === "APPROVED" ? "var(--positive-soft)" : "var(--critical-soft)",
                  color: analystDecision === "APPROVED" ? "var(--positive)" : "var(--critical)",
                  fontWeight: "bold",
                }}
              >
                {analystDecision === "APPROVED" ? "✓ Proposta Homologada pelo Analista Responsável" : "✕ Proposta Retida / Ajustada"}
              </span>
            ) : (
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <button
                  onClick={() => setAnalystDecision("APPROVED")}
                  className="button button--primary"
                  style={{ padding: "0.5rem 1rem", fontSize: "0.9rem" }}
                >
                  ✓ Homologar Proposta
                </button>
                <button
                  onClick={() => setAnalystDecision("REJECTED")}
                  className="button button--secondary"
                  style={{ padding: "0.5rem 1rem", fontSize: "0.9rem" }}
                >
                  Rejeitar / Solicitar Dados
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
