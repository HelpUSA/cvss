"use client";

import {
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

export function InvitationAcceptForm({
  token,
  userEmail,
}: {
  token: string;
  userEmail: string;
}) {
  const router = useRouter();

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  async function accept() {
    setPending(true);
    setMessage("");

    try {
      const response = await fetch(
        "/api/invitations/accept",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            token,
          }),
        },
      );

      const payload =
        await response
          .json()
          .catch(() => null);

      if (!response.ok) {
        throw new Error(
          payload?.message ??
            "O convite não pôde ser aceito.",
        );
      }

      setMessage(
        "Convite aceito com sucesso.",
      );

      router.push(
        `/app/${payload.organization.slug}`,
      );

      router.refresh();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Falha inesperada.",
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="auth-lifecycle-form">
      <p>
        Conta autenticada:{" "}
        <strong>{userEmail}</strong>
      </p>

      <button
        className="button button--primary"
        type="button"
        disabled={pending}
        onClick={accept}
      >
        {pending
          ? "Aceitando..."
          : "Aceitar convite"}
      </button>

      {message ? (
        <p
          className="management-feedback"
          role="status"
        >
          {message}
        </p>
      ) : null}
    </section>
  );
}
