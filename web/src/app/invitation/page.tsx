import type {
  Metadata,
} from "next";

import {
  getActiveSession,
} from "@/lib/session";
import {
  InvitationAcceptForm,
} from "./InvitationAcceptForm";

export const dynamic =
  "force-dynamic";

export const metadata: Metadata = {
  title:
    "Convite | CVSS",

  referrer:
    "no-referrer",

  robots: {
    index: false,
    follow: false,
  },
};

type InvitationSearchParams =
  Promise<
    Record<
      string,
      string |
      string[] |
      undefined
    >
  >;

export default async function InvitationPage({
  searchParams,
}: {
  searchParams:
    InvitationSearchParams;
}) {
  const resolved =
    await searchParams;

  const rawToken =
    resolved.token;

  const token =
    typeof rawToken === "string"
      ? rawToken
      : "";

  const currentSession =
    await getActiveSession();

  return (
    <main className="auth-lifecycle-page">
      <span className="section-kicker">
        Convite organizacional
      </span>

      <h1>
        Aceitar convite
      </h1>

      {!token ? (
        <section className="tenant-empty-state">
          <h2>
            Convite inválido.
          </h2>
        </section>
      ) : !currentSession ? (
        <section className="tenant-empty-state">
          <h2>
            Entre na conta convidada.
          </h2>

          <p>
            Depois do login, abra novamente
            o endereço recebido por e-mail.
          </p>

          <a
            className="button button--primary"
            href="/login"
          >
            Entrar
          </a>
        </section>
      ) : (
        <InvitationAcceptForm
          token={token}
          userEmail={
            currentSession.user.email
          }
        />
      )}
    </main>
  );
}
