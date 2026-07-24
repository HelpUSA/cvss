import type {
  Metadata,
} from "next";

import {
  ResetPasswordForm,
} from "./ResetPasswordForm";

export const dynamic =
  "force-dynamic";

export const metadata: Metadata = {
  title:
    "Nova senha | CVSS",

  referrer:
    "no-referrer",

  robots: {
    index: false,
    follow: false,
  },
};

type ResetPasswordSearchParams =
  Promise<
    Record<
      string,
      string |
      string[] |
      undefined
    >
  >;

export default async function ResetPasswordPage({
  searchParams,
}: {
  searchParams:
    ResetPasswordSearchParams;
}) {
  const resolved =
    await searchParams;

  const rawToken =
    resolved.token;

  const token =
    typeof rawToken === "string"
      ? rawToken
      : "";

  return (
    <main className="auth-lifecycle-page">
      <a
        className="tenant-back-link"
        href="/login"
      >
        ← Voltar ao login
      </a>

      <span className="section-kicker">
        Segurança da conta
      </span>

      <h1>
        Defina uma nova senha
      </h1>

      {token ? (
        <>
          <p>
            O link será invalidado após o uso.
            Todas as sessões existentes serão
            encerradas.
          </p>

          <ResetPasswordForm
            token={token}
          />
        </>
      ) : (
        <section className="tenant-empty-state">
          <h2>
            Link inválido.
          </h2>

          <a
            className="button button--primary"
            href="/forgot-password"
          >
            Solicitar novo link
          </a>
        </section>
      )}
    </main>
  );
}
