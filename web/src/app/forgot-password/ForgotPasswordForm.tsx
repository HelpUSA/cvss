"use client";

import {
  type FormEvent,
  useState,
} from "react";

export function ForgotPasswordForm() {
  const [email, setEmail] =
    useState("");

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  async function submit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setPending(true);
    setMessage("");

    try {
      await fetch(
        "/api/account/password-reset/request",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            email,
          }),
        },
      );

      setMessage(
        "Caso a conta esteja apta, as instruções serão enviadas por e-mail.",
      );
    } catch {
      setMessage(
        "Caso a conta esteja apta, as instruções serão enviadas por e-mail.",
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
        <label htmlFor="reset-email">
          E-mail
        </label>

        <input
          id="reset-email"
          type="email"
          value={email}
          onChange={(event) =>
            setEmail(
              event.target.value,
            )
          }
          maxLength={320}
          required
          autoComplete="email"
        />
      </div>

      <button
        className="button button--primary"
        type="submit"
        disabled={pending}
      >
        {pending
          ? "Enviando..."
          : "Solicitar redefinição"}
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
