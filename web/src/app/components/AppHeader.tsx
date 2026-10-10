export function AppHeader() {
  return (
    <header className="site-header">
      <div className="site-header__inner">
        <a
          className="brand"
          href="#top"
          aria-label="HelpUS CVSS — início"
        >
          <img
            src="/helpus-logo.jpg"
            alt="Logo Oficial HelpUS"
            style={{
              width: "42px",
              height: "42px",
              borderRadius: "50%",
              objectFit: "cover",
              border: "2px solid #38bdf8",
              boxShadow: "0 0 12px rgba(56, 189, 248, 0.4)",
              background: "#081324",
            }}
          />

          <span className="brand__text">
            <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
              <strong style={{ fontSize: "17px", fontWeight: 800 }}>
                Help<span style={{ color: "#38bdf8" }}>US</span> CVSS
              </strong>
              <span
                style={{
                  fontSize: "10px",
                  fontWeight: 700,
                  textTransform: "uppercase",
                  background: "rgba(56, 189, 248, 0.15)",
                  color: "#38bdf8",
                  padding: "2px 7px",
                  borderRadius: "6px",
                  border: "1px solid rgba(56, 189, 248, 0.35)",
                  letterSpacing: "0.5px",
                }}
              >
                AI Watcher
              </span>
            </span>
            <small style={{ color: "#94a3b8", fontSize: "11px", fontWeight: 500 }}>
              Console Operacional • FIRST CVSS v4.0
            </small>
          </span>
        </a>

        <nav
          className="primary-nav"
          aria-label="Navegação principal"
        >
          <a href="#dashboard">Visão geral</a>
          <a href="#simulator">Simulador 5 Camadas</a>
          <a href="#methodology">Metodologia</a>
          <a
            href="https://cvss.helpusbr.com"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: "#38bdf8",
              display: "inline-flex",
              alignItems: "center",
              gap: "4px",
              fontWeight: 600,
              background: "rgba(56, 189, 248, 0.08)",
              padding: "4px 10px",
              borderRadius: "8px",
              border: "1px solid rgba(56, 189, 248, 0.25)",
            }}
          >
            🔬 Portal Científico & Topologia ↗
          </a>
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
