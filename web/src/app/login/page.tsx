import type { Metadata } from "next";
import { redirect } from "next/navigation";

import {
  getActiveSession,
} from "@/lib/session";

import { LoginForm } from "./LoginForm";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export const metadata: Metadata = {
  title: "Entrar",

  description:
    "Acesso autenticado à área operacional da plataforma HelpUS CVSS.",

  robots: {
    index: false,
    follow: false,
  },
};

type LoginSearchParams = Promise<{
  callbackURL?: string | string[];
  reason?: string | string[];
}>;

function firstValue(
  value: string | string[] | undefined,
): string | undefined {
  return Array.isArray(value)
    ? value[0]
    : value;
}

function safeCallbackUrl(
  value: string | undefined,
): string {
  if (
    value &&
    value.startsWith("/app") &&
    !value.startsWith("//")
  ) {
    return value;
  }

  return "/app";
}

export default async function LoginPage({
  searchParams,
}: {
  searchParams: LoginSearchParams;
}) {
  const existingSession =
    await getActiveSession();

  if (existingSession) {
    redirect("/app");
  }

  const resolvedSearchParams =
    await searchParams;

  const callbackURL = safeCallbackUrl(
    firstValue(
      resolvedSearchParams.callbackURL,
    ),
  );

  const reason = firstValue(
    resolvedSearchParams.reason,
  );

  return (
    <main className="auth-page">
      <section className="auth-shell">
        <div className="auth-introduction">
          <a className="auth-brand" href="/" style={{ display: "flex", alignItems: "center", gap: "12px", textDecoration: "none" }}>
            <img
              src="/helpus-logo.jpg"
              alt="Logo Oficial HelpUS"
              style={{
                width: "44px",
                height: "44px",
                borderRadius: "50%",
                objectFit: "cover",
                border: "2px solid #38bdf8",
                boxShadow: "0 0 12px rgba(56, 189, 248, 0.4)",
                background: "#081324",
              }}
            />
            <div>
              <strong style={{ fontSize: "18px", color: "#ffffff", display: "flex", alignItems: "center", gap: "6px" }}>
                Help<span style={{ color: "#38bdf8" }}>US</span> CVSS
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
                  }}
                >
                  AI Watcher
                </span>
              </strong>
              <small style={{ color: "#94a3b8", fontSize: "11px", display: "block" }}>
                Console Operacional • FIRST CVSS v4.0
              </small>
            </div>
          </a>

          <span className="section-kicker">
            Área Operacional Corporativa
          </span>

          <h1>
            Contexto, evidências e decisões com acesso seguro.
          </h1>

          <p>
            Plataforma unificada de priorização com motor determinístico, recibos de proveniência RFC 8785 e governança supervisionada pelo SuperAdmin.
          </p>

          <div style={{ marginTop: "16px", marginBottom: "20px" }}>
            <a
              href="https://cvss.helpusbr.com"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "8px 16px",
                borderRadius: "10px",
                background: "rgba(56, 189, 248, 0.1)",
                border: "1px solid rgba(56, 189, 248, 0.3)",
                color: "#38bdf8",
                fontSize: "12px",
                fontWeight: 700,
                textDecoration: "none",
              }}
            >
              <span>🔬</span> Acessar Portal Científico & Demonstrador Público ↗
            </a>
          </div>

          <ul className="auth-principles">
            <li>
              Autenticação unificada Google SSO ou credenciais
            </li>

            <li>
              Sessões auditadas e governança Human-in-the-Loop
            </li>

            <li>
              Recibos criptográficos com hash RFC 8785 SHA-256
            </li>

            <li>
              Conexão com telemetria e controles de rede em tempo real
            </li>
          </ul>
        </div>

        <div className="auth-panel">
          <div className="auth-panel__heading">
            <span className="section-kicker">
              Acesso Seguro
            </span>

            <h2>Entrar na Plataforma</h2>

            <p>
              Use sua conta Google corporativa ou credenciais autorizadas.
            </p>
          </div>

          {reason === "session-required" ? (
            <p
              className="auth-notice"
              role="status"
            >
              Entre para acessar a área solicitada.
            </p>
          ) : null}

          <LoginForm
            callbackURL={callbackURL}
          />

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "16px", fontSize: "12px" }}>
            <a
              className="auth-back-link"
              href="/"
              style={{ color: "#94a3b8" }}
            >
              ← Painel Operacional
            </a>
            <a
              href="https://cvss.helpusbr.com"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: "#38bdf8", fontWeight: 600, textDecoration: "none" }}
            >
              Portal Científico ↗
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}
