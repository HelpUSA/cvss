export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="site-footer__inner">
        <div>
          <strong>HelpUS CVSS</strong>
          <p>
            Inteligência contextual para decisões de vulnerabilidade
            explicáveis e auditáveis.
          </p>
        </div>

        <nav aria-label="Navegação do rodapé">
          <a href="#dashboard">Visão geral</a>
          <a href="#explorer">Explorador</a>
          <a href="#methodology">Metodologia</a>
          <a href="#evidence">Evidências</a>
        </nav>

        <small>© 2026 HelpUS. Uso técnico e demonstrativo.</small>
      </div>
    </footer>
  );
}
