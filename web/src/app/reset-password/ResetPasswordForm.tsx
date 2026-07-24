"use client";

import {
  type FormEvent,
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

export function ResetPasswordForm({
  token,
}: {
  token: string;
}) {
  const router = useRouter();

  const [password, setPassword] =
    useState("");

  const [confirmation, setConfirmation] =
    useState("");

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  async function submit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setMessage("");

    if (password !== confirmation) {
      setMessage(
        "As senhas não coincidem.",
      );

      return;
    }

    setPending(true);

    try {
      const response = await fetch(
        "/api/account/password-reset/confirm",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            token,
            password,
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
            "O link é inválido ou expirou.",
        );
      }

      setMessage(
        "Senha redefinida. Todas as sessões anteriores foram encerradas.",
      );

      setTimeout(() => {
        router.push("/login");
      }, 800);
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Não foi possível redefinir a senha.",
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <form
      className="auth-lifecycle-form"
      onSubmit={submit}
    >
      <div className="field">
        <label htmlFor="new-password">
          Nova senha
        </label>

        <input
          id="new-password"
          type="password"
          value={password}
          onChange={(event) =>
            setPassword(
              event.target.value,
            )
          }
          minLength={12}
          maxLength={128}
          required
          autoComplete="new-password"
        />
      </div>

      <div className="field">
        <label htmlFor="confirm-password">
          Confirmar senha
        </label>

        <input
          id="confirm-password"
          type="password"
          value={confirmation}
          onChange={(event) =>
            setConfirmation(
              event.target.value,
            )
          }
          minLength={12}
          maxLength={128}
          required
          autoComplete="new-password"
        />
      </div>

      <button
        className="button button--primary"
        type="submit"
        disabled={pending}
      >
        {pending
          ? "Redefinindo..."
          : "Redefinir senha"}
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
