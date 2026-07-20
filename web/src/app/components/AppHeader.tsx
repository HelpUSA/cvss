export function AppHeader() {
  return (
    <header className="site-header">
      <div className="site-header__inner">
        <a
          className="brand"
          href="#top"
          aria-label="HelpUS CVSS — início"
        >
          <span
            className="brand__mark"
            aria-hidden="true"
          >
            H
          </span>

          <span className="brand__text">
            <strong>HelpUS CVSS</strong>
            <small>
              Contextual Risk Intelligence
            </small>
          </span>
        </a>

        <nav
          className="primary-nav"
          aria-label="Navegação principal"
        >
          <a href="#dashboard">Visão geral</a>
          <a href="#explorer">Explorador</a>
          <a href="#findings">Achados</a>
          <a href="#methodology">Metodologia</a>
          <a href="#evidence">Evidências</a>
        </nav>

        <a
          className="header-cta"
          href="/login"
        >
          Entrar
        </a>
      </div>
    </header>
  );
}
