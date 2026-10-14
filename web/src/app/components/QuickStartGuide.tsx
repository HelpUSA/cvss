"use client";

import {
  useState,
} from "react";

export function QuickStartGuide() {
  const [
    activeTab,
    setActiveTab,
  ] = useState<
    "what" | "how" | "first"
  >("what");

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <span className="section-kicker">
            Guia rápido
          </span>
          <h3>
            Entenda sem misturar conceitos
          </h3>
        </div>

        <div
          style={{
            display: "flex",
            gap: ".5rem",
            flexWrap: "wrap",
          }}
        >
          <button
            type="button"
            className={
              activeTab === "what"
                ? "button button--primary"
                : "button button--secondary"
            }
            onClick={() =>
              setActiveTab("what")
            }
          >
            1. O que é
          </button>
          <button
            type="button"
            className={
              activeTab === "how"
                ? "button button--primary"
                : "button button--secondary"
            }
            onClick={() =>
              setActiveTab("how")
            }
          >
            2. Como funciona
          </button>
          <button
            type="button"
            className={
              activeTab === "first"
                ? "button button--primary"
                : "button button--secondary"
            }
            onClick={() =>
              setActiveTab("first")
            }
          >
            3. Padrão FIRST
          </button>
        </div>
      </div>

      {activeTab === "what" ? (
        <div>
          <p>
            O HelpUS CVSS ajuda o consumidor
            a aplicar o contexto do seu
            ambiente às métricas ambientais
            CVSS v4.0, preservando o vetor e
            score publicados pela fonte.
          </p>
          <p>
            CVSS mede severidade. A decisão
            de prioridade operacional é uma
            política separada da organização.
          </p>
        </div>
      ) : null}

      {activeTab === "how" ? (
        <ol
          style={{
            display: "grid",
            gap: ".6rem",
          }}
        >
          <li>
            Preserve o CVSS-B de origem.
          </li>
          <li>
            Registre fatos verificáveis do
            ambiente.
          </li>
          <li>
            O catálogo determinístico resolve
            métricas quando a evidência é
            suficiente.
          </li>
          <li>
            O scorer determinístico calcula
            o resultado; evidência
            insuficiente pode produzir
            ABSTAIN.
          </li>
          <li>
            Cada execução e evidência fica
            rastreável no workspace.
          </li>
        </ol>
      ) : null}

      {activeTab === "first" ? (
        <div>
          <p>
            A FIRST organiza CVSS v4.0 em
            Base, Threat, Environmental e
            Supplemental. O HelpUS mantém
            essa separação e usa a
            nomenclatura CVSS-B, CVSS-BT,
            CVSS-BE e CVSS-BTE.
          </p>
          <a
            href="https://www.first.org/cvss/v4.0/user-guide"
            target="_blank"
            rel="noreferrer"
          >
            Abrir User Guide oficial ↗
          </a>
        </div>
      ) : null}
    </section>
  );
}
