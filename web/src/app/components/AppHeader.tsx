"use client";

import { useEffect, useState } from "react";

export function AppHeader() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Close mobile menu when Escape key is pressed
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        setMobileMenuOpen(false);
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Prevent background scrolling when mobile menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileMenuOpen]);

  const closeMenu = () => setMobileMenuOpen(false);

  return (
    <header className="site-header">
      <div className="site-header__inner">
        <a
          className="brand"
          href="#top"
          aria-label="HelpUS CVSS — início"
          onClick={closeMenu}
        >
          <img
            src="/helpus-logo.jpg"
            alt="Logo Oficial HelpUS"
            className="brand__logo-img"
          />

          <span className="brand__text">
            <span className="brand__title-row">
              <strong className="brand__title">
                Help<span style={{ color: "#38bdf8" }}>US</span> CVSS
              </strong>
              <span className="brand__ai-badge">
                AI Watcher
              </span>
            </span>
            <small className="brand__subtitle">
              Console Operacional • FIRST CVSS v4.0
            </small>
          </span>
        </a>

        {/* Desktop Navigation */}
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

        {/* Desktop CTA */}
        <a
          className="header-cta desktop-only-cta"
          href="/login"
        >
          Entrar
        </a>

        {/* Mobile Hamburger Button (Os três tracinhos) */}
        <button
          type="button"
          className={`hamburger-btn ${mobileMenuOpen ? "is-active" : ""}`}
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-expanded={mobileMenuOpen}
          aria-label={mobileMenuOpen ? "Fechar menu" : "Abrir menu de navegação"}
        >
          <span className="hamburger-line line-1" />
          <span className="hamburger-line line-2" />
          <span className="hamburger-line line-3" />
        </button>
      </div>

      {/* Mobile Drawer Overlay */}
      {mobileMenuOpen && (
        <div
          className="mobile-menu-overlay"
          onClick={closeMenu}
          aria-hidden="true"
        />
      )}

      {/* Mobile Drawer Menu */}
      <div
        className={`mobile-menu-drawer ${mobileMenuOpen ? "is-open" : ""}`}
        aria-label="Navegação móvel"
      >
        <nav className="mobile-nav">
          <a href="#dashboard" onClick={closeMenu} className="mobile-nav__link">
            <span className="mobile-nav__icon">📊</span>
            <span>Visão geral</span>
          </a>
          <a href="#simulator" onClick={closeMenu} className="mobile-nav__link">
            <span className="mobile-nav__icon">⚡</span>
            <span>Simulador 5 Camadas</span>
          </a>
          <a href="#methodology" onClick={closeMenu} className="mobile-nav__link">
            <span className="mobile-nav__icon">📐</span>
            <span>Metodologia</span>
          </a>
          <a
            href="https://cvss.helpusbr.com"
            target="_blank"
            rel="noopener noreferrer"
            onClick={closeMenu}
            className="mobile-nav__link mobile-nav__link--external"
          >
            <span className="mobile-nav__icon">🔬</span>
            <span>Portal Científico ↗</span>
          </a>

          <div className="mobile-nav__footer">
            <a
              className="mobile-nav__cta"
              href="/login"
              onClick={closeMenu}
            >
              🔐 Entrar no Console
            </a>
          </div>
        </nav>
      </div>
    </header>
  );
}
