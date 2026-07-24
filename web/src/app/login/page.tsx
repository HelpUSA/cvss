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
          <a className="auth-brand" href="/">
            <span aria-hidden="true">
              H
            </span>

            <strong>HelpUS CVSS</strong>
          </a>

          <span className="section-kicker">
            Área operacional
          </span>

          <h1>
            Contexto, evidências e decisões
            com acesso seguro.
          </h1>

          <p>
            A autenticação protege a fundação
            multiusuário sem misturar o CVSS
            oficial com a priorização contextual.
          </p>

          <ul className="auth-principles">
            <li>
              Sessões persistidas no PostgreSQL
            </li>

            <li>
              Senhas protegidas com Argon2id
            </li>

            <li>
              Registro público desabilitado
            </li>

            <li>
              Validação autoritativa no servidor
            </li>
          </ul>
        </div>

        <div className="auth-panel">
          <div className="auth-panel__heading">
            <span className="section-kicker">
              Acesso seguro
            </span>

            <h2>Entrar na plataforma</h2>

            <p>
              Use uma conta provisionada pelo
              administrador.
            </p>
          </div>

          {reason === "session-required" ? (
            <p
              className="auth-notice"
              role="status"
            >
              Entre para acessar a área
              solicitada.
            </p>
          ) : null}

          <LoginForm
            callbackURL={callbackURL}
          />

          <a
            className="auth-back-link"
            href="/"
          >
            Voltar ao painel público
          </a>
        </div>
      </section>
    </main>
  );
}
