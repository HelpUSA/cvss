"use client";

import { useState } from "react";

type DemoResult = {
  success?: boolean;
  mode?: string;
  persisted?: boolean;
  timestamp?: string;
  cveId?: string;
  sourceAssessment?: {
    score: number;
    vector: string;
    nomenclature: string;
    severity?: string;
    provider?: string;
    [key: string]: unknown;
  };
  environmentalAssessment?:
    | {
        score: number;
        vector: string;
        nomenclature: string;
        severity?: string;
        delta: number;
        decision: string;
      }
    | {
        status: "ABSTAINED";
        reasons: string[];
      };
  operationalDisposition?: {
    code?: string;
    label?: string;
    caveat?: string;
    policyApplied?: boolean;
    [key: string]: unknown;
  };
  inferenceAnalysis?: {
    reviewStatus?: string;
    abstentionReasons?: string[];
    candidateMetrics?: Record<string, string>;
    citations?: string[];
    reachabilityClass?: string;
  };
  auditReceipt?: {
    canonicalAlgorithm?: string;
    digestAlgorithm?: string;
    receiptDigest?: string;
    schemaVersion?: string;
  };
  error?: string;
};

const PRESETS = [
  {
    label: "CVE-2024-4251 (Core Banking RCE)",
    cveId: "CVE-2024-4251",
    baseVector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    provider: "CNA_PUBLISHED",
    reachability: "INTERNAL_ROUTED",
    telemetryAgeDays: 0.2,
    evidenceQuality: "SUFFICIENT",
    businessCriticality: "critical",
    dataSensitivity: "payment",
    firewallActive: true,
    pciScope: true,
    highAvailability: true,
  },
  {
    label: "CVE-2023-38606 (Kernel Memory Corruption)",
    cveId: "CVE-2023-38606",
    baseVector: "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    provider: "NVD_INDEXED",
    reachability: "LOCAL_ONLY",
    telemetryAgeDays: 0.5,
    evidenceQuality: "SUFFICIENT",
    businessCriticality: "high",
    dataSensitivity: "restricted",
    firewallActive: true,
    pciScope: false,
    highAvailability: true,
  },
  {
    label: "CVE-2024-21413 (Outlook Moniker Preview)",
    cveId: "CVE-2024-21413",
    baseVector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    provider: "CNA_PUBLISHED",
    reachability: "PUBLIC_ROUTED",
    telemetryAgeDays: 0.1,
    evidenceQuality: "SUFFICIENT",
    businessCriticality: "high",
    dataSensitivity: "confidential",
    firewallActive: false,
    pciScope: false,
    highAvailability: false,
  },
  {
    label: "CVE-2024-6387 (regreSSHion Pre-auth RCE)",
    cveId: "CVE-2024-6387",
    baseVector: "CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    provider: "INVESTIGATOR_GROUND_TRUTH",
    reachability: "PUBLIC_ROUTED",
    telemetryAgeDays: 0.3,
    evidenceQuality: "SUFFICIENT",
    businessCriticality: "critical",
    dataSensitivity: "internal",
    firewallActive: true,
    pciScope: true,
    highAvailability: true,
  },
  {
    label: "⚠️ Teste Fail-Safe (Telemetria Obsoleta)",
    cveId: "CVE-2024-4251",
    baseVector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    provider: "CNA_PUBLISHED",
    reachability: "INTERNAL_ROUTED",
    telemetryAgeDays: 2.5,
    evidenceQuality: "INSUFFICIENT",
    businessCriticality: "critical",
    dataSensitivity: "payment",
    firewallActive: true,
    pciScope: true,
    highAvailability: true,
  },
];

export function EnvironmentSimulator() {
  const [cveId, setCveId] = useState("CVE-2024-4251");
  const [baseVector, setBaseVector] = useState(
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
  );
  const [sourceProvider, setSourceProvider] = useState("CNA_PUBLISHED");
  const [reachability, setReachability] = useState("INTERNAL_ROUTED");
  const [telemetryAgeDays, setTelemetryAgeDays] = useState(0.2);
  const [evidenceQuality, setEvidenceQuality] = useState("SUFFICIENT");
  const [businessCriticality, setBusinessCriticality] = useState("critical");
  const [dataSensitivity, setDataSensitivity] = useState("payment");
  const [firewallActive, setFirewallActive] = useState(true);
  const [pciScope, setPciScope] = useState(true);
  const [highAvailability, setHighAvailability] = useState(true);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DemoResult | null>(null);
  const [analystDecision, setAnalystDecision] = useState<string | null>(null);

  function applyPreset(preset: (typeof PRESETS)[0]) {
    setCveId(preset.cveId);
    setBaseVector(preset.baseVector);
    setSourceProvider(preset.provider);
    setReachability(preset.reachability);
    setTelemetryAgeDays(preset.telemetryAgeDays);
    setEvidenceQuality(preset.evidenceQuality);
    setBusinessCriticality(preset.businessCriticality);
    setDataSensitivity(preset.dataSensitivity);
    setFirewallActive(preset.firewallActive);
    setPciScope(preset.pciScope);
    setHighAvailability(preset.highAvailability);
    setResult(null);
    setAnalystDecision(null);
  }

  async function runAnalysis() {
    setLoading(true);
    setResult(null);
    setAnalystDecision(null);

    try {
      const response = await fetch("/api/analyze-environment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          cveId,
          baseVector,
          sourceAssessmentMeta: {
            provider: sourceProvider,
          },
          evidence: {
            evidenceQuality,
            telemetryAgeDays: Number(telemetryAgeDays),
            telemetryProfile: "dynamic",
            maxTelemetryAgeDays: 1.0,
            reachability,
            organizationPolicyId: "POL-SEC-2026-V1",
            policyVersion: "1.0",
            firewallActive,
            pciScope,
            highAvailability,
            businessCriticality,
            dataSensitivity,
            securityRequirements: {
              CR:
                businessCriticality === "critical"
                  ? "H"
                  : businessCriticality === "high"
                  ? "M"
                  : "L",
              IR:
                dataSensitivity === "payment" || dataSensitivity === "restricted"
                  ? "H"
                  : dataSensitivity === "confidential"
                  ? "M"
                  : "L",
              AR: highAvailability ? "H" : "M",
            },
            operationalPolicy: {
              policyId: "POL-SEC-2026-V1",
              policyVersion: "1.0",
              scoreBands: [
                {
                  code: "P0_IMMEDIATE",
                  label: "P0 - Remediação Imediata (24h)",
                  minScore: 9.0,
                  maxScore: 10.0,
                  caveat: "Risco crítico aos ativos vitais da organização.",
                },
                {
                  code: "P1_EXPEDITED",
                  label: "P1 - Remediação Acelerada (7d)",
                  minScore: 7.0,
                  maxScore: 8.9,
                  caveat: "Severidade alta no contexto produtivo.",
                },
                {
                  code: "P2_SCHEDULED",
                  label: "P2 - Ciclo Regular de Patching (30d)",
                  minScore: 4.0,
                  maxScore: 6.9,
                  caveat: "Severidade média mitigada por controles de borda.",
                },
                {
                  code: "P3_MONITOR",
                  label: "P3 - Monitoramento Ativo (90d)",
                  minScore: 0.1,
                  maxScore: 3.9,
                  caveat: "Severidade baixa ou impacto residual.",
                },
                {
                  code: "P4_DEFER_RECOMMENDED",
                  label: "P4 - Deferimento Recomendado",
                  minScore: 0.0,
                  maxScore: 0.0,
                  caveat: "Risco residual nulo ou formalmente aceito.",
                },
              ],
            },
          },
        }),
      });

      const payload = await response.json();
      setResult(payload);
    } catch (error) {
      setResult({
        error: error instanceof Error ? error.message : "Falha inesperada.",
      });
    } finally {
      setLoading(false);
    }
  }

  const abstained =
    result?.environmentalAssessment &&
    "status" in result.environmentalAssessment &&
    result.environmentalAssessment.status === "ABSTAINED";

  const envAssessment =
    result?.environmentalAssessment &&
    !("status" in result.environmentalAssessment)
      ? result.environmentalAssessment
      : null;

  return (
    <section
      id="simulator"
      className="panel"
      style={{
        marginTop: "2rem",
        marginBottom: "2rem",
        padding: "1.75rem",
        borderRadius: "16px",
        background: "linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(10, 16, 30, 0.98) 100%)",
        border: "1px solid rgba(56, 189, 248, 0.25)",
        boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)",
      }}
    >
      {/* Header com Kicker e Botão de Execução */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          flexWrap: "wrap",
          gap: "1.25rem",
          paddingBottom: "1.25rem",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
        }}
      >
        <div>
          <span
            className="section-kicker"
            style={{
              color: "#38bdf8",
              fontSize: "0.85rem",
              fontWeight: 700,
              textTransform: "uppercase",
              letterSpacing: "0.05em",
            }}
          >
            ⚡ Laboratório Interativo & Benchmark Operacional
          </span>
          <h2 style={{ fontSize: "1.75rem", margin: "0.25rem 0 0.5rem", color: "#f8fafc" }}>
            Simulador de Ambiente Operacional CVSS v4.0 (5 Camadas)
          </h2>
          <p style={{ color: "#94a3b8", maxWidth: "820px", margin: 0, fontSize: "0.95rem" }}>
            Avaliação contextual determinística em estrita conformidade com o algoritmo de MacroVetores FIRST CVSS v4.0.
            Separação formal entre score de origem, vetor ambiental derivado, disposição operacional P0–P4 e governança HITL.
          </p>
        </div>

        <button
          onClick={runAnalysis}
          disabled={loading}
          type="button"
          className="button button--primary"
          style={{
            padding: "0.85rem 1.75rem",
            fontSize: "1rem",
            fontWeight: 700,
            cursor: loading ? "wait" : "pointer",
            borderRadius: "12px",
            background: "linear-gradient(135deg, #0284c7 0%, #2563eb 100%)",
            border: "none",
            color: "#ffffff",
            boxShadow: "0 4px 14px rgba(2, 132, 199, 0.4)",
            display: "inline-flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          {loading ? (
            <>
              <svg
                style={{ width: "18px", height: "18px", animation: "spin 1s linear infinite" }}
                viewBox="0 0 24 24"
                fill="none"
              >
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" strokeOpacity="0.25" />
                <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <span>Calculando Inferência...</span>
            </>
          ) : (
            <span>▶ Executar Avaliação CVSS v4.0</span>
          )}
        </button>
      </div>

      {/* Barra de Presets Rápidos */}
      <div style={{ marginTop: "1.25rem" }}>
        <span
          style={{
            display: "block",
            fontSize: "0.8rem",
            color: "#64748b",
            fontWeight: 600,
            marginBottom: "0.5rem",
            textTransform: "uppercase",
            letterSpacing: "0.05em",
          }}
        >
          Cenários de Benchmark Pré-Configurados:
        </span>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {PRESETS.map((preset) => (
            <button
              key={preset.label}
              type="button"
              onClick={() => applyPreset(preset)}
              style={{
                fontSize: "0.8rem",
                padding: "6px 12px",
                borderRadius: "8px",
                background:
                  cveId === preset.cveId && baseVector === preset.baseVector
                    ? "rgba(56, 189, 248, 0.2)"
                    : "rgba(255, 255, 255, 0.05)",
                border:
                  cveId === preset.cveId && baseVector === preset.baseVector
                    ? "1px solid #38bdf8"
                    : "1px solid rgba(255, 255, 255, 0.1)",
                color:
                  cveId === preset.cveId && baseVector === preset.baseVector
                    ? "#38bdf8"
                    : "#cbd5e1",
                cursor: "pointer",
                fontWeight: 600,
                transition: "all 0.15s ease",
              }}
            >
              {preset.label}
            </button>
          ))}
        </div>
      </div>

      {/* Grid de Configuração em 3 Colunas */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "1.25rem",
          marginTop: "1.5rem",
        }}
      >
        {/* Coluna 1: Dados da Origem */}
        <div
          style={{
            background: "rgba(30, 41, 59, 0.5)",
            padding: "1.25rem",
            borderRadius: "12px",
            border: "1px solid rgba(255, 255, 255, 0.06)",
          }}
        >
          <h4
            style={{
              margin: "0 0 1rem",
              color: "#38bdf8",
              fontSize: "0.95rem",
              display: "flex",
              alignItems: "center",
              gap: "6px",
            }}
          >
            <span>📌</span> 1. Vetor de Origem (Source)
          </h4>

          <div style={{ marginBottom: "0.85rem" }}>
            <label
              htmlFor="sim-cve"
              style={{ display: "block", fontSize: "0.85rem", color: "#94a3b8", marginBottom: "0.3rem" }}
            >
              Identificador CVE
            </label>
            <input
              id="sim-cve"
              type="text"
              value={cveId}
              onChange={(e) => setCveId(e.target.value.toUpperCase())}
              style={{
                width: "100%",
                padding: "0.6rem 0.75rem",
                borderRadius: "8px",
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.15)",
                color: "#f8fafc",
                fontSize: "0.9rem",
              }}
            />
          </div>

          <div style={{ marginBottom: "0.85rem" }}>
            <label
              htmlFor="sim-vector"
              style={{ display: "block", fontSize: "0.85rem", color: "#94a3b8", marginBottom: "0.3rem" }}
            >
              Vetor CVSS v4.0 de Origem
            </label>
            <textarea
              id="sim-vector"
              rows={3}
              value={baseVector}
              onChange={(e) => setBaseVector(e.target.value)}
              style={{
                width: "100%",
                padding: "0.6rem 0.75rem",
                borderRadius: "8px",
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.15)",
                color: "#f8fafc",
                fontSize: "0.8rem",
                fontFamily: "monospace",
                resize: "vertical",
              }}
            />
          </div>

          <div>
            <label
              htmlFor="sim-provider"
              style={{ display: "block", fontSize: "0.85rem", color: "#94a3b8", marginBottom: "0.3rem" }}
            >
              Origem do Registro (Provenance)
            </label>
            <select
              id="sim-provider"
              value={sourceProvider}
              onChange={(e) => setSourceProvider(e.target.value)}
              style={{
                width: "100%",
                padding: "0.6rem 0.75rem",
                borderRadius: "8px",
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.15)",
                color: "#f8fafc",
                fontSize: "0.85rem",
              }}
            >
              <option value="CNA_PUBLISHED">CNA Autorizado (CNA_PUBLISHED)</option>
              <option value="NVD_INDEXED">Indexado pelo NVD (NVD_INDEXED)</option>
              <option value="INVESTIGATOR_GROUND_TRUTH">Pesquisa Experimental (Anotação de Especialistas)</option>
            </select>
          </div>
        </div>

        {/* Coluna 2: Telemetria & Topologia */}
        <div
          style={{
            background: "rgba(30, 41, 59, 0.5)",
            padding: "1.25rem",
            borderRadius: "12px",
            border: "1px solid rgba(255, 255, 255, 0.06)",
          }}
        >
          <h4
            style={{
              margin: "0 0 1rem",
              color: "#38bdf8",
              fontSize: "0.95rem",
              display: "flex",
              alignItems: "center",
              gap: "6px",
            }}
          >
            <span>🌐</span> 2. Topologia & Telemetria
          </h4>

          <div style={{ marginBottom: "0.85rem" }}>
            <label
              htmlFor="sim-reachability"
              style={{ display: "block", fontSize: "0.85rem", color: "#94a3b8", marginBottom: "0.3rem" }}
            >
              Classe de Alcançabilidade (MAV)
            </label>
            <select
              id="sim-reachability"
              value={reachability}
              onChange={(e) => setReachability(e.target.value)}
              style={{
                width: "100%",
                padding: "0.6rem 0.75rem",
                borderRadius: "8px",
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.15)",
                color: "#f8fafc",
                fontSize: "0.85rem",
              }}
            >
              <option value="PUBLIC_ROUTED">PUBLIC_ROUTED → MAV:N (Internet pública)</option>
              <option value="INTERNAL_ROUTED">INTERNAL_ROUTED → MAV:N (Rede interna L3)</option>
              <option value="ADJACENT_ONLY">ADJACENT_ONLY → MAV:A (Adjacência L2 restrita)</option>
              <option value="LOCAL_ONLY">LOCAL_ONLY → MAV:L (Sessão local no host)</option>
              <option value="PHYSICAL_ONLY">PHYSICAL_ONLY → MAV:P (Acesso físico requerido)</option>
            </select>
          </div>

          <div style={{ marginBottom: "0.85rem" }}>
            <label
              htmlFor="sim-age"
              style={{
                display: "flex",
                justifyContent: "space-between",
                fontSize: "0.85rem",
                color: "#94a3b8",
                marginBottom: "0.3rem",
              }}
            >
              <span>Idade da Telemetria:</span>
              <strong style={{ color: telemetryAgeDays > 1.0 ? "#f87171" : "#38bdf8" }}>
                {telemetryAgeDays.toFixed(1)} dia(s)
              </strong>
            </label>
            <input
              id="sim-age"
              type="range"
              min="0.0"
              max="3.0"
              step="0.1"
              value={telemetryAgeDays}
              onChange={(e) => setTelemetryAgeDays(parseFloat(e.target.value))}
              style={{ width: "100%", accentColor: telemetryAgeDays > 1.0 ? "#ef4444" : "#38bdf8" }}
            />
            {telemetryAgeDays > 1.0 ? (
              <small style={{ color: "#f87171", display: "block", marginTop: "0.25rem", fontSize: "0.78rem" }}>
                ⚠️ Acima de 1.0 dia aciona abstenção segura fail-safe (telemetria obsoleta).
              </small>
            ) : (
              <small style={{ color: "#64748b", display: "block", marginTop: "0.25rem", fontSize: "0.78rem" }}>
                ✓ Limite de validade dinâmica: até 1.0 dia.
              </small>
            )}
          </div>

          <div>
            <label
              htmlFor="sim-quality"
              style={{ display: "block", fontSize: "0.85rem", color: "#94a3b8", marginBottom: "0.3rem" }}
            >
              Qualidade da Evidência
            </label>
            <select
              id="sim-quality"
              value={evidenceQuality}
              onChange={(e) => setEvidenceQuality(e.target.value)}
              style={{
                width: "100%",
                padding: "0.6rem 0.75rem",
                borderRadius: "8px",
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.15)",
                color: "#f8fafc",
                fontSize: "0.85rem",
              }}
            >
              <option value="SUFFICIENT">SUFFICIENT (Evidência verificada e íntegra)</option>
              <option value="INSUFFICIENT">INSUFFICIENT (Evidência parcial → Força ABSTAIN)</option>
              <option value="CONFLICTING">CONFLICTING (Fontes divergentes → Força ABSTAIN)</option>
            </select>
          </div>
        </div>

        {/* Coluna 3: Governança & Política Organizacional */}
        <div
          style={{
            background: "rgba(30, 41, 59, 0.5)",
            padding: "1.25rem",
            borderRadius: "12px",
            border: "1px solid rgba(255, 255, 255, 0.06)",
          }}
        >
          <h4
            style={{
              margin: "0 0 1rem",
              color: "#38bdf8",
              fontSize: "0.95rem",
              display: "flex",
              alignItems: "center",
              gap: "6px",
            }}
          >
            <span>🛡️</span> 3. Política & Controles Defensivos
          </h4>

          <div style={{ marginBottom: "0.85rem" }}>
            <label
              htmlFor="sim-criticality"
              style={{ display: "block", fontSize: "0.85rem", color: "#94a3b8", marginBottom: "0.3rem" }}
            >
              Criticidade Operacional do Ativo (CR)
            </label>
            <select
              id="sim-criticality"
              value={businessCriticality}
              onChange={(e) => setBusinessCriticality(e.target.value)}
              style={{
                width: "100%",
                padding: "0.6rem 0.75rem",
                borderRadius: "8px",
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.15)",
                color: "#f8fafc",
                fontSize: "0.85rem",
              }}
            >
              <option value="critical">Crítica (Interrupção de Serviços Vitais → CR:H)</option>
              <option value="high">Alta (Operação Corporativa Relevante → CR:M)</option>
              <option value="medium">Média (Sustentação Interna Auxiliar → CR:L)</option>
              <option value="low">Baixa (Dev / Sandbox Isolado → CR:L)</option>
            </select>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "0.6rem", marginTop: "0.5rem" }}>
            <label
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
                fontSize: "0.85rem",
                color: "#cbd5e1",
                cursor: "pointer",
              }}
            >
              <input
                type="checkbox"
                checked={firewallActive}
                onChange={(e) => setFirewallActive(e.target.checked)}
                style={{ width: "16px", height: "16px", accentColor: "#38bdf8" }}
              />
              Firewall / WAF perimetral ativo (não altera MAC:H isoladamente)
            </label>

            <label
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
                fontSize: "0.85rem",
                color: "#cbd5e1",
                cursor: "pointer",
              }}
            >
              <input
                type="checkbox"
                checked={pciScope}
                onChange={(e) => setPciScope(e.target.checked)}
                style={{ width: "16px", height: "16px", accentColor: "#38bdf8" }}
              />
              Escopo PCI-DSS (Mapeamento formal via POL-SEC-2026-V1)
            </label>

            <label
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
                fontSize: "0.85rem",
                color: "#cbd5e1",
                cursor: "pointer",
              }}
            >
              <input
                type="checkbox"
                checked={highAvailability}
                onChange={(e) => setHighAvailability(e.target.checked)}
                style={{ width: "16px", height: "16px", accentColor: "#38bdf8" }}
              />
              Cluster de Alta Disponibilidade (não reduz AR:L por norma)
            </label>
          </div>
        </div>
      </div>

      {/* Exibição dos Resultados em 5 Camadas Auditáveis */}
      {result ? (
        <div
          style={{
            marginTop: "2rem",
            padding: "1.75rem",
            borderRadius: "14px",
            background: "rgba(10, 25, 45, 0.95)",
            border: "1px solid rgba(56, 189, 248, 0.4)",
            boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
          }}
        >
          {result.error ? (
            <div
              style={{
                padding: "1rem",
                background: "rgba(239, 68, 68, 0.15)",
                border: "1px solid #ef4444",
                borderRadius: "8px",
                color: "#fca5a5",
              }}
            >
              <strong>Não foi possível calcular:</strong>
              <p style={{ margin: "0.25rem 0 0" }}>{result.error}</p>
            </div>
          ) : (
            <>
              {/* Cabeçalho do Resultado */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: "1rem",
                  paddingBottom: "1rem",
                  borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
                }}
              >
                <div>
                  <h3 style={{ margin: 0, color: "#38bdf8", fontSize: "1.25rem" }}>
                    📊 Arquitetura de Avaliação em 5 Camadas Auditáveis
                  </h3>
                  <small style={{ color: "#64748b" }}>
                    Execução determinística em conformidade FIRST CVSS v4.0 • Modo: {result.mode ?? "PUBLIC_STATELESS_DEMO"}
                  </small>
                </div>

                <span
                  style={{
                    padding: "0.35rem 0.9rem",
                    borderRadius: "999px",
                    fontSize: "0.85rem",
                    fontWeight: 700,
                    background: abstained
                      ? "rgba(245, 158, 11, 0.15)"
                      : "rgba(34, 197, 94, 0.15)",
                    color: abstained ? "#fbbf24" : "#4ade80",
                    border: abstained
                      ? "1px solid #f59e0b"
                      : "1px solid #22c55e",
                  }}
                >
                  Status:{" "}
                  {abstained
                    ? "ABSTAIN (Fail-Safe)"
                    : result.inferenceAnalysis?.reviewStatus ?? "AUTO_ACCEPT_READY"}
                </span>
              </div>

              {/* Cards das Camadas 1, 2 e 3 */}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
                  gap: "1rem",
                  margin: "1.5rem 0",
                }}
              >
                {/* Camada 1: Score de Origem Preservado */}
                <div
                  style={{
                    padding: "1.25rem",
                    borderRadius: "10px",
                    background: "rgba(15, 23, 42, 0.8)",
                    border: "1px solid rgba(255, 255, 255, 0.08)",
                  }}
                >
                  <span style={{ fontSize: "0.8rem", color: "#94a3b8", display: "block" }}>
                    Camada 1: Score de Origem (Preservado)
                  </span>
                  <div style={{ fontSize: "2.2rem", fontWeight: 800, color: "#f87171", margin: "0.2rem 0" }}>
                    {result.sourceAssessment?.score?.toFixed(1) ?? "n/d"}
                  </div>
                  <small style={{ color: "#cbd5e1", display: "block" }}>
                    Nomenclatura: {result.sourceAssessment?.nomenclature ?? "CVSS-B"}
                  </small>
                  <small style={{ color: "#64748b" }}>
                    Origem: {String(result.sourceAssessment?.provider ?? sourceProvider)}
                  </small>
                </div>

                {/* Camada 2: CVSS v4.0 Ambiental Derivado */}
                <div
                  style={{
                    padding: "1.25rem",
                    borderRadius: "10px",
                    background: "rgba(15, 23, 42, 0.8)",
                    border: "1px solid rgba(255, 255, 255, 0.08)",
                  }}
                >
                  <span style={{ fontSize: "0.8rem", color: "#94a3b8", display: "block" }}>
                    Camada 2: CVSS v4.0 Ambiental Derivado
                  </span>
                  {abstained ? (
                    <div>
                      <div
                        style={{
                          fontSize: "1.6rem",
                          fontWeight: 800,
                          color: "#fbbf24",
                          margin: "0.2rem 0",
                        }}
                      >
                        ABSTENÇÃO
                      </div>
                      <small style={{ color: "#94a3b8", display: "block" }}>
                        Fail-safe: Sem rebaixamento automático
                      </small>
                      <small style={{ color: "#f59e0b" }}>
                        Preserva score Base oficial
                      </small>
                    </div>
                  ) : (
                    <div>
                      <div
                        style={{
                          fontSize: "2.2rem",
                          fontWeight: 800,
                          color:
                            envAssessment && envAssessment.delta < 0
                              ? "#4ade80"
                              : envAssessment && envAssessment.delta > 0
                              ? "#f87171"
                              : "#38bdf8",
                          margin: "0.2rem 0",
                        }}
                      >
                        {envAssessment?.score?.toFixed(1) ?? "n/d"}
                      </div>
                      <small style={{ color: "#cbd5e1", display: "block" }}>
                        Nomenclatura: {envAssessment?.nomenclature ?? "CVSS-BE"}
                      </small>
                      <small
                        style={{
                          color:
                            envAssessment && envAssessment.delta < 0
                              ? "#4ade80"
                              : envAssessment && envAssessment.delta > 0
                              ? "#f87171"
                              : "#94a3b8",
                          fontWeight: 700,
                        }}
                      >
                        Delta:{" "}
                        {envAssessment && envAssessment.delta > 0
                          ? `+${envAssessment.delta.toFixed(1)}`
                          : envAssessment?.delta?.toFixed(1) ?? "0.0"}
                      </small>
                    </div>
                  )}
                </div>

                {/* Camada 3: Disposição Operacional Local */}
                <div
                  style={{
                    padding: "1.25rem",
                    borderRadius: "10px",
                    background: "rgba(15, 23, 42, 0.8)",
                    border: "1px solid rgba(255, 255, 255, 0.08)",
                  }}
                >
                  <span style={{ fontSize: "0.8rem", color: "#94a3b8", display: "block" }}>
                    Camada 3: Disposição Operacional Local
                  </span>
                  <div
                    style={{
                      fontSize: "1.3rem",
                      fontWeight: 800,
                      color: "#38bdf8",
                      margin: "0.4rem 0 0.2rem",
                    }}
                  >
                    {result.operationalDisposition?.code ?? "PENDING_POLICY_REVIEW"}
                  </div>
                  <small style={{ color: "#cbd5e1", display: "block", marginTop: "0.2rem" }}>
                    {result.operationalDisposition?.label ?? "Recomendação Operacional"}
                  </small>
                  <small
                    style={{
                      color: "#64748b",
                      display: "block",
                      marginTop: "0.2rem",
                      fontSize: "0.75rem",
                    }}
                  >
                    {result.operationalDisposition?.caveat ??
                      "Recomendação interna sujeita à política organizacional."}
                  </small>
                </div>
              </div>

              {/* Camada 4: Citações & Cadeia de Evidências */}
              <div
                style={{
                  marginTop: "1.25rem",
                  padding: "1rem",
                  background: "rgba(15, 23, 42, 0.6)",
                  borderRadius: "10px",
                }}
              >
                <h4 style={{ margin: "0 0 0.5rem", fontSize: "0.95rem", color: "#f8fafc" }}>
                  🔍 Camada 4: Justificativas de Inferência & Cadeia de Evidências:
                </h4>

                {result.inferenceAnalysis?.abstentionReasons &&
                  result.inferenceAnalysis.abstentionReasons.length > 0 && (
                    <div
                      style={{
                        marginBottom: "0.75rem",
                        padding: "0.75rem",
                        background: "rgba(239, 68, 68, 0.15)",
                        border: "1px solid rgba(239, 68, 68, 0.3)",
                        borderRadius: "8px",
                      }}
                    >
                      <strong style={{ color: "#f87171", fontSize: "0.85rem" }}>
                        Motivos da Abstenção Segura (Fail-Safe):
                      </strong>
                      <ul
                        style={{
                          margin: "0.3rem 0 0",
                          paddingLeft: "1.2rem",
                          color: "#fca5a5",
                          fontSize: "0.85rem",
                        }}
                      >
                        {result.inferenceAnalysis.abstentionReasons.map((r, idx) => (
                          <li key={idx}>{r}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                {result.inferenceAnalysis?.citations &&
                  result.inferenceAnalysis.citations.length > 0 && (
                    <ul
                      style={{
                        margin: 0,
                        paddingLeft: "1.25rem",
                        color: "#94a3b8",
                        fontSize: "0.85rem",
                      }}
                    >
                      {result.inferenceAnalysis.citations.map((c, idx) => (
                        <li key={idx} style={{ marginBottom: "0.25rem" }}>
                          {c}
                        </li>
                      ))}
                    </ul>
                  )}

                {/* Vetor Calculado */}
                {envAssessment?.vector && (
                  <div style={{ marginTop: "0.75rem" }}>
                    <span style={{ fontSize: "0.8rem", color: "#64748b" }}>
                      Vetor Contextual Resultante:
                    </span>
                    <pre
                      style={{
                        margin: "0.25rem 0 0",
                        padding: "0.6rem 0.8rem",
                        background: "rgba(0, 0, 0, 0.4)",
                        borderRadius: "6px",
                        fontSize: "0.8rem",
                        color: "#38bdf8",
                        fontFamily: "monospace",
                        whiteSpace: "pre-wrap",
                        wordBreak: "break-all",
                      }}
                    >
                      {envAssessment.vector}
                    </pre>
                  </div>
                )}
              </div>

              {/* Recibo Criptográfico Canônico RFC 8785 */}
              {result.auditReceipt?.receiptDigest && (
                <div
                  style={{
                    marginTop: "1rem",
                    padding: "0.85rem",
                    background: "rgba(0, 0, 0, 0.35)",
                    borderRadius: "10px",
                    border: "1px solid rgba(255, 255, 255, 0.05)",
                    fontSize: "0.8rem",
                  }}
                >
                  <span style={{ color: "#64748b" }}>
                    Recibo Criptográfico de Auditoria (JCS RFC 8785 → SHA-256):
                  </span>
                  <div
                    style={{
                      fontFamily: "monospace",
                      color: "#38bdf8",
                      marginTop: "0.25rem",
                      wordBreak: "break-all",
                      fontSize: "0.85rem",
                    }}
                  >
                    {result.auditReceipt.receiptDigest}
                  </div>
                </div>
              )}

              {/* Camada 5: Governança HITL Gate */}
              <div
                style={{
                  marginTop: "1.5rem",
                  paddingTop: "1.25rem",
                  borderTop: "1px solid rgba(255, 255, 255, 0.1)",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: "1rem",
                }}
              >
                <div>
                  <strong style={{ color: "#f8fafc", fontSize: "0.95rem" }}>
                    Camada 5: Governança HITL (Human-in-the-Loop Obrigatória)
                  </strong>
                  <div style={{ fontSize: "0.85rem", color: "#94a3b8", maxWidth: "600px" }}>
                    Rebaixamento automático desativado por política. Nenhuma recomendação entra em vigor sem homologação de especialista credenciado.
                  </div>
                </div>

                {analystDecision ? (
                  <span
                    style={{
                      padding: "0.6rem 1.2rem",
                      borderRadius: "8px",
                      background:
                        analystDecision === "APPROVED"
                          ? "rgba(34, 197, 94, 0.2)"
                          : "rgba(239, 68, 68, 0.2)",
                      color: analystDecision === "APPROVED" ? "#4ade80" : "#f87171",
                      border:
                        analystDecision === "APPROVED"
                          ? "1px solid #22c55e"
                          : "1px solid #ef4444",
                      fontWeight: 700,
                      fontSize: "0.9rem",
                    }}
                  >
                    {analystDecision === "APPROVED"
                      ? "✓ Proposta Homologada pelo Analista Responsável"
                      : "✕ Proposta Retida / Ajustada pelo Especialista"}
                  </span>
                ) : (
                  <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
                    <button
                      type="button"
                      onClick={() => setAnalystDecision("APPROVED")}
                      style={{
                        padding: "0.6rem 1.2rem",
                        borderRadius: "8px",
                        background: "#22c55e",
                        color: "#0f172a",
                        border: "none",
                        fontWeight: 700,
                        fontSize: "0.9rem",
                        cursor: "pointer",
                      }}
                    >
                      ✓ Homologar Proposta
                    </button>
                    <button
                      type="button"
                      onClick={() => setAnalystDecision("REJECTED")}
                      style={{
                        padding: "0.6rem 1.2rem",
                        borderRadius: "8px",
                        background: "rgba(255, 255, 255, 0.1)",
                        color: "#f8fafc",
                        border: "1px solid rgba(255, 255, 255, 0.2)",
                        fontWeight: 600,
                        fontSize: "0.9rem",
                        cursor: "pointer",
                      }}
                    >
                      ✕ Rejeitar / Exigir Telemetria
                    </button>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      ) : null}
    </section>
  );
}
