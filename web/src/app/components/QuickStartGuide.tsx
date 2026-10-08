"use client";

import { useState } from "react";

export function QuickStartGuide() {
  const [activeTab, setActiveTab] = useState<"what" | "how" | "why">("what");

  return (
    <section
      className="panel"
      style={{
        margin: "1.5rem 0",
        padding: "1.75rem",
        borderRadius: "var(--radius-lg)",
        background: "rgba(16, 36, 58, 0.75)",
        border: "1px solid var(--border)",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem", marginBottom: "1.25rem" }}>
        <div>
          <span className="section-kicker" style={{ color: "var(--primary)" }}>
            💡 Guia Rápido de Introdução
          </span>
          <h3 style={{ margin: "0.25rem 0 0", fontSize: "1.35rem" }}>
            Primeira vez aqui? Entenda o propósito em 3 passos
          </h3>
        </div>

        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button
            onClick={() => setActiveTab("what")}
            className={`button ${activeTab === "what" ? "button--primary" : "button--secondary"}`}
            style={{ padding: "0.4rem 0.85rem", fontSize: "0.85rem" }}
          >
            1. O que é?
          </button>
          <button
            onClick={() => setActiveTab("how")}
            className={`button ${activeTab === "how" ? "button--primary" : "button--secondary"}`}
            style={{ padding: "0.4rem 0.85rem", fontSize: "0.85rem" }}
          >
            2. Como funciona?
          </button>
          <button
            onClick={() => setActiveTab("why")}
            className={`button ${activeTab === "why" ? "button--primary" : "button--secondary"}`}
            style={{ padding: "0.4rem 0.85rem", fontSize: "0.85rem" }}
          >
            3. Inovação Científica
          </button>
        </div>
      </div>

      <div style={{ color: "var(--text-soft)", fontSize: "0.95rem", lineHeight: "1.6" }}>
        {activeTab === "what" && (
          <div>
            <p style={{ marginTop: 0 }}>
              O <strong>HelpUS CVSS</strong> é uma plataforma de inteligência de risco que resolve o maior problema da gestão de vulnerabilidades moderna:
              <strong> o excesso de alarmes falsos e prioridades infladas</strong>.
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "1rem" }}>
              <div style={{ padding: "1rem", borderRadius: "var(--radius-sm)", background: "var(--surface-soft)" }}>
                <strong style={{ color: "var(--critical)" }}>🔴 CVSS Oficial (NVD)</strong>
                <p style={{ margin: "0.3rem 0 0", fontSize: "0.88rem" }}>
                  Mede o risco intrínseco teórico da falha no mundo. Uma falha crítica 9.8 é tratada como urgente mesmo em um computador isolado de testes.
                </p>
              </div>
              <div style={{ padding: "1rem", borderRadius: "var(--radius-sm)", background: "var(--surface-soft)" }}>
                <strong style={{ color: "var(--positive)" }}>🟢 CVSS Contextual (Nosso Motor)</strong>
                <p style={{ margin: "0.3rem 0 0", fontSize: "0.88rem" }}>
                  Cruza a vulnerabilidade com as <strong>evidências do seu ambiente real</strong> (firewall, rede, WAF, escopo bancário) para priorizar o que realmente importa.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === "how" && (
          <div>
            <ol style={{ margin: 0, paddingLeft: "1.25rem", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              <li>
                <strong>Ingestão de Scanner Real:</strong> O sistema lê saídas de ferramentas como <code>Trivy</code>, <code>OpenVAS</code> ou relatórios em JSON.
              </li>
              <li>
                <strong>Extração de Evidências por IA:</strong> Nossos agentes de IA analisam as configurações de rede, regras de firewall e criticidade de negócio do ativo.
              </li>
              <li>
                <strong>Cálculo Matemático Rigoroso:</strong> A IA propõe os vetores ambientais (ex: <code>MAV:A</code>, <code>CR:H</code>), mas a nota final é calculada segundo a fórmula matemática oficial da FIRST (CVSS v4.0).
              </li>
              <li>
                <strong>Gate de Homologação Humana:</strong> Toda decisão operacional é mantida sob auditoria com justificativas rastreáveis.
              </li>
            </ol>
          </div>
        )}

        {activeTab === "why" && (
          <div>
            <p style={{ marginTop: 0 }}>
              Na literatura acadêmica e no mercado corporativo, equipes quase nunca preenchem o vetor ambiental do CVSS porque exige analisar manualmente dezenas de controles.
            </p>
            <p style={{ margin: 0 }}>
              <strong>A inovação no nosso trabalho:</strong> Automatizamos a coleta de evidências e calculamos o vetor ambiental de forma determinística segundo a especificação FIRST CVSS v4.0 com rastreabilidade auditável e governança com especialista humano (HITL).
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
