import type {
  Metadata,
} from "next";

import {
  EnvironmentSimulator,
} from "../components/EnvironmentSimulator";

export const metadata: Metadata = {
  title:
    "Demonstração CVSS v4.0 — HelpUS",
  description:
    "Demonstração stateless da contextualização ambiental CVSS v4.0.",
};

export default function DemoPage() {
  return (
    <main className="page-shell">
      <header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent:
            "space-between",
          gap: "1rem",
          flexWrap: "wrap",
        }}
      >
        <a
          className="brand"
          href="/"
        >
          <img
            src="/helpus-logo.jpg"
            alt="HelpUS"
            className="brand__logo-img"
          />
          <span className="brand__text">
            <strong>
              HelpUS CVSS
            </strong>
            <small>
              Demonstração pública
            </small>
          </span>
        </a>

        <div
          style={{
            display: "flex",
            gap: ".75rem",
            flexWrap: "wrap",
          }}
        >
          <a
            className="button button--quiet"
            href="/"
          >
            ← Início
          </a>
          <a
            className="button button--primary"
            href="/login?callbackURL=/app"
          >
            Entrar no workspace
          </a>
        </div>
      </header>

      <section
        className="tenant-page-heading"
        style={{
          marginTop: "3rem",
        }}
      >
        <span className="section-kicker">
          Aprenda antes de operar
        </span>
        <h1>
          Demonstração curta e sem
          persistência.
        </h1>
        <p>
          O objetivo é mostrar a separação
          entre o CVSS-B publicado pela
          fonte e o contexto ambiental do
          consumidor. Para registrar
          projetos, ambientes e histórico,
          use o workspace autenticado.
        </p>
      </section>

      <div className="panel">
        <strong>
          Referência FIRST
        </strong>
        <p>
          O score Base mede severidade, não
          risco. A FIRST orienta consumidores
          a enriquecer a avaliação com dados
          do ativo e do ambiente quando
          aplicável.
        </p>
        <div
          style={{
            display: "flex",
            gap: ".75rem",
            flexWrap: "wrap",
          }}
        >
          <a
            className="button button--quiet"
            href="https://www.first.org/cvss/v4.0/user-guide"
            target="_blank"
            rel="noreferrer"
          >
            Guia FIRST ↗
          </a>
          <a
            className="button button--quiet"
            href="https://www.first.org/cvss/calculator/4.0"
            target="_blank"
            rel="noreferrer"
          >
            Calculadora FIRST ↗
          </a>
        </div>
      </div>

      <EnvironmentSimulator />
    </main>
  );
}
