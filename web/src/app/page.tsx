import type {
  Metadata,
} from "next";

export const metadata: Metadata = {
  title:
    "HelpUS CVSS — Contextualização Ambiental CVSS v4.0",
  description:
    "Fluxo guiado para contextualização ambiental CVSS v4.0 com cálculo determinístico, evidências rastreáveis e workspace multi-tenant.",
};

const steps = [
  {
    number: "01",
    title:
      "Parta do CVSS-B publicado",
    text:
      "Informe a CVE e o vetor CVSS v4.0 de origem. O score de origem é preservado e nunca é sobrescrito.",
    first:
      "Base Metrics / CVSS-B",
  },
  {
    number: "02",
    title:
      "Descreva o ambiente real",
    text:
      "Associe projeto, ambiente, alcance de rede, qualidade e atualidade das evidências e requisitos de segurança definidos pela organização.",
    first:
      "Environmental Metrics",
  },
  {
    number: "03",
    title:
      "Execute a avaliação",
    text:
      "O motor aplica regras versionadas e o cálculo determinístico. Quando a evidência não é suficiente, o fluxo pode ABSTAIN em vez de adivinhar.",
    first:
      "CVSS-BE / CVSS-BTE",
  },
  {
    number: "04",
    title:
      "Use o resultado operacional",
    text:
      "Compare score, vetor, evidências e histórico de execuções. A priorização local permanece separada do score CVSS.",
    first:
      "Consumer workflow",
  },
];

export default function Home() {
  return (
    <main
      className="page-shell"
      style={{
        paddingTop: "2rem",
      }}
    >
      <header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent:
            "space-between",
          gap: "1rem",
          flexWrap: "wrap",
          paddingBottom: "2rem",
        }}
      >
        <a
          className="brand"
          href="/"
          aria-label="HelpUS CVSS"
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
              FIRST CVSS v4.0 •
              Workspace operacional
            </small>
          </span>
        </a>

        <nav
          aria-label="Ações principais"
          style={{
            display: "flex",
            gap: ".75rem",
            flexWrap: "wrap",
          }}
        >
          <a
            className="button button--secondary"
            href="/demo"
          >
            Abrir demonstração
          </a>
          <a
            className="button button--primary"
            href="/login?callbackURL=/app"
          >
            Entrar no workspace
          </a>
        </nav>
      </header>

      <section
        className="hero-section"
        style={{
          minHeight: "auto",
          paddingTop: "3rem",
          paddingBottom: "3rem",
        }}
      >
        <div className="hero-section__content">
          <span className="hero-kicker">
            Fluxo guiado • CVSS v4.0
          </span>

          <h1>
            Do score de origem ao
            contexto do seu ambiente,
            <span>
              {" "}passo a passo.
            </span>
          </h1>

          <p className="hero-lead">
            A HelpUS organiza a
            contextualização ambiental em
            uma sequência prática:
            organização, projeto,
            ambiente, vulnerabilidade,
            evidências, execução e
            resultado. Menos informação
            por tela, mais orientação sobre
            o próximo passo.
          </p>

          <div className="hero-actions">
            <a
              className="button button--primary"
              href="/login?callbackURL=/app"
            >
              Começar no workspace
            </a>
            <a
              className="button button--secondary"
              href="/demo"
            >
              Testar sem persistência
            </a>
          </div>
        </div>

        <aside className="hero-context">
          <span className="section-kicker">
            Antes de começar
          </span>
          <h2>
            CVSS mede severidade.
          </h2>
          <p className="context-detail">
            O CVSS-B representa as
            características intrínsecas da
            vulnerabilidade. O contexto do
            consumidor é aplicado por meio
            das métricas ambientais. A
            política de priorização da
            organização fica separada do
            cálculo CVSS.
          </p>
          <div
            style={{
              display: "grid",
              gap: ".65rem",
              marginTop: "1rem",
            }}
          >
            <a
              className="button button--quiet"
              href="https://www.first.org/cvss/v4.0/user-guide"
              target="_blank"
              rel="noreferrer"
            >
              Guia oficial FIRST ↗
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
        </aside>
      </section>

      <section
        aria-labelledby="workflow-title"
        style={{
          marginTop: "2.5rem",
        }}
      >
        <div
          className="section-heading"
        >
          <div>
            <span className="section-kicker">
              Roteiro prático
            </span>
            <h2 id="workflow-title">
              Quatro etapas que seguem a
              lógica do consumidor CVSS.
            </h2>
          </div>
          <p>
            A FIRST recomenda enriquecer
            resultados de vulnerabilidade
            com informações do ativo e do
            ambiente. O workspace organiza
            essa tarefa sem misturar
            contexto local com o score de
            origem.
          </p>
        </div>

        <div
          className="methodology-grid"
          style={{
            gridTemplateColumns:
              "repeat(auto-fit, minmax(220px, 1fr))",
          }}
        >
          {steps.map((step) => (
            <article
              className="methodology-card"
              key={step.number}
            >
              <span className="methodology-card__number">
                {step.number}
              </span>
              <h3>{step.title}</h3>
              <p>{step.text}</p>
              <code>{step.first}</code>
            </article>
          ))}
        </div>
      </section>

      <section
        className="panel"
        style={{
          marginTop: "3rem",
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(260px, 1fr))",
          gap: "1rem",
        }}
      >
        <div>
          <span className="section-kicker">
            Demonstração pública
          </span>
          <h2>
            Quero apenas entender o
            cálculo.
          </h2>
          <p>
            Use uma execução stateless,
            sem criar histórico em uma
            organização.
          </p>
          <a
            className="button button--secondary"
            href="/demo"
          >
            Abrir demonstração
          </a>
        </div>

        <div>
          <span className="section-kicker">
            Uso real
          </span>
          <h2>
            Quero registrar avaliações da
            minha organização.
          </h2>
          <p>
            Entre com Google para manter
            projetos, ambientes,
            avaliações, evidências e
            execuções separados por
            organização.
          </p>
          <a
            className="button button--primary"
            href="/login?callbackURL=/app"
          >
            Entrar no workspace
          </a>
        </div>
      </section>

      <footer
        className="site-footer"
        style={{
          marginTop: "4rem",
        }}
      >
        <div className="site-footer__inner">
          <div>
            <strong>
              HelpUS CVSS
            </strong>
            <p>
              Contextualização ambiental
              CVSS v4.0 com evidência
              rastreável e cálculo
              determinístico.
            </p>
          </div>
          <small>
            CVSS é propriedade da FIRST.Org,
            Inc. e é utilizado com
            atribuição.
          </small>
        </div>
      </footer>
    </main>
  );
}
