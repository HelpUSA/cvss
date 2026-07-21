import type {
  Metadata,
} from "next";

import {
  ForgotPasswordForm,
} from "./ForgotPasswordForm";

export const metadata: Metadata = {
  title:
    "Redefinir senha | CVSS",

  robots: {
    index: false,
    follow: false,
  },
};

export default function ForgotPasswordPage() {
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
        Redefinir senha
      </h1>

      <p>
        Informe o e-mail da conta. A resposta
        será sempre a mesma, exista ou não uma
        conta elegível.
      </p>

      <ForgotPasswordForm />
    </main>
  );
}
