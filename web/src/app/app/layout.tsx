import type {
  Metadata,
} from "next";
import type {
  ReactNode,
} from "react";

import {
  requireActiveSession,
} from "@/lib/session";

import {
  SignOutButton,
} from "./SignOutButton";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export const metadata: Metadata = {
  title: "Área operacional",

  robots: {
    index: false,
    follow: false,
  },
};

export default async function OperationalLayout({
  children,
}: {
  children: ReactNode;
}) {
  const currentSession =
    await requireActiveSession();

  const roleLabel =
    currentSession.user.platformRole ===
    "PLATFORM_ADMIN"
      ? "Administrador da plataforma"
      : "Usuário da plataforma";

  return (
    <div className="operational-shell">
      <header className="operational-header">
        <a className="auth-brand" href="/">
          <span aria-hidden="true">
            H
          </span>

          <span>
            <strong>HelpUS CVSS</strong>
            <small>Área operacional</small>
          </span>
        </a>

        <nav
          className="operational-nav"
          aria-label="Navegação operacional"
        >
          <a href="/app">Início</a>
          <a href="/">Painel público</a>
        </nav>

        <div className="operational-user">
          <div>
            <strong>
              {currentSession.user.name}
            </strong>

            <span>{roleLabel}</span>
          </div>

          <SignOutButton />
        </div>
      </header>

      <main className="operational-main">
        {children}
      </main>
    </div>
  );
}
