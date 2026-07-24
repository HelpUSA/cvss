"use client";

import {
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

type SessionItem = {
  id: string;
  createdAt: string;
  updatedAt: string;
  expiresAt: string;
  ipAddress: string | null;
  userAgent: string | null;
  current: boolean;
};

export function SessionControls({
  sessions,
}: {
  sessions: SessionItem[];
}) {
  const router = useRouter();

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  async function execute(
    url: string,
    method: "POST" | "DELETE",
  ) {
    setPending(true);
    setMessage("");

    try {
      const response = await fetch(
        url,
        {
          method,

          headers: {
            "Content-Type":
              "application/json",
          },

          body: "{}",
        },
      );

      const payload =
        await response
          .json()
          .catch(() => null);

      if (!response.ok) {
        throw new Error(
          payload?.message ??
            "A operação não pôde ser concluída.",
        );
      }

      if (
        payload?.revokedCurrent ||
        url.endsWith("/revoke-all")
      ) {
        window.location.href =
          "/login";

        return;
      }

      setMessage(
        "Sessões atualizadas.",
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
    <>
      <div className="session-actions">
        <button
          className="button button--secondary"
          type="button"
          disabled={pending}
          onClick={() =>
            execute(
              "/api/account/sessions/revoke-others",
              "POST",
            )
          }
        >
          Encerrar outras sessões
        </button>

        <button
          className="button button--secondary"
          type="button"
          disabled={pending}
          onClick={() =>
            execute(
              "/api/account/sessions/revoke-all",
              "POST",
            )
          }
        >
          Encerrar todas
        </button>
      </div>

      {message ? (
        <p
          className="management-feedback"
          role="status"
        >
          {message}
        </p>
      ) : null}

      <section className="session-list">
        {sessions.map((session) => (
          <article
            className="session-card"
            key={session.id}
          >
            <div>
              <strong>
                {session.current
                  ? "Sessão atual"
                  : "Sessão ativa"}
              </strong>

              <span>
                {session.ipAddress ??
                  "IP não informado"}
              </span>

              <small>
                Atualizada em{" "}
                {new Date(
                  session.updatedAt,
                ).toLocaleString()}
              </small>

              <small>
                {session.userAgent ??
                  "Navegador não informado"}
              </small>
            </div>

            <button
              className="button button--secondary"
              type="button"
              disabled={pending}
              onClick={() =>
                execute(
                  `/api/account/sessions/${encodeURIComponent(
                    session.id,
                  )}`,
                  "DELETE",
                )
              }
            >
              Encerrar
            </button>
          </article>
        ))}
      </section>
    </>
  );
}
