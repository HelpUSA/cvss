"use client";

import {
  type FormEvent,
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

const ROLES = [
  "ADMIN",
  "OPERATOR",
  "REVIEWER",
  "VIEWER",
] as const;

type InvitationItem = {
  id: string;
  email: string;
  role:
    (typeof ROLES)[number];
  expiresAt: string;
  createdAt: string;
  createdByName: string;
};

export function InvitationsPanel({
  organizationSlug,
  initialInvitations,
}: {
  organizationSlug: string;
  initialInvitations:
    InvitationItem[];
}) {
  const router = useRouter();

  const [email, setEmail] =
    useState("");

  const [role, setRole] =
    useState<
      (typeof ROLES)[number]
    >("VIEWER");

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  async function createInvitation(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setPending(true);
    setMessage("");

    try {
      const response = await fetch(
        `/api/organizations/${encodeURIComponent(
          organizationSlug,
        )}/invitations`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            email,
            role,
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
            "O convite não pôde ser enviado.",
        );
      }

      setEmail("");
      setRole("VIEWER");

      setMessage(
        "Convite enviado com sucesso.",
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

  async function revokeInvitation(
    invitationId: string,
  ) {
    setPending(true);
    setMessage("");

    try {
      const response = await fetch(
        `/api/organizations/${encodeURIComponent(
          organizationSlug,
        )}/invitations/${encodeURIComponent(
          invitationId,
        )}`,
        {
          method: "DELETE",

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
            "O convite não pôde ser revogado.",
        );
      }

      setMessage(
        "Convite revogado.",
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
    <section className="invitation-panel">
      <div>
        <span className="section-kicker">
          Convites
        </span>

        <h2>
          Convidar usuário
        </h2>

        <p>
          A aceitação exige uma conta ativa
          com o mesmo endereço de e-mail.
        </p>
      </div>

      <form
        className="management-form management-form--inline"
        onSubmit={createInvitation}
      >
        <div className="field">
          <label htmlFor="invitation-email">
            E-mail
          </label>

          <input
            id="invitation-email"
            type="email"
            value={email}
            onChange={(event) =>
              setEmail(
                event.target.value,
              )
            }
            maxLength={320}
            required
          />
        </div>

        <div className="field">
          <label htmlFor="invitation-role">
            Papel
          </label>

          <select
            id="invitation-role"
            value={role}
            onChange={(event) =>
              setRole(
                event.target.value as
                  (typeof ROLES)[number],
              )
            }
          >
            {ROLES.map((value) => (
              <option
                value={value}
                key={value}
              >
                {value}
              </option>
            ))}
          </select>
        </div>

        <button
          className="button button--primary"
          type="submit"
          disabled={pending}
        >
          {pending
            ? "Enviando..."
            : "Enviar convite"}
        </button>
      </form>

      {message ? (
        <p
          className="management-feedback"
          role="status"
        >
          {message}
        </p>
      ) : null}

      {initialInvitations.length > 0 ? (
        <div className="invitation-list">
          {initialInvitations.map(
            (invitation) => (
              <article
                className="invitation-card"
                key={invitation.id}
              >
                <div>
                  <strong>
                    {invitation.email}
                  </strong>

                  <span>
                    {invitation.role}
                  </span>

                  <small>
                    Expira em{" "}
                    {new Date(
                      invitation.expiresAt,
                    ).toLocaleString()}
                  </small>
                </div>

                <button
                  className="button button--secondary"
                  type="button"
                  disabled={pending}
                  onClick={() =>
                    revokeInvitation(
                      invitation.id,
                    )
                  }
                >
                  Revogar
                </button>
              </article>
            ),
          )}
        </div>
      ) : (
        <p className="tenant-muted-copy">
          Nenhum convite pendente.
        </p>
      )}
    </section>
  );
}
