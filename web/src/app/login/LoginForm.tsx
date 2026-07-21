"use client";

import type {
  FormEvent,
} from "react";
import { useRouter } from "next/navigation";
import { useState } from "react";

import {
  authClient,
} from "@/lib/auth-client";
import {
  normalizeEmail,
} from "@/lib/normalize-email";

export function LoginForm({
  callbackURL,
}: {
  callbackURL: string;
}) {
  const router = useRouter();

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [rememberMe, setRememberMe] =
    useState(true);

  const [pending, setPending] =
    useState(false);

  const [
    errorMessage,
    setErrorMessage,
  ] = useState("");

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (pending) {
      return;
    }

    setPending(true);
    setErrorMessage("");

    try {
      const result =
        await authClient.signIn.email({
          email: normalizeEmail(email),
          password,
          rememberMe,
        });

      if (result.error) {
        setErrorMessage(
          "Não foi possível autenticar com as credenciais informadas.",
        );

        return;
      }

      router.replace(callbackURL);
      router.refresh();
    } catch {
      setErrorMessage(
        "O serviço de autenticação não respondeu. Tente novamente.",
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <form
      className="auth-form"
      onSubmit={handleSubmit}
      noValidate
    >
      <div className="auth-field">
        <label htmlFor="auth-email">
          E-mail
        </label>

        <input
          id="auth-email"
          type="email"
          name="email"
          autoComplete="username"
          inputMode="email"
          value={email}
          onChange={(event) =>
            setEmail(event.target.value)
          }
          required
          disabled={pending}
        />
      </div>

      <div className="auth-field">
        <label htmlFor="auth-password">
          Senha
        </label>

        <input
          id="auth-password"
          type="password"
          name="password"
          autoComplete="current-password"
          minLength={12}
          maxLength={128}
          value={password}
          onChange={(event) =>
            setPassword(event.target.value)
          }
          required
          disabled={pending}
        />
      </div>

      <label className="auth-remember">
        <input
          type="checkbox"
          checked={rememberMe}
          onChange={(event) =>
            setRememberMe(
              event.target.checked,
            )
          }
          disabled={pending}
        />

        <span>
          Manter a sessão neste navegador
        </span>
      </label>

      {errorMessage ? (
        <p
          className="auth-error"
          role="alert"
          aria-live="polite"
        >
          {errorMessage}
        </p>
      ) : null}

      <button
        className={
          "button button--primary " +
          "auth-submit"
        }
        type="submit"
        disabled={pending}
      >
        {pending
          ? "Autenticando..."
          : "Entrar"}
      </button>
            <a
          className="login-help-link"
          href="/forgot-password"
        >
          Esqueci minha senha
        </a>
</form>
  );
}
