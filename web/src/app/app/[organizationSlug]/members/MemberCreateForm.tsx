"use client";

import {
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

export function MemberCreateForm({
  organizationSlug,
}: {
  organizationSlug: string;
}) {
  const router = useRouter();

  const [email, setEmail] =
    useState("");

  const [role, setRole] =
    useState<(typeof ROLES)[number]>(
      "VIEWER",
    );

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  async function submit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setPending(true);
    setMessage("");

    try {
      const response = await fetch(
        `/api/organizations/${encodeURIComponent(
          organizationSlug,
        )}/memberships`,
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
            "A membership não pôde ser criada.",
        );
      }

      setEmail("");
      setRole("VIEWER");
      setMessage(
        "Membership criada com sucesso.",
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
    <form
      className="management-form management-form--inline"
      onSubmit={submit}
    >
      <div className="field">
        <label htmlFor="member-email">
          Usuário existente
        </label>

        <input
          id="member-email"
          type="email"
          value={email}
          onChange={(event) =>
            setEmail(event.target.value)
          }
          maxLength={320}
          placeholder="usuario@empresa.com"
          required
          autoComplete="email"
        />
      </div>

      <div className="field">
        <label htmlFor="member-role">
          Papel
        </label>

        <select
          id="member-role"
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
          ? "Adicionando..."
          : "Adicionar membro"}
      </button>

      {message ? (
        <p
          className="management-feedback"
          role="status"
        >
          {message}
        </p>
      ) : null}
    </form>
  );
}
